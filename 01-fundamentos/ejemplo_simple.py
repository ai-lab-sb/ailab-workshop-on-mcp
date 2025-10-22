"""
Ejemplo simple de servidor MCP con FastMCP.
Este servidor expone una herramienta básica para convertir temperaturas.
"""

from fastmcp import FastMCP

# Crear instancia del servidor MCP
app = FastMCP("Temperature Converter")

@app.tool
def celsius_to_fahrenheit(celsius: float) -> float:
    """
    Convierte temperatura de Celsius a Fahrenheit.
    
    Args:
        celsius: Temperatura en grados Celsius
        
    Returns:
        Temperatura en grados Fahrenheit
    """
    return (celsius * 9/5) + 32

@app.tool
def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    Convierte temperatura de Fahrenheit a Celsius.
    
    Args:
        fahrenheit: Temperatura en grados Fahrenheit
        
    Returns:
        Temperatura en grados Celsius
    """
    return (fahrenheit - 32) * 5/9

@app.tool
def celsius_to_kelvin(celsius: float) -> float:
    """
    Convierte temperatura de Celsius a Kelvin.
    
    Args:
        celsius: Temperatura en grados Celsius
        
    Returns:
        Temperatura en Kelvin
    """
    return celsius + 273.15

if __name__ == "__main__":
    print("Iniciando servidor MCP de conversión de temperaturas...")
    print("Puerto: 8100")
    print("\nHerramientas disponibles:")
    print("  - celsius_to_fahrenheit")
    print("  - fahrenheit_to_celsius")
    print("  - celsius_to_kelvin")
    print("\nPresiona Ctrl+C para detener\n")
    
    # Iniciar servidor con transporte HTTP
    app.run(transport="streamable-http", host="0.0.0.0", port=8100)
