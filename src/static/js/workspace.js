
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
            const id = actionBtn.dataset.id;
            const name = actionBtn.dataset.name;
            const path = actionBtn.dataset.path;
            const type = actionBtn.dataset.type;

            if (action === 'rename') {
                renameItem(name, path, type);
            } else if (action === 'delete') {
                deleteItem(name, path, type, id);
            } else if (action === 'open' && type === 'directory') {
                window.location.href = path;
            }
        });
    }

    async function deleteItem(name, path, type, id) {
        if (!confirm(`Are you sure you want to delete this ${type}: "${name}"?`)) {
            return;
        }

        if (!id && type === 'file') {
            console.error("Delete aborted: File ID is missing.");
            alert("Error: File ID not found. This file might not have a database record.");
            return;
        }

        console.log(`Attempting delete for ${type}: ${path} (ID: ${id})`);
        
        if (type === 'file') {
            const formData = new FormData();
            formData.append('file_id', id);
            formData.append('full_path', path);

            try {
                const response = await fetch('/workspace/file/', {
                    method: 'DELETE',
                    body: formData
                });

                if (response.ok) {
                    window.location.reload();
                } else {
                    const errorJson = await response.json().catch(() => ({}));
                    console.error("Delete failed status:", response.status, errorJson);
                    const detail = errorJson.detail ? JSON.stringify(errorJson.detail) : "Unknown error";
                    alert(`Deletion Failed (${response.status}): ${detail}`);
                }
            } catch (err) {
                console.error("Fetch error:", err);
                alert("Network error. Check connection.");
            }
        } else {
            const formData = new FormData();
            formData.append('id', id);
            formData.append('name', name);
            formData.append('path', path);

            try{ 
                const response = await fetch('/workspace/dir/', {
                    method: 'DELETE',
                    body: formData
                });

                if (response.ok) {
                    window.location.reload();
                } else {
                    const errorJson = await response.json().catch(() => ({}));
                    console.error("Delete folder failed status:", response.status, errorJson);
                    const detail = errorJson.message || "Unknown error";
                    alert(`Deletion Failed: ${detail}`);
                }

            }catch (err) {
                console.error("Fetch error:", err);
                alert("Network error. Check connection.");
            }
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
        const modal = document.getElementById("create-folder-modal");
        if (!modal) return;

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

        const openModal = () => {
            modal.classList.remove("hidden");
            setTimeout(() => { if(input) input.focus(); }, 50);
        };

        // Delegate click for multiple Create Folder buttons
        document.addEventListener("click", (e) => {
            if (e.target.closest(".create-folder-btn")) {
                openModal();
            }
        });

        if(closeBtn) closeBtn.addEventListener("click", closeModal);
        if(cancelBtn) cancelBtn.addEventListener("click", closeModal);
        if(backdrop) backdrop.addEventListener("click", (e) => {
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
