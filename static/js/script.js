
// Скрипт за дродаун менюто

document.addEventListener("DOMContentLoaded", function () {
    const dropdownBtn = document.getElementById("user-dropdown-btn");
    const dropdownMenu = document.getElementById("user-dropdown");

    if (dropdownBtn) {
        dropdownBtn.addEventListener("click", function (event) {
            event.stopPropagation();
            dropdownMenu.classList.toggle("show");
            dropdownBtn.classList.toggle("active");
        });

        // Скрий дропдауна, ако се кликне извън него
        document.addEventListener("click", function (event) {
            if (!dropdownBtn.contains(event.target) && !dropdownMenu.contains(event.target)) {
                dropdownMenu.classList.remove("show");
                dropdownBtn.classList.remove("active");
            }
        });
    }
});

// =============================
// JavaScript за мобилното меню
document.getElementById("mobile-menu-button").addEventListener("click", function () {
    document.getElementById("nav-menu").classList.toggle("active");
});

// ========================
