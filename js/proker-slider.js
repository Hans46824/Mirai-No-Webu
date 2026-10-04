// Shared Independent Documentation Slider (Portrait & Landscape)
// Used in kegiatan.html and all proker pages (ktn.html, njr.html, konbini.html, ramadhan.html)
function initIndependentSliders() {
  const wrappers = document.querySelectorAll('.slider-wrapper');

  wrappers.forEach((wrapper) => {
    if (wrapper.dataset.sliderInitialized) return;
    wrapper.dataset.sliderInitialized = 'true';

    const slider = wrapper.querySelector('.independent-slider');
    if (!slider) return;

    const prevBtn = wrapper.querySelector('.prev-btn');
    const nextBtn = wrapper.querySelector('.next-btn');

    // Event Click Next (jika ada tombol)
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        slider.scrollBy({ left: 250, behavior: 'smooth' });
      });
    }

    // Event Click Prev (jika ada tombol)
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        slider.scrollBy({ left: -250, behavior: 'smooth' });
      });
    }

    // Auto-Slide Interval (setiap 3500ms)
    let timer = null;
    function startAutoSlide() {
      stopAutoSlide();
      timer = setInterval(() => {
        if (slider.scrollLeft + slider.clientWidth >= slider.scrollWidth - 10) {
          slider.scrollTo({ left: 0, behavior: 'smooth' });
        } else {
          slider.scrollBy({ left: 250, behavior: 'smooth' });
        }
      }, 3500);
    }

    function stopAutoSlide() {
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
    }

    startAutoSlide();

    // Hentikan sementara saat di-hover atau disentuh agar interaksi user nyaman
    wrapper.addEventListener('mouseenter', stopAutoSlide);
    wrapper.addEventListener('mouseleave', startAutoSlide);
    wrapper.addEventListener('touchstart', stopAutoSlide, { passive: true });
    wrapper.addEventListener('touchend', startAutoSlide, { passive: true });

    // Drag-to-scroll halus dengan Mouse / Trackpad click-drag
    let isDown = false;
    let startX = 0;
    let scrollStart = 0;
    let hasMoved = false;

    slider.addEventListener('mousedown', (e) => {
      isDown = true;
      hasMoved = false;
      slider.classList.add('is-dragging');
      startX = e.pageX - slider.offsetLeft;
      scrollStart = slider.scrollLeft;
      stopAutoSlide();
    });

    window.addEventListener('mouseup', () => {
      if (isDown) {
        isDown = false;
        slider.classList.remove('is-dragging');
        startAutoSlide();
      }
    });

    slider.addEventListener('mousemove', (e) => {
      if (!isDown) return;
      e.preventDefault();
      hasMoved = true;
      const x = e.pageX - slider.offsetLeft;
      const walk = (x - startX) * 1.35;
      slider.scrollLeft = scrollStart - walk;
    });

    // Mencegah drag bawaan gambar browser saat drag manual
    slider.querySelectorAll('img').forEach((img) => {
      img.addEventListener('dragstart', (e) => e.preventDefault());
      img.addEventListener('click', (e) => {
        if (hasMoved) {
          e.preventDefault();
          e.stopPropagation();
        }
      });
    });

    // Navigasi horizontal menggunakan wheel scroll mousepad / mouse
    slider.addEventListener('wheel', (e) => {
      if (Math.abs(e.deltaY) > Math.abs(e.deltaX) && Math.abs(e.deltaY) > 6) {
        e.preventDefault();
        slider.scrollBy({ left: e.deltaY * 1.15, behavior: 'auto' });
      }
    }, { passive: false });
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initIndependentSliders);
} else {
  initIndependentSliders();
}

