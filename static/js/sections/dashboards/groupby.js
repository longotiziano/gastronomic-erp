/*
* Agrupa los registros recibidos de manera diaria, mensual o anual
*/
export function groupBy(data, campo, yKey = 'cantidad', operation = 'sum') {
    const grouped = {};

    data.forEach(d => {
        let key;

        if (campo === 'daily') {
            key = d.fecha.slice(0, 10);
        } else if (campo === 'monthly') {
            key = d.fecha.slice(0, 7);
        } else if (campo === 'yearly') {
            key = d.fecha.slice(0, 4);
        }

        if (!key) return;

        if (!grouped[key]) {
            grouped[key] = {
                total: 0,
                count: 0
            };
        }

        grouped[key].total += Number(d[yKey] || 0);
        grouped[key].count++;
    });

    return Object.keys(grouped).map(key => ({
        fecha: key,
        [yKey]:
            operation === 'avg'
                ? grouped[key].total / grouped[key].count
                : grouped[key].total
    }));
}

export function initGroupByButtons(callback) {
    const buttons = document.querySelectorAll('[data-graphdate]');
    
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            callback(btn.dataset.graphdate);
        });
    });
}