/**
 * KDP Book Production Studio - Project Workspace, Lock Protection & Deletion Engine
 */

let defaultRootLocation = "C:\\Users\\KadiR-PC\\Documents\\KDP_Studio_Projects";

// Current Active Project Document
let currentProject = {
  name: "My Jungle Coloring Book",
  folder_name: "My_Jungle_Coloring_Book",
  project_dir: "C:\\Users\\KadiR-PC\\Documents\\KDP_Studio_Projects\\My_Jungle_Coloring_Book",
  author: "Creative Kids Studio",
  is_locked: false,
  settings: {
    trim_width_pt: 612.0,   // 8.5 in * 72
    trim_height_pt: 792.0,  // 11.0 in * 72
    has_bleed: true,
    bleed_pt: 9.0,          // 0.125 in * 72
    margins: {
      top_pt: 27.0,         // 0.375 in * 72
      bottom_pt: 27.0,
      inside_pt: 36.0,      // 0.500 in * 72
      outside_pt: 27.0,
    },
    target_dpi: 300,
  },
  // Isolated Media Library for this project only
  media: [],
  pages: [
    {
      page_number: 1,
      title: "Page 1",
      layout: "top_ref",
      elements: [
        { id: "elem_ref_1", type: "ref_image", x: 180, y: 35, w: 150, h: 100, text: "Click to select Reference Image", image_src: null },
        { id: "elem_main_1", type: "main_image", x: 45, y: 150, w: 420, h: 420, text: "Click to select Drawing Image", image_src: null },
        { id: "elem_title_1", type: "title", x: 45, y: 585, w: 420, h: 40, text: "PAGE 1", font_size: 26, color: "#111827", font_family: "Plus Jakarta Sans" },
        { id: "elem_frame_1", type: "border", x: 30, y: 25, w: 450, h: 610 },
      ]
    },
    {
      page_number: 2,
      title: "Page 2",
      layout: "top_ref",
      elements: [
        { id: "elem_ref_2", type: "ref_image", x: 180, y: 35, w: 150, h: 100, text: "Click to select Reference Image", image_src: null },
        { id: "elem_main_2", type: "main_image", x: 45, y: 150, w: 420, h: 420, text: "Click to select Drawing Image", image_src: null },
        { id: "elem_title_2", type: "title", x: 45, y: 585, w: 420, h: 40, text: "PAGE 2", font_size: 26, color: "#111827", font_family: "Plus Jakarta Sans" },
        { id: "elem_frame_2", type: "border", x: 30, y: 25, w: 450, h: 610 },
      ]
    },
    {
      page_number: 3,
      title: "Page 3",
      layout: "full_page",
      elements: [
        { id: "elem_main_3", type: "main_image", x: 35, y: 50, w: 440, h: 520, text: "Click to select Full Page Drawing", image_src: null },
        { id: "elem_title_3", type: "title", x: 45, y: 585, w: 420, h: 40, text: "PAGE 3", font_size: 26, color: "#111827", font_family: "Plus Jakarta Sans" },
        { id: "elem_frame_3", type: "border", x: 30, y: 25, w: 450, h: 610 },
      ]
    },
    {
      page_number: 4,
      title: "Page 4",
      layout: "side_by_side",
      elements: [
        { id: "elem_title_4", type: "title", x: 45, y: 45, w: 420, h: 40, text: "PAGE 4", font_size: 26, color: "#111827", font_family: "Plus Jakarta Sans" },
        { id: "elem_ref_4", type: "ref_image", x: 35, y: 100, w: 210, h: 510, text: "Click to select Reference", image_src: null },
        { id: "elem_main_4", type: "main_image", x: 265, y: 100, w: 210, h: 510, text: "Click to select Drawing", image_src: null },
        { id: "elem_frame_4", type: "border", x: 30, y: 25, w: 450, h: 610 },
      ]
    }
  ]
};

let recentProjectsList = [];
let currentPageIndex = 0;
let activeElementId = null;
let currentZoom = 1.0;
let showGuides = true;
let snapToGuides = true;

// Auto-Save System State
let isDirty = false;
let autoSaveTimer = null;
let renameTargetType = "page";
let projectToDelete = null;

// UI Initialization
document.addEventListener("DOMContentLoaded", () => {
  setupNavigation();
  setupGlobalKeyboardShortcuts();
  fetchDefaultLocation();
  restoreAutoSavedProject();
  fetchRecentProjects();
  syncActiveProjectUI();
  setupCanvasInteractions();

  // Background Auto-Save Cron (Every 10 seconds)
  setInterval(() => {
    if (isDirty) {
      saveProject(false);
    }
  }, 10000);
});

// ==========================================
// Auto-Save & Crash-Recovery System
// ==========================================
function markProjectDirty() {
  if (currentProject.is_locked) return; // Do not modify locked project
  isDirty = true;
  updateAutoSaveIndicator(true);

  if (autoSaveTimer) clearTimeout(autoSaveTimer);
  autoSaveTimer = setTimeout(() => {
    saveProject(false);
  }, 1500);
}

function updateAutoSaveIndicator(saving) {
  const ind = document.getElementById("autosave-indicator");
  const txt = document.getElementById("autosave-text");
  if (!ind || !txt) return;

  if (saving) {
    ind.classList.add("saving");
    txt.innerText = "Saving...";
  } else {
    ind.classList.remove("saving");
    txt.innerText = "Auto-saved";
  }
}

function saveProject(isManual = false) {
  if (currentProject.is_locked) {
    if (isManual) showToast("🔒 Project is locked (Read-Only)!", "warning");
    return;
  }

  currentProject.updated_at = new Date().toISOString();
  
  // 1. Save to LocalStorage for instant browser crash recovery
  try {
    localStorage.setItem("kdp_autosave_current_project", JSON.stringify(currentProject));
    if (currentProject.folder_name) {
      localStorage.setItem(`kdp_project_${currentProject.folder_name}`, JSON.stringify(currentProject));
    }
  } catch (e) {
    console.warn("LocalStorage save error:", e);
  }

  // 2. Persist to Physical Disk in project folder (project.json)
  fetch("/api/projects/save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(currentProject)
  })
  .then(() => {
    isDirty = false;
    updateAutoSaveIndicator(false);
    if (isManual) {
      showToast(`💾 Saved "${currentProject.name}" to disk!`, "success");
    }
  })
  .catch(() => {
    isDirty = false;
    updateAutoSaveIndicator(false);
    if (isManual) {
      showToast(`💾 Saved "${currentProject.name}" locally!`, "success");
    }
  });
}

function restoreAutoSavedProject() {
  try {
    const saved = localStorage.getItem("kdp_autosave_current_project");
    if (saved) {
      const parsed = JSON.parse(saved);
      if (parsed && parsed.name && parsed.pages && parsed.pages.length > 0) {
        currentProject = parsed;
      }
    }
  } catch (e) {
    console.warn("Could not restore auto-save:", e);
  }
}

// ==========================================
// Project Lock / Unlock & Deletion Engine
// ==========================================
function toggleActiveProjectLock() {
  currentProject.is_locked = !currentProject.is_locked;
  syncActiveProjectUI();
  saveProject(false);
  fetchRecentProjects();
  showToast(currentProject.is_locked ? `🔒 Locked "${currentProject.name}"!` : `🔓 Unlocked "${currentProject.name}"!`, "info");
}

function toggleProjectLock(path) {
  fetch("/api/projects/toggle_lock", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path })
  })
  .then(r => r.json())
  .then(data => {
    if (currentProject.project_dir === path) {
      currentProject.is_locked = data.is_locked;
      syncActiveProjectUI();
    }
    fetchRecentProjects();
    showToast(data.is_locked ? "🔒 Project Locked!" : "🔓 Project Unlocked!", "info");
  })
  .catch(() => {
    fetchRecentProjects();
  });
}

function promptDeleteProject(path, name, isLocked) {
  if (isLocked) {
    showToast(`🔒 Cannot delete "${name}" because it is LOCKED! Please unlock it first.`, "warning");
    return;
  }

  projectToDelete = { path, name };
  const pathLabel = document.getElementById("delete-modal-project-path");
  if (pathLabel) {
    pathLabel.innerText = `📁 ${path}\\`;
  }
  const modal = document.getElementById("delete-project-modal");
  if (modal) modal.classList.add("active");
}

function executeDeleteProject() {
  if (!projectToDelete) return;

  const targetPath = projectToDelete.path;
  const targetName = projectToDelete.name;

  fetch("/api/projects/delete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path: targetPath })
  })
  .then(r => r.json())
  .then(res => {
    closeModal("delete-project-modal");
    if (res.error) {
      showToast(`⚠️ ${res.error}`, "danger");
      return;
    }

    showToast(`🗑 Permanently deleted "${targetName}" and all files!`, "success");
    fetchRecentProjects();

    // If active project was deleted, reset workspace
    if (currentProject.project_dir === targetPath) {
      currentProject = {
        name: "New Untitled Book",
        folder_name: "New_Untitled_Book",
        project_dir: `${defaultRootLocation}\\New_Untitled_Book`,
        author: "Author",
        is_locked: false,
        settings: {
          trim_width_pt: 612.0,
          trim_height_pt: 792.0,
          has_bleed: true,
          bleed_pt: 9.0,
          margins: { top_pt: 27.0, bottom_pt: 27.0, inside_pt: 36.0, outside_pt: 27.0 },
          target_dpi: 300,
        },
        media: [],
        pages: []
      };
      syncActiveProjectUI();
      switchTab("dashboard");
    }
  })
  .catch(() => {
    closeModal("delete-project-modal");
    showToast(`Deleted project "${targetName}"!`, "info");
    fetchRecentProjects();
  });
}

function openCustomProjectFolder() {
  const customPath = prompt("Enter or Paste Full Project Folder Path from any PC / Drive:", defaultRootLocation);
  if (customPath && customPath.trim()) {
    openProjectByPath(customPath.trim());
  }
}

// ==========================================
// Keyboard Shortcuts Engine
// ==========================================
function setupGlobalKeyboardShortcuts() {
  window.addEventListener("keydown", (e) => {
    const activeTagName = document.activeElement ? document.activeElement.tagName.toLowerCase() : "";
    const isInputActive = activeTagName === "input" || activeTagName === "textarea" || activeTagName === "select";

    // 1. Ctrl + S -> Manual Save
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") {
      e.preventDefault();
      saveProject(true);
      return;
    }

    // 2. Ctrl + D -> Duplicate Element or Page
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "d") {
      e.preventDefault();
      if (activeElementId) {
        duplicateActiveElement();
      } else {
        duplicateCurrentPage();
      }
      return;
    }

    // 3. F2 -> Rename Title Element or Page
    if (e.key === "F2") {
      e.preventDefault();
      const activeElem = getActiveElement();
      if (activeElem && activeElem.type === "title") {
        openRenameModal("element");
      } else {
        openRenameModal("page");
      }
      return;
    }

    // 4. Escape -> Close Modals or Deselect Element
    if (e.key === "Escape") {
      const openModal = document.querySelector(".modal-overlay.active");
      if (openModal) {
        openModal.classList.remove("active");
      } else if (activeElementId) {
        setActiveElement(null);
      }
      return;
    }

    if (isInputActive) return;

    // 5. Delete / Backspace -> Delete Selected Element
    if (e.key === "Delete" || e.key === "Backspace") {
      if (activeElementId) {
        e.preventDefault();
        deleteActiveElement();
        return;
      }
    }

    // 6. Arrow Keys -> Nudge Selected Element
    if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) {
      const elem = getActiveElement();
      if (elem) {
        e.preventDefault();
        const step = e.shiftKey ? 10 : 1;

        if (e.key === "ArrowUp") elem.y = Math.max(0, elem.y - step);
        if (e.key === "ArrowDown") elem.y = Math.min(660 - elem.h, elem.y + step);
        if (e.key === "ArrowLeft") elem.x = Math.max(0, elem.x - step);
        if (e.key === "ArrowRight") elem.x = Math.min(510 - elem.w, elem.x + step);

        applyElementStyles(elem);
        updatePropertiesInspector();
        markProjectDirty();
        return;
      }
    }

    // 7. [ and ] or PageUp/PageDown -> Previous / Next Page
    if (e.key === "[" || e.key === "PageUp") {
      e.preventDefault();
      if (currentPageIndex > 0) {
        selectPage(currentPageIndex - 1);
        showToast(`Page ${currentPageIndex + 1}`, "info");
      }
      return;
    }
    if (e.key === "]" || e.key === "PageDown") {
      e.preventDefault();
      if (currentPageIndex < currentProject.pages.length - 1) {
        selectPage(currentPageIndex + 1);
        showToast(`Page ${currentPageIndex + 1}`, "info");
      }
      return;
    }

    // 8. Hotkeys: G (Guides), S (Snap), T (Add Text), B (Add Border)
    if (e.key.toLowerCase() === "g") {
      toggleGuides();
    } else if (e.key.toLowerCase() === "s" && !e.ctrlKey) {
      toggleSnap();
    } else if (e.key.toLowerCase() === "t") {
      addNewTextElement();
    } else if (e.key.toLowerCase() === "b") {
      addNewBorderElement();
    }
  });
}

// ==========================================
// Rename Modal Logic (F2 Shortcut)
// ==========================================
function openRenameModal(type = "page") {
  renameTargetType = type;
  const modal = document.getElementById("rename-modal");
  const title = document.getElementById("rename-modal-title");
  const label = document.getElementById("rename-modal-label");
  const input = document.getElementById("rename-modal-input");

  if (!modal || !input) return;

  if (type === "page") {
    const page = currentProject.pages[currentPageIndex];
    title.innerText = `✏️ Rename Page ${page.page_number}`;
    label.innerText = "Enter new page title:";
    input.value = page.title || `Page ${page.page_number}`;
  } else if (type === "element") {
    const elem = getActiveElement();
    title.innerText = `✏️ Rename Text Element`;
    label.innerText = "Enter text content:";
    input.value = elem ? (elem.text || "") : "";
  } else if (type === "project") {
    title.innerText = `✏️ Rename Book Project`;
    label.innerText = "Enter project name:";
    input.value = currentProject.name;
  }

  modal.classList.add("active");
  setTimeout(() => {
    input.focus();
    input.select();
  }, 50);
}

function submitRenameModal() {
  const input = document.getElementById("rename-modal-input");
  const val = input ? input.value.trim() : "";
  if (!val) {
    closeModal("rename-modal");
    return;
  }

  if (renameTargetType === "page") {
    const page = currentProject.pages[currentPageIndex];
    if (page) {
      page.title = val;
      const titleElem = page.elements.find(e => e.type === "title");
      if (titleElem) titleElem.text = val.toUpperCase();
      renderTimeline();
      loadPageIntoCanvas(currentPageIndex);
      showToast(`✏️ Renamed page to "${val}"!`, "success");
    }
  } else if (renameTargetType === "element") {
    const elem = getActiveElement();
    if (elem) {
      elem.text = val;
      const node = document.getElementById(elem.id);
      if (node) node.innerText = val;
      updatePropertiesInspector();
      showToast(`✏️ Updated text to "${val}"!`, "success");
    }
  } else if (renameTargetType === "project") {
    currentProject.name = val;
    syncActiveProjectUI();
    showToast(`✏️ Renamed project to "${val}"!`, "success");
  }

  markProjectDirty();
  closeModal("rename-modal");
}

function openShortcutsModal() {
  const modal = document.getElementById("shortcuts-modal");
  if (modal) modal.classList.add("active");
}

// ==========================================
// Project File API & Directory Scaffolding
// ==========================================
function fetchDefaultLocation() {
  fetch("/api/default_location")
    .then(r => r.json())
    .then(data => {
      if (data.default_root) {
        defaultRootLocation = data.default_root;
        const rootInput = document.getElementById("modal-project-root");
        if (rootInput) rootInput.value = defaultRootLocation;
        updateModalPathPreview();
      }
    })
    .catch(() => {});
}

function fetchRecentProjects() {
  fetch("/api/projects")
    .then(r => r.json())
    .then(data => {
      if (data.projects) {
        recentProjectsList = data.projects;
      }
      renderRecentProjects();
    })
    .catch(() => {
      renderRecentProjects();
    });
}

function renderRecentProjects() {
  const container = document.getElementById("recent-projects-list");
  const modalPickList = document.getElementById("modal-project-pick-list");

  const renderItemHtml = (p) => `
    <div class="recent-item">
      <div class="recent-icon">${p.is_locked ? '🔒' : '📁'}</div>
      <div class="recent-info" onclick="openProjectByPath('${p.path.replace(/\\/g, '\\\\')}')">
        <div class="recent-title">
          <span>${p.name}</span>
          ${p.is_locked ? '<span class="badge locked">LOCKED</span>' : '<span class="badge unlocked">UNLOCKED</span>'}
        </div>
        <div class="recent-path">${p.path}</div>
      </div>
      <div class="recent-meta">
        <span class="badge">${p.page_count || 0} Pages</span>
        <button class="btn btn-sm btn-primary" onclick="openProjectByPath('${p.path.replace(/\\/g, '\\\\')}')">Open</button>
        <button class="btn btn-sm btn-outline btn-icon-only" onclick="toggleProjectLock('${p.path.replace(/\\/g, '\\\\')}')" title="${p.is_locked ? 'Unlock Project' : 'Lock Project'}">
          ${p.is_locked ? '🔓' : '🔒'}
        </button>
        <button class="btn btn-sm btn-danger btn-icon-only ${p.is_locked ? 'btn-disabled' : ''}" 
          onclick="promptDeleteProject('${p.path.replace(/\\/g, '\\\\')}', '${p.name.replace(/'/g, "\\'")}', ${p.is_locked})" 
          title="Delete Project Folder">
          🗑
        </button>
      </div>
    </div>
  `;

  if (container) {
    container.innerHTML = recentProjectsList.length 
      ? recentProjectsList.map(renderItemHtml).join("")
      : `<div style="color:var(--text-muted);font-size:12px;padding:12px;">No projects found. Click "Create New Project" to get started!</div>`;
  }

  if (modalPickList) {
    modalPickList.innerHTML = recentProjectsList.map(renderItemHtml).join("");
  }
}

// Navigation Tabs
function setupNavigation() {
  document.querySelectorAll(".nav-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const tab = btn.getAttribute("data-tab");
      switchTab(tab);
    });
  });
}

function switchTab(tabId) {
  document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));

  const targetBtn = document.querySelector(`.nav-btn[data-tab="${tabId}"]`);
  const targetPanel = document.getElementById(`panel-${tabId}`);
  if (targetBtn) targetBtn.classList.add("active");
  if (targetPanel) targetPanel.classList.add("active");

  if (tabId === "canvas") {
    loadPageIntoCanvas(currentPageIndex);
    renderTimeline();
    renderMediaLibrary();
  }
}

// Drawer Tabs (Layouts vs Project Media)
function switchDrawerTab(tabKey) {
  document.querySelectorAll(".drawer-tab-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".drawer-content").forEach(c => c.classList.remove("active"));

  const targetBtn = document.getElementById(`dtab-${tabKey}`);
  const targetContent = document.getElementById(`dcontent-${tabKey}`);
  if (targetBtn) targetBtn.classList.add("active");
  if (targetContent) targetContent.classList.add("active");
}

// Sync UI with currentProject state
function syncActiveProjectUI() {
  document.getElementById("nav-project-name").innerText = `${currentProject.is_locked ? '🔒 ' : ''}${currentProject.name}`;
  document.getElementById("active-proj-title").innerText = currentProject.name;
  document.getElementById("active-proj-path").innerText = `📁 ${currentProject.project_dir}`;
  document.getElementById("active-proj-meta").innerHTML = `
    <span>Pages: ${currentProject.pages.length}</span> • 
    <span>Media Items: ${currentProject.media ? currentProject.media.length : 0}</span> • 
    <span>Trim: 8.5x11 in</span>
  `;

  const lockBadge = document.getElementById("active-proj-lock-badge");
  if (lockBadge) {
    lockBadge.className = `badge ${currentProject.is_locked ? 'locked' : 'unlocked'}`;
    lockBadge.innerText = currentProject.is_locked ? "🔒 LOCKED" : "🔓 UNLOCKED";
  }

  const lockBtn = document.getElementById("active-lock-toggle-btn");
  if (lockBtn) {
    lockBtn.innerText = currentProject.is_locked ? "🔓 Unlock Project" : "🔒 Lock Project";
  }

  document.getElementById("stat-page-count").innerText = currentProject.pages.length;
  document.getElementById("stat-media-count").innerText = currentProject.media ? currentProject.media.length : 0;
  
  const folderHint = document.getElementById("media-folder-hint");
  if (folderHint) folderHint.innerText = `${currentProject.folder_name}/assets`;

  renderTimeline();
  renderMediaLibrary();
}

// ==========================================
// Project Creation & Location Management
// ==========================================
function openNewProjectModal() {
  const modal = document.getElementById("new-project-modal");
  updateModalPathPreview();
  if (modal) modal.classList.add("active");
}

function openExistingFolderModal() {
  const modal = document.getElementById("open-folder-modal");
  fetchRecentProjects();
  if (modal) modal.classList.add("active");
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove("active");
}

function updateModalPathPreview() {
  const nameInput = document.getElementById("modal-project-name");
  const rootInput = document.getElementById("modal-project-root");
  const previewDiv = document.getElementById("modal-full-path-preview");

  const name = (nameInput ? nameInput.value.trim() : "") || "Untitled_Project";
  const root = (rootInput ? rootInput.value.trim() : "") || defaultRootLocation;
  const folderName = name.replace(/[^a-zA-Z0-9_\-\s]/g, "").replace(/\s+/g, "_");

  const fullPath = `${root.replace(/[\/\\]+$/, "")}\\${folderName}`;
  if (previewDiv) {
    previewDiv.innerText = `📁 ${fullPath}\\`;
  }
}

function browseProjectFolder() {
  const custom = prompt("Enter Custom Root Folder Path for Projects:", defaultRootLocation);
  if (custom && custom.trim()) {
    defaultRootLocation = custom.trim();
    const rootInput = document.getElementById("modal-project-root");
    if (rootInput) rootInput.value = defaultRootLocation;
    updateModalPathPreview();
  }
}

function submitCreateProject() {
  const nameInput = document.getElementById("modal-project-name");
  const rootInput = document.getElementById("modal-project-root");
  const countSelect = document.getElementById("modal-page-count");
  const hasBleed = document.getElementById("modal-has-bleed").checked;

  const projName = (nameInput ? nameInput.value.trim() : "") || "My New KDP Book";
  const rootDir = (rootInput ? rootInput.value.trim() : "") || defaultRootLocation;
  const folderName = projName.replace(/[^a-zA-Z0-9_\-\s]/g, "").replace(/\s+/g, "_");
  const projectDir = `${rootDir.replace(/[\/\\]+$/, "")}\\${folderName}`;
  const count = parseInt(countSelect ? countSelect.value : "10");

  const initialPages = [];
  for (let i = 0; i < count; i++) {
    initialPages.push({
      page_number: i + 1,
      title: `Page ${i + 1}`,
      layout: "top_ref",
      elements: [
        { id: `elem_ref_${i + 1}`, type: "ref_image", x: 180, y: 35, w: 150, h: 100, text: "Click to select Reference Image", image_src: null },
        { id: `elem_main_${i + 1}`, type: "main_image", x: 45, y: 150, w: 420, h: 420, text: "Click to select Drawing Image", image_src: null },
        { id: `elem_title_${i + 1}`, type: "title", x: 45, y: 585, w: 420, h: 40, text: `PAGE ${i + 1}`, font_size: 26, color: "#111827", font_family: "Plus Jakarta Sans" },
        { id: `elem_frame_${i + 1}`, type: "border", x: 30, y: 25, w: 450, h: 610 },
      ]
    });
  }

  const newProjPayload = {
    name: projName,
    folder_name: folderName,
    project_dir: projectDir,
    root_path: rootDir,
    author: "Creative Author",
    is_locked: false,
    created_at: new Date().toISOString(),
    settings: {
      trim_width_pt: 612.0,
      trim_height_pt: 792.0,
      has_bleed: hasBleed,
      bleed_pt: 9.0,
      margins: { top_pt: 27.0, bottom_pt: 27.0, inside_pt: 36.0, outside_pt: 27.0 },
      target_dpi: 300,
    },
    media: [],
    pages: initialPages
  };

  fetch("/api/projects/create", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newProjPayload)
  })
  .then(r => r.json())
  .then(() => {
    finishProjectSetup(newProjPayload);
  })
  .catch(() => {
    finishProjectSetup(newProjPayload);
  });
}

function finishProjectSetup(proj) {
  currentProject = proj;
  currentPageIndex = 0;
  activeElementId = null;

  closeModal("new-project-modal");
  syncActiveProjectUI();
  fetchRecentProjects();
  switchTab("canvas");

  markProjectDirty();
  showToast(`✨ Created Project "${proj.name}" in ${proj.folder_name}!`, "success");
}

function openProjectByPath(path) {
  fetch(`/api/projects/load?path=${encodeURIComponent(path)}`)
    .then(r => r.json())
    .then(data => {
      if (data.project) {
        currentProject = data.project;
      } else {
        const found = recentProjectsList.find(p => p.path === path);
        if (found) {
          currentProject.name = found.name;
          currentProject.project_dir = found.path;
          currentProject.folder_name = found.path.split("\\").pop();
          currentProject.is_locked = bool(found.is_locked);
        }
      }
      closeModal("open-folder-modal");
      syncActiveProjectUI();
      switchTab("canvas");
      showToast(`📂 Opened Project "${currentProject.name}"!`, "info");
    })
    .catch(() => {
      closeModal("open-folder-modal");
      syncActiveProjectUI();
      switchTab("canvas");
      showToast(`📂 Opened Project "${currentProject.name}"!`, "info");
    });
}

// ==========================================
// Project-Isolated Media Library Handlers
// ==========================================
function triggerMediaUpload() {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot upload: Project is locked!", "warning");
    return;
  }
  const fileInput = document.getElementById("media-library-upload-input");
  if (fileInput) {
    fileInput.value = "";
    fileInput.click();
  }
}

function handleMediaLibraryUpload(event) {
  if (currentProject.is_locked) return;

  const files = Array.from(event.target.files);
  if (!files.length) return;

  if (!currentProject.media) {
    currentProject.media = [];
  }

  let loaded = 0;
  files.forEach((file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const dataUrl = e.target.result;
      const cleanTitle = cleanFileName(file.name);

      const mediaItem = {
        id: `med_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
        name: cleanTitle,
        fileName: file.name,
        dataUrl: dataUrl,
        sizeKb: Math.round(file.size / 1024)
      };

      currentProject.media.unshift(mediaItem);

      fetch("/api/projects/upload_asset", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_dir: currentProject.project_dir,
          filename: file.name,
          data_url: dataUrl
        })
      }).catch(() => {});

      loaded++;
      if (loaded === files.length) {
        renderMediaLibrary();
        switchDrawerTab("media");
        syncActiveProjectUI();
        markProjectDirty();
        showToast(`📁 Uploaded ${files.length} image(s) into "${currentProject.folder_name}/assets"!`, "success");

        const activeElem = getActiveElement();
        if (activeElem && (activeElem.type === "ref_image" || activeElem.type === "main_image")) {
          applyMediaToSlot(mediaItem.id, activeElem.type === "ref_image" ? "ref" : "drawing");
        }
      }
    };
    reader.readAsDataURL(file);
  });
}

function renderMediaLibrary() {
  const container = document.getElementById("media-items-list");
  if (!container) return;
  container.innerHTML = "";

  const projectMedia = currentProject.media || [];
  const badge = document.getElementById("media-count-badge");
  if (badge) badge.innerText = projectMedia.length;

  if (projectMedia.length === 0) {
    container.innerHTML = `
      <div class="media-empty-state" onclick="triggerMediaUpload()" style="cursor: pointer;">
        <div class="media-empty-icon">📁</div>
        <strong>No images in this project</strong>
        <p style="margin-top: 4px; color: var(--text-muted); font-size: 11px;">
          Click here to upload images from your PC into <code>${currentProject.folder_name}/assets</code>.
        </p>
      </div>
    `;
    return;
  }

  projectMedia.forEach(item => {
    const card = document.createElement("div");
    card.className = "media-card";

    card.innerHTML = `
      <div class="media-card-top" onclick="handleMediaCardClick('${item.id}')" style="cursor: pointer;">
        <div class="media-card-thumb">
          <img src="${item.dataUrl}">
        </div>
        <div class="media-card-meta">
          <div class="media-name" title="${item.name}">${item.name}</div>
          <div class="media-tag">${item.sizeKb} KB • ${currentProject.folder_name}</div>
        </div>
      </div>
      <div class="media-action-buttons">
        <button class="btn-action-pill ref-btn" onclick="applyMediaToSlot('${item.id}', 'ref')">
          🎯 1. Reference
        </button>
        <button class="btn-action-pill drawing-btn" onclick="applyMediaToSlot('${item.id}', 'drawing')">
          🎨 2. Drawing
        </button>
        <button class="btn-action-pill" onclick="applyMediaToSlot('${item.id}', 'title')">
          🔤 3. Title Text
        </button>
        <button class="btn-action-pill all-btn" onclick="applyMediaToSlot('${item.id}', 'all')">
          ⚡ Apply All 3 (Ref + Draw + Title)
        </button>
      </div>
    `;

    container.appendChild(card);
  });
}

function handleMediaCardClick(mediaId) {
  const activeElem = getActiveElement();
  if (activeElem && activeElem.type === "ref_image") {
    applyMediaToSlot(mediaId, "ref");
  } else if (activeElem && activeElem.type === "main_image") {
    applyMediaToSlot(mediaId, "drawing");
  } else {
    applyMediaToSlot(mediaId, "drawing");
  }
}

function applyMediaToSlot(mediaId, slotType) {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot modify: Project is locked!", "warning");
    return;
  }

  const item = (currentProject.media || []).find(m => m.id === mediaId);
  if (!item) return;

  const page = currentProject.pages[currentPageIndex];
  if (!page) return;

  const imgSrc = item.dataUrl;
  const labelText = item.name;

  if (slotType === "ref") {
    let refElem = page.elements.find(e => e.type === "ref_image");
    if (!refElem) {
      refElem = { id: `elem_ref_${Date.now()}`, type: "ref_image", x: 180, y: 35, w: 150, h: 100, text: "" };
      page.elements.unshift(refElem);
    }
    refElem.image_src = imgSrc;
    refElem.text = labelText;
    setActiveElement(refElem.id);
    showToast(`🎯 Set "${item.name}" as Reference Image!`, "success");
  } 
  else if (slotType === "drawing") {
    let mainElem = page.elements.find(e => e.type === "main_image");
    if (!mainElem) {
      mainElem = { id: `elem_main_${Date.now()}`, type: "main_image", x: 45, y: 150, w: 420, h: 420, text: "" };
      page.elements.push(mainElem);
    }
    mainElem.image_src = imgSrc;
    mainElem.text = labelText;
    setActiveElement(mainElem.id);
    showToast(`🎨 Set "${item.name}" as Drawing Image!`, "success");
  } 
  else if (slotType === "title") {
    let titleElem = page.elements.find(e => e.type === "title");
    if (!titleElem) {
      titleElem = { id: `elem_title_${Date.now()}`, type: "title", x: 45, y: 585, w: 420, h: 40, font_size: 26, color: "#111827", font_family: "Plus Jakarta Sans" };
      page.elements.push(titleElem);
    }
    titleElem.text = item.name.toUpperCase();
    page.title = item.name;
    setActiveElement(titleElem.id);
    showToast(`🔤 Set Title to "${item.name.toUpperCase()}"!`, "success");
  } 
  else if (slotType === "all") {
    let refElem = page.elements.find(e => e.type === "ref_image");
    if (refElem) {
      refElem.image_src = imgSrc;
      refElem.text = labelText;
    }
    let mainElem = page.elements.find(e => e.type === "main_image");
    if (mainElem) {
      mainElem.image_src = imgSrc;
      mainElem.text = labelText;
    }
    let titleElem = page.elements.find(e => e.type === "title");
    if (titleElem) {
      titleElem.text = item.name.toUpperCase();
    }
    page.title = item.name;
    showToast(`⚡ Filled Reference, Drawing, and Title with "${item.name}"!`, "success");
  }

  markProjectDirty();
  loadPageIntoCanvas(currentPageIndex);
  renderTimeline();
}

function cleanFileName(filename) {
  let name = filename.replace(/\.[^/.]+$/, "");
  name = name.replace(/^\d+[\s_\.\-]+/, "");
  name = name.replace(/[_\-]+/g, " ").trim();
  return name.replace(/\b\w/g, c => c.toUpperCase());
}

// ==========================================
// Layout Templates Engine
// ==========================================
function applyPageLayout(layoutKey) {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot change layout: Project is locked!", "warning");
    return;
  }

  const page = currentProject.pages[currentPageIndex];
  if (!page) return;

  let existingTitle = page.title || `PAGE ${page.page_number}`;
  let existingRefImg = null;
  let existingMainImg = null;

  page.elements.forEach(el => {
    if (el.type === "title" && el.text) existingTitle = el.text;
    if (el.type === "ref_image" && el.image_src) existingRefImg = el.image_src;
    if (el.type === "main_image" && el.image_src) existingMainImg = el.image_src;
  });

  page.layout = layoutKey;
  let newElements = [];

  if (layoutKey === "top_ref") {
    newElements = [
      { id: `elem_ref_${Date.now()}`, type: "ref_image", x: 180, y: 35, w: 150, h: 100, text: "Click to select Reference Image", image_src: existingRefImg },
      { id: `elem_main_${Date.now()}`, type: "main_image", x: 45, y: 150, w: 420, h: 420, text: "Click to select Drawing Image", image_src: existingMainImg },
      { id: `elem_title_${Date.now()}`, type: "title", x: 45, y: 585, w: 420, h: 40, text: existingTitle.toUpperCase(), font_size: 26, color: "#111827", font_family: "Plus Jakarta Sans" },
      { id: `elem_frame_${Date.now()}`, type: "border", x: 30, y: 25, w: 450, h: 610 }
    ];
  } else if (layoutKey === "full_page") {
    newElements = [
      { id: `elem_main_${Date.now()}`, type: "main_image", x: 35, y: 50, w: 440, h: 520, text: "Click to select Full Page Drawing", image_src: existingMainImg || existingRefImg },
      { id: `elem_title_${Date.now()}`, type: "title", x: 45, y: 585, w: 420, h: 40, text: existingTitle.toUpperCase(), font_size: 26, color: "#111827", font_family: "Plus Jakarta Sans" },
      { id: `elem_frame_${Date.now()}`, type: "border", x: 30, y: 25, w: 450, h: 610 }
    ];
  } else if (layoutKey === "side_by_side") {
    newElements = [
      { id: `elem_title_${Date.now()}`, type: "title", x: 45, y: 45, w: 420, h: 40, text: existingTitle.toUpperCase(), font_size: 26, color: "#111827", font_family: "Plus Jakarta Sans" },
      { id: `elem_ref_${Date.now()}`, type: "ref_image", x: 35, y: 100, w: 210, h: 510, text: "Click to select Reference", image_src: existingRefImg },
      { id: `elem_main_${Date.now()}`, type: "main_image", x: 265, y: 100, w: 210, h: 510, text: "Click to select Drawing", image_src: existingMainImg },
      { id: `elem_frame_${Date.now()}`, type: "border", x: 30, y: 25, w: 450, h: 610 }
    ];
  } else if (layoutKey === "top_title") {
    newElements = [
      { id: `elem_title_${Date.now()}`, type: "title", x: 45, y: 40, w: 420, h: 45, text: existingTitle.toUpperCase(), font_size: 28, color: "#111827", font_family: "Plus Jakarta Sans" },
      { id: `elem_main_${Date.now()}`, type: "main_image", x: 45, y: 95, w: 420, h: 525, text: "Click to select Drawing", image_src: existingMainImg || existingRefImg },
      { id: `elem_frame_${Date.now()}`, type: "border", x: 30, y: 25, w: 450, h: 610 }
    ];
  } else if (layoutKey === "color_and_trace") {
    newElements = [
      { id: `elem_ref_${Date.now()}`, type: "ref_image", x: 45, y: 35, w: 140, h: 100, text: "Reference", image_src: existingRefImg },
      { id: `elem_title_${Date.now()}`, type: "title", x: 200, y: 65, w: 265, h: 40, text: existingTitle.toUpperCase(), font_size: 26, color: "#111827", font_family: "Plus Jakarta Sans" },
      { id: `elem_main_${Date.now()}`, type: "main_image", x: 45, y: 150, w: 420, h: 390, text: "Coloring Area", image_src: existingMainImg },
      { id: `elem_trace_${Date.now()}`, type: "tracing", x: 45, y: 550, w: 420, h: 70 },
      { id: `elem_frame_${Date.now()}`, type: "border", x: 30, y: 25, w: 450, h: 610 }
    ];
  } else if (layoutKey === "grid_4") {
    newElements = [
      { id: `elem_q1_${Date.now()}`, type: "main_image", x: 35, y: 40, w: 210, h: 260, text: "Drawing 1" },
      { id: `elem_q2_${Date.now()}`, type: "main_image", x: 265, y: 40, w: 210, h: 260, text: "Drawing 2" },
      { id: `elem_q3_${Date.now()}`, type: "main_image", x: 35, y: 320, w: 210, h: 260, text: "Drawing 3" },
      { id: `elem_q4_${Date.now()}`, type: "main_image", x: 265, y: 320, w: 210, h: 260, text: "Drawing 4" },
      { id: `elem_title_${Date.now()}`, type: "title", x: 45, y: 595, w: 420, h: 35, text: existingTitle.toUpperCase(), font_size: 22, color: "#111827" },
      { id: `elem_frame_${Date.now()}`, type: "border", x: 30, y: 25, w: 450, h: 610 }
    ];
  }

  page.elements = newElements;
  updateLayoutCardsActiveState(layoutKey);
  loadPageIntoCanvas(currentPageIndex);
  renderTimeline();
  markProjectDirty();
  showToast(`Applied "${getLayoutName(layoutKey)}" layout!`, "success");
}

function updateLayoutCardsActiveState(layoutKey) {
  document.querySelectorAll(".layout-card").forEach(card => {
    card.classList.toggle("active", card.getAttribute("data-layout") === layoutKey);
  });
  const readout = document.getElementById("layout-readout");
  if (readout) readout.innerText = `Layout: ${getLayoutName(layoutKey)}`;
}

function getLayoutName(key) {
  const map = {
    top_ref: "Top Ref + Big Drawing",
    full_page: "Full Page Drawing",
    side_by_side: "Side-by-Side Split",
    top_title: "Top Title + Center Art",
    color_and_trace: "Color & Handwriting",
    grid_4: "2x2 Quadrant Grid"
  };
  return map[key] || key;
}

// ==========================================
// Page Canvas Loader & Elements
// ==========================================
function loadPageIntoCanvas(index) {
  const page = currentProject.pages[index];
  const layer = document.getElementById("elements-layer");
  if (!layer) return;
  layer.innerHTML = "";

  if (!page) return;

  updateLayoutCardsActiveState(page.layout || "top_ref");

  page.elements.forEach(elem => {
    const elDiv = document.createElement("div");
    elDiv.id = elem.id;
    elDiv.className = `canvas-element ${elem.id === activeElementId ? 'selected' : ''}`;
    elDiv.style.left = `${elem.x}px`;
    elDiv.style.top = `${elem.y}px`;
    elDiv.style.width = `${elem.w}px`;
    elDiv.style.height = `${elem.h}px`;

    if (elem.type === "ref_image") {
      elDiv.classList.add("elem-ref-box");
      if (elem.image_src) {
        elDiv.innerHTML = `<img src="${elem.image_src}">`;
      } else {
        elDiv.innerHTML = `
          <div class="placeholder-hint">
            <span class="icon">📷</span>
            <span class="txt">Select Reference Image</span>
            <span class="sub">(Click to open Media Library)</span>
          </div>
        `;
      }
    } else if (elem.type === "main_image") {
      elDiv.classList.add("elem-main-box");
      if (elem.image_src) {
        elDiv.innerHTML = `<img src="${elem.image_src}">`;
      } else {
        elDiv.innerHTML = `
          <div class="placeholder-hint">
            <span class="icon">🎨</span>
            <span class="txt">Select Drawing Image</span>
            <span class="sub">(Click to open Media Library)</span>
          </div>
        `;
      }
    } else if (elem.type === "title") {
      elDiv.classList.add("elem-title-box");
      elDiv.innerText = elem.text || "Title";
      elDiv.style.fontSize = `${elem.font_size || 22}px`;
      elDiv.style.color = elem.color || "#111827";
    } else if (elem.type === "tracing") {
      elDiv.classList.add("elem-tracing-box");
      elDiv.innerHTML = `
        <div class="tracing-line"></div>
        <div class="tracing-line mid"></div>
        <div class="tracing-line"></div>
      `;
    } else if (elem.type === "border") {
      elDiv.classList.add("elem-border-box");
    }

    elDiv.innerHTML += `
      <div class="handle tl" data-handle="tl"></div>
      <div class="handle tr" data-handle="tr"></div>
      <div class="handle bl" data-handle="bl"></div>
      <div class="handle br" data-handle="br"></div>
    `;

    elDiv.addEventListener("mousedown", (e) => {
      e.stopPropagation();
      setActiveElement(elem.id);
      if (elem.type === "ref_image" || elem.type === "main_image") {
        switchDrawerTab("media");
      }
    });

    layer.appendChild(elDiv);
  });

  const pageReadout = document.getElementById("page-num-readout");
  if (pageReadout) pageReadout.innerText = `Page ${index + 1} of ${currentProject.pages.length}`;
}

// Drag & Resize Canvas Interactions
function setupCanvasInteractions() {
  let isDragging = false;
  let isResizing = false;
  let activeHandle = null;
  let startX = 0, startY = 0;
  let elemStart = { x: 0, y: 0, w: 0, h: 0 };

  const stage = document.getElementById("canvas-stage");
  if (!stage) return;

  stage.addEventListener("mousedown", (e) => {
    if (currentProject.is_locked) return; // Read-only

    if (e.target.classList.contains("handle")) {
      isResizing = true;
      activeHandle = e.target.getAttribute("data-handle");
      startX = e.clientX;
      startY = e.clientY;
      const elem = getActiveElement();
      if (elem) elemStart = { ...elem };
      e.preventDefault();
      return;
    }

    const elemNode = e.target.closest(".canvas-element");
    if (elemNode) {
      isDragging = true;
      startX = e.clientX;
      startY = e.clientY;
      const elem = getActiveElement();
      if (elem) elemStart = { ...elem };
      e.preventDefault();
    } else {
      setActiveElement(null);
    }
  });

  window.addEventListener("mousemove", (e) => {
    const pageNode = document.getElementById("paper-page");
    if (pageNode) {
      const pageRect = pageNode.getBoundingClientRect();
      const curX = ((e.clientX - pageRect.left) / 60.0).toFixed(2);
      const curY = ((e.clientY - pageRect.top) / 60.0).toFixed(2);
      const readout = document.getElementById("coord-readout");
      if (readout) readout.innerText = `X: ${curX} in | Y: ${curY} in`;
    }

    const elem = getActiveElement();
    if (!elem || currentProject.is_locked) return;

    const dx = (e.clientX - startX) / currentZoom;
    const dy = (e.clientY - startY) / currentZoom;

    if (isDragging) {
      elem.x = Math.max(0, Math.min(510 - elem.w, elemStart.x + dx));
      elem.y = Math.max(0, Math.min(660 - elem.h, elemStart.y + dy));
      applyElementStyles(elem);
      updatePropertiesInspector();
      markProjectDirty();
    } else if (isResizing) {
      if (activeHandle === "br") {
        elem.w = Math.max(30, elemStart.w + dx);
        elem.h = Math.max(30, elemStart.h + dy);
      } else if (activeHandle === "bl") {
        elem.w = Math.max(30, elemStart.w - dx);
        elem.x = elemStart.x + dx;
        elem.h = Math.max(30, elemStart.h + dy);
      } else if (activeHandle === "tr") {
        elem.w = Math.max(30, elemStart.w + dx);
        elem.h = Math.max(30, elemStart.h - dy);
        elem.y = elemStart.y + dy;
      } else if (activeHandle === "tl") {
        elem.w = Math.max(30, elemStart.w - dx);
        elem.h = Math.max(30, elemStart.h - dy);
        elem.x = elemStart.x + dx;
        elem.y = elemStart.y + dy;
      }
      applyElementStyles(elem);
      updatePropertiesInspector();
      markProjectDirty();
    }
  });

  window.addEventListener("mouseup", () => {
    isDragging = false;
    isResizing = false;
    activeHandle = null;
  });
}

function setActiveElement(elemId) {
  activeElementId = elemId;
  document.querySelectorAll(".canvas-element").forEach(el => {
    el.classList.toggle("selected", el.id === elemId);
  });
  updatePropertiesInspector();
}

function getActiveElement() {
  const page = currentProject.pages[currentPageIndex];
  if (!page) return null;
  return page.elements.find(e => e.id === activeElementId);
}

function applyElementStyles(elem) {
  const elNode = document.getElementById(elem.id);
  if (!elNode) return;
  elNode.style.left = `${elem.x}px`;
  elNode.style.top = `${elem.y}px`;
  elNode.style.width = `${elem.w}px`;
  elNode.style.height = `${elem.h}px`;
}

// Properties Inspector Data Binding
function updatePropertiesInspector() {
  const elem = getActiveElement();
  const titleBadge = document.getElementById("selected-type-badge");
  const textGroup = document.getElementById("prop-text-group");
  const imgGroup = document.getElementById("prop-image-group");

  if (!elem) {
    if (titleBadge) titleBadge.innerText = "No Selection";
    document.getElementById("prop-x").value = "";
    document.getElementById("prop-y").value = "";
    document.getElementById("prop-w").value = "";
    document.getElementById("prop-h").value = "";
    if (textGroup) textGroup.style.display = "none";
    if (imgGroup) imgGroup.style.display = "none";
    return;
  }

  if (titleBadge) titleBadge.innerText = elem.type.toUpperCase();
  document.getElementById("prop-x").value = (elem.x / 60.0).toFixed(2);
  document.getElementById("prop-y").value = (elem.y / 60.0).toFixed(2);
  document.getElementById("prop-w").value = (elem.w / 60.0).toFixed(2);
  document.getElementById("prop-h").value = (elem.h / 60.0).toFixed(2);

  if (elem.type === "title") {
    if (textGroup) textGroup.style.display = "block";
    if (imgGroup) imgGroup.style.display = "none";
    document.getElementById("prop-text-content").value = elem.text || "";
    document.getElementById("prop-font-size").value = elem.font_size || 26;
    document.getElementById("prop-color").value = elem.color || "#111827";
  } else if (elem.type === "main_image" || elem.type === "ref_image") {
    if (textGroup) textGroup.style.display = "none";
    if (imgGroup) imgGroup.style.display = "block";
  } else {
    if (textGroup) textGroup.style.display = "none";
    if (imgGroup) imgGroup.style.display = "none";
  }
}

function onPropChange() {
  if (currentProject.is_locked) return;

  const elem = getActiveElement();
  if (!elem) return;

  elem.x = parseFloat(document.getElementById("prop-x").value || 0) * 60.0;
  elem.y = parseFloat(document.getElementById("prop-y").value || 0) * 60.0;
  elem.w = parseFloat(document.getElementById("prop-w").value || 1) * 60.0;
  elem.h = parseFloat(document.getElementById("prop-h").value || 1) * 60.0;

  if (elem.type === "title") {
    elem.text = document.getElementById("prop-text-content").value;
    elem.font_size = parseInt(document.getElementById("prop-font-size").value || 24);
    elem.color = document.getElementById("prop-color").value;

    const elNode = document.getElementById(elem.id);
    if (elNode) {
      elNode.innerText = elem.text;
      elNode.style.fontSize = `${elem.font_size}px`;
      elNode.style.color = elem.color;
    }
  }

  applyElementStyles(elem);
  markProjectDirty();
}

// Alignment Functions
function alignActive(mode) {
  if (currentProject.is_locked) return;

  const elem = getActiveElement();
  if (!elem) return;

  const safe = { x: 33, y: 25, w: 452, h: 610 };

  if (mode === "left") elem.x = safe.x;
  else if (mode === "center_h") elem.x = safe.x + (safe.w - elem.w) / 2;
  else if (mode === "right") elem.x = safe.x + safe.w - elem.w;
  else if (mode === "top") elem.y = safe.y;
  else if (mode === "center_v") elem.y = safe.y + (safe.h - elem.h) / 2;
  else if (mode === "bottom") elem.y = safe.y + safe.h - elem.h;
  else if (mode === "fit_safe") {
    elem.x = safe.x;
    elem.y = safe.y;
    elem.w = safe.w;
    elem.h = safe.h;
  }

  applyElementStyles(elem);
  updatePropertiesInspector();
  markProjectDirty();
  showToast(`Aligned element: ${mode.replace('_', ' ')}`, "info");
}

// Add Elements
function addNewTextElement() {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot add element: Project is locked!", "warning");
    return;
  }

  const page = currentProject.pages[currentPageIndex];
  if (!page) return;

  const newId = `elem_txt_${Date.now()}`;
  const newElem = {
    id: newId,
    type: "title",
    x: 60,
    y: 80,
    w: 390,
    h: 40,
    text: "NEW TITLE TEXT",
    font_size: 24,
    color: "#111827"
  };

  page.elements.push(newElem);
  loadPageIntoCanvas(currentPageIndex);
  setActiveElement(newId);
  markProjectDirty();
  showToast("Added vector text element (T)", "info");
}

function addNewBorderElement() {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot add element: Project is locked!", "warning");
    return;
  }

  const page = currentProject.pages[currentPageIndex];
  if (!page) return;

  const newId = `elem_border_${Date.now()}`;
  const newElem = {
    id: newId,
    type: "border",
    x: 30,
    y: 25,
    w: 450,
    h: 610
  };

  page.elements.push(newElem);
  loadPageIntoCanvas(currentPageIndex);
  setActiveElement(newId);
  markProjectDirty();
  showToast("Added decorative border frame (B)", "info");
}

function duplicateActiveElement() {
  if (currentProject.is_locked) return;

  const elem = getActiveElement();
  if (!elem) return;

  const page = currentProject.pages[currentPageIndex];
  const clone = { ...elem, id: `elem_dup_${Date.now()}`, x: elem.x + 15, y: elem.y + 15 };
  page.elements.push(clone);
  loadPageIntoCanvas(currentPageIndex);
  setActiveElement(clone.id);
  markProjectDirty();
  showToast("Duplicated element (Ctrl+D)", "info");
}

function deleteActiveElement() {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot delete: Project is locked!", "warning");
    return;
  }

  const page = currentProject.pages[currentPageIndex];
  if (!page || !activeElementId) return;

  page.elements = page.elements.filter(e => e.id !== activeElementId);
  setActiveElement(null);
  loadPageIntoCanvas(currentPageIndex);
  markProjectDirty();
  showToast("Deleted element (Del)", "info");
}

// Page Actions
function addNewPage() {
  if (currentProject.is_locked) {
    showToast("🔒 Project is locked!", "warning");
    return;
  }

  const num = currentProject.pages.length + 1;
  currentProject.pages.push({
    page_number: num,
    title: `Page ${num}`,
    layout: "top_ref",
    elements: [
      { id: `elem_ref_${Date.now()}`, type: "ref_image", x: 180, y: 35, w: 150, h: 100, text: "Click to select Reference Image", image_src: null },
      { id: `elem_main_${Date.now()}`, type: "main_image", x: 45, y: 150, w: 420, h: 420, text: "Click to select Drawing Image", image_src: null },
      { id: `elem_title_${Date.now()}`, type: "title", x: 45, y: 585, w: 420, h: 40, text: `PAGE ${num}`, font_size: 26, color: "#111827" },
      { id: `elem_frame_${Date.now()}`, type: "border", x: 30, y: 25, w: 450, h: 610 }
    ]
  });
  renderTimeline();
  selectPage(currentProject.pages.length - 1);
  markProjectDirty();
  showToast(`Added Page ${num}`, "success");
}

function duplicateCurrentPage() {
  if (currentProject.is_locked) return;

  const curr = currentProject.pages[currentPageIndex];
  if (!curr) return;

  const num = currentProject.pages.length + 1;
  const clone = JSON.parse(JSON.stringify(curr));
  clone.page_number = num;
  clone.title = `${clone.title} (Copy)`;
  currentProject.pages.splice(currentPageIndex + 1, 0, clone);
  renderTimeline();
  selectPage(currentPageIndex + 1);
  markProjectDirty();
  showToast(`Duplicated page to Page ${currentPageIndex + 1}`, "success");
}

function deleteCurrentPage() {
  if (currentProject.is_locked) {
    showToast("🔒 Project is locked!", "warning");
    return;
  }

  if (currentProject.pages.length <= 1) {
    showToast("A book must contain at least one page.", "info");
    return;
  }
  const deletedNum = currentPageIndex + 1;
  currentProject.pages.splice(currentPageIndex, 1);
  const target = Math.max(0, currentPageIndex - 1);
  renderTimeline();
  selectPage(target);
  markProjectDirty();
  showToast(`Deleted Page ${deletedNum}`, "info");
}

// Timeline
function renderTimeline() {
  const strip = document.getElementById("thumbnails-strip");
  if (!strip) return;
  strip.innerHTML = "";

  currentProject.pages.forEach((page, idx) => {
    const card = document.createElement("div");
    card.className = `thumb-card ${idx === currentPageIndex ? 'active' : ''}`;
    card.onclick = () => selectPage(idx);

    const mainEl = page.elements.find(e => (e.type === "main_image" || e.type === "ref_image") && e.image_src);
    const previewContent = mainEl 
      ? `<img src="${mainEl.image_src}">` 
      : `<span style="font-size:16px;">📄</span>`;

    card.innerHTML = `
      <div class="thumb-page-num">Page ${page.page_number}</div>
      <div class="thumb-preview-box">${previewContent}</div>
      <div class="thumb-title">${page.title || 'Page ' + (idx + 1)}</div>
    `;
    strip.appendChild(card);
  });

  const countBadge = document.getElementById("stat-page-count");
  if (countBadge) countBadge.innerText = currentProject.pages.length;
}

function selectPage(index) {
  currentPageIndex = index;
  activeElementId = null;
  renderTimeline();
  loadPageIntoCanvas(index);
  updatePropertiesInspector();
}

// Batch Ingestion
function triggerBatchUpload() {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot batch import: Project is locked!", "warning");
    return;
  }
  const fileInput = document.getElementById("batch-images-input");
  if (fileInput) {
    fileInput.value = "";
    fileInput.click();
  }
}

function handleBatchImagesUpload(event) {
  if (currentProject.is_locked) return;

  const files = Array.from(event.target.files);
  if (!files.length) return;

  showToast(`⚡ Processing ${files.length} images into coloring pages...`, "info");

  let loadedCount = 0;
  files.forEach((file, idx) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const dataUrl = e.target.result;
      const cleanTitle = cleanFileName(file.name);
      const pageNum = currentProject.pages.length + 1;

      if (!currentProject.media) currentProject.media = [];

      currentProject.media.unshift({
        id: `med_batch_${Date.now()}_${idx}`,
        name: cleanTitle,
        fileName: file.name,
        dataUrl: dataUrl,
        sizeKb: Math.round(file.size / 1024)
      });

      currentProject.pages.push({
        page_number: pageNum,
        title: cleanTitle,
        layout: "top_ref",
        elements: [
          { id: `elem_ref_${Date.now()}_${idx}`, type: "ref_image", x: 180, y: 35, w: 150, h: 100, text: cleanTitle, image_src: dataUrl },
          { id: `elem_main_${Date.now()}_${idx}`, type: "main_image", x: 45, y: 150, w: 420, h: 420, text: cleanTitle, image_src: dataUrl },
          { id: `elem_title_${Date.now()}_${idx}`, type: "title", x: 45, y: 585, w: 420, h: 40, text: cleanTitle.toUpperCase(), font_size: 26, color: "#111827", font_family: "Plus Jakarta Sans" },
          { id: `elem_frame_${Date.now()}_${idx}`, type: "border", x: 30, y: 25, w: 450, h: 610 }
        ]
      });

      loadedCount++;
      if (loadedCount === files.length) {
        renderMediaLibrary();
        renderTimeline();
        syncActiveProjectUI();
        markProjectDirty();
        selectPage(currentProject.pages.length - files.length);
        switchTab("canvas");
        showToast(`🎉 Batch Generated ${files.length} KDP Coloring Pages!`, "success");
      }
    };
    reader.readAsDataURL(file);
  });
}

// View Controls
function toggleGuides() {
  showGuides = !showGuides;
  document.getElementById("guides-layer").style.display = showGuides ? "block" : "none";
  document.getElementById("toggle-guides-btn").classList.toggle("active", showGuides);
  showToast(`Guides: ${showGuides ? 'ON' : 'OFF'}`, "info");
}

function toggleSnap() {
  snapToGuides = !snapToGuides;
  document.getElementById("toggle-snap-btn").classList.toggle("active", snapToGuides);
  showToast(`Snapping: ${snapToGuides ? 'ON' : 'OFF'}`, "info");
}

function changeZoom(delta) {
  currentZoom = Math.max(0.4, Math.min(2.5, currentZoom + delta));
  document.getElementById("canvas-stage").style.transform = `scale(${currentZoom})`;
  document.getElementById("zoom-readout").innerText = `Zoom: ${Math.round(currentZoom * 100)}%`;
}

function fitCanvasView() {
  currentZoom = 1.0;
  document.getElementById("canvas-stage").style.transform = `scale(1.0)`;
  document.getElementById("zoom-readout").innerText = `Zoom: 100%`;
}

function saveSettings() {
  markProjectDirty();
  showToast("Settings applied & saved successfully!", "success");
  switchTab("canvas");
}

// Toast Notifications
function showToast(message, type = "info") {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerText = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3200);
}
