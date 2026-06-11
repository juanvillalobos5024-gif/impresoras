"""
Aplicación Flask - Sistema de Control de Impresoras y Gestión de Consumibles TI
"""
from flask import Flask, session
from flask_session import Session
import os
import tempfile
from datetime import timedelta

# Importar base de datos
from app.database.db import init_db

# Importar blueprints
from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.impresoras import impresoras_bp
from app.routes.contadores import contadores_bp
from app.routes.toners import toners_bp
from app.routes.productos import productos_bp
from app.routes.movimientos import movimientos_bp

def create_app():
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Configuración
    app.config['SECRET_KEY'] = 'tu-clave-secreta-segura-cambiar-en-produccion'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_COOKIE_SECURE'] = False  # Cambiar a True en producción con HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # En Vercel, usa la sesión de Flask basada en cookies si el directorio no es escribible
    app.config['SESSION_COOKIE_NAME'] = 'session'
    use_filesystem_session = not bool(os.getenv('VERCEL') or os.getenv('VERCEL_ENV'))
    if use_filesystem_session:
        session_dir = os.getenv('SESSION_FILE_DIR') or os.path.join(tempfile.gettempdir(), 'flask_session')
        try:
            os.makedirs(session_dir, exist_ok=True)
            test_path = os.path.join(session_dir, '.session_test')
            with open(test_path, 'w', encoding='utf-8') as f:
                f.write('ok')
            os.remove(test_path)
        except OSError:
            use_filesystem_session = False

    if use_filesystem_session:
        app.config['SESSION_TYPE'] = 'filesystem'
        session_dir = os.getenv('SESSION_FILE_DIR') or os.path.join(tempfile.gettempdir(), 'flask_session')
        app.config['SESSION_FILE_DIR'] = session_dir
        app.config['SESSION_FILE_THRESHOLD'] = 500
        app.config['SESSION_FILE_MODE'] = 0o600
        Session(app)
    
    # Inicializar base de datos
    with app.app_context():
        init_db()
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(impresoras_bp)
    app.register_blueprint(contadores_bp)
    app.register_blueprint(toners_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(movimientos_bp)
    
    # Funciones de contexto global para templates
    @app.context_processor
    def inject_user():
        """Inyectar datos del usuario en los templates"""
        return {
            'usuario_id': session.get('usuario_id'),
            'usuario_nombre': session.get('usuario_nombre'),
            'usuario_rol': session.get('usuario_rol')
        }
    
    # Manejadores de errores
    @app.errorhandler(404)
    def not_found(error):
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>404 - Página no encontrada</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            <div class="container d-flex align-items-center justify-content-center" style="min-height: 100vh;">
                <div class="text-center">
                    <h1 class="display-1 fw-bold text-danger">404</h1>
                    <p class="fs-3 fw-semibold">Página no encontrada</p>
                    <p class="text-muted mb-4">Lo siento, la página que buscas no existe.</p>
                    <a href="/" class="btn btn-primary">Volver al inicio</a>
                </div>
            </div>
        </body>
        </html>
        ''', 404
    
    @app.errorhandler(500)
    def server_error(error):
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>500 - Error del servidor</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            <div class="container d-flex align-items-center justify-content-center" style="min-height: 100vh;">
                <div class="text-center">
                    <h1 class="display-1 fw-bold text-danger">500</h1>
                    <p class="fs-3 fw-semibold">Error del servidor</p>
                    <p class="text-muted mb-4">Algo salió mal. Por favor, intenta más tarde.</p>
                    <a href="/" class="btn btn-primary">Volver al inicio</a>
                </div>
            </div>
        </body>
        </html>
        ''', 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
