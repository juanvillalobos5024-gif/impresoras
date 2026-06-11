## 🎬 Demostración de Características

### 📺 Pantalla de Login
```
┌─────────────────────────────────────────┐
│  Sistema de Control de Impresoras TI    │
│                                         │
│  📧 admin@sistema.com                   │
│  🔑 admin123                            │
│                                         │
│  [Iniciar Sesión]                       │
│                                         │
│  Credenciales de prueba ↑               │
└─────────────────────────────────────────┘
```

### 📊 Dashboard Principal
```
┌─────────────────────────────────────────────────────────┐
│  🏠 Dashboard                                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐         │
│  │  Total     │ │  Activas   │ │  Pag.Este  │         │
│  │ Impresoras │ │            │ │    Mes    │         │
│  │    15      │ │     12     │ │  45,230   │         │
│  └────────────┘ └────────────┘ └────────────┘         │
│                                                         │
│  [Gráfica: Impresiones por Mes]                        │
│  [Gráfica: Movimientos Inventario]                     │
│  [Top 10 Impresoras]                                   │
│  [Últimos Movimientos]                                 │
│  [Inventario por Categoría]                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 🖨️ Módulo de Impresoras

**Lista de Impresoras:**
```
┌─────────────────────────────────────────────────────────┐
│ Impresoras | ➕ Nueva Impresora | 🔍 Buscar           │
├─────────────────────────────────────────────────────────┤
│ Código   │ Marca/Modelo │ Ubicación │ Área │ IP        │
├──────────┼──────────────┼───────────┼──────┼──────────┤
│ IMP-001  │ HP LaserJet  │ Piso 1    │ Adm  │ 192.1... │
│ IMP-002  │ Xerox C245   │ Piso 2    │ IT   │ 192.2... │
│ IMP-003  │ Brother DCP  │ Piso 1    │ Rec  │ 192.3... │
└─────────────────────────────────────────────────────────┘
```

**Detalle de Impresora:**
```
┌─────────────────────────────────────────────────────────┐
│ IMP-001 - HP LaserJet M428  [🔧 Editar] [QR] [←]      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Información General:                                   │
│  Marca: HP                  Serie: CNK2341502N         │
│  Modelo: LaserJet M428     IP: 192.168.1.50           │
│  Ubicación: Piso 1, Recepción                         │
│  Área: Recepción           Responsable: Juan García   │
│                                                         │
│ [📊 Contadores] [🥁 Tóners]                           │
│                                                         │
│ Últimas Lecturas:                                      │
│ Fecha      │ Contador Anterior │ Actual │ Páginas    │
│ 2024-06-15 │ 125,480          │ 127,340 │ 1,860    │
│ 2024-06-08 │ 123,250          │ 125,480 │ 2,230    │
│                                                         │
│ [Gráfica: Últimas 12 Meses]                           │
│                                                         │
│ Tóners Instalados:                                     │
│ Referencia: CF279A (Instalado hace 45 días)           │
│ [🔴 Retirar Tóner]                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 📈 Módulo de Contadores

**Registrar Lectura:**
```
┌─────────────────────────────────────────────────────────┐
│ Registrar Lectura de Contador                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Impresora: [Dropdown: IMP-001 HP LaserJet]            │
│ Fecha:     [06/15/2024]                               │
│                                                         │
│ Contador Anterior: 125,480 (auto-cargado)             │
│ Contador Actual:   [127340___________]                │
│                                                         │
│ ℹ️  Páginas Impresas: 1,860                            │
│                                                         │
│ Observaciones: [Lectura manual verificada]            │
│                                                         │
│ [Guardar] [Cancelar]                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 🥁 Módulo de Tóners

**Instalar Tóner:**
```
┌─────────────────────────────────────────────────────────┐
│ Instalar Tóner                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Impresora:          [IMP-001 HP LaserJet]             │
│ Referencia:         [CF279A_______________]            │
│ Fecha Instalación:  [06/15/2024]                      │
│ Contador:           [127340_______________]            │
│ Observaciones:      [Original HP]                      │
│                                                         │
│ [Guardar] [Cancelar]                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 📦 Módulo de Consumibles

**Inventario:**
```
┌─────────────────────────────────────────────────────────┐
│ Consumibles | 🔍 Búsqueda | Categoría: [Todos ▼]     │
├─────────────────────────────────────────────────────────┤
│ Código  │ Nombre        │ Stock │ Mínimo │ Precio     │
├─────────┼───────────────┼───────┼────────┼──────────┤
│ TON-001 │ Tóner HP 79A  │ 12    │ 5      │ $45,000  │
│ TON-002 │ Tóner BR TN660│ 3  🔴 │ 5      │ $35,000  │
│ MOUSE-01│ Logitech M705 │ 25    │ 10     │ $25,000  │
│ CABLE-01│ HDMI 2m       │ 8  🟡 │ 10     │ $12,000  │
└─────────────────────────────────────────────────────────┘

🔴 Bajo Stock: 3 productos requieren compra inmediata
```

### 🔄 Módulo de Movimientos

**Registrar Movimiento:**
```
┌─────────────────────────────────────────────────────────┐
│ Registrar Movimiento de Inventario                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Tipo: [Entrada ▼]                                     │
│ Producto: [Tóner HP 79A ▼]                            │
│ Cantidad: [5___________]                               │
│ Fecha: [06/15/2024]                                   │
│ Responsable: Juan García (auto)                        │
│ Observaciones: [Compra Proveedor ABC]                 │
│                                                         │
│ Stock Actual: 12 → 17 (después de este movimiento)   │
│                                                         │
│ [Guardar] [Cancelar]                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 🔐 Seguridad

**Cambiar Contraseña:**
```
┌─────────────────────────────────────────────────────────┐
│ Cambiar Contraseña                                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Contraseña Actual:    [•••••••]                        │
│ Nueva Contraseña:     [•••••••] (mín. 6 caracteres)   │
│ Confirmar:            [•••••••]                        │
│                                                         │
│ [Guardar] [Cancelar]                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 Elementos Visuales

### Indicadores de Estado

**Impresoras:**
```
🟢 Activa           🟡 Mantenimiento       🔴 Fuera de Servicio
```

**Stock:**
```
🟢 Normal (>= mínimo)
🟡 Bajo (90-100% de mínimo)
🔴 Crítico (< mínimo)
```

**Movimientos:**
```
🟢 Entrada (compra)
🔴 Salida (uso/consumo)
```

### Gráficas Interactivas

- **Línea**: Tendencia de impresiones mensuales
- **Barras**: Comparativa entrada vs salida de inventario
- **Tabla**: Top 10 impresoras por volumen
- **Pie**: Distribución de consumibles por categoría

---

## 📱 Funcionalidades Automáticas

### Cálculos Automáticos
- ✅ Páginas impresas = Contador Actual - Contador Anterior
- ✅ Rendimiento tóner = Contador Retiro - Contador Instalación
- ✅ Stock = Stock Anterior + Entradas - Salidas
- ✅ Valor inventario = Cantidad × Precio Unitario

### Generación Automática
- ✅ Código QR por impresora (PNG)
- ✅ Fecha/Hora de creación
- ✅ ID de usuario en cada operación
- ✅ Resumen estadístico

### Alertas Automáticas
- ✅ Bajo stock (< mínimo)
- ✅ Impresora sin lectura (30+ días)
- ✅ Rendimiento tóner bajo (< promedio)
- ✅ Mantenimiento próximo

---

## 🎯 Casos de Uso Reales

### Mañana: Inspección Diaria
1. Revisar dashboard
2. Identificar 3 impresoras con bajo stock de tóner
3. Registrar lecturas
4. Crear órdenes de compra

### Viernes: Reporte Semanal
1. Exportar tabla de consumibles
2. Generar gráfica de impresiones
3. Identificar impresoras con mayor volumen
4. Planificar mantenimiento

### Fin de Mes: Cierre
1. Registrar todos los contadores
2. Generar reporte de movimientos
3. Calcular costo de tóners usados
4. Hacer backup de BD

---

**Sistema Completo y Funcional** ✅
