const panels = document.querySelectorAll('.panel');
const fixedPanels = document.querySelectorAll('.fixed-block');
const overlay = document.querySelector('.overlay');

/**
 * @param {NodeList} panels - NodeList de paneles a los que se les asignará la funcionalidad de abrir/cerrar.
 * @param {Element} overlay - Elemento de superposición.
 * @param {boolean} overlayModify - Indica si se debe modificar el overlay.
 */
const toggleModals = (panels, overlay, overlayModify = false) => {
    panels.forEach(panel => {
        const btnId = panel.dataset.openby
        const btnElement = document.getElementById(btnId);
        const cancelBtn = panel.querySelector('.cancel-btn');
        if (btnElement) {
            btnElement.addEventListener('click', () => {
                panel.classList.toggle('open');
                if (overlayModify) overlay.classList.toggle('active');
            });
        if (cancelBtn) {
            cancelBtn.addEventListener('click', () => {
                panel.classList.remove('open');
                if (overlayModify) overlay.classList.remove('active');
            });
        }
        overlay.addEventListener('click', () => {
                panel.classList.remove('open');
                overlay.classList.remove('active');
            });}
    });
};

toggleModals(panels, overlay, true);
toggleModals(fixedPanels, overlay);