"""
Rutas del Módulo de Tóner
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.database.db import get_db_connection
from app.routes.auth import login_required
from app.models.toner import Toner
from app.models.impresora import Impresora

toners_bp = Blueprint('toners', __name__, url_prefix='/toners')

@toners_bp.route('/')
@login_required
def listar():
    """Listar todos los tóners"""
    impresoras = Impresora.obtener_todas()
    
    # Filtrar por impresora si se proporciona
    impresora_id = request.args.get('impresora_id')
    
    if impresora_id:
        toners = Toner.obtener_por_impresora(int(impresora_id))
        impresora_seleccionada = Impresora.obtener_por_id(int(impresora_id))
    else:
        toners = Toner.obtener_todos()
        impresora_seleccionada = None
    
    return render_template('toners/listar.html',
                         toners=toners,
                         impresoras=impresoras,
                         impresora_seleccionada=impresora_seleccionada)

@toners_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """Crear un nuevo registro de tóner"""
    impresoras = Impresora.obtener_todas()
    
    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            datos['tecnico_id'] = session.get('usuario_id')
            datos['contador_instalacion'] = int(datos.get('contador_instalacion', 0))
            
            toner_id = Toner.crear(datos)
            flash('Tóner instalado exitosamente.', 'success')
            
            impresora_id = datos.get('impresora_id')
            return redirect(url_for('impresoras.detalle', id=impresora_id))
        except Exception as e:
            flash(f'Error al instalar el tóner: {str(e)}', 'danger')
    
    return render_template('toners/crear.html', impresoras=impresoras)

@toners_bp.route('/<int:id>/retirar', methods=['GET', 'POST'])
@login_required
def retirar(id):
    """Retirar un tóner"""
    conn = __import__('app.database.db', fromlist=['get_db_connection']).get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM toners WHERE id = ?', (id,))
    toner = cursor.fetchone()
    conn.close()
    
    if not toner:
        flash('Tóner no encontrado.', 'danger')
        return redirect(url_for('toners.listar'))
    
    toner = dict(toner)
    
    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            datos['contador_instalacion'] = toner['contador_instalacion']
            datos['contador_retiro'] = int(datos.get('contador_retiro', 0))
            
            Toner.retirar_toner(id, datos)
            flash('Tóner retirado exitosamente.', 'success')
            return redirect(url_for('impresoras.detalle', id=toner['impresora_id']))
        except Exception as e:
            flash(f'Error al retirar el tóner: {str(e)}', 'danger')
    
    return render_template('toners/retirar.html', toner=toner)

@toners_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Editar un tóner"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM toners WHERE id = ?', (id,))
    toner = cursor.fetchone()
    conn.close()

    if not toner:
        flash('Tóner no encontrado.', 'danger')
        return redirect(url_for('toners.listar'))

    toner = dict(toner)
    impresoras = Impresora.obtener_todas()

    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            datos['contador_instalacion'] = int(datos.get('contador_instalacion', toner.get('contador_instalacion', 0)) or 0)
            datos['estado'] = toner.get('estado')

            Toner.actualizar(id, datos)
            flash('Tóner actualizado exitosamente.', 'success')
            return redirect(url_for('impresoras.detalle', id=toner['impresora_id']))
        except Exception as e:
            flash(f'Error al actualizar el tóner: {str(e)}', 'danger')

    return render_template('toners/editar.html', toner=toner, impresoras=impresoras)

@toners_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar(id):
    """Eliminar un registro de tóner"""
    conn = __import__('app.database.db', fromlist=['get_db_connection']).get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT impresora_id FROM toners WHERE id = ?', (id,))
    result = cursor.fetchone()
    conn.close()
    
    impresora_id = result['impresora_id'] if result else None
    
    try:
        Toner.eliminar(id)
        flash('Tóner eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el tóner: {str(e)}', 'danger')
    
    return redirect(url_for('impresoras.detalle', id=impresora_id)) if impresora_id \
           else redirect(url_for('toners.listar'))
