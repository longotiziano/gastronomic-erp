import { setupCrudModal } from './crud.js'
console.log("¡¡EL ARCHIVO DE MENUS CARGÓ CON ÉXITO!!");

const fields = {
        name: 'name',
        category: 'category',
        description: 'description',
        price: 'price',
        available: 'available',
        image_url: 'image_url'
    };
const createUrl = '/admin/menus/create';
const updateUrlBase = '/admin/menus/update';
const toggleUrlBase = '/admin/menus/toggle_status';

setupCrudModal(fields, createUrl, updateUrlBase, toggleUrlBase);