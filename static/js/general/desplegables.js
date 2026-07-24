document.addEventListener('DOMContentLoaded', () => {
    const triggers = document.querySelectorAll('.fire-desplegable');

    triggers.forEach((trigger) => {
        const wrapper = trigger.closest('.dropdown-wrapper');
        if (!wrapper) return;

        const menu = wrapper.querySelector('.relative-block');
        if (!menu) return;

        trigger.addEventListener('click', (event) => {
            event.stopPropagation();

            const isOpen = menu.classList.contains('open');

            document.querySelectorAll('.relative-block.open').forEach((otroMenu) => {
                if (otroMenu !== menu) {
                    otroMenu.classList.remove('open');
                }
            });

            menu.classList.toggle('open', !isOpen);
        });
    });

    document.addEventListener('click', (event) => {
        document.querySelectorAll('.relative-block.open').forEach((menu) => {
            const wrapper = menu.closest('.dropdown-wrapper');
            if (wrapper && !wrapper.contains(event.target)) {
                menu.classList.remove('open');
            }
        });
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            document.querySelectorAll('.relative-block.open').forEach((menu) => {
                menu.classList.remove('open');
            });
        }
    });
});