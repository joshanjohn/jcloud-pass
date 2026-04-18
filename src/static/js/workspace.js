
/**
 * Workspace UI Logic
 * Handles folder creation, dropdowns, and file operations.
 */

// Global access for layout triggers
window.handleUploadTrigger = function(id) {
    const input = document.getElementById(id);
    if (input) {
        console.log("Triggering input:", id);
        input.click();
    }
};

window.handleFileChange = function(input) {
    if (input.files && input.files.length > 0) {
        console.log("File selected, submitting form...");
        input.form.submit();
    }
};

window.handleLogout = function() {
    window.location.href = '/logout';
};

(function() {
    function init() {
        console.log("Workspace JS initializing...");
        
        // Initialize Lucide Icons
        if (window.lucide) {
            window.lucide.createIcons();
        }

        initCreateFolder();
        checkErrors();
        initDropdowns();
        initActionHandlers();
    }

    /**
     * Handle Dropdown logic using event delegation
     */
    function initDropdowns() {
        document.addEventListener("click", (e) => {
            const toggle = e.target.closest('.dropdown-toggle');
            if (toggle) {
                e.preventDefault();
                e.stopPropagation();
                
                const dropdown = toggle.closest('.dropdown');
                const content = dropdown.querySelector('.dropdown-content');
                
                // Close other open dropdowns
                document.querySelectorAll('.dropdown-content.show').forEach(d => {
                    if (d !== content) d.classList.remove('show');
                });

                content.classList.toggle('show');
                return;
            }

            // Close dropdowns when clicking outside
            if (!e.target.closest('.dropdown')) {
                document.querySelectorAll('.dropdown-content.show').forEach(d => {
                    d.classList.remove('show');
                });
            }
        });

        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") {
                document.querySelectorAll('.dropdown-content.show').forEach(d => {
                    d.classList.remove('show');
                });
            }
        });
    }

    /**
     * Handle Item Actions (Rename, Delete)
     */
    function initActionHandlers() {
        document.addEventListener("click", (e) => {
            const actionBtn = e.target.closest('[data-action]');
            if (!actionBtn) return;

            const action = actionBtn.dataset.action;
            const name = actionBtn.dataset.name;
            const path = actionBtn.dataset.path;
            const type = actionBtn.dataset.type;

            if (action === 'rename') {
                renameItem(name, path, type);
            } else if (action === 'delete') {
                deleteItem(name, path, type);
            } else if (action === 'open' && type === 'directory') {
                window.location.href = path;
            }
        });
    }

    function deleteItem(name, path, type) {
        if (confirm(`Are you sure you want to delete this ${type}: "${name}"?`)) {
            console.log(`Deleting ${type}: ${path}`);
            alert("Delete functionality coming soon!");
        }
    }

    function renameItem(name, path, type) {
        const newName = prompt(`Enter new name for ${type}:`, name);
        if (newName && newName !== name) {
            console.log(`Renaming ${type} from ${name} to ${newName} at ${path}`);
            alert("Rename functionality coming soon!");
        }
    }

    function initCreateFolder() {
        const btn = document.getElementById("create-folder-btn");
        const modal = document.getElementById("create-folder-modal");
        if (!btn || !modal) return;

        const closeBtn = document.getElementById("create-folder-modal-close-btn");
        const cancelBtn = document.getElementById("create-folder-modal-cancel-btn");
        const backdrop = document.getElementById("modal-backdrop");
        const input = document.getElementById("folder-name-input");
        const confirmBtn = document.getElementById("create-folder-modal-confirm-btn");
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
        backdrop.addEventListener("click", (e) => {
            if (e.target === backdrop) closeModal();
        });

        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape" && !modal.classList.contains("hidden")) {
                closeModal();
            }
        });

        const errorEl = document.getElementById("modal-error");
        if (errorEl && input) {
            input.addEventListener("input", () => {
                errorEl.classList.add("hidden");
                input.classList.remove("input-error");
            });
        }
    }

    function checkErrors() {
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

                const url = new URL(window.location);
                url.searchParams.delete('error');
                window.history.replaceState({}, '', url);
            }
        }
    }

    // Run initialization
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
