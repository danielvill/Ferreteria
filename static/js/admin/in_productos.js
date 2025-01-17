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

// No permitir valores negativos ni el singo +
document.querySelector('input[name="cantidad"]').addEventListener('input', function(e) {
    if (this.value < 0 || this.value.includes('+') || this.value.includes('.')) {
        e.preventDefault();
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: '¡Solo valores enteros!'
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
//document.querySelector('#medida').addEventListener('input', function(e) {
//    var value = this.value;
//    var regex = /^\d*\.?\d*$/;
//
//    if (!regex.test(value)) {
//        e.preventDefault();
//        Swal.fire({
//            icon: 'error',
//            title: 'Oops...',
//            text: 'Por favor, ingresa un número válido. Solo se permiten números y un punto decimal.'
//        });
//        this.value = value.substr(0, value.length - 1);
//    }
//});
