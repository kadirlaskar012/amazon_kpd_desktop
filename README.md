# KDP Book Production Studio

> A professional, offline-first Windows desktop studio built with **Python 3.12+** and **PySide6** to automate the rapid creation, editing, preflight validation, and PDF export of Amazon KDP children's coloring and activity books.

---

## Key Highlights

- **Local & Offline-First**: 100% offline desktop application with no mandatory accounts or cloud dependencies.
- **Physical Precision Engine**: Coordinates and margins stored internally in standard typographic points ($72\text{ pt/in} = 25.4\text{ mm}$), ensuring zero floating-point scaling drift during 300 DPI PDF generation.
- **KDP-Compliant Preflight**: Built-in support for official Amazon KDP trim sizes, bleed specifications, inside binding gutter calculations, and safe margin zones.
- **Extensible Modular Plugin System**: Pluggable `BookModule` architecture (Coloring Book in V1; Tracing, Activity, Puzzles, and Dot-to-Dot ready for subsequent releases).
- **Atomic Disk Persistence**: Crash-resilient saving with `.tmp` flushing, `.bak` rollover, and recent project management.

---

## Quickstart & Installation

### 1. Requirements
- Python 3.12+ (Tested on Python 3.14 on Windows 64-bit)
- Windows 10/11

### 2. Setup Virtual Environment
```powershell
# Create virtual environment
python -m venv .venv

# Activate environment
.\.venv\Scripts\Activate.ps1

# Install pinned dependencies
pip install -r requirements.txt
```

### 3. Launch Application
```powershell
.\.venv\Scripts\python.exe app\main.py
```

### 4. Run Test Suite
```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -v
```

---

## Application Structure

```
Amazon_KPD/
├── app/
│   ├── main.py                     # App entry point, High-DPI setup, Theme loader
│   ├── core/                       # Units engine, document & page data models
│   │   ├── units.py                # Unit conversion (in, mm, cm, pt, px)
│   │   ├── document_model.py       # DocumentModel, BookSettings, KDPProfile
│   │   ├── page_model.py           # PageModel, LayerModel, ElementModel
│   │   ├── asset_model.py          # AssetModel, AssetRegistry
│   │   ├── template_model.py       # TemplateModel, LayoutSlot
│   │   ├── project_manager.py      # Project lifecycle, New, Load, Save, Autosave
│   │   └── settings_manager.py     # Global app config (QSettings / JSON)
│   ├── modules/                    # Pluggable Book Modules
│   │   ├── base_module.py          # Abstract BookModule interface
│   │   ├── registry.py             # Module registry and discovery
│   │   └── coloring_book/          # Primary V1 Module
│   │       ├── module.py           # ColoringBookModule implementation
│   │       ├── templates.py        # Default coloring templates
│   │       └── generator.py        # Automatic filename-to-title page batch generator
│   ├── storage/                    # Disk persistence
│   │   └── project_storage.py      # Atomic JSON serialization & scaffolding
│   ├── ui/                         # PySide6 Desktop User Interface
│   │   ├── theme.py                # Dark/Light Modern Studio Theme & CSS tokens
│   │   ├── main_window.py          # Main Window, top navigation ribbon, status bar
│   │   ├── dashboard.py            # Dashboard view (Recent projects, Quick Start)
│   │   ├── project_setup.py        # New Project Wizard (Type, Title, Author, Path)
│   │   └── book_settings.py        # Book Settings inspector (Trim, Bleed, Margins, DPI)
│   └── resources/                  # App icons, fonts, presets
├── docs/
│   └── ARCHITECTURE.md             # Complete Technical Architecture Document
├── tests/                          # Automated Pytest Suite
│   ├── test_units.py
│   ├── test_document_model.py
│   ├── test_project_storage.py
│   ├── test_coloring_module.py
│   └── test_ui_smoke.py
├── requirements.txt
└── pyproject.toml
```

---

## Roadmap & Milestones

- [x] **Milestone 1: Technical Architecture & Core Application Shell**
  - Architecture specifications, Pydantic/Dataclass data models, units engine, atomic disk storage, dashboard, new project wizard, book settings panel, status bar, and automated test suite.
- [ ] **Milestone 2: Canvas Engine & Interactive Page Editor**
  - `QGraphicsView` & `QGraphicsScene` canvas, snap-to-guides (bleed, trim, safe, gutter), physical property inspector, layer controls, and bottom page timeline ribbon.
- [ ] **Milestone 3: Asset Manager & Image Ingestion**
  - Folder drop target, SHA-256 deduplication, EXIF/DPI inspection, and thumbnail cache.
- [ ] **Milestone 4: Coloring Book Engine & Bulk Page Generator**
  - Batch template applicator, OpenCV non-AI line-art extraction filter, and filename-to-title parser.
- [ ] **Milestone 5: Text System, Undo/Redo & Bulk Editing**
  - Rich text typography, local TTF font manager, `QUndoStack` commands, and multi-page batch updates.
- [ ] **Milestone 6: PDF Generation Engine & Spread Preview**
  - Multi-threaded 300 DPI PyMuPDF/ReportLab PDF compiler and realistic flipbook spread preview.
- [ ] **Milestone 7: KDP Preflight Quality Checker**
  - Automatic diagnostics for low-resolution images, bleed safety violations, inside gutter overflow, and blank pages.
- [ ] **Milestone 8: Cover Builder & Spine Calculator**
  - Full-wrap cover designer with dynamic spine thickness formula based on page count and paper type.
