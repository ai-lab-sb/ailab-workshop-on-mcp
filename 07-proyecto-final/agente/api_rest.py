"""
API REST para exponer el agente de seguros.
Permite interacción con el agente via HTTP requests.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
from agente_seguros import AgenteSeguro

app = FastAPI(
    title="API Agente de Seguros",
    description="API REST para interactuar con el agente de seguros que usa MCP",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agente = None


class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    response: str
    thread_id: str
    tools_used: List[Dict[str, Any]]


class HistoryResponse(BaseModel):
    thread_id: str
    messages: List[Dict[str, Any]]


@app.on_event("startup")
async def startup_event():
    """Inicializa el agente al arrancar la API"""
    global agente
    try:
        print("Inicializando agente de seguros...")
        agente = AgenteSeguro()
        await agente.initialize()
        print("✅ Agente inicializado correctamente")
    except Exception as e:
        print(f"❌ Error al inicializar agente: {e}")
        raise


@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "API Agente de Seguros con MCP",
        "version": "1.0.0",
        "endpoints": {
            "POST /chat": "Enviar mensaje al agente",
            "GET /history/{thread_id}": "Obtener historial de conversación",
            "GET /health": "Verificar estado del sistema"
        }
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Envía un mensaje al agente y recibe una respuesta.
    
    Args:
        request: Objeto con message y thread_id opcional
        
    Returns:
        Respuesta del agente con herramientas utilizadas
    """
    if agente is None:
        raise HTTPException(status_code=503, detail="Agente no inicializado")
    
    try:
        respuesta = await agente.chat(request.message, request.thread_id)
        return ChatResponse(
            response=respuesta,
            thread_id=request.thread_id,
            tools_used=[]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar mensaje: {str(e)}")


@app.get("/history/{thread_id}", response_model=HistoryResponse)
async def get_history(thread_id: str):
    """
    Obtiene el historial de conversación de un thread específico.
    
    Args:
        thread_id: ID del thread de conversación
        
    Returns:
        Historial de mensajes del thread
    """
    if agente is None:
        raise HTTPException(status_code=503, detail="Agente no inicializado")
    
    try:
        historial = agente.get_history(thread_id)
        return HistoryResponse(thread_id=thread_id, messages=historial)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener historial: {str(e)}")


@app.get("/health")
async def health_check():
    """
    Verifica el estado del sistema.
    
    Returns:
        Estado de salud de los componentes
    """
    health_status = {
        "status": "healthy" if agente is not None else "unhealthy",
        "api": "online",
        "agente": "initialized" if agente is not None else "not_initialized"
    }
    
    # Verificar conexión con servidor MCP
    try:
        if agente and agente.tools:
            health_status["mcp_server"] = "connected"
            health_status["tools_available"] = len(agente.tools)
        else:
            health_status["mcp_server"] = "not_connected"
    except Exception:
        health_status["mcp_server"] = "error"
    
    status_code = 200 if health_status["status"] == "healthy" else 503
    return health_status


if __name__ == "__main__":
    print("=" * 60)
    print("API REST - Agente de Seguros")
    print("=" * 60)
    print("\n🚀 Iniciando servidor en http://localhost:8000")
    print("\n📋 Endpoints disponibles:")
    print("   • POST /chat                  - Enviar mensaje")
    print("   • GET /history/{thread_id}    - Ver historial")
    print("   • GET /health                 - Estado del sistema")
    print("\n📖 Documentación interactiva:")
    print("   • http://localhost:8000/docs  - Swagger UI")
    print("   • http://localhost:8000/redoc - ReDoc")
    print("\n💡 Presiona Ctrl+C para detener el servidor\n")
    print("=" * 60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
