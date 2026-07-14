/**
 * =============================================================
 * Main JavaScript — Healthcare Theme
 * Lung Cancer Prediction using Deep Neural Network
 * =============================================================
 * Handles: form validation, scroll animations, navbar behavior,
 * alert auto-dismiss, and interactive UI enhancements.
 */

document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    // ============================================================
    // 1. AUTO-DISMISS FLASH ALERTS (after 5 seconds)
    // ============================================================
    const alerts = document.querySelectorAll(".alert-dismissible");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });

    // ============================================================
    // 2. NAVBAR SCROLL SHADOW
    // ============================================================
    const navbar = document.querySelector(".navbar");
    if (navbar) {
        window.addEventListener("scroll", function () {
            if (window.scrollY > 20) {
                navbar.classList.add("shadow");
            } else {
                navbar.classList.remove("shadow");
            }
        });
    }

    // ============================================================
    // 3. SMOOTH SCROLL FOR ANCHOR LINKS
    // ============================================================
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener("click", function (e) {
            const targetId = this.getAttribute("href");
            if (targetId && targetId !== "#") {
                e.preventDefault();
                const target = document.querySelector(targetId);
                if (target) {
                    target.scrollIntoView({ behavior: "smooth", block: "start" });
                }
            }
        });
    });

    // ============================================================
    // 4. SCROLL-TRIGGERED FADE-IN ANIMATION
    // ============================================================
    const animateElements = document.querySelectorAll(
        ".step-card, .feature-card-new, .tech-card, .stat-card, " +
        ".dashboard-stat-card, .quick-action-card, .cta-card, " +
        ".medical-card, .floating-mini"
    );

    if ("IntersectionObserver" in window && animateElements.length > 0) {
        const observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry, index) {
                    if (entry.isIntersecting) {
                        // Stagger the animation slightly
                        setTimeout(function () {
                            entry.target.style.opacity = "1";
                            entry.target.style.transform = "translateY(0)";
                        }, index * 60);
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
        );

        animateElements.forEach(function (el) {
            el.style.opacity = "0";
            el.style.transform = "translateY(20px)";
            el.style.transition = "opacity 0.5s ease, transform 0.5s ease";
            observer.observe(el);
        });
    }

    // ============================================================
    // 5. PREDICTION FORM — CONFIRMATION DIALOG
    // ============================================================
    const predictForm = document.getElementById("predictForm");
    if (predictForm) {
        predictForm.addEventListener("submit", function (e) {
            // Only confirm if Bootstrap validation passes
            if (this.checkValidity()) {
                const confirmed = confirm(
                    "Are you sure you want to submit this prediction?\nPlease verify all inputs before proceeding."
                );
                if (!confirmed) {
                    e.preventDefault();
                }
            }
        });
    }

    // ============================================================
    // 6. ACTIVE NAV LINK HIGHLIGHTING
    // ============================================================
    const currentPath = window.location.pathname;
    document.querySelectorAll(".navbar .nav-link").forEach(function (link) {
        const href = link.getAttribute("href");
        if (href && currentPath === href) {
            link.classList.add("active");
        }
    });

    // ============================================================
    // 7. FORM RESET — Clear validation state
    // ============================================================
    const forms = document.querySelectorAll("form");
    forms.forEach(function (form) {
        const resetBtn = form.querySelector('[type="reset"]');
        if (resetBtn) {
            resetBtn.addEventListener("click", function () {
                setTimeout(function () {
                    form.classList.remove("was-validated");
                }, 10);
            });
        }
    });

    // ============================================================
    // 8. TOOLTIP INITIALIZATION (if any are present)
    // ============================================================
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0) {
        tooltipTriggerList.forEach(function (el) {
            new bootstrap.Tooltip(el);
        });
    }

    // Log successful initialization
    console.log("LungAI Application loaded successfully.");
});
