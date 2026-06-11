"""
Rutas del Módulo de Impresoras
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, session
from app.routes.auth import login_required, admin_required
from app.models.impresora import Impresora
from app.models.contador import Contador
from app.models.toner import Toner
from werkzeug.utils import secure_filename
import os

impresoras_bp = Blueprint('impresoras', __name__, url_prefix='/impresoras')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'app/static/uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@impresoras_bp.route('/')
@login_required
def listar():
    """Listar todas las impresoras"""
    impresoras = Impresora.obtener_todas()
    return render_template('impresoras/listar.html', impresoras=impresoras)

@impresoras_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear():
    """Crear una nueva impresora"""
    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            
            # Procesar fotografía
            if 'fotografia' in request.files:
                file = request.files['fotografia']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    datos['fotografía'] = filename
            
            impresora = Impresora.crear(datos)
            flash('Impresora creada exitosamente.', 'success')
            return redirect(url_for('impresoras.detalle', id=impresora['id']))
        except Exception as e:
            flash(f'Error al crear la impresora: {str(e)}', 'danger')
    
    return render_template('impresoras/crear.html')

@impresoras_bp.route('/<int:id>')
@login_required
def detalle(id):
    """Ver detalle de una impresora"""
    impresora = Impresora.obtener_por_id(id)
    
    if not impresora:
        flash('Impresora no encontrada.', 'danger')
        return redirect(url_for('impresoras.listar'))
    
    # Obtener contadores
    contadores = Contador.obtener_por_impresora(id)
    
    # Obtener tóners
    toners = Toner.obtener_por_impresora(id)
    toner_actual = Toner.obtener_instalado(id)
    rendimiento_promedio = Toner.obtener_rendimiento_promedio(id)
    
    # Gráfica de impresiones
    grafica_data = Contador.obtener_grafica_mensual(id)
    
    return render_template('impresoras/detalle.html',
                         impresora=impresora,
                         contadores=contadores,
                         toners=toners,
                         toner_actual=toner_actual,
                         rendimiento_promedio=rendimiento_promedio,
                         grafica_data=grafica_data)

@impresoras_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    """Editar una impresora"""
    impresora = Impresora.obtener_por_id(id)
    
    if not impresora:
        flash('Impresora no encontrada.', 'danger')
        return redirect(url_for('impresoras.listar'))
    
    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            
            # Procesar fotografía
            if 'fotografia' in request.files:
                file = request.files['fotografia']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    datos['fotografía'] = filename
            
            Impresora.actualizar(id, datos)
            flash('Impresora actualizada exitosamente.', 'success')
            return redirect(url_for('impresoras.detalle', id=id))
        except Exception as e:
            flash(f'Error al actualizar la impresora: {str(e)}', 'danger')
    
    return render_template('impresoras/editar.html', impresora=impresora)

@impresoras_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar(id):
    """Eliminar una impresora"""
    try:
        Impresora.eliminar(id)
        flash('Impresora eliminada exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar la impresora: {str(e)}', 'danger')
    
    return redirect(url_for('impresoras.listar'))

@impresoras_bp.route('/buscar')
@login_required
def buscar():
    """Buscar impresoras"""
    termino = request.args.get('q', '')
    impresoras = Impresora.buscar(termino) if termino else []
    return render_template('impresoras/listar.html',
                         impresoras=impresoras,
                         termino_busqueda=termino)

@impresoras_bp.route('/<int:id>/qr')
@login_required
def descargar_qr(id):
    """Descargar QR de una impresora"""
    impresora = Impresora.obtener_por_id(id)
    
    if not impresora or not impresora['qr_codigo']:
        flash('Código QR no disponible.', 'danger')
        return redirect(url_for('impresoras.detalle', id=id))
    
    qr_path = os.path.join(UPLOAD_FOLDER, impresora['qr_codigo'])
    
    if not os.path.exists(qr_path):
        flash('Archivo QR no encontrado.', 'danger')
        return redirect(url_for('impresoras.detalle', id=id))
    
    return send_file(qr_path, as_attachment=True,
                    download_name=f"qr_impresora_{impresora['codigo_interno']}.png")
