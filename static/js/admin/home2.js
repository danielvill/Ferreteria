// Codigo para ocultar la tabla para lo que es productos 
// Ocultar la tabla existente
var tablaExistente = document.getElementById('myTable3');
tablaExistente.style.display = 'none';

// Código para crear la tabla con el valor total de meses y productos
var fechas = document.querySelectorAll('#myTable3 .fecha');
var productos = document.querySelectorAll('#myTable3 .producto');
var salidas = document.querySelectorAll('#myTable3 .cantidad2');
var datosPorMesYProducto = {};

for (var i = 0; i < fechas.length; i++) {
    var fecha = new Date(fechas[i].textContent);
    var mes = fecha.getFullYear() + '-' + ('0' + (fecha.getMonth() + 1)).slice(-2);
    var producto = productos[i].textContent;

    var clave = mes + '-' + producto;

    if (!datosPorMesYProducto[clave]) {
        datosPorMesYProducto[clave] = 0;
    }

    datosPorMesYProducto[clave] += parseFloat(salidas[i].textContent);
}

var tabla = document.createElement('table');
tabla.id = 'myTable4'; // Agregar un id para aplicar DataTables
tabla.className = 'table table-striped table-bordered table-hover'; // Agregar las clases
var thead = document.createElement('thead');
var tbody = document.createElement('tbody');
var encabezado = document.createElement('tr');
encabezado.innerHTML = '<th>Mes</th><th>Producto</th><th>Total</th>';
thead.appendChild(encabezado);
tabla.appendChild(thead);

var meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

for (var clave in datosPorMesYProducto) {
    var fila = document.createElement('tr');
    var partes = clave.split('-');
    var mesNombre = meses[parseInt(partes[1]) - 1] + ' ' + partes[0];
    var producto = partes[2];
    fila.innerHTML = '<td>' + mesNombre + '</td><td>' + producto + '</td><td>' + datosPorMesYProducto[clave].toFixed(2) + '</td>';
    tbody.appendChild(fila);
}

tabla.appendChild(tbody);
tablaExistente.parentNode.insertBefore(tabla, tablaExistente);

// Inicializar DataTables
$('#myTable4').DataTable();
