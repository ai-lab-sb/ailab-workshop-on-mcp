"""
Servidor MCP con herramientas de validación de datos.
Incluye validación de emails, passwords, URLs y números de teléfono.
"""

from typing import Dict, Any
from fastmcp import FastMCP
import re

app = FastMCP("Data Validation Server")

@app.tool
def validar_email(email: str) -> Dict[str, Any]:
    """
    Valida un email y retorna información sobre su estructura.
    
    Args:
        email: Dirección de email a validar
        
    Returns:
        Diccionario con validez, usuario y dominio
    """
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    es_valido = bool(re.match(patron, email))
    
    if es_valido:
        usuario, dominio = email.split('@')
        return {
            "valido": True,
            "usuario": usuario,
            "dominio": dominio,
            "longitud": len(email)
        }
    else:
        return {
            "valido": False,
            "error": "Formato de email inválido"
        }

@app.tool
def validar_password(password: str) -> Dict[str, Any]:
    """
    Valida la fortaleza de una contraseña.
    
    Requisitos:
    - Mínimo 8 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un número
    - Al menos un carácter especial
    
    Args:
        password: Contraseña a validar
        
    Returns:
        Diccionario con validez, errores y nivel de fortaleza
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
    
    fortaleza = "débil"
    if len(errores) == 0:
        fortaleza = "fuerte"
    elif len(errores) <= 2:
        fortaleza = "media"
    
    return {
        "valida": len(errores) == 0,
        "errores": errores,
        "fortaleza": fortaleza,
        "longitud": len(password)
    }

@app.tool
def validar_url(url: str) -> Dict[str, Any]:
    """
    Valida una URL y extrae sus componentes.
    
    Args:
        url: URL a validar
        
    Returns:
        Diccionario con validez y componentes de la URL
    """
    patron = r'^(https?://)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/.*)?$'
    es_valida = bool(re.match(patron, url))
    
    if es_valida:
        tiene_protocolo = url.startswith('http://') or url.startswith('https://')
        tiene_www = 'www.' in url
        
        dominio_match = re.search(r'([a-zA-Z0-9-]+\.[a-zA-Z]{2,})', url)
        dominio = dominio_match.group(1) if dominio_match else "desconocido"
        
        return {
            "valida": True,
            "tiene_protocolo": tiene_protocolo,
            "tiene_www": tiene_www,
            "dominio": dominio
        }
    else:
        return {
            "valida": False,
            "error": "Formato de URL inválido"
        }

@app.tool
def validar_telefono(telefono: str, pais: str = "CO") -> Dict[str, Any]:
    """
    Valida un número de teléfono.
    
    Args:
        telefono: Número de teléfono a validar
        pais: Código de país (CO, US, ES, etc.)
        
    Returns:
        Diccionario con validez y formato
    """
    telefono_limpio = re.sub(r'[\s\-\(\)]', '', telefono)
    
    patrones = {
        "CO": r'^(\+57)?[0-9]{10}$',
        "US": r'^(\+1)?[0-9]{10}$',
        "ES": r'^(\+34)?[0-9]{9}$',
        "MX": r'^(\+52)?[0-9]{10}$'
    }
    
    if pais not in patrones:
        return {
            "valido": False,
            "error": f"País {pais} no soportado"
        }
    
    es_valido = bool(re.match(patrones[pais], telefono_limpio))
    
    if es_valido:
        tiene_codigo = telefono_limpio.startswith('+')
        return {
            "valido": True,
            "pais": pais,
            "tiene_codigo_pais": tiene_codigo,
            "telefono_limpio": telefono_limpio
        }
    else:
        return {
            "valido": False,
            "error": f"Formato inválido para país {pais}"
        }

@app.tool
def validar_rango_numerico(
    valor: float,
    minimo: float,
    maximo: float,
    inclusive: bool = True
) -> Dict[str, Any]:
    """
    Valida que un número esté dentro de un rango.
    
    Args:
        valor: Número a validar
        minimo: Valor mínimo del rango
        maximo: Valor máximo del rango
        inclusive: Si los extremos están incluidos
        
    Returns:
        Diccionario con validez y posición en el rango
    """
    if inclusive:
        es_valido = minimo <= valor <= maximo
    else:
        es_valido = minimo < valor < maximo
    
    if es_valido:
        porcentaje = ((valor - minimo) / (maximo - minimo)) * 100
        return {
            "valido": True,
            "porcentaje_en_rango": round(porcentaje, 2)
        }
    else:
        fuera_por = "abajo" if valor < minimo else "arriba"
        return {
            "valido": False,
            "error": f"Valor fuera del rango por {fuera_por}"
        }

if __name__ == "__main__":
    # Usa stdio para comunicación directa entre procesos
    app.run()
