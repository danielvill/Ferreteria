$(document).ready(function () {
    $('#myTable').DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.21/i18n/Spanish.json"
        }
    });
    var table = $('#myTable').DataTable();
    //Cambio de english a spanish
    // Funcionalidad de edición
    table.on('click', '.editar', function () {
        var row = $(this).closest('tr');
        var data = table.row(row).data();
        // Aquí puedes abrir el modal y llenar los campos del formulario con los datos del usuario
        // Por ejemplo:
        $('#cedula').val(data[0]);
        $('#user').val(data[1]);
        $('#correo').val(data[2]);
        $('#direccion').val(data[3]);
        $('#rol').val(data[4]);
        $('#editForm').attr('action','/edit_user/'+ data[0]); // Recuerda que en esta parte el 0 es la posicion selectora del codigo que estas usando en este caso es 0 ya que usas la cedula
        $('#editModal').dialog('open');
    });
    // Inicializar el modal
    $('#editModal').dialog({
        autoOpen: false,
        modal: true,
        buttons: [
            {
                text: 'Guardar',
                click: function () {
                    $('#editForm').submit();
                },
                // Agregar una clase al botón
                class: 'guardar'
            },
            {
                text: 'Cancelar',
                click: function () {
                    $(this).dialog('close');
                },
                // Agregar una clase al botón
                class: 'cancelar'
            }
        ]
    });
});


$(".eliminar").click(function (event) {
    event.preventDefault();
    var url = $(this).attr('href'); // Guarda la URL del enlace
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¿Estás seguro de que quieres eliminar?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar!',
        cancelButtonText: 'No, cancelar!'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url; // Navega a la URL del enlace
        }
    });
});

