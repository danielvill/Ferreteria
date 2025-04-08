$(document).ready(function () {
    // Si ya existe una instancia de DataTables, la destruimos antes de inicializar
    if ($.fn.DataTable.isDataTable('#myTable')) {
        $('#myTable').DataTable().destroy();
    }

    $('#myTable').DataTable({
        "language": {
            "url": "/static/js/Spanish.json"
        },
        "pageLength": 2
    });
});

// $(document).ready(function () {
//     $('select').select2();
// });
// $('#myTable').DataTable({
//     "language": {
//         "url": "/static/js/Spanish.json"
//     },
//     "pageLength": 2
    
// });

// Validacion si los campos estan vacios
document.querySelector('form').onsubmit = function (e) {
    var inputs = this.querySelectorAll('input');
    var todosLlenos = true; // Asume que todos los campos están llenos

    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].value === '') {
            todosLlenos = false; // Si un campo está vacío, establece todosLlenos en falso
            break; // No necesitas verificar el resto de los campos, así que puedes salir del bucle
        }
    }

    if (!todosLlenos) {
        e.preventDefault(); // Previene el envío del formulario
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Campos estan vacios'
        });
    }
};

// Validacion para que no se envie si no hay la cantidad de productos suficiente 
document.querySelector('form').addEventListener('submit', function (e) {
    var c_producto = parseInt(document.querySelector('.c_producto').value);
    var cantidad = parseInt(document.querySelector('input[name="cantidad"]').value);

    if (cantidad > c_producto) {
        e.preventDefault();
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'No tienes esa cantidad de producto!'
        });
    }
});


// No permitir valores negativos ni el singo +
document.querySelector('input[name="cantidad"]').addEventListener('input', function (e) {
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


// Multiplicacion de productos con precio 

window.onload = function () {
    var precio = document.querySelector('.pvp');
    var cantidad = document.querySelector('.cantidad');
    var total = document.querySelector('.total');

    function calcularTotal() {
        total.value = Number(precio.value) * Number(cantidad.value);
    }
    precio.oninput = calcularTotal;
    cantidad.oninput = calcularTotal;
};

// Codigo para que no agrege punto ni coma
document.querySelector('#cantidad').addEventListener('input', function(e) {
    var value = this.value;
    var regex = /^\d+$/;

    if (!regex.test(value)) {
        e.preventDefault();
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Por favor, ingresa una cantidad validad. Solo se permiten números enteros.'
        });
        this.value = value.substr(0, value.length - 1);
    }
});