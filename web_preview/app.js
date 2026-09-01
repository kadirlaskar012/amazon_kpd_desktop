/**
 * KDP Book Production Studio - Complete Application Engine with Undo/Redo History, Automatic Front Matter, Pre-flight PDF Export Preview & Amazon KDP Single-Sided Blank Page Rules
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
    contents_style: "numbered",  // numbered, bullet, plain
    show_page_numbers: true,
    publisher_name: "KDP Creative Publishing",
    isbn: "978-X-XXXXX-XXX-X"
  },
  media: [],
  pages: [
    {
      page_number: 1,
      page_type: "front_matter_disclaimer",
      title: "Disclaimer & Copyright",
      layout: "disclaimer_standard",
      elements: [
        { id: "elem_disc_frame", type: "border", x: 35, y: 30, w: 440, h: 600 },
        { id: "elem_disc_title", type: "title", x: 45, y: 65, w: 420, h: 40, text: "MY JUNGLE COLORING BOOK", font_size: 24, color: "#0f172a" },
        { id: "elem_disc_sub", type: "title", x: 45, y: 110, w: 420, h: 25, text: "First Edition • Premium KDP Edition", font_size: 13, color: "#475569" },
        { id: "elem_disc_copy", type: "title", x: 45, y: 180, w: 420, h: 25, text: "Copyright © 2026 by Creative Kids Studio", font_size: 14, color: "#1e293b" },
        { id: "elem_disc_rights", type: "title", x: 45, y: 210, w: 420, h: 20, text: "All rights reserved.", font_size: 12, color: "#475569" },
        { id: "elem_disc_p1", type: "title", x: 45, y: 260, w: 420, h: 20, text: "No part of this publication may be reproduced, distributed, or transmitted in any form", font_size: 10, color: "#64748b" },
        { id: "elem_disc_p2", type: "title", x: 45, y: 285, w: 420, h: 20, text: "or by any means, including photocopying, recording, or other electronic methods,", font_size: 10, color: "#64748b" },
        { id: "elem_disc_p3", type: "title", x: 45, y: 310, w: 420, h: 20, text: "without the prior written permission of the author and publisher.", font_size: 10, color: "#64748b" },
        { id: "elem_disc_pub", type: "title", x: 45, y: 400, w: 420, h: 20, text: "Published by: KDP Creative Publishing", font_size: 11, color: "#334155" },
        { id: "elem_disc_isbn", type: "title", x: 45, y: 430, w: 420, h: 20, text: "ISBN-13: 978-X-XXXXX-XXX-X", font_size: 11, color: "#334155" },
        { id: "elem_disc_contact", type: "title", x: 45, y: 480, w: 420, h: 20, text: "Visit us: www.kdpbooks.com • support@kdpbooks.com", font_size: 10, color: "#64748b" },
        { id: "elem_disc_kdp", type: "title", x: 45, y: 550, w: 420, h: 20, text: "Printed for Amazon KDP Distribution • First Printing", font_size: 9, color: "#94a3b8" }
      ]
    },
    {
      page_number: 2,
      page_type: "front_matter_contents",
      title: "Table of Contents",
      layout: "contents_standard",
      elements: [
        { id: "elem_cnt_frame", type: "border", x: 35, y: 30, w: 440, h: 600 },
        { id: "elem_cnt_head", type: "title", x: 45, y: 55, w: 420, h: 35, text: "TABLE OF CONTENTS", font_size: 22, color: "#0f172a" },
        { id: "elem_cnt_sub", type: "title", x: 45, y: 90, w: 420, h: 20, text: "Explore all the illustrations and coloring pages in this book", font_size: 11, color: "#64748b" },
        { id: "elem_cnt_item_1", type: "title", x: 65, y: 140, w: 380, h: 24, text: "1. Playful Lion ........................ Page 3", font_size: 12, color: "#1e293b" },
        { id: "elem_cnt_item_2", type: "title", x: 65, y: 168, w: 380, h: 24, text: "2. Gentle Elephant .................... Page 4", font_size: 12, color: "#1e293b" }
      ]
    },
    {
      page_number: 3,
      page_type: "content",
      title: "Playful Lion",
      layout: "top_ref",
      elements: [
        { id: "elem_ref_1", type: "ref_image", x: 180, y: 35, w: 150, h: 100, text: "Playful Lion Reference", image_src: null },
        { id: "elem_main_1", type: "main_image", x: 45, y: 150, w: 420, h: 420, text: "Playful Lion Drawing", image_src: null },
        { id: "elem_title_1", type: "title", x: 45, y: 585, w: 420, h: 40, text: "PLAYFUL LION", font_size: 26, color: "#111827", font_family: "Plus Jakarta Sans" },
        { id: "elem_frame_1", type: "border", x: 30, y: 25, w: 450, h: 610 },
      ]
    },
    {
      page_number: 4,
      page_type: "content",
      title: "Gentle Elephant",
      layout: "top_ref",
      elements: [
        { id: "elem_ref_2", type: "ref_image", x: 180, y: 35, w: 150, h: 100, text: "Gentle Elephant Reference", image_src: null },
        { id: "elem_main_2", type: "main_image", x: 45, y: 150, w: 420, h: 420, text: "Gentle Elephant Drawing", image_src: null },
        { id: "elem_title_2", type: "title", x: 45, y: 585, w: 420, h: 40, text: "GENTLE ELEPHANT", font_size: 26, color: "#111827", font_family: "Plus Jakarta Sans" },
        { id: "elem_frame_2", type: "border", x: 30, y: 25, w: 450, h: 610 },
      ]
    }
  ]
};

let recentProjectsList = [];
let currentPageIndex = 0;
let currentSpreadIndex = 0;
let activeElementId = null;
let currentZoom = 1.0;
let showGuides = true;
let snapToGuides = true;

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

// UI Initialization
document.addEventListener("DOMContentLoaded", () => {
  setupNavigation();
  setupGlobalKeyboardShortcuts();
  fetchDefaultLocation();
  loadInitialProject();
  fetchRecentProjects();
  setupCanvasInteractions();
  updateUndoRedoButtons();

  // Background Auto-Save Cron (Every 10 seconds)
  setInterval(() => {
    if (isDirty) {
      saveProject(false);
    }
  }, 10000);
});

// ==========================================
// Undo / Redo History Stack Implementation
// ==========================================
function recordHistoryState(actionName = "Edit") {
  if (isHistoryAction) return;

  try {
    const snapshot = {
      project: JSON.parse(JSON.stringify(currentProject)),
      pageIndex: currentPageIndex,
      activeElementId: activeElementId,
      action: actionName
    };

    undoStack.push(snapshot);
    if (undoStack.length > MAX_HISTORY) {
      undoStack.shift();
    }

    // Reset Redo stack whenever a new user action is performed
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
      project: JSON.parse(JSON.stringify(currentProject)),
      pageIndex: currentPageIndex,
      activeElementId: activeElementId,
      action: "Current State"
    };
    redoStack.push(currentState);

    const previousState = undoStack.pop();
    currentProject = previousState.project;
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
      project: JSON.parse(JSON.stringify(currentProject)),
      pageIndex: currentPageIndex,
      activeElementId: activeElementId,
      action: "Current State"
    };
    undoStack.push(currentState);

    const nextState = redoStack.pop();
    currentProject = nextState.project;
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

function cleanFileName(filename) {
  let name = filename.replace(/\.[^/.]+$/, "");
  name = name.replace(/^(page\s*[\-_]*)?\d+[\s_\.\-]+/i, "");
  name = name.replace(/[\-_](coloring[\-_]?page|lineart|drawing|illustration|vector|bw|art)$/i, "");
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
    } else {
      page.page_type = "content";
      if (!page.title || /^Page\s*\d+$/i.test(page.title.trim())) {
        page.title = `Page ${contentPageCounter}`;
      }
      if (page.elements && Array.isArray(page.elements)) {
        page.elements.forEach(elem => {
          if (elem.type === "title") {
            const txt = (elem.text || "").trim();
            if (/^PAGE\s*\d+$/i.test(txt) || txt === "PAGE" || txt === "") {
              elem.text = `PAGE ${contentPageCounter}`;
            }
          }
        });
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

  const contentPages = currentProject.pages.filter(p => p.page_type !== "front_matter_disclaimer" && p.page_type !== "front_matter_contents");
  
  const elements = [
    { id: "elem_cnt_frame", type: "border", x: 35, y: 30, w: 440, h: 600 },
    { id: "elem_cnt_head", type: "title", x: 45, y: 55, w: 420, h: 35, text: cfg.contents_heading || "TABLE OF CONTENTS", font_size: 22, color: "#0f172a" },
    { id: "elem_cnt_sub", type: "title", x: 45, y: 90, w: 420, h: 20, text: "Explore all the illustrations and coloring pages in this book", font_size: 11, color: "#64748b" }
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
        color: "#1e293b"
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
        color: "#1e293b"
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
        color: "#1e293b"
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
      { id: "elem_disc_frame", type: "border", x: 35, y: 30, w: 440, h: 600 },
      { id: "elem_disc_title", type: "title", x: 45, y: 65, w: 420, h: 40, text: projName.toUpperCase(), font_size: 24, color: "#0f172a" },
      { id: "elem_disc_sub", type: "title", x: 45, y: 110, w: 420, h: 25, text: "First Edition • Premium KDP Edition", font_size: 13, color: "#475569" },
      { id: "elem_disc_copy", type: "title", x: 45, y: 180, w: 420, h: 25, text: `Copyright © ${year} by ${authorName}`, font_size: 14, color: "#1e293b" },
      { id: "elem_disc_rights", type: "title", x: 45, y: 210, w: 420, h: 20, text: "All rights reserved.", font_size: 12, color: "#475569" },
      { id: "elem_disc_p1", type: "title", x: 45, y: 260, w: 420, h: 20, text: "No part of this publication may be reproduced, distributed, or transmitted in any form", font_size: 10, color: "#64748b" },
      { id: "elem_disc_p2", type: "title", x: 45, y: 285, w: 420, h: 20, text: "or by any means, including photocopying, recording, or other electronic methods,", font_size: 10, color: "#64748b" },
      { id: "elem_disc_p3", type: "title", x: 45, y: 310, w: 420, h: 20, text: "without the prior written permission of the author and publisher.", font_size: 10, color: "#64748b" },
      { id: "elem_disc_pub", type: "title", x: 45, y: 400, w: 420, h: 20, text: "Published by: KDP Creative Publishing", font_size: 11, color: "#334155" },
      { id: "elem_disc_isbn", type: "title", x: 45, y: 430, w: 420, h: 20, text: "ISBN-13: 978-X-XXXXX-XXX-X", font_size: 11, color: "#334155" },
      { id: "elem_disc_contact", type: "title", x: 45, y: 480, w: 420, h: 20, text: "Visit us: www.kdpbooks.com • support@kdpbooks.com", font_size: 10, color: "#64748b" },
      { id: "elem_disc_kdp", type: "title", x: 45, y: 550, w: 420, h: 20, text: "Printed for Amazon KDP Distribution • First Printing", font_size: 9, color: "#94a3b8" }
    ]
  };

  const contentsPage = {
    page_number: 2,
    page_type: "front_matter_contents",
    title: "Table of Contents",
    layout: "contents_standard",
    elements: [
      { id: "elem_cnt_frame", type: "border", x: 35, y: 30, w: 440, h: 600 },
      { id: "elem_cnt_head", type: "title", x: 45, y: 55, w: 420, h: 35, text: "TABLE OF CONTENTS", font_size: 22, color: "#0f172a" },
      { id: "elem_cnt_sub", type: "title", x: 45, y: 90, w: 420, h: 20, text: "Explore all the illustrations and coloring pages in this book", font_size: 11, color: "#64748b" }
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
// Robust Initial Project Loader & Tab Memory
// ==========================================
function loadInitialProject() {
  try {
    const cachedData = localStorage.getItem("kdp_active_project_data") || localStorage.getItem("kdp_autosave_current_project");
    if (cachedData) {
      const parsed = JSON.parse(cachedData);
      if (parsed && parsed.name && parsed.pages && parsed.pages.length > 0) {
        currentProject = parsed;
      }
    }
  } catch (e) {
    console.warn("Local cache read error:", e);
  }

  renumberPages();
  syncActiveProjectUI();
  loadPageIntoCanvas(currentPageIndex);
  renderTimeline();

  const savedTab = localStorage.getItem("kdp_active_tab") || "canvas";
  switchTab(savedTab);

  const activePath = localStorage.getItem("kdp_active_project_path") || currentProject.project_dir;
  if (activePath) {
    fetch(`/api/projects/load?path=${encodeURIComponent(activePath)}`)
      .then(r => r.json())
      .then(data => {
        if (data.project && data.project.pages && data.project.pages.length > 0) {
          currentProject = data.project;
          renumberPages();
          syncActiveProjectUI();
          loadPageIntoCanvas(currentPageIndex);
          renderTimeline();
          renderMediaLibrary();
          if (savedTab === "preview") renderSpreadPreview();
        }
      })
      .catch(() => {});
  }
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

function openExportPdfModal() {
  const modal = document.getElementById("export-pdf-modal");
  if (!modal) return;

  // Sync Specs Info
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

  updateExportModalPreview();
  modal.classList.add("active");
}

function updateExportModalPreview() {
  const container = document.getElementById("export-pages-grid");
  const totalLabel = document.getElementById("exp-spec-pages");
  const countLabel = document.getElementById("exp-grid-count");
  if (!container) return;

  const singleSided = document.getElementById("exp-opt-single-sided") ? document.getElementById("exp-opt-single-sided").checked : true;
  const blankNote = document.getElementById("exp-opt-blank-note") ? document.getElementById("exp-opt-blank-note").checked : false;

  const pages = currentProject.pages || [];
  let html = "";
  let totalOutputPages = 0;

  pages.forEach((p, idx) => {
    totalOutputPages++;
    const isDisclaimer = p.page_type === "front_matter_disclaimer";
    const isContents = p.page_type === "front_matter_contents";
    const isContent = !isDisclaimer && !isContents;

    const mainEl = p.elements.find(e => (e.type === "main_image" || e.type === "ref_image") && e.image_src);
    const thumbImg = mainEl 
      ? `<img src="${mainEl.image_src}">` 
      : `<span style="font-size:24px;">${isDisclaimer ? '📜' : (isContents ? '📋' : '🎨')}</span>`;

    html += `
      <div class="export-page-card">
        <div class="export-page-badge recto">Page ${totalOutputPages} • ${isDisclaimer ? 'Disclaimer' : (isContents ? 'Contents' : 'Drawing')}</div>
        <div class="export-page-thumb">${thumbImg}</div>
        <div class="export-page-title">${p.title || `Page ${p.page_number}`}</div>
      </div>
    `;

    // Amazon KDP Single-Sided Blank Back Page Insertion
    if (singleSided) {
      if (isContent) {
        totalOutputPages++;
        html += `
          <div class="export-page-card blank-verso">
            <div class="export-page-badge verso">Page ${totalOutputPages} • Blank Back</div>
            <div class="export-page-thumb" style="background:#f8fafc;">
              <span style="font-size:10px;color:#94a3b8;text-align:center;padding:6px;">
                ${blankNote ? '🛡️ Bleed-Safe Blank' : '⚪ Blank White Page'}
              </span>
            </div>
            <div class="export-page-title" style="color:#94a3b8;">Blank Verso</div>
          </div>
        `;
      } else if (isDisclaimer || isContents) {
        const isLastFrontMatter = (idx + 1 < pages.length && pages[idx + 1].page_type === "content");
        if (isLastFrontMatter) {
          totalOutputPages++;
          html += `
            <div class="export-page-card blank-verso">
              <div class="export-page-badge verso">Page ${totalOutputPages} • Blank Back</div>
              <div class="export-page-thumb" style="background:#f8fafc;">
                <span style="font-size:10px;color:#94a3b8;text-align:center;padding:6px;">⚪ Blank Verso</span>
              </div>
              <div class="export-page-title" style="color:#94a3b8;">Blank Verso</div>
            </div>
          `;
        }
      }
    }
  });

  container.innerHTML = html;
  if (totalLabel) totalLabel.innerText = `${totalOutputPages} Total PDF Pages`;
  if (countLabel) countLabel.innerText = `${totalOutputPages} Pages`;
}

function executePdfExport(openInBrowser = true) {
  const singleSided = document.getElementById("exp-opt-single-sided") ? document.getElementById("exp-opt-single-sided").checked : true;
  const blankNote = document.getElementById("exp-opt-blank-note") ? document.getElementById("exp-opt-blank-note").checked : false;

  showToast("⚙️ Generating 300 DPI Amazon KDP PDF...", "info");

  const payload = {
    ...currentProject,
    single_sided: singleSided,
    blank_page_note: blankNote
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
      showToast(`⚠️ PDF Export failed: ${data.error || 'Unknown error'}`, "danger");
    }
  })
  .catch(err => {
    closeModal("export-pdf-modal");
    showToast(`⚠️ PDF Export error: ${err.message}`, "danger");
  });
}

// ==========================================
// Spread Preview (Realistic 2-Page Book View)
// ==========================================
function renderSpreadPreview() {
  const container = document.getElementById("spread-book-container");
  const indicator = document.getElementById("spread-page-indicator");
  if (!container) return;

  const totalPages = currentProject.pages ? currentProject.pages.length : 0;
  if (totalPages === 0) {
    container.innerHTML = `<div style="padding:40px;color:#94a3b8;">No pages available in this project.</div>`;
    return;
  }

  const leftIdx = currentSpreadIndex * 2;
  const rightIdx = leftIdx + 1;

  const leftPage = currentProject.pages[leftIdx];
  const rightPage = rightIdx < totalPages ? currentProject.pages[rightIdx] : null;

  if (indicator) {
    indicator.innerText = rightPage 
      ? `Spread: Pages ${leftPage.page_number} - ${rightPage.page_number} (of ${totalPages})`
      : `Spread: Page ${leftPage.page_number} (Final Page)`;
  }

  const renderPageHtml = (page, isLeft) => {
    if (!page) {
      return `
        <div class="spread-page ${isLeft ? 'left-page' : 'right-page'}" style="background:#f8fafc;display:flex;align-items:center;justify-content:center;">
          <div style="color:#94a3b8;font-size:12px;font-style:italic;">[ End of Book / Blank Page ]</div>
        </div>
      `;
    }

    const titleEl = page.elements.find(e => e.type === "title");
    const mainEl = page.elements.find(e => (e.type === "main_image" || e.type === "ref_image") && e.image_src);
    const refEl = page.elements.find(e => e.type === "ref_image" && e.image_src);

    const titleText = titleEl ? titleEl.text : (page.title || `PAGE ${page.page_number}`);
    const imgContent = mainEl 
      ? `<div class="spread-img-box"><img src="${mainEl.image_src}"></div>`
      : `<div class="spread-img-placeholder"><span>🎨</span><span>Drawing Area</span></div>`;

    return `
      <div class="spread-page ${isLeft ? 'left-page' : 'right-page'}">
        <div class="spread-page-header">Page ${page.page_number} • ${page.page_type === 'front_matter_disclaimer' ? 'Disclaimer' : (page.page_type === 'front_matter_contents' ? 'Contents' : 'Interior')}</div>
        <div class="spread-inner-content">
          ${refEl ? `<div style="font-size:10px;color:#64748b;font-weight:700;">Ref: ${refEl.text || 'Reference'}</div>` : ''}
          ${imgContent}
          <div class="spread-title-text">${titleText}</div>
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
  const totalPages = currentProject.pages ? currentProject.pages.length : 0;
  const maxSpread = Math.floor((totalPages - 1) / 2);
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
    fetchRecentProjects();

    if (currentProject.project_dir === targetPath) {
      localStorage.removeItem("kdp_active_project_path");
      localStorage.removeItem("kdp_active_project_data");
      currentProject = {
        name: "New Book Project",
        folder_name: "New_Book_Project",
        project_dir: `${defaultRootLocation}\\New_Book_Project`,
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
      undoStack = [];
      redoStack = [];
      updateUndoRedoButtons();
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
function setupNavigation() {
  document.querySelectorAll(".nav-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const tab = btn.getAttribute("data-tab");
      switchTab(tab);
    });
  });
}

function switchTab(tabId) {
  localStorage.setItem("kdp_active_tab", tabId);

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

  if (tabId === "canvas") {
    loadPageIntoCanvas(currentPageIndex);
    renderTimeline();
    renderMediaLibrary();
  } else if (tabId === "preview") {
    renderSpreadPreview();
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
  const isLocked = Boolean(currentProject.is_locked);
  const lockIcon = isLocked ? "🔒" : "🔓";
  const lockText = isLocked ? "LOCKED" : "UNLOCKED";
  const lockBtnText = isLocked ? "🔓 Unlock Project" : "🔒 Lock Project";

  const navProjName = document.getElementById("nav-project-name");
  if (navProjName) {
    navProjName.innerText = `${lockIcon} ${currentProject.name}`;
  }

  document.getElementById("active-proj-title").innerText = currentProject.name;
  document.getElementById("active-proj-path").innerText = `📁 ${currentProject.project_dir}`;
  document.getElementById("active-proj-meta").innerHTML = `
    <span>Pages: ${currentProject.pages.length}</span> • 
    <span>Author: ${currentProject.author || 'Creative Author'}</span> • 
    <span>Trim: 8.5x11 in</span>
  `;

  const lockBadge = document.getElementById("active-proj-lock-badge");
  if (lockBadge) {
    lockBadge.className = `badge ${isLocked ? 'locked' : 'unlocked'}`;
    lockBadge.innerText = `${lockIcon} ${lockText}`;
  }

  const lockBtn = document.getElementById("active-lock-toggle-btn");
  if (lockBtn) {
    lockBtn.innerText = lockBtnText;
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

  document.getElementById("stat-page-count").innerText = currentProject.pages.length;
  document.getElementById("stat-media-count").innerText = currentProject.media ? currentProject.media.length : 0;
  
  const folderHint = document.getElementById("media-folder-hint");
  if (folderHint) folderHint.innerText = `${currentProject.folder_name}/assets`;

  renderTimeline();
  renderMediaLibrary();
  updateUndoRedoButtons();
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
  const autoFrontMatter = document.getElementById("modal-auto-front-matter") ? document.getElementById("modal-auto-front-matter").checked : true;

  const projName = (nameInput ? nameInput.value.trim() : "") || "My New KDP Book";
  const rootDir = (rootInput ? rootInput.value.trim() : "") || defaultRootLocation;
  const folderName = projName.replace(/[^a-zA-Z0-9_\-\s]/g, "").replace(/\s+/g, "_");
  const projectDir = `${rootDir.replace(/[\/\\]+$/, "")}\\${folderName}`;
  const count = parseInt(countSelect ? countSelect.value : "10");

  const pagesList = [];

  if (autoFrontMatter) {
    pagesList.push({
      page_number: 1,
      page_type: "front_matter_disclaimer",
      title: "Disclaimer & Copyright",
      layout: "disclaimer_standard",
      elements: [
        { id: "elem_disc_frame", type: "border", x: 35, y: 30, w: 440, h: 600 },
        { id: "elem_disc_title", type: "title", x: 45, y: 65, w: 420, h: 40, text: projName.toUpperCase(), font_size: 24, color: "#0f172a" },
        { id: "elem_disc_sub", type: "title", x: 45, y: 110, w: 420, h: 25, text: "First Edition • Premium KDP Edition", font_size: 13, color: "#475569" },
        { id: "elem_disc_copy", type: "title", x: 45, y: 180, w: 420, h: 25, text: `Copyright © ${new Date().getFullYear()} by Creative Kids Studio`, font_size: 14, color: "#1e293b" },
        { id: "elem_disc_rights", type: "title", x: 45, y: 210, w: 420, h: 20, text: "All rights reserved.", font_size: 12, color: "#475569" },
        { id: "elem_disc_p1", type: "title", x: 45, y: 260, w: 420, h: 20, text: "No part of this publication may be reproduced, distributed, or transmitted in any form", font_size: 10, color: "#64748b" },
        { id: "elem_disc_p2", type: "title", x: 45, y: 285, w: 420, h: 20, text: "or by any means, including photocopying, recording, or other electronic methods,", font_size: 10, color: "#64748b" },
        { id: "elem_disc_p3", type: "title", x: 45, y: 310, w: 420, h: 20, text: "without the prior written permission of the author and publisher.", font_size: 10, color: "#64748b" },
        { id: "elem_disc_pub", type: "title", x: 45, y: 400, w: 420, h: 20, text: "Published by: KDP Creative Publishing", font_size: 11, color: "#334155" },
        { id: "elem_disc_isbn", type: "title", x: 45, y: 430, w: 420, h: 20, text: "ISBN-13: 978-X-XXXXX-XXX-X", font_size: 11, color: "#334155" },
        { id: "elem_disc_contact", type: "title", x: 45, y: 480, w: 420, h: 20, text: "Visit us: www.kdpbooks.com • support@kdpbooks.com", font_size: 10, color: "#64748b" },
        { id: "elem_disc_kdp", type: "title", x: 45, y: 550, w: 420, h: 20, text: "Printed for Amazon KDP Distribution • First Printing", font_size: 9, color: "#94a3b8" }
      ]
    });

    pagesList.push({
      page_number: 2,
      page_type: "front_matter_contents",
      title: "Table of Contents",
      layout: "contents_standard",
      elements: [
        { id: "elem_cnt_frame", type: "border", x: 35, y: 30, w: 440, h: 600 },
        { id: "elem_cnt_head", type: "title", x: 45, y: 55, w: 420, h: 35, text: "TABLE OF CONTENTS", font_size: 22, color: "#0f172a" },
        { id: "elem_cnt_sub", type: "title", x: 45, y: 90, w: 420, h: 20, text: "Explore all the illustrations and coloring pages in this book", font_size: 11, color: "#64748b" }
      ]
    });
  }

  const startNum = pagesList.length + 1;
  for (let i = 0; i < count; i++) {
    const docPageNum = startNum + i;
    const contentNum = i + 1;
    pagesList.push({
      page_number: docPageNum,
      page_type: "content",
      title: `Page ${contentNum}`,
      layout: "top_ref",
      elements: [
        { id: `elem_ref_${docPageNum}`, type: "ref_image", x: 180, y: 35, w: 150, h: 100, text: "Click to select Reference Image", image_src: null },
        { id: `elem_main_${docPageNum}`, type: "main_image", x: 45, y: 150, w: 420, h: 420, text: "Click to select Drawing Image", image_src: null },
        { id: `elem_title_${docPageNum}`, type: "title", x: 45, y: 585, w: 420, h: 40, text: `PAGE ${contentNum}`, font_size: 26, color: "#111827", font_family: "Plus Jakarta Sans" },
        { id: `elem_frame_${docPageNum}`, type: "border", x: 30, y: 25, w: 450, h: 610 },
      ]
    });
  }

  const newProjPayload = {
    name: projName,
    folder_name: folderName,
    project_dir: projectDir,
    root_path: rootDir,
    author: "Creative Kids Studio",
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
  undoStack = [];
  redoStack = [];

  renumberPages();
  localStorage.setItem("kdp_active_project_path", currentProject.project_dir);
  localStorage.setItem("kdp_active_project_data", JSON.stringify(currentProject));

  closeModal("new-project-modal");
  syncActiveProjectUI();
  fetchRecentProjects();
  switchTab("canvas");

  showToast(`✨ Created Project with Front Matter (Disclaimer + Contents)!`, "success");
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
      currentPageIndex = 0;
      activeElementId = null;
      undoStack = [];
      redoStack = [];

      renumberPages();
      localStorage.setItem("kdp_active_project_path", currentProject.project_dir);
      localStorage.setItem("kdp_active_project_data", JSON.stringify(currentProject));

      closeModal("open-folder-modal");
      syncActiveProjectUI();
      loadPageIntoCanvas(currentPageIndex);
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

  recordHistoryState("Upload Media");

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

  recordHistoryState(`Apply Media (${slotType})`);

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
    grid_4: "2x2 Quadrant Grid",
    disclaimer_standard: "Disclaimer & Copyright",
    contents_standard: "Table of Contents"
  };
  return map[key] || key;
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
      if (elem.alignment === "center") {
        elDiv.style.textAlign = "center";
      } else if (elem.alignment === "left") {
        elDiv.style.textAlign = "left";
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
  if (pageReadout) {
    const pageTypeTag = page.page_type === "front_matter_disclaimer" 
      ? " (Disclaimer)" 
      : (page.page_type === "front_matter_contents" ? " (Contents)" : "");
    pageReadout.innerText = `Page ${index + 1} of ${currentProject.pages.length}${pageTypeTag}`;
  }
}

// Drag & Resize Canvas Interactions with Undo History
function setupCanvasInteractions() {
  let isDragging = false;
  let isResizing = false;
  let activeHandle = null;
  let startX = 0, startY = 0;
  let elemStart = { x: 0, y: 0, w: 0, h: 0 };
  let hasMoved = false;

  const stage = document.getElementById("canvas-stage");
  if (!stage) return;

  stage.addEventListener("mousedown", (e) => {
    if (currentProject.is_locked) return;

    if (e.target.classList.contains("handle")) {
      isResizing = true;
      activeHandle = e.target.getAttribute("data-handle");
      startX = e.clientX;
      startY = e.clientY;
      const elem = getActiveElement();
      if (elem) elemStart = { ...elem };
      hasMoved = false;
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
      hasMoved = false;
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
      if (!hasMoved && (Math.abs(dx) > 2 || Math.abs(dy) > 2)) {
        recordHistoryState("Move Element");
        hasMoved = true;
      }
      elem.x = Math.max(0, Math.min(510 - elem.w, elemStart.x + dx));
      elem.y = Math.max(0, Math.min(660 - elem.h, elemStart.y + dy));
      applyElementStyles(elem);
      updatePropertiesInspector();
      markProjectDirty();
    } else if (isResizing) {
      if (!hasMoved && (Math.abs(dx) > 2 || Math.abs(dy) > 2)) {
        recordHistoryState("Resize Element");
        hasMoved = true;
      }
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
    hasMoved = false;
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

  recordHistoryState("Edit Properties");

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

  recordHistoryState("Add Text Element");

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

  recordHistoryState("Add Border Frame");

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

  recordHistoryState("Duplicate Element");

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

// Page Actions
function addNewPage() {
  if (currentProject.is_locked) {
    showToast("🔒 Project is locked!", "warning");
    return;
  }

  recordHistoryState("Add New Page");

  const num = currentProject.pages.length + 1;
  currentProject.pages.push({
    page_number: num,
    page_type: "content",
    title: `Page ${num}`,
    layout: "top_ref",
    elements: [
      { id: `elem_ref_${Date.now()}`, type: "ref_image", x: 180, y: 35, w: 150, h: 100, text: "Click to select Reference Image", image_src: null },
      { id: `elem_main_${Date.now()}`, type: "main_image", x: 45, y: 150, w: 420, h: 420, text: "Click to select Drawing Image", image_src: null },
      { id: `elem_title_${Date.now()}`, type: "title", x: 45, y: 585, w: 420, h: 40, text: `PAGE ${num}`, font_size: 26, color: "#111827" },
      { id: `elem_frame_${Date.now()}`, type: "border", x: 30, y: 25, w: 450, h: 610 }
    ]
  });

  renumberPages();
  renderTimeline();
  selectPage(currentProject.pages.length - 1);
  syncActiveProjectUI();
  markProjectDirty();
  showToast(`Added Page ${currentProject.pages.length}`, "success");
}

function duplicateCurrentPage() {
  if (currentProject.is_locked) return;

  const curr = currentProject.pages[currentPageIndex];
  if (!curr) return;

  recordHistoryState(`Duplicate Page ${curr.page_number}`);

  const num = currentProject.pages.length + 1;
  const clone = JSON.parse(JSON.stringify(curr));
  clone.page_number = num;
  clone.title = `${clone.title} (Copy)`;
  currentProject.pages.splice(currentPageIndex + 1, 0, clone);

  renumberPages();
  renderTimeline();
  selectPage(currentPageIndex + 1);
  syncActiveProjectUI();
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

// Timeline
function renderTimeline() {
  const strip = document.getElementById("thumbnails-strip");
  if (!strip) return;
  strip.innerHTML = "";

  currentProject.pages.forEach((page, idx) => {
    const card = document.createElement("div");
    card.className = `thumb-card ${idx === currentPageIndex ? 'active' : ''}`;
    card.onclick = () => selectPage(idx);

    let typeBadge = "";
    if (page.page_type === "front_matter_disclaimer") {
      typeBadge = `<div style="font-size:9px;color:var(--warning);font-weight:700;">[Disclaimer]</div>`;
    } else if (page.page_type === "front_matter_contents") {
      typeBadge = `<div style="font-size:9px;color:var(--secondary);font-weight:700;">[Contents]</div>`;
    }

    const mainEl = page.elements.find(e => (e.type === "main_image" || e.type === "ref_image") && e.image_src);
    const previewContent = mainEl 
      ? `<img src="${mainEl.image_src}">` 
      : `<span style="font-size:16px;">${page.page_type === 'front_matter_disclaimer' ? '📜' : (page.page_type === 'front_matter_contents' ? '📋' : '📄')}</span>`;

    card.innerHTML = `
      <div class="thumb-page-num">Page ${page.page_number} ${typeBadge}</div>
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

  recordHistoryState(`Batch Import ${files.length} Images`);
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
        page_type: "content",
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
        renumberPages();
        renderMediaLibrary();
        renderTimeline();
        syncActiveProjectUI();
        markProjectDirty();
        selectPage(currentProject.pages.length - files.length);
        switchTab("canvas");
        showToast(`🎉 Batch Generated ${files.length} KDP Pages & Synced Table of Contents!`, "success");
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
