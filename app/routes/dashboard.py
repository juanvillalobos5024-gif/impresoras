"""
Rutas del Dashboard
"""
from flask import Blueprint, render_template
from app.routes.auth import login_required
from app.models.impresora import Impresora
from app.models.contador import Contador
from app.models.toner import Toner
from app.models.producto import Producto
from app.models.movimiento import Movimiento

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    """Dashboard principal"""
    # Estadísticas de impresoras
    stats_impresoras = Impresora.obtener_estadisticas()
    
    # Estadísticas de contadores
    stats_contadores = Contador.obtener_estadisticas_mes()
    
    # Top impresoras
    top_impresoras = Contador.obtener_top_impresoras()
    
    # Estadísticas de tóners
    stats_toners = Toner.obtener_estadisticas()
    
    # Productos con bajo stock
    bajo_stock = Producto.obtener_bajo_stock()
    
    # Últimos movimientos
    ultimos_movimientos = Movimiento.obtener_ultimos(5)
    
    # Datos para gráficas
    grafica_impresiones = Contador.obtener_grafica_mensual()
    grafica_movimientos = Movimiento.obtener_grafica_mensual()
    
    # Estadísticas de productos
    stats_productos = Producto.obtener_estadisticas()
    
    return render_template('dashboard/index.html',
                         stats_impresoras=stats_impresoras,
                         stats_contadores=stats_contadores,
                         top_impresoras=top_impresoras,
                         stats_toners=stats_toners,
                         bajo_stock=bajo_stock,
                         ultimos_movimientos=ultimos_movimientos,
                         grafica_impresiones=grafica_impresiones,
                         grafica_movimientos=grafica_movimientos,
                         stats_productos=stats_productos)
