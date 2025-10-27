"""
Script para probar el servidor MCP de matemáticas.
Usa el cliente de FastMCP para comunicarse via stdio (comunicación directa entre procesos).
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import Dict, Any

def print_test_header(test_name: str):
    """Imprime un encabezado formateado para cada test"""
    print(f"\n{'=' * 60}")
    print(f"Test: {test_name}")
    print('=' * 60)

def print_result(operation: str, args: Dict[str, Any], result: Any):
    """Imprime el resultado de una operación"""
    print(f"✅ Operación: {operation}")
    print(f"   Argumentos: {args}")
    print(f"   Resultado: {result}")

async def test_list_tools(session: ClientSession):
    """Test: Listar todas las herramientas disponibles"""
    print_test_header("Listar herramientas disponibles")
    
    try:
        tools_result = await session.list_tools()
        tools = tools_result.tools
        
        print(f"✅ Herramientas encontradas: {len(tools)}")
        for tool in tools:
            print(f"   • {tool.name}: {tool.description}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_tool_call(session: ClientSession, tool_name: str, arguments: Dict[str, Any]):
    """Test: Llamar a una herramienta específica"""
    try:
        result = await session.call_tool(tool_name, arguments=arguments)
        print_result(tool_name, arguments, result.content[0].text)
        return True
    except Exception as e:
        print(f"❌ Error llamando {tool_name} con {arguments}: {e}")
        return False

async def test_addition(session: ClientSession):
    """Test: Suma de números"""
    print_test_header("Suma de números")
    
    tests = [
        {"a": 5, "b": 3},
        {"a": -10, "b": 20},
        {"a": 3.14, "b": 2.86},
    ]
    
    for args in tests:
        await test_tool_call(session, "add", args)

async def test_subtraction(session: ClientSession):
    """Test: Resta de números"""
    print_test_header("Resta de números")
    
    tests = [
        {"a": 10, "b": 3},
        {"a": 5, "b": 15},
        {"a": 0, "b": 0},
    ]
    
    for args in tests:
        await test_tool_call(session, "subtract", args)

async def test_multiplication(session: ClientSession):
    """Test: Multiplicación de números"""
    print_test_header("Multiplicación de números")
    
    tests = [
        {"a": 4, "b": 5},
        {"a": -3, "b": 7},
        {"a": 2.5, "b": 4},
    ]
    
    for args in tests:
        await test_tool_call(session, "multiply", args)

async def test_division(session: ClientSession):
    """Test: División de números"""
    print_test_header("División de números")
    
    tests = [
        {"a": 10, "b": 2},
        {"a": 7, "b": 3},
        {"a": 100, "b": 25},
    ]
    
    for args in tests:
        await test_tool_call(session, "divide", args)

async def test_division_by_zero(session: ClientSession):
    """Test: División por cero (caso de error)"""
    print_test_header("División por cero (test de error)")
    
    print("Intentando dividir 10 / 0...")
    try:
        result = await session.call_tool("divide", arguments={"a": 10, "b": 0})
        print("❌ Obtuvo:", result.content[0].text)
    except Exception as e:
        print(f"✅ Error manejado correctamente: {str(e)}")

async def run_all_tests():
    """Ejecuta todos los tests usando stdio"""
    print("\n" + "=" * 60)
    print("Suite de Testing - Servidor MCP Matemáticas")
    print("=" * 60)
    print("\n📝 Nota: Este test usa comunicación stdio (directa entre procesos)")
    print("   FastMCP inicia automáticamente el servidor cuando es necesario.")
    
    input("\nPresiona Enter para comenzar los tests...")
    
    # Configurar parámetros del servidor stdio
    server_params = StdioServerParameters(
        command="python",
        args=["servidor_math.py"],
        env=None
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Inicializar la sesión
                await session.initialize()
                
                # Ejecutar tests
                await test_list_tools(session)
                await test_addition(session)
                await test_subtraction(session)
                await test_multiplication(session)
                await test_division(session)
                await test_division_by_zero(session)
                
                print("\n" + "=" * 60)
                print("✅ Tests completados exitosamente")
                print("=" * 60 + "\n")
                
    except Exception as e:
        print(f"\n❌ Error ejecutando tests: {e}")
        print("   Verifica que servidor_math.py esté en el directorio actual")

if __name__ == "__main__":
    asyncio.run(run_all_tests())
