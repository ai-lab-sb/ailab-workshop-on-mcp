# Módulo 1: Fundamentos de MCP

## ¿Qué es Model Context Protocol (MCP)?

**Model Context Protocol (MCP)** es un protocolo estándar abierto que permite que las aplicaciones de IA accedan a datos y herramientas de manera segura y controlada. Fue creado por Anthropic en 2024 como respuesta a la fragmentación en el ecosistema de integraciones de IA.

### El Problema que Resuelve

Antes de MCP, cada aplicación de IA necesitaba:
- Integraciones personalizadas para cada fuente de datos
- Código específico para cada herramienta
- Mantenimiento constante de conectores
- Duplicación de esfuerzos entre proyectos

**MCP unifica todo esto en un protocolo estándar.**

### Analogía Simple

Piensa en MCP como **USB para IA**:
- Antes: cada dispositivo tenía su propio conector
- Después: un estándar universal (USB) para conectar cualquier cosa
- MCP hace lo mismo para conectar IA con datos y herramientas

## Arquitectura de MCP

### Componentes Principales

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Cliente   │ ◄─MCP──►│   Servidor   │ ◄─────► │   Recurso   │
│   (Host)    │         │     MCP      │         │  (Base de   │
│             │         │              │         │   Datos)    │
└─────────────┘         └──────────────┘         └─────────────┘
     ▲                        ▲
     │                        │
     │                        ├── Tools (herramientas)
     │                        ├── Resources (datos)
     │                        └── Prompts (plantillas)
     │
  Agente IA
```

### 1. **Cliente (Host)**
- Aplicación que consume el servidor MCP
- Puede ser Claude Desktop, VS Code, o tu agente personalizado
- Descubre capacidades disponibles en el servidor

### 2. **Servidor MCP**
- Expone herramientas, recursos y prompts
- Se comunica via protocolo MCP estandarizado
- Puede conectarse a múltiples fuentes de datos

### 3. **Recursos**
- Bases de datos
- APIs externas
- Sistemas de archivos
- Cualquier fuente de información

## Capacidades de MCP

### 🔧 Tools (Herramientas)
Funciones que el cliente puede ejecutar:
```python
# Ejemplo: herramienta de suma
@app.tool
def add(a: int, b: int) -> int:
    """Suma dos números"""
    return a + b
```

### 📄 Resources (Recursos)
Datos que el cliente puede leer:
```python
# Ejemplo: recurso de configuración
@app.resource("config://settings")
def get_settings() -> str:
    return json.dumps({"theme": "dark", "lang": "es"})
```

### 💬 Prompts (Plantillas)
Prompts predefinidos con argumentos:
```python
# Ejemplo: prompt para análisis
@app.prompt
def analyze_code(language: str, code: str) -> str:
    return f"Analiza este código {language}:\n{code}"
```

## Casos de Uso

### 1. **Acceso a Bases de Datos**
Un agente de IA puede consultar bases de datos sin exponer credenciales:
- Cliente solicita "obtener productos"
- Servidor MCP ejecuta query segura
- Cliente recibe solo los datos permitidos

### 2. **Integración con APIs**
Conecta tu agente con servicios externos:
- APIs de clima, noticias, finanzas
- Servicios internos de tu empresa
- Microservicios especializados

### 3. **Sistemas de Archivos**
Lee y escribe archivos de manera controlada:
- Lectura de documentación
- Generación de reportes
- Acceso a configuraciones

### 4. **Herramientas Especializadas**
Expón funcionalidades específicas:
- Cálculos complejos
- Procesamiento de imágenes
- Análisis de datos

## Ventajas de MCP

### ✅ Estandarización
- Un protocolo para todas las integraciones
- Compatible con múltiples clientes y servidores
- Reduce la complejidad del ecosistema

### 🔒 Seguridad
- Control granular de permisos
- No se exponen credenciales al cliente
- Validación en el servidor

### 🔄 Reutilización
- Escribe un servidor, úsalo en múltiples proyectos
- Comparte servidores con la comunidad
- Ecosistema creciente de servidores públicos

### ⚡ Simplicidad
- Frameworks como FastMCP facilitan la creación
- Menos código boilerplate
- Desarrollo rápido

## FastMCP: Framework Moderno

**FastMCP** es un framework Python que simplifica la creación de servidores MCP.

### Características Principales

- **Decoradores simples**: `@app.tool`, `@app.resource`, `@app.prompt`
- **Type hints**: Validación automática de tipos
- **Async support**: Operaciones asíncronas nativas
- **Multiple transports**: HTTP, stdio, SSE
- **Documentación automática**: Genera descripciones desde docstrings

### Ejemplo Mínimo

```python
from fastmcp import FastMCP

app = FastMCP("Mi Servidor")

@app.tool
def saludar(nombre: str) -> str:
    """Saluda a una persona"""
    return f"¡Hola, {nombre}!"

if __name__ == "__main__":
    app.run()
```

Eso es todo para crear un servidor MCP funcional. 🎉

## Transporte HTTP vs STDIO

### STDIO (Standard Input/Output)
- Cliente y servidor en la misma máquina
- Comunicación via stdin/stdout
- Usado por Claude Desktop, VS Code
- **No requiere red**

### HTTP/SSE (Server-Sent Events)
- Cliente y servidor pueden estar remotos
- Comunicación via HTTP
- Útil para servicios web
- **Requiere puerto de red**

En este workshop usaremos **HTTP** porque es más fácil de testear y debuggear.

## Ecosistema MCP

### Clientes Populares
- **Claude Desktop**: App de Anthropic con soporte MCP nativo
- **VS Code**: Via extensiones
- **Agentes personalizados**: Usando langchain-mcp-adapters

### Servidores Disponibles
- **Oficiales**: filesystem, sqlite, postgres, github
- **Comunidad**: cientos de integraciones disponibles
- **Propios**: crea los tuyos con FastMCP

Explora servidores en: [GitHub MCP Servers](https://github.com/modelcontextprotocol/servers)

## Conceptos Clave

### Descubrimiento Automático
El cliente puede pedir al servidor:
- ¿Qué herramientas tienes disponibles?
- ¿Qué recursos puedo consultar?
- ¿Qué prompts ofreces?

Todo esto sin conocimiento previo del servidor.

### Invocación Dinámica
El cliente puede llamar herramientas descubiertas en tiempo real:
```
Cliente: "¿Qué herramientas tienes?"
Servidor: "Tengo: add, subtract, multiply, divide"
Cliente: "Ejecuta add con a=5, b=3"
Servidor: "Resultado: 8"
```

### Type Safety
MCP valida tipos automáticamente:
- Parámetros incorrectos = error antes de ejecutar
- Documentación clara de qué acepta cada herramienta
- Mejor experiencia de desarrollo

## ¿Por Qué es Importante MCP?

### Antes de MCP
```python
# Integración específica para cada cliente
def query_database_for_claude(query):
    # Código específico de Claude

def query_database_for_chatgpt(query):
    # Código específico de ChatGPT

def query_database_for_gemini(query):
    # Código específico de Gemini
```

### Con MCP
```python
# Un servidor para todos
@app.tool
def query_database(query: str) -> List[Dict]:
    """Consulta la base de datos"""
    return execute_query(query)

# Funciona con Claude, ChatGPT, Gemini, o cualquier cliente MCP
```

## Próximos Pasos

Ahora que entiendes los fundamentos de MCP, es hora de ver código real.

En el archivo `ejemplo_simple.py` encontrarás tu primer servidor MCP funcional.

### Ejercicio

1. Lee y ejecuta `ejemplo_simple.py`
2. Observa cómo se define una herramienta
3. Prueba el servidor con diferentes entradas
4. Modifica la herramienta para aceptar más parámetros

**Continúa con:** [`ejemplo_simple.py`](./ejemplo_simple.py)
