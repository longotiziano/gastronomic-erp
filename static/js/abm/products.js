document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('toggle-recipe-form');
    const recipeSection = document.getElementById('recipe-form-section');

    toggleButton?.addEventListener('click', () => {
        const isHidden = recipeSection?.style.display === 'none';
        if (recipeSection) {
            recipeSection.style.display = isHidden ? 'block' : 'none';
        }
        if (toggleButton) {
            toggleButton.textContent = isHidden ? 'Ocultar receta' : 'Agregar receta';
        }
    });
});
