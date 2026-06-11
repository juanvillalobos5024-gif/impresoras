#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de verificación de la instalación
Verifica que todos los archivos y directorios necesarios existan
"""

import os
import sys
from pathlib import Path

def print_check(status, message):
    """Imprime un check o X"""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {message}")

def verify_installation():
    """Verifica que la instalación sea correcta"""
    print("\n" + "="*60)
    print("  Verificación de Instalación del Sistema")
    print("="*60 + "\n")
    
    all_ok = True
    
    # Verificar directorios
    print("📁 Verificando directorios:")
    dirs = [
        'app',
        'app/models',
        'app/routes',
        'app/database',
        'app/static',
        'app/static/css',
        'app/static/js',
        'app/static/uploads',
        'app/templates',
        'app/templates/auth',
        'app/templates/dashboard',
        'app/templates/impresoras',
        'app/templates/contadores',
        'app/templates/toners',
        'app/templates/productos',
        'app/templates/movimientos',
    ]
    
    for dir_path in dirs:
        exists = os.path.isdir(dir_path)
        print_check(exists, f"  {dir_path}/")
        if not exists:
            all_ok = False
    
    # Verificar archivos Python
    print("\n🐍 Verificando archivos Python:")
    python_files = [
        'app.py',
        'app/__init__.py',
        'app/database/__init__.py',
        'app/database/db.py',
        'app/models/__init__.py',
        'app/models/usuario.py',
        'app/models/impresora.py',
        'app/models/contador.py',
        'app/models/toner.py',
        'app/models/producto.py',
        'app/models/movimiento.py',
        'app/routes/__init__.py',
        'app/routes/auth.py',
        'app/routes/dashboard.py',
        'app/routes/impresoras.py',
        'app/routes/contadores.py',
        'app/routes/toners.py',
        'app/routes/productos.py',
        'app/routes/movimientos.py',
    ]
    
    for file_path in python_files:
        exists = os.path.isfile(file_path)
        print_check(exists, f"  {file_path}")
        if not exists:
            all_ok = False
    
    # Verificar templates
    print("\n🎨 Verificando templates HTML:")
    templates = [
        'app/templates/base.html',
        'app/templates/auth/login.html',
        'app/templates/auth/cambiar_contraseña.html',
        'app/templates/dashboard/index.html',
        'app/templates/impresoras/listar.html',
        'app/templates/impresoras/crear.html',
        'app/templates/impresoras/editar.html',
        'app/templates/impresoras/detalle.html',
        'app/templates/contadores/listar.html',
        'app/templates/contadores/crear.html',
        'app/templates/contadores/editar.html',
        'app/templates/toners/listar.html',
        'app/templates/toners/crear.html',
        'app/templates/toners/retirar.html',
        'app/templates/productos/listar.html',
        'app/templates/productos/crear.html',
        'app/templates/productos/editar.html',
        'app/templates/productos/detalle.html',
        'app/templates/productos/bajo_stock.html',
        'app/templates/movimientos/listar.html',
        'app/templates/movimientos/crear.html',
    ]
    
    for template_path in templates:
        exists = os.path.isfile(template_path)
        print_check(exists, f"  {template_path}")
        if not exists:
            all_ok = False
    
    # Verificar archivos estáticos
    print("\n📄 Verificando archivos estáticos:")
    static_files = [
        'app/static/css/style.css',
        'app/static/js/main.js',
    ]
    
    for static_path in static_files:
        exists = os.path.isfile(static_path)
        print_check(exists, f"  {static_path}")
        if not exists:
            all_ok = False
    
    # Verificar archivos de configuración
    print("\n⚙️  Verificando archivos de configuración:")
    config_files = [
        'requirements.txt',
        'README.md',
        'DOCUMENTACION.md',
        'INICIO_RAPIDO.md',
        '.gitignore',
        '.env.example',
    ]
    
    for config_path in config_files:
        exists = os.path.isfile(config_path)
        print_check(exists, f"  {config_path}")
        if not exists and config_path not in ['requirements.txt', 'README.md']:
            # Algunos archivos opcionales
            pass
        elif not exists:
            all_ok = False
    
    # Verificar Python
    print("\n🔍 Verificando entorno Python:")
    python_ok = sys.version_info >= (3, 8)
    print_check(python_ok, f"  Python {sys.version_info.major}.{sys.version_info.minor} (requerido 3.8+)")
    if not python_ok:
        all_ok = False
    
    # Verificar dependencias
    print("\n📦 Verificando dependencias Python:")
    required_packages = [
        'flask',
        'werkzeug',
        'qrcode',
        'pillow',
        'flask-session',
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print_check(True, f"  {package}")
        except ImportError:
            print_check(False, f"  {package} (NO INSTALADO)")
            all_ok = False
    
    # Resumen
    print("\n" + "="*60)
    if all_ok:
        print("✅ ¡Verificación completada exitosamente!")
        print("\n🚀 Puedes iniciar la aplicación con: python app.py")
    else:
        print("❌ Se encontraron problemas en la verificación")
        print("\n💡 Soluciones:")
        print("  1. Verifica que estés en el directorio correcto")
        print("  2. Ejecuta: pip install -r requirements.txt")
        print("  3. Consulta README.md para más detalles")
    print("="*60 + "\n")
    
    return all_ok

if __name__ == '__main__':
    success = verify_installation()
    sys.exit(0 if success else 1)
