"""
New Project Wizard Dialog.
Guides the user through Book Type, Project Name, Metadata, Location, and Initial Trim Size.
"""

from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QCheckBox,
    QFileDialog,
    QMessageBox,
    QFrame,
    QGridLayout,
    QRadioButton,
    QButtonGroup,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from app.core.document_model import BookType, TrimPreset, KDP_TRIM_PRESETS, ProjectDocument
from app.core.project_manager import ProjectManager
from app.core.settings_manager import SettingsManager
from app.modules.registry import ModuleRegistry
from app.ui.theme import Theme


class ProjectSetupDialog(QDialog):
    project_created = Signal(object)  # Emits ProjectDocument

    def __init__(self, parent=None, initial_book_type: BookType = BookType.COLORING_BOOK):
        super().__init__(parent)
        self.setWindowTitle("Create New KDP Book Project")
        self.setModal(True)
        self.setMinimumWidth(620)
        self.setMinimumHeight(560)

        self.project_manager = ProjectManager.get_instance()
        self.settings_manager = SettingsManager.get_instance()
        self.module_registry = ModuleRegistry.get_instance()

        self.selected_book_type = initial_book_type
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(18)

        # Header Title & Subtitle
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        title_lbl = QLabel("Create New Book Project")
        title_font = QFont("Segoe UI", 16, QFont.Bold)
        title_lbl.setFont(title_font)
        title_lbl.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")

        subtitle_lbl = QLabel("Configure your KDP book settings and initialize a local offline workspace.")
        subtitle_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 13px;")

        header_layout.addWidget(title_lbl)
        header_layout.addWidget(subtitle_lbl)
        main_layout.addLayout(header_layout)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet(f"background-color: {Theme.BORDER}; max-height: 1px;")
        main_layout.addWidget(divider)

        # Form Layout Grid
        form_grid = QGridLayout()
        form_grid.setVerticalSpacing(14)
        form_grid.setHorizontalSpacing(16)
        row = 0

        # 1. Book Type Selection
        type_lbl = QLabel("Book Type:")
        type_lbl.setStyleSheet(f"font-weight: 600; color: {Theme.TEXT_PRIMARY};")
        self.type_combo = QComboBox()
        
        modules = self.module_registry.get_all_modules()
        for mod in modules:
            tag = "" if mod.is_available_in_v1 else " (Coming Soon)"
            self.type_combo.addItem(f"{mod.display_name}{tag}", mod.module_id)
            if mod.module_id == self.selected_book_type.value:
                self.type_combo.setCurrentIndex(self.type_combo.count() - 1)

        self.type_combo.currentIndexChanged.connect(self._on_type_changed)
        form_grid.addWidget(type_lbl, row, 0, Qt.AlignRight)
        form_grid.addWidget(self.type_combo, row, 1)
        row += 1

        # 2. Project Name
        name_lbl = QLabel("Project Name:")
        name_lbl.setStyleSheet(f"font-weight: 600; color: {Theme.TEXT_PRIMARY};")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g. Animal Kingdom Coloring Book")
        self.name_edit.setText("Animal Coloring Book")
        self.name_edit.textChanged.connect(self._update_path_preview)
        form_grid.addWidget(name_lbl, row, 0, Qt.AlignRight)
        form_grid.addWidget(self.name_edit, row, 1)
        row += 1

        # 3. Author / Publisher
        author_lbl = QLabel("Author / Brand:")
        author_lbl.setStyleSheet(f"font-weight: 600; color: {Theme.TEXT_PRIMARY};")
        self.author_edit = QLineEdit()
        self.author_edit.setPlaceholderText("e.g. Creative Kids Press")
        form_grid.addWidget(author_lbl, row, 0, Qt.AlignRight)
        form_grid.addWidget(self.author_edit, row, 1)
        row += 1

        # 4. Project Parent Location
        loc_lbl = QLabel("Project Folder:")
        loc_lbl.setStyleSheet(f"font-weight: 600; color: {Theme.TEXT_PRIMARY};")
        
        loc_layout = QHBoxLayout()
        loc_layout.setSpacing(8)
        self.loc_edit = QLineEdit()
        default_dir = self.settings_manager.default_project_dir
        self.loc_edit.setText(str(default_dir))
        self.loc_edit.textChanged.connect(self._update_path_preview)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_location)
        loc_layout.addWidget(self.loc_edit)
        loc_layout.addWidget(browse_btn)

        form_grid.addWidget(loc_lbl, row, 0, Qt.AlignRight)
        form_grid.addLayout(loc_layout, row, 1)
        row += 1

        # Path preview label
        self.path_preview_lbl = QLabel()
        self.path_preview_lbl.setStyleSheet(f"color: {Theme.TEXT_MUTED}; font-size: 11px; font-style: italic;")
        form_grid.addWidget(self.path_preview_lbl, row, 1)
        row += 1

        # 5. Trim Size
        trim_lbl = QLabel("KDP Trim Size:")
        trim_lbl.setStyleSheet(f"font-weight: 600; color: {Theme.TEXT_PRIMARY};")
        self.trim_combo = QComboBox()
        for preset in KDP_TRIM_PRESETS:
            desc = f" - {preset.description}" if preset.description else ""
            self.trim_combo.addItem(f"{preset.name}{desc}", preset.id)
        form_grid.addWidget(trim_lbl, row, 0, Qt.AlignRight)
        form_grid.addWidget(self.trim_combo, row, 1)
        row += 1

        # 6. Bleed Setting
        bleed_lbl = QLabel("Bleed:")
        bleed_lbl.setStyleSheet(f"font-weight: 600; color: {Theme.TEXT_PRIMARY};")
        self.bleed_chk = QCheckBox("Enable Full Page Bleed (+0.125 in outer trim margin)")
        self.bleed_chk.setToolTip("Select if illustrations or backgrounds extend to the outer edge of the cut page.")
        form_grid.addWidget(bleed_lbl, row, 0, Qt.AlignRight)
        form_grid.addWidget(self.bleed_chk, row, 1)
        row += 1

        main_layout.addLayout(form_grid)
        main_layout.addStretch(1)

        # Bottom Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        self.create_btn = QPushButton("Create Project Workspace")
        self.create_btn.setProperty("primary", True)
        self.create_btn.clicked.connect(self._create_project)

        btn_layout.addStretch(1)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(self.create_btn)
        main_layout.addLayout(btn_layout)

        self._update_path_preview()

    def _on_type_changed(self, index: int):
        mod_id = self.type_combo.currentData()
        mod = self.module_registry.get_module(mod_id)
        if mod and not mod.is_available_in_v1:
            QMessageBox.information(
                self,
                f"{mod.display_name} - Coming Soon",
                f"The '{mod.display_name}' module is currently in architecture preview.\n\n"
                "In V1, please select 'Coloring Book' for the active production pipeline.",
            )
            # Revert to Coloring Book
            self.type_combo.setCurrentIndex(0)

    def _browse_location(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Parent Folder for Projects",
            self.loc_edit.text(),
        )
        if folder:
            self.loc_edit.setText(folder)
            self._update_path_preview()

    def _sanitize_folder_name(self, name: str) -> str:
        clean = "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).strip()
        return clean.replace(" ", "_") if clean else "Untitled_Book"

    def _update_path_preview(self):
        parent_dir = self.loc_edit.text().strip()
        proj_name = self.name_edit.text().strip()
        folder_name = self._sanitize_folder_name(proj_name)
        target = Path(parent_dir) / folder_name if parent_dir else Path(folder_name)
        self.path_preview_lbl.setText(f"Workspace path: {target}")

    def _create_project(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Project Name Required", "Please enter a name for your book project.")
            self.name_edit.setFocus()
            return

        parent_dir_str = self.loc_edit.text().strip()
        if not parent_dir_str:
            QMessageBox.warning(self, "Location Required", "Please specify a folder location for your project.")
            return

        folder_name = self._sanitize_folder_name(name)
        project_dir = Path(parent_dir_str) / folder_name

        if project_dir.exists() and any(project_dir.iterdir()):
            reply = QMessageBox.question(
                self,
                "Folder Not Empty",
                f"The directory '{project_dir.name}' already contains files.\n\nDo you want to initialize the project here anyway?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                return

        # Lookup selected trim preset
        preset_id = self.trim_combo.currentData()
        preset = next((p for p in KDP_TRIM_PRESETS if p.id == preset_id), KDP_TRIM_PRESETS[0])

        try:
            doc = self.project_manager.create_new_project(
                name=name,
                location_dir=project_dir,
                author=self.author_edit.text().strip(),
                publisher="",
                book_type=BookType.COLORING_BOOK,
                trim_preset=preset,
                has_bleed=self.bleed_chk.isChecked(),
            )
            self.project_created.emit(doc)
            self.accept()
        except Exception as ex:
            QMessageBox.critical(
                self,
                "Project Creation Error",
                f"Failed to create project workspace at {project_dir}:\n\n{str(ex)}",
            )
