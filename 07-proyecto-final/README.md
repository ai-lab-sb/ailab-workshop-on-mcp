# Módulo 7: Proyecto Final - Agente de Seguros con MCP

## Descripción del Proyecto

En este módulo construirás un **sistema completo de agente conversacional** para una aseguradora que consulta información de pólizas, clientes y productos de seguros via MCP. El proyecto incluye:

1. **Servidor MCP** con base de datos SQLite de seguros
2. **Agente LangGraph** que consume el servidor MCP
3. **API REST** para exponer el agente
4. **Testing completo** del sistema

Este es un proyecto de nivel producción que demuestra la integración completa de MCP en una aplicación real del sector asegurador.

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
│  LangGraph      │   (langchain-mcp)    │  Aseguradora    │
│  + Memoria      │                      └────────┬────────┘
└─────────────────┘                              │
                                                 ▼
                                          ┌──────────────┐
                                          │   SQLite     │
                                          │ seguros.db   │
                                          └──────────────┘
```

## Componentes del Proyecto

### 1. servidor/servidor_seguros.py

Servidor MCP completo con:
- Consultas de pólizas (por ID, tipo, estado)
- Consultas de clientes asegurados (por ID, ciudad)
- Productos de seguros disponibles
- Búsquedas avanzadas y filtros

**Herramientas disponibles**:
- `obtener_todas_polizas()` - Lista todas las pólizas activas
- `buscar_poliza_por_id(id)` - Busca póliza específica
- `buscar_polizas_por_cliente(cliente_id)` - Pólizas de un cliente
- `buscar_polizas_por_tipo(tipo)` - Filtra por tipo de seguro
- `obtener_productos_seguros()` - Lista productos de seguros disponibles
- `buscar_producto_seguro(id)` - Busca producto de seguro específico
- `obtener_todos_clientes()` - Lista todos los clientes asegurados
- `buscar_cliente_por_id(id)` - Busca cliente específico
- `buscar_clientes_por_ciudad(ciudad)` - Filtra clientes por ciudad

### 2. agente/agente_seguros.py

Agente LangGraph con:
- Integración con servidor MCP
- Memoria de conversación (threads)
- System message especializado en seguros
- Manejo robusto de errores

**Características**:
- Solo responde sobre pólizas, productos de seguros y clientes
- Usa herramientas MCP automáticamente
- Mantiene contexto de conversación
- Proporciona respuestas claras sobre seguros

### 3. agente/api_rest.py

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

### 4. agente/test_agente.py

Suite de testing completa (opcional):
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
cd 07-proyecto-final/servidor
python servidor_seguros.py
```

Debe mostrar:
```
Servidor MCP - Aseguradora
Iniciando servidor en http://localhost:8200
```

### Paso 2: Iniciar API REST

```bash
# Terminal 2
cd 07-proyecto-final/agente
python api_rest.py
```

Debe mostrar:
```
API REST - Agente de Seguros
Accede a http://localhost:8000/docs
```

### Paso 3: Probar desde Swagger UI

Abre tu navegador en `http://localhost:8000/docs` y verás la interfaz interactiva de Swagger donde puedes:

1. **POST /chat** - Enviar mensajes al agente
2. **GET /history/{thread_id}** - Ver historial de conversación
3. **GET /health** - Verificar estado del sistema

### Paso 4 (Opcional): Probar con curl o Postman

Si prefieres usar la línea de comandos:

**Verificar salud**:
```bash
curl http://localhost:8000/health
```

**Enviar mensaje**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Qué tipos de seguros ofrecen?",
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
  "message": "Muéstrame las pólizas de seguro de vida",
  "thread_id": "usuario_1"
}
```

**Response**:
```json
{
  "response": "Tenemos 3 pólizas activas de seguro de vida:\n\n1. Póliza #1001 - Cliente: Juan Pérez - Prima: $150.00/mes - Cobertura: $100,000.00\n2. Póliza #1004 - Cliente: Luis Rodríguez - Prima: $200.00/mes - Cobertura: $150,000.00\n3. Póliza #1006 - Cliente: Laura Fernández - Prima: $120.00/mes - Cobertura: $80,000.00",
  "thread_id": "usuario_1",
  "tools_used": [
    {
      "name": "buscar_polizas_por_tipo",
      "args": {"tipo": "Vida"}
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
  "message": "¿Qué pólizas tiene activas Juan Pérez?",
  "thread_id": "user_123"
}
# Respuesta: Lista de pólizas del cliente

# Segunda pregunta (usa contexto)
POST /chat
{
  "message": "¿Cuánto paga en total al mes?",
  "thread_id": "user_123"
}
# El agente recuerda las pólizas y calcula el total
```

## Testing

### Ejecutar Tests Automatizados (Opcional)

```bash
cd 07-proyecto-final/agente
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
Pregunta: "¿Cuántas pólizas activas hay?"
Esperado: Usa obtener_todas_polizas() y cuenta
```

**Test 2: Búsqueda por Tipo**
```
Pregunta: "Muéstrame las pólizas de seguro de auto"
Esperado: Usa buscar_polizas_por_tipo("Auto")
```

**Test 3: Consulta de Cliente**
```
Pregunta: "¿Qué seguros tiene contratados María García?"
Esperado: Busca cliente y sus pólizas
```

**Test 4: Productos Disponibles**
```
Pregunta: "¿Qué tipos de seguros ofrecen?"
Esperado: Usa obtener_productos_seguros()
```

**Test 5: Pregunta Fuera de Dominio**
```
Pregunta: "¿Cuál es la capital de Francia?"
Esperado: "Lo siento, solo puedo ayudar con consultas sobre seguros, pólizas y clientes"
```

## Personalización

### Cambiar el System Message

Edita `agente_seguros.py` para modificar el comportamiento:

```python
self.system_message = SystemMessage(
    content="""Eres un asistente de seguros profesional y empático...
    
    - Explica coberturas de forma clara
    - Ayuda a comparar pólizas
    - Responde dudas sobre seguros
    """
)
```

### Añadir Más Herramientas

En `servidor_seguros.py`:

```python
@app.tool
def calcular_prima_total_cliente(cliente_id: int) -> Dict[str, Any]:
    """Calcula el total de primas mensuales de un cliente"""
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

### Ejercicio 1: Cálculo de Cotizaciones
Añade funcionalidad de cotizaciones:
- Calcular prima según edad y cobertura
- Comparar diferentes planes
- Generar cotización personalizada

### Ejercicio 2: Renovaciones
Implementa sistema de renovaciones:
- Pólizas próximas a vencer
- Alertas de renovación
- Historial de renovaciones

### Ejercicio 3: Reclamaciones
Sistema básico de reclamaciones:
- Registrar nueva reclamación
- Consultar estado de reclamaciones
- Historial de reclamaciones por cliente

### Ejercicio 4: Analytics
Dashboard de analíticas:
- Pólizas más contratadas
- Clientes por tipo de seguro
- Ingresos por primas mensuales

## Recursos del Proyecto

**Archivos**:
- [`servidor/servidor_seguros.py`](./servidor/servidor_seguros.py) - Servidor MCP de seguros
- [`agente/agente_seguros.py`](./agente/agente_seguros.py) - Agente LangGraph especializado
- [`agente/api_rest.py`](./agente/api_rest.py) - API REST con FastAPI
- [`agente/test_agente.py`](./agente/test_agente.py) - Suite de testing (opcional)

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
