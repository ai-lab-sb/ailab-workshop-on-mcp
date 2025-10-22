"""
Suite de testing completa para el proyecto final.
Verifica servidor MCP, agente LangGraph y API REST.
"""

import asyncio
import httpx
from agente_seguros import AgenteSeguro


async def test_servidor_mcp():
    """Test 1: Verificar que el servidor MCP esté disponible"""
    print("\n" + "=" * 60)
    print("Test 1: Servidor MCP")
    print("=" * 60)
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8200/mcp/tools", timeout=5.0)
            
            if response.status_code == 200:
                tools = response.json()
                print(f"✅ Servidor MCP disponible")
                print(f"   Herramientas encontradas: {len(tools.get('tools', []))}")
                return True
            else:
                print(f"❌ Servidor respondió con código {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Error al conectar con servidor MCP: {e}")
        print("   Ejecuta: python servidor_seguros.py")
        return False


def test_agente_inicializacion():
    """Test 2: Verificar que el agente se inicialice correctamente"""
    print("\n" + "=" * 60)
    print("Test 2: Inicialización del Agente")
    print("=" * 60)
    
    try:
        agente = AgenteSeguro()
        
        if agente.graph and agente.client:
            print(f"✅ Agente inicializado correctamente")
            print(f"   Herramientas cargadas: {len(agente.client.get_tools())}")
            return True, agente
        else:
            print("❌ Agente no se inicializó correctamente")
            return False, None
            
    except Exception as e:
        print(f"❌ Error al inicializar agente: {e}")
        return False, None


def test_agente_consultas(agente):
    """Test 3: Probar consultas al agente"""
    print("\n" + "=" * 60)
    print("Test 3: Consultas al Agente")
    print("=" * 60)
    
    if agente is None:
        print("⚠️  Saltando test - agente no disponible")
        return False
    
    test_queries = [
        "¿Cuántas pólizas activas tenemos?",
        "Muéstrame los seguros de vida",
    ]
    
    exito = True
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nConsulta {i}: {query}")
        try:
            resultado = agente.chat(query, thread_id="test")
            
            if resultado:
                print(f"✅ Respuesta recibida ({len(resultado)} caracteres)")
            else:
                print("❌ Sin respuesta")
                exito = False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            exito = False
    
    return exito


async def test_api_rest():
    """Test 4: Verificar endpoints de la API REST"""
    print("\n" + "=" * 60)
    print("Test 4: API REST")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    try:
        async with httpx.AsyncClient() as client:
            # Test health endpoint
            print("\nProbando GET /health...")
            response = await client.get(f"{base_url}/health", timeout=5.0)
            if response.status_code == 200:
                print("✅ Health endpoint funciona")
            else:
                print(f"❌ Health endpoint retornó {response.status_code}")
                return False
            
            # Test chat endpoint
            print("\nProbando POST /chat...")
            chat_data = {
                "message": "¿Qué pólizas de vida están activas?",
                "thread_id": "test_api"
            }
            response = await client.post(
                f"{base_url}/chat",
                json=chat_data,
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Chat endpoint funciona")
                print(f"   Respuesta: {data['response'][:100]}...")
            else:
                print(f"❌ Chat endpoint retornó {response.status_code}")
                return False
            
            # Test history endpoint
            print("\nProbando GET /history/test_api...")
            response = await client.get(f"{base_url}/history/test_api", timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ History endpoint funciona")
                print(f"   Mensajes en historial: {len(data['messages'])}")
            else:
                print(f"❌ History endpoint retornó {response.status_code}")
                return False
            
            return True
            
    except httpx.ConnectError:
        print("❌ No se pudo conectar a la API")
        print("   Ejecuta: python api_rest.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 60)
    print("SUITE DE TESTING - Proyecto Final MCP Workshop")
    print("=" * 60)
    print("\n⚠️  Asegúrate de tener corriendo:")
    print("1. Terminal 1: python servidor_seguros.py")
    print("2. Terminal 2: python api_rest.py")
    
    input("\nPresiona Enter para comenzar los tests...")
    
    resultados = {
        "servidor_mcp": False,
        "agente_init": False,
        "agente_queries": False,
        "api_rest": False
    }
    
    # Test 1: Servidor MCP
    resultados["servidor_mcp"] = await test_servidor_mcp()
    
    if not resultados["servidor_mcp"]:
        print("\n⚠️  Tests restantes requieren que el servidor MCP esté corriendo")
        print_resultados(resultados)
        return
    
    # Test 2 y 3: Agente
    agente_ok, agente = test_agente_inicializacion()
    resultados["agente_init"] = agente_ok
    
    if agente_ok:
        resultados["agente_queries"] = test_agente_consultas(agente)
    
    # Test 4: API REST
    resultados["api_rest"] = await test_api_rest()
    
    # Resumen
    print_resultados(resultados)


def print_resultados(resultados):
    """Imprime resumen de resultados"""
    print("\n" + "=" * 60)
    print("RESUMEN DE RESULTADOS")
    print("=" * 60 + "\n")
    
    total = len(resultados)
    exitosos = sum(1 for v in resultados.values() if v)
    
    for nombre, resultado in resultados.items():
        icono = "✅" if resultado else "❌"
        print(f"{icono} {nombre.replace('_', ' ').title()}")
    
    print(f"\n{'=' * 60}")
    print(f"Total: {exitosos}/{total} tests pasaron")
    
    if exitosos == total:
        print("🎉 ¡Todos los tests pasaron exitosamente!")
    else:
        print("⚠️  Algunos tests fallaron - revisa los mensajes arriba")
    
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
