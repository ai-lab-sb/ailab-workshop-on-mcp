"""
Servidor MCP completo para gestión de aseguradora.
Expone herramientas para consultar pólizas, productos de seguros y clientes via base de datos SQLite.
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from fastmcp import FastMCP

app = FastMCP("Aseguradora Server")

DB_PATH = os.path.join(os.path.dirname(__file__), "seguros.db")

def init_database():
    """Inicializa la base de datos con estructura y datos de ejemplo"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos_seguros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            descripcion TEXT,
            cobertura_base REAL NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefono TEXT,
            ciudad TEXT,
            fecha_nacimiento TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS polizas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_poliza TEXT UNIQUE NOT NULL,
            cliente_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_vencimiento TEXT NOT NULL,
            prima_mensual REAL NOT NULL,
            monto_cobertura REAL NOT NULL,
            estado TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (producto_id) REFERENCES productos_seguros(id)
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM productos_seguros")
    if cursor.fetchone()[0] == 0:
        productos = [
            ("Seguro de Vida Básico", "Vida", "Cobertura en caso de fallecimiento", 100000.00),
            ("Seguro de Vida Premium", "Vida", "Cobertura ampliada con beneficios adicionales", 250000.00),
            ("Seguro de Auto Básico", "Auto", "Cobertura por daños a terceros", 50000.00),
            ("Seguro de Auto Completo", "Auto", "Cobertura total incluyendo robo y daños propios", 100000.00),
            ("Seguro de Hogar", "Hogar", "Protección para tu vivienda y contenido", 150000.00),
            ("Seguro de Salud Individual", "Salud", "Cobertura médica individual", 80000.00),
            ("Seguro de Salud Familiar", "Salud", "Cobertura médica para toda la familia", 200000.00),
            ("Seguro de Accidentes Personales", "Accidentes", "Cobertura por accidentes personales", 75000.00)
        ]
        cursor.executemany(
            "INSERT INTO productos_seguros (nombre, tipo, descripcion, cobertura_base) VALUES (?, ?, ?, ?)",
            productos
        )
        print(f"✅ {len(productos)} productos de seguros insertados")
    
    cursor.execute("SELECT COUNT(*) FROM clientes")
    if cursor.fetchone()[0] == 0:
        clientes = [
            ("Juan Pérez", "juan.perez@email.com", "+57-300-1234567", "Bogotá", "1985-03-15"),
            ("María García", "maria.garcia@email.com", "+57-310-2345678", "Medellín", "1990-07-22"),
            ("Carlos López", "carlos.lopez@email.com", "+57-320-3456789", "Cali", "1978-11-30"),
            ("Ana Martínez", "ana.martinez@email.com", "+57-315-4567890", "Barranquilla", "1995-05-18"),
            ("Luis Rodríguez", "luis.rodriguez@email.com", "+57-305-5678901", "Cartagena", "1982-09-25"),
            ("Laura Fernández", "laura.fernandez@email.com", "+57-312-6789012", "Bogotá", "1988-12-10")
        ]
        cursor.executemany(
            "INSERT INTO clientes (nombre, email, telefono, ciudad, fecha_nacimiento) VALUES (?, ?, ?, ?, ?)",
            clientes
        )
        print(f"✅ {len(clientes)} clientes insertados")
    
    cursor.execute("SELECT COUNT(*) FROM polizas")
    if cursor.fetchone()[0] == 0:
        fecha_actual = datetime.now()
        polizas = [
            ("POL-2024-1001", 1, 1, (fecha_actual - timedelta(days=180)).strftime("%Y-%m-%d"), 
             (fecha_actual + timedelta(days=185)).strftime("%Y-%m-%d"), 150.00, 100000.00, "Activa"),
            ("POL-2024-1002", 1, 3, (fecha_actual - timedelta(days=90)).strftime("%Y-%m-%d"), 
             (fecha_actual + timedelta(days=275)).strftime("%Y-%m-%d"), 200.00, 50000.00, "Activa"),
            ("POL-2024-1003", 2, 4, (fecha_actual - timedelta(days=120)).strftime("%Y-%m-%d"), 
             (fecha_actual + timedelta(days=245)).strftime("%Y-%m-%d"), 350.00, 100000.00, "Activa"),
            ("POL-2024-1004", 3, 2, (fecha_actual - timedelta(days=200)).strftime("%Y-%m-%d"), 
             (fecha_actual + timedelta(days=165)).strftime("%Y-%m-%d"), 200.00, 150000.00, "Activa"),
            ("POL-2024-1005", 4, 6, (fecha_actual - timedelta(days=60)).strftime("%Y-%m-%d"), 
             (fecha_actual + timedelta(days=305)).strftime("%Y-%m-%d"), 180.00, 80000.00, "Activa"),
            ("POL-2024-1006", 5, 1, (fecha_actual - timedelta(days=150)).strftime("%Y-%m-%d"), 
             (fecha_actual + timedelta(days=215)).strftime("%Y-%m-%d"), 120.00, 80000.00, "Activa"),
            ("POL-2024-1007", 6, 5, (fecha_actual - timedelta(days=100)).strftime("%Y-%m-%d"), 
             (fecha_actual + timedelta(days=265)).strftime("%Y-%m-%d"), 220.00, 150000.00, "Activa")
        ]
        cursor.executemany(
            "INSERT INTO polizas (numero_poliza, cliente_id, producto_id, fecha_inicio, fecha_vencimiento, prima_mensual, monto_cobertura, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            polizas
        )
        print(f"✅ {len(polizas)} pólizas insertadas")
    
    conn.commit()
    conn.close()

@app.tool
def obtener_todas_polizas() -> List[Dict[str, Any]]:
    """Obtiene la lista completa de todas las pólizas activas"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.id, p.numero_poliza, c.nombre, ps.nombre, ps.tipo,
               p.fecha_inicio, p.fecha_vencimiento, p.prima_mensual, 
               p.monto_cobertura, p.estado
        FROM polizas p
        JOIN clientes c ON p.cliente_id = c.id
        JOIN productos_seguros ps ON p.producto_id = ps.id
        ORDER BY p.numero_poliza
    """)
    rows = cursor.fetchall()
    
    polizas = [
        {
            "id": r[0],
            "numero_poliza": r[1],
            "cliente": r[2],
            "producto": r[3],
            "tipo": r[4],
            "fecha_inicio": r[5],
            "fecha_vencimiento": r[6],
            "prima_mensual": r[7],
            "monto_cobertura": r[8],
            "estado": r[9]
        }
        for r in rows
    ]
    
    conn.close()
    return polizas

@app.tool
def buscar_poliza_por_id(poliza_id: int) -> Optional[Dict[str, Any]]:
    """
    Busca una póliza específica por su ID.
    
    Args:
        poliza_id: ID único de la póliza
        
    Returns:
        Diccionario con información completa de la póliza o None si no existe
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.id, p.numero_poliza, c.nombre, c.email, ps.nombre, ps.tipo,
               ps.descripcion, p.fecha_inicio, p.fecha_vencimiento, 
               p.prima_mensual, p.monto_cobertura, p.estado
        FROM polizas p
        JOIN clientes c ON p.cliente_id = c.id
        JOIN productos_seguros ps ON p.producto_id = ps.id
        WHERE p.id = ?
    """, (poliza_id,))
    row = cursor.fetchone()
    
    if row:
        poliza = {
            "id": row[0],
            "numero_poliza": row[1],
            "cliente": row[2],
            "email_cliente": row[3],
            "producto": row[4],
            "tipo": row[5],
            "descripcion": row[6],
            "fecha_inicio": row[7],
            "fecha_vencimiento": row[8],
            "prima_mensual": row[9],
            "monto_cobertura": row[10],
            "estado": row[11]
        }
    else:
        poliza = None
    
    conn.close()
    return poliza

@app.tool
def buscar_polizas_por_cliente(cliente_id: int) -> List[Dict[str, Any]]:
    """
    Busca todas las pólizas de un cliente específico.
    
    Args:
        cliente_id: ID del cliente
        
    Returns:
        Lista de pólizas del cliente
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.id, p.numero_poliza, ps.nombre, ps.tipo,
               p.fecha_inicio, p.fecha_vencimiento, p.prima_mensual, 
               p.monto_cobertura, p.estado
        FROM polizas p
        JOIN productos_seguros ps ON p.producto_id = ps.id
        WHERE p.cliente_id = ?
        ORDER BY p.fecha_inicio DESC
    """, (cliente_id,))
    rows = cursor.fetchall()
    
    polizas = [
        {
            "id": r[0],
            "numero_poliza": r[1],
            "producto": r[2],
            "tipo": r[3],
            "fecha_inicio": r[4],
            "fecha_vencimiento": r[5],
            "prima_mensual": r[6],
            "monto_cobertura": r[7],
            "estado": r[8]
        }
        for r in rows
    ]
    
    conn.close()
    return polizas

@app.tool
def buscar_polizas_por_tipo(tipo: str) -> List[Dict[str, Any]]:
    """
    Busca pólizas por tipo de seguro.
    
    Args:
        tipo: Tipo de seguro (Vida, Auto, Hogar, Salud, Accidentes)
        
    Returns:
        Lista de pólizas de ese tipo
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.id, p.numero_poliza, c.nombre, ps.nombre, ps.tipo,
               p.prima_mensual, p.monto_cobertura, p.estado
        FROM polizas p
        JOIN clientes c ON p.cliente_id = c.id
        JOIN productos_seguros ps ON p.producto_id = ps.id
        WHERE ps.tipo LIKE ?
        ORDER BY p.prima_mensual
    """, (f"%{tipo}%",))
    rows = cursor.fetchall()
    
    polizas = [
        {
            "id": r[0],
            "numero_poliza": r[1],
            "cliente": r[2],
            "producto": r[3],
            "tipo": r[4],
            "prima_mensual": r[5],
            "monto_cobertura": r[6],
            "estado": r[7]
        }
        for r in rows
    ]
    
    conn.close()
    return polizas

@app.tool
def obtener_productos_seguros() -> List[Dict[str, Any]]:
    """Obtiene todos los productos de seguros disponibles"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, nombre, tipo, descripcion, cobertura_base
        FROM productos_seguros
        ORDER BY tipo, nombre
    """)
    rows = cursor.fetchall()
    
    productos = [
        {
            "id": r[0],
            "nombre": r[1],
            "tipo": r[2],
            "descripcion": r[3],
            "cobertura_base": r[4]
        }
        for r in rows
    ]
    
    conn.close()
    return productos

@app.tool
def buscar_producto_seguro(producto_id: int) -> Optional[Dict[str, Any]]:
    """
    Busca un producto de seguro específico por su ID.
    
    Args:
        producto_id: ID del producto de seguro
        
    Returns:
        Diccionario con información del producto o None si no existe
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, nombre, tipo, descripcion, cobertura_base
        FROM productos_seguros
        WHERE id = ?
    """, (producto_id,))
    row = cursor.fetchone()
    
    if row:
        producto = {
            "id": row[0],
            "nombre": row[1],
            "tipo": row[2],
            "descripcion": row[3],
            "cobertura_base": row[4]
        }
    else:
        producto = None
    
    conn.close()
    return producto

@app.tool
def obtener_todos_clientes() -> List[Dict[str, Any]]:
    """Obtiene la lista completa de todos los clientes asegurados"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, nombre, email, telefono, ciudad, fecha_nacimiento
        FROM clientes
        ORDER BY nombre
    """)
    rows = cursor.fetchall()
    
    clientes = [
        {
            "id": r[0],
            "nombre": r[1],
            "email": r[2],
            "telefono": r[3],
            "ciudad": r[4],
            "fecha_nacimiento": r[5]
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
    
    cursor.execute("""
        SELECT id, nombre, email, telefono, ciudad, fecha_nacimiento
        FROM clientes
        WHERE id = ?
    """, (cliente_id,))
    row = cursor.fetchone()
    
    if row:
        cliente = {
            "id": row[0],
            "nombre": row[1],
            "email": row[2],
            "telefono": row[3],
            "ciudad": row[4],
            "fecha_nacimiento": row[5]
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
    
    cursor.execute("""
        SELECT id, nombre, email, telefono, ciudad, fecha_nacimiento
        FROM clientes
        WHERE ciudad LIKE ?
        ORDER BY nombre
    """, (f"%{ciudad}%",))
    rows = cursor.fetchall()
    
    clientes = [
        {
            "id": r[0],
            "nombre": r[1],
            "email": r[2],
            "telefono": r[3],
            "ciudad": r[4],
            "fecha_nacimiento": r[5]
        }
        for r in rows
    ]
    
    conn.close()
    return clientes

if __name__ == "__main__":
    print("=" * 60)
    print("Inicializando Base de Datos de Seguros")
    print("=" * 60 + "\n")
    init_database()
    
    print("\n" + "=" * 60)
    print("Servidor MCP - Aseguradora")
    print("=" * 60)
    print("\n🚀 Iniciando servidor en http://localhost:8200")
    print("\n📋 Herramientas disponibles:")
    print("   • obtener_todas_polizas")
    print("   • buscar_poliza_por_id")
    print("   • buscar_polizas_por_cliente")
    print("   • buscar_polizas_por_tipo")
    print("   • obtener_productos_seguros")
    print("   • buscar_producto_seguro")
    print("   • obtener_todos_clientes")
    print("   • buscar_cliente_por_id")
    print("   • buscar_clientes_por_ciudad")
    print("\n💡 Presiona Ctrl+C para detener el servidor\n")
    print("=" * 60 + "\n")
    
    app.run(transport="streamable-http", host="0.0.0.0", port=8200)
