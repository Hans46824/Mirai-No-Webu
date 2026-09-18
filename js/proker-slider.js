// Shared Independent Documentation Slider (Portrait & Landscape)
// Used in kegiatan.html and all proker pages (ktn.html, njr.html, konbini.html, ramadhan.html)
function initIndependentSliders() {
  const wrappers = document.querySelectorAll('.slider-wrapper');

  wrappers.forEach((wrapper) => {
    if (wrapper.dataset.sliderInitialized) return;
    wrapper.dataset.sliderInitialized = 'true';

    const slider = wrapper.querySelector('.independent-slider');
    const prevBtn = wrapper.querySelector('.prev-btn');
    const nextBtn = wrapper.querySelector('.next-btn');

    if (!slider) return;

    // Event Click Next
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        slider.scrollBy({ left: 250, behavior: 'smooth' });
      });
    }

    // Event Click Prev
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        slider.scrollBy({ left: -250, behavior: 'smooth' });
      });
    }

    // Auto-Slide Interval (setiap 3000ms / 3 detik)
    let timer = null;
    function startAutoSlide() {
      stopAutoSlide();
      timer = setInterval(() => {
        if (slider.scrollLeft + slider.clientWidth >= slider.scrollWidth - 10) {
          slider.scrollTo({ left: 0, behavior: 'smooth' });
        } else {
          slider.scrollBy({ left: 250, behavior: 'smooth' });
        }
      }, 3000);
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
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initIndependentSliders);
} else {
  initIndependentSliders();
}
