"""
Rutas del Módulo de Movimientos
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.routes.auth import login_required
from app.models.movimiento import Movimiento
from app.models.producto import Producto

movimientos_bp = Blueprint('movimientos', __name__, url_prefix='/movimientos')

@movimientos_bp.route('/')
@login_required
def listar():
    """Listar todos los movimientos"""
    movimientos = Movimiento.obtener_todos()
    return render_template('movimientos/listar.html', movimientos=movimientos)

@movimientos_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """Crear un nuevo movimiento"""
    productos = Producto.obtener_todos()
    
    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            datos['cantidad'] = int(datos.get('cantidad', 0))
            datos['responsable_id'] = session.get('usuario_id')
            
            movimiento_id = Movimiento.crear(datos)
            flash('Movimiento registrado exitosamente.', 'success')
            return redirect(url_for('movimientos.listar'))
        except Exception as e:
            flash(f'Error al registrar el movimiento: {str(e)}', 'danger')
    
    return render_template('movimientos/crear.html',
                         productos=productos,
                         tipos=['entrada', 'salida'])

@movimientos_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar(id):
    """Eliminar un movimiento (reversión)"""
    try:
        Movimiento.eliminar(id)
        flash('Movimiento revertido exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al revertir el movimiento: {str(e)}', 'danger')
    
    return redirect(url_for('movimientos.listar'))

@movimientos_bp.route('/producto/<int:producto_id>')
@login_required
def por_producto(producto_id):
    """Ver movimientos de un producto"""
    producto = Producto.obtener_por_id(producto_id)
    
    if not producto:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('movimientos.listar'))
    
    movimientos = Movimiento.obtener_por_producto(producto_id)
    
    return render_template('movimientos/por_producto.html',
                         producto=producto,
                         movimientos=movimientos)

@movimientos_bp.route('/mes/<mes>')
@login_required
def por_mes(mes):
    """Ver movimientos de un mes específico"""
    movimientos = Movimiento.obtener_por_mes(mes)
    
    return render_template('movimientos/listar.html',
                         movimientos=movimientos,
                         mes_seleccionado=mes)
