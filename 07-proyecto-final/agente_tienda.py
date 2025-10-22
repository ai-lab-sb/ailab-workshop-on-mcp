"""
Agente LangGraph que consume servidor MCP de tienda.
Especializado en consultas sobre productos y clientes con memoria de conversación.
"""

import os
from typing import List, Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv

load_dotenv()


class AgenteТienda:
    """
    Agente especializado en consultas de tienda que utiliza MCP tools.
    Mantiene memoria de conversación y solo responde preguntas sobre productos/clientes.
    """
    
    def __init__(self, google_api_key: str = None, mcp_server_url: str = "http://localhost:8200/mcp"):
        """
        Inicializa el agente de tienda.
        
        Args:
            google_api_key: API key de Google para Gemini
            mcp_server_url: URL del servidor MCP de tienda
        """
        if google_api_key:
            os.environ["GOOGLE_API_KEY"] = google_api_key
        elif not os.environ.get("GOOGLE_API_KEY"):
            raise ValueError("Se requiere GOOGLE_API_KEY en el archivo .env")
        
        self.mcp_server_url = mcp_server_url
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0)
        self.memory = MemorySaver()
        self._tools = None
        self._graph = None
        
        self.system_message = SystemMessage(
            content="""Eres un asistente especializado en consultas de tienda que SOLO puede responder preguntas sobre productos y clientes de nuestra tienda.

INSTRUCCIONES IMPORTANTES:
- SOLO responde preguntas sobre productos y clientes de la tienda
- Si te preguntan sobre cualquier otro tema, responde: "Lo siento, solo puedo ayudar con consultas sobre productos y clientes de nuestra tienda."
- Usa las herramientas disponibles para consultar la base de datos
- Proporciona respuestas claras, organizadas y amigables
- Si necesitas hacer múltiples consultas, hazlas en orden lógico
- Siempre verifica los datos antes de responder
- Puedes ayudar con:
  * Buscar productos por nombre, categoría o rango de precios
  * Consultar información de clientes
  * Verificar stock de productos
  * Buscar clientes por ciudad
  * Mostrar listas completas de productos o clientes
  * Recomendar productos según necesidades

FORMATO DE RESPUESTAS:
- Sé conciso pero completo
- Usa listas cuando muestres múltiples items
- Incluye precios con formato claro ($XXX.XX)
- Menciona stock disponible cuando sea relevante
"""
        )
    
    async def _initialize_tools(self):
        """Inicializa las herramientas MCP si no están ya cargadas"""
        if self._tools is None:
            client = MultiServerMCPClient({
                "tienda": {
                    "transport": "streamable_http",
                    "url": self.mcp_server_url
                }
            })
            self._tools = await client.get_tools()
    
    async def _build_graph(self):
        """Construye el grafo de conversación"""
        await self._initialize_tools()
        
        llm_with_tools = self.llm.bind_tools(self._tools)
        
        def assistant_node(state: MessagesState) -> Dict[str, List[BaseMessage]]:
            messages = [self.system_message] + state["messages"]
            response = llm_with_tools.invoke(messages)
            return {"messages": [response]}
        
        builder = StateGraph(MessagesState)
        builder.add_node("assistant", assistant_node)
        builder.add_node("tools", ToolNode(self._tools))
        
        builder.add_edge(START, "assistant")
        builder.add_conditional_edges("assistant", tools_condition)
        builder.add_edge("tools", "assistant")
        
        self._graph = builder.compile(checkpointer=self.memory)
    
    async def chat(self, message: str, thread_id: str = "default") -> Dict[str, Any]:
        """
        Procesa un mensaje del usuario.
        
        Args:
            message: Mensaje del usuario
            thread_id: ID del hilo de conversación
            
        Returns:
            Respuesta del agente con metadatos
        """
        if self._graph is None:
            await self._build_graph()
        
        config = {"configurable": {"thread_id": thread_id}}
        human_message = HumanMessage(content=message)
        
        result = await self._graph.ainvoke({"messages": [human_message]}, config)
        
        # Extraer la última respuesta del asistente
        last_ai_message = None
        for msg in reversed(result["messages"]):
            if hasattr(msg, 'type') and msg.type == 'ai':
                last_ai_message = msg
                break
        
        response = {
            "response": last_ai_message.content if last_ai_message else "No se pudo generar respuesta",
            "thread_id": thread_id,
            "tools_used": []
        }
        
        # Identificar herramientas utilizadas
        for msg in result["messages"]:
            if hasattr(msg, 'type') and msg.type == 'ai' and hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    response["tools_used"].append({
                        "name": tool_call["name"],
                        "args": tool_call["args"]
                    })
        
        return response
    
    async def get_conversation_history(self, thread_id: str = "default") -> List[Dict[str, Any]]:
        """
        Obtiene el historial de conversación de un thread.
        
        Args:
            thread_id: ID del hilo de conversación
            
        Returns:
            Lista de mensajes del historial
        """
        if self._graph is None:
            await self._build_graph()
            
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            state = self._graph.get_state(config)
            
            if not state.values or "messages" not in state.values:
                return []
            
            history = []
            for msg in state.values["messages"]:
                if hasattr(msg, 'type') and msg.type in ['human', 'ai']:
                    msg_dict = {
                        "type": msg.type,
                        "content": msg.content
                    }
                    history.append(msg_dict)
            
            return history
        
        except Exception:
            return []


async def demo():
    """Función de demostración del agente"""
    print("=" * 60)
    print("Demo: Agente de Tienda con MCP")
    print("=" * 60 + "\n")
    
    try:
        agente = AgenteТienda()
        print("✅ Agente inicializado\n")
        
        preguntas = [
            "¿Qué productos tienes disponibles?",
            "Muéstrame los productos de Electrónica",
            "¿Qué productos cuestan menos de $100?",
            "¿Cuántos clientes tengo en Bogotá?"
        ]
        
        for i, pregunta in enumerate(preguntas, 1):
            print(f"\n{'─' * 60}")
            print(f"Pregunta {i}: {pregunta}")
            print('─' * 60)
            
            respuesta = await agente.chat(pregunta, thread_id="demo")
            
            print(f"\n🤖 Respuesta:\n{respuesta['response']}")
            
            if respuesta['tools_used']:
                print(f"\n🔧 Herramientas usadas:")
                for tool in respuesta['tools_used']:
                    print(f"   • {tool['name']}")
        
        print("\n" + "=" * 60)
        print("✅ Demo completada")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nVerifica que:")
        print("1. El servidor MCP esté corriendo (python servidor_tienda.py)")
        print("2. Tengas GOOGLE_API_KEY configurada en .env")


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo())
