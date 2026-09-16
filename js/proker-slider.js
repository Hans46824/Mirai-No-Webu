// Shared Documentation Slider
// Usage: call initDocSlider() after DOM is ready
function initDocSlider() {
    const wraps = document.querySelectorAll('[data-doc-slider]');
    wraps.forEach((wrap) => {
        const track = wrap.querySelector('[data-slider-track]');
        const slides = wrap.querySelectorAll('[data-slide]');
        const prev = wrap.querySelector('[data-slider-prev]');
        const next = wrap.querySelector('[data-slider-next]');
        const dotsWrap = wrap.querySelector('[data-slider-dots]');
        if (!track || slides.length === 0) return;

        let current = 0;
        let autoTimer = null;
        const total = slides.length;

        // Build dots
        if (dotsWrap) {
            slides.forEach((_, i) => {
                const dot = document.createElement('button');
                dot.className = 'doc-dot' + (i === 0 ? ' is-active' : '');
                dot.type = 'button';
                dot.setAttribute('aria-label', `Slide ${i + 1}`);
                dot.addEventListener('click', () => goTo(i));
                dotsWrap.appendChild(dot);
            });
        }

        function getDots() { return dotsWrap ? dotsWrap.querySelectorAll('.doc-dot') : []; }

        function goTo(index) {
            current = (index + total) % total;
            track.style.transform = `translateX(-${current * 100}%)`;
            getDots().forEach((d, i) => d.classList.toggle('is-active', i === current));
        }

        function startAuto() {
            clearInterval(autoTimer);
            autoTimer = setInterval(() => goTo(current + 1), 3500);
        }

        function stopAuto() { clearInterval(autoTimer); }

        prev?.addEventListener('click', () => { stopAuto(); goTo(current - 1); startAuto(); });
        next?.addEventListener('click', () => { stopAuto(); goTo(current + 1); startAuto(); });

        // Pause on hover
        wrap.addEventListener('mouseenter', stopAuto);
        wrap.addEventListener('mouseleave', startAuto);

        // Touch swipe
        let touchStartX = 0;
        wrap.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; }, { passive: true });
        wrap.addEventListener('touchend', (e) => {
            const diff = touchStartX - e.changedTouches[0].clientX;
            if (Math.abs(diff) > 40) { stopAuto(); goTo(current + (diff > 0 ? 1 : -1)); startAuto(); }
        });

        goTo(0);
        startAuto();
    });
}

document.addEventListener('DOMContentLoaded', initDocSlider);

