$('#myTable').DataTable({
    
});
var table = $('#myTable').DataTable();
// Codigo para mostrar faltantes de productos
window.onload = function () {
    // Multiplicacio del apartado de productos 
    var cantidades = document.querySelectorAll('.valor1');
    var precios = document.querySelectorAll('.valor2');
    var totales = document.querySelectorAll('.total');

    for (var i = 0; i < cantidades.length; i++) {
        var total = parseInt(cantidades[i].textContent) * parseFloat(precios[i].textContent);
        totales[i].textContent = total.toFixed(2);
    }

    // Ocultar la tabla existente codigo para visualizar las ventas mensuales 
    var tablaExistente = document.getElementById('myTable2');
    tablaExistente.style.display = 'none';
    // Código para crear la tabla con el valor total de meses
    var fechas = document.querySelectorAll('#myTable2 td:nth-child(1)');
    var totales = document.querySelectorAll('#myTable2 .total');
    var datosPorMes = {};

    for (var i = 0; i < fechas.length; i++) {
        var fecha = new Date(fechas[i].textContent);
        var mes = fecha.getFullYear() + '-' + ('0' + (fecha.getMonth() + 1)).slice(-2);

        if (!datosPorMes[mes]) {
            datosPorMes[mes] = 0;
        }

        datosPorMes[mes] += parseFloat(totales[i].textContent);
    }

    var tabla = document.createElement('table');
    tabla.id = 'myTable3'; // Agregar un id para aplicar DataTables
    tabla.className = 'table table-striped table-bordered table-hover'; // Agregar las clases
    var thead = document.createElement('thead');
    var tbody = document.createElement('tbody');
    var encabezado = document.createElement('tr');
    encabezado.innerHTML = '<th>Mes</th><th>Total</th>';
    thead.appendChild(encabezado);
    tabla.appendChild(thead);

    var meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

    for (var mes in datosPorMes) {
        var fila = document.createElement('tr');
        var mesNombre = meses[parseInt(mes.split('-')[1]) - 1] + ' ' + mes.split('-')[0];
        fila.innerHTML = '<td>' + mesNombre + '</td><td>' + datosPorMes[mes].toFixed(2) + '</td>';
        tbody.appendChild(fila);
    }

    tabla.appendChild(tbody);
    tablaExistente.parentNode.appendChild(tabla);

    // Inicializar DataTables
    $('#myTable3').DataTable();
    // * termina el codigo para que se visualice las ventas mensuales para la tabla 
    // * Empieza datos para lo que es inventario de tabla 
    // * Ocultar la tabla existente
}

