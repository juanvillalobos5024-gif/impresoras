# ✅ LISTA DE VERIFICACIÓN - Sistema Listo para Usar

## Pre-Ejecución (Realizar antes de iniciar)

- [ ] Python 3.8+ instalado: `python --version`
- [ ] Estar en el directorio correcto: `d:\EVIM\Documents\Nueva carpeta`
- [ ] Archivo `requirements.txt` existe
- [ ] Archivo `app.py` existe
- [ ] Carpeta `app/` existe con subcarpetas

## Instalación (Primera vez)

- [ ] Crear entorno virtual: `python -m venv venv`
- [ ] Activar: `venv\Scripts\activate`
- [ ] Instalar dependencias: `pip install -r requirements.txt`
- [ ] Verificación: `python verificar.py` ✅ (sin errores)

## Ejecución

- [ ] Entorno virtual activado (venv está en amarillo en terminal)
- [ ] Ejecutar: `python app.py`
- [ ] Mensaje de inicio correcto aparece
- [ ] No hay errores en la consola
- [ ] URL http://localhost:5000 es accesible

## Pruebas Funcionales (Primera vez)

- [ ] **Login**: 
  - Email: `admin@sistema.com`
  - Password: `admin123`
  - ✅ Se carga dashboard

- [ ] **Impresoras**:
  - [ ] Ver listado
  - [ ] Crear nueva impresora (llenar todos los campos)
  - [ ] Verificar que aparece en lista
  - [ ] Ir a detalle
  - [ ] Descargar QR
  - [ ] Editar impresora

- [ ] **Contador**:
  - [ ] Crear nueva lectura
  - [ ] Verificar cálculo automático de páginas
  - [ ] Ver gráfica en detalle de impresora

- [ ] **Tóner**:
  - [ ] Instalar tóner en la impresora
  - [ ] Aparecer en tab de tóners
  - [ ] Retirar tóner
  - [ ] Verificar cálculo de rendimiento

- [ ] **Productos**:
  - [ ] Crear nuevo producto
  - [ ] Verificar que aparece
  - [ ] Crear movimiento (entrada)
  - [ ] Verificar actualización de stock

- [ ] **Movimientos**:
  - [ ] Crear salida de producto
  - [ ] Verificar stock decrece
  - [ ] Eliminar movimiento
  - [ ] Verificar reversión de stock

- [ ] **Dashboard**:
  - [ ] Tarjetas KPI muestran datos
  - [ ] Gráficas renderean correctamente
  - [ ] Top impresoras aparece
  - [ ] Últimos movimientos se muestran

- [ ] **Seguridad**:
  - [ ] Cambiar contraseña funciona
  - [ ] Logout y login nuevamente
  - [ ] No acceso sin autenticación

## Performance y Estabilidad

- [ ] Dashboard carga en < 2 segundos
- [ ] Búsquedas responden rápido
- [ ] Gráficas se renderean sin problemas
- [ ] No hay errores en consola del navegador
- [ ] Sin warnings en servidor Python

## Datos de Prueba Creados

Después de las pruebas, deberías tener:
- [ ] ≥ 1 impresora creada
- [ ] ≥ 1 lectura de contador registrada
- [ ] ≥ 1 tóner instalado
- [ ] ≥ 1 producto en inventario
- [ ] ≥ 2 movimientos registrados

## Preparación para Producción

- [ ] ⚠️ Cambiar `SECRET_KEY` en `app/__init__.py`
- [ ] ⚠️ Cambiar contraseña de admin
- [ ] ⚠️ Crear usuario adicional (técnico)
- [ ] ⚠️ Hacer backup de `app/database/app.db`
- [ ] ⚠️ Revisar `.env.example` para producción

## Archivos de Documentación

- [ ] README.md - Leído para referencia
- [ ] INICIO_RAPIDO.md - Consultado si hay dudas
- [ ] DOCUMENTACION.md - Para procedimientos específicos
- [ ] ESTRUCTURA.md - Entendimiento del proyecto
- [ ] DEMO.md - Casos de uso revisados

## Solución de Problemas Comunes

Si algo no funciona:

1. **Error al iniciar**: 
   - [ ] Verificar: `python verificar.py`
   - [ ] Reinstalar: `pip install -r requirements.txt --force-reinstall`

2. **Base de datos corrupta**:
   - [ ] Eliminar: `app/database/app.db`
   - [ ] Reiniciar: `python app.py`

3. **Puerto ocupado**:
   - [ ] Cambiar puerto en `app.py` línea 8
   - [ ] O: `netstat -ano | findstr :5000` (Windows)

4. **No se carga la página**:
   - [ ] Limpiar caché: CTRL+SHIFT+DEL
   - [ ] Probar en navegador diferente
   - [ ] Reiniciar servidor

## Confirmación Final

- [ ] ✅ Proyecto instalado correctamente
- [ ] ✅ Aplicación ejecutándose
- [ ] ✅ Todas las pruebas funcionales pasadas
- [ ] ✅ Documentación revisada
- [ ] ✅ Listo para uso en producción

---

## 🎯 Próximos Pasos

1. **Crear usuarios**: 
   - Acceder como admin
   - Crear técnicos adicionales

2. **Registrar impresoras**: 
   - Datos de todas las impresoras de la empresa

3. **Automatizar lecturas**: 
   - Registrar contadores regularmente
   - Generar reportes mensuales

4. **Monitorear alertas**: 
   - Revisar bajo stock
   - Planificar mantenimiento

5. **Análisis**: 
   - Usar datos para optimizar consumo
   - Identificar tendencias

---

**¡Sistema Operativo y Listo!** 🚀
