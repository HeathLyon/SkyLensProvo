// Menu toggle for mobile nav
const toggleButton = document.getElementById('menu-toggle');
const navLinks = document.getElementById('nav-links');

toggleButton.addEventListener('click', () => {
  navLinks.classList.toggle('active');
});

// Update last modified time in footer
const lastUpdated = document.getElementById('last-updated');
if (lastUpdated) {
  const updated = new Date(document.lastModified);
  lastUpdated.textContent = `Last updated: ${updated.toLocaleDateString()} ${updated.toLocaleTimeString()}`;
}
document.addEventListener("DOMContentLoaded", function () {
  const today = new Date();
  const endOfAugust = new Date(today.getFullYear(), 7, 31); // Month is 0-indexed: 7 = August
  const timeDiff = endOfAugust - today;
  const daysLeft = Math.max(0, Math.ceil(timeDiff / (1000 * 60 * 60 * 24)));

  const daysLeftEl = document.getElementById("days-left");
  if (daysLeftEl) {
    daysLeftEl.textContent = daysLeft;
  }
});
let slideIndex = 0;
const showSlides = () => {
  const slides = document.getElementsByClassName("slide");
  for (let s of slides) s.style.display = "none";

  slideIndex++;
  if (slideIndex > slides.length) slideIndex = 1;

  slides[slideIndex - 1].style.display = "block";
  setTimeout(showSlides, 10000); // Change every 5 seconds
};

showSlides();

// Manual controls
document.querySelector(".prev").onclick = () => {
  slideIndex -= 2;
  if (slideIndex < 0) slideIndex = 0;
  showSlides();
};

document.querySelector(".next").onclick = () => {
  showSlides();
};

// Custom cursor for drone emoji
// Select the drone element
const drone = document.getElementById("cursor-drone");

// Images to avoid
const avoidanceTargets = document.querySelectorAll(".slide-img, .portfolio-item img");

const DRONE_RADIUS = 14; // half of SVG size
const AVOID_PADDING = 6; // distance from image

let mouseX = 0;
let mouseY = 0;
let droneX = 0;
let droneY = 0;

document.addEventListener("mousemove", (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
});

// Check collision
function collides(x, y, rect) {
  return (
    x + DRONE_RADIUS > rect.left - AVOID_PADDING &&
    x - DRONE_RADIUS < rect.right + AVOID_PADDING &&
    y + DRONE_RADIUS > rect.top - AVOID_PADDING &&
    y - DRONE_RADIUS < rect.bottom + AVOID_PADDING
  );
}

// Calculate safe position with orbit
function getSafePosition(targetX, targetY) {
  for (const el of avoidanceTargets) {
    const rect = el.getBoundingClientRect();

    if (collides(targetX, targetY, rect)) {
      // Find center of image
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;

      // Vector from center to mouse
      let dx = targetX - centerX;
      let dy = targetY - centerY;
      let distance = Math.sqrt(dx * dx + dy * dy);

      // If mouse is exactly at center, give default vector
      if (distance === 0) {
        dx = 1;
        dy = 0;
        distance = 1;
      }

      // Minimum distance to orbit
      const minDist = Math.max(rect.width, rect.height) / 2 + DRONE_RADIUS + AVOID_PADDING;

      // Normalize vector
      const nx = dx / distance;
      const ny = dy / distance;

      const orbitX = centerX + nx * minDist;
      const orbitY = centerY + ny * minDist;

      return { x: orbitX, y: orbitY };
    }
  }

  return { x: targetX, y: targetY };
}

// Animate drone
function animate() {
  const safe = getSafePosition(mouseX, mouseY);

  // Smooth follow
  droneX += (safe.x - droneX) * 0.1;
  droneY += (safe.y - droneY) * 0.1;

  drone.style.left = droneX + "px";
  drone.style.top = droneY + "px";

  requestAnimationFrame(animate);
}

animate();
