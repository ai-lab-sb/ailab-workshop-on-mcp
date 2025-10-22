"""
Servidor MCP con base de datos SQLite.
Expone herramientas para consultar y manipular productos y clientes.
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP

app = FastMCP("Database Server")

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
            ciudad TEXT
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        productos = [
            ("Laptop", 999.99, "Electrónica", 15),
            ("Mouse", 29.99, "Electrónica", 50),
            ("Teclado", 79.99, "Electrónica", 30),
            ("Monitor", 299.99, "Electrónica", 20),
            ("Silla Oficina", 199.99, "Muebles", 10),
            ("Escritorio", 449.99, "Muebles", 5)
        ]
        cursor.executemany(
            "INSERT INTO productos (nombre, precio, categoria, stock) VALUES (?, ?, ?, ?)",
            productos
        )
    
    cursor.execute("SELECT COUNT(*) FROM clientes")
    if cursor.fetchone()[0] == 0:
        clientes = [
            ("Juan Pérez", "juan@email.com", "Bogotá"),
            ("María García", "maria@email.com", "Medellín"),
            ("Carlos López", "carlos@email.com", "Cali")
        ]
        cursor.executemany(
            "INSERT INTO clientes (nombre, email, ciudad) VALUES (?, ?, ?)",
            clientes
        )
    
    conn.commit()
    conn.close()

@app.tool
def obtener_todos_productos() -> List[Dict[str, Any]]:
    """Obtiene la lista completa de productos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nombre, precio, categoria, stock FROM productos")
    rows = cursor.fetchall()
    
    productos = []
    for row in rows:
        productos.append({
            "id": row[0],
            "nombre": row[1],
            "precio": row[2],
            "categoria": row[3],
            "stock": row[4]
        })
    
    conn.close()
    return productos

@app.tool
def buscar_producto_por_id(producto_id: int) -> Optional[Dict[str, Any]]:
    """
    Busca un producto específico por su ID.
    
    Args:
        producto_id: ID del producto a buscar
        
    Returns:
        Diccionario con datos del producto o None si no existe
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
        categoria: Nombre de la categoría
        
    Returns:
        Lista de productos en esa categoría
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, nombre, precio, categoria, stock FROM productos WHERE categoria LIKE ?",
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
def buscar_productos_por_precio(precio_min: float, precio_max: float) -> List[Dict[str, Any]]:
    """
    Busca productos dentro de un rango de precios.
    
    Args:
        precio_min: Precio mínimo
        precio_max: Precio máximo
        
    Returns:
        Lista de productos en ese rango de precios
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, nombre, precio, categoria, stock FROM productos WHERE precio BETWEEN ? AND ?",
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
def obtener_todos_clientes() -> List[Dict[str, Any]]:
    """Obtiene la lista completa de clientes"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nombre, email, ciudad FROM clientes")
    rows = cursor.fetchall()
    
    clientes = [
        {
            "id": r[0],
            "nombre": r[1],
            "email": r[2],
            "ciudad": r[3]
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
        cliente_id: ID del cliente a buscar
        
    Returns:
        Diccionario con datos del cliente o None si no existe
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, nombre, email, ciudad FROM clientes WHERE id = ?",
        (cliente_id,)
    )
    row = cursor.fetchone()
    
    if row:
        cliente = {
            "id": row[0],
            "nombre": row[1],
            "email": row[2],
            "ciudad": row[3]
        }
    else:
        cliente = None
    
    conn.close()
    return cliente

if __name__ == "__main__":
    print("Inicializando base de datos...")
    init_database()
    print("Base de datos lista")
    
    print("\n" + "=" * 60)
    print("Servidor MCP - Base de Datos")
    print("=" * 60)
    print("\n🚀 Iniciando servidor en http://localhost:8002")
    print("\n📋 Herramientas disponibles:")
    print("   • obtener_todos_productos")
    print("   • buscar_producto_por_id")
    print("   • buscar_productos_por_categoria")
    print("   • buscar_productos_por_precio")
    print("   • obtener_todos_clientes")
    print("   • buscar_cliente_por_id")
    print("\n💡 Presiona Ctrl+C para detener el servidor\n")
    print("=" * 60 + "\n")
    
    app.run(transport="streamable-http", host="0.0.0.0", port=8002)
