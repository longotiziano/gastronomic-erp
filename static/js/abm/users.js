import { setupCrudModal } from './crud.js'

// campos del formulario que se van a rellenar
const fields = {
    username: 'name',
    email: 'email',
    category: 'category'
};

const createUrl = '/admin/users/create';
const updateUrlBase = '/admin/users/update';
const toggleUrlBase = '/admin/users/toggle_status';

setupCrudModal(fields, createUrl, updateUrlBase, toggleUrlBase);