"""
Servidor MCP con herramientas de procesamiento de texto.
Incluye análisis, transformación y búsqueda en textos.
"""

from typing import Dict, List, Optional
from fastmcp import FastMCP
import re

app = FastMCP("Text Processing Server")

@app.tool
def analizar_texto(texto: str) -> Dict[str, int]:
    """
    Analiza un texto y retorna estadísticas completas.
    
    Args:
        texto: Texto a analizar
        
    Returns:
        Diccionario con palabras, caracteres, oraciones y párrafos
    """
    palabras = len(texto.split())
    caracteres = len(texto)
    caracteres_sin_espacios = len(texto.replace(" ", ""))
    oraciones = len(re.findall(r'[.!?]+', texto))
    parrafos = len([p for p in texto.split('\n\n') if p.strip()])
    
    return {
        "palabras": palabras,
        "caracteres": caracteres,
        "caracteres_sin_espacios": caracteres_sin_espacios,
        "oraciones": max(oraciones, 1),
        "parrafos": max(parrafos, 1)
    }

@app.tool
def transformar_texto(texto: str, operacion: str) -> str:
    """
    Transforma texto según la operación especificada.
    
    Args:
        texto: Texto a transformar
        operacion: Tipo de transformación (mayusculas, minusculas, titulo, invertir)
        
    Returns:
        Texto transformado
        
    Raises:
        ValueError: Si la operación no es válida
    """
    operaciones_validas = ['mayusculas', 'minusculas', 'titulo', 'invertir']
    
    if operacion not in operaciones_validas:
        raise ValueError(f"Operación debe ser una de: {', '.join(operaciones_validas)}")
    
    if operacion == 'mayusculas':
        return texto.upper()
    elif operacion == 'minusculas':
        return texto.lower()
    elif operacion == 'titulo':
        return texto.title()
    elif operacion == 'invertir':
        return texto[::-1]
    
    return texto

@app.tool
def buscar_en_texto(texto: str, patron: str, case_sensitive: bool = False) -> Dict[str, any]:
    """
    Busca un patrón en el texto.
    
    Args:
        texto: Texto donde buscar
        patron: Patrón a buscar
        case_sensitive: Si la búsqueda distingue mayúsculas/minúsculas
        
    Returns:
        Diccionario con coincidencias y posiciones
    """
    if not case_sensitive:
        texto_busqueda = texto.lower()
        patron_busqueda = patron.lower()
    else:
        texto_busqueda = texto
        patron_busqueda = patron
    
    coincidencias = []
    posicion = 0
    
    while True:
        posicion = texto_busqueda.find(patron_busqueda, posicion)
        if posicion == -1:
            break
        coincidencias.append(posicion)
        posicion += 1
    
    return {
        "encontrado": len(coincidencias) > 0,
        "total_coincidencias": len(coincidencias),
        "posiciones": coincidencias
    }

@app.tool
def limpiar_texto(texto: str, remover_espacios_extra: bool = True, 
                  remover_puntuacion: bool = False) -> str:
    """
    Limpia un texto removiendo elementos no deseados.
    
    Args:
        texto: Texto a limpiar
        remover_espacios_extra: Eliminar espacios múltiples
        remover_puntuacion: Eliminar signos de puntuación
        
    Returns:
        Texto limpio
    """
    resultado = texto.strip()
    
    if remover_espacios_extra:
        resultado = ' '.join(resultado.split())
    
    if remover_puntuacion:
        resultado = re.sub(r'[^\w\s]', '', resultado)
    
    return resultado

@app.tool
def extraer_palabras_unicas(texto: str, min_longitud: int = 1) -> List[str]:
    """
    Extrae palabras únicas del texto.
    
    Args:
        texto: Texto del cual extraer palabras
        min_longitud: Longitud mínima de palabras a incluir
        
    Returns:
        Lista de palabras únicas ordenadas alfabéticamente
    """
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in set(palabras) if len(p) >= min_longitud]
    return sorted(palabras_filtradas)

if __name__ == "__main__":
    # Usa stdio para comunicación directa entre procesos
    app.run()
