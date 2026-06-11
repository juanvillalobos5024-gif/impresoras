#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Guía de Instalación y Ejecución
Sistema de Control de Impresoras y Gestión de Consumibles TI
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Imprime un encabezado formateado"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_step(step, text):
    """Imprime un paso numerado"""
    print(f"\n{step}. {text}")
    print("-" * 60)

def check_python_version():
    """Verifica si la versión de Python es correcta"""
    print_header("Verificación de Requisitos")
    print(f"Versión de Python: {sys.version}")
    
    if sys.version_info < (3, 8):
        print("❌ Se requiere Python 3.8 o superior")
        sys.exit(1)
    else:
        print("✅ Versión de Python correcta")

def create_virtual_env():
    """Crea un entorno virtual"""
    print_step(1, "Crear Entorno Virtual")
    
    if os.path.exists('venv'):
        print("⚠️  Ya existe un entorno virtual")
    else:
        try:
            subprocess.check_call([sys.executable, '-m', 'venv', 'venv'])
            print("✅ Entorno virtual creado")
        except Exception as e:
            print(f"❌ Error al crear entorno virtual: {e}")
            sys.exit(1)

def activate_virtual_env():
    """Muestra instrucciones para activar el entorno virtual"""
    print_step(2, "Activar Entorno Virtual")
    
    if sys.platform == "win32":
        print("Windows:")
        print("  venv\\Scripts\\activate")
    else:
        print("macOS/Linux:")
        print("  source venv/bin/activate")

def install_dependencies():
    """Instala las dependencias del proyecto"""
    print_step(3, "Instalar Dependencias")
    
    try:
        print("Instalando paquetes desde requirements.txt...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencias instaladas correctamente")
    except Exception as e:
        print(f"❌ Error al instalar dependencias: {e}")
        sys.exit(1)

def initialize_database():
    """Inicializa la base de datos"""
    print_step(4, "Inicializar Base de Datos")
    
    try:
        from app.database.db import init_db
        init_db()
        print("✅ Base de datos inicializada")
    except Exception as e:
        print(f"❌ Error al inicializar BD: {e}")
        sys.exit(1)

def create_env_file():
    """Crea archivo .env si no existe"""
    if not os.path.exists('.env'):
        try:
            with open('.env.example', 'r') as source:
                with open('.env', 'w') as dest:
                    dest.write(source.read())
            print("✅ Archivo .env creado (basado en .env.example)")
        except:
            print("⚠️  No se pudo crear .env, continuando...")

def print_usage():
    """Imprime instrucciones de uso"""
    print_header("Instrucciones de Uso")
    
    print("\n📝 Para iniciar la aplicación:")
    print("   python app.py")
    
    print("\n🌐 Acceder a la aplicación en:")
    print("   http://localhost:5000")
    
    print("\n🔐 Credenciales por defecto:")
    print("   Email: admin@sistema.com")
    print("   Contraseña: admin123")
    
    print("\n⚠️  IMPORTANTE para Producción:")
    print("   1. Cambiar SECRET_KEY en app/__init__.py")
    print("   2. Cambiar credenciales de administrador")
    print("   3. Habilitar HTTPS")
    print("   4. Usar una base de datos robusta (MySQL)")

def main():
    """Función principal"""
    print_header("Sistema de Control de Impresoras TI - Instalación")
    
    # Verificar Python
    check_python_version()
    
    # Crear entorno virtual
    create_virtual_env()
    
    # Activar entorno virtual
    activate_virtual_env()
    
    # Instalar dependencias (solo si está el entorno activo o se ejecuta directamente)
    print_step(3, "Instalar Dependencias")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencias instaladas correctamente")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Crear archivo .env
    create_env_file()
    
    # Inicializar BD
    try:
        initialize_database()
    except ImportError:
        print("⚠️  No se pudo inicializar la BD automáticamente")
        print("   Intenta ejecutar: python app.py")
    
    # Mostrar instrucciones de uso
    print_usage()
    
    print("\n✅ Instalación completada. ¡Listo para usar!")

if __name__ == '__main__':
    main()
