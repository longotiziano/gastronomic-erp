import { setupCrudModal } from './crud.js'

console.log("¡¡EL ARCHIVO DE RESERVACIONES CARGÓ CON ÉXITO!!");

// {<input id>: <clave del dataset que da el valor de cada columna>}
const fields = {
        table_display: 'table_number',
        fecha: 'fecha',
        hora: 'hora',
        people_amount: 'people_amount',
        user_email: 'user_email',
        status_reservation: 'status_reservation'
    };
const createUrl = null;
const updateUrlBase = '/admin/reservations/update';
const toggleUrlBase = null;
const idKey = 'id';

setupCrudModal(fields, createUrl, updateUrlBase, toggleUrlBase);