"""
Script de pruebas para el servidor de conversión de temperaturas.
Usa el cliente MCP con comunicación stdio para verificar las conversiones.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def print_test_header(test_name: str):
    """Imprime encabezado para cada test"""
    print(f"\n{'=' * 60}")
    print(f"Test: {test_name}")
    print('=' * 60)

def print_result(operation: str, input_value: float, result: str):
    """Imprime resultado de una conversión"""
    print(f"Operación: {operation}")
    print(f"Entrada: {input_value}")
    print(f"Resultado: {result}")

async def test_list_tools(session: ClientSession):
    """Verifica que todas las herramientas estén disponibles"""
    print_test_header("Listar herramientas disponibles")
    
    try:
        tools_result = await session.list_tools()
        tools = tools_result.tools
        
        print(f"Herramientas encontradas: {len(tools)}")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        expected_tools = {"celsius_to_fahrenheit", "fahrenheit_to_celsius", "celsius_to_kelvin"}
        found_tools = {tool.name for tool in tools}
        
        if expected_tools == found_tools:
            print("\nResultado: Todas las herramientas están disponibles")
        else:
            print(f"\nAdvertencia: Se esperaban {expected_tools}, se encontraron {found_tools}")
            
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

async def test_celsius_to_fahrenheit(session: ClientSession):
    """Prueba conversión de Celsius a Fahrenheit"""
    print_test_header("Conversión Celsius a Fahrenheit")
    
    test_cases = [
        (0, 32),      # Punto de congelación del agua
        (100, 212),   # Punto de ebullición del agua
        (-40, -40),   # Punto donde C = F
        (37, 98.6),   # Temperatura corporal
    ]
    
    for celsius, expected_f in test_cases:
        try:
            result = await session.call_tool("celsius_to_fahrenheit", arguments={"celsius": celsius})
            fahrenheit = float(result.content[0].text)
            status = "OK" if abs(fahrenheit - expected_f) < 0.1 else "FAIL"
            print(f"{celsius}°C -> {fahrenheit}°F (esperado: {expected_f}°F) [{status}]")
        except Exception as e:
            print(f"Error en conversión {celsius}°C: {e}")

async def test_fahrenheit_to_celsius(session: ClientSession):
    """Prueba conversión de Fahrenheit a Celsius"""
    print_test_header("Conversión Fahrenheit a Celsius")
    
    test_cases = [
        (32, 0),      # Punto de congelación del agua
        (212, 100),   # Punto de ebullición del agua
        (-40, -40),   # Punto donde F = C
        (98.6, 37),   # Temperatura corporal
    ]
    
    for fahrenheit, expected_c in test_cases:
        try:
            result = await session.call_tool("fahrenheit_to_celsius", arguments={"fahrenheit": fahrenheit})
            celsius = float(result.content[0].text)
            status = "OK" if abs(celsius - expected_c) < 0.1 else "FAIL"
            print(f"{fahrenheit}°F -> {celsius}°C (esperado: {expected_c}°C) [{status}]")
        except Exception as e:
            print(f"Error en conversión {fahrenheit}°F: {e}")

async def test_celsius_to_kelvin(session: ClientSession):
    """Prueba conversión de Celsius a Kelvin"""
    print_test_header("Conversión Celsius a Kelvin")
    
    test_cases = [
        (0, 273.15),      # Punto de congelación del agua
        (100, 373.15),    # Punto de ebullición del agua
        (-273.15, 0),     # Cero absoluto
        (25, 298.15),     # Temperatura ambiente
    ]
    
    for celsius, expected_k in test_cases:
        try:
            result = await session.call_tool("celsius_to_kelvin", arguments={"celsius": celsius})
            kelvin = float(result.content[0].text)
            status = "OK" if abs(kelvin - expected_k) < 0.1 else "FAIL"
            print(f"{celsius}°C -> {kelvin}K (esperado: {expected_k}K) [{status}]")
        except Exception as e:
            print(f"Error en conversión {celsius}°C: {e}")

async def run_all_tests():
    """Ejecuta todos los tests del servidor de temperaturas"""
    print("\n" + "=" * 60)
    print("Suite de Testing - Servidor de Conversión de Temperaturas")
    print("=" * 60)
    print("\nEste test usa comunicación stdio (directa entre procesos)")
    
    input("\nPresiona Enter para comenzar los tests...")
    
    server_params = StdioServerParameters(
        command="python",
        args=["ejemplo_simple.py"],
        env=None
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                await test_list_tools(session)
                await test_celsius_to_fahrenheit(session)
                await test_fahrenheit_to_celsius(session)
                await test_celsius_to_kelvin(session)
                
                print("\n" + "=" * 60)
                print("Tests completados")
                print("=" * 60 + "\n")
                
    except Exception as e:
        print(f"\nError ejecutando tests: {e}")
        print("Verifica que ejemplo_simple.py esté en el directorio actual")

if __name__ == "__main__":
    asyncio.run(run_all_tests())
