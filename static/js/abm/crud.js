import { parseDateTime } from "../general/utils.js";
console.log("¡¡EL ARCHIVO DE MENUS CARGÓ CON ÉXITO!!");
console.log("¡¡EL ARCHIVO DE MENUS CARGÓ CON ÉXITO!!");
console.log("¡¡EL ARCHIVO DE MENUS CARGÓ CON ÉXITO!!");
const fillForm = (fields, data, idKey, form, deleteForm, createUrl, updateUrlBase, toggleUrlBase) => {
    Object.entries(fields).forEach(([fieldId, dataKey]) => {
        const input = document.getElementById(fieldId);
        if (!input) return;

        if (input.type === 'checkbox') {
            // chequeo medio raro por formateo
            input.checked = data[dataKey] === true || data[dataKey] === 'true' || data[dataKey] === '1';
        } else {
            input.value = data[dataKey] || '';
        }
    });

    const id = data[idKey];
    if (id) {
        form.action = `${updateUrlBase}/${id}`;
        if (deleteForm) deleteForm.action = `${toggleUrlBase}/${id}`;
    }
};

export const setupCrudModal = (fields, createUrl, updateUrlBase, toggleUrlBase, idKey = 'id') => {
    const modal = document.querySelector('[data-openby="formOpener"]');
    const overlay = document.querySelector('.overlay');
    const form = document.getElementById('form-principal');
    const deleteForm = document.getElementById('formDelete');
    const addBtn = document.getElementById('add-btn');
    const submitBtn = document.querySelector('.submit-btn[type="submit"]');
    const deleteBtn = document.querySelector('.delete-btn');
    const title = modal.querySelector('.block-header h2');

    const openModal = () => { modal.classList.add('open'); overlay.classList.add('active'); };
    const closeModal = () => { modal.classList.remove('open'); overlay.classList.remove('active'); };

    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            console.log('Entrando a Edit')
            if (deleteBtn) deleteBtn.hidden = false;
            submitBtn.textContent = 'Actualizar';
            if (title) title.textContent = 'Actualizar';
            fillForm(fields, btn.dataset, idKey, form, deleteForm, createUrl, updateUrlBase, toggleUrlBase);
            openModal();
        });
    });

    addBtn?.addEventListener('click', () => {
        console.log('Entrando a Add')
        if (deleteBtn) deleteBtn.hidden = true;
        submitBtn.textContent = 'Crear';
        if (title) title.textContent = 'Crear';
        console.log(`Reseteando form -> ${form.outerHTML}`)
        form.reset();
        form.action = createUrl;
        openModal();
    });

    document.getElementById('closeAdmin')?.addEventListener('click', closeModal);
    overlay.addEventListener('click', closeModal);
};