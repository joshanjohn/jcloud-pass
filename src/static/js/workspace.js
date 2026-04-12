
document.addEventListener("DOMContentLoaded", () => {
    initCreateFolder();
    checkErrors();
});

function initCreateFolder() {
    const btn = document.getElementById("create-folder-btn");
    const modal = document.getElementById("create-folder-modal");
    if (!btn || !modal) return;

    const closeBtn = document.getElementById("modal-close-btn");
    const cancelBtn = document.getElementById("modal-cancel-btn");
    const backdrop = document.getElementById("modal-backdrop");
    const input = document.getElementById("folder-name-input");
    const confirmBtn = document.getElementById("modal-confirm-btn");
    const btnLabel = document.getElementById("btn-label");

    const form = modal.querySelector('form');
    if (form) {
        form.addEventListener("submit", () => {
            if (confirmBtn) confirmBtn.disabled = true;
            if (btnLabel) btnLabel.textContent = "Creating...";
        });
    }

    const closeModal = () => {
        modal.classList.add("hidden");
    };

    btn.addEventListener("click", () => {
        modal.classList.remove("hidden");
        setTimeout(() => input.focus(), 50);
    });

    closeBtn.addEventListener("click", closeModal);
    cancelBtn.addEventListener("click", closeModal);

    // Clicking backdrop closes modal
    backdrop.addEventListener("click", (e) => {
        if (e.target === backdrop) closeModal();
    });

    // Escape key closes modal
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && !modal.classList.contains("hidden")) {
            closeModal();
        }
    });

    // Clear error locally if user types again
    const errorEl = document.getElementById("modal-error");
    if (errorEl && input) {
        input.addEventListener("input", () => {
            errorEl.classList.add("hidden");
            input.classList.remove("input-error");
        });
    }
}

function checkErrors() {
    // If the server redirected back with an ?error= message, 
    const urlParams = new URLSearchParams(window.location.search);
    const errorMsg = urlParams.get('error');
    if (errorMsg) {
        const modal = document.getElementById("create-folder-modal");
        const errorEl = document.getElementById("modal-error");
        const input = document.getElementById("folder-name-input");

        if (modal && errorEl) {
            modal.classList.remove("hidden");
            errorEl.textContent = errorMsg;
            errorEl.classList.remove("hidden");
            
            if (input) {
                input.classList.add("input-error");
            }

            // Clean exactly the ?error parameter from the URL to avoid reopening after a refresh
            const url = new URL(window.location);
            url.searchParams.delete('error');
            // This replaces the URL without reloading the page
            window.history.replaceState({}, '', url);
        }
    }
}
