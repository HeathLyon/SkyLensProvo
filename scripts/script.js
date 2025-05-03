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