// Revenue Stats Chart
const ctx = document.getElementById('revenueChart').getContext('2d');

// Extraer los datos de la tabla
const table = document.querySelector('.table');
const rows = table.querySelectorAll('tbody tr');

// Arrays para almacenar los nombres de productos y cantidades
const productNames = [];
const quantities = [];

// Recorrer las filas de la tabla y extraer los datos
rows.forEach(row => {
    const productName = row.querySelector('td:first-child').textContent.trim();
    const quantity = parseInt(row.querySelector('td:last-child').textContent.trim(), 10);

    productNames.push(productName);
    quantities.push(quantity);
});
const revenueCtx = document.getElementById('revenueChart').getContext('2d');
const revenueChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: productNames,
        datasets: [{
            label: 'Cantidad de productos',
            data: quantities,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 2,
            tension: 0.3,
            pointBackgroundColor: 'rgba(54, 162, 235, 1)',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 5,
            pointHoverRadius: 7
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    drawBorder: false,
                    color: 'rgba(0, 0, 0, 0.05)'
                },
                ticks: {
                    callback: function (value) {
                        return value;
                    }
                }
            },
            x: {
                grid: {
                    display: false
                }
            }
        },
        plugins: {
            legend: {
                display: false
            }
        }
    }
});

// Sales by Category Chart

// Obtener todas las filas de la tabla
const filas = document.querySelectorAll("#ventas tbody tr");
// Objeto para almacenar los totales por mes
const totalesPorMes = {};
// Iterar por las filas de la tabla
filas.forEach((fila) => {
    const fechaTD = fila.querySelector("td:nth-child(1)").textContent; // La fecha
    const totalTD = parseInt(fila.querySelector("td:nth-child(2)").textContent); // El total
    const fecha = new Date(fechaTD); // Convertir a objeto Date
    const mes = fecha.toLocaleString("es-ES", { month: "long" }); // Nombre del mes en español
    // Sumar el total al mes correspondiente
    if (totalesPorMes[mes]) {
        totalesPorMes[mes] += totalTD;
    } else {
        totalesPorMes[mes] = totalTD;
    }
});

// Crear una nueva tabla con los resultados
const nuevaTabla = document.createElement("table");
nuevaTabla.classList.add("table");
nuevaTabla.id = "ventas-por-mes";
nuevaTabla.style.display = "none";
nuevaTabla.innerHTML = `
<thead >
<tr>
    <th>Mes</th>
    <th>Total</th>
</tr>
</thead>
<tbody>
${Object.entries(totalesPorMes)
        .map(
            ([mes, total]) => `
        <tr>
            <td>${mes.charAt(0).toUpperCase() + mes.slice(1)}</td>
            <td>${total}</td>
        </tr>
    `
        )
        .join("")}
</tbody>
`;

// Reemplazar la tabla antigua con la nueva
const tablaAntigua = document.querySelector("#ventas");
tablaAntigua.replaceWith(nuevaTabla);

// Encontrar el valor máximo y mínimo de ventas
let maxVenta = 0;
let minVenta = Infinity;
let mesMaxVenta = '';
let mesMinVenta = '';

Object.entries(totalesPorMes).forEach(([mes, total]) => {
    if (total > maxVenta) {
        maxVenta = total;
        mesMaxVenta = mes;
    }
    if (total < minVenta) {
        minVenta = total;
        mesMinVenta = mes;
    }
});

// Actualizar la información de mayor y menor venta
document.querySelector('.time-selector').textContent =
    `Mayor venta: ${mesMaxVenta.charAt(0).toUpperCase() + mesMaxVenta.slice(1)} (${maxVenta}) | Menor venta: ${mesMinVenta.charAt(0).toUpperCase() + mesMinVenta.slice(1)} (${minVenta})`;

// Crear el gráfico de doughnut
const ctx2 = document.getElementById('categoryChart').getContext('2d');

// Extraer los datos para el gráfico
const meses = Object.keys(totalesPorMes).map(mes => mes.charAt(0).toUpperCase() + mes.slice(1));
const totales = Object.values(totalesPorMes);

// Generar colores aleatorios para cada mes
const colores = meses.map(() => {
    const r = Math.floor(Math.random() * 200) + 55; // Evitar colores muy oscuros
    const g = Math.floor(Math.random() * 200) + 55;
    const b = Math.floor(Math.random() * 200) + 55;
    return `rgba(${r}, ${g}, ${b}, 0.7)`;
});

// Configurar el gráfico
const myChart = new Chart(ctx2, {
    type: 'doughnut',
    data: {
        labels: meses,
        datasets: [{
            data: totales,
            backgroundColor: colores,
            borderColor: colores.map(color => color.replace('0.7', '1')),
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Ventas por Mes'
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        const label = context.label || '';
                        const value = context.raw || 0;
                        const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                        const percentage = Math.round((value / total) * 100);
                        return `${label}: ${value} (${percentage}%)`;
                    }
                }
            }
        },
        cutout: '60%'
    }
});
