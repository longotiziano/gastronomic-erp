import { setupCrudModal } from './crud.js';

const fields = {
    name: 'name',
    address: 'address',
};

const createUrl = '/bars/create';
const updateUrlBase = '/bars/update';
const toggleUrlBase = '/bars/alt_status';

setupCrudModal(fields, createUrl, updateUrlBase, toggleUrlBase);
