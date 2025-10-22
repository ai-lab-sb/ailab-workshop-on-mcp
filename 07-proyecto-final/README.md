# Módulo 7: Proyecto Final - Agente de Tienda con MCP

## Descripción del Proyecto

En este módulo construirás un **sistema completo de agente conversacional** que consulta una base de datos de productos y clientes via MCP. El proyecto incluye:

1. **Servidor MCP** con base de datos SQLite
2. **Agente LangGraph** que consume el servidor MCP
3. **API REST** para exponer el agente
4. **Testing completo** del sistema

Este es un proyecto de nivel producción que demuestra la integración completa de MCP en una aplicación real.

## Arquitectura del Sistema

```
┌─────────────────┐
│   Cliente Web   │
│   o Postman     │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│   API REST      │
│   (FastAPI)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐         MCP          ┌─────────────────┐
│  Agente         │◄─────────────────────►│  Servidor MCP   │
│  LangGraph      │   (langchain-mcp)    │  Base de Datos  │
│  + Memoria      │                      └────────┬────────┘
└─────────────────┘                              │
                                                 ▼
                                          ┌──────────────┐
                                          │   SQLite     │
                                          │  tienda.db   │
                                          └──────────────┘
```

## Componentes del Proyecto

### 1. servidor_tienda.py

Servidor MCP completo con:
- Consultas de productos (por ID, categoría, precio)
- Consultas de clientes (por ID, ciudad)
- Estadísticas y agregaciones
- Búsquedas avanzadas

**Herramientas disponibles**:
- `obtener_todos_productos()` - Lista todos los productos
- `buscar_producto_por_id(id)` - Busca producto específico
- `buscar_productos_por_categoria(categoria)` - Filtra por categoría
- `buscar_productos_por_precio(min, max)` - Filtra por rango de precio
- `productos_en_stock()` - Solo productos disponibles
- `obtener_todos_clientes()` - Lista todos los clientes
- `buscar_cliente_por_id(id)` - Busca cliente específico
- `buscar_clientes_por_ciudad(ciudad)` - Filtra por ciudad

### 2. agente_tienda.py

Agente LangGraph con:
- Integración con servidor MCP
- Memoria de conversación (threads)
- System message especializado
- Manejo robusto de errores

**Características**:
- Solo responde sobre productos y clientes
- Usa herramientas MCP automáticamente
- Mantiene contexto de conversación
- Proporciona respuestas claras y estructuradas

### 3. api_rest.py

API REST con FastAPI:
- Endpoint `/chat` para conversar con el agente
- Endpoint `/history` para ver historial
- Endpoint `/health` para verificar estado
- Soporte para múltiples threads de conversación

**Endpoints**:
```
POST /chat
GET /history/{thread_id}
GET /health
```

### 4. test_agente.py

Suite de testing completa:
- Tests de servidor MCP
- Tests del agente LangGraph
- Tests de la API REST
- Tests de integración end-to-end

## Instalación y Configuración

### 1. Dependencias

Todas las dependencias ya están en el `requirements.txt` general del workshop.

### 2. Variables de Entorno

Crea un archivo `.env` en la raíz del workshop:

```bash
GOOGLE_API_KEY=tu_api_key_aqui
```

Obtén tu API key en: https://makersuite.google.com/app/apikey

### 3. Inicializar Base de Datos

```bash
cd 07-proyecto-final
python -c "from servidor_tienda import init_database; init_database()"
```

## Ejecución del Proyecto

### Paso 1: Iniciar Servidor MCP

```bash
# Terminal 1
cd 07-proyecto-final
python servidor_tienda.py
```

Debe mostrar:
```
Servidor MCP - Tienda
Iniciando servidor en http://localhost:8200
```

### Paso 2: Probar Agente Directamente (Opcional)

```bash
# Terminal 2
python agente_tienda.py
```

Esto ejecuta una demo del agente con preguntas predefinidas.

### Paso 3: Iniciar API REST

```bash
# Terminal 2 (o 3 si usaste el paso 2)
python api_rest.py
```

Debe mostrar:
```
API REST - Agente de Tienda
Accede a http://localhost:8000/docs
```

### Paso 4: Probar con Postman o curl

**Verificar salud**:
```bash
curl http://localhost:8000/health
```

**Enviar mensaje**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Qué productos tienes?",
    "thread_id": "usuario_1"
  }'
```

**Ver historial**:
```bash
curl http://localhost:8000/history/usuario_1
```

## Uso de la API

### Endpoint: POST /chat

Envía un mensaje al agente y recibe respuesta.

**Request**:
```json
{
  "message": "Muéstrame los productos de Electrónica",
  "thread_id": "usuario_1"
}
```

**Response**:
```json
{
  "response": "Tenemos 4 productos en la categoría Electrónica:\n\n1. Laptop Dell XPS - $999.99 (15 en stock)\n2. Mouse Logitech - $29.99 (50 en stock)\n3. Teclado Mecánico - $79.99 (30 en stock)\n4. Monitor 24 pulgadas - $299.99 (20 en stock)",
  "thread_id": "usuario_1",
  "tools_used": [
    {
      "name": "buscar_productos_por_categoria",
      "args": {"categoria": "Electrónica"}
    }
  ]
}
```

### Endpoint: GET /history/{thread_id}

Obtiene el historial de conversación de un thread.

**Response**:
```json
{
  "thread_id": "usuario_1",
  "messages": [
    {
      "type": "human",
      "content": "Muéstrame los productos de Electrónica"
    },
    {
      "type": "ai",
      "content": "Tenemos 4 productos en la categoría Electrónica..."
    }
  ]
}
```

### Endpoint: GET /health

Verifica el estado del sistema.

**Response**:
```json
{
  "status": "healthy",
  "mcp_server": "connected",
  "database": "ready"
}
```

## Flujo de Conversación

El agente mantiene contexto entre mensajes usando threads:

```python
# Primera pregunta
POST /chat
{
  "message": "¿Qué productos tienes?",
  "thread_id": "user_123"
}
# Respuesta: Lista de productos

# Segunda pregunta (usa contexto)
POST /chat
{
  "message": "¿Cuáles son los más baratos?",
  "thread_id": "user_123"
}
# El agente recuerda que ya mostró productos
```

## Testing

### Ejecutar Tests

```bash
cd 07-proyecto-final
python test_agente.py
```

Los tests verifican:
1. ✅ Servidor MCP responde
2. ✅ Herramientas MCP funcionan
3. ✅ Agente se inicializa correctamente
4. ✅ Agente responde preguntas
5. ✅ API REST está disponible
6. ✅ Endpoints retornan datos correctos

### Tests Manuales

**Test 1: Consulta Simple**
```
Pregunta: "¿Cuántos productos tienes?"
Esperado: Usa obtener_todos_productos() y cuenta
```

**Test 2: Búsqueda por Categoría**
```
Pregunta: "Muéstrame productos de Muebles"
Esperado: Usa buscar_productos_por_categoria("Muebles")
```

**Test 3: Filtro por Precio**
```
Pregunta: "¿Qué productos cuestan menos de $100?"
Esperado: Usa buscar_productos_por_precio(0, 100)
```

**Test 4: Consulta de Clientes**
```
Pregunta: "¿Qué clientes tengo en Bogotá?"
Esperado: Usa buscar_clientes_por_ciudad("Bogotá")
```

**Test 5: Pregunta Fuera de Dominio**
```
Pregunta: "¿Cuál es la capital de Francia?"
Esperado: "Lo siento, solo puedo ayudar con consultas sobre productos y clientes"
```

## Personalización

### Cambiar el System Message

Edita `agente_tienda.py` para modificar el comportamiento:

```python
self.system_message = SystemMessage(
    content="""Eres un asistente de ventas amigable...
    
    - Saluda siempre al cliente
    - Ofrece recomendaciones
    - Pregunta si necesita algo más
    """
)
```

### Añadir Más Herramientas

En `servidor_tienda.py`:

```python
@app.tool
def recomendar_productos(categoria: str, presupuesto: float) -> List[Dict]:
    """Recomienda productos según categoría y presupuesto"""
    # Tu lógica aquí
    pass
```

El agente las usará automáticamente.

### Modificar la Base de Datos

Ejecuta `init_db.py` del módulo 5 para resetear y personalizar datos.

## Despliegue a Producción

### Consideraciones

1. **Base de Datos**: Migrar de SQLite a PostgreSQL
2. **Seguridad**: Añadir autenticación (JWT tokens)
3. **Rate Limiting**: Limitar requests por usuario
4. **Logging**: Registrar todas las interacciones
5. **Monitoring**: Métricas de uso y rendimiento

### Docker (Opcional)

Crear `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY 07-proyecto-final/ .

EXPOSE 8000 8200

CMD ["python", "api_rest.py"]
```

## Ejercicios de Extensión

### Ejercicio 1: Carrito de Compras
Añade funcionalidad de carrito:
- Agregar producto al carrito
- Ver carrito actual
- Calcular total

### Ejercicio 2: Recomendaciones
Implementa sistema de recomendaciones:
- Productos similares
- Frecuentemente comprados juntos
- Basado en historial del cliente

### Ejercicio 3: Multilenguaje
Soporte para varios idiomas:
- Detectar idioma del usuario
- Responder en el idioma correspondiente
- Mantener nombres de productos originales

### Ejercicio 4: Analytics
Dashboard de analíticas:
- Productos más consultados
- Preguntas más frecuentes
- Tasa de conversión (consulta → compra)

## Recursos del Proyecto

**Archivos**:
- [`servidor_tienda.py`](./servidor_tienda.py) - Servidor MCP
- [`agente_tienda.py`](./agente_tienda.py) - Agente LangGraph
- [`api_rest.py`](./api_rest.py) - API REST con FastAPI
- [`test_agente.py`](./test_agente.py) - Suite de testing

## Conclusión

¡Felicitaciones! Has completado el workshop de MCP con FastMCP.

Has aprendido:
- ✅ Fundamentos de Model Context Protocol
- ✅ Crear servidores MCP con FastMCP
- ✅ Herramientas avanzadas y validaciones
- ✅ Integración con bases de datos
- ✅ Conectar MCP con LangGraph
- ✅ Construir agentes conversacionales completos
- ✅ Exponer agentes via API REST

**Próximos pasos**:
1. Personaliza el proyecto para tu caso de uso
2. Explora servidores MCP de la comunidad
3. Contribuye al ecosistema MCP
4. Comparte tu experiencia

---

**¿Preguntas?** Revisa la documentación oficial de [MCP](https://modelcontextprotocol.io/) y [FastMCP](https://github.com/jlowin/fastmcp).
