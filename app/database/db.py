"""
Configuración de la base de datos SQLite
"""
import sqlite3
import os
import tempfile
from datetime import datetime

DATABASE_PATH = os.getenv('DATABASE_PATH') or os.path.join('app', 'database', 'app.db')
use_temp_db = bool(os.getenv('VERCEL') or os.getenv('VERCEL_ENV'))
if not use_temp_db:
    db_dir = os.path.dirname(DATABASE_PATH)
    if db_dir and not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir, exist_ok=True)
        except OSError:
            use_temp_db = True
if use_temp_db:
    DATABASE_PATH = os.getenv('DATABASE_PATH') or os.path.join(tempfile.gettempdir(), 'app.db')

def get_db_connection():
    """Obtiene conexión a la base de datos"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos con todas las tablas"""
    db_dir = os.path.dirname(DATABASE_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                contraseña TEXT NOT NULL,
                rol TEXT NOT NULL DEFAULT 'tecnico',
                estado TEXT DEFAULT 'activo',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de impresoras
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS impresoras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_interno TEXT UNIQUE NOT NULL,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                numero_serie TEXT UNIQUE NOT NULL,
                direccion_ip TEXT UNIQUE NOT NULL,
                ubicacion TEXT NOT NULL,
                area TEXT NOT NULL,
                responsable TEXT,
                tipo TEXT NOT NULL,
                estado TEXT DEFAULT 'activa',
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                impresora_id INTEGER NOT NULL,
                referencia TEXT NOT NULL,
                fecha_instalacion DATE,
                contador_instalacion INTEGER,
                fecha_retiro DATE,
                contador_retiro INTEGER,
                rendimiento_obtenido INTEGER,
                estado TEXT DEFAULT 'instalado',
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                marca TEXT,
                stock_actual INTEGER DEFAULT 0,
                stock_minimo INTEGER DEFAULT 5,
                precio_unitario REAL,
                proveedor TEXT,
                ubicacion TEXT,
                fecha_compra DATE,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de movimientos de inventario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
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
        print("✓ Base de datos inicializada correctamente")
        
        # Crear usuario administrador por defecto si no existe
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', ('admin@sistema.com',))
        if not cursor.fetchone():
            from werkzeug.security import generate_password_hash
            cursor.execute('''
                INSERT INTO usuarios (nombre, email, contraseña, rol, estado)
                VALUES (?, ?, ?, ?, ?)
            ''', ('Administrador', 'admin@sistema.com', generate_password_hash('admin123'), 'administrador', 'activo'))
            conn.commit()
            print("✓ Usuario administrador creado: admin@sistema.com / admin123")
        
    except Exception as e:
        print(f"✗ Error al inicializar la base de datos: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_query(query, params=None):
    """Ejecuta una consulta SELECT"""
    conn = get_db_connection()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def execute_query(query, params=None):
    """Ejecuta una consulta INSERT/UPDATE/DELETE"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
