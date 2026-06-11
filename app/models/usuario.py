"""
Modelo de Usuario
"""
from werkzeug.security import generate_password_hash, check_password_hash
from app.database.db import get_db_connection

class Usuario:
    def __init__(self, nombre, email, contraseña, rol='tecnico', id=None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.rol = rol
        self._contraseña = generate_password_hash(contraseña)
    
    @staticmethod
    def crear(nombre, email, contraseña, rol='tecnico'):
        """Crea un nuevo usuario"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO usuarios (nombre, email, contraseña, rol, estado)
                VALUES (?, ?, ?, ?, 'activo')
            ''', (nombre, email, generate_password_hash(contraseña), rol))
            conn.commit()
            usuario_id = cursor.lastrowid
            return Usuario.obtener_por_id(usuario_id)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def obtener_por_id(usuario_id):
        """Obtiene un usuario por ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            usuario = Usuario(row['nombre'], row['email'], '', row['rol'], row['id'])
            usuario._contraseña = row['contraseña']
            return usuario
        return None
    
    @staticmethod
    def obtener_por_email(email):
        """Obtiene un usuario por email"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            usuario = Usuario(row['nombre'], row['email'], '', row['rol'], row['id'])
            usuario._contraseña = row['contraseña']
            return usuario
        return None
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los usuarios"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios ORDER BY nombre')
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def verificar_contraseña(self, contraseña):
        """Verifica la contraseña"""
        return check_password_hash(self._contraseña, contraseña)
    
    def actualizar(self):
        """Actualiza el usuario"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE usuarios SET nombre = ?, rol = ? WHERE id = ?
            ''', (self.nombre, self.rol, self.id))
            conn.commit()
        finally:
            conn.close()
    
    def cambiar_contraseña(self, nueva_contraseña):
        """Cambia la contraseña del usuario"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE usuarios SET contraseña = ? WHERE id = ?
            ''', (generate_password_hash(nueva_contraseña), self.id))
            conn.commit()
        finally:
            conn.close()
