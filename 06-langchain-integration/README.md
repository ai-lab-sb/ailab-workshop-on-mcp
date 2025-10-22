# Módulo 6: Integración con LangChain

## LangChain MCP Adapters

En este módulo aprenderás a conectar servidores MCP con agentes LangGraph usando **langchain-mcp-adapters**, una biblioteca que convierte herramientas MCP en herramientas LangChain.

## ¿Qué son los MCP Adapters?

**langchain-mcp-adapters** es un puente entre MCP y LangChain que:

1. **Descubre** herramientas disponibles en servidores MCP
2. **Convierte** herramientas MCP a formato LangChain Tool
3. **Permite** que agentes LangGraph las usen transparentemente

### Arquitectura

```
┌──────────────┐         ┌─────────────────┐         ┌──────────────┐
│   Servidor   │ ◄─MCP──►│  MCP Adapters   │ ◄─────► │   Agente     │
│     MCP      │         │  (langchain-    │         │  LangGraph   │
│              │         │   mcp-adapters) │         │              │
└──────────────┘         └─────────────────┘         └──────────────┘
   (FastMCP)              (Adaptador)                  (LangGraph)
```

## Instalación

```bash
pip install langchain-mcp-adapters
```

Esta biblioteca maneja:
- Comunicación con servidores MCP via HTTP
- Conversión de esquemas de herramientas
- Invocación de herramientas remotas
- Manejo de errores y timeouts

## Cliente MCP Básico

### Configuración Simple

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient({
    "math": {
        "transport": "streamable_http",
        "url": "http://localhost:8001/mcp"
    }
})

tools = await client.get_tools()
```

Esto conecta con el servidor MCP de matemáticas y obtiene todas sus herramientas.

### Configuración Multi-Servidor

```python
client = MultiServerMCPClient({
    "math": {
        "transport": "streamable_http",
        "url": "http://localhost:8001/mcp"
    },
    "database": {
        "transport": "streamable_http",
        "url": "http://localhost:8002/mcp"
    },
    "text": {
        "transport": "streamable_http",
        "url": "http://localhost:8102/mcp"
    }
})

tools = await client.get_tools()
```

El cliente puede conectarse a múltiples servidores simultáneamente.

## Uso con LangChain

### Obtener Herramientas

```python
async def obtener_herramientas_mcp():
    """Obtiene herramientas de un servidor MCP"""
    client = MultiServerMCPClient({
        "math": {
            "transport": "streamable_http",
            "url": "http://localhost:8001/mcp"
        }
    })
    
    tools = await client.get_tools()
    
    print(f"Herramientas disponibles: {len(tools)}")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    return tools
```

### Invocar Herramientas Directamente

```python
async def usar_herramienta():
    """Invoca una herramienta MCP directamente"""
    client = MultiServerMCPClient({
        "math": {
            "transport": "streamable_http",
            "url": "http://localhost:8001/mcp"
        }
    })
    
    tools = await client.get_tools()
    
    # Encontrar herramienta por nombre
    add_tool = next(t for t in tools if t.name == "add")
    
    # Invocar herramienta
    resultado = await add_tool.ainvoke({"a": 5, "b": 3})
    print(f"Resultado: {resultado}")
```

## Integración con LangGraph

### Agente Simple con MCP

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_mcp_adapters.client import MultiServerMCPClient

async def crear_agente():
    """Crea un agente LangGraph que usa herramientas MCP"""
    
    # 1. Obtener herramientas MCP
    client = MultiServerMCPClient({
        "math": {
            "transport": "streamable_http",
            "url": "http://localhost:8001/mcp"
        }
    })
    tools = await client.get_tools()
    
    # 2. Crear LLM con herramientas
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    llm_with_tools = llm.bind_tools(tools)
    
    # 3. Definir nodo de asistente
    def assistant_node(state: MessagesState):
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}
    
    # 4. Construir grafo
    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant_node)
    builder.add_node("tools", ToolNode(tools))
    
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")
    
    return builder.compile()

# Uso
graph = await crear_agente()
result = await graph.ainvoke({
    "messages": [{"role": "user", "content": "¿Cuánto es 15 + 27?"}]
})
```

### Agente con Memoria

```python
from langgraph.checkpoint.memory import MemorySaver

async def crear_agente_con_memoria():
    """Agente con memoria de conversación"""
    
    client = MultiServerMCPClient({
        "database": {
            "transport": "streamable_http",
            "url": "http://localhost:8002/mcp"
        }
    })
    tools = await client.get_tools()
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    llm_with_tools = llm.bind_tools(tools)
    
    def assistant_node(state: MessagesState):
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}
    
    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant_node)
    builder.add_node("tools", ToolNode(tools))
    
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")
    
    # Agregar memoria
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    
    return graph

# Uso con threads
graph = await crear_agente_con_memoria()
config = {"configurable": {"thread_id": "user_123"}}

# Primera pregunta
result1 = await graph.ainvoke({
    "messages": [{"role": "user", "content": "Muéstrame todos los productos"}]
}, config)

# Segunda pregunta (usa contexto de la anterior)
result2 = await graph.ainvoke({
    "messages": [{"role": "user", "content": "¿Cuáles son electrónicos?"}]
}, config)
```

## System Messages

Puedes dar instrucciones específicas al agente:

```python
from langchain_core.messages import SystemMessage

system_message = SystemMessage(
    content="""Eres un asistente especializado en consultas de base de datos.

INSTRUCCIONES:
- SOLO responde preguntas sobre productos y clientes de la tienda
- Usa las herramientas disponibles para consultar la base de datos
- Proporciona respuestas claras y organizadas
- Si te preguntan sobre otros temas, indica que solo puedes ayudar con datos de la tienda
"""
)

def assistant_node(state: MessagesState):
    messages = [system_message] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}
```

## Manejo de Errores

```python
async def agente_con_manejo_errores():
    """Agente que maneja errores de conexión"""
    try:
        client = MultiServerMCPClient({
            "database": {
                "transport": "streamable_http",
                "url": "http://localhost:8002/mcp"
            }
        })
        
        tools = await client.get_tools()
        
        if not tools:
            raise ValueError("No se encontraron herramientas en el servidor")
        
        return tools
        
    except ConnectionError:
        print("Error: No se pudo conectar al servidor MCP")
        print("Verifica que el servidor esté corriendo")
        return []
        
    except Exception as e:
        print(f"Error inesperado: {e}")
        return []
```

## Archivo cliente_simple.py

Implementa un cliente básico que:
- Conecta con un servidor MCP
- Lista herramientas disponibles
- Invoca herramientas directamente
- Muestra resultados

Uso:
```bash
python cliente_simple.py
```

## Archivo agente_simple.py

Implementa un agente LangGraph completo que:
- Usa herramientas MCP de matemáticas
- Responde preguntas en lenguaje natural
- Ejecuta cálculos usando las herramientas
- Mantiene conversación fluida

Uso:
```bash
python agente_simple.py
```

## Testing

### Test de Conexión

```python
async def test_conexion():
    """Verifica que el servidor esté disponible"""
    try:
        client = MultiServerMCPClient({
            "math": {
                "transport": "streamable_http",
                "url": "http://localhost:8001/mcp"
            }
        })
        
        tools = await client.get_tools()
        print(f"✅ Conectado. {len(tools)} herramientas disponibles")
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
```

### Test de Herramientas

```python
async def test_herramientas():
    """Prueba todas las herramientas disponibles"""
    client = MultiServerMCPClient({
        "math": {
            "transport": "streamable_http",
            "url": "http://localhost:8001/mcp"
        }
    })
    
    tools = await client.get_tools()
    
    for tool in tools:
        try:
            if tool.name == "add":
                result = await tool.ainvoke({"a": 5, "b": 3})
                print(f"✅ {tool.name}: {result}")
        except Exception as e:
            print(f"❌ {tool.name}: {e}")
```

## Ejercicios

### Ejercicio 1: Cliente Multi-Servidor
Crea un cliente que conecte simultáneamente a:
- Servidor de matemáticas
- Servidor de texto
- Servidor de validaciones

### Ejercicio 2: Agente Especializado
Crea un agente que:
- Use solo herramientas de base de datos
- Responda solo preguntas sobre productos
- Rechace preguntas fuera de su dominio

### Ejercicio 3: Chat Interactivo
Crea un script de chat en consola que:
- Mantenga conversación con memoria
- Use herramientas MCP cuando sea necesario
- Permita cambiar de thread de conversación

## Próximos Pasos

En el **Módulo 7** construirás un proyecto completo que integra todo lo aprendido: un agente LangGraph con API REST que consume un servidor MCP de base de datos.

**Archivos del módulo**:
- [`cliente_simple.py`](./cliente_simple.py) - Cliente MCP básico
- [`agente_simple.py`](./agente_simple.py) - Agente LangGraph con MCP
