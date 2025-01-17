 // Para validar el bajo stock si es que tiene la mercaderia utilizando lo que es paginacion demora pero funciona para lo que es el punto 
// $(document).ready(function() {
//    // Suponiendo que #myTable es el ID de tu tabla

$(document).ready(function() {
    // Suponiendo que #myTable es el ID de tu tabla
    $('#myTable').on('draw.dt', function() {
        var cantidades = document.querySelectorAll('td.cantidad');
        var mensajes = document.querySelectorAll('.mostrar');
        var umbralBajoStock = parseInt(document.getElementById('b_stock').value);

        for (var i = 0; i < cantidades.length; i++) {
            if (parseInt(cantidades[i].textContent) < umbralBajoStock) {
                mensajes[i].style.display = 'block';
                mensajes[i].style.color = 'red';
                mensajes[i].textContent = 'bajo stock';
            } else {
                mensajes[i].style.display = 'none';
            }
        }
    });
});




    // Ocultar la tabla existente
    var tablaExistente = document.getElementById('myTable5');
    tablaExistente.style.display = 'none';

    // Código para crear la tabla con el valor total de ventas por usuario por mes
    var fechas = document.querySelectorAll('#myTable5 td:nth-child(1)');
    var usuarios = document.querySelectorAll('#myTable5 td:nth-child(3)');
    var valores = document.querySelectorAll('#myTable5 td:nth-child(2)');
    var datosPorUsuarioPorMes = {};

    for (var i = 0; i < fechas.length; i++) {
        var fecha = new Date(fechas[i].textContent);
        var mes = fecha.getFullYear() + '-' + ('0' + (fecha.getMonth() + 1)).slice(-2);
        var usuario = usuarios[i].textContent;

        if (!datosPorUsuarioPorMes[usuario]) {
            datosPorUsuarioPorMes[usuario] = {};
        }

        if (!datosPorUsuarioPorMes[usuario][mes]) {
            datosPorUsuarioPorMes[usuario][mes] = 0;
        }

        datosPorUsuarioPorMes[usuario][mes] += parseFloat(valores[i].textContent);
    }

    var tabla = document.createElement('table');
    tabla.id = 'myTable6'; // Agregar un id para aplicar DataTables
    tabla.className = 'table table-striped table-bordered table-hover'; // Agregar las clases
    var thead = document.createElement('thead');
    var tbody = document.createElement('tbody');
    var encabezado = document.createElement('tr');
    encabezado.innerHTML = '<th>Mes</th><th>Usuario</th><th>Total</th>';
    thead.appendChild(encabezado);
    tabla.appendChild(thead);

    var meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

    for (var usuario in datosPorUsuarioPorMes) {
        for (var mes in datosPorUsuarioPorMes[usuario]) {
            var fila = document.createElement('tr');
            var mesNombre = meses[parseInt(mes.split('-')[1]) - 1] + ' ' + mes.split('-')[0];
            fila.innerHTML = '<td>' + mesNombre + '</td><td>' + usuario + '</td><td>' + datosPorUsuarioPorMes[usuario][mes].toFixed(2) + '</td>';
            tbody.appendChild(fila);
        }
    }

    tabla.appendChild(tbody);
    tablaExistente.parentNode.appendChild(tabla);

    // Inicializar DataTables
    $('#myTable6').DataTable();

