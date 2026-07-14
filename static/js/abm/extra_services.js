import { setupCrudModal } from './crud.js'

const fields = {
    nombre: 'nombre',
    descripcion: 'descripcion',
    activo: 'activo'
};
const createUrl = '/admin/extra_services/create';
const updateUrlBase = '/admin/extra_services/update';
const toggleUrlBase = '/admin/extra_services/toggle_status';

setupCrudModal(fields, createUrl, updateUrlBase, toggleUrlBase);
