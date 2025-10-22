"""
Script para probar el servidor MCP de matemáticas.
Realiza llamadas HTTP para verificar que las herramientas funcionan correctamente.
"""

import httpx
import asyncio
from typing import Dict, Any

SERVER_URL = "http://localhost:8001/mcp"

def print_test_header(test_name: str):
    """Imprime un encabezado formateado para cada test"""
    print(f"\n{'=' * 60}")
    print(f"Test: {test_name}")
    print('=' * 60)

def print_result(operation: str, args: Dict[str, Any], result: Any):
    """Imprime el resultado de una operación"""
    print(f"Operación: {operation}")
    print(f"Argumentos: {args}")
    print(f"Resultado: {result}")

async def test_list_tools():
    """Test: Listar todas las herramientas disponibles"""
    print_test_header("Listar herramientas disponibles")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{SERVER_URL}/tools")
            tools = response.json()
            
            print(f"Herramientas encontradas: {len(tools.get('tools', []))}")
            for tool in tools.get('tools', []):
                print(f"  • {tool['name']}: {tool.get('description', 'Sin descripción')}")
            
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

async def test_tool_call(tool_name: str, arguments: Dict[str, Any]):
    """Test: Llamar a una herramienta específica"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{SERVER_URL}/call_tool",
                json={
                    "name": tool_name,
                    "arguments": arguments
                }
            )
            
            result = response.json()
            print_result(tool_name, arguments, result.get('result'))
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

async def test_addition():
    """Test: Suma de números"""
    print_test_header("Suma de números")
    
    tests = [
        {"a": 5, "b": 3},
        {"a": -10, "b": 20},
        {"a": 3.14, "b": 2.86},
    ]
    
    for args in tests:
        await test_tool_call("add", args)

async def test_subtraction():
    """Test: Resta de números"""
    print_test_header("Resta de números")
    
    tests = [
        {"a": 10, "b": 3},
        {"a": 5, "b": 15},
        {"a": 0, "b": 0},
    ]
    
    for args in tests:
        await test_tool_call("subtract", args)

async def test_multiplication():
    """Test: Multiplicación de números"""
    print_test_header("Multiplicación de números")
    
    tests = [
        {"a": 4, "b": 5},
        {"a": -3, "b": 7},
        {"a": 2.5, "b": 4},
    ]
    
    for args in tests:
        await test_tool_call("multiply", args)

async def test_division():
    """Test: División de números"""
    print_test_header("División de números")
    
    tests = [
        {"a": 10, "b": 2},
        {"a": 7, "b": 3},
        {"a": 100, "b": 25},
    ]
    
    for args in tests:
        await test_tool_call("divide", args)

async def test_division_by_zero():
    """Test: División por cero (caso de error)"""
    print_test_header("División por cero (test de error)")
    
    print("Intentando dividir 10 / 0...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{SERVER_URL}/call_tool",
                json={
                    "name": "divide",
                    "arguments": {"a": 10, "b": 0}
                }
            )
            
            result = response.json()
            if "error" in result or response.status_code != 200:
                print("✅ Error manejado correctamente")
                print(f"   Mensaje: {result.get('error', 'Error en el servidor')}")
            else:
                print("❌ Debería haber lanzado un error")
                
        except Exception as e:
            print(f"✅ Excepción capturada: {e}")

async def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 60)
    print("Suite de Testing - Servidor MCP Matemáticas")
    print("=" * 60)
    print("\nAsegúrate de que el servidor esté corriendo en el puerto 8001")
    print("Comando: python servidor_math.py")
    
    input("\nPresiona Enter para comenzar los tests...")
    
    # Verificar que el servidor esté disponible
    try:
        async with httpx.AsyncClient() as client:
            await client.get(f"{SERVER_URL}/tools", timeout=2.0)
    except Exception:
        print("\n❌ Error: No se pudo conectar al servidor")
        print("   Verifica que servidor_math.py esté corriendo")
        return
    
    # Ejecutar tests
    await test_list_tools()
    await test_addition()
    await test_subtraction()
    await test_multiplication()
    await test_division()
    await test_division_by_zero()
    
    print("\n" + "=" * 60)
    print("✅ Tests completados")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    asyncio.run(run_all_tests())
