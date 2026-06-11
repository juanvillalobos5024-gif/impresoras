"""
Rutas del Módulo de Contadores de Impresiones
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.routes.auth import login_required
from app.models.contador import Contador
from app.models.impresora import Impresora
from app.models.usuario import Usuario
from datetime import datetime
import http.client
import re

contadores_bp = Blueprint('contadores', __name__, url_prefix='/contadores')

@contadores_bp.route('/')
@login_required
def listar():
    """Listar todos los contadores"""
    impresoras = Impresora.obtener_todas()
    
    # Filtrar por impresora si se proporciona
    impresora_id = request.args.get('impresora_id')
    
    if impresora_id:
        contadores = Contador.obtener_por_impresora(int(impresora_id))
        impresora_seleccionada = Impresora.obtener_por_id(int(impresora_id))
    else:
        contadores = Contador.obtener_todos()
        impresora_seleccionada = None
    
    return render_template('contadores/listar.html',
                         contadores=contadores,
                         impresoras=impresoras,
                         impresora_seleccionada=impresora_seleccionada)

def extraer_contador_de_texto(texto):
    """Busca el número de contador más probable dentro de un texto."""
    # Buscar valores explícitos relacionados con el total de impresiones
    patrones = [
        r'(?i)(?:total\s*(?:de\s*)?(?:impresiones|impresiones equivalentes|paginas|páginas|pages)|contador\s*actual|page\s*count|print\s*count)\s*[:\-]?\s*([\d.,]+)',
        r'(?i)(?:paginas\s*impresas|páginas\s*impresas|print\s*pages|printed\s*pages)\s*[:\-]?\s*([\d.,]+)',
        r'(?i)(?:Total\s+de\s+impresiones|Impresiones\s+Totales|Total\s+de\s+pages|Total\s+de\s+impresiones\s+equivalentes)\s*[:\-]?\s*([\d.,]+)',
    ]
    for patron in patrones:
        encontrado = re.search(patron, texto)
        if encontrado:
            numero = re.sub(r'[^0-9]', '', encontrado.group(1) or '')
            if numero and int(numero) > 0:
                return int(numero)

    numeros = re.findall(r'\b\d{4,}\b', texto)
    if not numeros:
        return None
    try:
        return int(max(numeros, key=len))
    except ValueError:
        return None


def obtener_contador_por_ip(ip):
    """Intenta obtener el contador actual desde la impresora usando HTTP/HTTPS."""
    ip = ip.strip()
    if ip.startswith('http://') or ip.startswith('https://'):
        ip_limpia = ip
    else:
        ip_limpia = f'http://{ip}'

    rutas_comunes = [
        '/',
        '/index.html',
        '/hp/device/Index.html',
        '/hp/device/Status.html',
        '/hp/device/Info.html',
        '/hp/device/Printer/Printer.html',
        '/printerstatus.html',
        '/hp/device/soap/Printer',
        '/hp/smf?path=Security',
    ]

    esquemas = ['http', 'https'] if not ip.startswith(('http://', 'https://')) else [ip.split(':', 1)[0]]

    for esquema in esquemas:
        base = ip_limpia if ip_limpia.startswith(esquema) else f'{esquema}://{re.sub(r"^https?://", "", ip_limpia)}'
        for ruta in rutas_comunes:
            url = base.rstrip('/') + ruta
            try:
                parsed = re.match(r'^(https?)://([^:/]+)(?::(\d+))?(.*)$', url)
                if not parsed:
                    continue
                scheme, host, port, path = parsed.groups()
                port = int(port) if port else (443 if scheme == 'https' else 80)
                conn = http.client.HTTPSConnection(host, port, timeout=6) if scheme == 'https' else http.client.HTTPConnection(host, port, timeout=6)
                conn.request('GET', path or '/')
                resp = conn.getresponse()
                if resp.status == 200:
                    body = resp.read(32768).decode('utf-8', errors='ignore')
                    contador = extraer_contador_de_texto(body)
                    if contador is not None:
                        return contador
            except Exception:
                pass
            finally:
                try:
                    conn.close()
                except Exception:
                    pass
    return None


@contadores_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """Crear un nuevo registro de contador"""
    impresoras = Impresora.obtener_todas()
    
    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            datos['contador_anterior'] = int(datos['contador_anterior'])
            datos['contador_actual'] = int(datos['contador_actual'])
            datos['tecnico_id'] = session.get('usuario_id')
            
            contador_id = Contador.crear(datos)
            flash('Registro de contador creado exitosamente.', 'success')
            
            impresora_id = datos.get('impresora_id')
            return redirect(url_for('impresoras.detalle', id=impresora_id))
        except Exception as e:
            flash(f'Error al crear el registro: {str(e)}', 'danger')
    
    return render_template('contadores/crear.html', impresoras=impresoras)


@contadores_bp.route('/actualizar-por-ip', methods=['GET', 'POST'])
@login_required
def actualizar_por_ip():
    """Actualiza contadores usando IPs de impresoras."""
    impresoras = Impresora.obtener_todas()
    resultados = []
    errores = []

    if request.method == 'POST':
        datos = request.form.to_dict()
        lineas = [line.strip() for line in datos.get('ips', '').splitlines() if line.strip()]
        tecnico_id = session.get('usuario_id')

        for linea in lineas:
            partes = [parte.strip() for parte in linea.split(',')]
            if not partes:
                continue

            ip = partes[0]
            ip_limpia = re.sub(r'^https?://', '', ip).rstrip('/').rstrip(':').strip()
            contador_actual = None
            if len(partes) > 1 and partes[1]:
                try:
                    contador_actual = int(re.sub(r'[^0-9]', '', partes[1]))
                except ValueError:
                    contador_actual = None

            impresora = Impresora.obtener_por_ip(ip_limpia)
            if not impresora:
                errores.append(f'IP {ip}: no existe impresora registrada con esa dirección IP.')
                continue

            ultimo = Contador.obtener_ultimo_contador(impresora['id'])

            if contador_actual is None:
                contador_actual = obtener_contador_por_ip(ip_limpia)
                if contador_actual is None:
                    errores.append(f'IP {ip}: no se pudo obtener el contador desde la impresora. Verifique si la impresora es accesible por HTTP y si muestra el total de páginas impresas.')
                    continue
                if contador_actual == 0:
                    contador_actual = None
                    errores.append(f'IP {ip}: el valor leído es inválido (0). Verifique el acceso HTTP y el contenido de la página de la impresora.')
                    continue

            contador_anterior = ultimo['contador_actual'] if ultimo else 0

            if contador_actual < contador_anterior:
                errores.append(f'IP {ip}: el contador actual ({contador_actual}) es menor que el anterior ({contador_anterior}).')
                continue

            try:
                datos_contador = {
                    'impresora_id': impresora['id'],
                    'fecha': datetime.now().strftime('%Y-%m-%d'),
                    'contador_anterior': contador_anterior,
                    'contador_actual': contador_actual,
                    'tecnico_id': tecnico_id,
                    'observaciones': f'Actualizado por IP {ip}'
                }
                Contador.crear(datos_contador)
                resultados.append(f'IP {ip}: contador actualizado a {contador_actual}.')
            except Exception as e:
                errores.append(f'IP {ip}: error al guardar el contador ({str(e)}).')

    return render_template('contadores/actualizar_por_ip.html', impresoras=impresoras, resultados=resultados, errores=errores)


@contadores_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Editar un registro de contador"""
    conn = __import__('app.database.db', fromlist=['get_db_connection']).get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contadores WHERE id = ?', (id,))
    contador = cursor.fetchone()
    conn.close()
    
    if not contador:
        flash('Registro no encontrado.', 'danger')
        return redirect(url_for('contadores.listar'))
    
    contador = dict(contador)
    impresoras = Impresora.obtener_todas()
    
    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            datos['contador_anterior'] = int(datos['contador_anterior'])
            datos['contador_actual'] = int(datos['contador_actual'])
            
            Contador.actualizar(id, datos)
            flash('Registro actualizado exitosamente.', 'success')
            return redirect(url_for('impresoras.detalle', id=contador['impresora_id']))
        except Exception as e:
            flash(f'Error al actualizar el registro: {str(e)}', 'danger')
    
    return render_template('contadores/editar.html',
                         contador=contador,
                         impresoras=impresoras)

@contadores_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar(id):
    """Eliminar un registro de contador"""
    conn = __import__('app.database.db', fromlist=['get_db_connection']).get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT impresora_id FROM contadores WHERE id = ?', (id,))
    result = cursor.fetchone()
    conn.close()
    
    impresora_id = result['impresora_id'] if result else None
    
    try:
        Contador.eliminar(id)
        flash('Registro eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el registro: {str(e)}', 'danger')
    
    return redirect(url_for('impresoras.detalle', id=impresora_id)) if impresora_id \
           else redirect(url_for('contadores.listar'))

@contadores_bp.route('/api/grafica-mensual')
@login_required
def api_grafica_mensual():
    """API para obtener datos de gráfica mensual"""
    impresora_id = request.args.get('impresora_id')
    
    if impresora_id:
        datos = Contador.obtener_grafica_mensual(int(impresora_id))
    else:
        datos = Contador.obtener_grafica_mensual()
    
    return jsonify(datos)

@contadores_bp.route('/api/obtener-ultimo/<int:impresora_id>')
@login_required
def api_obtener_ultimo(impresora_id):
    """API para obtener el último contador de una impresora"""
    ultimo = Contador.obtener_ultimo_contador(impresora_id)
    
    if ultimo:
        return jsonify(ultimo)
    
    return jsonify(None)
