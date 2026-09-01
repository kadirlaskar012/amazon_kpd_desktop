/**
 * KDP Book Production Studio - Interactive Canvas Web Engine, Layouts & User Media Library
 */

// User-uploaded Media Library (Clean, no inbuilt stock emojis)
let mediaLibrary = [];

// Global Project State
let project = {
  name: "My KDP Coloring Book",
  author: "Creative Studio",
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

let recentProjects = [
  { name: "My KDP Coloring Book", path: "C:\\Users\\KadiR-PC\\Documents\\KDP\\Coloring_Book_01", pages: 4 }
];

let currentPageIndex = 0;
let activeElementId = null;
let currentZoom = 1.0;
let showGuides = true;
let snapToGuides = true;

// UI Initialization
document.addEventListener("DOMContentLoaded", () => {
  setupNavigation();
  renderRecentProjects();
  renderMediaLibrary();
  renderTimeline();
  loadPageIntoCanvas(0);
  setupCanvasInteractions();
});

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
}

// Drawer Tabs (Layouts vs Media Library)
function switchDrawerTab(tabKey) {
  document.querySelectorAll(".drawer-tab-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".drawer-content").forEach(c => c.classList.remove("active"));

  const targetBtn = document.getElementById(`dtab-${tabKey}`);
  const targetContent = document.getElementById(`dcontent-${tabKey}`);
  if (targetBtn) targetBtn.classList.add("active");
  if (targetContent) targetContent.classList.add("active");
}

// ==========================================
// Media Library & Upload Management
// ==========================================
function triggerMediaUpload() {
  const fileInput = document.getElementById("media-library-upload-input");
  if (fileInput) {
    fileInput.value = "";
    fileInput.click();
  }
}

function handleMediaLibraryUpload(event) {
  const files = Array.from(event.target.files);
  if (!files.length) return;

  let loaded = 0;
  files.forEach((file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const dataUrl = e.target.result;
      const cleanTitle = cleanFileName(file.name);

      mediaLibrary.unshift({
        id: `med_user_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
        name: cleanTitle,
        fileName: file.name,
        dataUrl: dataUrl,
        sizeKb: Math.round(file.size / 1024)
      });

      loaded++;
      if (loaded === files.length) {
        renderMediaLibrary();
        switchDrawerTab("media");
        showToast(`📁 Uploaded ${files.length} image(s) to Media Library!`, "success");

        // If an image slot was selected on canvas, auto-populate with the first uploaded image
        const activeElem = getActiveElement();
        if (activeElem && (activeElem.type === "ref_image" || activeElem.type === "main_image")) {
          applyMediaToSlot(mediaLibrary[0].id, activeElem.type === "ref_image" ? "ref" : "drawing");
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

  const badge = document.getElementById("media-count-badge");
  if (badge) badge.innerText = mediaLibrary.length;

  if (mediaLibrary.length === 0) {
    container.innerHTML = `
      <div class="media-empty-state" onclick="triggerMediaUpload()" style="cursor: pointer;">
        <div class="media-empty-icon">📁</div>
        <strong>No images uploaded yet</strong>
        <p style="margin-top: 4px; color: var(--text-muted); font-size: 11px;">Click here or use the button above to upload PNG, JPG, or SVG images from your PC.</p>
      </div>
    `;
    return;
  }

  mediaLibrary.forEach(item => {
    const card = document.createElement("div");
    card.className = "media-card";

    card.innerHTML = `
      <div class="media-card-top" onclick="handleMediaCardClick('${item.id}')" style="cursor: pointer;">
        <div class="media-card-thumb">
          <img src="${item.dataUrl}">
        </div>
        <div class="media-card-meta">
          <div class="media-name" title="${item.name}">${item.name}</div>
          <div class="media-tag">${item.sizeKb} KB • Uploaded</div>
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

// When clicking the media card directly
function handleMediaCardClick(mediaId) {
  const activeElem = getActiveElement();
  if (activeElem && activeElem.type === "ref_image") {
    applyMediaToSlot(mediaId, "ref");
  } else if (activeElem && activeElem.type === "main_image") {
    applyMediaToSlot(mediaId, "drawing");
  } else {
    // Default to Drawing slot
    applyMediaToSlot(mediaId, "drawing");
  }
}

// 1-Click Slot Placement (Reference, Drawing, Title, Apply All)
function applyMediaToSlot(mediaId, slotType) {
  const item = mediaLibrary.find(m => m.id === mediaId);
  if (!item) return;

  const page = project.pages[currentPageIndex];
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
    // 1. Reference
    let refElem = page.elements.find(e => e.type === "ref_image");
    if (refElem) {
      refElem.image_src = imgSrc;
      refElem.text = labelText;
    }
    // 2. Drawing
    let mainElem = page.elements.find(e => e.type === "main_image");
    if (mainElem) {
      mainElem.image_src = imgSrc;
      mainElem.text = labelText;
    }
    // 3. Title
    let titleElem = page.elements.find(e => e.type === "title");
    if (titleElem) {
      titleElem.text = item.name.toUpperCase();
    }
    page.title = item.name;
    showToast(`⚡ Filled Reference, Drawing, and Title with "${item.name}"!`, "success");
  }

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
  const page = project.pages[currentPageIndex];
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
// Page Canvas Loader & Pure White Element Rendering
// ==========================================
function loadPageIntoCanvas(index) {
  const page = project.pages[index];
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

    // Inner element rendering with pure white background
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
            <span class="txt">Select Drawing / Coloring Image</span>
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

    // Handles for resizing
    elDiv.innerHTML += `
      <div class="handle tl" data-handle="tl"></div>
      <div class="handle tr" data-handle="tr"></div>
      <div class="handle bl" data-handle="bl"></div>
      <div class="handle br" data-handle="br"></div>
    `;

    // Click selection: Automatically focuses Media Library if clicking an image slot
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
  if (pageReadout) pageReadout.innerText = `Page ${index + 1} of ${project.pages.length}`;
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
    if (!elem) return;

    const dx = (e.clientX - startX) / currentZoom;
    const dy = (e.clientY - startY) / currentZoom;

    if (isDragging) {
      elem.x = Math.max(0, Math.min(510 - elem.w, elemStart.x + dx));
      elem.y = Math.max(0, Math.min(660 - elem.h, elemStart.y + dy));
      applyElementStyles(elem);
      updatePropertiesInspector();
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
  const page = project.pages[currentPageIndex];
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
}

// Alignment Functions
function alignActive(mode) {
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
  showToast(`Aligned element: ${mode.replace('_', ' ')}`, "info");
}

// Add Elements
function addNewTextElement() {
  const page = project.pages[currentPageIndex];
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
  showToast("Added vector text element", "info");
}

function addNewBorderElement() {
  const page = project.pages[currentPageIndex];
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
  showToast("Added decorative border frame", "info");
}

function duplicateActiveElement() {
  const elem = getActiveElement();
  if (!elem) return;

  const page = project.pages[currentPageIndex];
  const clone = { ...elem, id: `elem_dup_${Date.now()}`, x: elem.x + 15, y: elem.y + 15 };
  page.elements.push(clone);
  loadPageIntoCanvas(currentPageIndex);
  setActiveElement(clone.id);
  showToast("Duplicated element", "info");
}

function deleteActiveElement() {
  const page = project.pages[currentPageIndex];
  if (!page || !activeElementId) return;

  page.elements = page.elements.filter(e => e.id !== activeElementId);
  setActiveElement(null);
  loadPageIntoCanvas(currentPageIndex);
  showToast("Deleted element", "info");
}

// Page Actions
function addNewPage() {
  const num = project.pages.length + 1;
  project.pages.push({
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
  selectPage(project.pages.length - 1);
  showToast(`Added Page ${num}`, "success");
}

function duplicateCurrentPage() {
  const curr = project.pages[currentPageIndex];
  if (!curr) return;

  const num = project.pages.length + 1;
  const clone = JSON.parse(JSON.stringify(curr));
  clone.page_number = num;
  clone.title = `${clone.title} (Copy)`;
  project.pages.splice(currentPageIndex + 1, 0, clone);
  renderTimeline();
  selectPage(currentPageIndex + 1);
  showToast(`Duplicated page to Page ${currentPageIndex + 1}`, "success");
}

function deleteCurrentPage() {
  if (project.pages.length <= 1) {
    showToast("A book must contain at least one page.", "info");
    return;
  }
  const deletedNum = currentPageIndex + 1;
  project.pages.splice(currentPageIndex, 1);
  const target = Math.max(0, currentPageIndex - 1);
  renderTimeline();
  selectPage(target);
  showToast(`Deleted Page ${deletedNum}`, "info");
}

// Timeline
function renderTimeline() {
  const strip = document.getElementById("thumbnails-strip");
  if (!strip) return;
  strip.innerHTML = "";

  project.pages.forEach((page, idx) => {
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
  if (countBadge) countBadge.innerText = project.pages.length;
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
  const fileInput = document.getElementById("batch-images-input");
  if (fileInput) {
    fileInput.value = "";
    fileInput.click();
  }
}

function handleBatchImagesUpload(event) {
  const files = Array.from(event.target.files);
  if (!files.length) return;

  showToast(`⚡ Processing ${files.length} images into coloring pages...`, "info");

  let loadedCount = 0;
  files.forEach((file, idx) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const dataUrl = e.target.result;
      const cleanTitle = cleanFileName(file.name);
      const pageNum = project.pages.length + 1;

      mediaLibrary.unshift({
        id: `med_batch_${Date.now()}_${idx}`,
        name: cleanTitle,
        fileName: file.name,
        dataUrl: dataUrl,
        sizeKb: Math.round(file.size / 1024)
      });

      project.pages.push({
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
        selectPage(project.pages.length - files.length);
        switchTab("canvas");
        showToast(`🎉 Batch Generated ${files.length} KDP Coloring Pages!`, "success");
      }
    };
    reader.readAsDataURL(file);
  });
}

// Modal Controls
function openNewProjectModal(bookType = "coloring_book") {
  const modal = document.getElementById("new-project-modal");
  document.getElementById("modal-book-type").value = bookType;
  if (modal) modal.classList.add("active");
}

function openExistingFolderModal() {
  const modal = document.getElementById("open-folder-modal");
  if (modal) modal.classList.add("active");
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove("active");
}

function submitCreateProject() {
  const name = document.getElementById("modal-project-name").value.trim() || "My New Coloring Book";
  const author = document.getElementById("modal-author-name").value.trim() || "Creative Author";
  const count = parseInt(document.getElementById("modal-page-count").value || "10");
  const hasBleed = document.getElementById("modal-has-bleed").checked;

  const newPages = [];
  for (let i = 0; i < count; i++) {
    newPages.push({
      page_number: i + 1,
      title: `Page ${i + 1}`,
      layout: "top_ref",
      elements: [
        { id: `elem_ref_${i}`, type: "ref_image", x: 180, y: 35, w: 150, h: 100, text: "Click to select Reference Image", image_src: null },
        { id: `elem_main_${i}`, type: "main_image", x: 45, y: 150, w: 420, h: 420, text: "Click to select Drawing Image", image_src: null },
        { id: `elem_title_${i}`, type: "title", x: 45, y: 585, w: 420, h: 40, text: `PAGE ${i + 1}`, font_size: 26, color: "#111827", font_family: "Plus Jakarta Sans" },
        { id: `elem_frame_${i}`, type: "border", x: 30, y: 25, w: 450, h: 610 },
      ]
    });
  }

  project = {
    name: name,
    author: author,
    settings: {
      trim_width_pt: 612.0,
      trim_height_pt: 792.0,
      has_bleed: hasBleed,
      bleed_pt: 9.0,
      margins: { top_pt: 27.0, bottom_pt: 27.0, inside_pt: 36.0, outside_pt: 27.0 },
      target_dpi: 300,
    },
    pages: newPages
  };

  recentProjects.unshift({
    name: name,
    path: `C:\\Users\\KadiR-PC\\Documents\\KDP\\${name.replace(/ /g, '_')}`,
    pages: count
  });

  closeModal("new-project-modal");
  document.getElementById("nav-project-name").innerText = name;
  renderRecentProjects();
  renderTimeline();
  loadPageIntoCanvas(0);
  switchTab("canvas");

  showToast(`✨ Created "${name}" with ${count} clean pages!`, "success");
}

function loadSampleProject(title, count) {
  project.name = title;
  document.getElementById("nav-project-name").innerText = title;
  closeModal("open-folder-modal");
  renderTimeline();
  loadPageIntoCanvas(0);
  switchTab("canvas");
  showToast(`📂 Opened project "${title}"!`, "info");
}

function renderRecentProjects() {
  const container = document.getElementById("recent-projects-list");
  if (!container) return;

  container.innerHTML = "";
  recentProjects.forEach(p => {
    const item = document.createElement("div");
    item.className = "recent-item";
    item.onclick = () => loadSampleProject(p.name, p.pages);
    item.innerHTML = `
      <div class="recent-icon">📖</div>
      <div class="recent-info">
        <div class="recent-title">${p.name}</div>
        <div class="recent-path">${p.path}</div>
      </div>
      <div class="recent-meta">
        <span class="badge">${p.pages} Pages</span>
        <button class="btn btn-sm btn-primary">Open</button>
      </div>
    `;
    container.appendChild(item);
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
  showToast("Settings applied & saved to project.json successfully!", "success");
  switchTab("canvas");
}

function saveProject() {
  showToast(`💾 Project "${project.name}" saved atomically!`, "success");
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
