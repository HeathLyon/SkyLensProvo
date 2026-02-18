document.addEventListener("DOMContentLoaded", () => {

  /* ===============================
     MOBILE MENU
  =============================== */
  const toggleButton = document.getElementById("menu-toggle");
  const navLinks = document.getElementById("nav-links");

  if (toggleButton && navLinks) {
    toggleButton.addEventListener("click", () => {
      navLinks.classList.toggle("active");
    });
  }

  /* ===============================
     FOOTER LAST UPDATED
  =============================== */
  const lastUpdated = document.getElementById("last-updated");
  if (lastUpdated) {
    const updated = new Date(document.lastModified);
    lastUpdated.textContent =
      `Last updated: ${updated.toLocaleDateString()} ${updated.toLocaleTimeString()}`;
  }

  /* ===============================
     COUNTDOWN (OPTIONAL)
  =============================== */
  const daysLeftEl = document.getElementById("days-left");
  if (daysLeftEl) {
    const today = new Date();
    const endOfAugust = new Date(today.getFullYear(), 7, 31);
    const daysLeft = Math.max(
      0,
      Math.ceil((endOfAugust - today) / (1000 * 60 * 60 * 24))
    );
    daysLeftEl.textContent = daysLeft;
  }

  /* ===============================
     SLIDESHOW
  =============================== */
  let slideIndex = 0;
  const slides = document.getElementsByClassName("slide");

  function showSlides() {
    if (!slides.length) return;

    for (let s of slides) s.style.display = "none";

    slideIndex++;
    if (slideIndex > slides.length) slideIndex = 1;

    slides[slideIndex - 1].style.display = "block";
    setTimeout(showSlides, 10000);
  }

  if (slides.length) {
    showSlides();

    const prev = document.querySelector(".prev");
    const next = document.querySelector(".next");

    if (prev) {
      prev.onclick = () => {
        slideIndex -= 2;
        if (slideIndex < 0) slideIndex = 0;
        showSlides();
      };
    }

    if (next) {
      next.onclick = showSlides;
    }
  }

 /* ===============================
   DRONE CURSOR (Hide Over Images)
=============================== */

const drone = document.getElementById("cursor-drone");
if (!drone) return;

const avoidanceTargets = document.querySelectorAll(
  ".slide-img, .portfolio-item img"
);

let mouseX = 0;
let mouseY = 0;

document.addEventListener("mousemove", (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;

  drone.style.left = mouseX + "px";
  drone.style.top = mouseY + "px";

  checkHover();
});

function checkHover() {
  let isOverImage = false;

  avoidanceTargets.forEach((el) => {
    const rect = el.getBoundingClientRect();

    if (
      mouseX >= rect.left &&
      mouseX <= rect.right &&
      mouseY >= rect.top &&
      mouseY <= rect.bottom
    ) {
      isOverImage = true;
    }
  });

  if (isOverImage) {
    drone.classList.add("hidden");
  } else {
    drone.classList.remove("hidden");
  }
}})