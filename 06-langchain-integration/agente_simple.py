"""
Agente LangGraph simple que usa herramientas MCP.
Demuestra la integración completa de MCP con LangGraph.
"""

import asyncio
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv

load_dotenv()

async def crear_agente_matematico():
    """Crea un agente que puede realizar operaciones matemáticas via MCP"""
    
    print("=" * 60)
    print("Inicializando Agente Matemático con MCP")
    print("=" * 60 + "\n")
    
    # 1. Conectar con servidor MCP
    print("1. Conectando con servidor MCP de matemáticas...")
    client = MultiServerMCPClient({
        "math": {
            "transport": "streamable_http",
            "url": "http://localhost:8001/mcp"
        }
    })
    
    tools = await client.get_tools()
    print(f"   ✅ {len(tools)} herramientas descubiertas\n")
    
    # 2. Configurar LLM
    print("2. Configurando modelo de lenguaje...")
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("Se requiere GOOGLE_API_KEY en el archivo .env")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0)
    llm_with_tools = llm.bind_tools(tools)
    print("   ✅ Modelo configurado\n")
    
    # 3. Construir grafo
    print("3. Construyendo grafo de conversación...")
    
    system_message = SystemMessage(
        content="""Eres un asistente matemático que puede realizar operaciones básicas.

INSTRUCCIONES:
- Puedes sumar, restar, multiplicar y dividir números
- Usa las herramientas disponibles para los cálculos
- Explica el resultado de forma clara
- Si te piden operaciones complejas, descompónlas en pasos simples
"""
    )
    
    def assistant_node(state: MessagesState):
        messages = [system_message] + state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant_node)
    builder.add_node("tools", ToolNode(tools))
    
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")
    
    graph = builder.compile()
    print("   ✅ Grafo creado\n")
    
    return graph

async def probar_agente(graph):
    """Prueba el agente con varias preguntas"""
    
    print("=" * 60)
    print("Probando el Agente")
    print("=" * 60 + "\n")
    
    preguntas = [
        "¿Cuánto es 25 + 17?",
        "Si tengo 100 y gasto 35, ¿cuánto me queda?",
        "¿Cuál es el resultado de 8 multiplicado por 7?",
    ]
    
    for i, pregunta in enumerate(preguntas, 1):
        print(f"\n{'─' * 60}")
        print(f"Pregunta {i}: {pregunta}")
        print('─' * 60)
        
        try:
            result = await graph.ainvoke({
                "messages": [HumanMessage(content=pregunta)]
            })
            
            # Extraer respuesta del asistente
            respuesta = None
            for msg in reversed(result["messages"]):
                if hasattr(msg, 'type') and msg.type == 'ai' and msg.content:
                    respuesta = msg.content
                    break
            
            if respuesta:
                print(f"\n🤖 Respuesta: {respuesta}")
            else:
                print("\n⚠️  No se obtuvo respuesta")
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    print("\n" + "=" * 60)

async def main():
    """Función principal"""
    try:
        graph = await crear_agente_matematico()
        await probar_agente(graph)
        
        print("\n✅ Demo completada exitosamente")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nVerifica que:")
        print("1. El servidor MCP esté corriendo (python 02-fastmcp-basico/servidor_math.py)")
        print("2. Tengas GOOGLE_API_KEY configurada en .env")

if __name__ == "__main__":
    asyncio.run(main())
