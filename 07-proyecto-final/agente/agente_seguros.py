"""
Agente LangGraph que consume el servidor MCP de seguros.
Utiliza langchain-mcp-adapters para conectarse al servidor y responder consultas sobre pólizas y clientes.
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

class AgenteSeguro:
    def __init__(self, mcp_server_url: str = "http://localhost:8200/mcp"):
        """
        Args:
            mcp_server_url: URL del servidor MCP de seguros
        """
        self.mcp_server_url = mcp_server_url
        self.llm = None
        self.graph = None
        self.tools = None
        self._initialized = False
    
    async def initialize(self):
        """Inicializa el cliente MCP y el grafo (debe llamarse después de crear la instancia)"""
        if not self._initialized:
            await self._setup_client()
            await self._setup_graph()
            self._initialized = True
    
    async def _setup_client(self):
        """Configura el cliente MCP y el modelo LLM con las herramientas"""
        self.client = MultiServerMCPClient(
            {"aseguradora": {"url": self.mcp_server_url, "transport": "streamable_http"}}
        )
        
        self.tools = await self.client.get_tools()
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.3
        ).bind_tools(self.tools)
    
    async def _setup_graph(self):
        """Configura el grafo de LangGraph con el agente y las herramientas"""
        tool_node = ToolNode(tools=self.tools)
        
        def call_model(state: MessagesState) -> Dict[str, Any]:
            messages = state["messages"]
            system_message = {
                "role": "system",
                "content": """Eres un asistente experto de una aseguradora. Tu objetivo es ayudar a los clientes 
a consultar información sobre sus pólizas, productos de seguros disponibles y datos de clientes.

Capacidades:
- Consultar todas las pólizas activas
- Buscar pólizas específicas por ID
- Ver todas las pólizas de un cliente
- Filtrar pólizas por tipo de seguro (Vida, Auto, Hogar, Salud, Accidentes)
- Consultar productos de seguros disponibles con sus coberturas
- Ver información de clientes asegurados
- Buscar clientes por ciudad

Siempre sé profesional, claro y conciso. Cuando presentes información de pólizas, incluye:
- Número de póliza
- Cliente
- Tipo de seguro
- Prima mensual
- Monto de cobertura
- Fechas de vigencia

Si no encuentras información, sugiere alternativas de búsqueda."""
            }
            response = self.llm.invoke([system_message] + messages)
            return {"messages": [response]}
        
        workflow = StateGraph(MessagesState)
        workflow.add_node("agent", call_model)
        workflow.add_node("tools", tool_node)
        
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges("agent", tools_condition)
        workflow.add_edge("tools", "agent")
        
        memory = MemorySaver()
        self.graph = workflow.compile(checkpointer=memory)
    
    async def chat(self, message: str, thread_id: str = "default") -> str:
        """
        Envía un mensaje al agente y obtiene la respuesta.
        
        Args:
            message: Mensaje del usuario
            thread_id: ID del hilo de conversación para mantener contexto
            
        Returns:
            Respuesta del agente
        """
        if not self._initialized:
            await self.initialize()
            
        response = await self.graph.ainvoke(
            {"messages": [{"role": "user", "content": message}]},
            config={"configurable": {"thread_id": thread_id}}
        )
        return response["messages"][-1].content
    
    def get_history(self, thread_id: str = "default") -> List[Dict[str, str]]:
        """
        Obtiene el historial de conversación de un hilo.
        
        Args:
            thread_id: ID del hilo de conversación
            
        Returns:
            Lista de mensajes con rol y contenido
        """
        state = self.graph.get_state(config={"configurable": {"thread_id": thread_id}})
        
        if state and state.values.get("messages"):
            return [
                {
                    "role": msg.type if hasattr(msg, "type") else "unknown",
                    "content": msg.content
                }
                for msg in state.values["messages"]
            ]
        return []
