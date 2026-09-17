"""
Configuración de la base de datos PostgreSQL (Vercel Postgres)
"""
import psycopg2
from psycopg2.extras import RealDictConnection
import os
from werkzeug.security import generate_password_hash

# La URL de conexión proporcionada por Vercel
# Si no está definida, intentará conectar a un PostgreSQL local por defecto
DATABASE_URL = os.getenv('POSTGRES_URL', 'postgresql://postgres:postgres@localhost:5432/impresoras')

def get_db_connection():
    """Obtiene conexión a la base de datos"""
    try:
        conn = psycopg2.connect(DATABASE_URL, connection_factory=RealDictConnection)
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        raise e

def init_db():
    """Inicializa la base de datos con todas las tablas"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                contraseña TEXT NOT NULL,
                rol VARCHAR(50) NOT NULL DEFAULT 'tecnico',
                estado VARCHAR(50) DEFAULT 'activo',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de impresoras
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS impresoras (
                id SERIAL PRIMARY KEY,
                codigo_interno VARCHAR(100) UNIQUE NOT NULL,
                marca VARCHAR(100) NOT NULL,
                modelo VARCHAR(100) NOT NULL,
                numero_serie VARCHAR(100) UNIQUE NOT NULL,
                direccion_ip VARCHAR(50) UNIQUE NOT NULL,
                ubicacion VARCHAR(255) NOT NULL,
                area VARCHAR(100) NOT NULL,
                responsable VARCHAR(255),
                tipo VARCHAR(100) NOT NULL,
                estado VARCHAR(50) DEFAULT 'activa',
                fecha_instalacion DATE,
                fotografía TEXT,
                observaciones TEXT,
                qr_codigo TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_contador_registro DATE
            )
        ''')
        
        # Tabla de contadores de impresiones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contadores (
                id SERIAL PRIMARY KEY,
                impresora_id INTEGER NOT NULL,
                fecha DATE NOT NULL,
                contador_anterior INTEGER DEFAULT 0,
                contador_actual INTEGER NOT NULL,
                paginas_impresas INTEGER,
                tecnico_id INTEGER,
                observaciones TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (impresora_id) REFERENCES impresoras(id) ON DELETE CASCADE,
                FOREIGN KEY (tecnico_id) REFERENCES usuarios(id),
                UNIQUE(impresora_id, fecha)
            )
        ''')
        
        # Tabla de tóner
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS toners (
                id SERIAL PRIMARY KEY,
                impresora_id INTEGER NOT NULL,
                referencia VARCHAR(255) NOT NULL,
                fecha_instalacion DATE,
                contador_instalacion INTEGER,
                fecha_retiro DATE,
                contador_retiro INTEGER,
                rendimiento_obtenido INTEGER,
                estado VARCHAR(50) DEFAULT 'instalado',
                tecnico_id INTEGER,
                observaciones TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (impresora_id) REFERENCES impresoras(id) ON DELETE CASCADE,
                FOREIGN KEY (tecnico_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Tabla de productos/consumibles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id SERIAL PRIMARY KEY,
                codigo VARCHAR(100) UNIQUE NOT NULL,
                nombre VARCHAR(255) NOT NULL,
                categoria VARCHAR(100) NOT NULL,
                marca VARCHAR(100),
                stock_actual INTEGER DEFAULT 0,
                stock_minimo INTEGER DEFAULT 5,
                precio_unitario NUMERIC(10,2),
                proveedor VARCHAR(255),
                ubicacion VARCHAR(255),
                fecha_compra DATE,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de movimientos de inventario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimientos (
                id SERIAL PRIMARY KEY,
                tipo VARCHAR(50) NOT NULL,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                fecha DATE NOT NULL,
                responsable_id INTEGER,
                observaciones TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
                FOREIGN KEY (responsable_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Crear índices para mejorar rendimiento
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_impresoras_area ON impresoras(area)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_impresoras_estado ON impresoras(estado)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_contadores_fecha ON contadores(fecha)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_movimientos_fecha ON movimientos(fecha)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_productos_categoria ON productos(categoria)')
        
        conn.commit()
        print("✓ Base de datos Postgres inicializada correctamente")
        
        # Crear usuario administrador por defecto si no existe
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', ('admin@sistema.com',))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO usuarios (nombre, email, contraseña, rol, estado)
                VALUES (%s, %s, %s, %s, %s)
            ''', ('Administrador', 'admin@sistema.com', generate_password_hash('admin123'), 'administrador', 'activo'))
            conn.commit()
            print("✓ Usuario administrador creado: admin@sistema.com / admin123")
        
    except Exception as e:
        print(f"✗ Error al inicializar la base de datos: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_query(query, params=None):
    """Ejecuta una consulta SELECT devolviendo un diccionario por cada fila"""
    conn = get_db_connection()
    # Usamos RealDictCursor para que los resultados sean diccionarios como dict(row) en sqlite
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()
        conn.close()

def execute_query(query, params=None, fetch_id=False):
    """Ejecuta una consulta INSERT/UPDATE/DELETE. 
    Si fetch_id es True, asume que la consulta incluye RETURNING id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        
        if fetch_id:
            # fetch the inserted id if requested (requires RETURNING id in query)
            row = cursor.fetchone()
            if row:
                return row[0]
        return cursor.rowcount
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
