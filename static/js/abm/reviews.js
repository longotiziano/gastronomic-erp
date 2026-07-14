import { setupCrudModal } from './crud.js';

const fields = {
    reservation_id: 'reservation_id',
    stars: 'stars',
    description: 'description',
};
const createUrl = '/reviews/create';
const updateUrlBase = '/reviews/update';
const toggleUrlBase = '/reviews/delete';

setupCrudModal(fields, createUrl, updateUrlBase, toggleUrlBase);

// Estrellas interactivas — crud.js setea el value del hidden, esto solo actualiza el visual
const starsInput = document.getElementById('stars');
const reservationGroup = document.getElementById('reservation-group');
let selectedStars = 0;

function setStars(value) {
    selectedStars = value;
    starsInput.value = value;
    document.querySelectorAll('.star-btn').forEach(btn => {
        btn.classList.toggle('active', Number(btn.dataset.value) <= value);
    });
}

document.querySelectorAll('.star-btn').forEach(btn => {
    btn.addEventListener('click', () => setStars(Number(btn.dataset.value)));
    btn.addEventListener('mouseenter', () => {
        document.querySelectorAll('.star-btn').forEach(b => {
            b.classList.toggle('active', Number(b.dataset.value) <= Number(btn.dataset.value));
        });
    });
    btn.addEventListener('mouseleave', () => setStars(selectedStars));
});

// Al abrir para editar: pintar estrellas y ocultar selector de reserva
document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        setStars(Number(btn.dataset.stars));
        if (reservationGroup) reservationGroup.hidden = true;
    });
});


