"""
Modelo de Movimiento de Inventario
"""
from app.database.db import get_db_connection
from app.models.producto import Producto

class Movimiento:
    ENTRADA = 'entrada'
    SALIDA = 'salida'
    
    @staticmethod
    def crear(datos):
        """Crea un nuevo movimiento de inventario"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Obtener producto
            producto = Producto.obtener_por_id(datos.get('producto_id'))
            if not producto:
                raise Exception("Producto no encontrado")
            
            # Registrar movimiento
            cursor.execute('''
                INSERT INTO movimientos 
                (tipo, producto_id, cantidad, fecha, responsable_id, observaciones)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datos.get('tipo'),
                datos.get('producto_id'),
                datos.get('cantidad'),
                datos.get('fecha'),
                datos.get('responsable_id'),
                datos.get('observaciones')
            ))
            
            # Actualizar stock
            nuevo_stock = producto['stock_actual']
            if datos.get('tipo') == Movimiento.ENTRADA:
                nuevo_stock += datos.get('cantidad', 0)
            elif datos.get('tipo') == Movimiento.SALIDA:
                nuevo_stock -= datos.get('cantidad', 0)
            
            cursor.execute('''
                UPDATE productos SET stock_actual = ? WHERE id = ?
            ''', (nuevo_stock, datos.get('producto_id')))
            
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los movimientos"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.*, p.nombre as producto_nombre, p.codigo as producto_codigo,
                   u.nombre as responsable_nombre
            FROM movimientos m
            LEFT JOIN productos p ON m.producto_id = p.id
            LEFT JOIN usuarios u ON m.responsable_id = u.id
            ORDER BY m.fecha DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def obtener_por_producto(producto_id):
        """Obtiene movimientos de un producto"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.*, u.nombre as responsable_nombre
            FROM movimientos m
            LEFT JOIN usuarios u ON m.responsable_id = u.id
            WHERE m.producto_id = ?
            ORDER BY m.fecha DESC
        ''', (producto_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def obtener_ultimos(limite=10):
        """Obtiene los últimos movimientos"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.*, p.nombre as producto_nombre, p.codigo as producto_codigo,
                   u.nombre as responsable_nombre
            FROM movimientos m
            LEFT JOIN productos p ON m.producto_id = p.id
            LEFT JOIN usuarios u ON m.responsable_id = u.id
            ORDER BY m.fecha DESC
            LIMIT ?
        ''', (limite,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def obtener_por_mes(mes_año):
        """Obtiene movimientos de un mes específico (formato: YYYY-MM)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.*, p.nombre as producto_nombre, u.nombre as responsable_nombre
            FROM movimientos m
            LEFT JOIN productos p ON m.producto_id = p.id
            LEFT JOIN usuarios u ON m.responsable_id = u.id
            WHERE strftime('%Y-%m', m.fecha) = ?
            ORDER BY m.fecha DESC
        ''', (mes_año,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def obtener_estadisticas_mes():
        """Obtiene estadísticas de movimientos del mes actual"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT tipo, COUNT(*) as cantidad, SUM(cantidad) as total
            FROM movimientos
            WHERE strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now')
            GROUP BY tipo
        ''')
        rows = cursor.fetchall()
        
        estadisticas = {}
        for row in rows:
            estadisticas[row['tipo']] = {
                'cantidad': row['cantidad'],
                'total': row['total']
            }
        
        conn.close()
        return estadisticas
    
    @staticmethod
    def obtener_grafica_mensual():
        """Obtiene datos para gráfica de movimientos"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT strftime('%Y-%m', fecha) as mes, tipo, COUNT(*) as cantidad
            FROM movimientos
            GROUP BY mes, tipo
            ORDER BY mes DESC
            LIMIT 12
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in reversed(rows)]
    
    @staticmethod
    def eliminar(movimiento_id):
        """Elimina un movimiento (reversión)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Obtener el movimiento
            cursor.execute('SELECT * FROM movimientos WHERE id = ?', (movimiento_id,))
            movimiento = cursor.fetchone()
            
            if not movimiento:
                raise Exception("Movimiento no encontrado")
            
            # Revertir el stock
            producto = Producto.obtener_por_id(movimiento['producto_id'])
            nuevo_stock = producto['stock_actual']
            
            if movimiento['tipo'] == Movimiento.ENTRADA:
                nuevo_stock -= movimiento['cantidad']
            elif movimiento['tipo'] == Movimiento.SALIDA:
                nuevo_stock += movimiento['cantidad']
            
            cursor.execute('''
                UPDATE productos SET stock_actual = ? WHERE id = ?
            ''', (nuevo_stock, movimiento['producto_id']))
            
            # Eliminar movimiento
            cursor.execute('DELETE FROM movimientos WHERE id = ?', (movimiento_id,))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
