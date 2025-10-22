# Módulo 5: Integración con Base de Datos

## Servidores MCP con Bases de Datos

En este módulo aprenderás a crear servidores MCP que interactúan con bases de datos, permitiendo que agentes de IA consulten datos de manera segura y controlada.

## ¿Por Qué MCP para Bases de Datos?

### Ventajas

1. **Seguridad**: No expones credenciales de BD al cliente
2. **Control**: Defines qué queries pueden ejecutarse
3. **Abstracción**: El cliente no necesita conocer SQL
4. **Validación**: Validas parámetros antes de consultar
5. **Logging**: Registras todas las consultas realizadas

### Casos de Uso

- Agentes que consultan catálogos de productos
- Sistemas de recomendación basados en historial
- Chatbots con acceso a datos empresariales
- Dashboards dinámicos con IA

## SQLite: Base de Datos Simple

En este workshop usamos **SQLite** por su simplicidad:
- No requiere servidor separado
- Archivo único de base de datos
- Perfecto para desarrollo y prototipos
- Sintaxis SQL estándar

Para producción, los mismos conceptos aplican a PostgreSQL, MySQL, etc.

## Estructura del Servidor de Base de Datos

### 1. Inicialización de la BD

```python
import sqlite3
import os

DB_PATH = "tienda.db"

def init_database():
    """Crea tablas y carga datos iniciales"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Crear tabla
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    
    # Datos iniciales
    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        productos = [
            ("Laptop", 999.99, 10),
            ("Mouse", 29.99, 50),
            ("Teclado", 79.99, 30)
        ]
        cursor.executemany(
            "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
            productos
        )
    
    conn.commit()
    conn.close()
```

### 2. Herramientas de Consulta

```python
@app.tool
def obtener_productos() -> List[Dict[str, Any]]:
    """Obtiene todos los productos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nombre, precio, stock FROM productos")
    rows = cursor.fetchall()
    
    productos = []
    for row in rows:
        productos.append({
            "id": row[0],
            "nombre": row[1],
            "precio": row[2],
            "stock": row[3]
        })
    
    conn.close()
    return productos
```

### 3. Herramientas con Parámetros

```python
@app.tool
def buscar_producto(id_producto: int) -> Optional[Dict[str, Any]]:
    """Busca un producto por ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, nombre, precio, stock FROM productos WHERE id = ?",
        (id_producto,)
    )
    row = cursor.fetchone()
    
    if row:
        producto = {
            "id": row[0],
            "nombre": row[1],
            "precio": row[2],
            "stock": row[3]
        }
    else:
        producto = None
    
    conn.close()
    return producto
```

## Buenas Prácticas

### 1. Usar Context Managers

```python
def obtener_productos():
    """Versión mejorada con context manager"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        return cursor.fetchall()
```

El context manager asegura que la conexión se cierre automáticamente.

### 2. Prevenir SQL Injection

```python
# ✅ CORRECTO: Usar placeholders
cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))

# ❌ INCORRECTO: Concatenar strings
cursor.execute(f"SELECT * FROM productos WHERE id = {id_producto}")
```

Siempre usa placeholders (`?`) para valores dinámicos.

### 3. Manejo de Errores

```python
@app.tool
def actualizar_stock(id_producto: int, nuevo_stock: int) -> Dict[str, Any]:
    """Actualiza stock de un producto"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE productos SET stock = ? WHERE id = ?",
            (nuevo_stock, id_producto)
        )
        
        if cursor.rowcount == 0:
            raise ValueError(f"Producto {id_producto} no encontrado")
        
        conn.commit()
        conn.close()
        
        return {"exito": True, "mensaje": "Stock actualizado"}
        
    except sqlite3.Error as e:
        raise Exception(f"Error de base de datos: {e}")
```

### 4. Validación de Datos

```python
@app.tool
def crear_producto(nombre: str, precio: float, stock: int) -> Dict[str, Any]:
    """Crea un nuevo producto con validación"""
    # Validar
    if len(nombre) < 2:
        raise ValueError("Nombre debe tener al menos 2 caracteres")
    if precio <= 0:
        raise ValueError("Precio debe ser positivo")
    if stock < 0:
        raise ValueError("Stock no puede ser negativo")
    
    # Insertar
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
        (nombre, precio, stock)
    )
    
    producto_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "exito": True,
        "id": producto_id,
        "mensaje": "Producto creado"
    }
```

## Consultas Avanzadas

### Búsqueda por Texto

```python
@app.tool
def buscar_por_nombre(termino: str) -> List[Dict[str, Any]]:
    """Busca productos por nombre (búsqueda parcial)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM productos WHERE nombre LIKE ?",
        (f"%{termino}%",)
    )
    
    productos = [
        {"id": row[0], "nombre": row[1], "precio": row[2], "stock": row[3]}
        for row in cursor.fetchall()
    ]
    
    conn.close()
    return productos
```

### Filtrado por Rango

```python
@app.tool
def productos_por_precio(precio_min: float, precio_max: float) -> List[Dict]:
    """Obtiene productos en un rango de precios"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM productos WHERE precio BETWEEN ? AND ?",
        (precio_min, precio_max)
    )
    
    productos = [
        {"id": r[0], "nombre": r[1], "precio": r[2], "stock": r[3]}
        for r in cursor.fetchall()
    ]
    
    conn.close()
    return productos
```

### Agregaciones

```python
@app.tool
def estadisticas_productos() -> Dict[str, Any]:
    """Obtiene estadísticas de productos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            AVG(precio) as precio_promedio,
            SUM(stock) as stock_total
        FROM productos
    """)
    
    row = cursor.fetchone()
    stats = {
        "total_productos": row[0],
        "precio_promedio": round(row[1], 2) if row[1] else 0,
        "stock_total": row[2]
    }
    
    conn.close()
    return stats
```

## Múltiples Tablas

### Relaciones

```python
# Tabla de clientes
cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
""")

# Tabla de pedidos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY,
        cliente_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
""")
```

### JOINs

```python
@app.tool
def obtener_pedidos_cliente(cliente_id: int) -> List[Dict[str, Any]]:
    """Obtiene pedidos de un cliente con detalles de productos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            pedidos.id,
            productos.nombre,
            productos.precio,
            pedidos.cantidad
        FROM pedidos
        JOIN productos ON pedidos.producto_id = productos.id
        WHERE pedidos.cliente_id = ?
    """, (cliente_id,))
    
    pedidos = [
        {
            "id": r[0],
            "producto": r[1],
            "precio_unitario": r[2],
            "cantidad": r[3],
            "total": r[2] * r[3]
        }
        for r in cursor.fetchall()
    ]
    
    conn.close()
    return pedidos
```

## Archivo init_db.py

El archivo `init_db.py` proporciona utilidades para:
- Crear la base de datos desde cero
- Poblar con datos de ejemplo
- Reset completo de la BD
- Verificar integridad

Uso:
```bash
python init_db.py
```

## Ejercicios

### Ejercicio 1: Tabla de Categorías
Añade una tabla `categorias` y relaciona productos con categorías.

### Ejercicio 2: Herramientas de Actualización
Implementa herramientas para:
- Actualizar precio de producto
- Incrementar/decrementar stock
- Cambiar nombre de producto

### Ejercicio 3: Reportes
Crea herramientas para:
- Top 5 productos más caros
- Productos con stock bajo (menos de 10)
- Total de valor en inventario

## Próximos Pasos

En el **Módulo 6** aprenderás a conectar estos servidores MCP con agentes LangGraph usando `langchain-mcp-adapters`.

**Archivos del módulo**:
- [`servidor_db.py`](./servidor_db.py) - Servidor MCP con SQLite
- [`init_db.py`](./init_db.py) - Inicializador de base de datos
