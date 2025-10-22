# Workshop: Model Context Protocol (MCP) con FastMCP

Bienvenido al workshop de **Model Context Protocol (MCP)** utilizando **FastMCP**. Este curso te enseñará a crear servidores MCP y conectarlos con agentes inteligentes usando LangGraph.

## 🎯 ¿Qué aprenderás?

Este workshop te guiará desde los fundamentos de MCP hasta la construcción de un agente LangGraph completo que consume servicios MCP:

- **Fundamentos de MCP**: Qué es, por qué existe y casos de uso
- **FastMCP**: Framework moderno para crear servidores MCP
- **Herramientas y recursos**: Exposición de funciones como herramientas
- **Integración con LangGraph**: Uso de `langchain-mcp-adapters`
- **Proyecto Final**: Agente completo que consulta base de datos via MCP

## 📋 Estructura del Workshop

### **Módulo 1: Introducción a MCP**
Conceptos fundamentales, historia y casos de uso del protocolo MCP.
- `01-fundamentos/README.md` - Teoría y conceptos
- `01-fundamentos/ejemplo_simple.py` - Primer servidor MCP

### **Módulo 2: FastMCP Básico**
Creación de servidores MCP con herramientas básicas.
- `02-fastmcp-basico/README.md` - Guía de FastMCP
- `02-fastmcp-basico/servidor_math.py` - Servidor de operaciones matemáticas
- `02-fastmcp-basico/test_servidor.py` - Testing del servidor

### **Módulo 3: Herramientas Avanzadas**
Herramientas complejas, validación y manejo de errores.
- `03-herramientas-avanzadas/README.md` - Conceptos avanzados
- `03-herramientas-avanzadas/servidor_texto.py` - Procesamiento de texto
- `03-herramientas-avanzadas/servidor_validaciones.py` - Validación de datos

### **Módulo 4: Recursos y Prompts**
Exposición de datos estáticos y prompts reutilizables.
- `04-recursos-prompts/README.md` - Recursos y prompts MCP
- `04-recursos-prompts/servidor_recursos.py` - Servidor con recursos
- `04-recursos-prompts/servidor_prompts.py` - Servidor con prompts

### **Módulo 5: Base de Datos**
Servidores MCP que interactúan con bases de datos.
- `05-base-datos/README.md` - Integración con SQLite
- `05-base-datos/servidor_db.py` - Servidor con base de datos
- `05-base-datos/init_db.py` - Inicialización de datos

### **Módulo 6: LangChain MCP Tools**
Integración de servidores MCP con LangChain y LangGraph.
- `06-langchain-integration/README.md` - Guía de integración
- `06-langchain-integration/cliente_simple.py` - Cliente básico
- `06-langchain-integration/agente_simple.py` - Agente con MCP

### **Módulo 7: Proyecto Final**
Agente completo con LangGraph que consume servidor MCP de base de datos.
- `07-proyecto-final/README.md` - Guía del proyecto
- `07-proyecto-final/servidor_tienda.py` - Servidor MCP de tienda
- `07-proyecto-final/agente_tienda.py` - Agente LangGraph
- `07-proyecto-final/api_rest.py` - API REST del agente
- `07-proyecto-final/test_agente.py` - Testing completo

## 🚀 Requisitos Previos

### Conocimientos
- Python intermedio (clases, async/await, decoradores)
- Conceptos básicos de APIs REST
- Familiaridad con LLMs (opcional pero recomendado)

### Software
- Python 3.10 o superior
- Editor de código (VS Code recomendado)
- Postman o curl para testing

### Dependencias
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Instalar dependencias base
pip install fastmcp langchain-google-genai langgraph langchain-mcp-adapters python-dotenv
```

## 📚 Metodología de Aprendizaje

1. **Lee el README** de cada módulo para entender la teoría
2. **Ejecuta los ejemplos** en orden para ver los conceptos en acción
3. **Modifica el código** para experimentar y aprender
4. **Completa los ejercicios** propuestos al final de cada módulo

## ⏱️ Duración Estimada

- **Lectura y teoría**: 2-3 horas
- **Práctica con ejemplos**: 3-4 horas
- **Proyecto final**: 2-3 horas
- **Total**: 8-10 horas

Se recomienda completar el workshop en 2-3 sesiones.

## 🎓 Niveles de Progreso

### 🟢 Nivel Principiante
- Completa módulos 1-3
- Entiende conceptos básicos de MCP
- Crea servidores simples con herramientas

### 🟡 Nivel Intermedio
- Completa módulos 1-5
- Integra bases de datos con MCP
- Maneja validaciones y errores

### 🔴 Nivel Avanzado
- Completa todos los módulos
- Construye agentes LangGraph con MCP
- Despliega APIs REST completas

## 📖 Recursos Adicionales

### Documentación Oficial
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [LangChain MCP Adapters](https://github.com/rectalogic/langchain-mcp-adapters)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

### Comunidad
- [MCP GitHub Discussions](https://github.com/modelcontextprotocol/mcp/discussions)
- [LangChain Community](https://github.com/langchain-ai/langchain/discussions)

## 🛠️ Estructura de Archivos

```
mcp-workshop/
├── README.md                          # Este archivo
├── requirements.txt                   # Dependencias del workshop
├── 01-fundamentos/
│   ├── README.md
│   └── ejemplo_simple.py
├── 02-fastmcp-basico/
│   ├── README.md
│   ├── servidor_math.py
│   └── test_servidor.py
├── 03-herramientas-avanzadas/
│   ├── README.md
│   ├── servidor_texto.py
│   └── servidor_validaciones.py
├── 04-recursos-prompts/
│   ├── README.md
│   ├── servidor_recursos.py
│   └── servidor_prompts.py
├── 05-base-datos/
│   ├── README.md
│   ├── servidor_db.py
│   └── init_db.py
├── 06-langchain-integration/
│   ├── README.md
│   ├── cliente_simple.py
│   └── agente_simple.py
└── 07-proyecto-final/
    ├── README.md
    ├── servidor_tienda.py
    ├── agente_tienda.py
    ├── api_rest.py
    └── test_agente.py
```

## 🚦 Inicio Rápido

### 1. Configuración Inicial
```bash
# Clonar o descargar el workshop
cd mcp-workshop

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar API Key
Crea un archivo `.env` en la raíz con tu Google API Key:
```
GOOGLE_API_KEY=tu_api_key_aqui
```

Obtén tu API key en: [Google AI Studio](https://makersuite.google.com/app/apikey)

### 3. Primer Ejemplo
```bash
# Ir al módulo 1
cd 01-fundamentos

# Ejecutar primer servidor MCP
python ejemplo_simple.py
```

## 💡 Consejos para el Workshop

- **Experimenta**: Modifica los ejemplos para entender cómo funcionan
- **Lee los comentarios**: El código está documentado para facilitar el aprendizaje
- **No te saltes módulos**: Los conceptos se construyen progresivamente
- **Usa el debugger**: Coloca breakpoints para entender el flujo
- **Consulta la documentación**: Los enlaces a recursos son tu mejor aliado

## 🤝 Soporte

Este workshop es parte de los materiales de AI Lab. Para preguntas o problemas:

1. Revisa el README del módulo específico
2. Consulta la documentación oficial de FastMCP
3. Busca en los GitHub Discussions de MCP

---

**¿Listo para empezar?** Dirígete a [`01-fundamentos/README.md`](./01-fundamentos/README.md) para comenzar tu viaje con MCP.
