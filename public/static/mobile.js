/**
 * CreditFit 360 - Universal Mobile Navigation Controller
 * Automatically equips every page with a responsive mobile topbar,
 * sliding drawer sidebar, and touch-friendly interaction.
 */

(function () {
    function initMobileNav() {
        const sidebar = document.querySelector(".sidebar");
        if (!sidebar) return; // If page doesn't have a sidebar (e.g. login), skip

        // 1. Create and inject Mobile Header if not present
        if (!document.querySelector(".mobile-header")) {
            const mobileHeader = document.createElement("header");
            mobileHeader.className = "mobile-header";
            mobileHeader.innerHTML = `
                <a href="/dashboard" class="mobile-header-brand">
                    <div class="mobile-header-icon">✓</div>
                    <div>CreditFit<span>360</span></div>
                </a>
                <button type="button" class="mobile-hamburger-btn" id="mobileMenuToggle" aria-label="Toggle navigation menu">
                    ☰
                </button>
            `;
            document.body.prepend(mobileHeader);
        }

        // 2. Create Backdrop Overlay
        let backdrop = document.querySelector(".sidebar-backdrop");
        if (!backdrop) {
            backdrop = document.createElement("div");
            backdrop.className = "sidebar-backdrop";
            document.body.appendChild(backdrop);
        }

        // 3. Add Close button inside Sidebar
        if (!sidebar.querySelector(".sidebar-close-btn")) {
            const closeBtn = document.createElement("button");
            closeBtn.type = "button";
            closeBtn.className = "sidebar-close-btn";
            closeBtn.innerHTML = "✕";
            closeBtn.setAttribute("aria-label", "Close Menu");
            sidebar.prepend(closeBtn);

            closeBtn.addEventListener("click", closeMobileSidebar);
        }

        // 4. Hamburger click handler
        const toggleBtn = document.getElementById("mobileMenuToggle");
        if (toggleBtn) {
            toggleBtn.addEventListener("click", function (e) {
                e.stopPropagation();
                toggleMobileSidebar();
            });
        }

        // 5. Backdrop click to close
        backdrop.addEventListener("click", closeMobileSidebar);

        // 6. Close when any navigation link inside sidebar is clicked
        sidebar.querySelectorAll(".menu a").forEach(link => {
            link.addEventListener("click", closeMobileSidebar);
        });

        // 7. Close on Escape key
        document.addEventListener("keydown", function (e) {
            if (e.key === "Escape") closeMobileSidebar();
        });

        // 8. Absolute clamp: Never allow sidebar to scroll horizontally
        sidebar.scrollLeft = 0;
        sidebar.addEventListener("scroll", function () {
            if (sidebar.scrollLeft !== 0) {
                sidebar.scrollLeft = 0;
            }
        }, { passive: true });
        window.addEventListener("resize", function () {
            if (sidebar) sidebar.scrollLeft = 0;
        });

        function toggleMobileSidebar() {
            sidebar.classList.toggle("mobile-open");
            backdrop.classList.toggle("active");
            document.body.style.overflow = sidebar.classList.contains("mobile-open") ? "hidden" : "";
            sidebar.scrollLeft = 0;
        }

        function closeMobileSidebar() {
            sidebar.classList.remove("mobile-open");
            backdrop.classList.remove("active");
            document.body.style.overflow = "";
            sidebar.scrollLeft = 0;
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initMobileNav);
    } else {
        initMobileNav();
    }
})();
