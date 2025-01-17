$(document).ready(function () {
    $('#myTable').DataTable({
    
    });
    var table = $('#myTable').DataTable();
    //Cambio de english a spanish
    // Funcionalidad de edición
    table.on('click', '.editar', function () {
        var row = $(this).closest('tr');
        var data = table.row(row).data();
        // Aquí puedes abrir el modal y llenar los campos del formulario con los datos del usuario
        // Por ejemplo:
        $('#id_producto').val(data[0]);
        $('#n_producto').val(data[1]);
        $('#descripcion').val(data[2]);
        $('#cantidad').val(data[3]);
        $('#categoria').val(data[4]);
        $('#marca').val(data[5]);
        $('#color').val(data[6]);
        $('#medida').val(data[7]);
        $('#cv').val(data[8]);
        $('#pvp').val(data[9]);
        $('#editForm').attr('action','/edit_pr/'+ data[0]); // Recuerda que en esta parte el 0 es la posicion selectora del codigo que estas usando en este caso es 0 ya que usas la cedula
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


// No permitir valores negativos ni el singo +
document.querySelector('input[name="cantidad"]').addEventListener('input', function(e) {
    if (this.value < 0 || this.value.includes('+')) {
        e.preventDefault();
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'No se permiten valores negativos!'
        });
        this.value = '';
    }
});

// que permita agregar punto en vez de coma al precio de productos
document.querySelector('#pvp').addEventListener('input', function(e) {
    var value = this.value;
    var regex = /^\d*\.?\d*$/;

    if (!regex.test(value)) {
        e.preventDefault();
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Por favor, ingresa un número válido. Solo se permiten números y un punto decimal.'
        });
        this.value = value.substr(0, value.length - 1);
    }
});

// que permita agregar punto en vez de coma al precio de productos
document.querySelector('#medida').addEventListener('input', function(e) {
    var value = this.value;
    var regex = /^\d*\.?\d*$/;

    if (!regex.test(value)) {
        e.preventDefault();
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Por favor, ingresa un número válido. Solo se permiten números y un punto decimal.'
        });
        this.value = value.substr(0, value.length - 1);
    }
});