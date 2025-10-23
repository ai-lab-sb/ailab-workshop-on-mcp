# Módulo 8 (Opcional): Usando MCP Servers Existentes

## 🎯 Aprendiendo con Jupyter Notebooks

Este módulo opcional usa **Jupyter Notebooks interactivos** para enseñarte a usar servidores MCP existentes de la comunidad. A diferencia de los módulos anteriores donde creabas tus propios servidores, aquí aprenderás a aprovechar servidores ya existentes.

## ¿Por Qué Este Módulo?

### Ventajas de Usar Servidores Existentes

1. ⚡ **Ahorro de Tiempo**: No reinventar la rueda
2. ✅ **Código Probado**: Implementaciones maduras y testeadas
3. 🌍 **Ecosistema Rico**: Cientos de servidores disponibles
4. 🎓 **Mejores Prácticas**: Aprende de expertos
5. 🔗 **Rápida Integración**: Conecta y usa en minutos

## 📚 Notebooks del Módulo

### Notebook 1: Introducción
**`01_introduccion_mcps_existentes.ipynb`**
- ¿Qué son los servidores MCP existentes?
- Ecosistema MCP (oficiales y comunitarios)
- Cuándo usar servidores existentes vs crear propios
- Configuración del entorno

### Notebook 2: SQLite MCP Básico
**`02_sqlite_mcp_basico.ipynb`**
- Instalación del servidor SQLite MCP
- Crear base de datos de ejemplo
- Conectar desde Python
- Explorar herramientas disponibles
- Primeras consultas

### Notebook 3: Agente con SQLite MCP
**`03_agente_con_sqlite_mcp.ipynb`**
- Crear agente LangGraph completo
- Integrar herramientas SQLite MCP
- System prompts especializados
- Consultas en lenguaje natural
- Ejemplos prácticos

### Notebook 4: Múltiples Servidores
**`04_multi_servidor.ipynb`**
- Conectar múltiples servidores simultáneamente
- Cliente unificado
- Filtrado de herramientas
- Casos de uso avanzados

## 🚀 Inicio Rápido

### 1. Instalar Jupyter

```bash
# Si no tienes Jupyter instalado
pip install jupyter notebook

# O usa JupyterLab (más moderno)
pip install jupyterlab
```

### 2. Instalar Node.js (para servidores npm)

Los servidores MCP oficiales están en npm, necesitas Node.js:
- Descarga desde: https://nodejs.org/
- Instala la versión LTS recomendada

### 3. Verificar instalaciones

```bash
# Verificar Python
python --version

# Verificar Node.js
node --version

# Verificar npm
npm --version
```

### 4. Iniciar Jupyter

```bash
cd 08-mcps-existentes

# Con Jupyter Notebook
jupyter notebook

# O con JupyterLab
jupyter lab
```

Se abrirá tu navegador con la interfaz de Jupyter.

### 5. Seguir los Notebooks en Orden

Abre y completa los notebooks en orden:
1. `01_introduccion_mcps_existentes.ipynb`
2. `02_sqlite_mcp_basico.ipynb`
3. `03_agente_con_sqlite_mcp.ipynb`
4. `04_multi_servidor.ipynb`

## 📋 Pre-requisitos

### Conocimientos
- Haber completado los módulos 1-6 del workshop
- Entender conceptos básicos de MCP y FastMCP
- Familiaridad con Jupyter Notebooks

### Software
- ✅ Python 3.10+
- ✅ Node.js 18+ (para servidores npm)
- ✅ Jupyter Notebook o JupyterLab
- ✅ Dependencias del workshop instaladas

### API Key
- Google API Key para usar Gemini
- Archivo `.env` en la raíz del proyecto

## 🎓 Metodología de Aprendizaje

### Con Jupyter Notebooks

1. **Lee las explicaciones** en las celdas markdown
2. **Ejecuta las celdas de código** una por una (Shift+Enter)
3. **Observa los resultados** después de cada celda
4. **Modifica el código** para experimentar
5. **Completa los ejercicios** al final de cada notebook

### Ventajas de Jupyter

- ✅ Ejecución interactiva paso a paso
- ✅ Visualización inmediata de resultados
- ✅ Experimentación segura (sin afectar otros archivos)
- ✅ Documentación integrada con código
- ✅ Fácil de compartir y revisar

## 🛠️ Estructura del Módulo

```
08-mcps-existentes/
├── README.md                              # Este archivo
├── INICIO-RAPIDO.md                       # Guía rápida
├── 01_introduccion_mcps_existentes.ipynb  # Notebook 1
├── 02_sqlite_mcp_basico.ipynb             # Notebook 2
├── 03_agente_con_sqlite_mcp.ipynb         # Notebook 3
├── 04_multi_servidor.ipynb                # Notebook 4
├── crear_db_ejemplo.py                    # Utilidad para crear BD
└── .gitignore                             # Ignorar archivos generados
```

## 🔧 Servidores MCP Cubiertos

### SQLite MCP (Principal)
- **Package**: `@modelcontextprotocol/server-sqlite`
- **Herramientas**: query, schema, list_tables, execute
- **Uso**: Consultas a bases de datos SQLite

### Otros Mencionados
- Filesystem MCP: Lectura/escritura de archivos
- GitHub MCP: Integración con GitHub API
- Custom MCP: Tus propios servidores FastMCP

## 💡 Casos de Uso Reales

### 1. Análisis de Datos
Agente que consulta bases de datos y genera insights

### 2. Automatización
Combinar múltiples servidores para flujos complejos

### 3. Chatbots Empresariales
Acceso seguro a datos corporativos

### 4. Herramientas de Desarrollo
Integración con GitHub, Docker, etc.

## 📖 Recursos Adicionales

### Documentación Oficial
- [MCP Servers Directory](https://github.com/modelcontextprotocol/servers)
- [SQLite MCP Docs](https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite)
- [Creating MCP Servers](https://modelcontextprotocol.io/docs/creating-servers)

### Comunidad
- [MCP GitHub Discussions](https://github.com/modelcontextprotocol/mcp/discussions)
- [Awesome MCP](https://github.com/punkpeye/awesome-mcp) - Lista curada

### Jupyter
- [Jupyter Documentation](https://jupyter.org/documentation)
- [JupyterLab Documentation](https://jupyterlab.readthedocs.io/)

## ⚠️ Troubleshooting Común

### Jupyter no inicia
```bash
pip install --upgrade jupyter notebook
```

### Error: kernel muerto
- Reinicia el kernel: Kernel → Restart
- Verifica que el entorno virtual esté activado

### Servidor MCP no conecta
- Verifica que el servidor esté corriendo
- Comprueba el puerto correcto (3000 por defecto)
- Revisa logs del servidor para errores

### Errores de import
```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- ✅ Instalar y ejecutar servidores MCP existentes
- ✅ Conectar agentes Python a servidores npm
- ✅ Usar SQLite MCP para consultas de base de datos
- ✅ Combinar múltiples servidores MCP
- ✅ Decidir cuándo usar servidores existentes vs crear propios
- ✅ Explorar el ecosistema MCP completo

## 🚦 Progresión Sugerida

```
1. Completa Notebook 1 → Entiende el ecosistema
2. Completa Notebook 2 → Usa SQLite MCP
3. Completa Notebook 3 → Crea agente completo
4. Completa Notebook 4 → Múltiples servidores
5. Experimenta libremente → Prueba otros servidores
```

## 🤝 Soporte

Para preguntas o problemas:
1. Revisa la sección de troubleshooting
2. Consulta la documentación de MCP
3. Busca en GitHub Discussions
4. Revisa los notebooks de ejemplo

## ⏭️ Próximos Pasos

Después de completar este módulo:

1. **Explora otros servidores**: Filesystem, GitHub, Google Maps
2. **Combina con tus servidores**: Usa FastMCP + servidores existentes
3. **Contribuye**: Crea y comparte tus propios servidores
4. **Aplica**: Integra en proyectos reales

---

**¿Listo para comenzar?** 

Inicia Jupyter y abre: [`01_introduccion_mcps_existentes.ipynb`](./01_introduccion_mcps_existentes.ipynb)

**Tip**: Usa `Shift + Enter` para ejecutar cada celda de código en los notebooks.

