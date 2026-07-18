import { parseDateTime } from "../general/utils.js";

const fillForm = (fields, data, idKey, form, deleteForm, updateUrlBase, toggleUrlBase) => {
    Object.entries(fields).forEach(([fieldName, dataKey]) => {
        // Buscar el campo DENTRO del form, no en todo el documento
        const input = form.querySelector(`[name="${fieldName}"]`);
        if (!input) return;

        if (input.type === 'checkbox') {
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

export const setupCrudModal = (container, fields, createUrl, updateUrlBase, toggleUrlBase, idKey = 'id') => {
    // Todo scopeado al container, no a document
    const modal = container.querySelector('[data-openby="formOpener"]');
    const overlay = document.querySelector('.overlay'); // este SÍ puede ser global si es compartido
    const form = container.querySelector('.form-principal');
    const deleteForm = container.querySelector('.formDelete');
    const addBtn = container.querySelector('.add-btn');
    const submitBtn = container.querySelector('.submit-btn[type="submit"]');
    const deleteBtn = container.querySelector('.delete-btn');
    const title = modal.querySelector('.block-header h2');

    const openModal = () => { modal.classList.add('open'); overlay.classList.add('active'); };
    const closeModal = () => { modal.classList.remove('open'); overlay.classList.remove('active'); };

    container.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            if (deleteBtn) deleteBtn.hidden = false;
            submitBtn.textContent = 'Actualizar';
            if (title) title.textContent = 'Actualizar';
            fillForm(fields, btn.dataset, idKey, form, deleteForm, updateUrlBase, toggleUrlBase);
            openModal();
        });
    });

    addBtn?.addEventListener('click', () => {
        if (deleteBtn) deleteBtn.hidden = true;
        submitBtn.textContent = 'Crear';
        if (title) title.textContent = 'Crear';
        form.reset();
        form.action = createUrl;
        openModal();
    });

    container.querySelector('.closeForm')?.addEventListener('click', closeModal);
    overlay.addEventListener('click', closeModal);
};