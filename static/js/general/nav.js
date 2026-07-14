let lastScroll = 0;
const navbar = document.querySelector('nav');

window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;

    if (currentScroll > lastScroll) {
        navbar.classList.add('hidden');   
    } else {
        navbar.classList.remove('hidden');
    }

    lastScroll = currentScroll;
});