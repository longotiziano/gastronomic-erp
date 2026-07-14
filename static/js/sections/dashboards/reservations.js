import { createLine, createBar, createPie, createHeatmap } from './charts.js';
import { initGroupByButtons, groupBy } from './groupby.js';

const canvasGraph1 = document.getElementById('graph1');

setTimeout(() => {
    createLine(canvasGraph1, data.by_period, 'fecha', 'cantidad', 'Reservas', 'Evolución de Reservas');

    initGroupByButtons((period) => {
        Chart.getChart(canvasGraph1)?.destroy(); 
        const dataAgrupada = groupBy(data.by_period, period, 'cantidad'); 
        createLine(canvasGraph1, dataAgrupada, 'fecha', 'cantidad', 'Reservas', 'Evolución de Reservas');
    });

    createPie(document.getElementById('graph2'), data.by_status, 'estado', 'cantidad', 'Estados', 'Estados de Reservas');
    createHeatmap(
        document.getElementById('graph3'), 
        data.heatmap, 
        'hora', 
        'dia', 
        'cantidad', 
        'Reservas', 
        'Distribución Horaria de Reservas'
    );
    createBar(document.getElementById('graph4'), data.by_weekday, 'dia', 'cantidad', 'Cantidad', 'Total por Día de Semana');
    
}, 100);