"""
Script de pruebas para los servidores de procesamiento de texto y validación.
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

def print_result(tool_name: str, args: dict, result: str):
    """Imprime resultado de una llamada"""
    print(f"Herramienta: {tool_name}")
    print(f"Argumentos: {args}")
    print(f"Resultado: {result}")

async def test_servidor_texto():
    """Tests para el servidor de procesamiento de texto"""
    print("\n" + "=" * 60)
    print("SERVIDOR: Procesamiento de Texto")
    print("=" * 60)
    
    server_params = StdioServerParameters(
        command="python",
        args=["servidor_texto.py"],
        env=None
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Test: Listar herramientas
                print_test_header("Listar herramientas")
                tools_result = await session.list_tools()
                print(f"Herramientas disponibles: {len(tools_result.tools)}")
                for tool in tools_result.tools:
                    print(f"  - {tool.name}")
                
                # Test: Analizar texto
                print_test_header("Analizar texto")
                texto = "Hola mundo. Este es un texto de prueba. Tiene tres oraciones."
                result = await session.call_tool("analizar_texto", arguments={"texto": texto})
                stats = json.loads(result.content[0].text)
                print(f"Texto: '{texto}'")
                print(f"Estadísticas: {stats}")
                
                # Test: Transformar texto
                print_test_header("Transformar texto")
                transformaciones = ["mayusculas", "minusculas", "titulo", "invertir"]
                for operacion in transformaciones:
                    result = await session.call_tool(
                        "transformar_texto",
                        arguments={"texto": "Hola Mundo", "operacion": operacion}
                    )
                    print(f"{operacion}: {result.content[0].text}")
                
                # Test: Buscar en texto
                print_test_header("Buscar en texto")
                result = await session.call_tool(
                    "buscar_en_texto",
                    arguments={
                        "texto": "Python es genial. Python es poderoso.",
                        "patron": "Python",
                        "case_sensitive": False
                    }
                )
                busqueda = json.loads(result.content[0].text)
                print(f"Búsqueda de 'Python': {busqueda}")
                
                # Test: Limpiar texto
                print_test_header("Limpiar texto")
                result = await session.call_tool(
                    "limpiar_texto",
                    arguments={
                        "texto": "  Texto   con    espacios   extra!!!  ",
                        "remover_espacios_extra": True,
                        "remover_puntuacion": True
                    }
                )
                print(f"Texto limpio: '{result.content[0].text}'")
                
                # Test: Extraer palabras únicas
                print_test_header("Extraer palabras únicas")
                result = await session.call_tool(
                    "extraer_palabras_unicas",
                    arguments={
                        "texto": "el gato y el perro juegan en el parque",
                        "min_longitud": 3
                    }
                )
                palabras = json.loads(result.content[0].text)
                print(f"Palabras únicas (min 3 caracteres): {palabras}")
                
                print("\n" + "=" * 60)
                print("Tests del servidor de texto completados")
                print("=" * 60)
                
    except Exception as e:
        print(f"\nError ejecutando tests de texto: {e}")

async def test_servidor_validaciones():
    """Tests para el servidor de validación de datos"""
    print("\n" + "=" * 60)
    print("SERVIDOR: Validación de Datos")
    print("=" * 60)
    
    server_params = StdioServerParameters(
        command="python",
        args=["servidor_validaciones.py"],
        env=None
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Test: Listar herramientas
                print_test_header("Listar herramientas")
                tools_result = await session.list_tools()
                print(f"Herramientas disponibles: {len(tools_result.tools)}")
                for tool in tools_result.tools:
                    print(f"  - {tool.name}")
                
                # Test: Validar emails
                print_test_header("Validar emails")
                emails = [
                    "usuario@ejemplo.com",
                    "invalido@",
                    "otro.usuario@dominio.co"
                ]
                for email in emails:
                    result = await session.call_tool("validar_email", arguments={"email": email})
                    validacion = json.loads(result.content[0].text)
                    status = "VÁLIDO" if validacion.get("valido") else "INVÁLIDO"
                    print(f"{email}: {status}")
                
                # Test: Validar contraseñas
                print_test_header("Validar contraseñas")
                passwords = [
                    "abc123",
                    "Password123!",
                    "debil"
                ]
                for pwd in passwords:
                    result = await session.call_tool("validar_password", arguments={"password": pwd})
                    validacion = json.loads(result.content[0].text)
                    print(f"'{pwd}': Fortaleza={validacion['fortaleza']}, Válida={validacion['valida']}")
                    if validacion['errores']:
                        print(f"  Errores: {', '.join(validacion['errores'])}")
                
                # Test: Validar URLs
                print_test_header("Validar URLs")
                urls = [
                    "https://www.ejemplo.com",
                    "google.com",
                    "http://sitio.co/pagina"
                ]
                for url in urls:
                    result = await session.call_tool("validar_url", arguments={"url": url})
                    validacion = json.loads(result.content[0].text)
                    status = "VÁLIDA" if validacion.get("valida") else "INVÁLIDA"
                    print(f"{url}: {status}")
                
                # Test: Validar teléfonos
                print_test_header("Validar teléfonos")
                telefonos = [
                    ("+573001234567", "CO"),
                    ("3001234567", "CO"),
                    ("+12025551234", "US")
                ]
                for telefono, pais in telefonos:
                    result = await session.call_tool(
                        "validar_telefono",
                        arguments={"telefono": telefono, "pais": pais}
                    )
                    validacion = json.loads(result.content[0].text)
                    status = "VÁLIDO" if validacion.get("valido") else "INVÁLIDO"
                    print(f"{telefono} ({pais}): {status}")
                
                # Test: Validar rango numérico
                print_test_header("Validar rango numérico")
                casos = [
                    (50, 0, 100),
                    (150, 0, 100),
                    (25.5, 0, 50)
                ]
                for valor, minimo, maximo in casos:
                    result = await session.call_tool(
                        "validar_rango_numerico",
                        arguments={
                            "valor": valor,
                            "minimo": minimo,
                            "maximo": maximo,
                            "inclusive": True
                        }
                    )
                    validacion = json.loads(result.content[0].text)
                    status = "VÁLIDO" if validacion.get("valido") else "INVÁLIDO"
                    print(f"{valor} en [{minimo}, {maximo}]: {status}")
                    if validacion.get("valido"):
                        print(f"  Posición: {validacion['porcentaje_en_rango']}%")
                
                print("\n" + "=" * 60)
                print("Tests del servidor de validación completados")
                print("=" * 60)
                
    except Exception as e:
        print(f"\nError ejecutando tests de validación: {e}")

async def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 60)
    print("Suite de Testing - Módulo 3: Herramientas Avanzadas")
    print("=" * 60)
    print("\nEste test ejecutará pruebas para:")
    print("  1. Servidor de procesamiento de texto")
    print("  2. Servidor de validación de datos")
    
    input("\nPresiona Enter para comenzar los tests...")
    
    await test_servidor_texto()
    await test_servidor_validaciones()
    
    print("\n" + "=" * 60)
    print("Todos los tests completados")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    asyncio.run(run_all_tests())
