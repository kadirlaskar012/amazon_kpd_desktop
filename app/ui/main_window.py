"""
MainWindow: The core application frame, top workflow navigation ribbon,
stacked view router, menubar, and live status bar.
"""

from pathlib import Path
from typing import Optional, Dict

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QMenuBar,
    QMenu,
    QFileDialog,
    QMessageBox,
    QFrame,
    QButtonGroup,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QKeySequence, QFont, QIcon

from app.core.document_model import ProjectDocument, BookType
from app.core.project_manager import ProjectManager
from app.core.settings_manager import SettingsManager
from app.core.units import format_dimension
from app.ui.theme import Theme
from app.ui.dashboard import DashboardView
from app.ui.book_settings import BookSettingsPanel
from app.ui.project_setup import ProjectSetupDialog
from app.ui.canvas.canvas_editor_view import CanvasEditorView


class StepPlaceholderWidget(QWidget):
    """Clean placeholder for upcoming pipeline milestones."""

    def __init__(self, step_number: int, step_name: str, description: str, next_milestone: str, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)

        card = QFrame()
        card.setMaximumWidth(580)
        card.setStyleSheet(
            f"background-color: {Theme.BG_CARD}; border: 1px solid {Theme.BORDER}; "
            f"border-radius: 12px; padding: 32px;"
        )
        c_layout = QVBoxLayout(card)
        c_layout.setAlignment(Qt.AlignCenter)
        c_layout.setSpacing(12)

        badge = QLabel(f"WORKFLOW STEP {step_number}")
        badge.setStyleSheet(
            f"background-color: {Theme.PRIMARY}; color: #ffffff; font-weight: bold; "
            f"font-size: 11px; padding: 4px 10px; border-radius: 4px;"
        )
        c_layout.addWidget(badge, 0, Qt.AlignCenter)

        title = QLabel(step_name)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #ffffff;")
        c_layout.addWidget(title, 0, Qt.AlignCenter)

        desc = QLabel(description)
        desc.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 13px;")
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        c_layout.addWidget(desc)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet(f"background-color: {Theme.BORDER}; max-height: 1px;")
        c_layout.addWidget(divider)

        milestone_lbl = QLabel(f"Scheduled for Implementation: {next_milestone}")
        milestone_lbl.setStyleSheet(f"color: {Theme.ACCENT}; font-weight: 600; font-size: 12px;")
        c_layout.addWidget(milestone_lbl, 0, Qt.AlignCenter)

        layout.addWidget(card)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KDP Book Production Studio")
        self.resize(1280, 840)
        self.setMinimumSize(960, 640)

        self.project_manager = ProjectManager.get_instance()
        self.settings_manager = SettingsManager.get_instance()

        self._init_ui()
        self._init_menu()
        self._update_status_bar()

        # Connect project manager signals
        self.project_manager.register_project_changed_listener(self._on_project_changed)
        self.project_manager.register_saved_listener(lambda path: self._update_status_bar())
        self.project_manager.register_dirty_listener(lambda dirty: self._update_status_bar())

    def _init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top Workflow Navigation Ribbon
        self.ribbon_frame = QFrame()
        self.ribbon_frame.setStyleSheet(
            f"background-color: {Theme.BG_SURFACE}; border-bottom: 1px solid {Theme.BORDER};"
        )
        ribbon_layout = QHBoxLayout(self.ribbon_frame)
        ribbon_layout.setContentsMargins(16, 6, 16, 6)
        ribbon_layout.setSpacing(6)

        # App Brand / Title
        brand_lbl = QLabel("📖 KDP Studio")
        brand_lbl.setFont(QFont("Segoe UI", 13, QFont.Bold))
        brand_lbl.setStyleSheet(f"color: {Theme.PRIMARY}; margin-right: 12px;")
        ribbon_layout.addWidget(brand_lbl)

        # Step Buttons
        self.step_btn_group = QButtonGroup(self)
        self.step_btn_group.setExclusive(True)

        self.steps_data = [
            ("1. Dashboard", "Home Hub & Projects"),
            ("2. Book Settings", "Trim, Margins, Bleed & DPI"),
            ("3. Templates", "Layout Slot Presets"),
            ("4. Assets", "Image Ingestion & Gallery"),
            ("5. Canvas Editor", "Interactive Page Designer"),
            ("6. Quality Check", "KDP Rule Preflight Engine"),
            ("7. Cover Builder", "Spine & Wrap Calculator"),
            ("8. Preview", "Multi-Page Spread Flipbook"),
            ("9. Export PDF", "300 DPI Print-Ready Export"),
        ]

        self.step_buttons = []
        for idx, (step_title, tooltip) in enumerate(self.steps_data):
            btn = QPushButton(step_title)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {Theme.TEXT_SECONDARY};
                    border: none;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-size: 12px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: {Theme.BG_CARD};
                    color: {Theme.TEXT_PRIMARY};
                }}
                QPushButton:checked {{
                    background-color: {Theme.PRIMARY};
                    color: #ffffff;
                    font-weight: bold;
                }}
                QPushButton:disabled {{
                    color: {Theme.TEXT_DISABLED};
                }}
            """)
            btn.clicked.connect(lambda checked=False, i=idx: self._switch_step(i))
            self.step_btn_group.addButton(btn, idx)
            self.step_buttons.append(btn)
            ribbon_layout.addWidget(btn)

        ribbon_layout.addStretch(1)

        # Quick Save Button on Ribbon
        self.quick_save_btn = QPushButton("💾 Save")
        self.quick_save_btn.setStyleSheet("padding: 5px 12px; font-size: 12px;")
        self.quick_save_btn.clicked.connect(self._save_project)
        self.quick_save_btn.setEnabled(False)
        ribbon_layout.addWidget(self.quick_save_btn)

        main_layout.addWidget(self.ribbon_frame)

        # 2. Central Stacked Views
        self.stack = QStackedWidget()

        # Step 0: Dashboard
        self.dashboard_view = DashboardView(self)
        self.dashboard_view.project_opened.connect(self._on_project_opened_from_dashboard)
        self.stack.addWidget(self.dashboard_view)

        # Step 1: Book Settings
        self.book_settings_view = BookSettingsPanel(self)
        self.stack.addWidget(self.book_settings_view)

        # Step 2: Templates Placeholder
        self.stack.addWidget(
            StepPlaceholderWidget(
                3,
                "Template System",
                "Select and customize standard multi-slot layouts for reference thumbnails, main coloring outlines, titles, and borders.",
                "Milestone 4 (Template & Bulk Engine)",
            )
        )

        # Step 3: Assets Placeholder
        self.stack.addWidget(
            StepPlaceholderWidget(
                4,
                "Asset Manager",
                "Batch import reference images, manage line-art conversions, preview DPI resolutions, and track assignment status.",
                "Milestone 3 (Asset Management & Pipeline)",
            )
        )

        # Step 4: Canvas Editor
        self.canvas_editor_view = CanvasEditorView(self)
        self.stack.addWidget(self.canvas_editor_view)

        # Step 5: Quality Check Placeholder
        self.stack.addWidget(
            StepPlaceholderWidget(
                6,
                "KDP Quality & Preflight Checker",
                "Automated validation against official KDP print guidelines: DPI, bleed boundary, safe margins, blank pages, and font availability.",
                "Milestone 7 (Quality Engine)",
            )
        )

        # Step 6: Cover Builder Placeholder
        self.stack.addWidget(
            StepPlaceholderWidget(
                7,
                "Cover & Spine Builder",
                "Dynamic spine width calculator based on page count and paper type, front/back wrap layout, and barcode reservation zone.",
                "Milestone 8 (Cover Builder)",
            )
        )

        # Step 7: Preview Placeholder
        self.stack.addWidget(
            StepPlaceholderWidget(
                8,
                "Realistic Spread Preview",
                "Single-page, two-page spread, and thumbnail grid proofing modes with physical page boundary rendering.",
                "Milestone 6 (PDF Rendering & Proofing)",
            )
        )

        # Step 8: Export PDF Placeholder
        self.stack.addWidget(
            StepPlaceholderWidget(
                9,
                "PDF Generation & Export",
                "Multi-threaded, high-speed 300 DPI KDP-compliant interior and cover PDF compilation with validation gating.",
                "Milestone 6 (PDF Exporter)",
            )
        )

        main_layout.addWidget(self.stack, 1)

        # 3. Status Bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Custom Status Widgets
        self.status_project_lbl = QLabel("No Project Open")
        self.status_project_lbl.setStyleSheet(f"font-weight: 600; color: {Theme.TEXT_PRIMARY};")

        self.status_pages_lbl = QLabel("0 Pages")
        self.status_pages_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")

        self.status_trim_lbl = QLabel("Trim: -")
        self.status_trim_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")

        self.status_bleed_lbl = QLabel("Bleed: -")
        self.status_bleed_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")

        self.status_dpi_lbl = QLabel("300 DPI")
        self.status_dpi_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")

        self.status_save_lbl = QLabel("● Ready")
        self.status_save_lbl.setStyleSheet(f"color: {Theme.SECONDARY}; font-weight: bold;")

        self.status_bar.addWidget(self.status_project_lbl)
        self.status_bar.addWidget(QLabel(" | "))
        self.status_bar.addWidget(self.status_pages_lbl)
        self.status_bar.addWidget(QLabel(" | "))
        self.status_bar.addWidget(self.status_trim_lbl)
        self.status_bar.addWidget(QLabel(" | "))
        self.status_bar.addWidget(self.status_bleed_lbl)
        self.status_bar.addWidget(QLabel(" | "))
        self.status_bar.addWidget(self.status_dpi_lbl)
        self.status_bar.addPermanentWidget(self.status_save_lbl)

        # Select initial dashboard button
        self.step_buttons[0].setChecked(True)
        self._update_step_button_states()

    def _init_menu(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("&File")

        new_act = QAction("✨ &New Project...", self)
        new_act.setShortcut(QKeySequence.New)
        new_act.triggered.connect(self._new_project_dialog)
        file_menu.addAction(new_act)

        open_act = QAction("&Open Project...", self)
        open_act.setShortcut(QKeySequence.Open)
        open_act.triggered.connect(self._open_project_dialog)
        file_menu.addAction(open_act)

        file_menu.addSeparator()

        self.save_act = QAction("&Save Project", self)
        self.save_act.setShortcut(QKeySequence.Save)
        self.save_act.triggered.connect(self._save_project)
        self.save_act.setEnabled(False)
        file_menu.addAction(self.save_act)

        self.close_act = QAction("&Close Project", self)
        self.close_act.triggered.connect(self._close_project)
        self.close_act.setEnabled(False)
        file_menu.addAction(self.close_act)

        file_menu.addSeparator()

        exit_act = QAction("E&xit", self)
        exit_act.setShortcut("Alt+F4")
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)

        # Book Menu
        book_menu = menubar.addMenu("&Book")
        settings_act = QAction("Book &Settings...", self)
        settings_act.triggered.connect(lambda: self._switch_step(1))
        book_menu.addAction(settings_act)

        # View Menu
        view_menu = menubar.addMenu("&View")
        dash_act = QAction("&Dashboard", self)
        dash_act.triggered.connect(lambda: self._switch_step(0))
        view_menu.addAction(dash_act)

        # Help Menu
        help_menu = menubar.addMenu("&Help")
        about_act = QAction("&About KDP Book Production Studio", self)
        about_act.triggered.connect(self._show_about)
        help_menu.addAction(about_act)

    def _switch_step(self, step_index: int):
        if 0 <= step_index < self.stack.count():
            self.stack.setCurrentIndex(step_index)
            if step_index < len(self.step_buttons):
                self.step_buttons[step_index].setChecked(True)

    def _update_step_button_states(self):
        has_doc = self.project_manager.current_document is not None
        # All steps except Dashboard require an active project
        for i in range(1, len(self.step_buttons)):
            self.step_buttons[i].setEnabled(has_doc)

        self.quick_save_btn.setEnabled(has_doc)
        if hasattr(self, "save_act"):
            self.save_act.setEnabled(has_doc)
        if hasattr(self, "close_act"):
            self.close_act.setEnabled(has_doc)

    def _on_project_changed(self, doc: Optional[ProjectDocument]):
        self._update_step_button_states()
        self._update_status_bar()

    def _on_project_opened_from_dashboard(self, doc: ProjectDocument):
        self._update_step_button_states()
        self._update_status_bar()
        # Automatically navigate to Book Settings or Canvas
        self._switch_step(1)

    def _update_status_bar(self):
        doc = self.project_manager.current_document
        if not doc:
            self.status_project_lbl.setText("No Project Open")
            self.status_pages_lbl.setText("0 Pages")
            self.status_trim_lbl.setText("Trim: -")
            self.status_bleed_lbl.setText("Bleed: -")
            self.status_dpi_lbl.setText("300 DPI")
            self.status_save_lbl.setText("● Ready")
            self.status_save_lbl.setStyleSheet(f"color: {Theme.TEXT_MUTED};")
            return

        st = doc.settings
        unit = st.units
        dpi = st.target_dpi

        w_str = format_dimension(st.trim_width_pt, unit, dpi)
        h_str = format_dimension(st.trim_height_pt, unit, dpi)

        self.status_project_lbl.setText(f"📁 {doc.name} ({doc.module_type.replace('_', ' ').title()})")
        self.status_pages_lbl.setText(f"{len(doc.pages)} Pages")
        self.status_trim_lbl.setText(f"Trim: {w_str} × {h_str}")
        self.status_bleed_lbl.setText("Bleed: ON" if st.has_bleed else "Bleed: OFF")
        self.status_dpi_lbl.setText(f"{dpi} DPI")

        if self.project_manager.is_dirty:
            self.status_save_lbl.setText("● Unsaved Changes")
            self.status_save_lbl.setStyleSheet(f"color: {Theme.ACCENT}; font-weight: bold;")
        else:
            self.status_save_lbl.setText("✓ Saved")
            self.status_save_lbl.setStyleSheet(f"color: {Theme.SECONDARY}; font-weight: bold;")

    def _new_project_dialog(self):
        dlg = ProjectSetupDialog(self)
        if dlg.exec():
            doc = self.project_manager.current_document
            if doc:
                self._switch_step(1)

    def _open_project_dialog(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select KDP Project Directory",
            str(self.settings_manager.default_project_dir),
        )
        if folder:
            try:
                doc = self.project_manager.open_project(Path(folder))
                self._switch_step(1)
            except Exception as ex:
                QMessageBox.critical(
                    self,
                    "Error Opening Project",
                    f"Could not load KDP project from {folder}:\n\n{str(ex)}",
                )

    def _save_project(self):
        try:
            saved_path = self.project_manager.save_current_project()
            if saved_path:
                self._update_status_bar()
        except Exception as ex:
            QMessageBox.critical(
                self,
                "Save Error",
                f"Failed to save project:\n\n{str(ex)}",
            )

    def _close_project(self):
        self.project_manager.close_current_project()
        self._switch_step(0)

    def _show_about(self):
        QMessageBox.about(
            self,
            "About KDP Book Production Studio",
            "<h3>KDP Book Production Studio v1.0</h3>"
            "<p>A professional, offline-first Windows desktop studio for rapid creation of Amazon KDP children's books.</p>"
            "<p><b>Features in V1:</b>"
            "<ul>"
            "<li>Modular Extensible Book Plugin Engine</li>"
            "<li>Typographic Point Physical Precision Coordinates</li>"
            "<li>KDP Trim, Bleed & Margin Safety Specifications</li>"
            "<li>Atomic Project Storage & Crash Recovery</li>"
            "</ul></p>"
            "<p>© 2026 KDP Studio Team. All rights reserved.</p>",
        )
