"""
Script de pruebas para los servidores de recursos y prompts.
Usa el cliente MCP con comunicación stdio.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def print_test_header(test_name: str):
    """Imprime encabezado para cada test"""
    print(f"\n{'=' * 60}")
    print(f"Test: {test_name}")
    print('=' * 60)

async def test_servidor_recursos():
    """Tests para el servidor de recursos"""
    print("\n" + "=" * 60)
    print("SERVIDOR: Recursos")
    print("=" * 60)
    
    server_params = StdioServerParameters(
        command="python",
        args=["servidor_recursos.py"],
        env=None
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Test: Listar recursos
                print_test_header("Listar recursos disponibles")
                resources_result = await session.list_resources()
                print(f"Recursos disponibles: {len(resources_result.resources)}")
                for resource in resources_result.resources:
                    print(f"  - {resource.uri}: {resource.name}")
                
                # Test: Leer documentación
                print_test_header("Leer recurso: docs://readme")
                result = await session.read_resource("docs://readme")
                content = result.contents[0].text
                print(f"Contenido (primeros 200 caracteres):")
                print(content[:200] + "...")
                
                # Test: Leer configuración
                print_test_header("Leer recurso: config://settings")
                result = await session.read_resource("config://settings")
                config = json.loads(result.contents[0].text)
                print("Configuración:")
                print(f"  Aplicación: {config['application']['name']}")
                print(f"  Versión: {config['application']['version']}")
                print(f"  Ambiente: {config['application']['environment']}")
                
                # Test: Leer versión
                print_test_header("Leer recurso: info://version")
                result = await session.read_resource("info://version")
                version = json.loads(result.contents[0].text)
                print("Información de versión:")
                print(f"  Versión: {version['version']}")
                print(f"  Fecha: {version['build_date']}")
                print(f"  Python: {version['python_version']}")
                print(f"  Features: {', '.join(version['features'])}")
                
                # Test: Leer datos de ejemplo
                print_test_header("Leer recurso: data://example")
                result = await session.read_resource("data://example")
                data = json.loads(result.contents[0].text)
                print("Datos de ejemplo:")
                print(f"  Total usuarios: {data['stats']['total_users']}")
                print(f"  Usuarios:")
                for user in data['users']:
                    print(f"    - {user['name']} ({user['role']})")
                
                # Test: Leer estado actual
                print_test_header("Leer recurso: status://current")
                result = await session.read_resource("status://current")
                status = json.loads(result.contents[0].text)
                print("Estado actual del sistema:")
                print(f"  Status: {status['status']}")
                print(f"  Timestamp: {status['timestamp']}")
                print(f"  Uptime: {status['uptime']}")
                print(f"  Requests: {status['requests_handled']}")
                print(f"  Errors: {status['errors']}")
                
                print("\n" + "=" * 60)
                print("Tests del servidor de recursos completados")
                print("=" * 60)
                
    except Exception as e:
        print(f"\nError ejecutando tests de recursos: {e}")

async def test_servidor_prompts():
    """Tests para el servidor de prompts"""
    print("\n" + "=" * 60)
    print("SERVIDOR: Prompts")
    print("=" * 60)
    
    server_params = StdioServerParameters(
        command="python",
        args=["servidor_prompts.py"],
        env=None
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Test: Listar prompts
                print_test_header("Listar prompts disponibles")
                prompts_result = await session.list_prompts()
                print(f"Prompts disponibles: {len(prompts_result.prompts)}")
                for prompt in prompts_result.prompts:
                    print(f"  - {prompt.name}: {prompt.description}")
                
                # Test: Prompt de revisión de código
                print_test_header("Prompt: revisar_codigo")
                codigo_ejemplo = """
def calcular_suma(a, b):
    resultado = a + b
    return resultado
"""
                result = await session.get_prompt(
                    "revisar_codigo",
                    arguments={
                        "lenguaje": "python",
                        "codigo": codigo_ejemplo,
                        "enfoque": "general"
                    }
                )
                prompt_text = result.messages[0].content.text
                print("Prompt generado (primeros 300 caracteres):")
                print(prompt_text[:300] + "...")
                
                # Test: Prompt de generación de tests
                print_test_header("Prompt: generar_tests")
                result = await session.get_prompt(
                    "generar_tests",
                    arguments={
                        "funcion_nombre": "calcular_promedio",
                        "funcion_codigo": "def calcular_promedio(numeros): return sum(numeros) / len(numeros)",
                        "lenguaje": "python"
                    }
                )
                prompt_text = result.messages[0].content.text
                print("Prompt generado (primeros 300 caracteres):")
                print(prompt_text[:300] + "...")
                
                # Test: Prompt de documentación de API
                print_test_header("Prompt: documentar_api")
                result = await session.get_prompt(
                    "documentar_api",
                    arguments={
                        "endpoint": "/api/users",
                        "metodo": "GET",
                        "descripcion": "Obtiene la lista de usuarios del sistema"
                    }
                )
                prompt_text = result.messages[0].content.text
                print("Prompt generado (primeros 300 caracteres):")
                print(prompt_text[:300] + "...")
                
                # Test: Prompt de explicación de código
                print_test_header("Prompt: explicar_codigo")
                codigo = "lambda x: x ** 2"
                result = await session.get_prompt(
                    "explicar_codigo",
                    arguments={
                        "codigo": codigo,
                        "nivel": "principiante"
                    }
                )
                prompt_text = result.messages[0].content.text
                print("Prompt generado (primeros 300 caracteres):")
                print(prompt_text[:300] + "...")
                
                # Test: Prompt de refactorización
                print_test_header("Prompt: refactorizar_codigo")
                codigo_refactor = """
                            x = 10
                            y = 20
                            z = x + y
                            print(z)
                            """
                result = await session.get_prompt(
                    "refactorizar_codigo",
                    arguments={
                        "codigo": codigo_refactor,
                        "objetivo": "legibilidad"
                    }
                )
                prompt_text = result.messages[0].content.text
                print("Prompt generado (primeros 300 caracteres):")
                print(prompt_text[:300] + "...")
                
                print("\n" + "=" * 60)
                print("Tests del servidor de prompts completados")
                print("=" * 60)
                
    except Exception as e:
        print(f"\nError ejecutando tests de prompts: {e}")

async def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 60)
    print("Suite de Testing - Módulo 4: Recursos y Prompts")
    print("=" * 60)
    print("\nEste test ejecutará pruebas para:")
    print("  1. Servidor de recursos (resources)")
    print("  2. Servidor de prompts")
    
    input("\nPresiona Enter para comenzar los tests...")
    
    await test_servidor_recursos()
    await test_servidor_prompts()
    
    print("\n" + "=" * 60)
    print("Todos los tests completados")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    asyncio.run(run_all_tests())
