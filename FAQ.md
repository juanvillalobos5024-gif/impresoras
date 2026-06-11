# ❓ Preguntas Frecuentes (FAQ)

## Instalación y Configuración

### P: ¿Cómo instalo el sistema?
**R:** Hay 3 formas:

**Rápida (recomendada):**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Interactiva:**
```bash
python setup.py
```

**Manual:**
Ver `INICIO_RAPIDO.md`

---

### P: ¿Qué versión de Python necesito?
**R:** Python 3.8 o superior. Verificar con:
```bash
python --version
```

---

### P: ¿Funciona en macOS/Linux?
**R:** Sí, funciona en cualquier plataforma. Solo cambian los comandos de activación:
- **Windows**: `venv\Scripts\activate`
- **macOS/Linux**: `source venv/bin/activate`

---

### P: ¿Puedo usar otro puerto que no sea 5000?
**R:** Sí. Edita `app.py` última línea:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Cambiar 5000 a otro
```

O instala una alternativa (localhost:8080):
```bash
python -c "from app import create_app; app=create_app(); app.run(port=8080)"
```

---

## Uso del Sistema

### P: ¿Cuáles son las credenciales por defecto?
**R:** 
- Email: `admin@sistema.com`
- Contraseña: `admin123`

⚠️ **Cambiar inmediatamente en producción**

---

### P: ¿Cómo creo un nuevo usuario?
**R:** Actualmente, solo el administrador puede crear usuarios editando la base de datos. Para producción, se recomienda implementar:
1. Módulo de gestión de usuarios en admin
2. O exportar datos y crear usuarios vía script SQL

---

### P: ¿Dónde se guardan los datos?
**R:** En SQLite: `app/database/app.db`

Para cambiar ubicación, edita `app/database/db.py`:
```python
DATABASE = '/nueva/ubicacion/app.db'
```

---

### P: ¿Puedo exportar datos?
**R:** Sí, las tablas tienen funciones de exportación a CSV desde JavaScript. Para exportar a Excel, se puede:
1. Usar la función CSV y abrir en Excel
2. Integrar librería `openpyxl` (ya en requirements.txt)
3. Crear endpoint `/api/export/excel`

---

## Problemas y Soluciones

### P: "ModuleNotFoundError: No module named 'flask'"
**R:** 
```bash
# Verificar que venv esté activado (debe mostrar (venv) en terminal)
pip install flask
# O reinstalar todo:
pip install -r requirements.txt
```

---

### P: "Address already in use"
**R:** El puerto 5000 está en uso:
```bash
# Opción 1: Cambiar puerto en app.py
# Opción 2: Liberar puerto (Windows):
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

### P: "Database is locked"
**R:** 
1. Cierra la aplicación (CTRL+C)
2. Espera 5 segundos
3. Reinicia

Si persiste:
```bash
# Elimina y reinicia
del app/database/app.db
python app.py
```

---

### P: Las gráficas no se muestran
**R:**
1. Abre F12 (Developer Tools)
2. Busca errores de JavaScript
3. Verifica conexión a Internet (necesita CDN de Chart.js)
4. Verifica que haya datos en la BD

---

### P: No puedo subir fotografías
**R:**
```bash
# Crear carpeta manualmente
mkdir app/static/uploads
# Verificar permisos de escritura
```

---

### P: La búsqueda no funciona
**R:** La búsqueda es case-insensitive. Prueba:
1. Escribir con menos caracteres
2. Buscar en campo de impresoras (no en otros módulos por ahora)

---

## Características y Funcionalidad

### P: ¿Qué es el código QR?
**R:** Cada impresora genera automáticamente un código QR que:
- Enlaza a la ficha técnica de la impresora
- Se descarga como PNG
- Se puede imprimir y pegar en la máquina

---

### P: ¿Cómo se calcula el rendimiento del tóner?
**R:** 
```
Rendimiento = Contador al Retirar - Contador al Instalar
Ej: 130,000 - 125,000 = 5,000 páginas
```

Se almacena al retirar el tóner.

---

### P: ¿Qué diferencia hay entre Administrador y Técnico?
**R:**

| Acción | Admin | Técnico |
|--------|:-----:|:-------:|
| Crear impresoras | ✅ | ❌ |
| Registrar contadores | ✅ | ✅ |
| Instalar tóners | ✅ | ✅ |
| Crear productos | ✅ | ❌ |
| Crear movimientos | ✅ | ✅ |
| Ver reportes | ✅ | ✅ |
| Descargar QR | ✅ | ✅ |

---

### P: ¿Cómo funcionan las alertas de bajo stock?
**R:**
1. Cada producto tiene `stock_minimo`
2. Cuando `stock_actual ≤ stock_minimo`, aparece alerta
3. Se muestra en Dashboard
4. Se puede ver en Consumibles > Bajo Stock

---

## Mantenimiento y Backup

### P: ¿Cómo hago backup de los datos?
**R:**
```bash
# Copiar el archivo de BD
copy app/database/app.db app/database/app.db.backup

# O comprimir:
# Usar 7-Zip o WinRAR para comprimir la BD
```

---

### P: ¿Cómo restauro un backup?
**R:**
```bash
# Detener aplicación (CTRL+C)
# Copiar backup
copy app/database/app.db.backup app/database/app.db
# Reiniciar
python app.py
```

---

### P: ¿Necesito hacer mantenimiento de BD?
**R:** SQLite es simple, pero para producción se recomienda:
1. Hacer backup diario
2. Monitorear tamaño de `app.db`
3. Limpiar registros antiguos regularmente
4. Migrar a MySQL si crece mucho

---

## Producción

### P: ¿Es seguro en producción?
**R:** Parcialmente. Antes de producción:

- [ ] Cambiar `SECRET_KEY` en `app/__init__.py`
- [ ] Cambiar contraseña de admin
- [ ] Habilitar HTTPS (`SESSION_COOKIE_SECURE=True`)
- [ ] Usar base de datos robusta (MySQL)
- [ ] Implementar backup automático
- [ ] Configurar logging
- [ ] Usar WSGI (Gunicorn, uWSGI)

---

### P: ¿Cómo despliego en producción?
**R:** Opciones:

**Local (simple):**
```bash
nohup python app.py &  # Linux
# O instalar como servicio en Windows
```

**Con Gunicorn:**
```bash
pip install gunicorn
gunicorn app:app --workers 4
```

**En la nube:**
- Heroku
- AWS
- Azure
- DigitalOcean

---

### P: ¿Necesito licencia para usar esto?
**R:** No, es software libre para uso interno de la empresa.

---

## Customización

### P: ¿Puedo cambiar los colores?
**R:** Sí. Edita `app/static/css/style.css`:
```css
:root {
  --primary-color: #0066cc;  /* Cambiar azul */
  --danger-color: #cc0000;   /* Cambiar rojo */
}
```

---

### P: ¿Puedo agregar más categorías de productos?
**R:** Sí. Edita `app/models/producto.py`:
```python
CATEGORIAS = [
    'Tóner',
    'Mouse',
    'Teclado',
    'Monitor',
    'Cable HDMI',
    'Cable VGA',
    'Cable de poder',
    'Memoria RAM',
    'Disco SSD',
    'Adaptadores',
    'Otros',
    'Nueva Categoría',  # Agregar aquí
]
```

---

### P: ¿Cómo agrego nuevos campos a impresoras?
**R:** Edita `app/database/db.py` en la tabla `CREATE TABLE impresoras` y luego `app/models/impresora.py`.

---

## Reportes y Análisis

### P: ¿Cómo genero reportes?
**R:** El sistema tiene:
1. **Dashboard**: KPIs principales
2. **Gráficas**: Impresiones y movimientos mensuales
3. **Exportación**: Tablas a CSV
4. **Top 10**: Impresoras por volumen

Para reportes más complejos, exporta a Excel y crea tablas dinámicas.

---

### P: ¿Puedo analizar tendencias?
**R:** Sí. Usa las gráficas del dashboard para:
1. Ver tendencia de impresiones (picos estacionales)
2. Analizar movimientos de inventario
3. Identificar impresoras problemáticas
4. Predecir necesidades de mantenimiento

---

## Contacto y Soporte

### P: ¿A quién contacto si tengo problemas?
**R:** 
- **Técnico**: Departamento de Sistemas
- **Reportar bugs**: sistemas@empresa.com
- **Documentación**: Consultar README.md, DOCUMENTACION.md

---

### P: ¿Hay un roadmap de nuevas características?
**R:** Sí, en README.md hay una lista de mejoras planeadas:
- SNMP automático
- Notificaciones por email
- Exportación a PDF
- API REST para móvil
- Backup automático
- Machine Learning para predicciones

---

## Referencias Técnicas

### Librerías Usadas
- **Flask 3.0.0**: Framework web
- **SQLite3**: Base de datos
- **Werkzeug 3.0.1**: Hashing de contraseñas
- **qrcode 7.4.2**: Generación de QR
- **Pillow 10.1.0**: Procesamiento de imágenes
- **Flask-Session 0.5.0**: Gestión de sesiones
- **Bootstrap 5.3.0**: Framework CSS
- **Chart.js 4.4.0**: Gráficas interactivas
- **Font Awesome 6.4.0**: Iconografía

### Estructuras de Base de Datos
Ver `ESTRUCTURA.md` para diagrama de tablas y relaciones.

### Endpoints API
Ver `README.md` sección "API Endpoints" para lista completa.

---

## Links Útiles

- **Flask Documentación**: https://flask.palletsprojects.com/
- **SQLite Documentación**: https://www.sqlite.org/docs.html
- **Bootstrap 5**: https://getbootstrap.com/docs/5.0/
- **Chart.js**: https://www.chartjs.org/docs/latest/
- **qrcode**: https://github.com/lincolnloop/python-qrcode

---

**¿No encontraste respuesta? Consulta DOCUMENTACION.md o contacta al departamento de Sistemas** 📞

---

**Última actualización**: Junio 2024  
**Versión del FAQ**: 1.0.0
