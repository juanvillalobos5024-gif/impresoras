"""
Configuración de la aplicación Flask
Sistema de Control de Impresoras y Gestión de Consumibles TI

Ejecutar: python app.py
Acceder: http://localhost:5000
"""

if __name__ == '__main__':
    from app import create_app
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   Sistema de Control de Impresoras y Consumibles TI      ║
    ║                    Iniciando...                          ║
    ╚══════════════════════════════════════════════════════════╝
    
    """)
    
    try:
        app = create_app()
        print("""
    ✅ Aplicación iniciada correctamente
    
    🌐 Accede a:  http://localhost:5000
    🔐 Email:     admin@sistema.com
    🔑 Contraseña: admin123
    
    ⚠️  Presiona CTRL+C para detener
        """)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    except Exception as e:
        print(f"""
    ❌ Error al iniciar la aplicación:
    {str(e)}
    
    Soluciones posibles:
    1. Ejecuta: pip install -r requirements.txt
    2. Verifica que Python 3.8+ esté instalado
    3. Comprueba que el puerto 5000 esté disponible
        """)
        exit(1)
