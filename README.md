# 🖨️ Sistema de Control de Impresoras y Gestión de Consumibles TI

Un sistema web profesional de gestión integral para controlar impresoras, tóners y consumibles de TI en empresas medianas.

## 🎯 Características Principales

### Módulo 1: Gestión de Impresoras
- Registro completo de impresoras (marca, modelo, serie, IP, ubicación, responsable)
- Estados: Activa, Mantenimiento, Fuera de Servicio
- Generación automática de códigos QR
- Fotografías y observaciones
- Búsqueda y filtrado avanzado

### Módulo 2: Contador de Impresiones
- Registro de lecturas de contador
- Cálculo automático de páginas impresas
- Historial completo por impresora
- Gráficas mensuales de volumen
- Identificación de impresoras sin lectura en 30 días

### Módulo 3: Gestión de Tóner
- Instalación y retiro de tóners
- Cálculo automático de rendimiento
- Rendimiento promedio por impresora
- Historial completo

### Módulo 4: Inventario de Consumibles
- 11 categorías predefinidas (Tóner, Mouse, Teclado, Monitor, Cables, RAM, SSD, Adaptadores, etc.)
- Control de stock con alertas de bajo stock
- Gestión de proveedores y ubicaciones
- Seguimiento de precios

### Módulo 5: Movimientos de Inventario
- Registro de entradas y salidas
- Actualización automática de stock
- Historial completo con trazabilidad
- Filtrado por periodo

### Módulo 6: Dashboard
- Tarjetas con KPIs principales
- Gráficas interactivas con Chart.js
- Top 10 impresoras por volumen
- Últimos movimientos
- Productos con bajo stock

### Módulo 7: Alertas
- Consumibles con stock mínimo
- Impresoras sin lectura en 30 días
- Rendimiento de tóners fuera del promedio

### Módulo 8: Códigos QR
- Generación automática por impresora
- Escaneo para acceder a ficha técnica
- Descarga de códigos QR

## 🛠️ Stack Tecnológico

- **Backend**: Python 3 + Flask
- **Base de Datos**: SQLite (migrable a MySQL)
- **Frontend**: HTML5 + Bootstrap 5 + JavaScript
- **Gráficas**: Chart.js
- **Códigos QR**: qrcode + Pillow
- **Autenticación**: Werkzeug (hashing seguro)

## 📋 Requisitos

- Python 3.8+
- pip (gestor de paquetes)
- Navegador web moderno

## 🚀 Instalación Rápida

### 1. Clonar/Descargar el proyecto
```bash
cd "ruta/del/proyecto"
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Ejecutar la aplicación
```bash
python app.py
```

### 6. Acceder a la aplicación
```
http://localhost:5000
```

## 📝 Credenciales por Defecto

- **Email**: `admin@sistema.com`
- **Contraseña**: `admin123`

⚠️ **Importante**: Cambiar estas credenciales en producción

## 📁 Estructura del Proyecto

```
/
├── app/
│   ├── __init__.py              # Inicialización de Flask
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py                # Configuración y esquema BD
│   ├── models/
│   │   ├── __init__.py
│   │   ├── usuario.py           # Modelo Usuario
│   │   ├── impresora.py         # Modelo Impresora
│   │   ├── contador.py          # Modelo Contador
│   │   ├── toner.py             # Modelo Tóner
│   │   ├── producto.py          # Modelo Producto
│   │   └── movimiento.py        # Modelo Movimiento
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py              # Rutas autenticación
│   │   ├── dashboard.py         # Rutas dashboard
│   │   ├── impresoras.py        # Rutas impresoras
│   │   ├── contadores.py        # Rutas contadores
│   │   ├── toners.py            # Rutas tóners
│   │   ├── productos.py         # Rutas productos
│   │   └── movimientos.py       # Rutas movimientos
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Estilos personalizados
│   │   ├── js/
│   │   │   └── main.js          # JavaScript principal
│   │   └── uploads/             # Fotografías y QR
│   └── templates/
│       ├── base.html            # Template base
│       ├── auth/
│       │   ├── login.html
│       │   └── cambiar_contraseña.html
│       ├── dashboard/
│       │   └── index.html
│       ├── impresoras/
│       ├── contadores/
│       ├── toners/
│       ├── productos/
│       └── movimientos/
├── app.py                        # Punto de entrada
├── requirements.txt              # Dependencias
└── README.md                     # Este archivo
```

## 🔐 Seguridad

- ✅ Contraseñas hasheadas con Werkzeug
- ✅ Sesiones seguras con signing
- ✅ Protección CSRF (Flask-Session)
- ✅ Validación de entrada en formularios
- ✅ Roles de usuario (Admin, Técnico)
- ✅ Control de acceso por ruta

## 📊 Modelos de Base de Datos

### Tablas principales:
- `usuarios` - Cuentas de usuario con autenticación
- `impresoras` - Registro de impresoras
- `contadores` - Lecturas de contador
- `toners` - Historial de tóners instalados/retirados
- `productos` - Inventario de consumibles
- `movimientos` - Entrada/salida de inventario

## 🎨 Interfaz

- **Diseño Responsivo**: Funciona en desktop, tablet y mobile
- **Bootstrap 5**: Componentes modernos y profesionales
- **Tema Oscuro Compatible**: Con Bootstrap 5
- **Gráficas Interactivas**: Chart.js para visualización de datos
- **Iconografía**: Font Awesome 6

## 🔄 Funcionalidades Principales

### Búsqueda y Filtrado
- Búsqueda global de impresoras
- Filtrado por área, estado, tipo
- Búsqueda de productos por categoría
- Historial filtrado por período

### Reportes
- Exportación de datos (exportación a CSV)
- Gráficas de tendencias mensuales
- Top impresoras por volumen
- Análisis de consumibles

### Notificaciones
- Alertas de bajo stock
- Alertas de impresoras sin lectura
- Rendimiento de tóners fuera de norma

## 🛠️ Configuración Avanzada

### Cambiar Clave Secreta (producción)
En `app/__init__.py`, línea 16:
```python
app.config['SECRET_KEY'] = 'tu-nueva-clave-segura-aqui'
```

### Habilitar HTTPS
En `app/__init__.py`, línea 21:
```python
app.config['SESSION_COOKIE_SECURE'] = True  # Cambiar a True con HTTPS
```

### Migrar a MySQL
1. Instalar: `pip install mysql-connector-python`
2. Modificar `app/database/db.py`
3. Usar SQLAlchemy para mejor soporte multi-DB

## 🐛 Troubleshooting

**Error: "No module named 'flask'"**
```bash
pip install -r requirements.txt
```

**Puerto 5000 en uso**
```bash
python app.py --port 5001
```

**Base de datos corrupta**
- Eliminar archivo `app/database/app.db`
- La BD se recreará automáticamente

## 📱 API Endpoints

### Autenticación
- `POST /login` - Iniciar sesión
- `GET /logout` - Cerrar sesión
- `POST /cambiar-contraseña` - Cambiar contraseña

### Dashboard
- `GET /` - Dashboard principal

### Impresoras
- `GET /impresoras/` - Listar
- `POST /impresoras/crear` - Crear
- `GET /impresoras/<id>` - Detalle
- `POST /impresoras/<id>/editar` - Editar
- `POST /impresoras/<id>/eliminar` - Eliminar
- `GET /impresoras/buscar` - Búsqueda

### Contadores
- `GET /contadores/` - Listar
- `POST /contadores/crear` - Registrar lectura
- `GET /contadores/api/grafica-mensual` - Datos gráfica

### Y más... (ver rutas en `app/routes/`)

## 📞 Soporte

Para reportar bugs o sugerir mejoras, contactar al departamento de sistemas.

## 📄 Licencia

Uso interno - Propiedad de la empresa

## 👨‍💻 Desarrollado por

**Senior Python Developer**
Especialista en Flask, SQLite, Bootstrap

---

## 🎯 Próximas Mejoras

- [ ] Integración con SNMP para lectores automáticos
- [ ] Notificaciones por email
- [ ] Exportación a PDF con reportes
- [ ] API REST para aplicaciones móviles
- [ ] Backup automático de base de datos
- [ ] Análisis de tendencias y predicciones
- [ ] Integración con Active Directory

---

**Versión**: 1.0.0  
**Última actualización**: Junio 2024  
**Compatibilidad**: Python 3.8+
#   i m p r e s o r a s  
 