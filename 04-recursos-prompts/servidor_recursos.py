"""
Servidor MCP con recursos (resources).
Demuestra cómo exponer datos estáticos y dinámicos via resources.
"""

from fastmcp import FastMCP
from datetime import datetime
import json

app = FastMCP("Resources Server")

@app.resource("docs://readme")
def get_readme():
    """Documentación principal del servidor"""
    return """# Servidor de Recursos MCP

Este servidor expone varios recursos de información:

## Resources Disponibles

- `docs://readme` - Esta documentación
- `config://settings` - Configuración del sistema
- `info://version` - Información de versión
- `data://example` - Datos de ejemplo

## Uso

Los resources se acceden via el protocolo MCP y proporcionan
información estática o dinámica sin ejecutar acciones.
"""

@app.resource("config://settings")
def get_settings():
    """Configuración del sistema"""
    return json.dumps({
        "application": {
            "name": "MCP Resources Server",
            "version": "1.0.0",
            "environment": "development"
        },
        "server": {
            "host": "0.0.0.0",
            "port": 8104,
            "debug": True
        },
        "features": {
            "logging": True,
            "metrics": True,
            "cache": False
        }
    }, indent=2)

@app.resource("info://version")
def get_version():
    """Información de versión del servidor"""
    return json.dumps({
        "version": "1.0.0",
        "build_date": "2024-01-15",
        "python_version": "3.10+",
        "mcp_version": "1.0",
        "features": ["resources", "dynamic_content"]
    }, indent=2)

@app.resource("data://example")
def get_example_data():
    """Datos de ejemplo para testing"""
    return json.dumps({
        "users": [
            {"id": 1, "name": "Juan", "role": "admin"},
            {"id": 2, "name": "María", "role": "user"},
            {"id": 3, "name": "Carlos", "role": "user"}
        ],
        "stats": {
            "total_users": 3,
            "active_sessions": 1,
            "last_update": datetime.now().isoformat()
        }
    }, indent=2)

@app.resource("status://current")
def get_current_status():
    """Estado actual del sistema (dinámico)"""
    return json.dumps({
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "uptime": "24 hours",
        "requests_handled": 1247,
        "errors": 3
    }, indent=2)

if __name__ == "__main__":
    print("=" * 60)
    print("Servidor MCP - Resources")
    print("=" * 60)
    print("\n🚀 Iniciando servidor en http://localhost:8104")
    print("\n📋 Resources disponibles:")
    print("   • docs://readme      - Documentación")
    print("   • config://settings  - Configuración")
    print("   • info://version     - Información de versión")
    print("   • data://example     - Datos de ejemplo")
    print("   • status://current   - Estado actual")
    print("\n💡 Presiona Ctrl+C para detener el servidor\n")
    print("=" * 60 + "\n")
    
    app.run(transport="streamable-http", host="0.0.0.0", port=8104)
