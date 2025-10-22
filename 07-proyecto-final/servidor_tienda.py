"""
Servidor MCP completo para gestión de tienda.
Expone herramientas para consultar productos y clientes via base de datos SQLite.
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP

app = FastMCP("Tienda Server")

DB_PATH = os.path.join(os.path.dirname(__file__), "tienda.db")

def init_database():
    """Inicializa la base de datos con estructura y datos de ejemplo"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            ciudad TEXT,
            telefono TEXT
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        productos = [
            ("Laptop Dell XPS 15", 1299.99, "Electrónica", 8),
            ("Mouse Logitech MX Master", 99.99, "Electrónica", 25),
            ("Teclado Mecánico Corsair", 149.99, "Electrónica", 15),
            ("Monitor Samsung 27\"", 349.99, "Electrónica", 12),
            ("Webcam Logitech C920", 79.99, "Electrónica", 20),
            ("Silla Ergonómica Herman Miller", 899.99, "Muebles", 5),
            ("Escritorio Ajustable", 599.99, "Muebles", 7),
            ("Lámpara de Escritorio LED", 49.99, "Iluminación", 30),
            ("Audífonos Sony WH-1000XM4", 349.99, "Electrónica", 18),
            ("Mochila para Laptop", 79.99, "Accesorios", 40)
        ]
        cursor.executemany(
            "INSERT INTO productos (nombre, precio, categoria, stock) VALUES (?, ?, ?, ?)",
            productos
        )
        print(f"✅ {len(productos)} productos insertados")
    
    cursor.execute("SELECT COUNT(*) FROM clientes")
    if cursor.fetchone()[0] == 0:
        clientes = [
            ("Juan Pérez", "juan.perez@email.com", "Bogotá", "+57-300-1234567"),
            ("María García", "maria.garcia@email.com", "Medellín", "+57-310-2345678"),
            ("Carlos López", "carlos.lopez@email.com", "Cali", "+57-320-3456789"),
            ("Ana Martínez", "ana.martinez@email.com", "Barranquilla", "+57-315-4567890"),
            ("Luis Rodríguez", "luis.rodriguez@email.com", "Cartagena", "+57-305-5678901"),
            ("Laura Fernández", "laura.fernandez@email.com", "Bogotá", "+57-312-6789012"),
        ]
        cursor.executemany(
            "INSERT INTO clientes (nombre, email, ciudad, telefono) VALUES (?, ?, ?, ?)",
            clientes
        )
        print(f"✅ {len(clientes)} clientes insertados")
    
    conn.commit()
    conn.close()

@app.tool
def obtener_todos_productos() -> List[Dict[str, Any]]:
    """Obtiene la lista completa de todos los productos en la tienda"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nombre, precio, categoria, stock FROM productos ORDER BY nombre")
    rows = cursor.fetchall()
    
    productos = [
        {
            "id": r[0],
            "nombre": r[1],
            "precio": r[2],
            "categoria": r[3],
            "stock": r[4]
        }
        for r in rows
    ]
    
    conn.close()
    return productos

@app.tool
def buscar_producto_por_id(producto_id: int) -> Optional[Dict[str, Any]]:
    """
    Busca un producto específico por su ID.
    
    Args:
        producto_id: ID único del producto
        
    Returns:
        Diccionario con información del producto o None si no existe
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, nombre, precio, categoria, stock FROM productos WHERE id = ?",
        (producto_id,)
    )
    row = cursor.fetchone()
    
    if row:
        producto = {
            "id": row[0],
            "nombre": row[1],
            "precio": row[2],
            "categoria": row[3],
            "stock": row[4]
        }
    else:
        producto = None
    
    conn.close()
    return producto

@app.tool
def buscar_productos_por_categoria(categoria: str) -> List[Dict[str, Any]]:
    """
    Busca productos por categoría.
    
    Args:
        categoria: Nombre de la categoría (Electrónica, Muebles, etc.)
        
    Returns:
        Lista de productos en esa categoría
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, nombre, precio, categoria, stock FROM productos WHERE categoria LIKE ? ORDER BY precio",
        (f"%{categoria}%",)
    )
    rows = cursor.fetchall()
    
    productos = [
        {
            "id": r[0],
            "nombre": r[1],
            "precio": r[2],
            "categoria": r[3],
            "stock": r[4]
        }
        for r in rows
    ]
    
    conn.close()
    return productos

@app.tool
def buscar_productos_por_nombre(termino: str) -> List[Dict[str, Any]]:
    """
    Busca productos por nombre (búsqueda parcial).
    
    Args:
        termino: Término de búsqueda a buscar en el nombre del producto
        
    Returns:
        Lista de productos que coinciden con el término
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, nombre, precio, categoria, stock FROM productos WHERE nombre LIKE ? ORDER BY nombre",
        (f"%{termino}%",)
    )
    rows = cursor.fetchall()
    
    productos = [
        {
            "id": r[0],
            "nombre": r[1],
            "precio": r[2],
            "categoria": r[3],
            "stock": r[4]
        }
        for r in rows
    ]
    
    conn.close()
    return productos

@app.tool
def buscar_productos_por_precio(precio_min: float, precio_max: float) -> List[Dict[str, Any]]:
    """
    Busca productos dentro de un rango de precios.
    
    Args:
        precio_min: Precio mínimo (inclusive)
        precio_max: Precio máximo (inclusive)
        
    Returns:
        Lista de productos en ese rango de precios
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, nombre, precio, categoria, stock FROM productos WHERE precio BETWEEN ? AND ? ORDER BY precio",
        (precio_min, precio_max)
    )
    rows = cursor.fetchall()
    
    productos = [
        {
            "id": r[0],
            "nombre": r[1],
            "precio": r[2],
            "categoria": r[3],
            "stock": r[4]
        }
        for r in rows
    ]
    
    conn.close()
    return productos

@app.tool
def productos_en_stock() -> List[Dict[str, Any]]:
    """
    Obtiene todos los productos que tienen stock disponible.
    
    Returns:
        Lista de productos con stock mayor a 0
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, nombre, precio, categoria, stock FROM productos WHERE stock > 0 ORDER BY stock DESC"
    )
    rows = cursor.fetchall()
    
    productos = [
        {
            "id": r[0],
            "nombre": r[1],
            "precio": r[2],
            "categoria": r[3],
            "stock": r[4]
        }
        for r in rows
    ]
    
    conn.close()
    return productos

@app.tool
def obtener_todos_clientes() -> List[Dict[str, Any]]:
    """Obtiene la lista completa de todos los clientes"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nombre, email, ciudad, telefono FROM clientes ORDER BY nombre")
    rows = cursor.fetchall()
    
    clientes = [
        {
            "id": r[0],
            "nombre": r[1],
            "email": r[2],
            "ciudad": r[3],
            "telefono": r[4]
        }
        for r in rows
    ]
    
    conn.close()
    return clientes

@app.tool
def buscar_cliente_por_id(cliente_id: int) -> Optional[Dict[str, Any]]:
    """
    Busca un cliente específico por su ID.
    
    Args:
        cliente_id: ID único del cliente
        
    Returns:
        Diccionario con información del cliente o None si no existe
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, nombre, email, ciudad, telefono FROM clientes WHERE id = ?",
        (cliente_id,)
    )
    row = cursor.fetchone()
    
    if row:
        cliente = {
            "id": row[0],
            "nombre": row[1],
            "email": row[2],
            "ciudad": row[3],
            "telefono": row[4]
        }
    else:
        cliente = None
    
    conn.close()
    return cliente

@app.tool
def buscar_clientes_por_ciudad(ciudad: str) -> List[Dict[str, Any]]:
    """
    Busca clientes por ciudad.
    
    Args:
        ciudad: Nombre de la ciudad
        
    Returns:
        Lista de clientes en esa ciudad
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, nombre, email, ciudad, telefono FROM clientes WHERE ciudad LIKE ? ORDER BY nombre",
        (f"%{ciudad}%",)
    )
    rows = cursor.fetchall()
    
    clientes = [
        {
            "id": r[0],
            "nombre": r[1],
            "email": r[2],
            "ciudad": r[3],
            "telefono": r[4]
        }
        for r in rows
    ]
    
    conn.close()
    return clientes

if __name__ == "__main__":
    print("=" * 60)
    print("Inicializando Base de Datos")
    print("=" * 60 + "\n")
    init_database()
    
    print("\n" + "=" * 60)
    print("Servidor MCP - Tienda")
    print("=" * 60)
    print("\n🚀 Iniciando servidor en http://localhost:8200")
    print("\n📋 Herramientas disponibles:")
    print("   • obtener_todos_productos")
    print("   • buscar_producto_por_id")
    print("   • buscar_productos_por_categoria")
    print("   • buscar_productos_por_nombre")
    print("   • buscar_productos_por_precio")
    print("   • productos_en_stock")
    print("   • obtener_todos_clientes")
    print("   • buscar_cliente_por_id")
    print("   • buscar_clientes_por_ciudad")
    print("\n💡 Presiona Ctrl+C para detener el servidor\n")
    print("=" * 60 + "\n")
    
    app.run(transport="streamable-http", host="0.0.0.0", port=8200)
