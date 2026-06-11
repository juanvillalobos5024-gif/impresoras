# ⚡ Referencia Rápida de Comandos

## 🚀 Iniciar el Sistema

```bash
# Activar entorno virtual
venv\Scripts\activate

# Ejecutar aplicación
python app.py

# Acceder
http://localhost:5000
```

## 📦 Gestionar Dependencias

```bash
# Instalar todas
pip install -r requirements.txt

# Instalar específico
pip install flask

# Actualizar paquete
pip install --upgrade flask

# Ver instalados
pip list

# Congelar versiones
pip freeze > requirements.txt
```

## 🔧 Verificación y Mantenimiento

```bash
# Verificar instalación
python verificar.py

# Verificar Python
python --version

# Eliminar caché Python
python -m py_compile app/

# Limpiar __pycache__
python -c "import shutil; shutil.rmtree('app/__pycache__', ignore_errors=True)"
```

## 🗄️ Base de Datos

```bash
# Conectarse a BD SQLite
sqlite3 app/database/app.db

# Listar tablas
.tables

# Ver esquema de tabla
.schema usuarios

# Hacer backup
copy app/database/app.db app/database/app.db.backup

# Restaurar backup
copy app/database/app.db.backup app/database/app.db

# Crear backup comprimido
# (Usar 7-Zip, WinRAR, o PowerShell)
Compress-Archive -Path app/database/app.db -DestinationPath backup_$(date +%Y%m%d).zip
```

## 🐍 Python Útil

```bash
# Ejecutar Python interactivo
python

# Importar app manualmente
python -c "from app import create_app; app = create_app()"

# Ejecutar script
python setup.py

# Debugging
python -m pdb app.py
```

## 🌐 Navegador / HTTP

```bash
# Aplicación
http://localhost:5000

# Dashboard
http://localhost:5000/

# Login
http://localhost:5000/login

# Impresoras
http://localhost:5000/impresoras/

# Consumibles
http://localhost:5000/productos/

# API Gráfica Mensual
http://localhost:5000/contadores/api/grafica-mensual

# Descargar QR
http://localhost:5000/impresoras/<ID>/qr
```

## 📁 Archivos Importantes

| Comando | Descripción |
|---------|-------------|
| `app.py` | Ejecutable principal |
| `requirements.txt` | Lista dependencias |
| `app/__init__.py` | Configuración Flask |
| `app/database/db.py` | BD y esquema |
| `app/database/app.db` | Base de datos (después de crear) |
| `app/static/uploads/` | Fotos y QR generados |

## 🛑 Detener/Controlar Aplicación

```bash
# Detener (en terminal donde corre)
Ctrl + C

# Matar proceso (si quedó colgado)
# Windows (buscar PID en puerto 5000)
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>

# O cambiar puerto en app.py
```

## 📊 Comandos de Git (si usas)

```bash
# Inicializar repo
git init

# Ver estado
git status

# Agregar archivos
git add .

# Commit
git commit -m "Mensaje"

# Ignore (ya incluido)
cat .gitignore

# Clonar
git clone <repositorio>
```

## 🔍 Buscar y Grep

```bash
# Buscar archivo
find . -name "*.py" -type f

# Buscar texto en archivos
grep -r "def crear" app/models/

# Contar líneas de código
find app -name "*.py" -exec wc -l {} +

# Ver estructura
tree app/
# O:
ls -R app/
```

## 📝 Editar Archivos

```bash
# Abrir en VS Code
code .

# Abrir archivo específico
code app/app.py

# Ver contenido
type app/requirements.txt  # Windows
cat app/requirements.txt   # Linux/Mac
```

## 🔐 Seguridad

```bash
# Generar clave segura (Python)
python -c "import secrets; print(secrets.token_hex(32))"

# Verificar contraseña (Python)
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('contraseña'))"

# Test contraseña (Python)
python -c "from werkzeug.security import check_password_hash; h='...'; print(check_password_hash(h, 'contraseña'))"
```

## 📈 Monitoreo

```bash
# Ver uso de memoria/CPU (Windows)
tasklist | findstr python
taskmgr

# Ver procesos Python (Linux)
ps aux | grep python

# Monitorizar archivos (Linux)
watch -n 1 "ls -la app/database/"

# Tamaño de BD
ls -lh app/database/app.db

# Tamaño total del proyecto
du -sh .
```

## 🧪 Testing (Opcional)

```bash
# Ejecutar tests (si existen)
python -m pytest

# Con cobertura
python -m pytest --cov=app

# Test específico
python -m pytest tests/test_auth.py
```

## 📦 Empaquetamiento

```bash
# Crear distributable
python setup.py sdist bdist_wheel

# Instalar en desarrollo
pip install -e .

# Construir ejecutable (pyinstaller)
pyinstaller --onefile app.py
```

## 🌍 Deployment

```bash
# Gunicorn (production)
pip install gunicorn
gunicorn app:app

# uWSGI (production)
pip install uwsgi
uwsgi --http :5000 --wsgi-file app.py --callable app

# Verificar con curl
curl http://localhost:5000/

# HEAD request (sin body)
curl -I http://localhost:5000/
```

## 📊 Estadísticas

```bash
# Contar líneas de código
find app -name "*.py" | xargs wc -l

# Contar archivos
find app -type f | wc -l

# Ver estructura (requiere tree)
tree app --dirsfirst

# Listar archivos grandes
du -h app/**/* | sort -rh | head -10
```

## 🎯 Atajos Útiles

| Atajo | Función |
|-------|---------|
| `Ctrl+C` | Detener aplicación |
| `F5` | Refrescar página |
| `F12` | Developer Tools (navegador) |
| `Ctrl+Shift+I` | Inspect (navegador) |
| `Ctrl+J` | Consola JavaScript |
| `Ctrl+Shift+K` | Logs (navegador) |

## 💡 Debugging

```bash
# Ver logs (en app.py)
# Flask imprime en consola automáticamente

# Habilitar debug máximo
# En app.py cambiar a:
app.run(debug=True)

# Ver requests HTTP
# En app.py agregar:
@app.before_request
def log_request():
    print(f"Request: {request.method} {request.path}")
```

## 🚨 Troubleshooting Rápido

```bash
# "No module named 'flask'"
pip install flask

# "Address already in use"
# Cambiar puerto en app.py o:
netstat -ano | findstr :5000

# "Database locked"
# Restart app o:
del app/database/app.db

# "Permission denied"
# Dar permisos:
chmod 755 app/static/uploads

# "Template not found"
# Verificar path en templates/
# Verificar que existe el archivo .html
```

---

## 📍 Estructura de Paths

```
d:\EVIM\Documents\Nueva carpeta\
├── app.py              ← Ejecutar desde aquí
├── app/
│   ├── __init__.py     ← Config Flask
│   ├── database/
│   │   └── app.db      ← Base de datos
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/    ← Fotos/QR aquí
│   └── templates/      ← HTML aquí
└── venv/               ← Ambiente virtual
```

---

## ⏱️ Tiempos Típicos

| Operación | Tiempo |
|-----------|--------|
| Instalar dependencias | 2-3 minutos |
| Iniciar app | 2-3 segundos |
| Crear impresora | 1 segundo |
| Cargar dashboard | 1-2 segundos |
| Gráfica render | 1 segundo |
| Generar QR | 0.5 segundos |

---

**Mantén esta página abierta mientras trabajas** 🔖

---

**Referencia Rápida v1.0** | Última actualización: Junio 2024
