/**
 * JavaScript Principal - Sistema de Control de Impresoras TI
 */

// Inicialización al cargar el DOM
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    initTooltips();
    
    // Inicializar eventos de confirmación
    initConfirmButtons();
    
    // Ocultar alertas después de 5 segundos
    autoHideAlerts();
});

/**
 * Inicializa tooltips de Bootstrap
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Inicializa botones de confirmación
 */
function initConfirmButtons() {
    const forms = document.querySelectorAll('form[onsubmit*="confirm"]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('¿Estás seguro de que deseas continuar?')) {
                e.preventDefault();
            }
        });
    });
}

/**
 * Oculta alertas después de 5 segundos
 */
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Muestra un spinner de carga
 */
function showLoading(element) {
    element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Cargando...';
    element.disabled = true;
}

/**
 * Restaura un elemento del estado de carga
 */
function hideLoading(element, text) {
    element.innerHTML = text;
    element.disabled = false;
}

/**
 * Formatea un número como moneda
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 2
    }).format(value);
}

/**
 * Formatea un número con separadores de miles
 */
function formatNumber(value) {
    return new Intl.NumberFormat('es-CO').format(value);
}

/**
 * Valida un formulario
 */
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
    }
    form.classList.add('was-validated');
}

/**
 * Muestra una notificación toast
 */
function showToast(message, type = 'info') {
    const toastHtml = `
        <div class="toast show" role="alert">
            <div class="toast-header bg-${type} text-white">
                <strong class="me-auto">${type.toUpperCase()}</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.innerHTML = toastHtml;
    document.body.appendChild(container);
    
    setTimeout(() => {
        container.remove();
    }, 5000);
}

/**
 * Realiza una petición AJAX GET
 */
async function ajaxGet(url) {
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error en petición GET:', error);
        showToast('Error al cargar los datos', 'danger');
        throw error;
    }
}

/**
 * Realiza una petición AJAX POST
 */
async function ajaxPost(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error en petición POST:', error);
        showToast('Error al enviar los datos', 'danger');
        throw error;
    }
}

/**
 * Copia texto al portapapeles
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copiado al portapapeles', 'success');
    }).catch(err => {
        console.error('Error al copiar:', err);
    });
}

/**
 * Exporta una tabla a CSV
 */
function exportTableToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    let csv = [];
    
    // Obtener encabezados
    const headers = [];
    table.querySelectorAll('th').forEach(th => {
        headers.push('"' + th.textContent.trim() + '"');
    });
    csv.push(headers.join(','));
    
    // Obtener filas
    table.querySelectorAll('tbody tr').forEach(tr => {
        const row = [];
        tr.querySelectorAll('td').forEach(td => {
            row.push('"' + td.textContent.trim().replace(/"/g, '""') + '"');
        });
        csv.push(row.join(','));
    });
    
    // Descargar
    downloadCSV(csv.join('\n'), filename);
}

/**
 * Descarga un archivo CSV
 */
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], {type: "text/csv;charset=utf-8;"});
    const link = document.createElement("a");
    link.href = URL.createObjectURL(csvFile);
    link.download = filename;
    link.click();
}

/**
 * Carga dinámica de datos en un select
 */
async function loadSelectOptions(selectId, url) {
    try {
        const select = document.getElementById(selectId);
        showLoading(select);
        
        const data = await ajaxGet(url);
        select.innerHTML = '';
        
        data.forEach(option => {
            const opt = document.createElement('option');
            opt.value = option.id;
            opt.text = option.nombre || option.name;
            select.appendChild(opt);
        });
        
        hideLoading(select, 'Cargar...');
    } catch (error) {
        console.error('Error cargando opciones:', error);
    }
}

/**
 * Filtra una tabla en tiempo real
 */
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    input.addEventListener('keyup', function() {
        const filter = input.value.toUpperCase();
        const rows = table.getElementsByTagName('tr');
        
        for (let i = 1; i < rows.length; i++) {
            const cells = rows[i].getElementsByTagName('td');
            let found = false;
            
            for (let j = 0; j < cells.length; j++) {
                if (cells[j].textContent.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
            
            rows[i].style.display = found ? '' : 'none';
        }
    });
}

/**
 * Imprime una página
 */
function printPage() {
    window.print();
}

/**
 * Redirige a una URL
 */
function redirect(url) {
    window.location.href = url;
}

/**
 * Verifica si un campo está vacío
 */
function isEmpty(value) {
    return value === null || value === undefined || value.trim() === '';
}

/**
 * Valida un email
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Convierte un string a slug
 */
function toSlug(str) {
    return str
        .toLowerCase()
        .trim()
        .replace(/[^\w\s-]/g, '')
        .replace(/[\s_]+/g, '-')
        .replace(/^-+|-+$/g, '');
}

/**
 * Obtiene un parámetro de URL
 */
function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    const results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

// Exportar funciones globales (si se usa como módulo)
window.appUtils = {
    showLoading,
    hideLoading,
    formatCurrency,
    formatNumber,
    validateForm,
    showToast,
    ajaxGet,
    ajaxPost,
    copyToClipboard,
    exportTableToCSV,
    loadSelectOptions,
    filterTable,
    printPage,
    redirect,
    isEmpty,
    validateEmail,
    toSlug,
    getUrlParameter
};
