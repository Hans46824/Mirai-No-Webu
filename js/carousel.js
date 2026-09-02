document.addEventListener("DOMContentLoaded", () => {
    const slider = document.querySelector("[data-slider]");
    if (!slider) return;

    const slides = [...slider.querySelectorAll(".benefit-slide")];
    const previous = document.querySelector("[data-slide='prev']");
    const next = document.querySelector("[data-slide='next']");
    const dots = document.querySelector("[data-dots]");
    let active = 0;
    let startX = null;

    const show = (index) => {
        active = (index + slides.length) % slides.length;
        slides.forEach((slide, i) => {
            slide.classList.toggle("is-active", i === active);
            slide.setAttribute("aria-hidden", String(i !== active));
        });
        dots.querySelectorAll("button").forEach((dot, i) => dot.classList.toggle("is-active", i === active));
    };

    slides.forEach((_, index) => {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.setAttribute("aria-label", "Tampilkan slide " + (index + 1));
        dot.addEventListener("click", () => show(index));
        dots.appendChild(dot);
    });

    previous.addEventListener("click", () => show(active - 1));
    next.addEventListener("click", () => show(active + 1));
    slider.addEventListener("touchstart", (event) => { startX = event.changedTouches[0].screenX; }, { passive: true });
    slider.addEventListener("touchend", (event) => {
        if (startX === null) return;
        const distance = event.changedTouches[0].screenX - startX;
        if (Math.abs(distance) > 45) show(active + (distance < 0 ? 1 : -1));
        startX = null;
    }, { passive: true });
    document.addEventListener("keydown", (event) => {
        if (!slider.matches(":hover") && document.activeElement.tagName === "INPUT") return;
        if (event.key === "ArrowLeft") show(active - 1);
        if (event.key === "ArrowRight") show(active + 1);
    });
    show(0);
});
