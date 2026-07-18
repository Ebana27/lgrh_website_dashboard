document.addEventListener('DOMContentLoaded', () => {
    const track = document.querySelector('.carousel-track');
    const slides = Array.from(track?.children || []);
    const nextBtn = document.querySelector('.next-btn');
    const prevBtn = document.querySelector('.prev-btn');
    const dotsNav = document.querySelector('.carousel-nav');

    if (!track || slides.length === 0) return;

    // Masquer les boutons si un seul slide
    if (slides.length <= 1) {
        if (nextBtn) nextBtn.style.display = 'none';
        if (prevBtn) prevBtn.style.display = 'none';
        return;
    }

    // Création des indicateurs
    slides.forEach((_, index) => {
        const dot = document.createElement('button');
        dot.classList.add('carousel-indicator');
        if (index === 0) dot.classList.add('active');
        dotsNav.appendChild(dot);
    });

    const dots = Array.from(dotsNav.children);
    let currentIndex = 0;

    const updateSlide = (index) => {
        currentIndex = index;
        track.style.transform = `translateX(-${currentIndex * 100}%)`;
        
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentIndex);
        });
    };

    // Événements boutons
    nextBtn?.addEventListener('click', () => {
        updateSlide((currentIndex + 1) % slides.length);
    });

    prevBtn?.addEventListener('click', () => {
        updateSlide((currentIndex - 1 + slides.length) % slides.length);
    });

    // Événements indicateurs
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => updateSlide(index));
    });

    // Normalisation de l'URL du site web
    const commentForm = document.querySelector('.comment-form');
    const siteInput = commentForm?.querySelector('input[name="site_web"]');

    const formatURL = (value) => {
        let val = value.trim();
        if (!val) return '';
        if (!val.startsWith('http')) {
            return val.startsWith('www.') ? `https://${val}` : `https://www.${val}`;
        }
        return val.replace(/^http:\/\//i, 'https://');
    };

    if (siteInput) {
        siteInput.addEventListener('blur', () => {
            siteInput.value = formatURL(siteInput.value);
        });
    }
});