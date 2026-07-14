const tabs = document.querySelectorAll('.tab-btn');
const cards = document.querySelectorAll('.dish-card');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        const selected = tab.dataset.category;
        cards.forEach(card => {
            card.hidden = selected !== 'all' && card.dataset.category !== selected;
        });
    });
});
