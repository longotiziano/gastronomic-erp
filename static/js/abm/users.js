import { setupCrudModal } from './crud.js'

// campos del formulario que se van a rellenar
const fields = {
    username: 'name',
    email: 'email',
    address: 'address',
    rol: 'rol',
    leave_at: 'leave_at',
    daily_salary: 'daily_salary',
    bar_id: 'bar_id',
};

const createUrl = '/users/create';
const updateUrlBase = '/users/update';
const toggleUrlBase = '/users/alt_status';

setupCrudModal(fields, createUrl, updateUrlBase, toggleUrlBase);