// Toggle Mobile Menu
const hamburgerMenu = document.getElementById("hamburger-menu");
const mobileMenuOverlay = document.getElementById("mobile-menu-overlay");
const closeBtn = document.getElementById("close-btn");

hamburgerMenu.addEventListener("click", function() {
    mobileMenuOverlay.style.display = "flex";
});

closeBtn.addEventListener("click", function() {
    mobileMenuOverlay.style.display = "none";
});
