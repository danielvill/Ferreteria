// Codigo para colocar automaticamente la fecha 

var fecha = document.querySelector('#fecha');
var hoy = new Date();

var dia = String(hoy.getDate()).padStart(2, '0');
var mes = String(hoy.getMonth() + 1).padStart(2, '0'); // Los meses en JavaScript empiezan en 0
var ano = hoy.getFullYear();

fecha.value = ano + '-' + mes + '-' + dia;