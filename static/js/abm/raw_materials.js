import { setupCrudModal } from './crud.js';

const fields = {
    name: 'name',
    category_id: 'category_id',
};

const createUrl = '/raw-materials/create';
const updateUrlBase = '/raw-materials/update';
const toggleUrlBase = '/raw-materials/alt_status';

setupCrudModal(fields, createUrl, updateUrlBase, toggleUrlBase);
