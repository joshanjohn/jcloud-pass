
// This function clicks the hidden "Select File" button 
window.handleUploadTrigger = function (id) {
    const input = document.getElementById(id);
    if (input) {
        console.log("Triggering input:", id);
        input.click();
    }
};

// This function starts the upload as soon as you choose a file.
window.handleFileChange = async function (input) {
    if (input.files && input.files.length > 0) {
        await uploadFile(input);
    }
};

// UPLOAD FILE
async function uploadFile(input, override = false) {
    const file = input.files[0];
    const formData = new FormData(input.form);
    
    if (override) {
        formData.set('override', 'true');
    }

    console.log(`Uploading file "${file.name}"...`);

    try {
        const response = await fetch(input.form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        });

        if (response.status === 409) {
            const data = await response.json();
            if (confirm(`The file "${file.name}" already exists in this directory. Do you want to override it?`)) {
                return await uploadFile(input, true);
            } else {
                input.value = ''; // Reset input
                return;
            }
        }

        if (response.ok) {
            const data = await response.json();
            window.location.href = data.url || window.location.pathname;
        } else {
            console.error("Upload failed with status:", response.status);
            window.showErrorToast("Upload failed. Please try again.");
        }
    } catch (err) {
        console.error("Error during upload:", err);
        window.showErrorToast("Network error. Check connection.");
    }
}

// LOGOUT
window.handleLogout = function () {
    window.location.href = '/logout';
};

// workspace back button 
window.handleWorkspaceBack = function (parentUrl) {
    if (parentUrl && parentUrl !== window.location.pathname) {
        window.location.href = parentUrl;
        return;
    }

    if (window.history.length > 1) {
        window.history.back();
        return;
    }

    window.location.href = '/workspace';
};

// Error tost function 
window.showErrorToast = function (message) {
    const container = document.getElementById('toast-container');
    const template = document.getElementById('toast-template');
    if (!container || !template) return;

    const toastNode = template.content.cloneNode(true);
    const toast = toastNode.firstElementChild;
    const messageEl = toast.querySelector('.toast-message');

    if (messageEl) {
        // update message content
        messageEl.textContent = message;
    }

    const closeBtn = toast.querySelector('.toast-close');
    if (closeBtn) {
        closeBtn.onclick = () => window.removeToast(toast);
    }

    container.appendChild(toast);

    if (window.lucide) {
        window.lucide.createIcons({ root: toast });
    }

    requestAnimationFrame(() => {
        toast.classList.remove('translate-y-4', 'opacity-0');
    });

    const timeoutId = setTimeout(() => {
        window.removeToast(toast);
    }, 15000); // 15 seconds 

    toast.dataset.timeoutId = timeoutId;
};

// remove Error tost 
window.removeToast = function (toast) {
    toast.classList.add('translate-y-4', 'opacity-0');
    if (toast.dataset.timeoutId) {
        clearTimeout(toast.dataset.timeoutId);
    }
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, 300);
};

(function () {
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



            if (action === 'delete') {
                deleteItem(name, path, type, id);
            } else if (action === 'download') {
                downloadItem(name, path, type, id);
            }
        });
    }


    // DELETE ITEM
    async function deleteItem(name, path, type, id) {
        if (!confirm(`Are you sure you want to delete this ${type}: "${name}"?`)) {
            return;
        }

        if (!id && type === 'file') {
            console.error("Delete aborted: File ID is missing.");
            window.showErrorToast("Error: File ID not found. This file might not have a database record.");
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
                    window.showErrorToast(`Deletion Failed (${response.status}): ${detail}`);
                }
            } catch (err) {
                console.error("Fetch error:", err);
                window.showErrorToast("Network error. Check connection.");
            }
        } else {
            const formData = new FormData();
            formData.append('path', path);

            try {
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
                    window.showErrorToast(`Deletion Failed: ${detail}`);
                }

            } catch (err) {
                console.error("Fetch error:", err);
                window.showErrorToast("Network error. Check connection.");
            }
        }
    }

    // DOWNLOAD
    async function downloadItem(name, path, type) {
        const formData = new FormData();
        formData.append('path', path);

        if (type === 'file') {
            try {
                const response = await fetch('/download-file', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = name;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    a.remove();
                } else {
                    const errorJson = await response.json().catch(() => ({}));
                    console.error("Download failed:", response.status, errorJson);
                    window.showErrorToast(`Download Failed: ${errorJson.message || "Unknown error"}`);
                }
            } catch (err) {
                console.error("Fetch error:", err);
                window.showErrorToast("Network error. Check connection.");
            }
        }
    }

    // ADD FOLDER
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
            setTimeout(() => { if (input) input.focus(); }, 50);
        };

        // Delegate click for multiple Create Folder buttons
        document.addEventListener("click", (e) => {
            if (e.target.closest(".create-folder-btn")) {
                openModal();
            }
        });

        if (closeBtn) closeBtn.addEventListener("click", closeModal);
        if (cancelBtn) cancelBtn.addEventListener("click", closeModal);
        if (backdrop) backdrop.addEventListener("click", (e) => {
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

    // Checking Error messages for create folder model 
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
