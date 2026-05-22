'use strict';

/* ===== NAVBAR DROPDOWN ===== */
document.addEventListener('DOMContentLoaded', function () {
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userMenu = document.getElementById('userMenu');

    if (userMenuBtn && userMenu) {
        userMenuBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            userMenu.classList.toggle('open');
        });
        document.addEventListener('click', function () {
            userMenu.classList.remove('open');
        });
    }

    /* ===== MOBILE HAMBURGER ===== */
    const hamburger = document.getElementById('hamburger');
    const catNav = document.querySelector('.category-nav');
    if (hamburger && catNav) {
        hamburger.addEventListener('click', function () {
            catNav.classList.toggle('cat-open');
            hamburger.classList.toggle('active');
        });
    }

    /* ===== AUTO-DISMISS ALERTS ===== */
    document.querySelectorAll('.alert').forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 400);
        }, 4500);
    });

    /* ===== ADD TO CART ANIMATION ===== */
    document.querySelectorAll('.btn-add-cart').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            const original = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-check"></i> Added!';
            btn.style.background = '#22c55e';
            setTimeout(() => {
                btn.innerHTML = original;
                btn.style.background = '';
            }, 1500);
        });
    });
});
