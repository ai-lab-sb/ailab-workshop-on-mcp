# Módulo 4: Recursos y Prompts en MCP

## Más Allá de las Herramientas

Hasta ahora hemos trabajado con **Tools** (herramientas), pero MCP soporta dos conceptos adicionales:

1. **Resources** (Recursos): Datos que el cliente puede leer
2. **Prompts**: Plantillas de prompts reutilizables

En este módulo aprenderás a exponer recursos y prompts desde tus servidores MCP.

## Resources: Exponiendo Datos

### ¿Qué son los Resources?

Resources son **datos estáticos o dinámicos** que el servidor expone para que los clientes los lean. A diferencia de las herramientas, los resources no ejecutan acciones, solo proporcionan información.

### Casos de Uso

- Documentación de API
- Configuraciones del sistema
- Contenido de archivos
- Esquemas de base de datos
- Logs del sistema

### Sintaxis Básica

```python
from fastmcp import FastMCP

app = FastMCP("Resource Server")

@app.resource("config://settings")
def get_settings():
    """Configuración del sistema"""
    return {
        "version": "1.0.0",
        "theme": "dark",
        "language": "es"
    }
```

### URI Pattern

Resources usan un patrón de URI para identificarse:
- `config://settings` - Configuración
- `file://docs/readme` - Archivo de documentación
- `db://schema/users` - Esquema de tabla

## Prompts: Plantillas Reutilizables

### ¿Qué son los Prompts?

Prompts son **plantillas de prompts con argumentos** que el servidor proporciona para tareas comunes. Facilitan la reutilización de prompts bien diseñados.

### Casos de Uso

- Análisis de código estándar
- Plantillas de documentación
- Prompts de revisión
- Generación de reportes

### Sintaxis Básica

```python
@app.prompt()
def analizar_codigo(lenguaje: str, codigo: str):
    """Analiza código y proporciona feedback"""
    return f"""Analiza el siguiente código en {lenguaje} y proporciona:
1. Evaluación de calidad
2. Posibles mejoras
3. Bugs potenciales

Código:
```{lenguaje}
{codigo}
```
"""
```

## Implementación Práctica

El archivo `servidor_recursos.py` implementa un servidor con:

### Resources Disponibles

1. **Documentación de API**
```python
@app.resource("docs://api")
def get_api_docs():
    """Documentación completa de la API"""
    return """
    # API Documentation
    
    ## Endpoints
    - GET /users - Lista usuarios
    - POST /users - Crea usuario
    ...
    """
```

2. **Configuración del Sistema**
```python
@app.resource("config://app")
def get_config():
    """Configuración de la aplicación"""
    return {
        "database": {
            "host": "localhost",
            "port": 5432
        },
        "cache": {
            "enabled": True,
            "ttl": 3600
        }
    }
```

3. **Estadísticas en Tiempo Real**
```python
@app.resource("stats://current")
def get_stats():
    """Estadísticas actuales del sistema"""
    import psutil
    return {
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }
```

## Prompts con FastMCP

El archivo `servidor_prompts.py` implementa prompts útiles:

### 1. Análisis de Código

```python
@app.prompt()
def revisar_codigo(lenguaje: str, codigo: str, enfoque: str = "general"):
    """Genera un prompt para revisar código"""
    return f"""Eres un experto en {lenguaje}. 
    
Revisa el siguiente código con enfoque en: {enfoque}

Código:
```{lenguaje}
{codigo}
```

Proporciona:
1. Análisis de calidad
2. Sugerencias de mejora
3. Problemas potenciales
"""
```

### 2. Generación de Documentación

```python
@app.prompt()
def generar_docs(tipo: str, nombre: str, descripcion: str):
    """Genera documentación para código"""
    return f"""Genera documentación completa para:

Tipo: {tipo}
Nombre: {nombre}
Descripción: {descripcion}

Incluye:
- Descripción detallada
- Parámetros y tipos
- Ejemplos de uso
- Casos especiales
"""
```

### 3. Plantilla de Testing

```python
@app.prompt()
def crear_tests(funcion: str, lenguaje: str = "python"):
    """Genera tests para una función"""
    return f"""Crea tests unitarios completos para la función: {funcion}

Lenguaje: {lenguaje}

Incluye:
- Tests de casos normales
- Tests de casos extremos
- Tests de errores
- Mocks si son necesarios
"""
```

## Resources Dinámicos

Resources pueden generar contenido dinámicamente:

```python
from datetime import datetime

@app.resource("logs://today")
def get_today_logs():
    """Logs del día actual"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Leer logs del día
    try:
        with open(f"logs/{today}.log", "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"No hay logs para {today}"
```

## Resources con Parámetros

Aunque resources no ejecutan funciones desde el cliente, pueden usar parámetros en su definición:

```python
@app.resource("file://{path}")
def get_file(path: str):
    """Lee un archivo del sistema"""
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"
```

## Combinando Resources, Prompts y Tools

Un servidor MCP completo puede exponer los tres tipos:

```python
app = FastMCP("Complete Server")

# Tool: Ejecuta acciones
@app.tool
def process_data(data: str) -> str:
    return data.upper()

# Resource: Proporciona datos
@app.resource("docs://help")
def get_help():
    return "Documentación del servidor"

# Prompt: Plantilla reutilizable
@app.prompt()
def analyze(text: str):
    return f"Analiza este texto: {text}"
```

## Descubrimiento de Resources y Prompts

Los clientes pueden descubrir resources y prompts igual que las herramientas:

```python
# Listar resources
GET /mcp/resources

# Listar prompts
GET /mcp/prompts

# Leer un resource
GET /mcp/resource/docs://api

# Obtener un prompt
GET /mcp/prompt/revisar_codigo?lenguaje=python
```

## Buenas Prácticas

### 1. URIs Descriptivos para Resources

```python
# ✅ Bien
@app.resource("config://database/connection")
@app.resource("docs://api/authentication")
@app.resource("logs://errors/today")

# ❌ Mal
@app.resource("r1")
@app.resource("data")
```

### 2. Prompts con Descripciones Claras

```python
@app.prompt()
def template(param: str):
    """
    Plantilla para [tarea específica].
    
    Args:
        param: Descripción del parámetro
        
    Returns:
        Prompt completo listo para usar
    """
    return f"Prompt con {param}"
```

### 3. Resources con Manejo de Errores

```python
@app.resource("data://users")
def get_users():
    """Lista de usuarios"""
    try:
        # Obtener datos
        return get_users_from_db()
    except Exception as e:
        return {"error": str(e), "data": []}
```

## Cuándo Usar Cada Concepto

### Usa **Tools** cuando:
- Necesitas ejecutar una acción
- Los datos cambian basados en parámetros
- Requieres procesamiento complejo

### Usa **Resources** cuando:
- Los datos son relativamente estáticos
- Solo necesitas lectura, no escritura
- Quieres exponer documentación o configuración

### Usa **Prompts** cuando:
- Tienes plantillas de prompts reutilizables
- Quieres estandarizar interacciones
- Necesitas prompts parametrizados

## Ejercicios

### Ejercicio 1: Resources de Documentación
Crea un servidor con resources que expongan:
- README del proyecto
- Changelog
- Licencia
- Guía de contribución

### Ejercicio 2: Prompts de Análisis
Crea prompts para:
- Análisis de rendimiento de código
- Revisión de seguridad
- Sugerencias de refactoring
- Generación de tests

### Ejercicio 3: Sistema de Logging
Crea resources que proporcionen:
- Logs del día actual
- Logs de errores
- Estadísticas de logs
- Búsqueda en logs

## Próximos Pasos

Continúa con el **Módulo 5** para integrar bases de datos con MCP.

**Archivos del módulo**:
- [`servidor_recursos.py`](./servidor_recursos.py) - Servidor con resources
- [`servidor_prompts.py`](./servidor_prompts.py) - Servidor con prompts

**Nota**: En este workshop nos enfocamos principalmente en Tools por ser los más utilizados, pero Resources y Prompts son características poderosas de MCP que vale la pena explorar.
