
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

// document.addEventListener("DOMContentLoaded", function () {
//     const mobileDropdownBtn = document.getElementById("mobile-user-dropdown-btn");
//     const mobileDropdownMenu = document.getElementById("mobile-user-dropdown");
//     const mobileMenuButton = document.getElementById("mobile-menu-button");
//     const mobileNavMenu = document.getElementById("mobile-nav-menu");
//
//     // 📌 ОТВАРЯНЕ/ЗАТВАРЯНЕ на мобилното меню (хамбургер)
//     mobileMenuButton.addEventListener("click", function () {
//         mobileNavMenu.classList.toggle("active");
//     });
//
//     // 📌 ОТВАРЯНЕ/ЗАТВАРЯНЕ на дропдаун менюто за профила
//     if (mobileDropdownBtn) {
//         mobileDropdownBtn.addEventListener("click", function (event) {
//             event.stopPropagation(); // Спира затварянето при клик върху бутона
//             mobileDropdownMenu.classList.toggle("hidden");
//
//             // Затваряне на всички други отворени дропдауни
//             document.querySelectorAll(".user-dropdown").forEach((dropdown) => {
//                 if (dropdown !== mobileDropdownMenu) {
//                     dropdown.classList.add("hidden");
//                 }
//             });
//         });
//
//         // 📌 Скриване на дропдауна при клик извън него
//         document.addEventListener("click", function (event) {
//             if (!mobileDropdownBtn.contains(event.target) && !mobileDropdownMenu.contains(event.target)) {
//                 mobileDropdownMenu.classList.add("hidden");
//             }
//         });
//     }
// });

document.addEventListener("DOMContentLoaded", function () {
    // 📌 Хамбургер меню
    const mobileMenuButton = document.getElementById("mobile-menu-button");
    const mobileNavMenu = document.getElementById("mobile-nav-menu");

    if (mobileMenuButton && mobileNavMenu) {
        mobileMenuButton.addEventListener("click", function () {
            mobileNavMenu.classList.toggle("active");
        });

        // 📌 Скриване на мобилното меню при клик извън него
        document.addEventListener("click", function (event) {
            if (!mobileMenuButton.contains(event.target) && !mobileNavMenu.contains(event.target)) {
                mobileNavMenu.classList.remove("active");
            }
        });
    }

    // 📌 Дропдаун за профил
    const mobileDropdownBtn = document.getElementById("mobile-user-dropdown-btn");
    const mobileDropdownMenu = document.getElementById("mobile-user-dropdown");

    if (mobileDropdownBtn && mobileDropdownMenu) {
        mobileDropdownBtn.addEventListener("click", function (event) {
            event.stopPropagation(); // Спира затварянето при клик върху бутона
            mobileDropdownMenu.classList.toggle("active");

            // Затваряне на всички други отворени дропдауни
            document.querySelectorAll(".user-dropdown").forEach((dropdown) => {
                if (dropdown !== mobileDropdownMenu) {
                    dropdown.classList.remove("active");
                }
            });
        });

        // 📌 Скриване на дропдауна при клик извън него
        document.addEventListener("click", function (event) {
            if (!mobileDropdownBtn.contains(event.target) && !mobileDropdownMenu.contains(event.target)) {
                mobileDropdownMenu.classList.remove("active");
            }
        });
    }
});


// ========================
