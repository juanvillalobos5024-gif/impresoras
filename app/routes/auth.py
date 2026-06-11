"""
Rutas de Autenticación
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.usuario import Usuario
from werkzeug.security import check_password_hash
import functools

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    """Decorator para verificar si el usuario está autenticado"""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesión primero.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator para verificar si el usuario es administrador"""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesión primero.', 'warning')
            return redirect(url_for('auth.login'))
        
        usuario = Usuario.obtener_por_id(session['usuario_id'])
        if usuario.rol != 'administrador':
            flash('No tienes permiso para acceder a esta página.', 'danger')
            return redirect(url_for('dashboard.index'))
        
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login de usuario"""
    if request.method == 'POST':
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        
        usuario = Usuario.obtener_por_email(email)
        
        if usuario and usuario.verificar_contraseña(contraseña):
            session['usuario_id'] = usuario.id
            session['usuario_nombre'] = usuario.nombre
            session['usuario_rol'] = usuario.rol
            flash(f'¡Bienvenido {usuario.nombre}!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Email o contraseña incorrectos.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout de usuario"""
    session.clear()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/cambiar-contraseña', methods=['GET', 'POST'])
@login_required
def cambiar_contraseña():
    """Cambiar contraseña del usuario"""
    if request.method == 'POST':
        contraseña_actual = request.form.get('contraseña_actual')
        contraseña_nueva = request.form.get('contraseña_nueva')
        contraseña_confirmar = request.form.get('contraseña_confirmar')
        
        usuario = Usuario.obtener_por_id(session['usuario_id'])
        
        if not usuario.verificar_contraseña(contraseña_actual):
            flash('La contraseña actual es incorrecta.', 'danger')
        elif contraseña_nueva != contraseña_confirmar:
            flash('Las contraseñas nuevas no coinciden.', 'danger')
        elif len(contraseña_nueva) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
        else:
            usuario.cambiar_contraseña(contraseña_nueva)
            flash('Contraseña cambiada correctamente.', 'success')
            return redirect(url_for('dashboard.index'))
    
    return render_template('auth/cambiar_contraseña.html')
