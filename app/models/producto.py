"""
Modelo de Producto/Consumible
"""
from app.database.db import get_db_connection

CATEGORIAS = [
    'Tóner',
    'Mouse',
    'Teclado',
    'Monitor',
    'Cable HDMI',
    'Cable VGA',
    'Cable de poder',
    'Memoria RAM',
    'Disco SSD',
    'Adaptadores',
    'Otros'
]

class Producto:
    @staticmethod
    def crear(datos):
        """Crea un nuevo producto"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO productos 
                (codigo, nombre, categoria, marca, stock_actual, stock_minimo, 
                 precio_unitario, proveedor, ubicacion, fecha_compra)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos.get('codigo'),
                datos.get('nombre'),
                datos.get('categoria'),
                datos.get('marca'),
                datos.get('stock_actual', 0),
                datos.get('stock_minimo', 5),
                datos.get('precio_unitario'),
                datos.get('proveedor'),
                datos.get('ubicacion'),
                datos.get('fecha_compra')
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def obtener_por_id(producto_id):
        """Obtiene un producto por ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los productos"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos ORDER BY nombre')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def obtener_por_categoria(categoria):
        """Obtiene productos por categoría"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE categoria = ? ORDER BY nombre', 
                      (categoria,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def obtener_bajo_stock():
        """Obtiene productos con bajo stock"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM productos 
            WHERE stock_actual <= stock_minimo 
            ORDER BY stock_actual ASC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def buscar(termino):
        """Busca productos por término"""
        conn = get_db_connection()
        cursor = conn.cursor()
        termino = f"%{termino}%"
        cursor.execute('''
            SELECT * FROM productos 
            WHERE codigo LIKE ? OR nombre LIKE ? OR marca LIKE ? OR proveedor LIKE ?
            ORDER BY nombre
        ''', (termino, termino, termino, termino))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def actualizar(producto_id, datos):
        """Actualiza un producto"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE productos 
                SET nombre = ?, categoria = ?, marca = ?, stock_minimo = ?,
                    precio_unitario = ?, proveedor = ?, ubicacion = ?
                WHERE id = ?
            ''', (
                datos.get('nombre'),
                datos.get('categoria'),
                datos.get('marca'),
                datos.get('stock_minimo'),
                datos.get('precio_unitario'),
                datos.get('proveedor'),
                datos.get('ubicacion'),
                producto_id
            ))
            conn.commit()
        finally:
            conn.close()
    
    @staticmethod
    def actualizar_stock(producto_id, nueva_cantidad):
        """Actualiza el stock de un producto"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE productos SET stock_actual = ? WHERE id = ?
            ''', (nueva_cantidad, producto_id))
            conn.commit()
        finally:
            conn.close()
    
    @staticmethod
    def eliminar(producto_id):
        """Elimina un producto"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
            conn.commit()
        finally:
            conn.close()
    
    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas de inventario"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM productos')
        total = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as bajo_stock FROM productos WHERE stock_actual <= stock_minimo')
        bajo_stock = cursor.fetchone()['bajo_stock']
        
        cursor.execute('SELECT SUM(stock_actual * precio_unitario) as valor_total FROM productos')
        valor_total = cursor.fetchone()['valor_total'] or 0
        
        cursor.execute('''
            SELECT categoria, COUNT(*) as cantidad, SUM(stock_actual) as stock_total
            FROM productos 
            GROUP BY categoria
            ORDER BY cantidad DESC
        ''')
        por_categoria = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'total': total,
            'bajo_stock': bajo_stock,
            'valor_total': round(valor_total, 2),
            'por_categoria': por_categoria
        }
