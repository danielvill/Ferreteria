$(document).ready(function () {
    // Inicialización de DataTables
    if ($.fn.DataTable.isDataTable('#myTable')) {
        $('#myTable').DataTable().destroy();
    }

    $('#myTable').DataTable({
        "language": {
            "url": "/static/js/Spanish.json"
        },
        "pageLength": 10 // Muestra 10 filas por página
    });
});