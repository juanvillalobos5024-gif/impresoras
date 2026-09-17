"""
Modelo de Contador de Impresiones
"""
from app.database.db import get_db_connection
from datetime import datetime, timedelta

class Contador:
    @staticmethod
    def crear(datos):
        """Crea un nuevo registro de contador"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            paginas = datos.get('contador_actual', 0) - datos.get('contador_anterior', 0)
            
            cursor.execute('''
                INSERT INTO contadores 
                (impresora_id, fecha, contador_anterior, contador_actual, 
                 paginas_impresas, tecnico_id, observaciones)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
            ''', (
                datos.get('impresora_id'),
                datos.get('fecha'),
                datos.get('contador_anterior'),
                datos.get('contador_actual'),
                paginas,
                datos.get('tecnico_id'),
                datos.get('observaciones')
            ))
            conn.commit()
            return cursor.fetchone()['id']
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def obtener_por_impresora(impresora_id):
        """Obtiene todos los contadores de una impresora"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM contadores 
            WHERE impresora_id = %s 
            ORDER BY fecha DESC
        ''', (impresora_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def obtener_todos():
        """Obtiene todos los contadores"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM contadores
            ORDER BY fecha DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def obtener_ultimo_contador(impresora_id):
        """Obtiene el último contador de una impresora"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM contadores 
            WHERE impresora_id = %s 
            ORDER BY fecha DESC 
            LIMIT 1
        ''', (impresora_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def obtener_estadisticas_mes():
        """Obtiene estadísticas de impresiones del mes actual"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total de páginas este mes
        cursor.execute('''
            SELECT COALESCE(SUM(paginas_impresas), 0) as total_paginas 
            FROM contadores 
            WHERE TO_CHAR(fecha, 'YYYY-MM') = TO_CHAR(CURRENT_DATE, 'YYYY-MM')
        ''')
        total_paginas = cursor.fetchone()['total_paginas']
        
        # Impresoras activas sin registro en 30 días
        hace_30_dias = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT COUNT(DISTINCT i.id) as impresoras_sin_lectura
            FROM impresoras i
            WHERE i.estado = 'activa' 
            AND i.id NOT IN (
                SELECT DISTINCT impresora_id FROM contadores 
                WHERE fecha >= %s
            )
        ''', (hace_30_dias,))
        impresoras_sin_lectura = cursor.fetchone()['impresoras_sin_lectura']
        
        conn.close()
        
        return {
            'total_paginas_mes': total_paginas,
            'impresoras_sin_lectura': impresoras_sin_lectura
        }
    
    @staticmethod
    def obtener_top_impresoras(limite=10):
        """Obtiene las impresoras con mayor volumen de impresión"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.id, i.codigo_interno, i.ubicacion, i.marca, i.modelo, 
                   SUM(c.paginas_impresas) as total_paginas
            FROM impresoras i
            LEFT JOIN contadores c ON i.id = c.impresora_id
            WHERE TO_CHAR(c.fecha, 'YYYY-MM') = TO_CHAR(CURRENT_DATE, 'YYYY-MM')
            GROUP BY i.id
            ORDER BY total_paginas DESC
            LIMIT %s
        ''', (limite,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def obtener_grafica_mensual(impresora_id=None):
        """Obtiene datos para gráfica de impresiones por mes"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if impresora_id:
            cursor.execute('''
                SELECT TO_CHAR(fecha, 'YYYY-MM') as mes, SUM(paginas_impresas) as total
                FROM contadores
                WHERE impresora_id = %s
                GROUP BY mes
                ORDER BY mes DESC
                LIMIT 12
            ''', (impresora_id,))
        else:
            cursor.execute('''
                SELECT TO_CHAR(fecha, 'YYYY-MM') as mes, SUM(paginas_impresas) as total
                FROM contadores
                GROUP BY mes
                ORDER BY mes DESC
                LIMIT 12
            ''')
        
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in reversed(rows)]
    
    @staticmethod
    def actualizar(contador_id, datos):
        """Actualiza un registro de contador"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            paginas = datos.get('contador_actual', 0) - datos.get('contador_anterior', 0)
            cursor.execute('''
                UPDATE contadores 
                SET contador_anterior = %s, contador_actual = %s, 
                    paginas_impresas = %s, observaciones = %s
                WHERE id = %s
            ''', (
                datos.get('contador_anterior'),
                datos.get('contador_actual'),
                paginas,
                datos.get('observaciones'),
                contador_id
            ))
            conn.commit()
        finally:
            conn.close()
    
    @staticmethod
    def eliminar(contador_id):
        """Elimina un registro de contador"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM contadores WHERE id = %s', (contador_id,))
            conn.commit()
        finally:
            conn.close()
