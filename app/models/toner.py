"""
Modelo de Tóner
"""
from app.database.db import get_db_connection

class Toner:
    @staticmethod
    def crear(datos):
        """Crea un nuevo registro de tóner"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO toners 
                (impresora_id, referencia, fecha_instalacion, 
                 contador_instalacion, estado, tecnico_id, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos.get('impresora_id'),
                datos.get('referencia'),
                datos.get('fecha_instalacion'),
                datos.get('contador_instalacion'),
                'instalado',
                datos.get('tecnico_id'),
                datos.get('observaciones')
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def obtener_por_impresora(impresora_id):
        """Obtiene todos los tóners de una impresora"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM toners 
            WHERE impresora_id = ? 
            ORDER BY fecha_instalacion DESC
        ''', (impresora_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def obtener_todos():
        """Obtiene todos los tóners"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM toners
            ORDER BY fecha_instalacion DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def obtener_instalado(impresora_id):
        """Obtiene el tóner instalado actualmente"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM toners 
            WHERE impresora_id = ? AND estado = 'instalado'
            LIMIT 1
        ''', (impresora_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def retirar_toner(toner_id, datos):
        """Retira un tóner de la impresora"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            rendimiento = datos.get('contador_retiro', 0) - datos.get('contador_instalacion', 0)
            
            cursor.execute('''
                UPDATE toners 
                SET fecha_retiro = ?, contador_retiro = ?, 
                    rendimiento_obtenido = ?, estado = 'retirado'
                WHERE id = ?
            ''', (
                datos.get('fecha_retiro'),
                datos.get('contador_retiro'),
                rendimiento,
                toner_id
            ))
            conn.commit()
        finally:
            conn.close()
    
    @staticmethod
    def obtener_rendimiento_promedio(impresora_id):
        """Obtiene el rendimiento promedio de tóners de una impresora"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT AVG(rendimiento_obtenido) as promedio
            FROM toners 
            WHERE impresora_id = ? AND estado = 'retirado' 
                  AND rendimiento_obtenido IS NOT NULL
        ''', (impresora_id,))
        row = cursor.fetchone()
        conn.close()
        
        return row['promedio'] if row['promedio'] else 0
    
    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas de tóners"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM toners WHERE estado = 'instalado'")
        instalados = cursor.fetchone()['total']
        
        cursor.execute("""
            SELECT AVG(rendimiento_obtenido) as promedio 
            FROM toners WHERE estado = 'retirado'
        """)
        rendimiento_promedio = cursor.fetchone()['promedio'] or 0
        
        cursor.execute('''
            SELECT i.id, i.codigo_interno, i.marca, COUNT(t.id) as cantidad
            FROM impresoras i
            LEFT JOIN toners t ON i.id = t.impresora_id AND t.estado = 'instalado'
            GROUP BY i.id
            ORDER BY cantidad DESC
        ''')
        toners_por_impresora = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'instalados': instalados,
            'rendimiento_promedio': round(rendimiento_promedio, 2),
            'por_impresora': toners_por_impresora
        }
    
    @staticmethod
    def actualizar(toner_id, datos):
        """Actualiza un registro de tóner"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            contador_instalacion = datos.get('contador_instalacion') or 0
            contador_instalacion = int(contador_instalacion)
            contador_retiro = datos.get('contador_retiro')
            fecha_retiro = datos.get('fecha_retiro') or None
            rendimiento = None
            estado = datos.get('estado', 'instalado')

            if contador_retiro not in (None, '', '0') and fecha_retiro:
                contador_retiro = int(contador_retiro)
                rendimiento = contador_retiro - contador_instalacion
                estado = 'retirado'
            else:
                contador_retiro = None
                fecha_retiro = None
                if estado != 'retirado':
                    estado = 'instalado'

            cursor.execute('''
                UPDATE toners SET referencia = ?, fecha_instalacion = ?, contador_instalacion = ?,
                    fecha_retiro = ?, contador_retiro = ?, rendimiento_obtenido = ?, observaciones = ?, estado = ?
                WHERE id = ?
            ''', (
                datos.get('referencia'),
                datos.get('fecha_instalacion'),
                contador_instalacion,
                fecha_retiro,
                contador_retiro,
                rendimiento,
                datos.get('observaciones'),
                estado,
                toner_id
            ))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def eliminar(toner_id):
        """Elimina un registro de tóner"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM toners WHERE id = ?', (toner_id,))
            conn.commit()
        finally:
            conn.close()
