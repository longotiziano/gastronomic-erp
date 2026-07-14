function getTitleConfig(titleText) {
    if (!titleText) return { display: false };
    return {
        display: true,
        text: titleText,
        color: '#ffffff',
        font: { size: 16, weight: 'bold', family: 'sans-serif' },
        padding: { top: 10, bottom: 15 }
    };
}

function getZoomConfig() {
    return {
        zoom: {
            wheel: { enabled: true, speed: 0.1 },
            pinch: { enabled: true },
            mode: 'x',
        },
        pan: {
            enabled: true,
            mode: 'x',
        }
    };
}

const hideXGrid = { x: { grid: { display: false } } };

export function createLine(canvas, data, xKey, yKey, label, titleText) {
    return new Chart(canvas, {
        type: 'line',
        data: {
            labels: data.map(d => d[xKey]),
            datasets: [{
                label: label,
                data: data.map(d => d[yKey]),
                fill: true,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                tension: 0.4,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: getTitleConfig(titleText),
                zoom: getZoomConfig()
            },
            scales: hideXGrid
        }
    });
}

export function createBar(ctx, data, x, y, label, titleText) {
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d[x]),
            datasets: [{
                label,
                data: data.map(d => d[y]),
                borderRadius: 4,
                backgroundColor: 'rgba(54, 162, 235, 0.8)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { 
                legend: { position: 'top' },
                title: getTitleConfig(titleText),
                zoom: getZoomConfig()
            },
            scales: hideXGrid
        }
    });
}

export function createPie(ctx, data, x, y, label, titleText) {
    return new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.map(d => d[x]),
            datasets: [{
                label,
                data: data.map(d => d[y]),
                hoverOffset: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { 
                legend: { position: 'right', labels: { color: '#ffffff' } },
                title: getTitleConfig(titleText)
            }
        }
    });
}

export function createHeatmap(ctx, data, xKey, yKey, valueKey, label, titleText) {
    const dias = ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab'];

    const maxValue = data.length > 0 ? Math.max(...data.map(d => d[valueKey])) : 1;

    return new Chart(ctx, {
        type: 'matrix',
        data: {
            datasets: [{
                label: label, 
                data: data.map(d => ({
                    x: d[xKey],    
                    y: d[yKey],    
                    v: d[valueKey]  
                })),
                width: ({ chart }) => chart.chartArea ? (chart.chartArea.width / 24) - 2 : 10,
                height: ({ chart }) => chart.chartArea ? (chart.chartArea.height / 7) - 2 : 20,
                
                backgroundColor(context) {
                    const value = context.dataset.data[context.dataIndex]?.v || 0;
                    if (value === 0) return 'rgba(0, 0, 0, 0.1)';
                    const alfa = value / maxValue;
                    return `rgba(54, 162, 235, ${Math.max(alfa, 0.2)})`;
                },
                borderColor: 'rgba(255, 255, 255, 0.05)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: getTitleConfig(titleText),
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        title: () => label,
                        label: (context) => {
                            const v = context.raw;
                            return ` ${dias[v.y - 1]} a las ${v.x}:00 hs: ${v.v} (${label.toLowerCase()})`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    type: 'linear', min: -0.5, max: 23.5,
                    ticks: { stepSize: 1, callback: (v) => v >= 0 && v <= 23 ? `${v}h` : '' },
                    grid: { display: false }
                },
                y: {
                    type: 'linear', min: 0.5, max: 7.5,
                    ticks: { stepSize: 1, callback: (v) => dias[v - 1] || '' },
                    grid: { display: false }
                }
            }
        }
    });
}