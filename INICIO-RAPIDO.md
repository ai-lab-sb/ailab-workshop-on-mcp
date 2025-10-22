# Inicio Rápido - MCP Workshop

Esta guía te ayudará a comenzar con el workshop en menos de 10 minutos.

## ⚡ Setup Express (5 minutos)

### 1. Crear Entorno Virtual

```powershell
# Navega a la carpeta del workshop
cd mcp-workshop

# Crea entorno virtual
python -m venv venv

# Activa el entorno
.\venv\Scripts\activate
```

### 2. Instalar Dependencias

```powershell
pip install -r requirements.txt
```

Esto instalará:
- fastmcp
- langchain-google-genai
- langgraph
- langchain-mcp-adapters
- fastapi, uvicorn
- Y otras dependencias

### 3. Configurar API Key

```powershell
# Copia el archivo de ejemplo
copy .env.example .env

# Edita .env y agrega tu API key
notepad .env
```

Obtén tu API key en: https://makersuite.google.com/app/apikey

## 🎯 Primera Prueba (2 minutos)

### Opción A: Servidor Simple

```powershell
cd 01-fundamentos
python ejemplo_simple.py
```

Deberías ver:
```
Iniciando servidor MCP de conversión de temperaturas...
Puerto: 8100
```

### Opción B: Servidor con Herramientas

```powershell
cd 02-fastmcp-basico
python servidor_math.py
```

Deberías ver:
```
Servidor MCP - Operaciones Matemáticas
Iniciando servidor en http://localhost:8001
```

## 🧪 Probar el Servidor (3 minutos)

### Con el Script de Testing

Abre una **nueva terminal**:

```powershell
cd 02-fastmcp-basico
python test_servidor.py
```

Presiona Enter y verás tests ejecutándose.

### Con curl (Opcional)

```powershell
# Listar herramientas
curl http://localhost:8001/mcp/tools

# Llamar herramienta
curl -X POST http://localhost:8001/mcp/call_tool `
  -H "Content-Type: application/json" `
  -d '{\"name\":\"add\",\"arguments\":{\"a\":5,\"b\":3}}'
```

## 🚀 Proyecto Final (10 minutos)

### Terminal 1: Servidor MCP

```powershell
cd 07-proyecto-final
python servidor_tienda.py
```

### Terminal 2: API REST

```powershell
cd 07-proyecto-final
python api_rest.py
```

### Terminal 3: Testing

```powershell
cd 07-proyecto-final
python test_agente.py
```

## 📖 Siguientes Pasos

### Ruta de Aprendizaje Recomendada

1. **Día 1** (2-3 horas):
   - Módulo 1: Fundamentos
   - Módulo 2: FastMCP Básico
   - Ejecuta ejemplos

2. **Día 2** (2-3 horas):
   - Módulo 3: Herramientas Avanzadas
   - Módulo 4: Recursos y Prompts
   - Completa ejercicios

3. **Día 3** (2-3 horas):
   - Módulo 5: Base de Datos
   - Módulo 6: LangChain Integration

4. **Día 4** (2-3 horas):
   - Módulo 7: Proyecto Final
   - Personaliza el proyecto

## 🛠️ Troubleshooting

### Error: "Import fastmcp could not be resolved"

```powershell
# Verifica que el entorno virtual esté activado
# Deberías ver (venv) en tu prompt

# Reinstala
pip install --upgrade fastmcp
```

### Error: "GOOGLE_API_KEY not found"

```powershell
# Verifica el archivo .env
type .env

# Debe contener:
# GOOGLE_API_KEY=tu_clave_aqui
```

### Error: "Connection refused"

El servidor MCP no está corriendo. Ejecuta:
```powershell
python servidor_math.py
```

### Puerto en Uso

Si el puerto 8001 está ocupado, cambia en el código:
```python
app.run(transport="streamable-http", host="0.0.0.0", port=8999)
```

## 📚 Recursos Rápidos

### Documentación
- [MCP Official](https://modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)

### Comandos Útiles

```powershell
# Ver puertos en uso
netstat -ano | findstr ":8001"

# Matar proceso en puerto
taskkill /PID <pid> /F

# Listar paquetes instalados
pip list

# Actualizar paquete
pip install --upgrade <paquete>
```

## ✅ Checklist de Verificación

Antes de comenzar el workshop, verifica:

- [ ] Python 3.10+ instalado (`python --version`)
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip list | findstr fastmcp`)
- [ ] Archivo .env configurado con API key
- [ ] Primer servidor ejecutado exitosamente
- [ ] Tests pasados correctamente

## 💡 Consejos

1. **Lee los READMEs**: Cada módulo tiene explicaciones detalladas
2. **Ejecuta el código**: No solo leas, ejecuta y modifica
3. **Usa comentarios**: El código está comentado para facilitar el aprendizaje
4. **Experimenta**: Modifica parámetros y observa resultados
5. **Consulta docs**: Los enlaces a documentación oficial son útiles

## 🎓 Después del Workshop

- Personaliza el proyecto final para tu caso de uso
- Explora servidores MCP de la comunidad
- Crea tu propio servidor MCP
- Comparte tu experiencia

---

**¿Listo?** Comienza con [`01-fundamentos/README.md`](./01-fundamentos/README.md)

**¿Problemas?** Revisa la sección de Troubleshooting arriba.

¡Éxito en tu aprendizaje de MCP! 🚀
