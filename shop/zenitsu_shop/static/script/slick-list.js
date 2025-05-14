document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.content-slider-carousel-wrapper').forEach(initCarousel);
});

function initCarousel(carouselWrapper) {
    const container = carouselWrapper.querySelector('.product-container');
    const cards = container.querySelectorAll('.product-card');
    const prevBtn = carouselWrapper.querySelector('.prev');
    const nextBtn = carouselWrapper.querySelector('.next');

    const cardsToScroll = 3;
    let currentIndex = 0;

    function updateCarousel() {
        if (cards.length === 0) return;
        const cardWidth = cards[0].offsetWidth + 20;
        const translateX = -currentIndex * cardWidth * cardsToScroll;
        container.style.transform = `translateX(${translateX}px)`;

        prevBtn.disabled = currentIndex === 0;
        nextBtn.disabled = currentIndex >= Math.ceil(cards.length / cardsToScroll) - 1;
    }

    function moveSlide(direction) {
        if (direction === -1 && currentIndex > 0) {
            currentIndex--;
        } else if (direction === 1 && currentIndex < Math.ceil(cards.length / cardsToScroll) - 1) {
            currentIndex++;
        }
        updateCarousel();
    }

    prevBtn.addEventListener('click', () => moveSlide(-1));
    nextBtn.addEventListener('click', () => moveSlide(1));

    updateCarousel();
    window.addEventListener('resize', updateCarousel);
}