// workspace.js — handles workspace UI interactions

document.addEventListener("DOMContentLoaded", () => {
  initCreateFolder();
});

/* ── Create Folder ──────────────────────────────────────────────── */

function initCreateFolder() {
  const btn = document.getElementById("create-folder-btn");
  if (!btn) return;

  btn.addEventListener("click", () => openCreateFolderModal());
}

function openCreateFolderModal() {
  // Remove any stale modal
  document.getElementById("create-folder-modal")?.remove();

  const overlay = document.createElement("div");
  overlay.id = "create-folder-modal";
  overlay.innerHTML = `
    <div class="modal-backdrop" id="modal-backdrop">
      <div class="modal-card" role="dialog" aria-modal="true" aria-labelledby="modal-title">

        <div class="modal-header">
          <span id="modal-title">New Folder</span>
          <button class="modal-close" id="modal-close-btn" aria-label="Close">&#x2715;</button>
        </div>

        <div class="modal-body">
          <label for="folder-name-input" class="modal-label">Folder name</label>
          <input
            id="folder-name-input"
            type="text"
            class="modal-input"
            placeholder="e.g. My Folder"
            maxlength="64"
            autocomplete="off"
          />
          <p id="modal-error" class="modal-error hidden"></p>
        </div>

        <div class="modal-footer">
          <button class="btn-secondary" id="modal-cancel-btn">Cancel</button>
          <button class="btn-primary" id="modal-confirm-btn">
            <span id="btn-label">Create</span>
            <span id="btn-spinner" class="spinner hidden"></span>
          </button>
        </div>

      </div>
    </div>
  `;


  document.body.appendChild(overlay);

  const input        = overlay.querySelector("#folder-name-input");
  const errorEl      = overlay.querySelector("#modal-error");
  const confirmBtn   = overlay.querySelector("#modal-confirm-btn");
  const cancelBtn    = overlay.querySelector("#modal-cancel-btn");
  const closeBtn     = overlay.querySelector("#modal-close-btn");
  const btnLabel     = overlay.querySelector("#btn-label");
  const btnSpinner   = overlay.querySelector("#btn-spinner");
  const backdrop     = overlay.querySelector("#modal-backdrop");

  // Focus input
  setTimeout(() => input.focus(), 50);

  // Close helpers
  const closeModal = () => overlay.remove();

  closeBtn.addEventListener("click", closeModal);
  cancelBtn.addEventListener("click", closeModal);
  backdrop.addEventListener("click", (e) => {
    if (e.target === backdrop) closeModal();
  });
  document.addEventListener("keydown", function escHandler(e) {
    if (e.key === "Escape") { closeModal(); document.removeEventListener("keydown", escHandler); }
  });

  // Confirm
  confirmBtn.addEventListener("click", () => submitCreateFolder(input, errorEl, confirmBtn, btnLabel, btnSpinner, closeModal));
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") submitCreateFolder(input, errorEl, confirmBtn, btnLabel, btnSpinner, closeModal);
  });

  // Clear error on typing
  input.addEventListener("input", () => {
    errorEl.classList.add("hidden");
    input.classList.remove("input-error");
  });
}

async function submitCreateFolder(input, errorEl, confirmBtn, btnLabel, btnSpinner, closeModal) {
  const name = input.value.trim();

  if (!name) {
    showError(input, errorEl, "Folder name cannot be empty.");
    return;
  }
  if (name.length > 64) {
    showError(input, errorEl, "Folder name must be 64 characters or fewer.");
    return;
  }

  // Loading state
  confirmBtn.disabled = true;
  btnLabel.textContent = "Creating…";
  btnSpinner.classList.remove("hidden");

  try {
    const res = await fetch("/workspace/create_directory", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });

    const data = await res.json();

    if (res.ok && data.success) {
      closeModal();
      // Reload page so the new folder appears in the grid + sidebar
      window.location.reload();
    } else {
      showError(input, errorEl, data.message || "Failed to create folder.");
      resetBtn(confirmBtn, btnLabel, btnSpinner);
    }
  } catch (err) {
    console.error("Create folder error:", err);
    showError(input, errorEl, "Network error. Please try again.");
    resetBtn(confirmBtn, btnLabel, btnSpinner);
  }
}

function showError(input, errorEl, message) {
  errorEl.textContent = message;
  errorEl.classList.remove("hidden");
  input.classList.add("input-error");
  input.focus();
}

function resetBtn(btn, label, spinner) {
  btn.disabled = false;
  label.textContent = "Create";
  spinner.classList.add("hidden");
}
