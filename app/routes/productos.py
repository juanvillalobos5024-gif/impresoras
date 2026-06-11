"""
Rutas del Módulo de Productos
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.routes.auth import login_required, admin_required
from app.models.producto import Producto, CATEGORIAS

productos_bp = Blueprint('productos', __name__, url_prefix='/productos')

@productos_bp.route('/')
@login_required
def listar():
    """Listar todos los productos"""
    categoria_filter = request.args.get('categoria')
    
    if categoria_filter:
        productos = Producto.obtener_por_categoria(categoria_filter)
    else:
        productos = Producto.obtener_todos()
    
    return render_template('productos/listar.html',
                         productos=productos,
                         categorias=CATEGORIAS,
                         categoria_seleccionada=categoria_filter)

@productos_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear():
    """Crear un nuevo producto"""
    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            datos['stock_actual'] = int(datos.get('stock_actual', 0))
            datos['stock_minimo'] = int(datos.get('stock_minimo', 5))
            datos['precio_unitario'] = float(datos.get('precio_unitario', 0))
            
            producto_id = Producto.crear(datos)
            flash('Producto creado exitosamente.', 'success')
            return redirect(url_for('productos.detalle', id=producto_id))
        except Exception as e:
            flash(f'Error al crear el producto: {str(e)}', 'danger')
    
    return render_template('productos/crear.html', categorias=CATEGORIAS)

@productos_bp.route('/<int:id>')
@login_required
def detalle(id):
    """Ver detalle de un producto"""
    producto = Producto.obtener_por_id(id)
    
    if not producto:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('productos.listar'))
    
    return render_template('productos/detalle.html', producto=producto)

@productos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    """Editar un producto"""
    producto = Producto.obtener_por_id(id)
    
    if not producto:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('productos.listar'))
    
    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            datos['stock_minimo'] = int(datos.get('stock_minimo', 5))
            datos['precio_unitario'] = float(datos.get('precio_unitario', 0))
            
            Producto.actualizar(id, datos)
            flash('Producto actualizado exitosamente.', 'success')
            return redirect(url_for('productos.detalle', id=id))
        except Exception as e:
            flash(f'Error al actualizar el producto: {str(e)}', 'danger')
    
    return render_template('productos/editar.html',
                         producto=producto,
                         categorias=CATEGORIAS)

@productos_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar(id):
    """Eliminar un producto"""
    try:
        Producto.eliminar(id)
        flash('Producto eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el producto: {str(e)}', 'danger')
    
    return redirect(url_for('productos.listar'))

@productos_bp.route('/bajo-stock')
@login_required
def bajo_stock():
    """Ver productos con bajo stock"""
    productos = Producto.obtener_bajo_stock()
    return render_template('productos/bajo_stock.html', productos=productos)

@productos_bp.route('/buscar')
@login_required
def buscar():
    """Buscar productos"""
    termino = request.args.get('q', '')
    productos = Producto.buscar(termino) if termino else []
    
    return render_template('productos/listar.html',
                         productos=productos,
                         termino_busqueda=termino,
                         categorias=CATEGORIAS)
