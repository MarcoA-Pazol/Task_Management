document.addEventListener('DOMContentLoaded', () => {
    const heroSection = document.querySelector('.hero-section');

    function animateOnScroll() {
        const windowHeight = window.innerHeight;
        const scrollY = window.scrollY || window.pageYOffset; // Cross-browser compatibility

        if (scrollY > windowHeight) {
            heroSection.classList.add('animate-in');
            window.removeEventListener('scroll', animateOnScroll);
        }
    }

    window.addEventListener('scroll', animateOnScroll);
});