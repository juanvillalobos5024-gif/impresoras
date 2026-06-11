"""
Modelo de Impresora
"""
from app.database.db import get_db_connection
import qrcode
import os
from io import BytesIO

class Impresora:
    def __init__(self, codigo_interno, marca, modelo, numero_serie, direccion_ip,
                 ubicacion, area, tipo, id=None):
        self.id = id
        self.codigo_interno = codigo_interno
        self.marca = marca
        self.modelo = modelo
        self.numero_serie = numero_serie
        self.direccion_ip = direccion_ip
        self.ubicacion = ubicacion
        self.area = area
        self.tipo = tipo
        self.estado = 'activa'
        self.responsable = None
        self.fecha_instalacion = None
        self.fotografía = None
        self.observaciones = None
        self.qr_codigo = None
    
    @staticmethod
    def crear(datos):
        """Crea una nueva impresora"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO impresoras 
                (codigo_interno, marca, modelo, numero_serie, direccion_ip, 
                 ubicacion, area, responsable, tipo, estado, fecha_instalacion, 
                 observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos.get('codigo_interno'),
                datos.get('marca'),
                datos.get('modelo'),
                datos.get('numero_serie'),
                datos.get('direccion_ip'),
                datos.get('ubicacion'),
                datos.get('area'),
                datos.get('responsable'),
                datos.get('tipo'),
                datos.get('estado', 'activa'),
                datos.get('fecha_instalacion'),
                datos.get('observaciones')
            ))
            conn.commit()
            impresora_id = cursor.lastrowid
            
            # Generar código QR
            Impresora.generar_qr(impresora_id)
            
            return Impresora.obtener_por_id(impresora_id)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def obtener_por_id(impresora_id):
        """Obtiene una impresora por ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM impresoras WHERE id = ?', (impresora_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def obtener_por_ip(direccion_ip):
        """Obtiene una impresora por su dirección IP"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM impresoras WHERE direccion_ip = ?', (direccion_ip,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def obtener_todas():
        """Obtiene todas las impresoras"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM impresoras ORDER BY codigo_interno')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def obtener_por_area(area):
        """Obtiene impresoras por área"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM impresoras WHERE area = ? ORDER BY codigo_interno', (area,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def obtener_por_estado(estado):
        """Obtiene impresoras por estado"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM impresoras WHERE estado = ? ORDER BY codigo_interno', (estado,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def buscar(termino):
        """Busca impresoras por término"""
        conn = get_db_connection()
        cursor = conn.cursor()
        termino = f"%{termino}%"
        cursor.execute('''
            SELECT * FROM impresoras 
            WHERE codigo_interno LIKE ? OR marca LIKE ? OR modelo LIKE ? 
               OR numero_serie LIKE ? OR ubicacion LIKE ? OR area LIKE ?
            ORDER BY codigo_interno
        ''', (termino, termino, termino, termino, termino, termino))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def actualizar(impresora_id, datos):
        """Actualiza una impresora"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE impresoras 
                SET marca = ?, modelo = ?, numero_serie = ?, direccion_ip = ?,
                    ubicacion = ?, area = ?, responsable = ?, tipo = ?, 
                    estado = ?, fecha_instalacion = ?, observaciones = ?
                WHERE id = ?
            ''', (
                datos.get('marca'),
                datos.get('modelo'),
                datos.get('numero_serie'),
                datos.get('direccion_ip'),
                datos.get('ubicacion'),
                datos.get('area'),
                datos.get('responsable'),
                datos.get('tipo'),
                datos.get('estado'),
                datos.get('fecha_instalacion'),
                datos.get('observaciones'),
                impresora_id
            ))
            conn.commit()
        finally:
            conn.close()
    
    @staticmethod
    def eliminar(impresora_id):
        """Elimina una impresora"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM impresoras WHERE id = ?', (impresora_id,))
            conn.commit()
        finally:
            conn.close()
    
    @staticmethod
    def generar_qr(impresora_id):
        """Genera un código QR para la impresora"""
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(f"http://localhost:5000/impresoras/{impresora_id}")
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Guardar en carpeta de uploads
            os.makedirs('app/static/uploads', exist_ok=True)
            qr_path = f'app/static/uploads/qr_impresora_{impresora_id}.png'
            img.save(qr_path)
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE impresoras SET qr_codigo = ? WHERE id = ?',
                         (f'qr_impresora_{impresora_id}.png', impresora_id))
            conn.commit()
            conn.close()
            
            return qr_path
        except Exception as e:
            print(f"Error generando QR: {e}")
            return None
    
    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas de impresoras"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM impresoras')
        total = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as activas FROM impresoras WHERE estado = 'activa'")
        activas = cursor.fetchone()['activas']
        
        cursor.execute("SELECT COUNT(*) as mantenimiento FROM impresoras WHERE estado = 'mantenimiento'")
        mantenimiento = cursor.fetchone()['mantenimiento']
        
        cursor.execute("SELECT COUNT(*) as fuera_servicio FROM impresoras WHERE estado = 'fuera de servicio'")
        fuera_servicio = cursor.fetchone()['fuera_servicio']
        
        cursor.execute('''
            SELECT area, COUNT(*) as cantidad FROM impresoras 
            GROUP BY area ORDER BY cantidad DESC
        ''')
        por_area = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute('''
            SELECT tipo, COUNT(*) as cantidad FROM impresoras 
            GROUP BY tipo ORDER BY cantidad DESC
        ''')
        por_tipo = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'total': total,
            'activas': activas,
            'mantenimiento': mantenimiento,
            'fuera_servicio': fuera_servicio,
            'por_area': por_area,
            'por_tipo': por_tipo
        }
