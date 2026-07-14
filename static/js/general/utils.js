// parsea de "Tue, 01 Dec 2026 20:00:00 GMT" a fecha y hora separados
export const parseDateTime = (dateString) => {
    const date = new Date(dateString);

    const fecha = date.toISOString().split('T')[0];
    const hora = date.getUTCHours();

    return { fecha, hora };
};