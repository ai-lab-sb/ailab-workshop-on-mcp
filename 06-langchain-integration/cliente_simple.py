"""
Cliente simple para probar conexión con servidores MCP.
Demuestra cómo descubrir e invocar herramientas MCP.
"""

import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

async def listar_herramientas():
    """Lista todas las herramientas disponibles en el servidor MCP"""
    print("=" * 60)
    print("Cliente MCP - Descubrimiento de Herramientas")
    print("=" * 60 + "\n")
    
    print("Conectando al servidor de matemáticas...")
    
    try:
        client = MultiServerMCPClient({
            "math": {
                "transport": "streamable_http",
                "url": "http://localhost:8001/mcp"
            }
        })
        
        tools = await client.get_tools()
        
        print(f"\n✅ Conectado exitosamente")
        print(f"📋 Herramientas disponibles: {len(tools)}\n")
        
        for i, tool in enumerate(tools, 1):
            print(f"{i}. {tool.name}")
            print(f"   Descripción: {tool.description}")
            print()
        
        return tools
        
    except Exception as e:
        print(f"\n❌ Error al conectar: {e}")
        print("Verifica que el servidor esté corriendo en el puerto 8001")
        return []

async def invocar_herramienta(tools):
    """Invoca una herramienta MCP directamente"""
    if not tools:
        print("No hay herramientas disponibles")
        return
    
    print("\n" + "=" * 60)
    print("Invocación de Herramientas")
    print("=" * 60 + "\n")
    
    add_tool = next((t for t in tools if t.name == "add"), None)
    
    if add_tool:
        print("Invocando herramienta 'add' con a=10, b=25...")
        try:
            resultado = await add_tool.ainvoke({"a": 10, "b": 25})
            print(f"✅ Resultado: {resultado}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
    multiply_tool = next((t for t in tools if t.name == "multiply"), None)
    
    if multiply_tool:
        print("Invocando herramienta 'multiply' con a=7, b=8...")
        try:
            resultado = await multiply_tool.ainvoke({"a": 7, "b": 8})
            print(f"✅ Resultado: {resultado}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")

async def main():
    """Función principal"""
    tools = await listar_herramientas()
    
    if tools:
        await invocar_herramienta(tools)
    
    print("=" * 60)
    print("Cliente finalizado")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
