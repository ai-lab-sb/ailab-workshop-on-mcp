# Módulo 2: FastMCP Básico

## Introducción a FastMCP

En este módulo aprenderás a crear servidores MCP usando **FastMCP**, un framework moderno que simplifica enormemente el desarrollo de servidores MCP.

## ¿Por Qué FastMCP?

### Comparación con MCP Nativo

**MCP Nativo (Sin Framework)**:
```python
# Código verboso, manejo manual del protocolo
class MyServer:
    def __init__(self):
        self.setup_protocol()
        self.register_handlers()
    
    async def handle_tool_call(self, request):
        # Parsear JSON, validar, ejecutar, serializar...
        pass
```

**Con FastMCP**:
```python
# Simple, declarativo, automático
@app.tool
def my_tool(param: str) -> str:
    return f"Resultado: {param}"
```

FastMCP maneja automáticamente:
- Serialización/deserialización JSON
- Validación de tipos
- Manejo de errores
- Documentación automática
- Registro de herramientas

## Componentes de un Servidor FastMCP

### 1. Instancia de FastMCP

```python
from fastmcp import FastMCP

app = FastMCP("Nombre del Servidor")
```

El nombre identifica tu servidor en el ecosistema MCP.

### 2. Decorador @app.tool

Define herramientas que los clientes pueden ejecutar:

```python
@app.tool
def nombre_herramienta(parametro: tipo) -> tipo_retorno:
    """Descripción de la herramienta"""
    # Lógica de la herramienta
    return resultado
```

**Elementos importantes**:
- **Type hints**: Obligatorios para validación automática
- **Docstring**: Se usa como descripción de la herramienta
- **Return type**: Define el tipo de respuesta

### 3. Ejecución del Servidor

```python
if __name__ == "__main__":
    # Para pruebas locales, usar stdio (comunicación directa entre procesos)
    app.run()
```

**Modos de Transporte**:

- **`stdio`** (por defecto): Comunicación directa entre procesos. **Recomendado para desarrollo y pruebas locales**
  - ✅ Más simple y confiable
  - ✅ No requiere configurar puertos
  - ✅ El cliente inicia/detiene el servidor automáticamente
  - ✅ Ideal para testing y desarrollo

- **`sse`** (Server-Sent Events): Comunicación HTTP con eventos
  ```python
  app.run(transport="sse", host="0.0.0.0", port=8000)
  ```
  - Requiere cliente compatible con SSE
  - Útil para integraciones web

- **`streamable-http`**: HTTP con streaming
  ```python
  app.run(transport="streamable-http", host="0.0.0.0", port=8000)
  ```
  - Para casos de uso avanzados con streaming, por ejemplo, casos con FastAPI

**💡 Nota importante**: Para este workshop usamos `stdio` porque es más simple y confiable para pruebas locales. No necesitas iniciar el servidor manualmente, el cliente de pruebas lo hace automáticamente.

## Tipos de Datos Soportados

FastMCP soporta tipos nativos de Python:

### Tipos Básicos
```python
@app.tool
def ejemplos_tipos(
    entero: int,
    flotante: float,
    texto: str,
    booleano: bool
) -> str:
    return "Todos los tipos básicos funcionan"
```

### Listas y Diccionarios
```python
from typing import List, Dict, Any

@app.tool
def procesar_lista(items: List[str]) -> List[str]:
    return [item.upper() for item in items]

@app.tool
def procesar_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {"procesado": True, "original": data}
```

### Tipos Opcionales
```python
from typing import Optional

@app.tool
def buscar(query: str, limite: Optional[int] = 10) -> List[str]:
    """El parámetro limite es opcional con valor por defecto"""
    return ["resultado1", "resultado2"][:limite]
```

## Operaciones Matemáticas: Ejemplo Completo

El archivo `servidor_math.py` implementa un servidor con operaciones matemáticas básicas:

### Características
- ✅ Cuatro operaciones: suma, resta, multiplicación, división
- ✅ Validación automática de tipos
- ✅ Manejo de errores (división por cero)
- ✅ Documentación completa

### Flujo de Ejecución

1. **Cliente descubre herramientas**:
   ```
   GET /mcp/tools
   ```

2. **Servidor responde**:
   ```json
   {
     "tools": [
       {
         "name": "add",
         "description": "Suma dos números",
         "parameters": {
           "a": "number",
           "b": "number"
         }
       },
       ...
     ]
   }
   ```

3. **Cliente ejecuta herramienta**:
   ```
   POST /mcp/call_tool
   {
     "name": "add",
     "arguments": {"a": 5, "b": 3}
   }
   ```

4. **Servidor procesa y responde**:
   ```json
   {
     "result": 8.0
   }
   ```

## Testing del Servidor

El archivo `test_servidor.py` muestra cómo probar un servidor MCP usando comunicación **stdio**.

### ¿Por qué stdio para testing?

En este módulo usamos **stdio** (standard input/output) en lugar de HTTP porque:

1. **Más simple**: No necesitas iniciar el servidor manualmente
2. **Automático**: El cliente inicia y detiene el servidor por ti
3. **Sin conflictos**: No hay problemas con puertos ocupados
4. **Más rápido**: Comunicación directa entre procesos
5. **Menos errores**: No hay problemas de red o endpoints

### Cómo funciona stdio

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configurar el servidor
server_params = StdioServerParameters(
    command="python",
    args=["servidor_math.py"],
    env=None
)

# Conectar via stdio
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Inicializar
        await session.initialize()
        
        # Usar el servidor
        result = await session.call_tool("add", arguments={"a": 5, "b": 3})
        print(result.content[0].text)  # "8.0"
```

El cliente:
1. Ejecuta `python servidor_math.py` como subproceso
2. Se conecta a su stdin/stdout
3. Envía mensajes JSON via stdin
4. Lee respuestas desde stdout
5. Al terminar, cierra el subproceso

### Ejecutar los Tests

```bash
# No necesitas iniciar el servidor manualmente
python test_servidor.py
```

El script de test se encarga de todo automáticamente.

## Buenas Prácticas

### 1. Nombres Descriptivos
```python
# ✅ Bien
@app.tool
def calculate_compound_interest(principal: float, rate: float) -> float:
    pass

# ❌ Mal
@app.tool
def calc(p: float, r: float) -> float:
    pass
```

### 2. Docstrings Completos
```python
@app.tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Convierte una cantidad de una moneda a otra.
    
    Args:
        amount: Cantidad a convertir
        from_currency: Código de moneda origen (ej: USD)
        to_currency: Código de moneda destino (ej: EUR)
        
    Returns:
        Cantidad convertida
        
    Raises:
        ValueError: Si las monedas no son válidas
    """
    pass
```

### 3. Validación de Entradas
```python
@app.tool
def divide(a: float, b: float) -> float:
    """Divide dos números"""
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b
```

### 4. Tipos Específicos
```python
from typing import List, Dict

# ✅ Específico
@app.tool
def get_users() -> List[Dict[str, str]]:
    return [{"id": "1", "name": "Juan"}]

# ❌ Genérico
@app.tool
def get_users() -> list:
    return [{"id": "1", "name": "Juan"}]
```

## Manejo de Errores

FastMCP captura y serializa excepciones automáticamente:

```python
@app.tool
def procesar_archivo(ruta: str) -> str:
    """Lee y procesa un archivo"""
    try:
        with open(ruta, 'r') as f:
            return f.read()
    except FileNotFoundError:
        raise ValueError(f"Archivo no encontrado: {ruta}")
    except PermissionError:
        raise ValueError(f"Sin permisos para leer: {ruta}")
```

El cliente recibirá un error estructurado si algo falla.

## Ejercicios Prácticos

### Ejercicio 1: Calculadora Extendida
Extiende `servidor_math.py` para incluir:
- Potencia (`power(base, exponente)`)
- Raíz cuadrada (`sqrt(numero)`)
- Módulo (`modulo(a, b)`)

### Ejercicio 2: Conversor de Unidades
Crea un servidor que convierta:
- Kilómetros ↔ Millas
- Kilogramos ↔ Libras
- Litros ↔ Galones

### Ejercicio 3: Utilidades de Texto
Crea herramientas para:
- Contar palabras en un texto
- Convertir a mayúsculas/minúsculas
- Invertir texto
- Contar vocales y consonantes

## Próximos Pasos

Ahora que dominas FastMCP básico:

1. No necesitas iniciar `servidor_math.py` manualmente
2. Ejecuta `python test_servidor.py` (inicia el servidor automáticamente)
3. Completa los ejercicios propuestos
4. Continúa con el **Módulo 3** para herramientas avanzadas

**Archivos del módulo**:
- [`servidor_math.py`](./servidor_math.py) - Servidor de matemáticas (usa stdio)
- [`test_servidor.py`](./test_servidor.py) - Suite de testing con cliente MCP stdio
