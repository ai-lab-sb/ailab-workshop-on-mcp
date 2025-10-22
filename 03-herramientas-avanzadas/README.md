# Módulo 3: Herramientas Avanzadas

## Herramientas Complejas en MCP

En este módulo aprenderás a crear herramientas más sofisticadas que manejan:
- Validación compleja de datos
- Procesamiento de estructuras de datos
- Manejo robusto de errores
- Operaciones con múltiples pasos

## Validación de Datos

### Validación Básica con Type Hints

Python type hints proporcionan validación automática:

```python
from typing import List, Dict, Optional

@app.tool
def procesar_usuarios(
    usuarios: List[Dict[str, str]],
    filtro: Optional[str] = None
) -> List[Dict[str, str]]:
    """FastMCP valida que usuarios sea una lista de diccionarios"""
    if filtro:
        return [u for u in usuarios if filtro in u.get('nombre', '')]
    return usuarios
```

### Validación Personalizada

Para reglas de negocio específicas:

```python
@app.tool
def crear_usuario(nombre: str, edad: int, email: str) -> Dict[str, str]:
    """
    Crea un nuevo usuario con validaciones.
    
    Raises:
        ValueError: Si los datos no son válidos
    """
    # Validar nombre
    if len(nombre) < 2:
        raise ValueError("El nombre debe tener al menos 2 caracteres")
    
    # Validar edad
    if edad < 0 or edad > 150:
        raise ValueError("Edad debe estar entre 0 y 150")
    
    # Validar email
    if '@' not in email or '.' not in email:
        raise ValueError("Email inválido")
    
    return {
        "id": "generated_id",
        "nombre": nombre,
        "edad": str(edad),
        "email": email
    }
```

## Procesamiento de Texto

El archivo `servidor_texto.py` implementa herramientas de procesamiento de texto:

### Operaciones Incluidas

1. **Análisis de texto**: Contar palabras, caracteres, oraciones
2. **Transformaciones**: Mayúsculas, minúsculas, capitalización
3. **Búsqueda**: Encontrar palabras o frases
4. **Limpieza**: Eliminar espacios, caracteres especiales

### Ejemplo de Implementación

```python
@app.tool
def analizar_texto(texto: str) -> Dict[str, int]:
    """
    Analiza un texto y retorna estadísticas.
    
    Returns:
        Diccionario con: palabras, caracteres, oraciones, párrafos
    """
    palabras = len(texto.split())
    caracteres = len(texto)
    oraciones = texto.count('.') + texto.count('!') + texto.count('?')
    parrafos = len([p for p in texto.split('\n\n') if p.strip()])
    
    return {
        "palabras": palabras,
        "caracteres": caracteres,
        "oraciones": oraciones,
        "parrafos": parrafos
    }
```

## Manejo de Errores Avanzado

### Jerarquía de Excepciones

Crea excepciones personalizadas para diferentes tipos de errores:

```python
class ValidationError(Exception):
    """Error de validación de datos"""
    pass

class ProcessingError(Exception):
    """Error durante el procesamiento"""
    pass

class ResourceNotFoundError(Exception):
    """Recurso no encontrado"""
    pass
```

### Uso en Herramientas

```python
@app.tool
def buscar_producto(id_producto: str) -> Dict[str, Any]:
    """
    Busca un producto por ID.
    
    Raises:
        ValidationError: Si el ID es inválido
        ResourceNotFoundError: Si el producto no existe
    """
    # Validar formato de ID
    if not id_producto.isalnum():
        raise ValidationError("El ID debe ser alfanumérico")
    
    # Buscar producto (simulado)
    productos = {"ABC123": {"nombre": "Laptop", "precio": 999}}
    
    if id_producto not in productos:
        raise ResourceNotFoundError(f"Producto {id_producto} no encontrado")
    
    return productos[id_producto]
```

## Operaciones con Múltiples Pasos

Algunas herramientas requieren varios pasos de procesamiento:

```python
@app.tool
def procesar_documento(
    contenido: str,
    formato: str,
    opciones: Optional[Dict[str, bool]] = None
) -> Dict[str, Any]:
    """
    Procesa un documento con múltiples transformaciones.
    
    Args:
        contenido: Texto del documento
        formato: Formato de salida (json, markdown, html)
        opciones: Opciones de procesamiento
    """
    opciones = opciones or {}
    
    # Paso 1: Limpieza
    contenido_limpio = contenido.strip()
    if opciones.get("remover_espacios_extra", True):
        contenido_limpio = " ".join(contenido_limpio.split())
    
    # Paso 2: Análisis
    palabras = contenido_limpio.split()
    estadisticas = {
        "palabras": len(palabras),
        "caracteres": len(contenido_limpio)
    }
    
    # Paso 3: Formateo
    if formato == "json":
        resultado = {
            "contenido": contenido_limpio,
            "estadisticas": estadisticas
        }
    elif formato == "markdown":
        resultado = {
            "contenido": f"# Documento\n\n{contenido_limpio}\n\n---\n*{estadisticas['palabras']} palabras*"
        }
    else:
        resultado = {"contenido": contenido_limpio}
    
    return resultado
```

## Trabajando con Estructuras de Datos

### Listas Complejas

```python
from typing import List, Dict

@app.tool
def filtrar_productos(
    productos: List[Dict[str, Any]],
    precio_min: float,
    precio_max: float,
    categoria: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Filtra productos por precio y categoría.
    
    Args:
        productos: Lista de productos con precio y categoria
        precio_min: Precio mínimo
        precio_max: Precio máximo
        categoria: Categoría opcional
    """
    resultado = []
    
    for producto in productos:
        precio = producto.get('precio', 0)
        cat = producto.get('categoria', '')
        
        # Filtrar por precio
        if precio < precio_min or precio > precio_max:
            continue
        
        # Filtrar por categoría si se especifica
        if categoria and cat != categoria:
            continue
        
        resultado.append(producto)
    
    return resultado
```

### Diccionarios Anidados

```python
@app.tool
def extraer_campos(
    data: Dict[str, Any],
    campos: List[str]
) -> Dict[str, Any]:
    """
    Extrae campos específicos de un diccionario anidado.
    
    Soporta notación de punto: 'usuario.perfil.nombre'
    """
    resultado = {}
    
    for campo in campos:
        partes = campo.split('.')
        valor = data
        
        # Navegar por el diccionario anidado
        try:
            for parte in partes:
                valor = valor[parte]
            resultado[campo] = valor
        except (KeyError, TypeError):
            resultado[campo] = None
    
    return resultado
```

## Validaciones con el Módulo servidor_validaciones.py

Este servidor implementa herramientas con validaciones robustas:

### Validación de Email
```python
import re

@app.tool
def validar_email(email: str) -> Dict[str, Any]:
    """Valida formato de email y retorna información"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    es_valido = bool(re.match(patron, email))
    
    if es_valido:
        usuario, dominio = email.split('@')
        return {
            "valido": True,
            "usuario": usuario,
            "dominio": dominio
        }
    else:
        return {"valido": False, "error": "Formato inválido"}
```

### Validación de Contraseña
```python
@app.tool
def validar_password(password: str) -> Dict[str, Any]:
    """
    Valida fortaleza de contraseña.
    
    Requisitos:
    - Mínimo 8 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un número
    - Al menos un carácter especial
    """
    errores = []
    
    if len(password) < 8:
        errores.append("Debe tener al menos 8 caracteres")
    if not re.search(r'[A-Z]', password):
        errores.append("Debe tener al menos una mayúscula")
    if not re.search(r'[a-z]', password):
        errores.append("Debe tener al menos una minúscula")
    if not re.search(r'\d', password):
        errores.append("Debe tener al menos un número")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errores.append("Debe tener al menos un carácter especial")
    
    return {
        "valida": len(errores) == 0,
        "errores": errores,
        "fortaleza": "fuerte" if len(errores) == 0 else "débil"
    }
```

## Patrones de Diseño

### Patrón: Validar-Procesar-Retornar

```python
@app.tool
def procesar_pedido(pedido: Dict[str, Any]) -> Dict[str, Any]:
    """Procesa un pedido con validación completa"""
    
    # 1. Validar
    if 'items' not in pedido or not pedido['items']:
        raise ValueError("El pedido debe tener items")
    
    if 'cliente_id' not in pedido:
        raise ValueError("Se requiere cliente_id")
    
    # 2. Procesar
    total = sum(item['precio'] * item['cantidad'] 
                for item in pedido['items'])
    
    # 3. Retornar
    return {
        "pedido_id": "generated_id",
        "cliente_id": pedido['cliente_id'],
        "total": total,
        "items": len(pedido['items']),
        "estado": "procesado"
    }
```

### Patrón: Try-Except-Log

```python
import logging

@app.tool
def operacion_riesgosa(data: Dict[str, Any]) -> Dict[str, Any]:
    """Operación que puede fallar"""
    try:
        # Operación principal
        resultado = procesar_data(data)
        return {"exito": True, "resultado": resultado}
        
    except ValueError as e:
        logging.error(f"Error de validación: {e}")
        raise ValueError(f"Datos inválidos: {e}")
        
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        raise Exception(f"Error al procesar: {e}")
```

## Ejercicios

### Ejercicio 1: Validador de Datos
Crea un servidor con herramientas para validar:
- Números de teléfono
- URLs
- Códigos postales
- Números de tarjeta de crédito (formato)

### Ejercicio 2: Procesador de JSON
Crea herramientas para:
- Aplanar JSON anidado
- Extraer valores por path
- Fusionar dos JSONs
- Comparar dos JSONs

### Ejercicio 3: Analizador de Logs
Crea herramientas para:
- Contar errores en logs
- Extraer timestamps
- Filtrar por nivel de log
- Generar resumen de logs

## Próximos Pasos

Continúa con el **Módulo 4** para aprender sobre recursos y prompts en MCP.

**Archivos del módulo**:
- [`servidor_texto.py`](./servidor_texto.py)
- [`servidor_validaciones.py`](./servidor_validaciones.py)
