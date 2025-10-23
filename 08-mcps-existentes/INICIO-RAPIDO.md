# Guía de Inicio Rápido - Módulo 8

## 📚 Usando Servidores MCP Existentes (Jupyter Notebooks)

Este módulo usa **Jupyter Notebooks interactivos** para enseñarte a usar servidores MCP existentes.

## 🚀 Inicio Rápido en 5 Pasos

### 1. Instalar Jupyter
```bash
pip install jupyter notebook
# O usa JupyterLab
pip install jupyterlab
```

### 2. Instalar Node.js
Los servidores MCP oficiales están en npm:
- Descarga: https://nodejs.org/
- Instala la versión LTS recomendada

### 3. Verificar Instalaciones
```bash
python --version  # 3.10+
node --version    # 18+
npm --version
```

### 4. Iniciar Jupyter
```bash
cd 08-mcps-existentes
jupyter notebook
# O
jupyter lab
```

### 5. Seguir los Notebooks en Orden
1. `01_introduccion_mcps_existentes.ipynb` - Conceptos y setup
2. `02_sqlite_mcp_basico.ipynb` - Instalar y usar SQLite MCP
3. `03_agente_con_sqlite_mcp.ipynb` - Crear agente completo
4. `04_multi_servidor.ipynb` - Múltiples servidores

## 📋 Pre-requisitos

- ✅ Python 3.10+
- ✅ Node.js 18+
- ✅ Jupyter Notebook
- ✅ Dependencias: `pip install -r requirements.txt`
- ✅ API Key: Archivo `.env` con `GOOGLE_API_KEY`

## 💡 Consejos para Jupyter

- **Ejecutar celda**: `Shift + Enter`
- **Añadir celda**: Botón `+` o `B` (abajo) / `A` (arriba)
- **Reiniciar kernel**: Kernel → Restart
- **Ver shortcuts**: Help → Keyboard Shortcuts

## 🔧 Flujo de Trabajo

1. **Notebook 1**: Verificar requisitos
2. **Antes de Notebook 2**: Ejecutar `python crear_db_ejemplo.py`
3. **Durante Notebook 2**: Iniciar servidor MCP en terminal separado
4. **Notebooks 3-4**: Experimentar con el agente

## ⚠️ Troubleshooting

### Jupyter no inicia
```bash
pip install --upgrade jupyter
```

### Servidor MCP no conecta
```bash
# Verificar que está corriendo
npx @modelcontextprotocol/server-sqlite ejemplo.db
# Debe mostrar: Server running on http://localhost:3000
```

### Error de imports
```bash
pip install -r ../requirements.txt
```

## 📖 Estructura del Módulo

```
08-mcps-existentes/
├── README.md                           # Documentación completa
├── INICIO-RAPIDO.md                    # Esta guía
├── 01_introduccion_mcps_existentes.ipynb
├── 02_sqlite_mcp_basico.ipynb
├── 03_agente_con_sqlite_mcp.ipynb
├── 04_multi_servidor.ipynb
└── crear_db_ejemplo.py                 # Utilidad
```

## 🎯 Objetivos de Aprendizaje

Después de completar este módulo:
- ✅ Instalar y ejecutar servidores MCP existentes
- ✅ Conectar agentes Python a servidores npm
- ✅ Usar SQLite MCP para consultas
- ✅ Combinar múltiples servidores
- ✅ Decidir cuándo usar existentes vs crear propios

## 🚦 Tiempo Estimado

- Notebook 1: 10-15 min
- Notebook 2: 20-30 min
- Notebook 3: 30-40 min
- Notebook 4: 15-20 min
- **Total**: ~1.5-2 horas

## 📚 Recursos

- [MCP Servers Directory](https://github.com/modelcontextprotocol/servers)
- [SQLite MCP Docs](https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite)
- [Jupyter Documentation](https://jupyter.org/documentation)

---

**¿Listo?** Inicia Jupyter y abre: `01_introduccion_mcps_existentes.ipynb`

