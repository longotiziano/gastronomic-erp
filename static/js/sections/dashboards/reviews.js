import { createLine, createBar } from './charts.js';
import { initGroupByButtons, groupBy } from './groupby.js';

const canvasGraph1 = document.getElementById('graph1');

setTimeout(() => {
    createLine(canvasGraph1, data.average_evolution, 'fecha', 'promedio', 'Promedio de estrellas', 'Evolución de Calificaciones');

    initGroupByButtons((period) => {
        Chart.getChart(canvasGraph1)?.destroy(); 
        const dataAgrupada = groupBy(data.average_evolution, period, 'promedio', 'avg'); 
        createLine(canvasGraph1, dataAgrupada, 'fecha', 'promedio', 'Promedio de estrellas', 'Evolución de Calificaciones');
    });

    createBar(document.getElementById('graph2'), data.stars_distribution, 'stars', 'cantidad', 'Opiniones', 'Distribución de Estrellas');

    createLine(document.getElementById('graph3'), data.count_by_period, 'fecha', 'cantidad', 'Reseñas', 'Cantidad de Reseñas por Período');
}, 100);