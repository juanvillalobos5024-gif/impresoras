## 🚀 INICIO RÁPIDO - 5 MINUTOS

### Paso 1: Requisitos
- Windows, macOS o Linux
- Python 3.8 o superior
- Navegador web

### Paso 2: Descargar Dependencias (2 minutos)

**Windows:**
```bash
cd "ruta\del\proyecto"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
cd ruta/del/proyecto
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Paso 3: Ejecutar la Aplicación (1 minuto)

```bash
python app.py
```

Verás un mensaje como este:
```
╔══════════════════════════════════════════════════════════╗
║   Sistema de Control de Impresoras y Consumibles TI      ║
║                    Iniciando...                          ║
╚══════════════════════════════════════════════════════════╝

✅ Aplicación iniciada correctamente

🌐 Accede a:  http://localhost:5000
🔐 Email:     admin@sistema.com
🔑 Contraseña: admin123

⚠️  Presiona CTRL+C para detener
```

### Paso 4: Acceder a la Aplicación (30 segundos)

1. Abre tu navegador
2. Escribe: `http://localhost:5000`
3. Inicia sesión con:
   - **Email**: `admin@sistema.com`
   - **Contraseña**: `admin123`

## ✨ ¡Listo! Ya estás dentro del sistema

### Primeros pasos recomendados:

1. **Cambiar contraseña de admin** (Perfil > Cambiar Contraseña)
2. **Crear una impresora** (Impresoras > Nueva)
3. **Registrar una lectura** (Contadores > Registrar Lectura)
4. **Explorar el Dashboard** (desde el inicio)

## 📌 Notas Importantes

- ⚠️ **NO ejecutes `venv\Scripts\activate` nuevamente si ya está activo**
- ⚠️ **El puerto 5000 debe estar disponible**
- ⚠️ **Cambia las credenciales por defecto antes de producción**
- ⚠️ **Haz backup de `app/database/app.db` regularmente**

## 🔧 Si Algo Sale Mal

### Error: "No module named 'flask'"
```bash
# Asegurate de activar el entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Luego instala dependencias
pip install -r requirements.txt
```

### Error: "Address already in use"
- El puerto 5000 está en uso por otra aplicación
- Soluciones:
  1. Cierra la otra aplicación
  2. O usa otro puerto:
     ```bash
     # Edita app.py y cambia: app.run(..., port=5001)
     ```

### Error: "Cannot open app.db"
- Permisos de acceso a base de datos
- Solución:
  ```bash
  # Elimina la BD y se recreará automáticamente
  del app/database/app.db
  # O en macOS/Linux:
  rm app/database/app.db
  ```

## 📚 Para Aprender Más

- **Documentación completa**: Ver `README.md`
- **Guía de uso**: Ver `DOCUMENTACION.md`
- **Estructura del proyecto**: Ver estructura en `README.md`

---

**¡Felicidades! El sistema está listo para usar** ✅
