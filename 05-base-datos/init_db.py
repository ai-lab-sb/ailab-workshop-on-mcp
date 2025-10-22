"""
Script para inicializar y gestionar la base de datos del workshop.
Permite crear, resetear y poblar la base de datos con datos de ejemplo.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "tienda.db")

def crear_tablas():
    """Crea las tablas de la base de datos"""
    print("Creando tablas...")
    
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
    
    conn.commit()
    conn.close()
    print("✅ Tablas creadas")

def poblar_datos():
    """Inserta datos de ejemplo en la base de datos"""
    print("\nInsertando datos de ejemplo...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    productos = [
        ("Laptop Dell XPS", 999.99, "Electrónica", 15),
        ("Mouse Logitech", 29.99, "Electrónica", 50),
        ("Teclado Mecánico", 79.99, "Electrónica", 30),
        ("Monitor 24 pulgadas", 299.99, "Electrónica", 20),
        ("Silla Ergonómica", 199.99, "Muebles", 10),
        ("Escritorio Moderno", 449.99, "Muebles", 5),
        ("Lámpara LED", 39.99, "Iluminación", 25),
        ("Webcam HD", 89.99, "Electrónica", 18)
    ]
    
    cursor.executemany(
        "INSERT INTO productos (nombre, precio, categoria, stock) VALUES (?, ?, ?, ?)",
        productos
    )
    print(f"✅ {len(productos)} productos insertados")
    
    clientes = [
        ("Juan Pérez", "juan@email.com", "Bogotá"),
        ("María García", "maria@email.com", "Medellín"),
        ("Carlos López", "carlos@email.com", "Cali"),
        ("Ana Martínez", "ana@email.com", "Barranquilla"),
        ("Luis Rodríguez", "luis@email.com", "Cartagena")
    ]
    
    cursor.executemany(
        "INSERT INTO clientes (nombre, email, ciudad) VALUES (?, ?, ?)",
        clientes
    )
    print(f"✅ {len(clientes)} clientes insertados")
    
    conn.commit()
    conn.close()

def mostrar_datos():
    """Muestra un resumen de los datos en la base de datos"""
    print("\n" + "=" * 60)
    print("Resumen de la Base de Datos")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM productos")
    total_productos = cursor.fetchone()[0]
    print(f"\n📦 Total de productos: {total_productos}")
    
    cursor.execute("SELECT categoria, COUNT(*) FROM productos GROUP BY categoria")
    print("\nProductos por categoría:")
    for row in cursor.fetchall():
        print(f"  • {row[0]}: {row[1]} productos")
    
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = cursor.fetchone()[0]
    print(f"\n👥 Total de clientes: {total_clientes}")
    
    cursor.execute("SELECT ciudad, COUNT(*) FROM clientes GROUP BY ciudad")
    print("\nClientes por ciudad:")
    for row in cursor.fetchall():
        print(f"  • {row[0]}: {row[1]} clientes")
    
    conn.close()
    print("\n" + "=" * 60 + "\n")

def resetear_base_datos():
    """Elimina la base de datos existente"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("✅ Base de datos eliminada")
    else:
        print("ℹ️  No existe base de datos para eliminar")

def inicializar_completa():
    """Proceso completo de inicialización"""
    print("=" * 60)
    print("Inicialización de Base de Datos - Workshop MCP")
    print("=" * 60 + "\n")
    
    if os.path.exists(DB_PATH):
        respuesta = input("Ya existe una base de datos. ¿Deseas resetearla? (s/n): ")
        if respuesta.lower() == 's':
            resetear_base_datos()
        else:
            print("Operación cancelada")
            return
    
    crear_tablas()
    poblar_datos()
    mostrar_datos()
    
    print("✅ Inicialización completada exitosamente")
    print(f"📁 Base de datos creada en: {DB_PATH}\n")

if __name__ == "__main__":
    inicializar_completa()
