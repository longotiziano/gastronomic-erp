// Código js para el funcionamiento de los carruseles

document.addEventListener("DOMContentLoaded", () => {

    const wrappers = document.querySelectorAll(".carousel-wrapper");

    wrappers.forEach(wrapper => {
        const carousel = wrapper.querySelector(".carousel");
        const prevBtn = wrapper.querySelector(".prev-btn");
        const nextBtn = wrapper.querySelector(".next-btn");

        if (carousel && prevBtn && nextBtn) {
            
            nextBtn.addEventListener("click", () => {
                const cardWidth = carousel.offsetWidth + 20;
                
                if (carousel.scrollLeft + carousel.offsetWidth >= carousel.scrollWidth - 5) {
                    carousel.scrollTo({ left: 0, behavior: "smooth" });
                } else {
                    carousel.scrollBy({ left: cardWidth, behavior: "smooth" });
                }
            });

            prevBtn.addEventListener("click", () => {
                const cardWidth = carousel.offsetWidth + 20;
                
                if (carousel.scrollLeft <= 0) {
                    carousel.scrollTo({ left: carousel.scrollWidth, behavior: "smooth" });
                } else {
                    carousel.scrollBy({ left: -cardWidth, behavior: "smooth" });
                }
            });
        }
    });
});