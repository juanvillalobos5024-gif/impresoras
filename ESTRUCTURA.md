# 📋 Índice del Proyecto - Sistema de Control de Impresoras TI

## Archivos en Raíz

| Archivo | Descripción |
|---------|-------------|
| `app.py` | **Punto de entrada principal** - Ejecutar con: `python app.py` |
| `run.py` | Script alternativo de ejecución (más detallado) |
| `verificar.py` | ✅ Script de verificación de instalación |
| `setup.py` | 📝 Guía interactiva de instalación |
| `requirements.txt` | 📦 Lista de dependencias Python |
| `README.md` | 📖 Documentación completa del proyecto |
| `DOCUMENTACION.md` | 📚 Guía detallada de uso y casos de uso |
| `INICIO_RAPIDO.md` | ⚡ Guía de inicio en 5 minutos |
| `.env.example` | ⚙️ Archivo de configuración de ejemplo |
| `.gitignore` | 🚫 Archivos ignorados por git |
| `ESTRUCTURA.md` | 📋 Este archivo - Índice del proyecto |

## 📁 Estructura de Directorios

```
/app
├── __init__.py                          # 🔧 Inicialización de Flask (factory pattern)
│
├── /database                             # 🗄️ Capa de Base de Datos
│   ├── __init__.py
│   └── db.py                             # Configuración SQLite, esquema, conexiones
│
├── /models                               # 📊 Modelos de Datos (MVC)
│   ├── __init__.py
│   ├── usuario.py                        # 👤 Modelo Usuario (autenticación)
│   ├── impresora.py                      # 🖨️ Modelo Impresora + QR
│   ├── contador.py                       # 📈 Modelo Contador Impresiones
│   ├── toner.py                          # 🥁 Modelo Gestión Tóner
│   ├── producto.py                       # 📦 Modelo Inventario Consumibles
│   └── movimiento.py                     # 🔄 Modelo Movimientos Inventario
│
├── /routes                               # 🛣️ Rutas/Controladores (MVC)
│   ├── __init__.py
│   ├── auth.py                           # 🔐 Rutas de Autenticación
│   ├── dashboard.py                      # 📊 Rutas Dashboard
│   ├── impresoras.py                     # 🖨️ CRUD Impresoras
│   ├── contadores.py                     # 📈 Rutas Contadores
│   ├── toners.py                         # 🥁 Rutas Tóners
│   ├── productos.py                      # 📦 CRUD Productos
│   └── movimientos.py                    # 🔄 Rutas Movimientos
│
├── /static                               # 🎨 Recursos Estáticos
│   ├── /css
│   │   └── style.css                     # 🎨 Estilos Bootstrap personalizados
│   ├── /js
│   │   └── main.js                       # ⚙️ JavaScript utilities y funciones
│   ├── /uploads                          # 📸 Fotografías de impresoras y QR
│   │   └── (generado dinámicamente)
│   └── (otros recursos)
│
└── /templates                            # 🎭 Vistas HTML (MVC)
    ├── base.html                         # 📄 Template base (navbar, footer)
    │
    ├── /auth                             # 🔐 Vistas de Autenticación
    │   ├── login.html                    # Login con demo credentials
    │   └── cambiar_contraseña.html       # Cambio de contraseña
    │
    ├── /dashboard                        # 📊 Vistas del Dashboard
    │   └── index.html                    # Dashboard con KPIs y gráficas
    │
    ├── /impresoras                       # 🖨️ Vistas de Impresoras
    │   ├── listar.html                   # Tabla de impresoras con búsqueda
    │   ├── crear.html                    # Formulario crear impresora
    │   ├── editar.html                   # Formulario editar impresora
    │   └── detalle.html                  # Vista detalle + historial + gráficas
    │
    ├── /contadores                       # 📈 Vistas de Contadores
    │   ├── listar.html                   # Tabla de lecturas
    │   ├── crear.html                    # Registrar lectura (con cálculo auto)
    │   └── editar.html                   # Editar lectura
    │
    ├── /toners                           # 🥁 Vistas de Tóners
    │   ├── listar.html                   # Tabla de tóners instalados/retirados
    │   ├── crear.html                    # Instalar tóner
    │   └── retirar.html                  # Retirar tóner (con cálculo rendimiento)
    │
    ├── /productos                        # 📦 Vistas de Productos
    │   ├── listar.html                   # Tabla inventario con filtro categoría
    │   ├── crear.html                    # Formulario nuevo producto
    │   ├── editar.html                   # Formulario editar producto
    │   ├── detalle.html                  # Vista detalle + estadísticas
    │   └── bajo_stock.html               # Tabla de alertas de bajo stock
    │
    └── /movimientos                      # 🔄 Vistas de Movimientos
        ├── listar.html                   # Tabla de movimientos (entrada/salida)
        └── crear.html                    # Formulario registrar movimiento
```

## 🔑 Módulos Principales

### 1. **Autenticación** (`app/routes/auth.py`)
- Login/Logout
- Cambio de contraseña
- Decoradores: `@login_required`, `@admin_required`

### 2. **Dashboard** (`app/routes/dashboard.py`)
- KPIs principales
- Gráficas con Chart.js
- Últimos movimientos

### 3. **Impresoras** (`app/routes/impresoras.py`, `app/models/impresora.py`)
- CRUD completo
- Generación automática QR
- Búsqueda avanzada
- Vista detalle con historial

### 4. **Contadores** (`app/routes/contadores.py`, `app/models/contador.py`)
- Registro de lecturas
- Cálculo automático de páginas
- Gráficas mensuales
- Top impresoras

### 5. **Tóners** (`app/routes/toners.py`, `app/models/toner.py`)
- Instalar/retirar tóners
- Cálculo automático rendimiento
- Rendimiento promedio por impresora

### 6. **Productos** (`app/routes/productos.py`, `app/models/producto.py`)
- CRUD inventario
- Gestión de categorías
- Alertas bajo stock
- Búsqueda por categoría

### 7. **Movimientos** (`app/routes/movimientos.py`, `app/models/movimiento.py`)
- Registro entrada/salida
- Actualización automática stock
- Historial completo con reversión

## 🗄️ Base de Datos

### Tabla: `usuarios`
```sql
id, nombre, email (UNIQUE), contraseña (hashed), rol, estado, fecha_creacion
```

### Tabla: `impresoras`
```sql
id, codigo_interno, marca, modelo, numero_serie, direccion_ip, ubicación, 
área, responsable, tipo, estado, fecha_instalacion, fotografía, observaciones, 
qr_codigo, fecha_creacion, ultimo_contador_registro
```

### Tabla: `contadores`
```sql
id, impresora_id (FK), fecha, contador_anterior, contador_actual, 
paginas_impresas (auto), tecnico_id (FK), observaciones, fecha_creacion
```

### Tabla: `toners`
```sql
id, impresora_id (FK), referencia, fecha_instalacion, contador_instalacion, 
fecha_retiro, contador_retiro, rendimiento_obtenido (auto), estado, 
tecnico_id (FK), observaciones, fecha_creacion
```

### Tabla: `productos`
```sql
id, codigo (UNIQUE), nombre, categoría, marca, stock_actual, stock_minimo, 
precio_unitario, proveedor, ubicación, fecha_compra, fecha_creacion
```

### Tabla: `movimientos`
```sql
id, tipo (entrada/salida), producto_id (FK), cantidad, fecha, 
responsable_id (FK), observaciones, fecha_creacion
```

## 🎯 Flujo de la Aplicación

```
usuario accede a http://localhost:5000
    ↓
[auth.py] ¿Sesión válida?
    ├─ NO → Redirige a login
    │       ↓
    │   [login.html] Ingresa credenciales
    │       ↓
    │   [auth.py] Valida usuario
    │
    └─ SÍ → [dashboard.py] Carga Dashboard
            ↓
        [dashboard/index.html] + Gráficas
            ↓
        Menú de navegación:
        ├─ Impresoras → [impresoras.py]
        ├─ Consumibles → [productos.py]
        ├─ Contadores → [contadores.py]
        ├─ Tóners → [toners.py]
        ├─ Movimientos → [movimientos.py]
        └─ Usuario → [auth.py]
```

## 🚀 Iniciar la Aplicación

1. **Activar entorno virtual**
   ```bash
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Instalar dependencias** (primera vez)
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar**
   ```bash
   python app.py
   # o
   python run.py
   ```

4. **Verificar instalación** (opcional)
   ```bash
   python verificar.py
   ```

## 📊 Configuración

- **HOST**: 0.0.0.0 (accesible desde cualquier máquina)
- **PORT**: 5000
- **DEBUG**: True (desarrollo)
- **DATABASE**: SQLite en `app/database/app.db`

## 🔐 Roles y Permisos

| Acción | Administrador | Técnico |
|--------|:-------------:|:-------:|
| Ver dashboard | ✅ | ✅ |
| Ver impresoras | ✅ | ✅ |
| Crear impresora | ✅ | ❌ |
| Registrar contador | ✅ | ✅ |
| Instalar tóner | ✅ | ✅ |
| Ver inventario | ✅ | ✅ |
| Crear producto | ✅ | ❌ |
| Registrar movimiento | ✅ | ✅ |

## 📞 Archivo de Contacto

Mantenimiento y soporte: **sistemas@empresa.com**

---

**Proyecto Completo - Sistema de Control de Impresoras TI** ✅  
**Versión**: 1.0.0  
**Última actualización**: Junio 2024
