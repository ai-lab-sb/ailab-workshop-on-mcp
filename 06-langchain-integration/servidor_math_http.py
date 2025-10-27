"""
Servidor MCP de matemáticas con transporte HTTP.
Este servidor está configurado específicamente para uso con LangChain MCP Adapters.
"""

from typing import Union
from fastmcp import FastMCP

app = FastMCP("Math Operations Server")

@app.tool
def add(a: Union[int, float], b: Union[int, float]) -> float:
    """
    Suma dos números.
    
    Args:
        a: Primer número
        b: Segundo número
        
    Returns:
        La suma de a + b
    """
    return float(a + b)

@app.tool
def subtract(a: Union[int, float], b: Union[int, float]) -> float:
    """
    Resta dos números.
    
    Args:
        a: Primer número (minuendo)
        b: Segundo número (sustraendo)
        
    Returns:
        La resta de a - b
    """
    return float(a - b)

@app.tool
def multiply(a: Union[int, float], b: Union[int, float]) -> float:
    """
    Multiplica dos números.
    
    Args:
        a: Primer número
        b: Segundo número
        
    Returns:
        El producto de a * b
    """
    return float(a * b)

@app.tool
def divide(a: Union[int, float], b: Union[int, float]) -> float:
    """
    Divide dos números.
    
    Args:
        a: Numerador
        b: Denominador
        
    Returns:
        El cociente de a / b
        
    Raises:
        ValueError: Si el denominador es cero
    """
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return float(a / b)

if __name__ == "__main__":
    print("=" * 60)
    print("Servidor MCP - Operaciones Matemáticas (HTTP)")
    print("=" * 60)
    print("\nIniciando servidor en http://localhost:8001")
    print("\nHerramientas disponibles:")
    print("   - add(a, b)      - Suma dos números")
    print("   - subtract(a, b) - Resta dos números")
    print("   - multiply(a, b) - Multiplica dos números")
    print("   - divide(a, b)   - Divide dos números")
    print("\nPresiona Ctrl+C para detener el servidor\n")
    print("=" * 60 + "\n")
    
    # Usar transporte HTTP para integración con LangChain
    app.run(transport="streamable-http", host="0.0.0.0", port=8001)
