import { setupCrudModal } from './crud.js'

// Campos del formulario que se van a rellenar
const fields = {
    number: 'number',
    capacity: 'capacity'
};

const createUrl = '/admin/tables/create';
const updateUrlBase = '/admin/tables/update';
const toggleUrlBase = '/admin/tables/toggle_status';

setupCrudModal(fields, createUrl, updateUrlBase, toggleUrlBase);
