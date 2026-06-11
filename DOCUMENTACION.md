# Documentación del Sistema

## 📖 Guía de Uso

### Roles y Permisos

#### Administrador
- ✅ Crear impresoras
- ✅ Editar impresoras
- ✅ Eliminar impresoras
- ✅ Crear productos
- ✅ Editar productos
- ✅ Eliminar productos
- ✅ Ver todos los reportes
- ✅ Descargar códigos QR

#### Técnico
- ✅ Ver impresoras
- ✅ Registrar lecturas de contador
- ✅ Instalar/retirar tóners
- ✅ Registrar movimientos de inventario
- ✅ Ver inventario
- ✅ Ver dashboard
- ❌ No puede crear/editar/eliminar impresoras
- ❌ No puede crear/editar/eliminar productos

### Flujos de Trabajo Principales

#### 1. Registrar una Nueva Impresora

1. Ir a **Impresoras** > **Crear Nueva** (solo Admin)
2. Completar todos los campos requeridos:
   - Código interno (único)
   - Marca, modelo, serie
   - Dirección IP
   - Ubicación y área
   - Responsable (opcional)
3. Subir fotografía (opcional)
4. Guardar

✅ Sistema genera automáticamente:
- Código QR
- Registro en BD

#### 2. Registrar Lectura de Contador

1. Ir a **Impresoras** > **Registrar Lectura** o desde detalle de impresora
2. Seleccionar impresora
3. Ingresar:
   - Fecha de lectura
   - Contador anterior (se carga automáticamente)
   - Contador actual
4. Sistema calcula automáticamente **Páginas Impresas**
5. Guardar

✅ El sistema actualiza:
- Historial de contadores
- Estadísticas de volumen
- Top impresoras

#### 3. Instalar Tóner

1. Ir a **Tóner** > **Instalar Tóner** o desde detalle de impresora
2. Seleccionar impresora
3. Ingresar:
   - Referencia del tóner (ej: CF279A)
   - Fecha de instalación
   - Contador al instalar
4. Guardar

✅ Sistema registra:
- Tóner activo en la impresora
- Fecha de instalación
- Contador inicial

#### 4. Registrar Movimiento de Inventario

1. Ir a **Consumibles** > **Registrar Movimiento**
2. Seleccionar:
   - Tipo: Entrada o Salida
   - Producto
   - Cantidad
   - Fecha
3. Agregar observaciones (opcional)
4. Guardar

✅ Sistema actualiza:
- Stock del producto
- Historial de movimientos
- Alertas si stock < mínimo

## 🎯 Casos de Uso

### Caso 1: Mantenimiento de Impresora

**Situación**: Impresora necesita mantenimiento
1. Ir a detalles de la impresora
2. Click en **Editar**
3. Cambiar estado a **"Mantenimiento"**
4. Agregar observaciones
5. Guardar

**Resultado**: 
- Impresora marcada como no disponible
- Se excluye de reportes de activas
- Se registra en historial

### Caso 2: Tóner Bajo Rendimiento

**Situación**: Un tóner no rinde lo esperado
1. Ir a **Tóner** > Detalle del tóner
2. Si el rendimiento es anormalmente bajo:
   - Ir a detalles de la impresora
   - Registrar un nuevo tóner
   - El anterior se marca como "Retirado"
3. Sistema calcula automáticamente el rendimiento

### Caso 3: Reorganizar Inventario

**Situación**: Se necesita cambiar ubicación de productos
1. Ir a **Consumibles** > **Inventario**
2. Click en el producto
3. Click en **Editar**
4. Cambiar ubicación
5. Guardar

**Nota**: Los movimientos de inventario NO afectan el stock, solo registran entrada/salida de transacciones

## 📊 Entendiendo los Reportes

### Dashboard

| Card | Significado |
|------|-------------|
| **Total Impresoras** | Cantidad total de impresoras registradas |
| **Activas** | Impresoras en estado activo |
| **Páginas Impresas** | Suma de todas las páginas este mes |
| **Tóners Instalados** | Cantidad de tóners actualmente instalados |
| **Bajo Stock** | Productos con cantidad ≤ stock mínimo |
| **En Mantenimiento** | Impresoras fuera de operación |
| **Fuera de Servicio** | Impresoras deshabilitadas |

### Gráficas

**Impresiones por Mes**: 
- Muestra tendencia de volumen
- Útil para detectar picos de demanda
- Ayuda a planificar cambios de tóner

**Movimientos de Inventario**:
- Entradas vs Salidas
- Detecta desbalances
- Identifica períodos de alto consumo

**Top 10 Impresoras**:
- Las más usadas este mes
- Priorizar mantenimiento
- Planificar tóners

## 🔍 Búsqueda y Filtrado

### Buscar Impresoras
```
Criterios: Código, Marca, Modelo, Serie, Ubicación, Área
Resultado: Lista de impresoras coincidentes
```

### Filtrar por Categoría (Productos)
```
Categorías: Tóner, Mouse, Teclado, Monitor, Cables, RAM, SSD, etc.
Resultado: Solo productos de esa categoría
```

### Filtrar por Estado (Impresoras)
```
Estados: Activa, Mantenimiento, Fuera de Servicio
Resultado: Impresoras en ese estado
```

## ⚙️ Configuraciones Avanzadas

### Cambiar Stock Mínimo de un Producto

1. **Consumibles** > **Inventario**
2. Click en producto
3. Click en **Editar**
4. Cambiar "Stock Mínimo"
5. Guardar

**Nota**: Cuando `stock_actual ≤ stock_minimo`, se muestra alerta

### Retirar Impresora del Servicio

1. Ir a detalles de impresora
2. Click en **Editar**
3. Cambiar estado a **"Fuera de Servicio"**
4. Agregar motivo en observaciones
5. Guardar

**Resultado**:
- No apareceré en reportes activos
- Se puede reactivar editando estado nuevamente

### Anular un Movimiento de Inventario

1. **Consumibles** > **Movimientos**
2. Localizar el movimiento
3. Click en eliminar (🗑️)
4. Confirmar

**Resultado**:
- Movimiento eliminado
- Stock se revierte automáticamente
- Acción registrada en historial

## 📈 Analítica

### Rendimiento de Tóner

- **Cálculo**: Contador Retiro - Contador Instalación
- **Promedio por Impresora**: Media de todos los tóners retirados
- **Alerta**: Si rendimiento < promedio * 0.8 (20% bajo)

### Volumen de Impresión

- **Cálculo**: Contador Actual - Contador Anterior
- **Período**: Se agrupa por mes
- **Tendencia**: Gráfica de últimos 12 meses

### Stock Crítico

- **Alarma**: Cuando `stock ≤ stock_minimo`
- **Ubicación**: Visible en Dashboard
- **Acción**: Registrar movimiento de entrada (compra)

## 🔐 Seguridad y Buenas Prácticas

### Contraseñas
- ✅ Mínimo 6 caracteres
- ✅ Cambiar regularmente
- ✅ No compartir credenciales
- ✅ Usar contraseñas seguras

### Datos
- ✅ Backup periódico de BD
- ✅ No eliminar registros sin necesidad
- ✅ Mantener datos precisos
- ✅ Revisar movimientos sospechosos

### Acceso
- ✅ Usar roles apropiados
- ✅ No compartir cuentas
- ✅ Cerrar sesión al terminar
- ✅ Reportar accesos no autorizados

## 🆘 Troubleshooting

### Problema: "Base de datos bloqueada"
**Solución**:
1. Detener aplicación (CTRL+C)
2. Esperar 10 segundos
3. Reiniciar aplicación

### Problema: "Formulario no se envía"
**Solución**:
1. Verificar que todos los campos requeridos estén completos
2. Buscar mensajes de error en la página
3. Refrescar página (F5)
4. Limpiar caché del navegador

### Problema: "Las gráficas no se muestran"
**Solución**:
1. Verificar conexión a Internet (necesita Chart.js CDN)
2. Abrir consola del navegador (F12)
3. Buscar errores JavaScript
4. Verificar que hay datos para la gráfica

### Problema: "No puedo subir fotografía"
**Solución**:
1. Verificar formato: PNG, JPG, JPEG, GIF
2. Verificar tamaño < 5MB
3. Verificar permisos de carpeta `app/static/uploads`
4. Crear carpeta manualmente si no existe

## 📞 Contacto y Soporte

Para problemas técnicos, contactar al departamento de Sistemas:
- Email: sistemas@empresa.com
- Teléfono: (XX) XXXX-XXXX
- Ticket: [Sistema de tickets]

---

**Última actualización**: Junio 2024  
**Versión**: 1.0.0
