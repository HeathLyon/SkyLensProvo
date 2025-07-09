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
