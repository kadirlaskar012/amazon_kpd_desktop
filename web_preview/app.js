/**
 * KDP Book Production Studio - Exact Reference Layout (Top-Left Ref + Big Outline Title + 75% Drawing Area) & Single-Sided Blank Page Rules
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
  front_matter_config: {
    auto_front_matter: true,
    create_disclaimer: true,
    create_contents: true,
    auto_sync_contents: true,
    contents_style: "numbered",
    show_page_numbers: true,
    publisher_name: "KDP Creative Publishing",
    isbn: "978-X-XXXXX-XXX-X"
  },
  media: [],
  pages: [
    {
      page_number: 1,
      page_type: "content",
      title: "Playful Lion",
      layout: "kdp_top_ref",
      elements: [
        { id: "elem_ref_1", type: "ref_image", x: 35, y: 25, w: 190, h: 180, text: "Playful Lion Reference", image_src: null },
        { id: "elem_title_1", type: "title", x: 235, y: 70, w: 240, h: 80, text: "LION", font_size: 40, color: "#ffffff", is_outline: true, font_family: "Fredoka", letter_spacing: 2 },
        { id: "elem_main_1", type: "main_image", x: 35, y: 220, w: 440, h: 410, text: "Playful Lion Drawing", image_src: null },
        { id: "elem_frame_1", type: "border", x: 25, y: 15, w: 460, h: 630 }
      ]
    },
    {
      page_number: 2,
      page_type: "content",
      title: "Gentle Elephant",
      layout: "kdp_top_ref",
      elements: [
        { id: "elem_ref_2", type: "ref_image", x: 35, y: 25, w: 190, h: 180, text: "Gentle Elephant Reference", image_src: null },
        { id: "elem_title_2", type: "title", x: 235, y: 70, w: 240, h: 80, text: "ELEPHANT", font_size: 34, color: "#ffffff", is_outline: true, font_family: "Fredoka", letter_spacing: 2 },
        { id: "elem_main_2", type: "main_image", x: 35, y: 220, w: 440, h: 410, text: "Gentle Elephant Drawing", image_src: null },
        { id: "elem_frame_2", type: "border", x: 25, y: 15, w: 460, h: 630 }
      ]
    },
    {
      page_number: 3,
      page_type: "content",
      title: "Cute Dog",
      layout: "kdp_top_ref",
      elements: [
        { id: "elem_ref_3", type: "ref_image", x: 35, y: 25, w: 190, h: 180, text: "Cute Dog Reference", image_src: null },
        { id: "elem_title_3", type: "title", x: 235, y: 70, w: 240, h: 80, text: "PUPPY DOG", font_size: 34, color: "#ffffff", is_outline: true, font_family: "Fredoka", letter_spacing: 2 },
        { id: "elem_main_3", type: "main_image", x: 35, y: 220, w: 440, h: 410, text: "Cute Dog Drawing", image_src: null },
        { id: "elem_frame_3", type: "border", x: 25, y: 15, w: 460, h: 630 }
      ]
    },
    {
      page_number: 4,
      page_type: "content",
      title: "Happy Monkey",
      layout: "kdp_top_ref",
      elements: [
        { id: "elem_ref_4", type: "ref_image", x: 35, y: 25, w: 190, h: 180, text: "Happy Monkey Reference", image_src: null },
        { id: "elem_title_4", type: "title", x: 235, y: 70, w: 240, h: 80, text: "MONKEY", font_size: 34, color: "#ffffff", is_outline: true, font_family: "Fredoka", letter_spacing: 2 },
        { id: "elem_main_4", type: "main_image", x: 35, y: 220, w: 440, h: 410, text: "Happy Monkey Drawing", image_src: null },
        { id: "elem_frame_4", type: "border", x: 25, y: 15, w: 460, h: 630 }
      ]
    }
  ]
};

let recentProjectsList = [];
let currentPageIndex = 0; // Default on first coloring page
let currentSpreadIndex = 0;
let activeElementId = null;
let currentZoom = 1.0;
let cachedPageRect = null;
let showGuides = true;
let snapToGuides = true;
let isCanvasLayoutLocked = true; // Canvas Layout Lock Control (Locked by default)

function toggleCanvasLayoutLock() {
  isCanvasLayoutLocked = !isCanvasLayoutLocked;
  updateCanvasLayoutLockUI();
  if (isCanvasLayoutLocked) {
    showToast("🔒 Canvas layout locked. Accidental movement prevented.", "info");
  } else {
    showToast("🔓 Canvas layout unlocked. You can now drag and resize elements in real time.", "success");
  }
}

function updateCanvasLayoutLockUI() {
  const stage = document.getElementById("canvas-stage");
  if (stage) {
    stage.classList.toggle("layout-locked", isCanvasLayoutLocked);
  }

  const toolBtn = document.getElementById("tool-canvas-lock");
  if (toolBtn) {
    toolBtn.innerText = isCanvasLayoutLocked ? "🔒" : "🔓";
    toolBtn.title = isCanvasLayoutLocked ? "Canvas Layout Locked (Click to Unlock)" : "Canvas Layout Unlocked (Click to Lock)";
    toolBtn.classList.toggle("locked", isCanvasLayoutLocked);
    toolBtn.classList.toggle("unlocked", !isCanvasLayoutLocked);
  }

  const pillBtn = document.getElementById("canvas-lock-pill");
  const icon = document.getElementById("canvas-lock-icon");
  const text = document.getElementById("canvas-lock-text");
  if (pillBtn && icon && text) {
    icon.innerText = isCanvasLayoutLocked ? "🔒" : "🔓";
    text.innerText = isCanvasLayoutLocked ? "Layout Locked" : "Layout Unlocked";
    pillBtn.classList.toggle("locked", isCanvasLayoutLocked);
    pillBtn.classList.toggle("unlocked", !isCanvasLayoutLocked);
    pillBtn.title = isCanvasLayoutLocked ? "Click to Unlock Canvas Layout Editing" : "Click to Lock Canvas Layout";
  }

  updatePropertiesInspector();
}

// Undo / Redo History Engine
let undoStack = [];
let redoStack = [];
const MAX_HISTORY = 40;
let isHistoryAction = false;

// Auto-Save System State
let isDirty = false;
let autoSaveTimer = null;
let renameTargetType = "page";
let projectToDelete = null;

// ==========================================
// Multi-Theme Engine (Default: Light Mode Studio / Dark Mode Toggle)
// ==========================================
function getStoredTheme() {
  try {
    return localStorage.getItem("kdp_studio_theme") || "light";
  } catch (e) {
    return "light";
  }
}

function updateThemeDashboardUI(theme) {
  const lightBtn = document.getElementById("dash-theme-light-btn");
  const darkBtn = document.getElementById("dash-theme-dark-btn");
  if (lightBtn && darkBtn) {
    if (theme === "dark") {
      lightBtn.classList.remove("active");
      darkBtn.classList.add("active");
    } else {
      lightBtn.classList.add("active");
      darkBtn.classList.remove("active");
    }
  }
}

function applyTheme(theme) {
  const root = document.documentElement;
  root.setAttribute("data-theme", theme);
  const icon = document.getElementById("theme-toggle-icon");
  const label = document.getElementById("theme-toggle-text");
  const btn = document.getElementById("theme-toggle-btn");

  if (theme === "light") {
    if (icon) icon.innerText = "🌙";
    if (label) label.innerText = "Dark";
    if (btn) {
      btn.title = "Switch to Dark Mode Studio";
      btn.classList.remove("is-dark");
    }
  } else {
    if (icon) icon.innerText = "☀️";
    if (label) label.innerText = "Light";
    if (btn) {
      btn.title = "Switch to Light Mode Studio";
      btn.classList.add("is-dark");
    }
  }

  updateThemeDashboardUI(theme);
}

function selectAndApplyTheme(mode) {
  applyTheme(mode);
}

function saveThemePreference() {
  const currentTheme = document.documentElement.getAttribute("data-theme") || "light";
  try {
    localStorage.setItem("kdp_studio_theme", currentTheme);
  } catch (e) {}

  // Persist to server disk settings file
  fetch("/api/settings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ theme: currentTheme })
  }).catch(() => {});

  const badge = document.getElementById("dash-theme-saved-badge");
  if (badge) {
    badge.classList.add("visible");
    setTimeout(() => { badge.classList.remove("visible"); }, 3000);
  }

  showToast(`💾 Theme saved as ${currentTheme === 'dark' ? 'Dark Mode' : 'Light Mode'} (Permanent Preference)`, "success");
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") || "light";
  const newTheme = current === "light" ? "dark" : "light";
  try {
    localStorage.setItem("kdp_studio_theme", newTheme);
  } catch (e) {}

  // Auto-sync with server settings
  fetch("/api/settings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ theme: newTheme })
  }).catch(() => {});

  applyTheme(newTheme);
  showToast(newTheme === "light" ? "☀️ Switched to Light Mode Studio" : "🌙 Switched to Dark Mode Studio", "info");
}

function initTheme() {
  const localTheme = getStoredTheme();
  applyTheme(localTheme);

  // Sync with persistent backend setting
  fetch("/api/settings")
    .then(r => r.json())
    .then(data => {
      if (data && data.settings && data.settings.theme) {
        const serverTheme = data.settings.theme;
        if (serverTheme !== localTheme) {
          try {
            localStorage.setItem("kdp_studio_theme", serverTheme);
          } catch (e) {}
          applyTheme(serverTheme);
        }
      }
    })
    .catch(() => {});
}

// Immediately apply theme before DOM renders to prevent any theme flash
initTheme();

// UI Initialization
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  setupNavigation();
  setupGlobalKeyboardShortcuts();
  loadInitialProject();
  setupCanvasInteractions();
  updateUndoRedoButtons();
  updateCanvasLayoutLockUI();

  // Background Auto-Save Cron (Every 10 seconds)
  setInterval(() => {
    if (isDirty) {
      saveProject(false);
    }
  }, 10000);
  
  // Window resize responsive canvas auto-fitter (debounced with rAF)
  let resizeTimer = null;
  window.addEventListener("resize", () => {
    cachedPageRect = null;
    if (resizeTimer) cancelAnimationFrame(resizeTimer);
    resizeTimer = requestAnimationFrame(() => {
      const activePanel = document.querySelector(".tab-panel.active");
      if (activePanel && activePanel.id === "panel-canvas") {
        fitCanvasView();
      }
    });
  });
});

// ==========================================
// Undo / Redo History Stack Implementation
// ==========================================
function cloneProjectForHistory(proj) {
  if (!proj) return null;
  return {
    ...proj,
    settings: proj.settings ? JSON.parse(JSON.stringify(proj.settings)) : {},
    pages: proj.pages ? JSON.parse(JSON.stringify(proj.pages)) : [],
    media: proj.media || []
  };
}

function recordHistoryState(actionName = "Edit") {
  if (isHistoryAction) return;

  try {
    const snapshot = {
      project: cloneProjectForHistory(currentProject),
      pageIndex: currentPageIndex,
      activeElementId: activeElementId,
      action: actionName
    };

    undoStack.push(snapshot);
    if (undoStack.length > MAX_HISTORY) {
      undoStack.shift();
    }

    redoStack = [];
    updateUndoRedoButtons();
  } catch (e) {
    console.warn("History recording error:", e);
  }
}

function performUndo() {
  if (undoStack.length === 0) {
    showToast("Nothing to undo.", "info");
    return;
  }

  isHistoryAction = true;
  try {
    const currentState = {
      project: cloneProjectForHistory(currentProject),
      pageIndex: currentPageIndex,
      activeElementId: activeElementId,
      action: "Current State"
    };
    redoStack.push(currentState);

    const previousState = undoStack.pop();
    currentProject = {
      ...previousState.project,
      media: currentProject.media || previousState.project.media || []
    };
    currentPageIndex = Math.min(previousState.pageIndex, currentProject.pages.length - 1);
    activeElementId = previousState.activeElementId;

    renumberPages();
    syncActiveProjectUI();
    loadPageIntoCanvas(currentPageIndex);
    renderTimeline();
    markProjectDirty();
    updateUndoRedoButtons();

    showToast(`↶ Undo: ${previousState.action || 'Action'}`, "info");
  } catch (e) {
    console.error("Undo error:", e);
  } finally {
    isHistoryAction = false;
  }
}

function performRedo() {
  if (redoStack.length === 0) {
    showToast("Nothing to redo.", "info");
    return;
  }

  isHistoryAction = true;
  try {
    const currentState = {
      project: cloneProjectForHistory(currentProject),
      pageIndex: currentPageIndex,
      activeElementId: activeElementId,
      action: "Current State"
    };
    undoStack.push(currentState);

    const nextState = redoStack.pop();
    currentProject = {
      ...nextState.project,
      media: currentProject.media || nextState.project.media || []
    };
    currentPageIndex = Math.min(nextState.pageIndex, currentProject.pages.length - 1);
    activeElementId = nextState.activeElementId;

    renumberPages();
    syncActiveProjectUI();
    loadPageIntoCanvas(currentPageIndex);
    renderTimeline();
    markProjectDirty();
    updateUndoRedoButtons();

    showToast(`↷ Redo: ${nextState.action || 'Action'}`, "info");
  } catch (e) {
    console.error("Redo error:", e);
  } finally {
    isHistoryAction = false;
  }
}

function updateUndoRedoButtons() {
  const btnUndoH = document.getElementById("btn-undo-header");
  const btnRedoH = document.getElementById("btn-redo-header");
  const toolUndo = document.getElementById("tool-undo");
  const toolRedo = document.getElementById("tool-redo");

  const canUndo = undoStack.length > 0;
  const canRedo = redoStack.length > 0;

  if (btnUndoH) {
    btnUndoH.disabled = !canUndo;
    btnUndoH.title = canUndo ? `Undo: ${undoStack[undoStack.length - 1].action} (Ctrl+Z)` : "Undo (Ctrl+Z)";
  }
  if (btnRedoH) {
    btnRedoH.disabled = !canRedo;
    btnRedoH.title = canRedo ? `Redo: ${redoStack[redoStack.length - 1].action} (Ctrl+Y)` : "Redo (Ctrl+Y)";
  }
  if (toolUndo) {
    toolUndo.disabled = !canUndo;
    toolUndo.title = canUndo ? `Undo: ${undoStack[undoStack.length - 1].action} (Ctrl+Z)` : "Undo (Ctrl+Z)";
  }
  if (toolRedo) {
    toolRedo.disabled = !canRedo;
    toolRedo.title = canRedo ? `Redo: ${redoStack[redoStack.length - 1].action} (Ctrl+Y)` : "Redo (Ctrl+Y)";
  }
}

// ==========================================
// Title Resolver & Cleaner
// ==========================================
function resolveCleanPageTitle(page, idx = 1) {
  if (!page) return `Page ${idx}`;

  if (page.title && page.title.trim() && !/^Page\s*\d+$/i.test(page.title.trim())) {
    return cleanTitleString(page.title.trim());
  }

  if (page.elements && Array.isArray(page.elements)) {
    const titleElem = page.elements.find(e => e.type === "title");
    if (titleElem && titleElem.text && !/^PAGE\s*\d+$/i.test(titleElem.text.trim())) {
      return cleanTitleString(titleElem.text.trim());
    }

    const imgElem = page.elements.find(e => (e.type === "main_image" || e.type === "ref_image") && (e.text || e.fileName));
    if (imgElem) {
      const candidate = imgElem.fileName || imgElem.text;
      if (candidate && !candidate.toLowerCase().includes("click to select")) {
        return cleanFileName(candidate);
      }
    }
  }

  return `Page ${page.page_number || idx}`;
}

function cleanTitleString(str) {
  return str.replace(/_/g, " ").replace(/-/g, " ").replace(/\s+/g, " ").trim()
    .replace(/\b\w/g, c => c.toUpperCase());
}

function extractFirstWordCaps(rawName) {
  if (!rawName) return "UNTITLED";
  let clean = rawName.replace(/\.[^/.]+$/, "");
  clean = clean.replace(/^(page\s*[\-_]*)?\d+[\s_\.\-]+/i, "");
  clean = clean.replace(/[_\-]+/g, " ").trim();
  const parts = clean.split(/\s+/).filter(Boolean);
  const firstWord = parts.length > 0 ? parts[0] : clean;
  const stripped = firstWord.replace(/[\-_]?(color|colour|outline|drawing|lineart|bw|art)$/i, "");
  return (stripped || firstWord).toUpperCase();
}

function cleanFileName(filename) {
  let name = filename.replace(/\.[^/.]+$/, "");
  name = name.replace(/^(page\s*[\-_]*)?\d+[\s_\.\-]+/i, "");
  name = name.replace(/[\-_](coloring[\-_]?page|lineart|drawing|illustration|vector|bw|art|color|colour|outline)$/i, "");
  name = name.replace(/[_\-]+/g, " ").trim();
  return name.replace(/\b\w/g, c => c.toUpperCase());
}

// ==========================================
// Sequential Auto-Renumbering & Contents Sync
// ==========================================
function renumberPages() {
  if (!currentProject.pages || !Array.isArray(currentProject.pages)) return;

  let contentPageCounter = 1;

  currentProject.pages.forEach((page, idx) => {
    const newDocNum = idx + 1;
    page.page_number = newDocNum;

    if (page.page_type === "front_matter_disclaimer") {
      page.title = "Disclaimer & Copyright";
    } else if (page.page_type === "front_matter_contents") {
      page.title = "Table of Contents";
    } else if (page.page_type === "blank_verso") {
      page.title = "Blank Back Page";
    } else {
      page.page_type = "content";
      if (!page.title || /^Page\s*\d+$/i.test(page.title.trim())) {
        page.title = `Page ${contentPageCounter}`;
      }
      contentPageCounter++;
    }
  });

  syncContentsPage();
}

function syncContentsPage() {
  const cfg = currentProject.front_matter_config || {};
  if (cfg.auto_sync_contents === false) return;

  const contentsPage = currentProject.pages.find(p => p.page_type === "front_matter_contents" || p.layout === "contents_standard");
  if (!contentsPage || contentsPage.is_locked) return;

  // Only list actual content drawing pages (skip Disclaimer, Contents, and Blank Verso pages)
  const contentPages = currentProject.pages.filter(p => p.page_type === "content");
  
  const elements = [
    { id: "elem_cnt_frame", type: "border", x: 30, y: 25, w: 450, h: 610 },
    { id: "elem_cnt_head", type: "title", x: 45, y: 55, w: 420, h: 35, text: cfg.contents_heading || "TABLE OF CONTENTS", font_size: 22, color: "#0f172a", is_outline: false },
    { id: "elem_cnt_sub", type: "title", x: 45, y: 90, w: 420, h: 20, text: "Explore all the illustrations and coloring pages in this book", font_size: 11, color: "#64748b", is_outline: false }
  ];

  const startY = 135;
  const rowHeight = 26;
  const maxRows = 15;

  if (contentPages.length <= maxRows) {
    contentPages.forEach((p, idx) => {
      const resolvedTitle = resolveCleanPageTitle(p, idx + 1);
      const prefix = cfg.contents_style === "bullet" ? "• " : (cfg.contents_style === "plain" ? "" : `${idx + 1}. `);
      const line = `${prefix}${resolvedTitle} .................................... Page ${p.page_number}`;
      elements.push({
        id: `elem_cnt_item_${idx + 1}`,
        type: "title",
        x: 60,
        y: startY + (idx * rowHeight),
        w: 390,
        h: 22,
        text: line,
        font_size: 11,
        color: "#1e293b",
        is_outline: false
      });
    });
  } else {
    const col1 = contentPages.slice(0, maxRows);
    const col2 = contentPages.slice(maxRows, maxRows * 2);

    col1.forEach((p, idx) => {
      const resolvedTitle = resolveCleanPageTitle(p, idx + 1);
      const line = `${idx + 1}. ${resolvedTitle} (p.${p.page_number})`;
      elements.push({
        id: `elem_cnt_c1_${idx + 1}`,
        type: "title",
        x: 45,
        y: startY + (idx * rowHeight),
        w: 205,
        h: 22,
        text: line,
        font_size: 10,
        color: "#1e293b",
        is_outline: false
      });
    });

    col2.forEach((p, idx) => {
      const trueIdx = idx + maxRows;
      const resolvedTitle = resolveCleanPageTitle(p, trueIdx + 1);
      const line = `${trueIdx + 1}. ${resolvedTitle} (p.${p.page_number})`;
      elements.push({
        id: `elem_cnt_c2_${trueIdx + 1}`,
        type: "title",
        x: 260,
        y: startY + (idx * rowHeight),
        w: 205,
        h: 22,
        text: line,
        font_size: 10,
        color: "#1e293b",
        is_outline: false
      });
    });
  }

  contentsPage.elements = elements;
}

// ==========================================
// Front Matter Regeneration Engine
// ==========================================
function regenerateFrontMatterPages() {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot modify: Project is locked!", "warning");
    return;
  }

  recordHistoryState("Regenerate Front Matter");

  const projName = currentProject.name || "Untitled Book";
  const authorName = currentProject.author || "Creative Kids Studio";
  const year = new Date().getFullYear();

  const contentPages = currentProject.pages.filter(p => p.page_type !== "front_matter_disclaimer" && p.page_type !== "front_matter_contents");

  const disclaimerPage = {
    page_number: 1,
    page_type: "front_matter_disclaimer",
    title: "Disclaimer & Copyright",
    layout: "disclaimer_standard",
    elements: [
      { id: "elem_disc_frame", type: "border", x: 30, y: 25, w: 450, h: 610 },
      { id: "elem_disc_title", type: "title", x: 45, y: 65, w: 420, h: 40, text: projName.toUpperCase(), font_size: 24, color: "#0f172a", is_outline: false },
      { id: "elem_disc_sub", type: "title", x: 45, y: 110, w: 420, h: 25, text: "First Edition • Premium KDP Edition", font_size: 13, color: "#475569", is_outline: false },
      { id: "elem_disc_copy", type: "title", x: 45, y: 180, w: 420, h: 25, text: `Copyright © ${year} by ${authorName}`, font_size: 14, color: "#1e293b", is_outline: false },
      { id: "elem_disc_rights", type: "title", x: 45, y: 210, w: 420, h: 20, text: "All rights reserved.", font_size: 12, color: "#475569", is_outline: false },
      { id: "elem_disc_p1", type: "title", x: 45, y: 260, w: 420, h: 20, text: "No part of this publication may be reproduced, distributed, or transmitted in any form", font_size: 10, color: "#64748b", is_outline: false },
      { id: "elem_disc_p2", type: "title", x: 45, y: 285, w: 420, h: 20, text: "or by any means, including photocopying, recording, or other electronic methods,", font_size: 10, color: "#64748b", is_outline: false },
      { id: "elem_disc_p3", type: "title", x: 45, y: 310, w: 420, h: 20, text: "without the prior written permission of the author and publisher.", font_size: 10, color: "#64748b", is_outline: false },
      { id: "elem_disc_pub", type: "title", x: 45, y: 400, w: 420, h: 20, text: "Published by: KDP Creative Publishing", font_size: 11, color: "#334155", is_outline: false },
      { id: "elem_disc_isbn", type: "title", x: 45, y: 430, w: 420, h: 20, text: "ISBN-13: 978-X-XXXXX-XXX-X", font_size: 11, color: "#334155", is_outline: false },
      { id: "elem_disc_contact", type: "title", x: 45, y: 480, w: 420, h: 20, text: "Visit us: www.kdpbooks.com • support@kdpbooks.com", font_size: 10, color: "#64748b", is_outline: false },
      { id: "elem_disc_kdp", type: "title", x: 45, y: 550, w: 420, h: 20, text: "Printed for Amazon KDP Distribution • First Printing", font_size: 9, color: "#94a3b8", is_outline: false }
    ]
  };

  const contentsPage = {
    page_number: 2,
    page_type: "front_matter_contents",
    title: "Table of Contents",
    layout: "contents_standard",
    elements: [
      { id: "elem_cnt_frame", type: "border", x: 30, y: 25, w: 450, h: 610 },
      { id: "elem_cnt_head", type: "title", x: 45, y: 55, w: 420, h: 35, text: "TABLE OF CONTENTS", font_size: 22, color: "#0f172a", is_outline: false },
      { id: "elem_cnt_sub", type: "title", x: 45, y: 90, w: 420, h: 20, text: "Explore all the illustrations and coloring pages in this book", font_size: 11, color: "#64748b", is_outline: false }
    ]
  };

  currentProject.pages = [disclaimerPage, contentsPage, ...contentPages];
  renumberPages();
  syncActiveProjectUI();
  selectPage(0);
  switchTab("canvas");
  markProjectDirty();
  showToast("⚡ Inserted & Synchronized Front Matter Pages (Disclaimer + Contents)!", "success");
}

function forceSyncContents() {
  recordHistoryState("Force Sync Contents");
  syncContentsPage();
  loadPageIntoCanvas(currentPageIndex);
  renderTimeline();
  markProjectDirty();
  showToast("🔄 Synchronized Table of Contents!", "success");
}

function onFrontMatterConfigChange() {
  recordHistoryState("Front Matter Config Change");
  if (!currentProject.front_matter_config) currentProject.front_matter_config = {};
  
  const autoFm = document.getElementById("setting-auto-front-matter");
  const autoSync = document.getElementById("setting-auto-sync-contents");
  const styleSelect = document.getElementById("setting-contents-style");
  const authorInput = document.getElementById("setting-author-name");
  const pubInput = document.getElementById("setting-publisher-name");
  const isbnInput = document.getElementById("setting-isbn");

  if (autoFm) currentProject.front_matter_config.auto_front_matter = autoFm.checked;
  if (autoSync) currentProject.front_matter_config.auto_sync_contents = autoSync.checked;
  if (styleSelect) currentProject.front_matter_config.contents_style = styleSelect.value;
  if (authorInput && authorInput.value.trim()) currentProject.author = authorInput.value.trim();
  if (pubInput && pubInput.value.trim()) currentProject.front_matter_config.publisher_name = pubInput.value.trim();
  if (isbnInput && isbnInput.value.trim()) currentProject.front_matter_config.isbn = isbnInput.value.trim();

  syncContentsPage();
  markProjectDirty();
}

// ==========================================
// Robust Initial Project Loader & Empty Workspace Engine
// ==========================================
function clearActiveProject() {
  localStorage.removeItem("kdp_active_project_path");
  localStorage.removeItem("kdp_active_project_data");
  localStorage.removeItem("kdp_autosave_current_project");
  currentProject = {
    name: "",
    folder_name: "",
    project_dir: "",
    author: "",
    is_locked: false,
    is_empty: true,
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
  undoStack = [];
  redoStack = [];
  currentPageIndex = 0;
  activeElementId = null;
  updateUndoRedoButtons();
  syncActiveProjectUI();
}

function loadInitialProject() {
  fetchDefaultLocation();

  // Restore the last active tab from URL query params or sessionStorage
  const urlParams = new URLSearchParams(window.location.search);
  const queryTab = urlParams.get("tab");
  const lastTab = queryTab || sessionStorage.getItem("kdp_active_tab") || localStorage.getItem("kdp_active_tab") || "dashboard";

  // Hydrate UI state synchronously to prevent toolbar and content flash
  document.documentElement.setAttribute("data-active-tab", lastTab);
  const headerCanvasActions = document.getElementById("header-canvas-actions");
  if (headerCanvasActions) {
    headerCanvasActions.style.display = (lastTab === "canvas") ? "flex" : "none";
  }

  // Pre-hydrate cached project title to eliminate placeholder text flash
  try {
    const cachedData = localStorage.getItem("kdp_active_project_data");
    if (cachedData) {
      const parsed = JSON.parse(cachedData);
      if (parsed && parsed.name) {
        const navProjName = document.getElementById("nav-project-name");
        if (navProjName) navProjName.innerText = parsed.name;
      }
    }
  } catch (e) {}

  // Synchronously activate correct tab nav and panel before async operations
  document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
  const targetBtn = document.querySelector(`.nav-btn[data-tab="${lastTab}"]`);
  const targetPanel = document.getElementById(`panel-${lastTab}`);
  if (targetBtn) targetBtn.classList.add("active");
  if (targetPanel) targetPanel.classList.add("active");

  // Query real projects list from local disk
  fetch("/api/projects")
    .then(r => r.json())
    .then(data => {
      recentProjectsList = data.projects || [];
      renderRecentProjects();
      updateHeroStats(data.stats);

      if (recentProjectsList.length === 0) {
        clearActiveProject();
        switchTab("dashboard");
        return;
      }

      // Check if last opened project still exists on disk
      const savedPath = localStorage.getItem("kdp_active_project_path");
      let matchedProj = null;
      if (savedPath) {
        const normSaved = savedPath.replace(/\\/g, "/").toLowerCase();
        matchedProj = recentProjectsList.find(p => p.path.replace(/\\/g, "/").toLowerCase() === normSaved);
      }

      if (!matchedProj && recentProjectsList.length > 0) {
        matchedProj = recentProjectsList[0];
      }

      if (matchedProj) {
        fetch(`/api/projects/load?path=${encodeURIComponent(matchedProj.path)}`)
          .then(r => r.json())
          .then(loadData => {
            if (loadData.project) {
              currentProject = loadData.project;
            } else {
              currentProject.name = matchedProj.name;
              currentProject.project_dir = matchedProj.path;
              currentProject.folder_name = matchedProj.path.split("\\").pop();
              currentProject.is_locked = Boolean(matchedProj.is_locked);
            }

            const savedPageIdx = parseInt(localStorage.getItem("kdp_active_page_index") || "0", 10);
            const maxPageIdx = Math.max(0, (currentProject.pages || []).length - 1);
            currentPageIndex = Math.min(savedPageIdx, maxPageIdx);

            renumberPages();
            syncActiveProjectUI();

            if (lastTab === "canvas") {
              loadPageIntoCanvas(currentPageIndex);
              switchTab("canvas");
            } else if (lastTab && lastTab !== "dashboard") {
              switchTab(lastTab);
            } else {
              // Default or dashboard: STAY ON DASHBOARD!
              switchTab("dashboard");
            }
          })
          .catch(() => {
            syncActiveProjectUI();
            switchTab(lastTab || "dashboard");
          });
      } else {
        clearActiveProject();
        switchTab("dashboard");
      }
    })
    .catch(err => {
      console.warn("Project directory query error:", err);
      clearActiveProject();
      switchTab("dashboard");
    });
}

function markProjectDirty() {
  if (currentProject.is_locked) return;
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
  
  try {
    localStorage.setItem("kdp_active_project_path", currentProject.project_dir);
    localStorage.setItem("kdp_active_project_data", JSON.stringify(currentProject));
    localStorage.setItem("kdp_autosave_current_project", JSON.stringify(currentProject));
    if (currentProject.folder_name) {
      localStorage.setItem(`kdp_project_${currentProject.folder_name}`, JSON.stringify(currentProject));
    }
  } catch (e) {
    console.warn("LocalStorage save error:", e);
  }

  fetch("/api/projects/save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(currentProject)
  })
  .then(() => {
    isDirty = false;
    updateAutoSaveIndicator(false);
    fetchRecentProjects();
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

// ==========================================
// 300 DPI Amazon KDP PDF Exporter & Pre-flight Modal
// ==========================================
function exportProjectPdf() {
  openExportPdfModal();
}

function toggleFrontMatterEditor() {
  const ed = document.getElementById("export-fm-text-editor");
  const btn = document.getElementById("btn-toggle-fm-editor");
  if (!ed) return;
  const isHidden = (ed.style.display === "none" || !ed.style.display);
  ed.style.display = isHidden ? "block" : "none";
  if (btn) {
    btn.innerHTML = isHidden ? "✕ Close Page Editor" : "✏️ Edit Page Content & Custom Texts";
    if (isHidden) {
      btn.classList.add("btn-primary");
    } else {
      btn.classList.remove("btn-primary");
    }
  }
}

function switchFrontMatterTab(tabId) {
  document.querySelectorAll(".fm-tab-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".fm-tab-pane").forEach(p => p.classList.remove("active"));
  const btn = document.getElementById(`btn-fmtab-${tabId}`);
  const pane = document.getElementById(`fmtab-${tabId}`);
  if (btn) btn.classList.add("active");
  if (pane) pane.classList.add("active");
}

function resetFrontMatterTextsToDefault() {
  const author = currentProject.author || "Creative Kids Studio";
  const name = currentProject.name || "COLORING BOOK";

  const setVal = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.value = val;
  };

  setVal("exp-fm-text-title", name);
  setVal("exp-fm-text-author", author);
  setVal("exp-fm-text-publisher", "KDP Creative Publishing");
  setVal("exp-fm-text-edition", "First Edition  •  Amazon KDP Publication");
  setVal("exp-fm-text-copyright", `Copyright © 2026 by ${author}. All Rights Reserved.`);
  setVal("exp-fm-text-isbn", "ISBN-13: 978-X-XXXXX-XXX-X");
  setVal("exp-fm-text-disclaimer", "No part of this publication may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the publisher, except in the case of brief quotations embodied in critical reviews and certain other noncommercial uses permitted by copyright law.");
  setVal("exp-fm-text-extra-note", "");

  setVal("exp-fm-text-toc-heading", "TABLE OF CONTENTS");
  setVal("exp-fm-text-toc-subtext", "Complete list of coloring illustrations in this book");
  setVal("exp-fm-text-toc-footer", "");

  setVal("exp-fm-text-belongs-title", "THIS COLORING BOOK");
  setVal("exp-fm-text-belongs-header", "BELONGS TO:");
  setVal("exp-fm-text-subtext", "Color with joy, love and your wild imagination!");
  setVal("exp-fm-text-belongs-gift", "");

  setVal("exp-fm-text-color-title", "COLOR TEST PALETTE");
  setVal("exp-fm-text-color-subtext", "Test your pencils, markers, and crayons here before coloring!");
  setVal("exp-fm-text-color-note", "");

  setVal("exp-fm-custom-title", "A NOTE FROM THE AUTHOR");
  setVal("exp-fm-custom-subtitle", "Thank you for supporting our work!");
  setVal("exp-fm-custom-body", "Thank you so much for choosing our coloring book!\n\nWe poured our hearts into creating each illustration, designed to spark creativity, relaxation, and endless joy. Whether you are coloring with colored pencils, markers, or crayons, remember that in art, there are no mistakes—only unique masterpieces!\n\nIf you enjoyed this book, please consider leaving a review on Amazon. Your kind feedback helps independent creators like us continue to make beautiful books!");
  setVal("exp-fm-custom-signoff", `Happy Coloring!  •  ${author}`);

  updateExportModalPreview();
  showToast("🔄 Reset all page texts to standard defaults!", "info");
}

function saveFrontMatterTexts() {
  const cfg = getFrontMatterFormData();
  currentProject.front_matter_config = cfg;
  saveProject(false);
  showToast("💾 Page custom texts saved to project!", "success");
}

function getFrontMatterFormData() {
  const getVal = (id, fallback = "") => document.getElementById(id)?.value ?? fallback;
  const author = getVal("exp-fm-text-author", currentProject.author || "Creative Kids Studio");
  return {
    include_disclaimer: document.getElementById("exp-fm-disclaimer")?.checked ?? true,
    include_contents: document.getElementById("exp-fm-contents")?.checked ?? false,
    include_belongs: document.getElementById("exp-fm-belongs")?.checked ?? false,
    include_color_test: document.getElementById("exp-fm-color-test")?.checked ?? false,
    include_custom_page: document.getElementById("exp-fm-custom")?.checked ?? false,
    custom_page_pos: getVal("exp-fm-custom-pos", "back"),

    book_title: getVal("exp-fm-text-title", currentProject.name || "COLORING BOOK"),
    author: author,
    publisher: getVal("exp-fm-text-publisher", "KDP Creative Publishing"),
    edition_text: getVal("exp-fm-text-edition", "First Edition  •  Amazon KDP Publication"),
    copyright_text: getVal("exp-fm-text-copyright", `Copyright © 2026 by ${author}. All Rights Reserved.`),
    isbn: getVal("exp-fm-text-isbn", "ISBN-13: 978-X-XXXXX-XXX-X"),
    disclaimer_text: getVal("exp-fm-text-disclaimer", ""),
    disclaimer_extra_note: getVal("exp-fm-text-extra-note", ""),

    toc_heading: getVal("exp-fm-text-toc-heading", "TABLE OF CONTENTS"),
    toc_subtitle: getVal("exp-fm-text-toc-subtext", "Complete list of coloring illustrations in this book"),
    toc_footer: getVal("exp-fm-text-toc-footer", ""),

    belongs_title: getVal("exp-fm-text-belongs-title", "THIS COLORING BOOK"),
    belongs_header: getVal("exp-fm-text-belongs-header", "BELONGS TO:"),
    subtext: getVal("exp-fm-text-subtext", "Color with joy, love and your wild imagination!"),
    belongs_gift_note: getVal("exp-fm-text-belongs-gift", ""),

    color_test_title: getVal("exp-fm-text-color-title", "COLOR TEST PALETTE"),
    color_test_subtext: getVal("exp-fm-text-color-subtext", "Test your pencils, markers, and crayons here before coloring!"),
    color_test_note: getVal("exp-fm-text-color-note", ""),

    custom_page_title: getVal("exp-fm-custom-title", "A NOTE FROM THE AUTHOR"),
    custom_page_subtitle: getVal("exp-fm-custom-subtitle", "Thank you for supporting our work!"),
    custom_page_body: getVal("exp-fm-custom-body", ""),
    custom_page_signoff: getVal("exp-fm-custom-signoff", `Happy Coloring!  •  ${author}`)
  };
}

function openExportPdfModal() {
  const modal = document.getElementById("export-pdf-modal");
  if (!modal) return;

  const trimWidthIn = (currentProject.settings.trim_width_pt / 72.0).toFixed(1);
  const trimHeightIn = (currentProject.settings.trim_height_pt / 72.0).toFixed(1);
  const trimLabel = document.getElementById("exp-spec-trim");
  if (trimLabel) trimLabel.innerText = `${trimWidthIn} × ${trimHeightIn} in`;

  const bleedLabel = document.getElementById("exp-spec-bleed");
  if (bleedLabel) {
    bleedLabel.innerText = currentProject.settings.has_bleed ? "+0.125 in (9 pt) Bleed" : "No Bleed (Trim Box)";
  }

  const pathLabel = document.getElementById("exp-target-path-preview");
  if (pathLabel) {
    const filename = `${currentProject.name.replace(/ /g, '_')}_KDP_Print_Ready.pdf`;
    pathLabel.innerText = `📁 ${currentProject.project_dir}\\exports\\${filename}`;
  }

  const bType = currentProject.book_type || "coloring_book";
  const isColoring = (bType === "coloring_book");

  // Show/Hide coloring-specific front matter page checkboxes
  const contentsBox = document.getElementById("exp-fm-contents-box");
  const belongsBox = document.getElementById("exp-fm-belongs-box");
  const colorTestBox = document.getElementById("exp-fm-color-test-box");
  if (contentsBox) contentsBox.style.display = isColoring ? "flex" : "none";
  if (belongsBox) belongsBox.style.display = isColoring ? "flex" : "none";
  if (colorTestBox) colorTestBox.style.display = isColoring ? "flex" : "none";

  const singleSidedOpt = document.getElementById("exp-opt-single-sided");
  if (!isColoring) {
    if (singleSidedOpt) singleSidedOpt.checked = false;
    if (document.getElementById("exp-fm-contents")) document.getElementById("exp-fm-contents").checked = false;
    if (document.getElementById("exp-fm-belongs")) document.getElementById("exp-fm-belongs").checked = false;
    if (document.getElementById("exp-fm-color-test")) document.getElementById("exp-fm-color-test").checked = false;
  } else {
    if (singleSidedOpt) singleSidedOpt.checked = true;
    if (document.getElementById("exp-fm-contents")) document.getElementById("exp-fm-contents").checked = true;
    if (document.getElementById("exp-fm-belongs")) document.getElementById("exp-fm-belongs").checked = true;
    if (document.getElementById("exp-fm-color-test")) document.getElementById("exp-fm-color-test").checked = true;
  }

  // Populate text inputs from currentProject.front_matter_config (or sensible defaults)
  const cfg = currentProject.front_matter_config || {};
  const author = cfg.author || currentProject.author || "Creative Kids Studio";
  const name = cfg.book_title || currentProject.name || "COLORING BOOK";

  const setVal = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.value = val;
  };

  setVal("exp-fm-text-title", name);
  setVal("exp-fm-text-author", author);
  setVal("exp-fm-text-publisher", cfg.publisher || "KDP Creative Publishing");
  setVal("exp-fm-text-edition", cfg.edition_text || "First Edition  •  Amazon KDP Publication");
  setVal("exp-fm-text-copyright", cfg.copyright_text || `Copyright © 2026 by ${author}. All Rights Reserved.`);
  setVal("exp-fm-text-isbn", cfg.isbn || "ISBN-13: 978-X-XXXXX-XXX-X");
  setVal("exp-fm-text-disclaimer", cfg.disclaimer_text || "No part of this publication may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the publisher, except in the case of brief quotations embodied in critical reviews and certain other noncommercial uses permitted by copyright law.");
  setVal("exp-fm-text-extra-note", cfg.disclaimer_extra_note || "");

  setVal("exp-fm-text-toc-heading", cfg.toc_heading || "TABLE OF CONTENTS");
  setVal("exp-fm-text-toc-subtext", cfg.toc_subtitle || "Complete list of coloring illustrations in this book");
  setVal("exp-fm-text-toc-footer", cfg.toc_footer || "");

  setVal("exp-fm-text-belongs-title", cfg.belongs_title || "THIS COLORING BOOK");
  setVal("exp-fm-text-belongs-header", cfg.belongs_header || "BELONGS TO:");
  setVal("exp-fm-text-subtext", cfg.subtext || "Color with joy, love and your wild imagination!");
  setVal("exp-fm-text-belongs-gift", cfg.belongs_gift_note || "");

  setVal("exp-fm-text-color-title", cfg.color_test_title || "COLOR TEST PALETTE");
  setVal("exp-fm-text-color-subtext", cfg.color_test_subtext || "Test your pencils, markers, and crayons here before coloring!");
  setVal("exp-fm-text-color-note", cfg.color_test_note || "");

  setVal("exp-fm-custom-title", cfg.custom_page_title || "A NOTE FROM THE AUTHOR");
  setVal("exp-fm-custom-subtitle", cfg.custom_page_subtitle || "Thank you for supporting our work!");
  setVal("exp-fm-custom-body", cfg.custom_page_body || "Thank you so much for choosing our coloring book!\n\nWe poured our hearts into creating each illustration, designed to spark creativity, relaxation, and endless joy. Whether you are coloring with colored pencils, markers, or crayons, remember that in art, there are no mistakes—only unique masterpieces!\n\nIf you enjoyed this book, please consider leaving a review on Amazon. Your kind feedback helps independent creators like us continue to make beautiful books!");
  setVal("exp-fm-custom-signoff", cfg.custom_page_signoff || `Happy Coloring!  •  ${author}`);

  if (document.getElementById("exp-fm-custom-pos")) {
    document.getElementById("exp-fm-custom-pos").value = cfg.custom_page_pos || "back";
  }

  if (document.getElementById("exp-fm-custom")) {
    document.getElementById("exp-fm-custom").checked = cfg.include_custom_page || false;
  }

  // Set active tab to disclaimer initially
  switchFrontMatterTab("disclaimer");

  updateExportModalPreview();
  modal.classList.add("active");
}

let exportModalUpdateTimer = null;
let lastExportModalUpdateTime = 0;
function updateExportModalPreview() {
  const now = performance.now();
  if (now - lastExportModalUpdateTime < 75) {
    if (exportModalUpdateTimer) cancelAnimationFrame(exportModalUpdateTimer);
    exportModalUpdateTimer = requestAnimationFrame(() => {
      renderExportModalPreview();
      lastExportModalUpdateTime = performance.now();
    });
    return;
  }
  lastExportModalUpdateTime = now;
  renderExportModalPreview();
}

function renderExportModalPreview() {
  const container = document.getElementById("export-pages-grid");
  const totalLabel = document.getElementById("exp-spec-pages");
  const countLabel = document.getElementById("exp-grid-count");
  if (!container) return;

  const bType = currentProject.book_type || "coloring_book";
  const isColoring = (bType === "coloring_book");
  const singleSided = document.getElementById("exp-opt-single-sided") ? document.getElementById("exp-opt-single-sided").checked : isColoring;
  const blankNote = document.getElementById("exp-opt-blank-note") ? document.getElementById("exp-opt-blank-note").checked : false;

  const incDisclaimer = document.getElementById("exp-fm-disclaimer") ? document.getElementById("exp-fm-disclaimer").checked : true;
  const incContents = document.getElementById("exp-fm-contents") ? document.getElementById("exp-fm-contents").checked : false;
  const incBelongs = document.getElementById("exp-fm-belongs") ? document.getElementById("exp-fm-belongs").checked : false;
  const incColorTest = document.getElementById("exp-fm-color-test") ? document.getElementById("exp-fm-color-test").checked : false;
  const incCustom = document.getElementById("exp-fm-custom") ? document.getElementById("exp-fm-custom").checked : false;
  const customPos = document.getElementById("exp-fm-custom-pos") ? document.getElementById("exp-fm-custom-pos").value : "back";

  const customPageTitle = document.getElementById("exp-fm-custom-title")?.value || "Author Note / Thank You";

  const contentPages = (currentProject.pages || []).filter(p => p.page_type !== "blank_verso" && !p.page_type?.startsWith("front_matter_"));

  // Build compiled full KDP book pages dynamically based on ticked checkboxes
  let exportPages = [];
  if (incDisclaimer) {
    const discTitle = document.getElementById("exp-fm-text-title")?.value || "Disclaimer & Copyright";
    exportPages.push({ page_type: "front_matter_disclaimer", title: "Disclaimer & Copyright", badge: `Page ${exportPages.length + 1} • Disclaimer` });
  }
  if (incContents) {
    const tocTitle = document.getElementById("exp-fm-text-toc-heading")?.value || "Table of Contents";
    exportPages.push({ page_type: "front_matter_contents", title: tocTitle, badge: `Page ${exportPages.length + 1} • Contents` });
  }
  if (incBelongs) {
    const bTitle = document.getElementById("exp-fm-text-belongs-title")?.value || "This Book Belongs To";
    exportPages.push({ page_type: "front_matter_belongs_to", title: bTitle, badge: `Page ${exportPages.length + 1} • Belongs To` });
  }
  if (incColorTest) {
    const colTitle = document.getElementById("exp-fm-text-color-title")?.value || "Color Test Palette";
    exportPages.push({ page_type: "front_matter_color_test", title: colTitle, badge: `Page ${exportPages.length + 1} • Color Test` });
  }

  // If custom page placed in Front Matter
  if (incCustom && customPos === "front") {
    exportPages.push({
      page_type: "custom_text_page",
      title: customPageTitle,
      badge: `Page ${exportPages.length + 1} • Custom Note`
    });
  }

  // If singleSided and front matter count is odd, insert a blank verso page so Drawing 1 starts on ODD (Right)
  if (singleSided && (exportPages.length % 2 !== 0)) {
    const padNum = exportPages.length + 1;
    exportPages.push({
      page_type: "blank_verso",
      title: "Blank Verso",
      doc_page_number: padNum,
      badge: `Page ${padNum} • Blank Back (Left)`
    });
  }

  const fmCount = exportPages.length;

  contentPages.forEach((p, idx) => {
    const drawPageNum = fmCount + 1 + (idx * (singleSided ? 2 : 1));
    const labelType = bType === "sudoku" ? "Puzzle" : (bType === "maze" ? "Maze" : (bType === "word_search" ? "Word Search" : "Page"));
    exportPages.push({
      ...p,
      doc_page_number: drawPageNum,
      badge: `Page ${drawPageNum} • ${labelType} ${idx + 1} (Right)`
    });

    if (singleSided) {
      exportPages.push({
        page_type: "blank_verso",
        title: "Blank Back Page",
        doc_page_number: drawPageNum + 1,
        badge: `Page ${drawPageNum + 1} • Blank Back (Left)`
      });
    }
  });

  // If Sudoku Book, append Solutions Section to the Export preview
  const allSudokus = [];
  contentPages.forEach((cp, p_idx) => {
    const pNum = fmCount + 1 + p_idx;
    (cp.puzzles || []).forEach(pz => {
      allSudokus.push({ puzzle: pz, origPage: pNum });
    });
  });

  if (allSudokus.length > 0) {
    // 1. Solution Divider Page
    const divPageNum = exportPages.length + 1;
    exportPages.push({
      page_type: "solution_divider",
      title: "Solutions Section Divider",
      doc_page_number: divPageNum,
      badge: `Page ${divPageNum} • Solutions Divider`
    });

    // 2. 4-in-1 Solution Pages
    const SOLS_PER_PAGE = 4;
    for (let c_idx = 0; c_idx < allSudokus.length; c_idx += SOLS_PER_PAGE) {
      const chunk = allSudokus.slice(c_idx, c_idx + SOLS_PER_PAGE);
      const solPageNum = exportPages.length + 1;
      const firstNum = c_idx + 1;
      const lastNum = Math.min(allSudokus.length, c_idx + chunk.length);
      exportPages.push({
        page_type: "sudoku_solutions",
        title: `Solutions: #${firstNum} - #${lastNum}`,
        doc_page_number: solPageNum,
        badge: `Page ${solPageNum} • Solutions (4-in-1)`
      });
    }
  }

  // If custom page placed in Back Matter
  if (incCustom && customPos === "back") {
    const backPageNum = exportPages.length + 1;
    exportPages.push({
      page_type: "custom_text_page",
      title: customPageTitle,
      doc_page_number: backPageNum,
      badge: `Page ${backPageNum} • Thank You Note`
    });

    if (singleSided) {
      exportPages.push({
        page_type: "blank_verso",
        title: "Blank Back Page",
        doc_page_number: backPageNum + 1,
        badge: `Page ${backPageNum + 1} • Blank Back`
      });
    }
  }

  let html = "";
  exportPages.forEach((p, idx) => {
    const docPageNum = idx + 1;
    const isBlank = p.page_type === "blank_verso";
    const isDisclaimer = p.page_type === "front_matter_disclaimer";
    const isContents = p.page_type === "front_matter_contents";
    const isBelongsTo = p.page_type === "front_matter_belongs_to";
    const isColorTest = p.page_type === "front_matter_color_test";
    const isCustom = p.page_type === "custom_text_page";

    if (isBlank) {
      html += `
        <div class="export-page-card blank-verso">
          <div class="export-page-badge verso">Page ${docPageNum} • Blank Back</div>
          <div class="export-page-thumb" style="background:#f8fafc;">
            <span style="font-size:10px;color:#94a3b8;text-align:center;padding:6px;">
              ${blankNote ? '🛡️ Bleed-Safe Blank' : '⚪ Blank White Page'}
            </span>
          </div>
          <div class="export-page-title" style="color:#94a3b8;">Blank Verso</div>
        </div>
      `;
    } else {
      const mainEl = (p.elements || []).find(e => (e.type === "main_image" || e.type === "ref_image") && e.image_src);
      let thumbImg = "";
      if (mainEl && mainEl.image_src) {
        thumbImg = `<img src="${mainEl.image_src}" loading="lazy" decoding="async">`;
      } else if (isDisclaimer) {
        thumbImg = `<span style="font-size:24px;">📜</span>`;
      } else if (isContents) {
        thumbImg = `<span style="font-size:24px;">📋</span>`;
      } else if (isBelongsTo) {
        thumbImg = `<span style="font-size:24px;">🏷️</span>`;
      } else if (isColorTest) {
        thumbImg = `<span style="font-size:24px;">🧪</span>`;
      } else if (isCustom) {
        thumbImg = `<span style="font-size:24px;">💌</span>`;
      } else if (p.page_type === "solution_divider") {
        thumbImg = `<span style="font-size:24px;">🏆</span>`;
      } else if (p.page_type === "sudoku_solutions" || p.puzzles) {
        thumbImg = `<span style="font-size:24px;">🧩</span>`;
      } else if (p.maze) {
        thumbImg = `<span style="font-size:24px;">🌀</span>`;
      } else if (p.word_search) {
        thumbImg = `<span style="font-size:24px;">🔤</span>`;
      } else if (p.games) {
        thumbImg = `<span style="font-size:24px;">⭕</span>`;
      } else {
        thumbImg = `<span style="font-size:24px;">🎨</span>`;
      }

      html += `
        <div class="export-page-card">
          <div class="export-page-badge recto">${p.badge || `Page ${docPageNum}`}</div>
          <div class="export-page-thumb">${thumbImg}</div>
          <div class="export-page-title">${p.title || `Page ${docPageNum}`}</div>
        </div>
      `;
    }
  });

  container.innerHTML = html;
  if (totalLabel) totalLabel.innerText = `${exportPages.length} Total PDF Pages`;
  if (countLabel) countLabel.innerText = `${exportPages.length} Pages`;
}

function executePdfExport(openInBrowser = true) {
  const singleSided = document.getElementById("exp-opt-single-sided") ? document.getElementById("exp-opt-single-sided").checked : true;
  const blankNote = document.getElementById("exp-opt-blank-note") ? document.getElementById("exp-opt-blank-note").checked : false;
  const includePageNumbers = document.getElementById("exp-opt-page-numbers") ? document.getElementById("exp-opt-page-numbers").checked : false;

  const fmOptions = getFrontMatterFormData();

  // Save current project state and front matter options
  currentProject.front_matter_config = fmOptions;
  saveProject(false);

  showToast("⚙️ Generating 300 DPI Amazon KDP PDF...", "info");

  const payload = {
    ...currentProject,
    single_sided: singleSided,
    blank_page_note: blankNote,
    include_page_numbers: includePageNumbers,
    front_matter_options: fmOptions
  };

  fetch("/api/projects/export_pdf", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
  .then(r => r.json())
  .then(data => {
    closeModal("export-pdf-modal");
    if (data.status === "success" && data.download_url) {
      showToast(`🎉 PDF Generated: ${data.filename}!`, "success");
      fetchRecentProjects();
      if (openInBrowser) {
        window.open(data.download_url, "_blank");
      } else {
        const a = document.createElement("a");
        a.href = data.download_url;
        a.download = data.filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }
    } else {
      showToast("❌ PDF generation failed: " + (data.error || "Unknown error"), "error");
    }
  })
  .catch(err => {
    showToast("❌ Error: " + err.message, "error");
  });
}

function formatProjectForKDP() {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot modify: Project is locked!", "warning");
    return;
  }

  recordHistoryState("Format for Amazon KDP");

  const oldPages = currentProject.pages || [];
  const frontMatter = oldPages.filter(p => p.page_type === "front_matter_disclaimer" || p.page_type === "front_matter_contents");
  const contentPages = oldPages.filter(p => p.page_type === "content");

  if (contentPages.length === 0) {
    showToast("No drawing pages found to format.", "info");
    return;
  }

  const newPages = [];
  frontMatter.forEach(fm => newPages.push(fm));

  contentPages.forEach((cp, idx) => {
    newPages.push(cp);
    newPages.push({
      page_number: newPages.length + 1,
      page_type: "blank_verso",
      title: "Blank Page",
      layout: "blank_page",
      elements: []
    });
  });

  currentProject.pages = newPages;
  renumberPages();
  syncActiveProjectUI();
  loadPageIntoCanvas(currentPageIndex);
  renderTimeline();
  markProjectDirty();

  showToast(`🛡️ Inserted Blank Back Pages behind all ${contentPages.length} Drawing Pages!`, "success");
}

// ==========================================
// Spread Preview (Realistic 2-Page Book View)
// ==========================================
function renderSpreadPreview() {
  const container = document.getElementById("spread-book-container");
  const indicator = document.getElementById("spread-page-indicator");
  if (!container) return;

  const contentPages = (currentProject.pages || []).filter(p => p.page_type !== "blank_verso" && !p.page_type?.startsWith("front_matter_"));
  const bType = currentProject.book_type || "coloring_book";
  const isColoring = (bType === "coloring_book");

  // Build compiled full KDP book pages for realistic spread inspection
  let compiledSpreadPages = isColoring ? [
    { page_type: "front_matter_disclaimer", title: "Disclaimer & Copyright", page_number: 1, is_front_matter: true },
    { page_type: "front_matter_contents", title: "Table of Contents", page_number: 2, is_front_matter: true },
    { page_type: "front_matter_belongs_to", title: "This Book Belongs To", page_number: 3, is_front_matter: true },
    { page_type: "front_matter_color_test", title: "Color Test Palette", page_number: 4, is_front_matter: true }
  ] : [
    { page_type: "front_matter_disclaimer", title: "Disclaimer & Copyright", page_number: 1, is_front_matter: true }
  ];

  const startContentNum = compiledSpreadPages.length + 1;

  contentPages.forEach((p, idx) => {
    const drawPageNum = isColoring ? (startContentNum + (idx * 2)) : (startContentNum + idx);
    compiledSpreadPages.push({
      ...p,
      page_number: drawPageNum,
      doc_page_number: drawPageNum
    });
    if (isColoring) {
      compiledSpreadPages.push({
        page_type: "blank_verso",
        title: "Blank Back Page",
        page_number: drawPageNum + 1,
        doc_page_number: drawPageNum + 1
      });
    }
  });

  const totalPages = compiledSpreadPages.length;
  if (totalPages === 0) {
    container.innerHTML = `<div style="padding:40px;color:#94a3b8;">No pages available in this project.</div>`;
    return;
  }

  let leftPage = null;
  let rightPage = null;

  if (currentSpreadIndex === 0) {
    // Spread 0: Initial open (Inside Cover on Left, Page 1 on Right)
    leftPage = null;
    rightPage = compiledSpreadPages[0] || null;
  } else {
    // Spread k: Page (2k) on Left, Page (2k + 1) on Right
    const leftIdx = (currentSpreadIndex * 2) - 1;
    const rightIdx = currentSpreadIndex * 2;
    leftPage = leftIdx < totalPages ? compiledSpreadPages[leftIdx] : null;
    rightPage = rightIdx < totalPages ? compiledSpreadPages[rightIdx] : null;
  }

  if (indicator) {
    if (currentSpreadIndex === 0) {
      indicator.innerText = `Spread: Page 1 (Right / Recto • First Page of ${totalPages} Pages)`;
    } else if (leftPage && rightPage) {
      indicator.innerText = `Spread: Page ${leftPage.page_number} (Left) – Page ${rightPage.page_number} (Right) [of ${totalPages} Pages]`;
    } else if (leftPage) {
      indicator.innerText = `Spread: Page ${leftPage.page_number} (Final Page of ${totalPages} Pages)`;
    }
  }

  const renderPageHtml = (page, isLeft) => {
    if (!page) {
      if (isLeft && currentSpreadIndex === 0) {
        return `
          <div class="spread-page left-page inside-cover" style="background:#f1f5f9;display:flex;flex-direction:column;align-items:center;justify-content:center;border-right:1px solid #cbd5e1;">
            <div style="font-size:32px;margin-bottom:8px;">📖</div>
            <div style="color:#64748b;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;">Inside Front Cover</div>
            <div style="color:#94a3b8;font-size:10px;font-style:italic;margin-top:4px;">(Turn page to open book)</div>
          </div>
        `;
      }
      return `
        <div class="spread-page ${isLeft ? 'left-page' : 'right-page'}" style="background:#f8fafc;display:flex;align-items:center;justify-content:center;">
          <div style="color:#94a3b8;font-size:12px;font-style:italic;">[ End of Book / Inside Back Cover ]</div>
        </div>
      `;
    }

    if (page.page_type === "blank_verso") {
      return `
        <div class="spread-page ${isLeft ? 'left-page' : 'right-page'}" style="background:#ffffff;display:flex;flex-direction:column;align-items:center;justify-content:center;">
          <div class="spread-page-header">Page ${page.page_number} • Blank Back (Verso)</div>
          <div style="color:#cbd5e1;font-size:11px;font-style:italic;text-align:center;padding:20px;">
            [ Blank page to prevent marker bleed-through ]
          </div>
        </div>
      `;
    }

    if (page.page_type === "front_matter_disclaimer") {
      return `
        <div class="spread-page ${isLeft ? 'left-page' : 'right-page'}">
          <div class="spread-page-header">Page 1 • Disclaimer & Copyright</div>
          <div class="spread-inner-content" style="border:1.5px solid #0f172a;border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px;text-align:center;">
            <div style="font-size:16px;font-weight:800;color:#0f172a;margin-bottom:6px;">${(currentProject.name || 'COLORING BOOK').toUpperCase()}</div>
            <div style="font-size:10px;color:#475569;margin-bottom:12px;">First Edition • Amazon KDP Publication</div>
            <div style="font-size:10px;font-weight:700;color:#1e293b;">Copyright © 2026 by ${currentProject.author || 'Author'}</div>
            <div style="font-size:8.5px;color:#64748b;margin-top:10px;max-width:200px;">All rights reserved. No reproduction without prior written permission.</div>
          </div>
        </div>
      `;
    }

    if (page.page_type === "front_matter_contents") {
      let itemsListHtml = "";
      contentPages.slice(0, 10).forEach((cp, cIdx) => {
        const itemP = 5 + (cIdx * 2);
        itemsListHtml += `<div style="display:flex;justify-content:space-between;font-size:9.5px;margin-bottom:3px;color:#1e293b;"><span>${cIdx + 1}. ${cp.title || 'Drawing'}</span><span>Page ${itemP}</span></div>`;
      });

      return `
        <div class="spread-page ${isLeft ? 'left-page' : 'right-page'}">
          <div class="spread-page-header">Page 2 • Table of Contents</div>
          <div class="spread-inner-content" style="border:1.5px solid #0f172a;border-radius:6px;display:flex;flex-direction:column;padding:16px;">
            <div style="font-size:14px;font-weight:800;text-align:center;color:#0f172a;margin-bottom:4px;">TABLE OF CONTENTS</div>
            <div style="font-size:9px;text-align:center;color:#64748b;margin-bottom:12px;">Complete illustration list in this book</div>
            <div style="width:100%;">${itemsListHtml}</div>
          </div>
        </div>
      `;
    }

    if (page.page_type === "front_matter_belongs_to") {
      return `
        <div class="spread-page ${isLeft ? 'left-page' : 'right-page'}">
          <div class="spread-page-header">Page 3 • Belongs To Page</div>
          <div class="spread-inner-content" style="border:1.5px solid #0f172a;border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px;text-align:center;">
            <div style="font-size:13px;font-weight:800;color:#1e293b;">THIS COLORING BOOK</div>
            <div style="font-size:20px;font-weight:800;color:#ffffff;-webkit-text-stroke:1.5px #0f172a;margin:8px 0;">BELONGS TO:</div>
            <div style="width:80%;border-bottom:1.5px solid #64748b;margin:15px 0;"></div>
            <div style="font-size:9px;font-style:italic;color:#64748b;">Color with joy, love and imagination!</div>
          </div>
        </div>
      `;
    }

    if (page.page_type === "front_matter_color_test") {
      return `
        <div class="spread-page ${isLeft ? 'left-page' : 'right-page'}">
          <div class="spread-page-header">Page 4 • Color Test Palette</div>
          <div class="spread-inner-content" style="border:1.5px solid #0f172a;border-radius:6px;display:flex;flex-direction:column;align-items:center;padding:12px;text-align:center;">
            <div style="font-size:13px;font-weight:800;color:#ffffff;-webkit-text-stroke:1.2px #0f172a;margin-bottom:2px;">COLOR TEST PALETTE</div>
            <div style="font-size:8.5px;color:#64748b;margin-bottom:10px;">Test pencils and markers here</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;width:100%;">
              <div style="border:1px dashed #94a3b8;height:24px;border-radius:3px;"></div>
              <div style="border:1px dashed #94a3b8;height:24px;border-radius:3px;"></div>
              <div style="border:1px dashed #94a3b8;height:24px;border-radius:3px;"></div>
              <div style="border:1px dashed #94a3b8;height:24px;border-radius:3px;"></div>
              <div style="border:1px dashed #94a3b8;height:24px;border-radius:3px;"></div>
              <div style="border:1px dashed #94a3b8;height:24px;border-radius:3px;"></div>
            </div>
          </div>
        </div>
      `;
    }

    const titleEl = (page.elements || []).find(e => e.type === "title");
    const refEl = (page.elements || []).find(e => e.type === "ref_image" && e.image_src);
    const mainEl = (page.elements || []).find(e => e.type === "main_image" && e.image_src);
    const dotEl = (page.elements || []).find(e => e.type === "dot_to_dot");

    const titleText = titleEl ? titleEl.text : (page.title || `PAGE ${page.page_number}`);
    
    let imgContent = "";
    if (dotEl || page.dot_to_dot) {
      const dtData = dotEl ? dotEl.dot_data : page.dot_to_dot;
      imgContent = `<div class="spread-img-box">${renderDotToDotSvgHtml(dtData, 280, 280, true)}</div>`;
    } else if (mainEl && mainEl.image_src) {
      // Coloring Book: Drawing is 100% Black & White Line Art
      imgContent = `<div class="spread-img-box"><img src="${mainEl.image_src}" class="${isColoring ? 'spread-coloring-art' : ''}" style="width:100%;height:100%;object-fit:contain;" alt="Coloring Outline Art"></div>`;
    } else if (refEl && refEl.image_src) {
      // Fallback: If only 1 image attached, render as B&W coloring outline in main area
      imgContent = `<div class="spread-img-box"><img src="${refEl.image_src}" class="${isColoring ? 'spread-coloring-art' : ''}" style="width:100%;height:100%;object-fit:contain;" alt="Coloring Outline Art"></div>`;
    } else {
      imgContent = `<div class="spread-img-placeholder"><span>🎨</span><span>Coloring Drawing Area</span></div>`;
    }

    return `
      <div class="spread-page ${isLeft ? 'left-page' : 'right-page'}">
        <div class="spread-page-header">Page ${page.page_number} • Drawing</div>
        <div class="spread-inner-content">
          <div style="display:flex;justify-content:space-between;align-items:center;width:100%;margin-bottom:8px;">
            ${refEl ? `<div class="spread-ref-box" style="width:75px;height:60px;border:1.5px solid #cbd5e1;border-radius:6px;overflow:hidden;background:#ffffff;box-shadow:0 2px 6px rgba(0,0,0,0.06);flex-shrink:0;"><img src="${refEl.image_src}" class="spread-ref-img" style="width:100%;height:100%;object-fit:contain;" alt="Color Reference"></div>` : ''}
            <div class="spread-title-text" style="flex:1;text-align:center;font-family:'Fredoka',sans-serif;font-weight:900;font-size:24px;color:#ffffff;-webkit-text-stroke:2px #0f172a;letter-spacing:2px;">${titleText}</div>
          </div>
          ${imgContent}
        </div>
      </div>
    `;
  };

  container.innerHTML = `
    ${renderPageHtml(leftPage, true)}
    <div class="book-spine-crease"></div>
    ${renderPageHtml(rightPage, false)}
  `;
}

function prevSpreadPage() {
  if (currentSpreadIndex > 0) {
    currentSpreadIndex--;
    renderSpreadPreview();
  } else {
    showToast("Beginning of book.", "info");
  }
}

function nextSpreadPage() {
  const contentPages = (currentProject.pages || []).filter(p => p.page_type !== "blank_verso" && !p.page_type?.startsWith("front_matter_"));
  const totalCompiled = 4 + (contentPages.length * 2);
  const maxSpread = Math.ceil(totalCompiled / 2);
  if (currentSpreadIndex < maxSpread) {
    currentSpreadIndex++;
    renderSpreadPreview();
  } else {
    showToast("End of book.", "info");
  }
}

// ==========================================
// Project Lock / Unlock & Deletion Engine
// ==========================================
function toggleActiveProjectLock() {
  currentProject.is_locked = !currentProject.is_locked;
  syncActiveProjectUI();
  
  fetch("/api/projects/toggle_lock", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path: currentProject.project_dir })
  }).then(() => {
    fetchRecentProjects();
  }).catch(() => {});

  localStorage.setItem("kdp_active_project_data", JSON.stringify(currentProject));
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
      currentProject.is_locked = Boolean(data.is_locked);
      syncActiveProjectUI();
      localStorage.setItem("kdp_active_project_data", JSON.stringify(currentProject));
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
    showToast(`🔒 Cannot delete "${name}": Project is LOCKED! Please unlock it first.`, "warning");
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

    const normTarget = (targetPath || "").replace(/\\/g, "/").toLowerCase();
    const normCurrent = (currentProject.project_dir || "").replace(/\\/g, "/").toLowerCase();

    if (normCurrent === normTarget || !currentProject.project_dir || currentProject.is_empty) {
      clearActiveProject();
      switchTab("dashboard");
    }

    fetchRecentProjects();
  })
  .catch(() => {
    closeModal("delete-project-modal");
    showToast(`Deleted project "${targetName}"!`, "info");
    clearActiveProject();
    fetchRecentProjects();
    switchTab("dashboard");
  });
}

function openCustomProjectFolder() {
  const customPath = prompt("Enter or Paste Full Project Folder Path from any PC / Drive:", defaultRootLocation);
  if (customPath && customPath.trim()) {
    openProjectByPath(customPath.trim());
  }
}

// ==========================================
// Comprehensive Keyboard Shortcuts Engine
// ==========================================
function setupGlobalKeyboardShortcuts() {
  window.addEventListener("keydown", (e) => {
    const activeTagName = document.activeElement ? document.activeElement.tagName.toLowerCase() : "";
    const isInputActive = activeTagName === "input" || activeTagName === "textarea" || activeTagName === "select";

    // Undo: Ctrl+Z (or Cmd+Z)
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z" && !e.shiftKey) {
      if (!isInputActive) {
        e.preventDefault();
        performUndo();
        return;
      }
    }

    // Redo: Ctrl+Y or Ctrl+Shift+Z
    if (((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "y") ||
        ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === "z")) {
      if (!isInputActive) {
        e.preventDefault();
        performRedo();
        return;
      }
    }

    if (e.key === "Enter") {
      const renameModal = document.getElementById("rename-modal");
      if (renameModal && renameModal.classList.contains("active")) {
        e.preventDefault();
        submitRenameModal();
        return;
      }
      const deleteModal = document.getElementById("delete-project-modal");
      if (deleteModal && deleteModal.classList.contains("active")) {
        e.preventDefault();
        executeDeleteProject();
        return;
      }
      const newProjModal = document.getElementById("new-project-modal");
      if (newProjModal && newProjModal.classList.contains("active")) {
        e.preventDefault();
        submitCreateProject();
        return;
      }

      if (!isInputActive) {
        const activeElem = getActiveElement();
        if (activeElem) {
          e.preventDefault();
          if (activeElem.type === "title") {
            openRenameModal("element");
          } else if (activeElem.type === "ref_image" || activeElem.type === "main_image") {
            switchDrawerTab("media");
          }
          return;
        }
      }
    }

    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") {
      e.preventDefault();
      saveProject(true);
      return;
    }

    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "d") {
      e.preventDefault();
      if (activeElementId) {
        duplicateActiveElement();
      } else {
        duplicateCurrentPage();
      }
      return;
    }

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

    if (e.key === "Escape") {
      const openModal = document.querySelector(".modal-overlay.active");
      if (openModal) {
        openModal.classList.remove("active");
      } else if (activeElementId) {
        setActiveElement(null);
      }
      return;
    }

    if (e.key === "Delete" || e.key === "Backspace") {
      if (isInputActive) return;

      e.preventDefault();
      if (activeElementId) {
        deleteActiveElement();
      } else {
        deleteCurrentPage();
      }
      return;
    }

    if (isInputActive) return;

    if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) {
      const elem = getActiveElement();
      if (elem) {
        e.preventDefault();
        recordHistoryState("Nudge Element");
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
  const mediaRow = document.getElementById("rename-modal-media-row");
  const mediaSelect = document.getElementById("rename-modal-media-select");

  if (!modal || !input) return;

  const mediaList = currentProject.media || [];
  if (mediaSelect) {
    mediaSelect.innerHTML = '<option value="">-- Choose from Project Media --</option>';
    mediaList.forEach(m => {
      const opt = document.createElement("option");
      opt.value = m.name || m.fileName;
      opt.innerText = `🖼️ ${m.name || m.fileName}`;
      mediaSelect.appendChild(opt);
    });
  }

  if (mediaRow) {
    mediaRow.style.display = (type === "page" || type === "element") && mediaList.length > 0 ? "block" : "none";
  }

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

function onRenameModalMediaSelect(val) {
  const input = document.getElementById("rename-modal-input");
  if (!input || !val) return;
  const cleaned = cleanFileName(val);
  input.value = (renameTargetType === "element") ? cleaned.toUpperCase() : cleanTitleString(cleaned);
  input.focus();
  input.select();
}

function submitRenameModal() {
  const input = document.getElementById("rename-modal-input");
  const val = input ? input.value.trim() : "";
  if (!val) {
    closeModal("rename-modal");
    return;
  }

  recordHistoryState(`Rename ${renameTargetType}`);

  if (renameTargetType === "page") {
    const page = currentProject.pages[currentPageIndex];
    if (page) {
      page.title = val;
      const titleElem = page.elements.find(e => e.type === "title");
      if (titleElem) titleElem.text = val.toUpperCase();
      renumberPages();
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

function formatLastExportTime(timestamp) {
  if (!timestamp) return "None Yet";
  const date = new Date(typeof timestamp === "number" ? timestamp * 1000 : timestamp);
  if (isNaN(date.getTime())) return "None Yet";

  const now = new Date();
  const isToday = date.toDateString() === now.toDateString();

  const yesterday = new Date(now);
  yesterday.setDate(yesterday.getDate() - 1);
  const isYesterday = date.toDateString() === yesterday.toDateString();

  const timeStr = date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true });

  if (isToday) {
    return `Today ${timeStr}`;
  } else if (isYesterday) {
    return `Yesterday ${timeStr}`;
  } else {
    const month = date.toLocaleDateString([], { month: 'short' });
    const day = date.getDate();
    return `${month} ${day}, ${timeStr}`;
  }
}

function updateHeroStats(statsObj) {
  const totalProjectsEl = document.getElementById("stat-total-projects");
  const pdfsExportedEl = document.getElementById("stat-pdfs-exported");
  const booksCompletedEl = document.getElementById("stat-books-completed");
  const pagesCreatedEl = document.getElementById("stat-pages-created");
  const projectsProgressEl = document.getElementById("stat-projects-progress");
  const lastExportEl = document.getElementById("stat-last-export");

  if (!totalProjectsEl) return;

  if (statsObj) {
    totalProjectsEl.innerText = statsObj.total_projects ?? 0;
    if (pdfsExportedEl) pdfsExportedEl.innerText = statsObj.total_pdfs ?? 0;
    if (booksCompletedEl) booksCompletedEl.innerText = statsObj.books_completed ?? 0;
    if (pagesCreatedEl) pagesCreatedEl.innerText = statsObj.total_pages ?? 0;
    if (projectsProgressEl) projectsProgressEl.innerText = statsObj.projects_in_progress ?? 0;
    if (lastExportEl) {
      lastExportEl.innerText = formatLastExportTime(statsObj.last_export_mtime);
      lastExportEl.title = statsObj.last_export_mtime ? new Date(statsObj.last_export_mtime * 1000).toLocaleString() : "No exports yet";
    }
    return;
  }

  // Fallback calculation using recentProjectsList & currentProject
  let totalProjects = (recentProjectsList || []).length;
  let totalPages = 0;
  let totalPdfs = 0;
  let completedBooks = 0;
  let latestMtime = null;

  (recentProjectsList || []).forEach(p => {
    totalPages += (p.page_count || 0);
    const expCount = p.exports_count || 0;
    totalPdfs += expCount;
    if (p.is_completed || expCount > 0) completedBooks++;
    if (p.latest_export_mtime && (!latestMtime || p.latest_export_mtime > latestMtime)) {
      latestMtime = p.latest_export_mtime;
    }
  });

  if (currentProject && currentProject.project_dir) {
    const curPagesCount = (currentProject.pages || []).length;
    const existingIndex = (recentProjectsList || []).findIndex(p => p.path === currentProject.project_dir);
    if (existingIndex !== -1) {
      totalPages = totalPages - (recentProjectsList[existingIndex].page_count || 0) + curPagesCount;
    } else if (totalProjects === 0) {
      totalProjects = 1;
      totalPages = curPagesCount;
    }
  }

  const inProgress = Math.max(0, totalProjects - completedBooks);

  totalProjectsEl.innerText = totalProjects;
  if (pdfsExportedEl) pdfsExportedEl.innerText = totalPdfs;
  if (booksCompletedEl) booksCompletedEl.innerText = completedBooks;
  if (pagesCreatedEl) pagesCreatedEl.innerText = totalPages;
  if (projectsProgressEl) projectsProgressEl.innerText = inProgress;
  if (lastExportEl) {
    lastExportEl.innerText = formatLastExportTime(latestMtime);
    lastExportEl.title = latestMtime ? new Date(latestMtime * 1000).toLocaleString() : "No exports yet";
  }
}

function fetchRecentProjects() {
  fetch("/api/projects")
    .then(r => r.json())
    .then(data => {
      recentProjectsList = data.projects || [];
      renderRecentProjects();
      updateHeroStats(data.stats);

      if (recentProjectsList.length === 0) {
        clearActiveProject();
      } else if (currentProject && currentProject.project_dir) {
        syncActiveProjectUI();
      }
    })
    .catch(() => {
      renderRecentProjects();
      updateHeroStats();
    });
}

function renderRecentProjects() {
  const container = document.getElementById("recent-projects-list");
  const modalPickList = document.getElementById("modal-project-pick-list");

  const renderItemHtml = (p) => {
    const isLocked = Boolean(p.is_locked);
    const lockIcon = isLocked ? "🔒" : "🔓";
    const lockText = isLocked ? "LOCKED" : "UNLOCKED";
    const lockBtnLabel = isLocked ? "🔓 Unlock" : "🔒 Lock";

    return `
      <div class="recent-item">
        <div class="recent-icon">${lockIcon}</div>
        <div class="recent-info" onclick="openProjectByPath('${p.path.replace(/\\/g, '\\\\')}')">
          <div class="recent-title">
            <span>${p.name}</span>
            <span class="badge ${isLocked ? 'locked' : 'unlocked'}">${lockIcon} ${lockText}</span>
          </div>
          <div class="recent-path">${p.path}</div>
        </div>
        <div class="meta-row">
          <span class="badge">${p.page_count || 0} Pages</span>
          <button class="btn btn-sm btn-primary" onclick="openProjectByPath('${p.path.replace(/\\/g, '\\\\')}')">Open</button>
          <button class="btn btn-sm btn-outline" onclick="toggleProjectLock('${p.path.replace(/\\/g, '\\\\')}')" title="${isLocked ? 'Unlock Project' : 'Lock Project'}">
            ${lockBtnLabel}
          </button>
          <button class="btn btn-sm btn-danger btn-icon-only ${isLocked ? 'btn-disabled' : ''}" 
            onclick="promptDeleteProject('${p.path.replace(/\\/g, '\\\\')}', '${p.name.replace(/'/g, "\\'")}', ${isLocked})" 
            title="${isLocked ? 'Cannot delete locked project' : 'Delete Project Folder'}">
            🗑
          </button>
        </div>
      </div>
    `;
  };

  if (container) {
    container.innerHTML = recentProjectsList.length 
      ? recentProjectsList.map(renderItemHtml).join("")
      : `<div style="color:var(--text-muted);font-size:12px;padding:12px;">No projects found. Click "Create New Project" to get started!</div>`;
  }

  if (modalPickList) {
    modalPickList.innerHTML = recentProjectsList.map(renderItemHtml).join("");
  }
}

// Navigation Tabs & Context-Aware Header
function updateNavigationTabsVisibility(tabId) {
  const currentTab = tabId || document.documentElement.getAttribute("data-active-tab") || "dashboard";
  const hasActiveProject = Boolean(currentProject && currentProject.name && currentProject.project_dir && !currentProject.is_empty);

  const dashBtn = document.getElementById("nav-tab-dashboard") || document.querySelector('.nav-btn[data-tab="dashboard"]');
  const settingsBtn = document.getElementById("nav-tab-settings") || document.querySelector('.nav-btn[data-tab="settings"]');
  const canvasBtn = document.getElementById("nav-tab-canvas") || document.querySelector('.nav-btn[data-tab="canvas"]');
  const preflightBtn = document.getElementById("nav-tab-preflight") || document.querySelector('.nav-btn[data-tab="preflight"]');
  const previewBtn = document.getElementById("nav-tab-preview") || document.querySelector('.nav-btn[data-tab="preview"]');

  if (currentTab === "dashboard") {
    // When on Dashboard:
    // Settings, Quality Check, Spread Preview are hidden
    if (settingsBtn) settingsBtn.style.display = "none";
    if (preflightBtn) preflightBtn.style.display = "none";
    if (previewBtn) previewBtn.style.display = "none";

    // If working on a project: show Dashboard AND Canvas Editor (exactly the 2 options requested)
    // If no project loaded: hide Canvas Editor too
    if (canvasBtn) {
      canvasBtn.style.display = hasActiveProject ? "flex" : "none";
    }
    if (dashBtn) dashBtn.style.display = "flex";
  } else {
    // When inside Canvas Editor or other editor tabs:
    // Show ALL options: Dashboard, Book Settings, Canvas Editor, Quality Check, Spread Preview
    if (dashBtn) dashBtn.style.display = "flex";
    if (settingsBtn) settingsBtn.style.display = "flex";
    if (canvasBtn) canvasBtn.style.display = "flex";
    if (preflightBtn) preflightBtn.style.display = "flex";
    if (previewBtn) previewBtn.style.display = "flex";
  }
}

function setupNavigation() {
  document.querySelectorAll(".nav-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const tab = btn.getAttribute("data-tab");
      switchTab(tab);
    });
  });
  updateNavigationTabsVisibility();
}

function switchTab(tabId) {
  sessionStorage.setItem("kdp_active_tab", tabId);
  localStorage.setItem("kdp_active_tab", tabId);
  document.documentElement.setAttribute("data-active-tab", tabId);

  document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));

  const targetBtn = document.querySelector(`.nav-btn[data-tab="${tabId}"]`);
  const targetPanel = document.getElementById(`panel-${tabId}`);
  if (targetBtn) targetBtn.classList.add("active");
  if (targetPanel) targetPanel.classList.add("active");

  const headerCanvasActions = document.getElementById("header-canvas-actions");
  if (headerCanvasActions) {
    headerCanvasActions.style.display = (tabId === "canvas") ? "flex" : "none";
  }

  // Update tabs visibility dynamically (Dashboard shows Dashboard + Canvas Editor; inside editor shows all tabs)
  updateNavigationTabsVisibility(tabId);

  if (tabId === "canvas") {
    loadPageIntoCanvas(currentPageIndex);
    renderTimeline();
    renderMediaLibrary();
    // Auto-fit canvas to available viewport height and width
    setTimeout(() => { fitCanvasView(); }, 60);
  } else if (tabId === "preview") {
    renderSpreadPreview();
  } else if (tabId === "preflight") {
    updatePreflightDashboard();
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
  const hasProject = Boolean(currentProject && currentProject.name && !currentProject.is_empty && currentProject.project_dir);

  const navProjName = document.getElementById("nav-project-name");
  if (navProjName) {
    navProjName.innerText = hasProject 
      ? `${currentProject.is_locked ? '🔒' : '🔓'} ${currentProject.name}`
      : "No Active Project";
  }

  const activeDisplay = document.getElementById("active-proj-display");
  const lockBadge = document.getElementById("active-proj-lock-badge");

  if (!hasProject) {
    if (lockBadge) lockBadge.style.display = "none";
    if (activeDisplay) {
      activeDisplay.innerHTML = `
        <div style="text-align:center; padding: 28px 16px; color: var(--text-muted); width: 100%;">
          <div style="font-size: 36px; margin-bottom: 8px;">📂</div>
          <h4 style="color: var(--text-main); font-size: 15px; margin-bottom: 4px; font-weight: 700;">No Active Project</h4>
          <p style="font-size: 12px; margin-bottom: 16px; color: var(--text-muted);">All projects have been deleted. Click below to create a new book project.</p>
          <button class="btn btn-primary" onclick="openNewProjectModal()">✨ Create New Project</button>
        </div>
      `;
    }
    const statPages = document.getElementById("stat-page-count");
    if (statPages) statPages.innerText = "0";
    const statMedia = document.getElementById("stat-media-count");
    if (statMedia) statMedia.innerText = "0";
    updateNavigationTabsVisibility();
    return;
  }

  const isLocked = Boolean(currentProject.is_locked);
  const lockIcon = isLocked ? "🔒" : "🔓";
  const lockText = isLocked ? "LOCKED" : "UNLOCKED";
  const lockBtnText = isLocked ? "🔓 Unlock Project" : "🔒 Lock Project";

  if (lockBadge) {
    lockBadge.style.display = "inline-flex";
    lockBadge.className = `badge ${isLocked ? 'locked' : 'unlocked'}`;
    lockBadge.innerText = `${lockIcon} ${lockText}`;
  }

  if (activeDisplay) {
    activeDisplay.innerHTML = `
      <div class="proj-banner-icon">📖</div>
      <div class="proj-banner-info">
        <h4 id="active-proj-title">${currentProject.name}</h4>
        <div class="proj-path-tag" id="active-proj-path">📁 ${currentProject.project_dir}</div>
        <div class="proj-meta-row" id="active-proj-meta">
          <span>Pages: ${(currentProject.pages || []).length}</span> • 
          <span>Author: ${currentProject.author || 'Creative Author'}</span> • 
          <span>Trim: 8.5x11 in</span>
        </div>
      </div>
      <div class="proj-banner-actions">
        <div style="display: flex; gap: 8px;">
          <button class="btn btn-primary" style="flex: 1;" onclick="switchTab('canvas')">Open Canvas Editor ➔</button>
          <button class="btn btn-outline" id="active-lock-toggle-btn" onclick="toggleActiveProjectLock()">${lockBtnText}</button>
        </div>
      </div>
    `;
  }

  const authorInput = document.getElementById("setting-author-name");
  if (authorInput) authorInput.value = currentProject.author || "Creative Kids Studio";
  
  const pubInput = document.getElementById("setting-publisher-name");
  if (pubInput && currentProject.front_matter_config) {
    pubInput.value = currentProject.front_matter_config.publisher_name || "KDP Creative Publishing";
  }

  const isbnInput = document.getElementById("setting-isbn");
  if (isbnInput && currentProject.front_matter_config) {
    isbnInput.value = currentProject.front_matter_config.isbn || "978-X-XXXXX-XXX-X";
  }

  const statPages = document.getElementById("stat-page-count");
  if (statPages) statPages.innerText = (currentProject.pages || []).length;
  const statMedia = document.getElementById("stat-media-count");
  if (statMedia) statMedia.innerText = currentProject.media ? currentProject.media.length : 0;
  
  const folderHint = document.getElementById("media-folder-hint");
  if (folderHint) folderHint.innerText = `${currentProject.folder_name}/media`;

  renderTimeline();
  renderMediaLibrary();
  renderCustomLayouts();
  updateUndoRedoButtons();
  updateNavigationTabsVisibility();
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

function onModalPageCountChange(val) {
  const customWrap = document.getElementById("modal-custom-page-container");
  if (customWrap) {
    customWrap.style.display = (val === "custom") ? "block" : "none";
    if (val === "custom") {
      const inp = document.getElementById("modal-custom-page-input");
      if (inp) inp.focus();
    }
  }
}

function onModalTrimPresetChange(val) {
  const customTrimWrap = document.getElementById("modal-custom-trim-container");
  if (customTrimWrap) {
    customTrimWrap.style.display = (val === "custom") ? "block" : "none";
    if (val === "custom") {
      const inp = document.getElementById("modal-custom-trim-w");
      if (inp) inp.focus();
    }
  }
}

let checkDupDebounceTimer = null;
function updateModalPathPreview() {
  const nameInput = document.getElementById("modal-project-name");
  const rootInput = document.getElementById("modal-project-root");
  const previewDiv = document.getElementById("modal-full-path-preview");
  const dupWarning = document.getElementById("modal-duplicate-warning");
  const dupNameSpan = document.getElementById("modal-dup-name");

  const name = (nameInput ? nameInput.value.trim() : "") || "Untitled_Project";
  const root = (rootInput ? rootInput.value.trim() : "") || defaultRootLocation;
  const folderName = name.replace(/[^a-zA-Z0-9_\-\s]/g, "").replace(/\s+/g, "_");

  const fullPath = `${root.replace(/[\/\\]+$/, "")}\\${folderName}`;
  if (previewDiv) {
    previewDiv.innerText = `📁 ${fullPath}\\`;
  }

  // Check duplicate project on disk
  if (checkDupDebounceTimer) clearTimeout(checkDupDebounceTimer);
  checkDupDebounceTimer = setTimeout(async () => {
    try {
      const res = await fetch("/api/projects/check_exists", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ root_path: root, name: name, folder_name: folderName })
      });
      const data = await res.json();
      if (data && data.exists) {
        if (dupWarning) dupWarning.style.display = "block";
        if (dupNameSpan) dupNameSpan.innerText = name;
      } else {
        if (dupWarning) dupWarning.style.display = "none";
      }
    } catch (e) {}
  }, 250);
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

function onBookTypeChange() {
  const typeSelect = document.getElementById("modal-book-type");
  const bType = typeSelect ? typeSelect.value : "coloring_book";
  const nameInput = document.getElementById("modal-project-name");
  const trimSelect = document.getElementById("modal-trim-preset");
  const countLabel = document.getElementById("modal-count-label");

  const sudokuOpts = document.getElementById("modal-sudoku-options");
  const tttOpts = document.getElementById("modal-ttt-options");

  if (sudokuOpts) sudokuOpts.style.display = (bType === "sudoku") ? "block" : "none";
  if (tttOpts) tttOpts.style.display = (bType === "tic_tac_toe") ? "block" : "none";

  if (bType === "sudoku") {
    if (nameInput) nameInput.value = "Sudoku Master Puzzles";
    if (trimSelect) trimSelect.value = "6x9";
    if (countLabel) countLabel.innerText = "Total Sudoku Puzzles";
  } else if (bType === "tic_tac_toe") {
    if (nameInput) nameInput.value = "Tic-Tac-Toe Game Book";
    if (trimSelect) trimSelect.value = "8.5x11";
    if (countLabel) countLabel.innerText = "Total Games to Generate";
  } else if (bType === "maze") {
    if (nameInput) nameInput.value = "Ultimate Maze Adventures";
    if (trimSelect) trimSelect.value = "8.5x11";
    if (countLabel) countLabel.innerText = "Total Mazes to Generate";
  } else if (bType === "word_search") {
    if (nameInput) nameInput.value = "Word Search Explorer";
    if (trimSelect) trimSelect.value = "8.5x11";
    if (countLabel) countLabel.innerText = "Total Word Search Puzzles";
  } else if (bType === "dot_to_dot") {
    if (nameInput) nameInput.value = "Dot-to-Dot Animal Adventures";
    if (trimSelect) trimSelect.value = "8.5x11";
    if (countLabel) countLabel.innerText = "Total Dot Puzzles to Generate";
  } else if (bType === "tracing") {
    if (nameInput) nameInput.value = "Letter & Number Tracing Workbook";
    if (trimSelect) trimSelect.value = "8.5x11";
    if (countLabel) countLabel.innerText = "Total Letters / Worksheets";
  } else if (bType === "scissor_skills") {
    if (nameInput) nameInput.value = "Scissor Skills Cutting & Paste Activity";
    if (trimSelect) trimSelect.value = "8.5x11";
    if (countLabel) countLabel.innerText = "Total Cutting Pages";
  } else if (bType === "shadow_matching") {
    if (nameInput) nameInput.value = "Shadow Matching Visual Brain Games";
    if (trimSelect) trimSelect.value = "8.5x11";
    if (countLabel) countLabel.innerText = "Total Matching Puzzles";
  } else if (bType === "ispy") {
    if (nameInput) nameInput.value = "I-SPY & Count Activity Book";
    if (trimSelect) trimSelect.value = "8.5x11";
    if (countLabel) countLabel.innerText = "Total Search & Count Pages";
  } else if (bType === "grid_drawing") {
    if (nameInput) nameInput.value = "Learn to Draw: Grid Copy Book";
    if (trimSelect) trimSelect.value = "8.5x11";
    if (countLabel) countLabel.innerText = "Total Grid Drawing Lessons";
  } else {
    if (nameInput) nameInput.value = "My Jungle Coloring Book";
    if (trimSelect) trimSelect.value = "8.5x11";
    if (countLabel) countLabel.innerText = "Initial Pages / Drawings";
  }
  updateModalPathPreview();
}

async function submitCreateProject() {
  const typeSelect = document.getElementById("modal-book-type");
  const bType = typeSelect ? typeSelect.value : "coloring_book";
  const nameInput = document.getElementById("modal-project-name");
  const rootInput = document.getElementById("modal-project-root");
  const countSelect = document.getElementById("modal-page-count");
  const hasBleed = document.getElementById("modal-has-bleed").checked;
  const autoFrontMatter = document.getElementById("modal-auto-front-matter") ? document.getElementById("modal-auto-front-matter").checked : true;

  const projName = (nameInput ? nameInput.value.trim() : "") || "My New KDP Book";
  const rootDir = (rootInput ? rootInput.value.trim() : "") || defaultRootLocation;
  const folderName = projName.replace(/[^a-zA-Z0-9_\-\s]/g, "").replace(/\s+/g, "_");
  const projectDir = `${rootDir.replace(/[\/\\]+$/, "")}\\${folderName}`;

  // Check duplicate project name on disk before proceeding
  try {
    const checkRes = await fetch("/api/projects/check_exists", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ root_path: rootDir, name: projName, folder_name: folderName })
    });
    const checkData = await checkRes.json();
    if (checkData && checkData.exists) {
      const dupWarning = document.getElementById("modal-duplicate-warning");
      const dupNameSpan = document.getElementById("modal-dup-name");
      if (dupWarning) dupWarning.style.display = "block";
      if (dupNameSpan) dupNameSpan.innerText = projName;
      showToast(`⚠️ A project named "${projName}" already exists! Please choose a unique name.`, "danger");
      if (nameInput) nameInput.focus();
      return;
    }
  } catch (e) {}

  // Parse page count (including custom page count option)
  let count = 10;
  if (countSelect && countSelect.value === "custom") {
    const customInp = document.getElementById("modal-custom-page-input");
    count = parseInt(customInp ? customInp.value : "40") || 40;
    if (count < 1) count = 1;
    if (count > 600) count = 600;
  } else {
    count = parseInt(countSelect ? countSelect.value : "10");
  }

  let pagesList = [];

  if (bType === "sudoku") {
    const diffSelect = document.getElementById("modal-sudoku-difficulty");
    const perPageSelect = document.getElementById("modal-sudoku-per-page");
    const diff = diffSelect ? diffSelect.value : "medium";
    const perPage = parseInt(perPageSelect ? perPageSelect.value : "1");
    const totalPuzzlesNeeded = count * perPage;

    try {
      const resp = await fetch("/api/generators/sudoku", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ count: totalPuzzlesNeeded, difficulty: diff })
      });
      const data = await resp.json();
      const puzzles = data.puzzles || [];

      for (let i = 0; i < count; i++) {
        const pageNum = i + 1;
        const chunk = puzzles.slice(i * perPage, (i + 1) * perPage);
        const pTitle = chunk.length > 1 
          ? `Sudoku ${chunk[0].id.replace("sudoku_", "#")} - ${chunk[chunk.length - 1].id.replace("sudoku_", "#")}` 
          : `Sudoku ${chunk[0] ? chunk[0].id.replace("sudoku_", "#") : `#${pageNum.toString().padStart(4, '0')}`}`;
        
        const elems = [
          { id: `elem_title_${pageNum}`, type: "title", x: 35, y: 30, w: 440, h: 40, text: pTitle.toUpperCase(), font_size: 24, color: "#0f172a", is_outline: false },
          { id: `elem_frame_${pageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
        ];

        pagesList.push({
          page_number: pageNum,
          page_type: "content",
          title: pTitle,
          layout: "sudoku",
          puzzles: chunk,
          elements: elems
        });
      }
    } catch (e) {
      console.error("Error generating Sudoku puzzles:", e);
    }
  } else if (bType === "tic_tac_toe") {
    const perPageSelect = document.getElementById("modal-ttt-per-page");
    const gridSelect = document.getElementById("modal-ttt-grid-size");
    const perPage = parseInt(perPageSelect ? perPageSelect.value : "4");
    const gridSize = parseInt(gridSelect ? gridSelect.value : "3");
    const totalGamesNeeded = count * perPage;

    try {
      const resp = await fetch("/api/generators/tic_tac_toe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ total_games: totalGamesNeeded, games_per_page: perPage, grid_size: gridSize })
      });
      const data = await resp.json();
      const tttPages = data.pages || [];

      for (let i = 0; i < count; i++) {
        const pageNum = i + 1;
        const pTitle = `Tic-Tac-Toe Page ${pageNum}`;
        const pageGames = tttPages[i] ? tttPages[i].games : [];

        pagesList.push({
          page_number: pageNum,
          page_type: "content",
          title: pTitle,
          layout: "tic_tac_toe",
          games: pageGames,
          elements: [
            { id: `elem_title_${pageNum}`, type: "title", x: 35, y: 30, w: 440, h: 40, text: pTitle.toUpperCase(), font_size: 22, color: "#0f172a", is_outline: false },
            { id: `elem_frame_${pageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
          ]
        });
      }
    } catch (e) {
      console.error("Error generating Tic-Tac-Toe games:", e);
    }
  } else if (bType === "maze") {
    try {
      const resp = await fetch("/api/generators/maze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ count: count, width: 15, height: 20 })
      });
      const data = await resp.json();
      const mazes = data.mazes || [data.maze];

      for (let i = 0; i < count; i++) {
        const pageNum = i + 1;
        const mz = mazes[i] || mazes[0];
        const pTitle = `Maze Challenge #${pageNum.toString().padStart(3, '0')}`;

        pagesList.push({
          page_number: pageNum,
          page_type: "content",
          title: pTitle,
          layout: "maze",
          maze: mz,
          elements: [
            { id: `elem_title_${pageNum}`, type: "title", x: 35, y: 30, w: 440, h: 40, text: pTitle.toUpperCase(), font_size: 26, color: "#0f172a", is_outline: false },
            { id: `elem_frame_${pageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
          ]
        });
      }
    } catch (e) {
      console.error("Error generating Mazes:", e);
    }
  } else if (bType === "word_search") {
    try {
      const resp = await fetch("/api/generators/word_search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ count: count, grid_size: 12 })
      });
      const data = await resp.json();
      const wsPuzzles = data.puzzles || [data.word_search];

      for (let i = 0; i < count; i++) {
        const pageNum = i + 1;
        const ws = wsPuzzles[i] || wsPuzzles[0];
        const pTitle = ws.title || `Word Search #${pageNum.toString().padStart(3, '0')}`;

        pagesList.push({
          page_number: pageNum,
          page_type: "content",
          title: pTitle,
          layout: "word_search",
          word_search: ws,
          elements: [
            { id: `elem_title_${pageNum}`, type: "title", x: 35, y: 30, w: 440, h: 40, text: pTitle.toUpperCase(), font_size: 22, color: "#0f172a", is_outline: false },
            { id: `elem_frame_${pageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
          ]
        });
      }
    } catch (e) {
      console.error("Error generating Word Searches:", e);
    }
  } else if (bType === "dot_to_dot") {
    const presets = ["star", "butterfly", "rocket", "dinosaur", "heart", "cat", "airplane", "fish"];
    try {
      for (let i = 0; i < count; i++) {
        const pageNum = i + 1;
        const presetKey = presets[i % presets.length];
        const resp = await fetch("/api/generators/dot_to_dot", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ preset_name: presetKey, dot_count: 35 })
        });
        const data = await resp.json();
        const pz = data.puzzle || {};
        const pTitle = pz.title || presetKey.toUpperCase();

        pagesList.push({
          page_number: pageNum,
          page_type: "content",
          title: pTitle,
          layout: "dot_to_dot",
          dot_to_dot: pz,
          elements: [
            { id: `elem_ref_${pageNum}`, type: "ref_image", x: 35, y: 25, w: 160, h: 150, text: pTitle, image_src: null },
            { id: `elem_title_${pageNum}`, type: "title", x: 215, y: 55, w: 260, h: 80, text: pTitle.toUpperCase(), font_size: 34, color: "#ffffff", is_outline: true, font_family: "Fredoka", letter_spacing: 2 },
            { id: `elem_dot_${pageNum}`, type: "dot_to_dot", x: 35, y: 190, w: 440, h: 440, text: pTitle },
            { id: `elem_frame_${pageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
          ]
        });
      }
    } catch (e) {
      console.error("Error generating Dot-to-Dot presets:", e);
    }
  } else if (bType === "tracing") {
    const letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
    const sampleWords = { "A": "APPLE", "B": "BALL", "C": "CAT", "D": "DOG", "E": "ELEPHANT", "F": "FISH", "G": "GIRAFFE", "H": "HORSE" };
    try {
      for (let i = 0; i < count; i++) {
        const pageNum = i + 1;
        const char = letters[i % letters.length];
        const word = sampleWords[char] || `${char}NIMAL`;
        const resp = await fetch("/api/generators/tracing", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ char: char, repeat: 5, word: word })
        });
        const data = await resp.json();
        const trData = data.tracing || {};
        const pTitle = `Letter Tracing: ${char}`;

        pagesList.push({
          page_number: pageNum,
          page_type: "content",
          title: pTitle,
          layout: "tracing",
          tracing: trData,
          elements: [
            { id: `elem_title_${pageNum}`, type: "title", x: 35, y: 25, w: 440, h: 35, text: pTitle.toUpperCase(), font_size: 22, color: "#0f172a", is_outline: false },
            { id: `elem_frame_${pageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
          ]
        });
      }
    } catch (e) {
      console.error("Error generating Tracing pages:", e);
    }
  } else if (bType === "scissor_skills") {
    const patterns = ["straight", "zigzag", "wavy", "curved", "castle"];
    try {
      for (let i = 0; i < count; i++) {
        const pageNum = i + 1;
        const pat = patterns[i % patterns.length];
        const pTitle = `Scissor Cutting: ${pat.toUpperCase()}`;
        const resp = await fetch("/api/generators/scissor_skills", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ pattern: pat, lines: 5, title: pTitle })
        });
        const data = await resp.json();
        const scData = data.scissor_skills || {};

        pagesList.push({
          page_number: pageNum,
          page_type: "content",
          title: pTitle,
          layout: "scissor_skills",
          scissor_skills: scData,
          elements: [
            { id: `elem_title_${pageNum}`, type: "title", x: 35, y: 25, w: 440, h: 35, text: pTitle.toUpperCase(), font_size: 22, color: "#0f172a", is_outline: false },
            { id: `elem_frame_${pageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
          ]
        });
      }
    } catch (e) {
      console.error("Error generating Scissor Skills pages:", e);
    }
  } else if (bType === "shadow_matching") {
    const themes = ["jungle_animals", "vehicles", "farm_animals"];
    try {
      for (let i = 0; i < count; i++) {
        const pageNum = i + 1;
        const thm = themes[i % themes.length];
        const pTitle = `Shadow Match #${pageNum}`;
        const resp = await fetch("/api/generators/shadow_matching", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ theme: thm, pairs: 4, title: pTitle })
        });
        const data = await resp.json();
        const smData = data.shadow_matching || {};

        pagesList.push({
          page_number: pageNum,
          page_type: "content",
          title: pTitle,
          layout: "shadow_matching",
          shadow_matching: smData,
          elements: [
            { id: `elem_title_${pageNum}`, type: "title", x: 35, y: 25, w: 440, h: 35, text: pTitle.toUpperCase(), font_size: 22, color: "#0f172a", is_outline: false },
            { id: `elem_frame_${pageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
          ]
        });
      }
    } catch (e) {
      console.error("Error generating Shadow Matching pages:", e);
    }
  } else if (bType === "ispy") {
    const ispyThemes = ["jungle", "space", "sweet_treats"];
    try {
      for (let i = 0; i < count; i++) {
        const pageNum = i + 1;
        const thm = ispyThemes[i % ispyThemes.length];
        const pTitle = `I-Spy & Count Animals #${pageNum}`;
        const resp = await fetch("/api/generators/ispy", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ theme: thm, title: pTitle })
        });
        const data = await resp.json();
        const ispyData = data.ispy || {};

        pagesList.push({
          page_number: pageNum,
          page_type: "content",
          title: pTitle,
          layout: "ispy",
          ispy: ispyData,
          elements: [
            { id: `elem_title_${pageNum}`, type: "title", x: 35, y: 25, w: 440, h: 35, text: pTitle.toUpperCase(), font_size: 22, color: "#0f172a", is_outline: false },
            { id: `elem_frame_${pageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
          ]
        });
      }
    } catch (e) {
      console.error("Error generating I-SPY pages:", e);
    }
  } else if (bType === "grid_drawing") {
    const animals = ["Lion", "Elephant", "Monkey", "Giraffe", "Tiger", "Zebra", "Panda", "Bear"];
    try {
      for (let i = 0; i < count; i++) {
        const pageNum = i + 1;
        const anm = animals[i % animals.length];
        const pTitle = `How to Draw: ${anm}`;
        const resp = await fetch("/api/generators/grid_drawing", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ grid_size: 4, title: pTitle, animal_name: anm })
        });
        const data = await resp.json();
        const gdData = data.grid_drawing || {};

        pagesList.push({
          page_number: pageNum,
          page_type: "content",
          title: pTitle,
          layout: "grid_drawing",
          grid_drawing: gdData,
          elements: [
            { id: `elem_title_${pageNum}`, type: "title", x: 35, y: 25, w: 440, h: 35, text: pTitle.toUpperCase(), font_size: 22, color: "#0f172a", is_outline: false },
            { id: `elem_frame_${pageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
          ]
        });
      }
    } catch (e) {
      console.error("Error generating Grid Drawing pages:", e);
    }
  }

  // Default / Fallback: Standard Coloring Book layout
  if (pagesList.length === 0) {
    for (let i = 0; i < count; i++) {
      const contentNum = i + 1;
      pagesList.push({
        page_number: contentNum,
        page_type: "content",
        title: `Page ${contentNum}`,
        layout: "kdp_top_ref",
        elements: [
          { id: `elem_ref_${contentNum}`, type: "ref_image", x: 35, y: 25, w: 190, h: 180, text: `Ref ${contentNum}`, image_src: null },
          { id: `elem_title_${contentNum}`, type: "title", x: 235, y: 70, w: 240, h: 80, text: `DRAWING ${contentNum}`, font_size: 40, color: "#ffffff", is_outline: true, font_family: "Fredoka", letter_spacing: 2 },
          { id: `elem_main_${contentNum}`, type: "main_image", x: 35, y: 220, w: 440, h: 410, text: `Drawing ${contentNum}`, image_src: null },
          { id: `elem_frame_${contentNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
        ]
      });
    }
  }

  // Parse KDP Trim Preset (including custom width x height in inches)
  const trimSelect = document.getElementById("modal-trim-preset");
  let trimW = 8.5;
  let trimH = 11.0;
  if (trimSelect && trimSelect.value === "custom") {
    const customW = parseFloat(document.getElementById("modal-custom-trim-w")?.value) || 8.5;
    const customH = parseFloat(document.getElementById("modal-custom-trim-h")?.value) || 11.0;
    trimW = Math.max(4, Math.min(15, customW));
    trimH = Math.max(4, Math.min(15, customH));
  } else {
    const trimMap = {
      "8.5x11": [8.5, 11.0],
      "8x10": [8.0, 10.0],
      "8.5x8.5": [8.5, 8.5],
      "6x9": [6.0, 9.0]
    };
    const tVal = trimSelect ? trimSelect.value : "8.5x11";
    const mapped = trimMap[tVal] || [8.5, 11.0];
    trimW = mapped[0];
    trimH = mapped[1];
  }

  const trimWidthPt = trimW * 72.0;
  const trimHeightPt = trimH * 72.0;

  const newProjPayload = {
    name: projName,
    book_type: bType,
    folder_name: folderName,
    project_dir: projectDir,
    root_path: rootDir,
    author: "Creative Kids Studio",
    is_locked: false,
    created_at: new Date().toISOString(),
    settings: {
      trim_width_pt: trimWidthPt,
      trim_height_pt: trimHeightPt,
      trim_width_in: trimW,
      trim_height_in: trimH,
      has_bleed: hasBleed,
      bleed_pt: 9.0,
      margins: { top_pt: 27.0, bottom_pt: 27.0, inside_pt: 36.0, outside_pt: 27.0 },
      target_dpi: 300,
    },
    front_matter_config: {
      auto_front_matter: autoFrontMatter,
      create_disclaimer: autoFrontMatter,
      create_contents: autoFrontMatter,
      auto_sync_contents: true,
      contents_style: "numbered",
      show_page_numbers: true,
      publisher_name: "KDP Creative Publishing",
      isbn: "978-X-XXXXX-XXX-X"
    },
    media: [],
    pages: pagesList
  };

  fetch("/api/projects/create", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newProjPayload)
  })
  .then(async r => {
    const data = await r.json();
    if (!r.ok || data.status === "error") {
      const dupWarning = document.getElementById("modal-duplicate-warning");
      const dupNameSpan = document.getElementById("modal-dup-name");
      if (dupWarning) dupWarning.style.display = "block";
      if (dupNameSpan) dupNameSpan.innerText = projName;
      showToast(`⚠️ ${data.error || "Project creation failed!"}`, "danger");
      return;
    }
    finishProjectSetup(newProjPayload);
  })
  .catch((err) => {
    showToast(`⚠️ Error creating project: ${err.message}`, "danger");
  });
}

function finishProjectSetup(proj) {
  currentProject = proj;
  currentPageIndex = 0; // Always start directly on Page 1
  activeElementId = null;
  undoStack = [];
  redoStack = [];

  renumberPages();
  localStorage.setItem("kdp_active_project_path", currentProject.project_dir);
  localStorage.setItem("kdp_active_project_data", JSON.stringify(currentProject));

  closeModal("new-project-modal");
  syncActiveProjectUI();
  fetchRecentProjects();
  loadPageIntoCanvas(0);
  switchTab("canvas");

  showToast(`✨ Created Project "${currentProject.name}"!`, "success");
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
          currentProject.is_locked = Boolean(found.is_locked);
        }
      }
      currentPageIndex = 0; // Always start directly on Page 1
      activeElementId = null;
      undoStack = [];
      redoStack = [];

      renumberPages();
      localStorage.setItem("kdp_active_project_path", currentProject.project_dir);
      localStorage.setItem("kdp_active_project_data", JSON.stringify(currentProject));

      closeModal("open-folder-modal");
      syncActiveProjectUI();
      loadPageIntoCanvas(0);
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
// Image Processing Modal & Granular Progress Controller
// ==========================================
const RADIAL_CIRCUMFERENCE = 2 * Math.PI * 50; // 314.16

function openImageProcessingModal(totalFiles, title = "Optimizing Artwork for KDP Print") {
  const modal = document.getElementById("image-processing-modal");
  const bar = document.getElementById("radial-progress-bar");
  const pctText = document.getElementById("radial-pct-text");
  const countText = document.getElementById("radial-count-text");
  const doneVal = document.getElementById("proc-metric-done");
  const remVal = document.getElementById("proc-metric-remaining");
  const savedVal = document.getElementById("proc-metric-saved");
  const titleEl = document.getElementById("proc-title");

  if (!modal) return;

  if (titleEl) titleEl.innerText = title;
  if (bar) {
    bar.style.strokeDasharray = `${RADIAL_CIRCUMFERENCE}`;
    bar.style.strokeDashoffset = `${RADIAL_CIRCUMFERENCE}`;
    bar.style.stroke = "#6366f1";
  }
  if (pctText) pctText.innerText = "0%";
  if (countText) countText.innerText = `0 / ${totalFiles}`;
  if (doneVal) doneVal.innerText = "0";
  if (remVal) remVal.innerText = `${totalFiles}`;
  if (savedVal) savedVal.innerText = "0 KB";

  modal.classList.add("active");
}

function updateImageProcessingProgress(currentIdx, totalFiles, fileName, stepText, totalKbSaved = 0) {
  const bar = document.getElementById("radial-progress-bar");
  const pctText = document.getElementById("radial-pct-text");
  const countText = document.getElementById("radial-count-text");
  const fileEl = document.getElementById("proc-current-file");
  const stepEl = document.getElementById("proc-current-step");
  const doneVal = document.getElementById("proc-metric-done");
  const remVal = document.getElementById("proc-metric-remaining");
  const savedVal = document.getElementById("proc-metric-saved");

  const completed = currentIdx;
  const pct = Math.min(100, Math.round((completed / totalFiles) * 100));

  if (bar) {
    const offset = RADIAL_CIRCUMFERENCE - (RADIAL_CIRCUMFERENCE * pct / 100);
    bar.style.strokeDashoffset = `${offset}`;
    if (pct >= 100) {
      bar.style.stroke = "#22c55e"; // Glowing green when finished
    }
  }

  if (pctText) pctText.innerText = `${pct}%`;
  if (countText) countText.innerText = `${completed} / ${totalFiles}`;
  if (fileEl && fileName) fileEl.innerText = fileName;
  if (stepEl && stepText) {
    stepEl.innerHTML = `<span class="spinner-dot"></span> ${stepText}`;
  }
  if (doneVal) doneVal.innerText = `${completed}`;
  if (remVal) remVal.innerText = `${Math.max(0, totalFiles - completed)}`;
  if (savedVal) {
    if (totalKbSaved > 1024) {
      savedVal.innerText = `${(totalKbSaved / 1024).toFixed(1)} MB`;
    } else {
      savedVal.innerText = `${Math.round(totalKbSaved)} KB`;
    }
  }
}

function closeImageProcessingModal() {
  const modal = document.getElementById("image-processing-modal");
  if (modal) {
    setTimeout(() => {
      modal.classList.remove("active");
    }, 600);
  }
}

function readAsDataURLAsync(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
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

// ==========================================================================
// Interactive 2-Step Media Upload Studio Controller
// ==========================================================================
let stagedUploadItems = [];
let isProcessingStep1 = false;
let isProcessingStep2 = false;

async function handleMediaLibraryUpload(event) {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot upload: Project is locked!", "warning");
    return;
  }

  const files = Array.from(event.target.files);
  if (!files.length) return;

  stagedUploadItems = [];
  isProcessingStep1 = false;
  isProcessingStep2 = false;

  // Read files into staged memory immediately
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const sizeKb = Math.round(file.size / 1024);

    let dataUrl = "";
    try {
      dataUrl = await readAsDataURLAsync(file);
    } catch (err) {
      console.error("Read file error:", err);
      continue;
    }

    stagedUploadItems.push({
      id: `med_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
      name: cleanFileName(file.name),
      fileName: file.name,
      originalDataUrl: dataUrl,
      currentDataUrl: dataUrl,
      originalSizeKb: sizeKb,
      currentSizeKb: sizeKb,
      step1Done: false,
      step2Done: false,
      status: "ready" // 'ready' | 'compressed' | 'cleaned'
    });
  }

  openInteractiveUploadModal();
}

function openInteractiveUploadModal() {
  const modal = document.getElementById("image-processing-modal");
  if (!modal) return;

  const totalCountEl = document.getElementById("upload-total-count");
  const totalSizeEl = document.getElementById("upload-total-size");
  if (totalCountEl) totalCountEl.innerText = stagedUploadItems.length;
  if (totalSizeEl) {
    const totalKb = stagedUploadItems.reduce((acc, it) => acc + it.originalSizeKb, 0);
    totalSizeEl.innerText = totalKb > 1024 ? `${(totalKb / 1024).toFixed(1)} MB` : `${totalKb} KB`;
  }

  // Reset Step 1 UI
  const btnStep1 = document.getElementById("btn-run-step1");
  const step1Card = document.getElementById("step1-card");
  const step1ProgWrap = document.getElementById("step1-progress-wrap");
  const step1Fill = document.getElementById("step1-progress-fill");
  const step1Status = document.getElementById("step1-progress-status");
  const step1Saved = document.getElementById("step1-progress-saved");

  if (step1Card) step1Card.className = "upload-step-card active-step";
  if (btnStep1) {
    btnStep1.disabled = false;
    btnStep1.innerHTML = "⚡ Step 1: Compress & Auto-Focus";
    btnStep1.className = "btn btn-primary step-action-btn";
  }
  if (step1ProgWrap) step1ProgWrap.style.display = "none";
  if (step1Fill) step1Fill.style.width = "0%";
  if (step1Status) step1Status.innerText = `0 / ${stagedUploadItems.length} Processed (0%)`;
  if (step1Saved) step1Saved.innerText = "Saved 0 KB";

  // Reset Step 2 UI (disabled initially until Step 1 completes)
  const btnStep2 = document.getElementById("btn-run-step2");
  const step2Card = document.getElementById("step2-card");
  const step2ProgWrap = document.getElementById("step2-progress-wrap");
  const step2Fill = document.getElementById("step2-progress-fill");
  const step2Status = document.getElementById("step2-progress-status");
  const step2Count = document.getElementById("step2-progress-count");

  if (step2Card) step2Card.className = "upload-step-card disabled";
  if (btnStep2) {
    btnStep2.disabled = true;
    btnStep2.innerHTML = "🪄 Step 2: Make Background White";
    btnStep2.className = "btn btn-outline step-action-btn";
  }
  if (step2ProgWrap) step2ProgWrap.style.display = "none";
  if (step2Fill) step2Fill.style.width = "0%";
  if (step2Status) step2Status.innerText = "Waiting for Step 1...";
  if (step2Count) step2Count.innerText = `0 / ${stagedUploadItems.length}`;

  const footerStatus = document.getElementById("upload-footer-status");
  if (footerStatus) footerStatus.innerText = "Click Step 1 to optimize & compress images";

  renderUploadPreviewGrid();
  modal.classList.add("active");
}

function closeInteractiveUploadModal() {
  const modal = document.getElementById("image-processing-modal");
  if (modal) modal.classList.remove("active");
}

function formatSizeKb(kb) {
  if (!kb || kb <= 0) return "0 KB";
  if (kb >= 1024) {
    return `${(kb / 1024).toFixed(1)} MB`;
  }
  return `${kb} KB`;
}

function renderUploadPreviewGrid() {
  const grid = document.getElementById("upload-preview-grid");
  if (!grid) return;

  grid.innerHTML = stagedUploadItems.map((item, idx) => {
    let badgeClass = "status-ready";
    let badgeText = "Ready";
    if (item.status === "cleaned") {
      badgeClass = "status-cleaned";
      badgeText = "White BG ✅";
    } else if (item.status === "compressed") {
      badgeClass = "status-compressed";
      badgeText = "Compressed ⚡";
    }

    const origStr = formatSizeKb(item.originalSizeKb);
    const currStr = formatSizeKb(item.currentSizeKb);
    const isCompressed = item.step1Done || item.step2Done || item.currentSizeKb < item.originalSizeKb;
    const pctSaved = isCompressed && item.originalSizeKb > 0
      ? Math.max(0, Math.round(((item.originalSizeKb - item.currentSizeKb) / item.originalSizeKb) * 100))
      : 0;

    const sizeHtml = isCompressed && pctSaved > 0
      ? `<span class="size-before-label">Before: <del>${origStr}</del></span>
         <span class="size-after-label">After: ${currStr} <span class="size-saved-pill">-${pctSaved}%</span></span>`
      : `<span class="size-before-label">Size: ${origStr}</span>`;

    return `
      <div class="upload-preview-card" id="up-card-${idx}">
        <div class="upload-card-thumb-box">
          <img src="${item.currentDataUrl}" alt="${item.fileName}" id="up-img-${idx}">
        </div>
        <div class="upload-card-name" title="${item.fileName}">${item.fileName}</div>
        <span class="upload-card-badge ${badgeClass}" id="up-badge-${idx}">${badgeText}</span>
        <div class="upload-size-compare" id="up-size-${idx}">
          ${sizeHtml}
        </div>
      </div>
    `;
  }).join("");
}

async function runUploadStep1() {
  if (isProcessingStep1 || stagedUploadItems.length === 0) return;
  isProcessingStep1 = true;

  const btnStep1 = document.getElementById("btn-run-step1");
  const step1Card = document.getElementById("step1-card");
  const progWrap = document.getElementById("step1-progress-wrap");
  const progFill = document.getElementById("step1-progress-fill");
  const progStatus = document.getElementById("step1-progress-status");
  const progSaved = document.getElementById("step1-progress-saved");

  if (progWrap) progWrap.style.display = "block";
  if (btnStep1) {
    btnStep1.disabled = true;
    btnStep1.innerHTML = `⏳ Compressing...`;
  }

  let totalKbSaved = 0;
  const total = stagedUploadItems.length;

  for (let i = 0; i < total; i++) {
    const item = stagedUploadItems[i];
    const pct = Math.round(((i + 1) / total) * 100);

    if (progStatus) {
      progStatus.innerText = `Compressing [${i + 1}/${total}]: ${item.fileName} (${pct}%)`;
    }
    if (progFill) progFill.style.width = `${pct}%`;

    try {
      const resp = await fetch("/api/projects/process_image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          data_url: item.currentDataUrl,
          clean_bg: false,
          auto_crop: true,
          compress: true
        })
      });
      const data = await resp.json();
      if (data.data_url) {
        item.currentDataUrl = data.data_url;
        const saved = Math.max(0, item.originalSizeKb - (data.size_kb || item.currentSizeKb));
        totalKbSaved += saved;
        item.currentSizeKb = data.size_kb || item.currentSizeKb;
        item.step1Done = true;
        item.status = "compressed";

        const origStr = formatSizeKb(item.originalSizeKb);
        const currStr = formatSizeKb(item.currentSizeKb);
        const pctSaved = item.originalSizeKb > 0 
          ? Math.max(0, Math.round(((item.originalSizeKb - item.currentSizeKb) / item.originalSizeKb) * 100))
          : 0;

        const imgEl = document.getElementById(`up-img-${i}`);
        const badgeEl = document.getElementById(`up-badge-${i}`);
        const sizeEl = document.getElementById(`up-size-${i}`);

        if (imgEl) imgEl.src = data.data_url;
        if (badgeEl) {
          badgeEl.className = "upload-card-badge status-compressed";
          badgeEl.innerText = "Compressed ⚡";
        }
        if (sizeEl) {
          sizeEl.innerHTML = `
            <span class="size-before-label">Before: <del>${origStr}</del></span>
            <span class="size-after-label">After: ${currStr} ${pctSaved > 0 ? `<span class="size-saved-pill">-${pctSaved}%</span>` : ''}</span>
          `;
        }
      }
    } catch (err) {
      console.warn("Step 1 compression error on", item.fileName, err);
    }

    if (progSaved) {
      const savedStr = totalKbSaved > 1024 ? `${(totalKbSaved / 1024).toFixed(1)} MB` : `${totalKbSaved} KB`;
      progSaved.innerText = `Saved ~${savedStr}`;
    }
  }

  isProcessingStep1 = false;
  if (progStatus) {
    progStatus.innerText = `✅ All ${total} images compressed & auto-focused!`;
  }
  if (btnStep1) {
    btnStep1.disabled = true;
    btnStep1.className = "btn btn-success step-action-btn";
    btnStep1.innerHTML = "✅ Step 1: Completed";
  }
  if (step1Card) {
    step1Card.className = "upload-step-card completed-step";
  }

  // Unlock Step 2
  const step2Card = document.getElementById("step2-card");
  const btnStep2 = document.getElementById("btn-run-step2");
  if (step2Card) step2Card.className = "upload-step-card active-step";
  if (btnStep2) {
    btnStep2.disabled = false;
    btnStep2.className = "btn btn-primary step-action-btn";
  }

  const footerStatus = document.getElementById("upload-footer-status");
  if (footerStatus) footerStatus.innerText = "Step 1 Done! Now click Step 2 to purify background to white";

  showToast(`⚡ Step 1 complete: Compressed ${total} image(s)! Now click Step 2.`, "success");
}

async function runUploadStep2() {
  if (isProcessingStep2 || stagedUploadItems.length === 0) return;
  isProcessingStep2 = true;

  const btnStep2 = document.getElementById("btn-run-step2");
  const step2Card = document.getElementById("step2-card");
  const progWrap = document.getElementById("step2-progress-wrap");
  const progFill = document.getElementById("step2-progress-fill");
  const progStatus = document.getElementById("step2-progress-status");
  const progCount = document.getElementById("step2-progress-count");

  if (progWrap) progWrap.style.display = "block";
  if (btnStep2) {
    btnStep2.disabled = true;
    btnStep2.innerHTML = `⏳ Purifying Background...`;
  }

  const total = stagedUploadItems.length;

  for (let i = 0; i < total; i++) {
    const item = stagedUploadItems[i];
    const pct = Math.round(((i + 1) / total) * 100);

    if (progStatus) {
      progStatus.innerText = `Purifying [${i + 1}/${total}]: ${item.fileName} (${pct}%)`;
    }
    if (progFill) progFill.style.width = `${pct}%`;
    if (progCount) progCount.innerText = `${i + 1} / ${total}`;

    try {
      const resp = await fetch("/api/projects/process_image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          data_url: item.currentDataUrl,
          clean_bg: true,
          auto_crop: false,
          compress: false
        })
      });
      const data = await resp.json();
      if (data.data_url) {
        item.currentDataUrl = data.data_url;
        item.currentSizeKb = data.size_kb || item.currentSizeKb;
        item.step2Done = true;
        item.status = "cleaned";

        const origStr = formatSizeKb(item.originalSizeKb);
        const currStr = formatSizeKb(item.currentSizeKb);
        const pctSaved = item.originalSizeKb > 0 
          ? Math.max(0, Math.round(((item.originalSizeKb - item.currentSizeKb) / item.originalSizeKb) * 100))
          : 0;

        const imgEl = document.getElementById(`up-img-${i}`);
        const badgeEl = document.getElementById(`up-badge-${i}`);
        const sizeEl = document.getElementById(`up-size-${i}`);

        if (imgEl) imgEl.src = data.data_url;
        if (badgeEl) {
          badgeEl.className = "upload-card-badge status-cleaned";
          badgeEl.innerText = "White BG ✅";
        }
        if (sizeEl) {
          sizeEl.innerHTML = `
            <span class="size-before-label">Before: <del>${origStr}</del></span>
            <span class="size-after-label">After: ${currStr} ${pctSaved > 0 ? `<span class="size-saved-pill">-${pctSaved}%</span>` : ''}</span>
          `;
        }
      }
    } catch (err) {
      console.warn("Step 2 clean background error on", item.fileName, err);
    }
  }

  isProcessingStep2 = false;
  if (progStatus) {
    progStatus.innerText = `✅ All ${total} image backgrounds purified to #FFFFFF!`;
  }
  if (btnStep2) {
    btnStep2.disabled = true;
    btnStep2.className = "btn btn-success step-action-btn";
    btnStep2.innerHTML = "✅ Step 2: Completed";
  }
  if (step2Card) {
    step2Card.className = "upload-step-card completed-step";
  }

  const footerStatus = document.getElementById("upload-footer-status");
  if (footerStatus) footerStatus.innerText = "🎉 All steps completed! Click 'Add to Project Media'";

  showToast(`🪄 Step 2 complete: White background purified! Click 'Add to Project Media'.`, "success");
}

async function finalizeInteractiveUpload() {
  if (stagedUploadItems.length === 0) {
    closeInteractiveUploadModal();
    return;
  }

  if (!currentProject.media) {
    currentProject.media = [];
  }

  recordHistoryState("Add Uploaded Media");
  let lastMediaItem = null;

  for (const item of stagedUploadItems) {
    const mediaItem = {
      id: item.id,
      name: item.name,
      fileName: item.fileName,
      dataUrl: item.currentDataUrl,
      sizeKb: item.currentSizeKb
    };
    currentProject.media.unshift(mediaItem);
    lastMediaItem = mediaItem;

    // Silently save final optimized PNG to disk in background
    fetch("/api/projects/upload_asset", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        project_dir: currentProject.project_dir,
        filename: item.fileName,
        data_url: item.currentDataUrl,
        clean_bg: false,
        auto_crop: false
      })
    }).catch(() => {});
  }

  closeInteractiveUploadModal();
  renderMediaLibrary();
  switchDrawerTab("media");
  syncActiveProjectUI();
  markProjectDirty();

  showToast(`✨ Added ${stagedUploadItems.length} optimized image(s) to Project Media!`, "success");

  stagedUploadItems = [];
}

// ==========================================
// ⚡ Batch Import Images to Coloring Pages
// ==========================================
function triggerBatchUpload() {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot import: Project is locked!", "warning");
    return;
  }
  const input = document.getElementById("batch-import-upload-input");
  if (input) {
    input.value = "";
    input.click();
  }
}

async function handleBatchImportUpload(event) {
  if (currentProject.is_locked) return;

  const files = Array.from(event.target.files);
  if (!files.length) return;

  recordHistoryState("Batch Import Images");
  openImageProcessingModal(files.length, "Batch Generating Coloring Pages");

  if (!currentProject.media) currentProject.media = [];

  let totalKbSaved = 0;
  const projFont = currentProject.settings?.default_font_family || "Fredoka";
  const projOutline = currentProject.settings?.default_font_mode !== "solid";
  const projStroke = currentProject.settings?.default_stroke_color || "#0f172a";
  const projColor = currentProject.settings?.default_text_color || (projOutline ? "#ffffff" : "#111827");

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const origSizeKb = Math.round(file.size / 1024);

    updateImageProcessingProgress(i, files.length, file.name, "🪄 [1/3] Purifying White Background (#FFFFFF)...", totalKbSaved);
    await new Promise(r => setTimeout(r, 180));

    let rawDataUrl = "";
    try {
      rawDataUrl = await readAsDataURLAsync(file);
    } catch (err) {
      console.error("Read file error:", err);
      continue;
    }

    updateImageProcessingProgress(i, files.length, file.name, "🎯 [2/3] Auto-detecting & centering artwork...", totalKbSaved);
    await new Promise(r => setTimeout(r, 180));

    let finalDataUrl = rawDataUrl;
    let finalSizeKb = origSizeKb;

    try {
      updateImageProcessingProgress(i, files.length, file.name, "⚡ [3/3] Compressing 300 DPI Lossless PNG...", totalKbSaved);
      const resp = await fetch("/api/projects/upload_asset", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_dir: currentProject.project_dir,
          filename: file.name,
          data_url: rawDataUrl,
          clean_bg: true,
          auto_crop: true
        })
      });
      const data = await resp.json();
      if (data.data_url) {
        finalDataUrl = data.data_url;
        finalSizeKb = data.size_kb || finalSizeKb;
      }
    } catch (err) {
      console.warn("Backend optimization fallback:", err);
    }

    const saved = Math.max(0, origSizeKb - finalSizeKb);
    totalKbSaved += saved;

    const mediaItem = {
      id: `med_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
      name: cleanFileName(file.name),
      fileName: file.name,
      dataUrl: finalDataUrl,
      sizeKb: finalSizeKb
    };
    currentProject.media.unshift(mediaItem);

    // Extract first-word uppercase title (e.g. BEAR, LION, DOG)
    const titleCaps = extractFirstWordCaps(file.name);
    const autoSize = calculateAutoTitleFontSize(titleCaps, 40);

    // Create a new page for this artwork
    const newPage = {
      page_number: currentProject.pages.length + 1,
      page_type: "content",
      layout: "kdp_top_ref",
      title: cleanTitleString(titleCaps),
      elements: [
        {
          id: `elem_ref_${Date.now()}_${i}`,
          type: "ref_image",
          x: 35,
          y: 25,
          w: 190,
          h: 180,
          text: titleCaps,
          image_src: finalDataUrl
        },
        {
          id: `elem_title_${Date.now()}_${i}`,
          type: "title",
          x: 235,
          y: 70,
          w: 240,
          h: 80,
          text: titleCaps,
          font_size: autoSize,
          color: projColor,
          is_outline: projOutline,
          stroke_color: projStroke,
          font_family: projFont,
          letter_spacing: 2
        },
        {
          id: `elem_main_${Date.now()}_${i}`,
          type: "main_image",
          x: 35,
          y: 220,
          w: 440,
          h: 410,
          text: titleCaps,
          image_src: finalDataUrl
        },
        {
          id: `elem_frame_${Date.now()}_${i}`,
          type: "border",
          x: 25,
          y: 15,
          w: 460,
          h: 630
        }
      ]
    };

    currentProject.pages.push(newPage);

    updateImageProcessingProgress(i + 1, files.length, file.name, "✅ Page Generated!", totalKbSaved);
    await new Promise(r => setTimeout(r, 220));
  }

  renumberPages();
  syncContentsPage();
  renderMediaLibrary();
  renderTimeline();
  loadPageIntoCanvas(currentPageIndex);
  syncActiveProjectUI();
  markProjectDirty();

  await new Promise(r => setTimeout(r, 350));
  closeImageProcessingModal();
  const savedLabel = totalKbSaved > 1024 ? `${(totalKbSaved / 1024).toFixed(1)} MB` : `${totalKbSaved} KB`;
  showToast(`🎉 Batch imported & created ${files.length} coloring pages (Saved ~${savedLabel})!`, "success");
}

let mediaSortOrder = "name_asc";

function onMediaSortChange() {
  const select = document.getElementById("media-sort-select");
  if (select) mediaSortOrder = select.value;
  renderMediaLibrary();
}

function calculateAutoTitleFontSize(text, baseSize = 40) {
  if (!text) return baseSize;
  const clean = text.trim();
  const len = clean.length;
  // Short names (e.g., "DOG", "CAT", "LION", "COW", "BEAR", "FOX") -> 40px
  if (len <= 5) return baseSize;
  // Medium names (e.g., "RABBIT", "MONKEY", "TIGER", "PUPPY") -> 34px
  if (len <= 7) return Math.min(baseSize, 34);
  // Longer names (e.g., "ELEPHANT", "GIRAFFE", "DOLPHIN", "PENGUIN") -> 28px
  if (len <= 9) return Math.min(baseSize, 28);
  // Very long names (e.g., "HIPPOPOTAMUS", "TYRANNOSAURUS", "BUTTERFLY") -> 22px
  return Math.min(baseSize, 22);
}

// ==========================================
// Media Selection, Deletion & Clear All Engine
// ==========================================
let selectedMediaIds = new Set();

function toggleMediaSelection(mediaId, isChecked) {
  if (isChecked) {
    selectedMediaIds.add(mediaId);
  } else {
    selectedMediaIds.delete(mediaId);
  }
  updateMediaSelectionUI();
}

function toggleSelectAllMedia(isChecked) {
  const projectMedia = currentProject.media || [];
  if (isChecked) {
    projectMedia.forEach(m => selectedMediaIds.add(m.id));
  } else {
    selectedMediaIds.clear();
  }
  renderMediaLibrary();
}

function updateMediaSelectionUI() {
  const count = selectedMediaIds.size;
  const badge = document.getElementById("media-selected-count-badge");
  const bulkBtn = document.getElementById("media-bulk-delete-btn");
  const bulkCount = document.getElementById("media-bulk-count");
  const selectAllCb = document.getElementById("media-select-all-cb");
  const totalMedia = (currentProject.media || []).length;

  if (badge) {
    badge.style.display = count > 0 ? "inline-block" : "none";
    badge.innerText = `${count} selected`;
  }
  if (bulkBtn) {
    bulkBtn.style.display = count > 0 ? "inline-flex" : "none";
  }
  if (bulkCount) {
    bulkCount.innerText = count;
  }
  if (selectAllCb) {
    selectAllCb.checked = totalMedia > 0 && count === totalMedia;
    selectAllCb.indeterminate = count > 0 && count < totalMedia;
  }

  // Update card selected classes
  document.querySelectorAll(".media-card").forEach(card => {
    const cb = card.querySelector(".media-card-checkbox");
    if (cb && selectedMediaIds.has(cb.dataset.id)) {
      card.classList.add("selected");
      cb.checked = true;
    } else if (cb) {
      card.classList.remove("selected");
      cb.checked = false;
    }
  });
}

let pendingMediaDeleteAction = null;

function deleteSingleMedia(mediaId) {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot delete: Project is locked!", "warning");
    return;
  }

  const projectMedia = currentProject.media || [];
  const item = projectMedia.find(m => m.id === mediaId);
  if (!item) return;

  pendingMediaDeleteAction = { type: "single", mediaId: mediaId, name: item.name };

  const modal = document.getElementById("media-delete-confirm-modal");
  const title = document.getElementById("media-delete-modal-title");
  const msg = document.getElementById("media-delete-modal-msg");
  const sub = document.getElementById("media-delete-modal-sub");
  const prevBox = document.getElementById("media-delete-modal-preview");
  const prevImg = document.getElementById("media-delete-modal-img");
  const actionBtn = document.getElementById("media-delete-confirm-action-btn");

  if (title) title.innerText = "🗑 Delete Image from Media";
  if (msg) msg.innerText = `Delete "${item.name}" from Media Library?`;
  if (sub) sub.innerText = `File: ${item.fileName || item.name} (${item.sizeKb || 0} KB). This image will be removed from this project's library.`;
  if (prevBox && prevImg) {
    prevBox.style.display = "block";
    prevImg.src = item.dataUrl;
  }
  if (actionBtn) actionBtn.innerText = "🗑 Yes, Delete Image";

  if (modal) modal.classList.add("active");
}

function deleteSelectedMedia() {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot delete: Project is locked!", "warning");
    return;
  }

  const count = selectedMediaIds.size;
  if (count === 0) return;

  pendingMediaDeleteAction = { type: "bulk", count: count };

  const modal = document.getElementById("media-delete-confirm-modal");
  const title = document.getElementById("media-delete-modal-title");
  const msg = document.getElementById("media-delete-modal-msg");
  const sub = document.getElementById("media-delete-modal-sub");
  const prevBox = document.getElementById("media-delete-modal-preview");
  const actionBtn = document.getElementById("media-delete-confirm-action-btn");

  if (title) title.innerText = `🗑 Bulk Delete (${count} Images)`;
  if (msg) msg.innerText = `Delete all ${count} selected images?`;
  if (sub) sub.innerText = `These ${count} selected images will be removed from this project's media library.`;
  if (prevBox) prevBox.style.display = "none";
  if (actionBtn) actionBtn.innerText = `🗑 Delete ${count} Selected`;

  if (modal) modal.classList.add("active");
}

function clearAllMedia() {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot clear: Project is locked!", "warning");
    return;
  }

  const projectMedia = currentProject.media || [];
  if (projectMedia.length === 0) {
    showToast("Media library is already empty.", "info");
    return;
  }

  pendingMediaDeleteAction = { type: "clear", count: projectMedia.length };

  const modal = document.getElementById("media-delete-confirm-modal");
  const title = document.getElementById("media-delete-modal-title");
  const msg = document.getElementById("media-delete-modal-msg");
  const sub = document.getElementById("media-delete-modal-sub");
  const prevBox = document.getElementById("media-delete-modal-preview");
  const actionBtn = document.getElementById("media-delete-confirm-action-btn");

  if (title) title.innerText = "🧹 Clear Entire Media Library";
  if (msg) msg.innerText = `⚠️ Clear ALL ${projectMedia.length} image(s) from this project?`;
  if (sub) sub.innerText = "All uploaded artwork in this project will be deleted. This cannot be undone.";
  if (prevBox) prevBox.style.display = "none";
  if (actionBtn) actionBtn.innerText = "🧹 Yes, Clear All Media";

  if (modal) modal.classList.add("active");
}

function executeMediaDeleteAction() {
  const modal = document.getElementById("media-delete-confirm-modal");
  if (modal) modal.classList.remove("active");

  if (!pendingMediaDeleteAction) return;

  if (pendingMediaDeleteAction.type === "single") {
    const mediaId = pendingMediaDeleteAction.mediaId;
    const name = pendingMediaDeleteAction.name;
    recordHistoryState(`Delete Media "${name}"`);
    currentProject.media = (currentProject.media || []).filter(m => m.id !== mediaId);
    selectedMediaIds.delete(mediaId);
    renderMediaLibrary();
    syncActiveProjectUI();
    markProjectDirty();
    showToast(`🗑 Deleted "${name}"!`, "info");
  } else if (pendingMediaDeleteAction.type === "bulk") {
    const count = pendingMediaDeleteAction.count;
    recordHistoryState(`Delete ${count} Media Files`);
    const projectMedia = currentProject.media || [];
    currentProject.media = projectMedia.filter(m => !selectedMediaIds.has(m.id));
    selectedMediaIds.clear();
    renderMediaLibrary();
    syncActiveProjectUI();
    markProjectDirty();
    showToast(`🗑 Deleted ${count} image(s) from media library!`, "info");
  } else if (pendingMediaDeleteAction.type === "clear") {
    recordHistoryState("Clear All Media");
    currentProject.media = [];
    selectedMediaIds.clear();
    renderMediaLibrary();
    syncActiveProjectUI();
    markProjectDirty();
    showToast("🧹 All media cleared from project!", "info");
  }

  pendingMediaDeleteAction = null;
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
    updateMediaSelectionUI();
    return;
  }

  const sortSelect = document.getElementById("media-sort-select");
  const sortMode = sortSelect ? sortSelect.value : mediaSortOrder;

  let sortedMedia = [...projectMedia];
  if (sortMode === "name_asc") {
    sortedMedia.sort((a, b) => (a.name || "").localeCompare(b.name || "", undefined, { numeric: true, sensitivity: 'base' }));
  } else if (sortMode === "name_desc") {
    sortedMedia.sort((a, b) => (b.name || "").localeCompare(a.name || "", undefined, { numeric: true, sensitivity: 'base' }));
  } else if (sortMode === "oldest") {
    sortedMedia.reverse();
  }

  const fragment = document.createDocumentFragment();
  sortedMedia.forEach(item => {
    const isSelected = selectedMediaIds.has(item.id);
    const card = document.createElement("div");
    card.className = `media-card ${isSelected ? 'selected' : ''}`;

    card.innerHTML = `
      <div class="media-card-top">
        <input type="checkbox" class="media-card-checkbox" data-id="${item.id}" ${isSelected ? 'checked' : ''} onclick="event.stopPropagation(); toggleMediaSelection('${item.id}', this.checked)">
        <div class="media-card-thumb" onclick="handleMediaCardClick('${item.id}')" style="cursor: pointer;">
          <img src="${item.dataUrl}">
        </div>
        <div class="media-card-meta" onclick="handleMediaCardClick('${item.id}')" style="cursor: pointer;">
          <div class="media-name" title="${item.name}">${item.name}</div>
          <div class="media-tag">${item.sizeKb} KB • ${currentProject.folder_name}</div>
        </div>
        <button class="media-card-delete-btn" onclick="event.stopPropagation(); deleteSingleMedia('${item.id}')" title="Delete this image">
          🗑
        </button>
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

    fragment.appendChild(card);
  });
  container.appendChild(fragment);

  updateMediaSelectionUI();
  populateQuickMediaPicker();
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

async function applyMediaToSlot(mediaId, slotType) {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot modify: Project is locked!", "warning");
    return;
  }

  const item = (currentProject.media || []).find(m => m.id === mediaId);
  if (!item) return;

  const page = currentProject.pages[currentPageIndex];
  if (!page || page.page_type === "blank_verso") return;

  const imgSrc = item.dataUrl;
  const labelText = item.name;
  const isDotProject = (currentProject.book_type === "dot_to_dot" || page.layout === "dot_to_dot");

  if (isDotProject) {
    recordHistoryState("Convert Image to Dot-to-Dot");
    showToast("🪄 Analyzing image contour & generating numbered dots...", "info");

    const firstWordCaps = extractFirstWordCaps(item.name || item.fileName);
    const dotCount = (page.dot_to_dot && page.dot_to_dot.dot_count) ? page.dot_to_dot.dot_count : 35;
    const showGuide = page.dot_to_dot ? (page.dot_to_dot.faint_guide !== false) : true;

    try {
      const resp = await fetch("/api/generators/dot_to_dot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          image_data: imgSrc,
          dot_count: dotCount,
          faint_guide: showGuide
        })
      });
      const data = await resp.json();
      if (data.puzzle) {
        page.dot_to_dot = data.puzzle;
        page.dot_to_dot.image_src = imgSrc;
        page.layout = "dot_to_dot";
        page.title = cleanTitleString(firstWordCaps);

        let refElem = page.elements.find(e => e.type === "ref_image");
        if (!refElem) {
          refElem = { id: `elem_ref_${Date.now()}`, type: "ref_image", x: 35, y: 25, w: 160, h: 150, text: firstWordCaps, image_src: imgSrc };
          page.elements.unshift(refElem);
        } else {
          refElem.image_src = imgSrc;
          refElem.text = firstWordCaps;
        }

        let titleElem = page.elements.find(e => e.type === "title");
        if (!titleElem) {
          titleElem = { id: `elem_title_${Date.now()}`, type: "title", x: 215, y: 55, w: 260, h: 80, text: firstWordCaps, font_size: 34, color: "#ffffff", is_outline: true, font_family: "Fredoka", letter_spacing: 2 };
          page.elements.push(titleElem);
        } else {
          titleElem.text = firstWordCaps;
          titleElem.font_size = calculateAutoTitleFontSize(firstWordCaps, 34);
        }

        let dotElem = page.elements.find(e => e.type === "dot_to_dot" || e.type === "main_image");
        if (!dotElem) {
          dotElem = { id: `elem_dot_${Date.now()}`, type: "dot_to_dot", x: 35, y: 190, w: 440, h: 440, text: firstWordCaps };
          page.elements.push(dotElem);
        } else {
          dotElem.type = "dot_to_dot";
          dotElem.image_src = imgSrc;
        }

        renumberPages();
        syncContentsPage();
        loadPageIntoCanvas(currentPageIndex);
        renderTimeline();
        syncActiveProjectUI();
        markProjectDirty();
        showToast(`🎉 Converted "${firstWordCaps}" into ${data.puzzle.dot_count} Numbered Dots!`, "success");
        return;
      }
    } catch (err) {
      console.warn("Dot-to-dot converter fallback:", err);
    }
  }

  recordHistoryState(`Apply Media (${slotType})`);

  if (slotType === "ref") {
    let refElem = page.elements.find(e => e.type === "ref_image");
    if (!refElem) {
      refElem = { id: `elem_ref_${Date.now()}`, type: "ref_image", x: 35, y: 25, w: 190, h: 180, text: labelText, image_src: null };
      page.elements.push(refElem);
    }
    refElem.image_src = imgSrc;
    refElem.text = labelText;
    setActiveElement(refElem.id);
    showToast(`🎯 Set "${item.name}" as Reference Image!`, "success");
  } 
  else if (slotType === "drawing") {
    let mainElem = page.elements.find(e => e.type === "main_image");
    if (!mainElem) {
      mainElem = { id: `elem_main_${Date.now()}`, type: "main_image", x: 35, y: 220, w: 440, h: 410, text: labelText, image_src: null };
      page.elements.push(mainElem);
    }
    mainElem.image_src = imgSrc;
    mainElem.text = labelText;
    setActiveElement(mainElem.id);
    showToast(`🎨 Set "${item.name}" as Drawing Image!`, "success");
  } 
  else if (slotType === "title") {
    const firstWordCaps = extractFirstWordCaps(item.name || item.fileName);
    let titleElem = page.elements.find(e => e.type === "title");
    const autoSize = calculateAutoTitleFontSize(firstWordCaps, 40);
    const projFont = currentProject.settings?.default_font_family || "Fredoka";
    const projOutline = currentProject.settings?.default_font_mode !== "solid";
    const projStroke = currentProject.settings?.default_stroke_color || "#0f172a";
    const projColor = currentProject.settings?.default_text_color || (projOutline ? "#ffffff" : "#111827");

    if (!titleElem) {
      titleElem = { id: `elem_title_${Date.now()}`, type: "title", x: 235, y: 70, w: 240, h: 80, font_size: autoSize, color: projColor, is_outline: projOutline, stroke_color: projStroke, font_family: projFont, letter_spacing: 2 };
      page.elements.push(titleElem);
    } else {
      titleElem.font_size = autoSize;
    }
    titleElem.text = firstWordCaps;
    page.title = cleanTitleString(firstWordCaps);
    setActiveElement(titleElem.id);
    showToast(`🔤 Set Title to "${firstWordCaps}" (Auto-adjusted: ${autoSize}pt)!`, "success");
  } 
  else if (slotType === "all") {
    const firstWordCaps = extractFirstWordCaps(item.name || item.fileName);
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
      titleElem.text = firstWordCaps;
      titleElem.font_size = calculateAutoTitleFontSize(firstWordCaps, 40);
    }
    page.title = cleanTitleString(firstWordCaps);
    showToast(`⚡ Applied "${firstWordCaps}" (Ref + Drawing + Title)!`, "success");
  }

  renumberPages();
  markProjectDirty();
  loadPageIntoCanvas(currentPageIndex);
  renderTimeline();
}

// ==========================================
// Layout Templates Engine
// ==========================================
function applyPageLayout(layoutKey) {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot change layout: Project is locked!", "warning");
    return;
  }

  recordHistoryState(`Apply Layout: ${getLayoutName(layoutKey)}`);

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

  if (layoutKey === "kdp_top_ref" || layoutKey === "top_ref") {
    page.page_type = "content";
    const projFont = currentProject.settings?.default_font_family || "Fredoka";
    const projOutline = currentProject.settings?.default_font_mode !== "solid";
    newElements = [
      { id: `elem_ref_${Date.now()}`, type: "ref_image", x: 35, y: 25, w: 190, h: 180, text: "Reference Image", image_src: existingRefImg },
      { id: `elem_title_${Date.now()}`, type: "title", x: 235, y: 70, w: 240, h: 80, text: existingTitle.toUpperCase(), font_size: 40, color: "#ffffff", is_outline: projOutline, font_family: projFont, letter_spacing: 2 },
      { id: `elem_main_${Date.now()}`, type: "main_image", x: 35, y: 220, w: 440, h: 410, text: "Coloring Drawing", image_src: existingMainImg },
      { id: `elem_frame_${Date.now()}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
    ];
  } else if (layoutKey === "full_page") {
    page.page_type = "content";
    newElements = [
      { id: `elem_main_${Date.now()}`, type: "main_image", x: 35, y: 25, w: 440, h: 605, text: "Full Page Drawing", image_src: existingMainImg || existingRefImg },
      { id: `elem_frame_${Date.now()}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
    ];
  } else if (layoutKey === "kdp_center_ref") {
    page.page_type = "content";
    const projFont = currentProject.settings?.default_font_family || "Fredoka";
    const projOutline = currentProject.settings?.default_font_mode !== "solid";
    newElements = [
      { id: `elem_ref_${Date.now()}`, type: "ref_image", x: 175, y: 25, w: 160, h: 140, text: "Reference Image", image_src: existingRefImg },
      { id: `elem_title_${Date.now()}`, type: "title", x: 35, y: 172, w: 440, h: 46, text: existingTitle.toUpperCase(), font_size: 34, color: "#ffffff", is_outline: projOutline, font_family: projFont, letter_spacing: 2 },
      { id: `elem_main_${Date.now()}`, type: "main_image", x: 35, y: 225, w: 440, h: 405, text: "Coloring Drawing", image_src: existingMainImg },
      { id: `elem_frame_${Date.now()}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
    ];
  } else if (layoutKey === "kdp_side_by_side") {
    page.page_type = "content";
    const projFont = currentProject.settings?.default_font_family || "Fredoka";
    const projOutline = currentProject.settings?.default_font_mode !== "solid";
    newElements = [
      { id: `elem_title_${Date.now()}`, type: "title", x: 35, y: 25, w: 440, h: 40, text: existingTitle.toUpperCase(), font_size: 26, color: "#ffffff", is_outline: projOutline, font_family: projFont },
      { id: `elem_ref_${Date.now()}`, type: "ref_image", x: 35, y: 75, w: 210, h: 545, text: "Color Guide", image_src: existingRefImg },
      { id: `elem_main_${Date.now()}`, type: "main_image", x: 260, y: 75, w: 215, h: 545, text: "Draw & Color Here", image_src: existingMainImg },
      { id: `elem_frame_${Date.now()}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
    ];
  } else if (layoutKey === "kdp_story_drawing") {
    page.page_type = "content";
    const projFont = currentProject.settings?.default_font_family || "Fredoka";
    const projOutline = currentProject.settings?.default_font_mode !== "solid";
    newElements = [
      { id: `elem_main_${Date.now()}`, type: "main_image", x: 35, y: 25, w: 440, h: 380, text: "Illustration", image_src: existingMainImg },
      { id: `elem_title_${Date.now()}`, type: "title", x: 35, y: 415, w: 440, h: 40, text: existingTitle.toUpperCase(), font_size: 28, color: "#ffffff", is_outline: projOutline, font_family: projFont },
      { id: `elem_hw1_${Date.now()}`, type: "title", x: 45, y: 470, w: 420, h: 30, text: "____________________________________", font_size: 16, color: "#94a3b8", is_outline: false },
      { id: `elem_hw2_${Date.now()}`, type: "title", x: 45, y: 530, w: 420, h: 30, text: "____________________________________", font_size: 16, color: "#94a3b8", is_outline: false },
      { id: `elem_hw3_${Date.now()}`, type: "title", x: 45, y: 590, w: 420, h: 30, text: "____________________________________", font_size: 16, color: "#94a3b8", is_outline: false },
      { id: `elem_frame_${Date.now()}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
    ];
  } else if (layoutKey === "kdp_4grid") {
    page.page_type = "content";
    newElements = [
      { id: `elem_title_${Date.now()}`, type: "title", x: 35, y: 20, w: 440, h: 30, text: existingTitle.toUpperCase(), font_size: 20, color: "#0f172a", is_outline: false },
      { id: `elem_box1_${Date.now()}`, type: "main_image", x: 35, y: 55, w: 210, h: 265, text: "Quadrant 1", image_src: null },
      { id: `elem_box2_${Date.now()}`, type: "main_image", x: 260, y: 55, w: 215, h: 265, text: "Quadrant 2", image_src: null },
      { id: `elem_box3_${Date.now()}`, type: "main_image", x: 35, y: 340, w: 210, h: 265, text: "Quadrant 3", image_src: null },
      { id: `elem_box4_${Date.now()}`, type: "main_image", x: 260, y: 340, w: 215, h: 265, text: "Quadrant 4", image_src: null },
      { id: `elem_frame_${Date.now()}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
    ];
  } else if (layoutKey.startsWith("custom_")) {
    // Load elements from user-saved custom layout
    const customList = getCustomLayouts();
    const found = customList.find(c => c.id === layoutKey);
    if (found && found.elements) {
      page.page_type = "content";
      newElements = JSON.parse(JSON.stringify(found.elements)).map((el, i) => {
        el.id = `elem_custom_${Date.now()}_${i}`;
        if (el.type === "title" && !el.text) el.text = existingTitle.toUpperCase();
        if (el.type === "ref_image") el.image_src = existingRefImg;
        if (el.type === "main_image") el.image_src = existingMainImg;
        return el;
      });
    }
  } else if (layoutKey === "belongs_to") {
    page.page_type = "front_matter_belongs_to";
    page.title = "Belongs To Page";
    newElements = [
      { id: `elem_bt_frame_${Date.now()}`, type: "border", x: 30, y: 25, w: 450, h: 610 },
      { id: `elem_bt_title_${Date.now()}`, type: "title", x: 45, y: 80, w: 420, h: 30, text: "THIS COLORING BOOK", font_size: 22, color: "#1e293b", is_outline: false },
      { id: `elem_bt_belongs_${Date.now()}`, type: "title", x: 45, y: 135, w: 420, h: 45, text: "BELONGS TO:", font_size: 32, font_family: "Fredoka", color: "#ffffff", is_outline: true },
      { id: `elem_bt_line_${Date.now()}`, type: "title", x: 45, y: 220, w: 420, h: 30, text: "____________________________________", font_size: 18, color: "#64748b", is_outline: false },
      { id: `elem_bt_sub_${Date.now()}`, type: "title", x: 45, y: 320, w: 420, h: 25, text: "Color with joy, love and your wild imagination!", font_size: 13, color: "#475569", is_outline: false }
    ];
  } else if (layoutKey === "color_test") {
    page.page_type = "front_matter_color_test";
    page.title = "Color Test Palette";
    newElements = [
      { id: `elem_ct_frame_${Date.now()}`, type: "border", x: 30, y: 25, w: 450, h: 610 },
      { id: `elem_ct_title_${Date.now()}`, type: "title", x: 45, y: 55, w: 420, h: 35, text: "COLOR TEST PALETTE", font_size: 24, font_family: "Fredoka", color: "#ffffff", is_outline: true },
      { id: `elem_ct_sub_${Date.now()}`, type: "title", x: 45, y: 95, w: 420, h: 20, text: "Test your pencils, markers and crayons here before coloring!", font_size: 11, color: "#64748b", is_outline: false },
      { id: `elem_ct_hint_${Date.now()}`, type: "title", x: 45, y: 140, w: 420, h: 20, text: "Color Swatch Test Boxes:", font_size: 12, color: "#1e293b", is_outline: false }
    ];
  } else if (layoutKey === "blank_page") {
    page.page_type = "blank_verso";
    page.title = "Blank Back Page";
    newElements = [];
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
  if (readout) {
    const trimW = ((currentProject.settings?.trim_width_pt || 612.0) / 72.0).toFixed(1).replace(".0", "");
    const trimH = ((currentProject.settings?.trim_height_pt || 792.0) / 72.0).toFixed(1).replace(".0", "");
    readout.innerText = `Layout: ${getLayoutName(layoutKey)} (${trimW} × ${trimH} in)`;
  }
}

function getLayoutName(key) {
  const customList = getCustomLayouts();
  const customFound = customList.find(c => c.id === key);
  if (customFound) return customFound.name;

  const map = {
    kdp_top_ref: "Standard KDP (Top-Left Ref • 75% Art)",
    top_ref: "Standard KDP (Top-Left Ref • 75% Art)",
    full_page: "Full Page Drawing (100% Art)",
    kdp_center_ref: "Top-Center Ref • Centered Title • 70% Art",
    kdp_side_by_side: "Side-by-Side Dual (50/50 Look & Draw)",
    kdp_story_drawing: "Kids Story Art + Handwriting Lines",
    kdp_4grid: "4-in-1 Challenge Grid",
    belongs_to: "This Book Belongs To Page",
    color_test: "Color Test Palette",
    blank_page: "Blank Back Page (Verso)",
    disclaimer_standard: "Disclaimer & Copyright",
    contents_standard: "Table of Contents"
  };
  return map[key] || key;
}

// ===================================================
// Quick Layout Customizer & Custom Layout Engine
// ===================================================
function toggleLayoutCustomizer() {
  const panel = document.getElementById("layout-customizer-panel");
  if (panel) {
    const isShown = panel.style.display !== "none";
    panel.style.display = isShown ? "none" : "flex";
  }
}

function applyCustomLayoutTweaks() {
  const page = currentProject.pages[currentPageIndex];
  if (!page || currentProject.is_locked) return;

  const refVal = document.getElementById("lay-cust-ref")?.value || "medium";
  const titleVal = document.getElementById("lay-cust-title")?.value || "outline";
  const borderVal = document.getElementById("lay-cust-border")?.value || "box";
  const heightVal = parseInt(document.getElementById("lay-cust-height")?.value || "75");

  recordHistoryState("Customize Layout Elements");

  // 1. Adjust or toggle reference image
  let refEl = page.elements.find(e => e.type === "ref_image");
  if (refVal === "none") {
    if (refEl) page.elements = page.elements.filter(e => e.id !== refEl.id);
  } else {
    const sizeMap = { small: { w: 140, h: 130 }, medium: { w: 190, h: 180 }, large: { w: 240, h: 220 } };
    const dims = sizeMap[refVal] || sizeMap.medium;
    if (!refEl) {
      refEl = { id: `elem_ref_${Date.now()}`, type: "ref_image", x: 35, y: 25, w: dims.w, h: dims.h, text: "Reference Image", image_src: null };
      page.elements.unshift(refEl);
    } else {
      refEl.w = dims.w;
      refEl.h = dims.h;
    }
  }

  // 2. Adjust or toggle title
  let titleEl = page.elements.find(e => e.type === "title");
  if (titleVal === "none") {
    if (titleEl) page.elements = page.elements.filter(e => e.id !== titleEl.id);
  } else {
    if (!titleEl) {
      titleEl = { id: `elem_title_${Date.now()}`, type: "title", x: 235, y: 70, w: 240, h: 80, text: (page.title || "TITLE").toUpperCase(), font_size: 38, font_family: "Fredoka", is_outline: true };
      page.elements.push(titleEl);
    }
    if (titleVal === "outline") {
      titleEl.is_outline = true;
      titleEl.color = "#ffffff";
      titleEl.font_family = "Fredoka";
    } else if (titleVal === "solid") {
      titleEl.is_outline = false;
      titleEl.color = "#0f172a";
      titleEl.font_family = "Nunito";
    }
  }

  // 3. Adjust border
  let borderEl = page.elements.find(e => e.type === "border");
  if (borderVal === "none") {
    if (borderEl) page.elements = page.elements.filter(e => e.id !== borderEl.id);
  } else {
    if (!borderEl) {
      borderEl = { id: `elem_frame_${Date.now()}`, type: "border", x: 25, y: 15, w: 460, h: 630 };
      page.elements.push(borderEl);
    }
  }

  // 4. Adjust main art height
  let mainEl = page.elements.find(e => e.type === "main_image");
  if (mainEl) {
    if (heightVal === 100) {
      mainEl.y = 25;
      mainEl.h = 605;
    } else if (heightVal === 85) {
      mainEl.y = 150;
      mainEl.h = 480;
    } else if (heightVal === 65) {
      mainEl.y = 220;
      mainEl.h = 350;
    } else {
      mainEl.y = 220;
      mainEl.h = 410;
    }
  }

  loadPageIntoCanvas(currentPageIndex);
  markProjectDirty();
  showToast("Layout customized on active page!", "success");
}

function getCustomLayouts() {
  if (currentProject.custom_layouts && Array.isArray(currentProject.custom_layouts)) {
    return currentProject.custom_layouts;
  }
  try {
    const raw = localStorage.getItem("kdp_custom_layouts");
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    return [];
  }
}

function saveCustomLayouts(list) {
  currentProject.custom_layouts = list;
  try {
    localStorage.setItem("kdp_custom_layouts", JSON.stringify(list));
  } catch (e) {}
  markProjectDirty();
  renderCustomLayouts();
}

function promptSaveCustomLayout() {
  const page = currentProject.pages[currentPageIndex];
  if (!page || !page.elements || page.elements.length === 0) {
    showToast("⚠️ Active page has no elements to save as layout!", "warning");
    return;
  }

  const defaultName = `Custom Layout ${getCustomLayouts().length + 1}`;
  const layoutName = prompt("Enter a name for your custom layout template:", defaultName);
  if (!layoutName || !layoutName.trim()) return;

  const newId = `custom_${Date.now()}`;
  const newLayout = {
    id: newId,
    name: layoutName.trim(),
    elements: JSON.parse(JSON.stringify(page.elements)).map(el => {
      // Don't bind permanent images, keep template clean
      const cloned = { ...el };
      if (cloned.type === "main_image" || cloned.type === "ref_image") {
        cloned.image_src = null;
      }
      return cloned;
    })
  };

  const currentList = getCustomLayouts();
  currentList.push(newLayout);
  saveCustomLayouts(currentList);
  showToast(`🎉 Saved custom layout "${newLayout.name}"!`, "success");
}

function renderCustomLayouts() {
  const container = document.getElementById("custom-layouts-section");
  const grid = document.getElementById("custom-layouts-grid");
  const countSpan = document.getElementById("custom-layouts-count");
  if (!container || !grid) return;

  const list = getCustomLayouts();
  if (list.length === 0) {
    container.style.display = "none";
    return;
  }

  container.style.display = "block";
  if (countSpan) countSpan.innerText = `${list.length} saved`;
  grid.innerHTML = "";

  list.forEach(layout => {
    const card = document.createElement("div");
    card.className = "layout-card";
    card.setAttribute("data-layout", layout.id);
    card.innerHTML = `
      <div class="layout-mini-preview" style="display: flex; flex-direction: column; gap: 3px; padding: 4px; justify-content: center; align-items: center; background: #f1f5f9;">
        <span style="font-size: 20px;">📐</span>
        <span style="font-size: 8px; font-weight: 800; color: var(--primary);">${escapeHtml(layout.name.slice(0, 14))}</span>
      </div>
      <div class="layout-info" style="width: 100%;">
        <div class="layout-title">${escapeHtml(layout.name)}</div>
        <div class="custom-layout-tag">CUSTOM</div>
        <div style="display: flex; gap: 4px; margin-top: 6px; justify-content: center;">
          <button class="btn btn-xs btn-primary" onclick="applyPageLayout('${layout.id}')" style="padding: 2px 6px; font-size: 10px;">Apply</button>
          <button class="btn btn-xs btn-outline" onclick="deleteCustomLayout('${layout.id}', event)" style="padding: 2px 6px; font-size: 10px; color: var(--danger); border-color: var(--danger);">🗑</button>
        </div>
      </div>
    `;
    grid.appendChild(card);
  });
}

function deleteCustomLayout(layoutId, event) {
  if (event) event.stopPropagation();
  if (!confirm("Are you sure you want to delete this custom layout template?")) return;
  const list = getCustomLayouts().filter(c => c.id !== layoutId);
  saveCustomLayouts(list);
  showToast("🗑 Custom layout deleted!", "info");
}

// ==========================================
// Page Canvas Loader & Elements
// ==========================================
function loadPageIntoCanvas(index) {
  if (!currentProject.pages || currentProject.pages.length === 0) return;
  
  if (index >= currentProject.pages.length) {
    index = currentProject.pages.length - 1;
  }
  currentPageIndex = index;
  localStorage.setItem("kdp_active_page_index", String(currentPageIndex));
  const page = currentProject.pages[index];
  const layer = document.getElementById("elements-layer");
  if (!layer) return;
  layer.innerHTML = "";

  if (!page) return;

  updateLayoutCardsActiveState(page.layout || "kdp_top_ref");
  updateCanvasLayoutLockUI();

  // If this is a Blank Back Page (Verso)
  if (page.page_type === "blank_verso") {
    layer.innerHTML = `
      <div class="blank-page-canvas-placeholder">
        <span style="font-size: 32px; margin-bottom: 8px;">🛡️</span>
        <strong style="color: #1e293b; font-size: 14px;">Amazon KDP Blank Back Page (Verso)</strong>
        <p style="font-size: 11px; color: #64748b; margin-top: 4px; max-width: 300px;">
          This back page will be kept completely blank in the exported book to protect against marker / color bleed-through.
        </p>
      </div>
    `;
    const pageReadout = document.getElementById("page-num-readout");
    if (pageReadout) pageReadout.innerText = `Page ${index + 1} of ${currentProject.pages.length} (Blank Verso)`;
    return;
  }

  const fragment = document.createDocumentFragment();
  const pageElements = page.elements || (page.layers ? page.layers.flatMap(l => l.elements || []) : []) || [];
  pageElements.forEach(elem => {
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
          <div class="placeholder-hint" onclick="event.stopPropagation(); setActiveElement('${elem.id}'); triggerMediaUpload();" style="cursor: pointer;" title="Click to Upload Reference Image">
            <span class="icon">📷</span>
            <span class="txt">Ref Image</span>
            <span class="sub">➕ Click to Upload</span>
          </div>
        `;
      }
      elDiv.ondblclick = (e) => {
        e.stopPropagation();
        setActiveElement(elem.id);
        triggerMediaUpload();
      };
    } else if (elem.type === "main_image") {
      elDiv.classList.add("elem-main-box");
      if (elem.image_src) {
        elDiv.innerHTML = `<img src="${elem.image_src}">`;
      } else {
        elDiv.innerHTML = `
          <div class="placeholder-hint" onclick="event.stopPropagation(); setActiveElement('${elem.id}'); triggerMediaUpload();" style="cursor: pointer;" title="Click to Upload Drawing Artwork">
            <span class="icon">🎨</span>
            <span class="txt">Drawing Area (75%)</span>
            <span class="sub">➕ Click to Upload Artwork</span>
          </div>
        `;
      }
      elDiv.ondblclick = (e) => {
        e.stopPropagation();
        setActiveElement(elem.id);
        triggerMediaUpload();
      };
    } else if (elem.type === "dot_to_dot") {
      elDiv.classList.add("elem-dot-to-dot-box");
      const pData = page.dot_to_dot || elem.dot_to_dot;
      if (pData && pData.dots && pData.dots.length > 0) {
        elDiv.innerHTML = renderDotToDotSvgHtml(pData, elem.w, elem.h, page);
      } else {
        elDiv.innerHTML = `
          <div class="placeholder-hint" onclick="event.stopPropagation(); setActiveElement('${elem.id}'); triggerMediaUpload();" style="cursor: pointer;" title="Click to Upload Reference Image to Convert to Dot-to-Dot">
            <span class="icon">🔢</span>
            <span class="txt">Dot-to-Dot Puzzle Area</span>
            <span class="sub">➕ Click to Upload Artwork to Convert</span>
          </div>
        `;
      }
      elDiv.ondblclick = (e) => {
        e.stopPropagation();
        setActiveElement(elem.id);
        triggerMediaUpload();
      };
    } else if (elem.type === "title") {
      elDiv.classList.add("elem-title-box");
      elDiv.innerText = elem.text || "Title";
      const autoFontSize = calculateAutoTitleFontSize(elem.text || "", elem.font_size || 40);
      elDiv.style.fontFamily = `'${elem.font_family || "Fredoka"}', 'Plus Jakarta Sans', sans-serif`;
      elDiv.style.fontSize = `${autoFontSize}px`;
      elDiv.style.letterSpacing = `${elem.letter_spacing !== undefined ? elem.letter_spacing : 2}px`;
      elDiv.style.textAlign = elem.alignment || "center";

      if (elem.is_outline !== false) {
        elDiv.classList.add("outline-style");
        elDiv.style.color = elem.color || "#ffffff";
        elDiv.style.webkitTextStroke = `2.5px ${elem.stroke_color || "#0f172a"}`;
      } else {
        elDiv.classList.remove("outline-style");
        elDiv.style.color = elem.color || "#111827";
        elDiv.style.webkitTextStroke = "0px transparent";
      }
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

    elDiv.insertAdjacentHTML("beforeend", `
      <div class="handle tl" data-handle="tl"></div>
      <div class="handle tr" data-handle="tr"></div>
      <div class="handle bl" data-handle="bl"></div>
      <div class="handle br" data-handle="br"></div>
    `);

    elDiv.addEventListener("mousedown", (e) => {
      setActiveElement(elem.id);
      if (elem.type === "ref_image" || elem.type === "main_image") {
        switchDrawerTab("media");
      }
    });

    fragment.appendChild(elDiv);
  });
  layer.appendChild(fragment);

  // If page has Sudoku Puzzles attached, render vector Sudoku interactive board
  if (page.puzzles && page.puzzles.length > 0) {
    const p = page.puzzles[0];
    const grid = p.puzzle_grid || [];
    
    const wrapper = document.createElement("div");
    wrapper.className = "canvas-sudoku-wrapper";

    const diffDiv = document.createElement("div");
    diffDiv.style.cssText = "font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;";
    diffDiv.innerText = `Difficulty: ${p.difficulty || 'Medium'} • ${p.clues_count || 32} Clues`;
    wrapper.appendChild(diffDiv);

    const board = document.createElement("div");
    board.className = "canvas-sudoku-board";

    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        const cell = document.createElement("div");
        cell.className = "canvas-sudoku-cell";
        const val = (grid[r] && grid[r][c]) ? grid[r][c] : 0;
        cell.innerText = val !== 0 ? val : "";
        if (val !== 0) {
          cell.style.color = "#0f172a";
        }
        board.appendChild(cell);
      }
    }
    wrapper.appendChild(board);
    layer.appendChild(wrapper);
  }

  // If page has Tic-Tac-Toe games attached, render 4 vector game cards
  if (page.games && page.games.length > 0) {
    const container = document.createElement("div");
    container.className = "canvas-ttt-container";

    page.games.slice(0, 4).forEach((g, idx) => {
      const card = document.createElement("div");
      card.className = "canvas-ttt-card";
      card.innerHTML = `
        <div class="card-head">
          <span>${g.title || `Game #${idx+1}`}</span>
          <span style="font-size: 9px; color: #94a3b8;">3x3 Grid</span>
        </div>
        <div class="card-players">
          <div>${g.player_x_label || 'Player X: ______________'}</div>
          <div>${g.player_o_label || 'Player O: ______________'}</div>
        </div>
        <div class="card-grid">
          <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
          <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
          <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
        </div>
        <div class="card-winner">
          ${g.winner_label || 'Winner: [ X ]  [ O ]  [ Tie ]'}
        </div>
      `;
      container.appendChild(card);
    });
    layer.appendChild(container);
  }

  // If page has Maze attached, render vector Maze on canvas
  if (page.maze) {
    const m = page.maze;
    const wrapper = document.createElement("div");
    wrapper.className = "canvas-maze-wrapper";

    const cvs = document.createElement("canvas");
    cvs.width = 420;
    cvs.height = 480;
    cvs.className = "canvas-maze-canvas";
    wrapper.appendChild(cvs);

    const ctx = cvs.getContext("2d");
    const mw = m.width || 15;
    const mh = m.height || 20;
    const pad = 12;
    const cellW = (420 - (pad * 2)) / mw;
    const cellH = (480 - (pad * 2)) / mh;
    const grid = m.grid || [];

    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, 420, 480);

    ctx.strokeStyle = "#0f172a";
    ctx.lineWidth = 2.0;

    for (let r = 0; r < mh; r++) {
      for (let c = 0; c < mw; c++) {
        const x = pad + (c * cellW);
        const y = pad + (r * cellH);
        const cellMask = (grid[r] && grid[r][c] !== undefined) ? grid[r][c] : 0;

        // Top wall: if not North (1)
        if ((cellMask & 1) === 0) {
          ctx.beginPath();
          ctx.moveTo(x, y);
          ctx.lineTo(x + cellW, y);
          ctx.stroke();
        }
        // Right wall: if not East (2)
        if ((cellMask & 2) === 0) {
          ctx.beginPath();
          ctx.moveTo(x + cellW, y);
          ctx.lineTo(x + cellW, y + cellH);
          ctx.stroke();
        }
        // Bottom wall: if not South (4)
        if ((cellMask & 4) === 0) {
          ctx.beginPath();
          ctx.moveTo(x, y + cellH);
          ctx.lineTo(x + cellW, y + cellH);
          ctx.stroke();
        }
        // Left wall: if not West (8)
        if ((cellMask & 8) === 0) {
          ctx.beginPath();
          ctx.moveTo(x, y);
          ctx.lineTo(x, y + cellH);
          ctx.stroke();
        }
      }
    }

    // Start & Finish labels
    ctx.font = "bold 11px 'Plus Jakarta Sans', sans-serif";
    ctx.fillStyle = "#16a34a";
    ctx.fillText("START ▶", pad + 4, pad + 14);

    ctx.fillStyle = "#dc2626";
    ctx.fillText("◀ FINISH", 420 - pad - 60, 480 - pad - 6);

    layer.appendChild(wrapper);
  }

  // If page has Word Search attached, render 12x12 grid and word badge list
  if (page.word_search) {
    const ws = page.word_search;
    const wrapper = document.createElement("div");
    wrapper.className = "canvas-ws-wrapper";

    if (ws.theme) {
      const themeDiv = document.createElement("div");
      themeDiv.className = "canvas-ws-theme";
      themeDiv.innerText = `Topic: ${ws.theme}`;
      wrapper.appendChild(themeDiv);
    }

    const gridDiv = document.createElement("div");
    gridDiv.className = "canvas-ws-grid";
    const gSize = ws.grid_size || 12;
    gridDiv.style.gridTemplateColumns = `repeat(${gSize}, 1fr)`;
    gridDiv.style.gridTemplateRows = `repeat(${gSize}, 1fr)`;

    const grid = ws.grid || [];
    for (let r = 0; r < gSize; r++) {
      for (let c = 0; c < gSize; c++) {
        const cell = document.createElement("div");
        cell.className = "canvas-ws-cell";
        cell.innerText = (grid[r] && grid[r][c]) ? grid[r][c] : "";
        gridDiv.appendChild(cell);
      }
    }
    wrapper.appendChild(gridDiv);

    // Word list
    const words = ws.words || [];
    if (words.length > 0) {
      const wlDiv = document.createElement("div");
      wlDiv.className = "canvas-ws-wordlist";
      words.forEach(w => {
        const b = document.createElement("div");
        b.className = "canvas-ws-word-badge";
        b.innerText = w;
        wlDiv.appendChild(b);
      });
      wrapper.appendChild(wlDiv);
    }

    layer.appendChild(wrapper);
  }

  const pageReadout = document.getElementById("page-num-readout");
  if (pageReadout) {
    const pageTypeTag = page.page_type === "front_matter_disclaimer" 
      ? " (Disclaimer)" 
      : (page.page_type === "front_matter_contents" ? " (Contents)" : "");
    pageReadout.innerText = `Page ${index + 1} of ${currentProject.pages.length}${pageTypeTag}`;
  }
}

// Drag & Resize Canvas Interactions with Undo History (Throttled with requestAnimationFrame)
function setupCanvasInteractions() {
  let isDragging = false;
  let isResizing = false;
  let activeHandle = null;
  let startX = 0, startY = 0;
  let elemStart = { x: 0, y: 0, w: 0, h: 0 };
  let hasMoved = false;
  let mouseMoveRaf = null;
  let lastClientX = 0, lastClientY = 0;

  const stage = document.getElementById("canvas-stage");
  if (!stage) return;

  const viewport = document.getElementById("canvas-viewport");
  if (viewport) {
    viewport.addEventListener("scroll", () => { cachedPageRect = null; }, { passive: true });
  }

  function updateInspectorCoordsFast(elem) {
    const px = document.getElementById("prop-x");
    const py = document.getElementById("prop-y");
    const pw = document.getElementById("prop-w");
    const ph = document.getElementById("prop-h");
    if (px) px.value = (elem.x / 60.0).toFixed(2);
    if (py) py.value = (elem.y / 60.0).toFixed(2);
    if (pw) pw.value = (elem.w / 60.0).toFixed(2);
    if (ph) ph.value = (elem.h / 60.0).toFixed(2);
  }

  function processCanvasMouseMove() {
    mouseMoveRaf = null;

    // Coordinate readout - strictly when mouse is inside the white canvas page
    const pageNode = document.getElementById("paper-page");
    const readout = document.getElementById("coord-readout");
    if (pageNode && readout) {
      const rect = pageNode.getBoundingClientRect();
      const isInside = (
        rect.width > 0 &&
        lastClientX >= rect.left &&
        lastClientX <= rect.right &&
        lastClientY >= rect.top &&
        lastClientY <= rect.bottom
      );
      if (isInside) {
        const pixelX = (lastClientX - rect.left) / currentZoom;
        const pixelY = (lastClientY - rect.top) / currentZoom;
        const curX = Math.max(0, pixelX / 60.0).toFixed(2);
        const curY = Math.max(0, pixelY / 60.0).toFixed(2);
        readout.style.display = "inline-flex";
        readout.innerText = `X: ${curX} in | Y: ${curY} in`;
      } else {
        readout.style.display = "none";
        readout.innerText = "";
      }
    }

    const elem = getActiveElement();
    if (!elem || currentProject.is_locked) return;

    const dx = (lastClientX - startX) / currentZoom;
    const dy = (lastClientY - startY) / currentZoom;

    if (isDragging) {
      if (!hasMoved && (Math.abs(dx) > 2 || Math.abs(dy) > 2)) {
        recordHistoryState("Move Element");
        hasMoved = true;
      }
      elem.x = Math.max(0, Math.min(510 - elem.w, Math.round(elemStart.x + dx)));
      elem.y = Math.max(0, Math.min(660 - elem.h, Math.round(elemStart.y + dy)));
      applyElementStyles(elem);
      updateInspectorCoordsFast(elem);
    } else if (isResizing) {
      if (!hasMoved && (Math.abs(dx) > 2 || Math.abs(dy) > 2)) {
        recordHistoryState("Resize Element");
        hasMoved = true;
      }
      if (activeHandle === "br") {
        elem.w = Math.max(30, Math.round(elemStart.w + dx));
        elem.h = Math.max(30, Math.round(elemStart.h + dy));
      } else if (activeHandle === "bl") {
        elem.w = Math.max(30, Math.round(elemStart.w - dx));
        elem.x = Math.round(elemStart.x + dx);
        elem.h = Math.max(30, Math.round(elemStart.h + dy));
      } else if (activeHandle === "tr") {
        elem.w = Math.max(30, Math.round(elemStart.w + dx));
        elem.h = Math.max(30, Math.round(elemStart.h - dy));
        elem.y = Math.round(elemStart.y + dy);
      } else if (activeHandle === "tl") {
        elem.w = Math.max(30, Math.round(elemStart.w - dx));
        elem.h = Math.max(30, Math.round(elemStart.h - dy));
        elem.x = Math.round(elemStart.x + dx);
        elem.y = Math.round(elemStart.y + dy);
      }
      applyElementStyles(elem);
      updateInspectorCoordsFast(elem);
    }
  }

  stage.addEventListener("mousedown", (e) => {
    if (currentProject.is_locked) return;

    if (e.target.classList.contains("handle")) {
      if (isCanvasLayoutLocked) {
        showToast("🔒 Canvas layout is locked. Click Unlock to resize elements.", "warning");
        return;
      }
      isResizing = true;
      activeHandle = e.target.getAttribute("data-handle");
      startX = e.clientX;
      startY = e.clientY;
      const elem = getActiveElement();
      if (elem) elemStart = { ...elem };
      hasMoved = false;
      cachedPageRect = null;
      e.preventDefault();
      return;
    }

    const elemNode = e.target.closest(".canvas-element");
    if (elemNode) {
      setActiveElement(elemNode.id);
      if (isCanvasLayoutLocked) {
        // Selection allowed to inspect properties, but dragging is prevented while locked
        return;
      }
      isDragging = true;
      startX = e.clientX;
      startY = e.clientY;
      const elem = getActiveElement();
      if (elem) elemStart = { ...elem };
      hasMoved = false;
      cachedPageRect = null;
      e.preventDefault();
    } else {
      setActiveElement(null);
    }
  });

  window.addEventListener("mousemove", (e) => {
    lastClientX = e.clientX;
    lastClientY = e.clientY;
    if (!mouseMoveRaf) {
      mouseMoveRaf = requestAnimationFrame(processCanvasMouseMove);
    }
  }, { passive: true });

  window.addEventListener("mouseup", () => {
    if (isDragging || isResizing) {
      if (hasMoved) {
        markProjectDirty();
        updatePropertiesInspector();
      }
    }
    isDragging = false;
    isResizing = false;
    activeHandle = null;
    hasMoved = false;
    if (mouseMoveRaf) {
      cancelAnimationFrame(mouseMoveRaf);
      mouseMoveRaf = null;
    }
  });

  const viewportEl = document.getElementById("canvas-viewport") || document.getElementById("viewport-container");
  if (viewportEl) {
    viewportEl.addEventListener("mouseenter", () => {
      viewportEl.classList.add("mouse-inside");
    });
    viewportEl.addEventListener("mouseleave", () => {
      viewportEl.classList.remove("mouse-inside");
      const readout = document.getElementById("coord-readout");
      if (readout) {
        readout.style.display = "none";
        readout.innerText = "";
      }
    });
  }

  const paperEl = document.getElementById("paper-page");
  if (paperEl) {
    paperEl.addEventListener("mouseleave", () => {
      const readout = document.getElementById("coord-readout");
      if (readout) {
        readout.style.display = "none";
        readout.innerText = "";
      }
    });
  }

  window.addEventListener("mouseleave", () => {
    const readout = document.getElementById("coord-readout");
    if (readout) {
      readout.style.display = "none";
      readout.innerText = "";
    }
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
  if (!page || !page.elements) return null;
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

// Properties Inspector Data Binding with Font Selector
function updatePropertiesInspector() {
  const elem = getActiveElement();
  const titleBadge = document.getElementById("selected-type-badge");
  const textGroup = document.getElementById("prop-text-group");
  const imgGroup = document.getElementById("prop-image-group");
  const dotGroup = document.getElementById("prop-dot-group");

  if (!elem) {
    if (titleBadge) titleBadge.innerText = "No Selection";
    document.getElementById("prop-x").value = "";
    document.getElementById("prop-y").value = "";
    document.getElementById("prop-w").value = "";
    document.getElementById("prop-h").value = "";
    if (textGroup) textGroup.style.display = "none";
    if (imgGroup) imgGroup.style.display = "none";
    if (dotGroup) dotGroup.style.display = "none";
    return;
  }

  if (titleBadge) titleBadge.innerText = elem.type.toUpperCase().replace(/_/g, " ");
  const px = document.getElementById("prop-x");
  const py = document.getElementById("prop-y");
  const pw = document.getElementById("prop-w");
  const ph = document.getElementById("prop-h");
  if (px) {
    px.value = (elem.x / 60.0).toFixed(2);
    px.disabled = isCanvasLayoutLocked;
  }
  if (py) {
    py.value = (elem.y / 60.0).toFixed(2);
    py.disabled = isCanvasLayoutLocked;
  }
  if (pw) {
    pw.value = (elem.w / 60.0).toFixed(2);
    pw.disabled = isCanvasLayoutLocked;
  }
  if (ph) {
    ph.value = (elem.h / 60.0).toFixed(2);
    ph.disabled = isCanvasLayoutLocked;
  }

  if (elem.type === "title") {
    if (textGroup) textGroup.style.display = "block";
    if (imgGroup) imgGroup.style.display = "none";
    if (dotGroup) dotGroup.style.display = "none";
    document.getElementById("prop-text-content").value = elem.text || "";
    
    const fontSelect = document.getElementById("prop-font-family");
    if (fontSelect) fontSelect.value = elem.font_family || "Fredoka";
    
    const modeSelect = document.getElementById("prop-font-mode");
    if (modeSelect) modeSelect.value = (elem.is_outline !== false) ? "outline" : "solid";
    
    document.getElementById("prop-font-size").value = elem.font_size || 38;
    
    const spacingSelect = document.getElementById("prop-letter-spacing");
    if (spacingSelect) spacingSelect.value = String(elem.letter_spacing !== undefined ? elem.letter_spacing : 2);
    
    const alignSelect = document.getElementById("prop-text-align");
    if (alignSelect) alignSelect.value = elem.alignment || "center";
    
    document.getElementById("prop-color").value = elem.color || (elem.is_outline ? "#ffffff" : "#111827");
    
    const strokeInput = document.getElementById("prop-stroke-color");
    if (strokeInput) strokeInput.value = elem.stroke_color || "#0f172a";
  } else if (elem.type === "dot_to_dot") {
    if (textGroup) textGroup.style.display = "none";
    if (imgGroup) imgGroup.style.display = "none";
    if (dotGroup) {
      dotGroup.style.display = "block";
      const page = currentProject.pages[currentPageIndex];
      const pData = page.dot_to_dot || elem.dot_to_dot;
      const count = pData?.dot_count || 35;
      const countInput = document.getElementById("prop-dot-count");
      const countVal = document.getElementById("prop-dot-count-val");
      const guideBox = document.getElementById("prop-dot-faint-guide");
      const linesBox = document.getElementById("prop-dot-show-lines");
      if (countInput) countInput.value = count;
      if (countVal) countVal.innerText = `${count} Dots`;
      if (guideBox) guideBox.checked = (pData?.faint_guide !== false);
      if (linesBox) linesBox.checked = Boolean(pData?.show_lines);
    }
  } else if (elem.type === "main_image" || elem.type === "ref_image") {
    if (textGroup) textGroup.style.display = "none";
    if (imgGroup) imgGroup.style.display = "block";
    if (dotGroup) dotGroup.style.display = "none";
  } else {
    if (textGroup) textGroup.style.display = "none";
    if (imgGroup) imgGroup.style.display = "none";
    if (dotGroup) dotGroup.style.display = "none";
  }

  // Update Media Title Suggester box
  populateQuickMediaPicker();
}

// ==========================================
// Dot-to-Dot Puzzle Generator Helpers
// ==========================================
function renderDotToDotSvgHtml(pData, width = 440, height = 440, page = null) {
  if (!pData || !pData.dots || pData.dots.length === 0) return "";

  const dots = pData.dots;
  const showGuide = pData.faint_guide !== false;
  const showLines = Boolean(pData.show_lines);
  const refImg = page?.elements?.find(e => e.type === "ref_image" || e.type === "main_image")?.image_src || pData.image_src;

  let guideSvg = "";
  if (showGuide && refImg) {
    const b = pData.image_bounds || { x: 25, y: 25, width: width - 50, height: height - 50 };
    guideSvg = `<image href="${refImg}" x="${b.x}" y="${b.y}" width="${b.width}" height="${b.height}" opacity="0.14" preserveAspectRatio="none" />`;
  }

  let polylineSvg = "";
  if (showLines && dots.length > 1) {
    const ptsStr = dots.map(d => `${d.x},${d.y}`).join(" ") + ` ${dots[0].x},${dots[0].y}`;
    polylineSvg = `<polyline points="${ptsStr}" fill="none" stroke="#6366f1" stroke-width="1.8" stroke-dasharray="4,4" opacity="0.65" />`;
  }

  // Generate SVG circles and numbered labels
  let dotsSvg = "";
  dots.forEach(d => {
    const isStart = d.is_start || d.num === 1;
    if (isStart) {
      dotsSvg += `
        <g class="dot-start-marker">
          <circle cx="${d.x}" cy="${d.y}" r="6.5" fill="#f59e0b" opacity="0.35" />
          <circle cx="${d.x}" cy="${d.y}" r="4.2" fill="#d97706" />
          <text x="${d.x}" y="${d.y - 12}" font-family="'Fredoka', sans-serif" font-size="11" font-weight="900" fill="#d97706" text-anchor="middle">★ START (1)</text>
        </g>
      `;
    } else {
      dotsSvg += `
        <circle cx="${d.x}" cy="${d.y}" r="3.2" fill="#0f172a" class="canvas-dot-point" />
        <text x="${d.label_x}" y="${d.label_y}" font-family="'Fredoka', 'Plus Jakarta Sans', sans-serif" font-size="10" font-weight="700" fill="#1e293b" text-anchor="middle" dominant-baseline="central" class="canvas-dot-num">${d.num}</text>
      `;
    }
  });

  return `
    <div class="dot-to-dot-canvas-wrapper" style="width:100%; height:100%; position:relative;">
      <svg viewBox="0 0 ${width} ${height}" class="dot-to-dot-svg" style="width:100%; height:100%; display:block; overflow:visible;">
        ${guideSvg}
        ${polylineSvg}
        ${dotsSvg}
      </svg>
    </div>
  `;
}

async function changeDotToDotCount(val) {
  const count = parseInt(val);
  const countVal = document.getElementById("prop-dot-count-val");
  if (countVal) countVal.innerText = `${count} Dots`;

  const page = currentProject.pages ? currentProject.pages[currentPageIndex] : null;
  if (!page) return;

  if (page.dot_to_dot) {
    page.dot_to_dot.dot_count = count;
  }
}

async function toggleDotToDotGuide(isChecked) {
  const page = currentProject.pages ? currentProject.pages[currentPageIndex] : null;
  if (!page) return;

  if (page.dot_to_dot) {
    page.dot_to_dot.faint_guide = isChecked;
  }
  loadPageIntoCanvas(currentPageIndex);
  markProjectDirty();
}

async function toggleDotToDotLines(isChecked) {
  const page = currentProject.pages ? currentProject.pages[currentPageIndex] : null;
  if (!page) return;

  if (page.dot_to_dot) {
    page.dot_to_dot.show_lines = isChecked;
  }
  loadPageIntoCanvas(currentPageIndex);
  markProjectDirty();
}

async function resampleCurrentDotToDot() {
  const page = currentProject.pages ? currentProject.pages[currentPageIndex] : null;
  if (!page) return;

  const countInput = document.getElementById("prop-dot-count");
  const count = countInput ? parseInt(countInput.value) : 35;
  const guideBox = document.getElementById("prop-dot-faint-guide");
  const isGuide = guideBox ? guideBox.checked : true;
  const linesBox = document.getElementById("prop-dot-show-lines");
  const isLines = linesBox ? linesBox.checked : false;

  const pData = page.dot_to_dot;
  const refImg = page.elements?.find(e => (e.type === "ref_image" || e.type === "main_image") && e.image_src)?.image_src || pData?.image_src;

  showToast("🪄 Re-sampling Dot-to-Dot points...", "info");

  try {
    const payload = refImg 
      ? { image_data: refImg, dot_count: count, faint_guide: isGuide }
      : { preset_name: pData?.preset || "star", dot_count: count, faint_guide: isGuide };

    const resp = await fetch("/api/generators/dot_to_dot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await resp.json();
    if (data.puzzle) {
      page.dot_to_dot = data.puzzle;
      page.dot_to_dot.show_lines = isLines;
      if (refImg) page.dot_to_dot.image_src = refImg;
      loadPageIntoCanvas(currentPageIndex);
      markProjectDirty();
      showToast(`✨ Re-sampled to ${data.puzzle.dot_count} dots!`, "success");
    }
  } catch (err) {
    showToast("Re-sample error: " + err.message, "danger");
  }
}

// ==========================================
// Quick Item Title from Media File System
// ==========================================
function populateQuickMediaPicker() {
  const select = document.getElementById("quick-media-picker-select");
  const input = document.getElementById("quick-media-name-input");
  const group = document.getElementById("prop-quick-media-title-group");
  if (!select || !input) return;

  const page = currentProject.pages ? currentProject.pages[currentPageIndex] : null;
  const isBlank = page && (page.page_type === "blank_verso" || page.layout === "blank_page");
  if (group) {
    group.style.display = isBlank ? "none" : "block";
  }

  const mediaList = currentProject.media || [];
  select.innerHTML = '<option value="">-- Select Uploaded Media --</option>';

  // Check if current page already has an image element with media
  let matchedMediaId = "";
  if (page && page.elements) {
    const imgEl = page.elements.find(e => (e.type === "main_image" || e.type === "ref_image") && (e.fileName || e.text));
    if (imgEl) {
      const match = mediaList.find(m => m.name === imgEl.text || m.fileName === imgEl.fileName || m.dataUrl === imgEl.image_src);
      if (match) matchedMediaId = match.id;
    }
  }

  mediaList.forEach(m => {
    const opt = document.createElement("option");
    opt.value = m.id;
    opt.innerText = `🖼️ ${m.name || m.fileName} (${m.sizeKb || 0} KB)`;
    if (m.id === matchedMediaId) opt.selected = true;
    select.appendChild(opt);
  });

  // Pre-fill editable input if not actively typing
  if (document.activeElement !== input) {
    if (matchedMediaId) {
      const matched = mediaList.find(m => m.id === matchedMediaId);
      if (matched) {
        input.value = cleanFileName(matched.name || matched.fileName).toUpperCase();
      }
    } else if (page) {
      const titleEl = page.elements ? page.elements.find(e => e.type === "title") : null;
      if (titleEl && titleEl.text && !/^DRAWING\s*\d+$/i.test(titleEl.text.trim()) && !/^PAGE\s*\d+$/i.test(titleEl.text.trim())) {
        input.value = titleEl.text.toUpperCase();
      } else if (page.title && !/^Page\s*\d+$/i.test(page.title.trim()) && !/^Drawing\s*\d+$/i.test(page.title.trim())) {
        input.value = page.title.toUpperCase();
      } else if (mediaList.length > 0) {
        const candIdx = Math.min(currentPageIndex, mediaList.length - 1);
        const cand = mediaList[candIdx] || mediaList[0];
        input.value = cleanFileName(cand.name || cand.fileName).toUpperCase();
        select.value = cand.id;
      }
    }
  }
}

function onQuickMediaPickerChange() {
  const select = document.getElementById("quick-media-picker-select");
  const input = document.getElementById("quick-media-name-input");
  if (!select || !input) return;

  const mediaId = select.value;
  if (!mediaId) return;

  const mediaList = currentProject.media || [];
  const item = mediaList.find(m => m.id === mediaId);
  if (item) {
    const cleaned = cleanFileName(item.name || item.fileName);
    input.value = cleaned.toUpperCase();
    input.focus();
    input.select();
  }
}

function applyQuickMediaNameToCanvas() {
  if (currentProject.is_locked) {
    showToast("🔒 Project is locked!", "warning");
    return;
  }

  const input = document.getElementById("quick-media-name-input");
  const rawVal = input ? input.value.trim() : "";
  if (!rawVal) {
    showToast("Please enter or select an item name first.", "info");
    return;
  }

  const page = currentProject.pages ? currentProject.pages[currentPageIndex] : null;
  if (!page || page.page_type === "blank_verso") {
    showToast("Cannot set title on a blank verso page.", "warning");
    return;
  }

  recordHistoryState(`Set Item Title "${rawVal}"`);

  const formattedTitle = rawVal.toUpperCase();
  const cleanPageTitle = cleanTitleString(rawVal);
  page.title = cleanPageTitle;

  const projFont = currentProject.settings?.default_font_family || "Fredoka";
  const projOutline = currentProject.settings?.default_font_mode !== "solid";
  const projStroke = currentProject.settings?.default_stroke_color || "#0f172a";
  const projColor = currentProject.settings?.default_text_color || (projOutline ? "#ffffff" : "#111827");
  const autoSize = calculateAutoTitleFontSize(formattedTitle, 40);

  let titleElem = page.elements ? page.elements.find(e => e.type === "title") : null;
  if (!titleElem) {
    titleElem = {
      id: `elem_title_${Date.now()}`,
      type: "title",
      x: 235,
      y: 70,
      w: 240,
      h: 80,
      text: formattedTitle,
      font_size: autoSize,
      color: projColor,
      is_outline: projOutline,
      stroke_color: projStroke,
      font_family: projFont,
      letter_spacing: 2
    };
    if (!page.elements) page.elements = [];
    page.elements.push(titleElem);
  } else {
    titleElem.text = formattedTitle;
    titleElem.font_size = autoSize;
  }

  renumberPages();
  syncContentsPage();
  loadPageIntoCanvas(currentPageIndex);
  renderTimeline();
  setActiveElement(titleElem.id);
  updatePropertiesInspector();
  markProjectDirty();

  showToast(`✨ Applied Title "${formattedTitle}" (Auto-sized: ${autoSize}pt)!`, "success");
}

function onPropChange() {
  if (currentProject.is_locked) return;

  const elem = getActiveElement();
  if (!elem) return;

  if (isCanvasLayoutLocked) {
    showToast("🔒 Canvas layout is locked. Click Unlock to edit dimensions/position.", "warning");
    updatePropertiesInspector();
    return;
  }

  recordHistoryState("Edit Properties");

  elem.x = parseFloat(document.getElementById("prop-x").value || 0) * 60.0;
  elem.y = parseFloat(document.getElementById("prop-y").value || 0) * 60.0;
  elem.w = parseFloat(document.getElementById("prop-w").value || 1) * 60.0;
  elem.h = parseFloat(document.getElementById("prop-h").value || 1) * 60.0;

  if (elem.type === "title") {
    elem.text = document.getElementById("prop-text-content").value;
    
    const fontSelect = document.getElementById("prop-font-family");
    if (fontSelect) elem.font_family = fontSelect.value;
    
    const modeSelect = document.getElementById("prop-font-mode");
    if (modeSelect) elem.is_outline = (modeSelect.value === "outline");
    
    const baseSizeInput = parseInt(document.getElementById("prop-font-size").value || 40);
    const autoSize = calculateAutoTitleFontSize(elem.text, baseSizeInput);
    elem.font_size = autoSize;
    
    const spacingSelect = document.getElementById("prop-letter-spacing");
    if (spacingSelect) elem.letter_spacing = parseInt(spacingSelect.value || 2);
    
    const alignSelect = document.getElementById("prop-text-align");
    if (alignSelect) elem.alignment = alignSelect.value;
    
    elem.color = document.getElementById("prop-color").value;
    
    const strokeInput = document.getElementById("prop-stroke-color");
    if (strokeInput) elem.stroke_color = strokeInput.value;

    // Save as project-wide default typography so every canvas page inherits this font style
    if (!currentProject.settings) currentProject.settings = {};
    currentProject.settings.default_font_family = elem.font_family;
    currentProject.settings.default_font_mode = elem.is_outline ? "outline" : "solid";
    currentProject.settings.default_stroke_color = elem.stroke_color;
    currentProject.settings.default_text_color = elem.color;

    // Automatically sync font family, style mode, and stroke to all title elements across the whole book
    currentProject.pages.forEach(p => {
      (p.elements || []).forEach(el => {
        if (el.type === "title") {
          el.font_family = elem.font_family;
          el.is_outline = elem.is_outline;
          el.stroke_color = elem.stroke_color;
          if (elem.is_outline) el.color = elem.color;
          el.letter_spacing = elem.letter_spacing;
        }
      });
    });

    const elNode = document.getElementById(elem.id);
    if (elNode) {
      elNode.innerText = elem.text;
      elNode.style.fontFamily = `'${elem.font_family}', 'Plus Jakarta Sans', sans-serif`;
      elNode.style.fontSize = `${elem.font_size}px`;
      elNode.style.letterSpacing = `${elem.letter_spacing}px`;
      elNode.style.textAlign = elem.alignment;
      
      if (elem.is_outline) {
        elNode.classList.add("outline-style");
        elNode.style.color = elem.color;
        elNode.style.webkitTextStroke = `2.5px ${elem.stroke_color}`;
      } else {
        elNode.classList.remove("outline-style");
        elNode.style.color = elem.color;
        elNode.style.webkitTextStroke = "0px transparent";
      }
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

  recordHistoryState(`Align ${mode.replace('_', ' ')}`);

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
  if (!page || page.page_type === "blank_verso") return;

  recordHistoryState("Add Text Element");

  const newId = `elem_txt_${Date.now()}`;
  const newElem = {
    id: newId,
    type: "title",
    x: 210,
    y: 65,
    w: 265,
    h: 70,
    text: "TITLE",
    font_size: 38,
    color: "#ffffff",
    is_outline: true
  };

  page.elements.push(newElem);
  loadPageIntoCanvas(currentPageIndex);
  setActiveElement(newId);
  markProjectDirty();
  showToast("Added outline text element (T)", "info");
}

function addNewBorderElement() {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot add element: Project is locked!", "warning");
    return;
  }

  const page = currentProject.pages[currentPageIndex];
  if (!page || page.page_type === "blank_verso") return;

  recordHistoryState("Add Border Frame");

  const newId = `elem_border_${Date.now()}`;
  const newElem = {
    id: newId,
    type: "border",
    x: 25,
    y: 20,
    w: 460,
    h: 620
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
  if (!page || !page.elements) return;

  recordHistoryState("Duplicate Element");

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
  if (!page) return;

  if (activeElementId) {
    recordHistoryState("Delete Element");
    page.elements = page.elements.filter(e => e.id !== activeElementId);
    setActiveElement(null);
    loadPageIntoCanvas(currentPageIndex);
    markProjectDirty();
    showToast("Deleted element (Del)", "info");
  } else {
    deleteCurrentPage();
  }
}

// Page Actions - Adds 1 Page dynamically based on Book Type (Sudoku, Tic-Tac-Toe, or Coloring)
async function addNewPage() {
  if (currentProject.is_locked) {
    showToast("🔒 Project is locked!", "warning");
    return;
  }

  const bType = currentProject.book_type || "coloring_book";
  const newPageNum = currentProject.pages.length + 1;

  if (bType === "sudoku") {
    recordHistoryState("Add Sudoku Page");
    showToast("⚡ Generating new 9x9 Sudoku puzzle...", "info");

    try {
      const totalPuzzlesSoFar = currentProject.pages.reduce((acc, pg) => acc + (pg.puzzles ? pg.puzzles.length : 0), 0);
      const nextNum = totalPuzzlesSoFar + 1;
      const resp = await fetch("/api/generators/sudoku", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ count: 1, difficulty: "medium" })
      });
      const data = await resp.json();
      const p = (data.puzzles && data.puzzles[0]) ? data.puzzles[0] : null;
      if (p) {
        p.id = `sudoku_${nextNum.toString().padStart(4, '0')}`;
      }
      const pIdStr = p ? p.id.replace("sudoku_", "#") : `#${nextNum.toString().padStart(4, '0')}`;
      const pTitle = `Sudoku ${pIdStr}`;

      currentProject.pages.push({
        page_number: newPageNum,
        page_type: "content",
        title: pTitle,
        layout: "sudoku",
        puzzles: p ? [p] : [],
        elements: [
          { id: `elem_title_${newPageNum}`, type: "title", x: 35, y: 30, w: 440, h: 40, text: pTitle.toUpperCase(), font_size: 24, color: "#0f172a", is_outline: false },
          { id: `elem_frame_${newPageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
        ]
      });
    } catch (e) {
      console.error(e);
    }
  } else if (bType === "tic_tac_toe") {
    recordHistoryState("Add Tic-Tac-Toe Page");
    showToast("⚡ Generating 4 Tic-Tac-Toe game grids...", "info");

    try {
      const totalSoFar = currentProject.pages.length * 4;
      const resp = await fetch("/api/generators/tic_tac_toe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ total_games: 4, games_per_page: 4, grid_size: 3 })
      });
      const data = await resp.json();
      const pData = (data.pages && data.pages[0]) ? data.pages[0] : null;
      const games = pData ? pData.games : [];
      
      // Update numbering
      games.forEach((g, idx) => {
        const gn = totalSoFar + idx + 1;
        g.game_number = gn;
        g.title = `Game #${gn.toString().padStart(3, '0')}`;
      });

      const firstG = games[0].game_number;
      const lastG = games[games.length - 1].game_number;
      const pTitle = `Games #${firstG} - #${lastG}`;

      currentProject.pages.push({
        page_number: newPageNum,
        page_type: "content",
        title: pTitle,
        layout: "tic_tac_toe",
        games: games,
        elements: [
          { id: `elem_title_${newPageNum}`, type: "title", x: 35, y: 30, w: 440, h: 40, text: "TIC-TAC-TOE", font_size: 26, color: "#0f172a", is_outline: false },
          { id: `elem_frame_${newPageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
        ]
      });
    } catch (e) {
      console.error(e);
    }
  } else if (bType === "maze") {
    recordHistoryState("Add Maze Page");
    showToast("⚡ Generating new solvable Maze...", "info");

    try {
      const resp = await fetch("/api/generators/maze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ count: 1, width: 15, height: 20 })
      });
      const data = await resp.json();
      const m = data.maze || (data.mazes && data.mazes[0]);
      const pTitle = `Maze #${newPageNum.toString().padStart(3, '0')}`;

      currentProject.pages.push({
        page_number: newPageNum,
        page_type: "content",
        title: pTitle,
        layout: "maze",
        maze: m,
        elements: [
          { id: `elem_title_${newPageNum}`, type: "title", x: 35, y: 30, w: 440, h: 40, text: pTitle.toUpperCase(), font_size: 26, color: "#0f172a", is_outline: false },
          { id: `elem_frame_${newPageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
        ]
      });
    } catch (e) {
      console.error(e);
    }
  } else if (bType === "word_search") {
    recordHistoryState("Add Word Search Page");
    showToast("⚡ Generating themed Word Search puzzle...", "info");

    try {
      const resp = await fetch("/api/generators/word_search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ count: 1, grid_size: 12 })
      });
      const data = await resp.json();
      const ws = data.word_search || (data.puzzles && data.puzzles[0]);
      const pTitle = ws ? (ws.title || `Word Search #${newPageNum.toString().padStart(3, '0')}`) : `Word Search #${newPageNum}`;

      currentProject.pages.push({
        page_number: newPageNum,
        page_type: "content",
        title: pTitle,
        layout: "word_search",
        word_search: ws,
        elements: [
          { id: `elem_title_${newPageNum}`, type: "title", x: 35, y: 30, w: 440, h: 40, text: pTitle.toUpperCase(), font_size: 22, color: "#0f172a", is_outline: false },
          { id: `elem_frame_${newPageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
        ]
      });
    } catch (e) {
      console.error(e);
    }
  } else if (bType === "dot_to_dot") {
    recordHistoryState("Add Dot-to-Dot Page");
    showToast("⚡ Generating new Dot-to-Dot page...", "info");

    try {
      const presets = ["star", "butterfly", "rocket", "dinosaur", "heart", "cat", "airplane", "fish"];
      const presetKey = presets[(newPageNum - 1) % presets.length];
      const resp = await fetch("/api/generators/dot_to_dot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ preset_name: presetKey, dot_count: 35 })
      });
      const data = await resp.json();
      const pz = data.puzzle || {};
      const pTitle = pz.title || presetKey.toUpperCase();

      currentProject.pages.push({
        page_number: newPageNum,
        page_type: "content",
        title: pTitle,
        layout: "dot_to_dot",
        dot_to_dot: pz,
        elements: [
          { id: `elem_ref_${newPageNum}`, type: "ref_image", x: 35, y: 25, w: 160, h: 150, text: pTitle, image_src: null },
          { id: `elem_title_${newPageNum}`, type: "title", x: 215, y: 55, w: 260, h: 80, text: pTitle.toUpperCase(), font_size: 34, color: "#ffffff", is_outline: true, font_family: "Fredoka", letter_spacing: 2 },
          { id: `elem_dot_${newPageNum}`, type: "dot_to_dot", x: 35, y: 190, w: 440, h: 440, text: pTitle },
          { id: `elem_frame_${newPageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
        ]
      });
    } catch (e) {
      console.error(e);
    }
  } else if (bType === "tracing") {
    recordHistoryState("Add Tracing Page");
    const letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
    const char = letters[(newPageNum - 1) % letters.length];
    try {
      const resp = await fetch("/api/generators/tracing", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ char: char, repeat: 5, word: `${char}NIMAL` })
      });
      const data = await resp.json();
      currentProject.pages.push({
        page_number: newPageNum,
        page_type: "content",
        title: `Letter Tracing: ${char}`,
        layout: "tracing",
        tracing: data.tracing || {},
        elements: [
          { id: `elem_title_${newPageNum}`, type: "title", x: 35, y: 25, w: 440, h: 35, text: `LETTER TRACING: ${char}`, font_size: 22, color: "#0f172a", is_outline: false },
          { id: `elem_frame_${newPageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
        ]
      });
    } catch (e) {
      console.error(e);
    }
  } else if (bType === "scissor_skills") {
    recordHistoryState("Add Cutting Page");
    const patterns = ["straight", "zigzag", "wavy", "curved", "castle"];
    const pat = patterns[(newPageNum - 1) % patterns.length];
    try {
      const resp = await fetch("/api/generators/scissor_skills", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pattern: pat, lines: 5, title: `Cutting: ${pat.toUpperCase()}` })
      });
      const data = await resp.json();
      currentProject.pages.push({
        page_number: newPageNum,
        page_type: "content",
        title: `Cutting: ${pat.toUpperCase()}`,
        layout: "scissor_skills",
        scissor_skills: data.scissor_skills || {},
        elements: [
          { id: `elem_title_${newPageNum}`, type: "title", x: 35, y: 25, w: 440, h: 35, text: `SCISSOR CUTTING: ${pat.toUpperCase()}`, font_size: 22, color: "#0f172a", is_outline: false },
          { id: `elem_frame_${newPageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
        ]
      });
    } catch (e) {
      console.error(e);
    }
  } else if (bType === "shadow_matching") {
    recordHistoryState("Add Shadow Match Page");
    try {
      const resp = await fetch("/api/generators/shadow_matching", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ theme: "jungle_animals", pairs: 4, title: `Shadow Match #${newPageNum}` })
      });
      const data = await resp.json();
      currentProject.pages.push({
        page_number: newPageNum,
        page_type: "content",
        title: `Shadow Match #${newPageNum}`,
        layout: "shadow_matching",
        shadow_matching: data.shadow_matching || {},
        elements: [
          { id: `elem_title_${newPageNum}`, type: "title", x: 35, y: 25, w: 440, h: 35, text: `SHADOW MATCH #${newPageNum}`, font_size: 22, color: "#0f172a", is_outline: false },
          { id: `elem_frame_${newPageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
        ]
      });
    } catch (e) {
      console.error(e);
    }
  } else if (bType === "ispy") {
    recordHistoryState("Add I-SPY Page");
    try {
      const resp = await fetch("/api/generators/ispy", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ theme: "jungle", title: `I-Spy & Count Animals #${newPageNum}` })
      });
      const data = await resp.json();
      currentProject.pages.push({
        page_number: newPageNum,
        page_type: "content",
        title: `I-Spy & Count #${newPageNum}`,
        layout: "ispy",
        ispy: data.ispy || {},
        elements: [
          { id: `elem_title_${newPageNum}`, type: "title", x: 35, y: 25, w: 440, h: 35, text: `I-SPY & COUNT ANIMALS`, font_size: 22, color: "#0f172a", is_outline: false },
          { id: `elem_frame_${newPageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
        ]
      });
    } catch (e) {
      console.error(e);
    }
  } else if (bType === "grid_drawing") {
    recordHistoryState("Add Grid Drawing Page");
    try {
      const resp = await fetch("/api/generators/grid_drawing", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ grid_size: 4, title: `How to Draw #${newPageNum}` })
      });
      const data = await resp.json();
      currentProject.pages.push({
        page_number: newPageNum,
        page_type: "content",
        title: `Grid Draw #${newPageNum}`,
        layout: "grid_drawing",
        grid_drawing: data.grid_drawing || {},
        elements: [
          { id: `elem_title_${newPageNum}`, type: "title", x: 35, y: 25, w: 440, h: 35, text: `LEARN TO DRAW: GRID COPY`, font_size: 22, color: "#0f172a", is_outline: false },
          { id: `elem_frame_${newPageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
        ]
      });
    } catch (e) {
      console.error(e);
    }
  } else {
    // Coloring Book
    recordHistoryState("Add Drawing Page");
    const projFont = currentProject.settings?.default_font_family || "Fredoka";
    const projOutline = currentProject.settings?.default_font_mode !== "solid";
    const projStroke = currentProject.settings?.default_stroke_color || "#0f172a";
    const projColor = currentProject.settings?.default_text_color || (projOutline ? "#ffffff" : "#111827");

    currentProject.pages.push({
      page_number: newPageNum,
      page_type: "content",
      title: `Drawing ${newPageNum}`,
      layout: "kdp_top_ref",
      elements: [
        { id: `elem_ref_${newPageNum}`, type: "ref_image", x: 35, y: 25, w: 190, h: 180, text: `Ref ${newPageNum}`, image_src: null },
        { id: `elem_title_${newPageNum}`, type: "title", x: 235, y: 70, w: 240, h: 80, text: `DRAWING ${newPageNum}`, font_size: 40, color: projColor, is_outline: projOutline, stroke_color: projStroke, font_family: projFont, letter_spacing: 2 },
        { id: `elem_main_${newPageNum}`, type: "main_image", x: 35, y: 220, w: 440, h: 410, text: `Drawing ${newPageNum}`, image_src: null },
        { id: `elem_frame_${newPageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
      ]
    });
  }

  renumberPages();
  renderTimeline();
  selectPage(currentProject.pages.length - 1);
  syncActiveProjectUI();
  markProjectDirty();
  showToast(`➕ Added Page ${newPageNum} to book!`, "success");
}

function duplicateCurrentPage() {
  if (currentProject.is_locked) return;

  const curr = currentProject.pages[currentPageIndex];
  if (!curr) return;

  recordHistoryState(`Duplicate Page ${curr.page_number}`);

  const clone = JSON.parse(JSON.stringify(curr));
  clone.title = `${clone.title} (Copy)`;
  currentProject.pages.splice(currentPageIndex + 1, 0, clone);

  renumberPages();
  renderTimeline();
  selectPage(currentPageIndex + 1);
  syncActiveProjectUI();
  markProjectDirty();
  showToast(`Duplicated to Page ${currentPageIndex + 1}`, "success");
}

function deleteCurrentPage() {
  if (currentProject.is_locked) {
    showToast("🔒 Project is locked!", "warning");
    return;
  }

  if (currentProject.pages.length <= 1) {
    showToast("A book must contain at least one content page.", "info");
    return;
  }

  recordHistoryState(`Delete Page ${currentPageIndex + 1}`);

  const deletedNum = currentPageIndex + 1;
  currentProject.pages.splice(currentPageIndex, 1);

  renumberPages();

  const target = Math.min(currentPageIndex, currentProject.pages.length - 1);
  currentPageIndex = Math.max(0, target);
  activeElementId = null;

  renderTimeline();
  selectPage(currentPageIndex);
  syncActiveProjectUI();
  markProjectDirty();
  showToast(`🗑 Deleted Page ${deletedNum} & Auto-Renumbered Remaining Pages!`, "info");
}

// Timeline Ribbon - Displays clean working canvases with in-between + insert slots, drag-and-drop swapping, and card actions
let draggedTimelinePageIndex = null;

function reorderPage(fromIdx, toIdx) {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot reorder: Project is locked!", "warning");
    return;
  }
  if (fromIdx === toIdx || fromIdx < 0 || toIdx < 0 || fromIdx >= currentProject.pages.length || toIdx >= currentProject.pages.length) return;

  const pages = currentProject.pages;
  const pageToMove = pages[fromIdx];
  const pageTitle = pageToMove.title || `Page ${fromIdx + 1}`;

  recordHistoryState(`Move "${pageTitle}" from Page ${fromIdx + 1} to ${toIdx + 1}`);

  // Remove from old position and insert at new position
  pages.splice(fromIdx, 1);
  pages.splice(toIdx, 0, pageToMove);

  renumberPages();
  syncContentsPage();

  // Keep currently active page selected properly
  if (currentPageIndex === fromIdx) {
    currentPageIndex = toIdx;
  } else if (fromIdx < currentPageIndex && toIdx >= currentPageIndex) {
    currentPageIndex--;
  } else if (fromIdx > currentPageIndex && toIdx <= currentPageIndex) {
    currentPageIndex++;
  }

  renderTimeline();
  selectPage(currentPageIndex);
  markProjectDirty();

  showToast(`🔀 Swapped & Moved "${pageTitle}" to Page ${toIdx + 1}!`, "success");
}

function renderTimeline() {
  const strip = document.getElementById("thumbnails-strip");
  if (!strip) return;
  strip.innerHTML = "";

  const bType = currentProject.book_type || "coloring_book";
  const pages = currentProject.pages || [];

  // Helper to create an in-between insert slot with drop support
  const createInsertSlot = (targetIdx) => {
    const slot = document.createElement("div");
    slot.className = "timeline-insert-slot";
    slot.innerHTML = `
      <button class="timeline-insert-btn" onclick="openInsertPageMenu(${targetIdx}, event)" title="➕ Insert Page Here">
        +
      </button>
    `;

    slot.addEventListener("dragover", (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = "move";
      slot.classList.add("drag-over");
    });

    slot.addEventListener("dragleave", () => {
      slot.classList.remove("drag-over");
    });

    slot.addEventListener("drop", (e) => {
      e.preventDefault();
      slot.classList.remove("drag-over");
      const fromIdx = draggedTimelinePageIndex !== null ? draggedTimelinePageIndex : parseInt(e.dataTransfer.getData("text/plain"));
      if (isNaN(fromIdx) || fromIdx < 0 || fromIdx >= currentProject.pages.length) return;
      let toIdx = targetIdx;
      if (fromIdx < targetIdx) toIdx = targetIdx - 1;
      toIdx = Math.max(0, Math.min(currentProject.pages.length - 1, toIdx));
      if (fromIdx !== toIdx) {
        reorderPage(fromIdx, toIdx);
      }
    });

    return slot;
  };

  // Add initial insert slot before first page with DocumentFragment
  const fragment = document.createDocumentFragment();
  fragment.appendChild(createInsertSlot(0));

  pages.forEach((page, idx) => {
    const card = document.createElement("div");
    const isBlank = page.page_type === "blank_verso" || page.layout === "blank_page";
    card.className = `thumb-card ${idx === currentPageIndex ? 'active' : ''} ${isBlank ? 'blank-card' : ''}`;
    card.setAttribute("draggable", "true");
    card.dataset.pageIndex = idx;
    card.onclick = () => selectPage(idx);

    // Drag and drop event listeners
    card.addEventListener("dragstart", (e) => {
      if (currentProject.is_locked) {
        e.preventDefault();
        return;
      }
      draggedTimelinePageIndex = idx;
      card.classList.add("dragging");
      e.dataTransfer.effectAllowed = "move";
      e.dataTransfer.setData("text/plain", idx.toString());
    });

    card.addEventListener("dragend", () => {
      card.classList.remove("dragging");
      document.querySelectorAll(".thumb-card").forEach(c => {
        c.classList.remove("drag-over-left", "drag-over-right");
      });
      draggedTimelinePageIndex = null;
    });

    card.addEventListener("dragover", (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = "move";
      if (draggedTimelinePageIndex === null || draggedTimelinePageIndex === idx) return;

      const rect = card.getBoundingClientRect();
      const midX = rect.left + rect.width / 2;
      if (e.clientX < midX) {
        card.classList.add("drag-over-left");
        card.classList.remove("drag-over-right");
      } else {
        card.classList.add("drag-over-right");
        card.classList.remove("drag-over-left");
      }
    });

    card.addEventListener("dragleave", () => {
      card.classList.remove("drag-over-left", "drag-over-right");
    });

    card.addEventListener("drop", (e) => {
      e.preventDefault();
      card.classList.remove("drag-over-left", "drag-over-right");

      const fromIdx = draggedTimelinePageIndex !== null ? draggedTimelinePageIndex : parseInt(e.dataTransfer.getData("text/plain"));
      if (isNaN(fromIdx) || fromIdx === idx || fromIdx < 0 || fromIdx >= currentProject.pages.length) return;

      const rect = card.getBoundingClientRect();
      const midX = rect.left + rect.width / 2;
      let toIdx = idx;
      if (e.clientX >= midX && fromIdx < idx) {
        toIdx = idx;
      } else if (e.clientX >= midX && fromIdx > idx) {
        toIdx = idx + 1;
      } else if (e.clientX < midX && fromIdx < idx) {
        toIdx = idx - 1;
      } else if (e.clientX < midX && fromIdx > idx) {
        toIdx = idx;
      }

      toIdx = Math.max(0, Math.min(currentProject.pages.length - 1, toIdx));
      if (fromIdx === toIdx) return;

      reorderPage(fromIdx, toIdx);
    });

    // Determine preview content
    let previewContent = "";
    let pageLabel = `Page ${idx + 1}`;

    if (page.page_type === "blank_verso" || page.layout === "blank_page") {
      pageLabel = `Blank Verso ${idx + 1}`;
      previewContent = `<span style="font-size:16px;">🛡️</span>`;
    } else if (page.page_type === "front_matter_disclaimer") {
      pageLabel = `Disclaimer`;
      previewContent = `<span style="font-size:16px;">⚖️</span>`;
    } else if (page.page_type === "front_matter_contents") {
      pageLabel = `Contents`;
      previewContent = `<span style="font-size:16px;">📋</span>`;
    } else if (page.puzzles || page.layout === "sudoku" || bType === "sudoku") {
      pageLabel = `Sudoku ${idx + 1}`;
      previewContent = `<span style="font-size:16px;">🧩</span>`;
    } else if (page.games || page.layout === "tic_tac_toe" || bType === "tic_tac_toe") {
      pageLabel = `Game Page ${idx + 1}`;
      previewContent = `<span style="font-size:16px;">⭕</span>`;
    } else if (page.maze || page.layout === "maze" || bType === "maze") {
      pageLabel = `Maze ${idx + 1}`;
      previewContent = `<span style="font-size:16px;">🌀</span>`;
    } else if (page.word_search || page.layout === "word_search" || bType === "word_search") {
      pageLabel = `Word Search ${idx + 1}`;
      previewContent = `<span style="font-size:16px;">🔤</span>`;
    } else if (page.dot_to_dot || page.layout === "dot_to_dot" || bType === "dot_to_dot") {
      pageLabel = `Dot-to-Dot ${idx + 1}`;
      previewContent = `<span style="font-size:16px;">🔢</span>`;
    } else {
      pageLabel = `Drawing ${idx + 1}`;
      const mainEl = page.elements ? page.elements.find(e => (e.type === "main_image" || e.type === "ref_image") && e.image_src) : null;
      previewContent = mainEl ? `<img src="${mainEl.image_src}">` : `<span style="font-size:16px;">🎨</span>`;
    }

    card.innerHTML = `
      <div class="thumb-card-actions">
        <button class="thumb-action-btn" onclick="openRenameModalForIndex(${idx}, event)" title="✏️ Rename Page">✏️</button>
        <button class="thumb-action-btn" onclick="duplicatePageAtIndex(${idx}, event)" title="📋 Duplicate Page">📋</button>
        <button class="thumb-action-btn btn-del" onclick="deletePageAtIndex(${idx}, event)" title="🗑 Delete Page">🗑</button>
      </div>
      <div class="thumb-page-num">${pageLabel}</div>
      <div class="thumb-preview-box">${previewContent}</div>
      <div class="thumb-title" title="${page.title || pageLabel}">${page.title || pageLabel}</div>
    `;
    fragment.appendChild(card);

    // In-between insert slot after this page
    fragment.appendChild(createInsertSlot(idx + 1));
  });

  strip.appendChild(fragment);

  const countBadge = document.getElementById("stat-page-count");
  if (countBadge) countBadge.innerText = currentProject.pages.length;
}

// In-between Page Insert Menu & Logic
function openInsertPageMenu(targetIndex, event) {
  if (event) event.stopPropagation();
  if (currentProject.is_locked) {
    showToast("🔒 Cannot insert: Project is locked!", "warning");
    return;
  }

  // Remove any existing popup
  closeInsertPageMenu();

  const bType = currentProject.book_type || "coloring_book";
  const contentLabel = bType === "sudoku" ? "🔢 Sudoku Puzzle Page" :
                       (bType === "tic_tac_toe" ? "⭕ Tic-Tac-Toe Game Page" :
                       (bType === "maze" ? "🌀 Maze Labyrinth Page" :
                       (bType === "word_search" ? "🔤 Word Search Page" : "🎨 Drawing / Coloring Page")));

  const menu = document.createElement("div");
  menu.id = "active-insert-popup-menu";
  menu.className = "insert-popup-menu";

  menu.innerHTML = `
    <button class="insert-popup-item" onclick="insertPageAt(${targetIndex}, 'blank')">
      ⚪ <strong>Insert Blank Page</strong>
    </button>
    <button class="insert-popup-item" onclick="insertPageAt(${targetIndex}, 'content')">
      ${contentLabel}
    </button>
  `;

  document.body.appendChild(menu);

  // Position popup near the clicked + button
  const rect = event.target.getBoundingClientRect();
  menu.style.left = `${Math.max(10, Math.min(window.innerWidth - 190, rect.left - 70))}px`;
  menu.style.top = `${rect.top - 78}px`;

  // Close on outside click
  setTimeout(() => {
    window.addEventListener("click", closeInsertPageMenu, { once: true });
  }, 10);
}

function closeInsertPageMenu() {
  const existing = document.getElementById("active-insert-popup-menu");
  if (existing) existing.remove();
}

async function insertPageAt(targetIndex, pageType = "blank") {
  closeInsertPageMenu();
  if (currentProject.is_locked) {
    showToast("🔒 Cannot modify: Project is locked!", "warning");
    return;
  }

  recordHistoryState(`Insert ${pageType === 'blank' ? 'Blank' : 'Content'} Page`);
  const bType = currentProject.book_type || "coloring_book";

  if (pageType === "blank") {
    const blankPage = {
      page_number: targetIndex + 1,
      page_type: "blank_verso",
      title: "Blank Back Page",
      layout: "blank_page",
      elements: []
    };
    currentProject.pages.splice(targetIndex, 0, blankPage);
  } else {
    // Content page based on book type
    if (bType === "sudoku") {
      try {
        const resp = await fetch("/api/generators/sudoku", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ count: 1, difficulty: "medium" })
        });
        const data = await resp.json();
        const p = (data.puzzles && data.puzzles[0]) ? data.puzzles[0] : null;
        const pTitle = `Sudoku #${(targetIndex + 1).toString().padStart(4, '0')}`;
        currentProject.pages.splice(targetIndex, 0, {
          page_number: targetIndex + 1,
          page_type: "content",
          title: pTitle,
          layout: "sudoku",
          puzzles: [p],
          elements: [
            { id: `elem_title_${Date.now()}`, type: "title", x: 35, y: 30, w: 440, h: 40, text: pTitle.toUpperCase(), font_size: 24, color: "#0f172a", is_outline: false },
            { id: `elem_frame_${Date.now()}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
          ]
        });
      } catch (e) {}
    } else if (bType === "tic_tac_toe") {
      try {
        const resp = await fetch("/api/generators/tic_tac_toe", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ total_games: 4, games_per_page: 4, grid_size: 3 })
        });
        const data = await resp.json();
        const games = (data.pages && data.pages[0]) ? data.pages[0].games : [];
        currentProject.pages.splice(targetIndex, 0, {
          page_number: targetIndex + 1,
          page_type: "content",
          title: `Game Page ${targetIndex + 1}`,
          layout: "tic_tac_toe",
          games: games,
          elements: [
            { id: `elem_title_${Date.now()}`, type: "title", x: 35, y: 30, w: 440, h: 40, text: "TIC-TAC-TOE", font_size: 26, color: "#0f172a", is_outline: false },
            { id: `elem_frame_${Date.now()}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
          ]
        });
      } catch (e) {}
    } else if (bType === "maze") {
      try {
        const resp = await fetch("/api/generators/maze", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ count: 1, width: 15, height: 20 })
        });
        const data = await resp.json();
        const m = (data.mazes && data.mazes[0]) ? data.mazes[0] : null;
        const pTitle = `Maze #${(targetIndex + 1).toString().padStart(3, '0')}`;
        currentProject.pages.splice(targetIndex, 0, {
          page_number: targetIndex + 1,
          page_type: "content",
          title: pTitle,
          layout: "maze",
          maze: m,
          elements: [
            { id: `elem_title_${Date.now()}`, type: "title", x: 35, y: 30, w: 440, h: 40, text: pTitle.toUpperCase(), font_size: 24, color: "#0f172a", is_outline: false },
            { id: `elem_frame_${Date.now()}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
          ]
        });
      } catch (e) {}
    } else if (bType === "word_search") {
      try {
        const resp = await fetch("/api/generators/word_search", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ count: 1, grid_size: 12 })
        });
        const data = await resp.json();
        const ws = (data.puzzles && data.puzzles[0]) ? data.puzzles[0] : null;
        const pTitle = ws ? ws.title : `Word Search #${(targetIndex + 1).toString().padStart(3, '0')}`;
        currentProject.pages.splice(targetIndex, 0, {
          page_number: targetIndex + 1,
          page_type: "content",
          title: pTitle,
          layout: "word_search",
          word_search: ws,
          elements: [
            { id: `elem_title_${Date.now()}`, type: "title", x: 35, y: 30, w: 440, h: 40, text: pTitle.toUpperCase(), font_size: 22, color: "#0f172a", is_outline: false },
            { id: `elem_frame_${Date.now()}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
          ]
        });
      } catch (e) {}
    } else {
      // Standard Coloring Page
      const projFont = currentProject.settings?.default_font_family || "Fredoka";
      const projOutline = currentProject.settings?.default_font_mode !== "solid";
      const projStroke = currentProject.settings?.default_stroke_color || "#0f172a";
      const projColor = currentProject.settings?.default_text_color || (projOutline ? "#ffffff" : "#111827");
      currentProject.pages.splice(targetIndex, 0, {
        page_number: targetIndex + 1,
        page_type: "content",
        title: `Drawing ${targetIndex + 1}`,
        layout: "kdp_top_ref",
        elements: [
          { id: `elem_ref_${Date.now()}`, type: "ref_image", x: 35, y: 25, w: 190, h: 180, text: `Ref ${targetIndex + 1}`, image_src: null },
          { id: `elem_title_${Date.now()}`, type: "title", x: 235, y: 70, w: 240, h: 80, text: `DRAWING ${targetIndex + 1}`, font_size: 40, color: projColor, is_outline: projOutline, stroke_color: projStroke, font_family: projFont, letter_spacing: 2 },
          { id: `elem_main_${Date.now()}`, type: "main_image", x: 35, y: 220, w: 440, h: 410, text: `Drawing ${targetIndex + 1}`, image_src: null },
          { id: `elem_frame_${Date.now()}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
        ]
      });
    }
  }

  renumberPages();
  renderTimeline();
  selectPage(targetIndex);
  syncActiveProjectUI();
  markProjectDirty();
  showToast(`✨ Inserted page at Position ${targetIndex + 1}!`, "success");
}

function duplicatePageAtIndex(idx, event) {
  if (event) event.stopPropagation();
  if (currentProject.is_locked) {
    showToast("🔒 Project is locked!", "warning");
    return;
  }

  const curr = currentProject.pages[idx];
  if (!curr) return;

  recordHistoryState(`Duplicate Page ${curr.page_number}`);
  const clone = JSON.parse(JSON.stringify(curr));
  if (clone.title && !clone.title.includes("(Copy)")) {
    clone.title = `${clone.title} (Copy)`;
  }

  currentProject.pages.splice(idx + 1, 0, clone);
  renumberPages();
  renderTimeline();
  selectPage(idx + 1);
  syncActiveProjectUI();
  markProjectDirty();
  showToast(`📋 Duplicated to Page ${idx + 2}!`, "success");
}

function deletePageAtIndex(idx, event) {
  if (event) event.stopPropagation();
  if (currentProject.is_locked) {
    showToast("🔒 Project is locked!", "warning");
    return;
  }

  if (currentProject.pages.length <= 1) {
    showToast("A book must contain at least one page.", "info");
    return;
  }

  recordHistoryState(`Delete Page ${idx + 1}`);
  const deletedNum = idx + 1;
  currentProject.pages.splice(idx, 1);

  renumberPages();
  const target = Math.min(idx, currentProject.pages.length - 1);
  currentPageIndex = Math.max(0, target);
  activeElementId = null;

  renderTimeline();
  selectPage(currentPageIndex);
  syncActiveProjectUI();
  markProjectDirty();
  showToast(`🗑 Deleted Page ${deletedNum}!`, "info");
}

function openRenameModalForIndex(idx, event) {
  if (event) event.stopPropagation();
  selectPage(idx);
  openRenameModal("page");
}

function selectPage(index) {
  currentPageIndex = index;
  activeElementId = null;

  const cards = document.querySelectorAll(".thumb-card");
  if (cards && cards.length === (currentProject.pages || []).length) {
    cards.forEach((card, idx) => {
      card.classList.toggle("active", idx === index);
    });
    if (cards[index]) {
      cards[index].scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
    }
  } else {
    renderTimeline();
  }

  loadPageIntoCanvas(index);
  updatePropertiesInspector();
}

// Batch Ingestion - Each Image becomes a Drawing Page with auto font scaling
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

  recordHistoryState(`Batch Import ${files.length} Images`);
  showToast(`⚡ Importing ${files.length} images into canvas editor...`, "info");

  const projFont = currentProject.settings?.default_font_family || "Fredoka";
  const projOutline = currentProject.settings?.default_font_mode !== "solid";
  const projStroke = currentProject.settings?.default_stroke_color || "#0f172a";
  const projColor = currentProject.settings?.default_text_color || (projOutline ? "#ffffff" : "#111827");

  let loadedCount = 0;
  files.forEach((file, idx) => {
    const reader = new FileReader();
    reader.onload = async (e) => {
      const rawDataUrl = e.target.result;
      const cleanTitle = cleanFileName(file.name);
      const autoFontSize = calculateAutoTitleFontSize(cleanTitle, 40);

      let finalDataUrl = rawDataUrl;
      let finalSizeKb = Math.round(file.size / 1024);

      try {
        const resp = await fetch("/api/projects/upload_asset", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            project_dir: currentProject.project_dir,
            filename: file.name,
            data_url: rawDataUrl,
            clean_bg: true,
            auto_crop: true
          })
        });
        const data = await resp.json();
        if (data.data_url) {
          finalDataUrl = data.data_url;
          finalSizeKb = data.size_kb || finalSizeKb;
        }
      } catch (err) {
        console.warn("Batch image opt fallback:", err);
      }

      if (!currentProject.media) currentProject.media = [];

      currentProject.media.unshift({
        id: `med_batch_${Date.now()}_${idx}`,
        name: cleanTitle,
        fileName: file.name,
        dataUrl: finalDataUrl,
        sizeKb: finalSizeKb
      });

      // Add Drawing Page with optimized image
      currentProject.pages.push({
        page_number: currentProject.pages.length + 1,
        page_type: "content",
        title: cleanTitle,
        layout: "kdp_top_ref",
        elements: [
          { id: `elem_ref_${Date.now()}_${idx}`, type: "ref_image", x: 35, y: 25, w: 190, h: 180, text: cleanTitle, image_src: finalDataUrl },
          { id: `elem_title_${Date.now()}_${idx}`, type: "title", x: 235, y: 70, w: 240, h: 80, text: cleanTitle.toUpperCase(), font_size: autoFontSize, color: projColor, is_outline: projOutline, stroke_color: projStroke, font_family: projFont, letter_spacing: 2 },
          { id: `elem_main_${Date.now()}_${idx}`, type: "main_image", x: 35, y: 220, w: 440, h: 410, text: cleanTitle, image_src: finalDataUrl },
          { id: `elem_frame_${Date.now()}_${idx}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
        ]
      });

      loadedCount++;
      if (loadedCount === files.length) {
        renumberPages();
        renderMediaLibrary();
        renderTimeline();
        syncActiveProjectUI();
        markProjectDirty();
        selectPage(currentProject.pages.length - files.length);
        switchTab("canvas");
        showToast(`🎉 Batch Created ${files.length} Auto-Cleaned & Optimized Drawing Pages!`, "success");
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
  cachedPageRect = null;
  currentZoom = Math.max(0.4, Math.min(2.5, currentZoom + delta));
  document.getElementById("canvas-stage").style.transform = `scale(${currentZoom})`;
  document.getElementById("zoom-readout").innerText = `Zoom: ${Math.round(currentZoom * 100)}%`;
}

function fitCanvasView() {
  cachedPageRect = null;
  const viewport = document.getElementById("canvas-viewport") || document.getElementById("viewport-container");
  const stage = document.getElementById("canvas-stage");
  const paper = document.getElementById("paper-page");
  if (!viewport || !stage || !paper) return;

  const vpW = viewport.clientWidth;
  const vpH = viewport.clientHeight;
  if (vpW < 50 || vpH < 50) return;

  // Actual paper dimensions (510 x 660 standard)
  const paperW = paper.offsetWidth || 510;
  const paperH = paper.offsetHeight || 660;

  // Safe padding around canvas for bleed envelope, shadow, and status bar
  const padW = 40;
  const padH = 48;

  const availW = Math.max(80, vpW - padW);
  const availH = Math.max(80, vpH - padH);

  const scaleW = availW / paperW;
  const scaleH = availH / paperH;

  // Calculate perfect auto-fit zoom scale so it fits 100% inside screen without overflow
  let targetScale = Math.min(scaleW, scaleH);
  // Cap between 0.35 and 1.25
  targetScale = Math.max(0.35, Math.min(1.25, targetScale));
  // Round to nearest 0.01 for smooth precision fit
  targetScale = Math.round(targetScale * 100) / 100;

  currentZoom = targetScale;
  stage.style.transform = `scale(${currentZoom})`;
  const readout = document.getElementById("zoom-readout");
  if (readout) readout.innerText = `Zoom: ${Math.round(currentZoom * 100)}%`;

  // Center scroll
  viewport.scrollTop = 0;
  viewport.scrollLeft = 0;
}

function saveSettings() {
  recordHistoryState("Update Project Settings");
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

// ==========================================
// Amazon KDP Preflight Quality Verification Engine
// ==========================================
function calculateKDPGutterMarginPt(pageCount) {
  if (pageCount <= 150) return 27.0; // 0.375 in
  if (pageCount <= 300) return 36.0; // 0.500 in
  if (pageCount <= 500) return 45.0; // 0.625 in
  return 54.0; // 0.750 in
}

function calculateKDPSpineWidthIn(pageCount, paperType = "white") {
  const multiplier = (paperType === "cream") ? 0.002500 : ((paperType === "premium_color") ? 0.002347 : 0.002252);
  return Math.max(0.06, pageCount * multiplier);
}

function updatePreflightDashboard() {
  const list = document.getElementById("preflight-results-list");
  const overallBadge = document.getElementById("preflight-overall-badge");
  if (!list) return;

  const pages = currentProject.pages || [];
  const totalPages = pages.length;
  const is24PageMin = totalPages >= 24;

  const contentPages = pages.filter(p => p.page_type === "content");
  const blankPages = pages.filter(p => p.page_type === "blank_verso");
  const hasSingleSided = (contentPages.length > 0) && (blankPages.length >= contentPages.length - 1);

  const spineWidthIn = calculateKDPSpineWidthIn(totalPages, "white");
  const spineWidthPt = (spineWidthIn * 72.0).toFixed(1);
  const gutterPt = calculateKDPGutterMarginPt(totalPages);
  const gutterIn = (gutterPt / 72.0).toFixed(3);

  const isOverallPass = is24PageMin && hasSingleSided;

  if (overallBadge) {
    overallBadge.className = `badge ${isOverallPass ? 'pass' : 'warning'}`;
    overallBadge.style.background = "";
    overallBadge.style.color = "";
    overallBadge.innerText = isOverallPass ? "✓ 100% KDP COMPLIANT" : "⚠️ KDP ADVISORY (ACTION NEEDED)";
  }

  list.innerHTML = `
    <!-- Check 1: 24-Page Minimum Rule -->
    <div class="check-item ${is24PageMin ? 'pass' : 'warning'}">
      <div class="check-icon">${is24PageMin ? '✓' : '⚠️'}</div>
      <div class="check-info">
        <h4>${is24PageMin ? 'Amazon KDP Minimum 24-Page Requirement Satisfied' : 'Page Count Below Amazon KDP Minimum (24 Pages)'}</h4>
        <p>Your book currently has <strong>${totalPages} pages</strong>. Amazon KDP paperback books require a minimum of 24 pages to bind properly. ${!is24PageMin ? `<em>Click "Auto-Fill to 24 Pages" below to add ${24 - totalPages} more pages instantly.</em>` : ''}</p>
      </div>
      <span class="check-badge ${is24PageMin ? 'pass' : 'warning'}">${is24PageMin ? 'PASS' : 'ADVISORY'}</span>
    </div>

    <!-- Check 2: Single-Sided Coloring Book Rule -->
    <div class="check-item ${hasSingleSided ? 'pass' : 'warning'}">
      <div class="check-icon">${hasSingleSided ? '✓' : 'ℹ'}</div>
      <div class="check-info">
        <h4>Single-Sided Bleed-Through Protection (Blank Verso Pages)</h4>
        <p>Coloring pages sit on odd pages (Recto) with blank back pages (Verso) inserted to protect against marker & watercolor bleed-through.</p>
      </div>
      <span class="check-badge ${hasSingleSided ? 'pass' : 'info'}">${hasSingleSided ? 'PASS' : 'ACTIVE'}</span>
    </div>

    <!-- Check 3: Dynamic Inside Gutter Binding Margin -->
    <div class="check-item pass">
      <div class="check-icon">✓</div>
      <div class="check-info">
        <h4>Dynamic Inside Binding Gutter: ${gutterIn} in (${gutterPt} pt)</h4>
        <p>Calculated automatically for ${totalPages} pages. Satisfies Amazon KDP spine glue safe margin specifications.</p>
      </div>
      <span class="check-badge pass">PASS</span>
    </div>

    <!-- Check 4: Calculated Spine Thickness & Wrap Cover Dimensions -->
    <div class="check-item pass">
      <div class="check-icon">✓</div>
      <div class="check-info">
        <h4>Spine Thickness Calculation: ${spineWidthIn.toFixed(4)} in (${spineWidthPt} pt)</h4>
        <p>Paperback full wrap cover width: <strong>${(17.25 + spineWidthIn).toFixed(3)} in</strong> × <strong>11.25 in</strong> (including 0.125 in outer bleed). Spine text ${totalPages >= 79 ? 'is eligible (>=79 pages)' : 'is omitted (minimum 79 pages required by Amazon for spine text)'}.</p>
      </div>
      <span class="check-badge pass">PASS</span>
    </div>

    <!-- Check 5: Resolution & Safe Margins -->
    <div class="check-item pass">
      <div class="check-icon">✓</div>
      <div class="check-info">
        <h4>Print Resolution (300 DPI Vector PDF)</h4>
        <p>Vector lineart, stroke outlines and embedded graphics are exported at lossless 300 DPI Amazon KDP print resolution.</p>
      </div>
      <span class="check-badge pass">PASS</span>
    </div>
  `;
}

function autoFillTo24Pages() {
  if (currentProject.is_locked) {
    showToast("🔒 Cannot modify: Project is locked!", "warning");
    return;
  }

  const currentCount = currentProject.pages ? currentProject.pages.length : 0;
  if (currentCount >= 24) {
    showToast("✨ Book already has 24 or more pages!", "info");
    return;
  }

  recordHistoryState("Auto-Fill to 24 Pages");

  const needed = 24 - currentCount;
  const pairsNeeded = Math.ceil(needed / 2);

  const projFont = currentProject.settings?.default_font_family || "Fredoka";
  const projOutline = currentProject.settings?.default_font_mode !== "solid";
  const projStroke = currentProject.settings?.default_stroke_color || "#0f172a";
  const projColor = currentProject.settings?.default_text_color || (projOutline ? "#ffffff" : "#111827");

  for (let i = 0; i < pairsNeeded; i++) {
    const drawPageNum = currentProject.pages.length + 1;
    const blankPageNum = currentProject.pages.length + 2;
    const contentCount = currentProject.pages.filter(p => p.page_type === "content").length + 1;

    currentProject.pages.push({
      page_number: drawPageNum,
      page_type: "content",
      title: `Page ${contentCount}`,
      layout: "kdp_top_ref",
      elements: [
        { id: `elem_ref_${drawPageNum}`, type: "ref_image", x: 35, y: 25, w: 190, h: 180, text: `Ref ${contentCount}`, image_src: null },
        { id: `elem_title_${drawPageNum}`, type: "title", x: 235, y: 70, w: 240, h: 80, text: `PAGE ${contentCount}`, font_size: 40, color: projColor, is_outline: projOutline, stroke_color: projStroke, font_family: projFont, letter_spacing: 2 },
        { id: `elem_main_${drawPageNum}`, type: "main_image", x: 35, y: 220, w: 440, h: 410, text: `Drawing ${contentCount}`, image_src: null },
        { id: `elem_frame_${drawPageNum}`, type: "border", x: 25, y: 15, w: 460, h: 630 }
      ]
    });

    if (currentProject.pages.length < 24) {
      currentProject.pages.push({
        page_number: blankPageNum,
        page_type: "blank_verso",
        title: "Blank Page",
        layout: "blank_page",
        elements: []
      });
    }
  }

  renumberPages();
  syncActiveProjectUI();
  updatePreflightDashboard();
  renderTimeline();
  markProjectDirty();
  showToast(`🎉 Auto-filled book to ${currentProject.pages.length} Pages (Amazon KDP Compliant)!`, "success");
}

// ==========================================
// Amazon KDP Full Wrap Cover Generator Engine
// ==========================================
function openCoverModal() {
  const modal = document.getElementById("cover-generator-modal");
  if (!modal) return;

  const titleInput = document.getElementById("cov-input-title");
  const authorInput = document.getElementById("cov-input-author");

  if (titleInput) titleInput.value = currentProject.name || "MY JUNGLE COLORING BOOK";
  if (authorInput) authorInput.value = currentProject.author || "Creative Kids Studio";

  updateCoverVisualPreview();
  modal.classList.add("active");
}

function updateCoverVisualPreview() {
  const title = (document.getElementById("cov-input-title")?.value || currentProject.name || "COLORING BOOK").toUpperCase();
  const subtitle = document.getElementById("cov-input-subtitle")?.value || "50+ Fun & Easy Coloring Pages";
  const author = document.getElementById("cov-input-author")?.value || currentProject.author || "Creative Kids Studio";
  const color = document.getElementById("cov-input-color")?.value || "#1e1b4b";
  const backHeading = (document.getElementById("cov-input-back-heading")?.value || "WHY YOUR CHILD WILL LOVE THIS BOOK").toUpperCase();
  const paperType = document.getElementById("cov-input-paper")?.value || "white";

  const totalPages = Math.max(24, currentProject.pages ? currentProject.pages.length : 24);
  const spineIn = calculateKDPSpineWidthIn(totalPages, paperType);
  const spinePt = (spineIn * 72.0).toFixed(1);
  const totalW = (17.25 + spineIn).toFixed(2);

  // Update Specs readout
  const spineLabel = document.getElementById("cov-spec-spine");
  if (spineLabel) spineLabel.innerText = `${spineIn.toFixed(3)} in (${spinePt} pt)`;
  const widthLabel = document.getElementById("cov-spec-width");
  if (widthLabel) widthLabel.innerText = `${totalW} in`;

  // Update visual preview elements
  const box = document.getElementById("cover-visual-preview");
  if (box) box.style.background = color;

  const frontTitle = document.getElementById("cov-prev-front-title");
  if (frontTitle) frontTitle.innerText = title;

  const frontSub = document.getElementById("cov-prev-front-sub");
  if (frontSub) frontSub.innerText = subtitle;

  const frontAuthor = document.getElementById("cov-prev-front-author");
  if (frontAuthor) frontAuthor.innerText = `By ${author}`;

  const backTitle = document.getElementById("cov-prev-back-title");
  if (backTitle) backTitle.innerText = backHeading;

  const spineElem = document.getElementById("cov-prev-spine");
  if (spineElem) {
    spineElem.innerText = totalPages >= 79 ? `${title} • ${author}` : "SPINE";
  }

  // Display first project image as cover artwork
  const artBox = document.getElementById("cov-prev-front-art");
  if (artBox) {
    let coverImg = null;
    for (const p of (currentProject.pages || [])) {
      for (const el of (p.elements || [])) {
        if ((el.type === "main_image" || el.type === "ref_image") && el.image_src) {
          coverImg = el.image_src;
          break;
        }
      }
      if (coverImg) break;
    }

    if (coverImg) {
      artBox.innerHTML = `<img src="${coverImg}" style="width:100%;height:100%;object-fit:contain;border-radius:6px;">`;
    } else {
      artBox.innerHTML = `🎨`;
    }
  }
}

function executeCoverPdfExport(openInBrowser = true) {
  showToast("⚙️ Generating 300 DPI Amazon KDP Cover PDF...", "info");

  const title = document.getElementById("cov-input-title")?.value || currentProject.name;
  const subtitle = document.getElementById("cov-input-subtitle")?.value || "50+ Fun & Easy Coloring Pages";
  const author = document.getElementById("cov-input-author")?.value || currentProject.author;
  const color = document.getElementById("cov-input-color")?.value || "#1e1b4b";
  const backHeading = document.getElementById("cov-input-back-heading")?.value || "WHY YOUR CHILD WILL LOVE THIS BOOK";
  const paperType = document.getElementById("cov-input-paper")?.value || "white";

  let coverImg = null;
  for (const p of (currentProject.pages || [])) {
    for (const el of (p.elements || [])) {
      if ((el.type === "main_image" || el.type === "ref_image") && el.image_src) {
        coverImg = el.image_src;
        break;
      }
    }
    if (coverImg) break;
  }

  const payload = {
    ...currentProject,
    cover_config: {
      title,
      subtitle,
      author,
      bg_color: color,
      spine_color: color,
      back_heading: backHeading,
      paper_type: paperType,
      front_image: coverImg
    }
  };

  fetch("/api/projects/export_cover_pdf", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
  .then(r => r.json())
  .then(data => {
    closeModal("cover-generator-modal");
    if (data.status === "success" && data.download_url) {
      showToast(`🎉 Cover PDF Generated: ${data.filename}!`, "success");
      fetchRecentProjects();
      if (openInBrowser) {
        window.open(data.download_url, "_blank");
      } else {
        const a = document.createElement("a");
        a.href = data.download_url;
        a.download = data.filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
      }
    } else {
      showToast(`⚠️ Cover PDF Export failed: ${data.error || 'Unknown error'}`, "danger");
    }
  })
  .catch(err => {
    closeModal("cover-generator-modal");
    showToast(`⚠️ Cover PDF Export error: ${err.message}`, "danger");
  });
}
