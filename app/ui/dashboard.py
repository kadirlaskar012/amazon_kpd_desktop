"""
Modern Dashboard view for KDP Book Production Studio.
Displays Recent Projects, Quick Create actions, Book Type selector, and Templates.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QFileDialog,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QCursor

from app.core.document_model import BookType
from app.core.project_manager import ProjectManager
from app.core.settings_manager import SettingsManager
from app.modules.registry import ModuleRegistry
from app.ui.theme import Theme
from app.ui.project_setup import ProjectSetupDialog


class DashboardView(QWidget):
    project_opened = Signal(object)  # Emits ProjectDocument

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_manager = ProjectManager.get_instance()
        self.settings_manager = SettingsManager.get_instance()
        self.module_registry = ModuleRegistry.get_instance()

        self._init_ui()
        self.refresh_recent_projects()

        # Connect project manager listener
        self.project_manager.register_project_changed_listener(lambda doc: self.refresh_recent_projects())

    def _init_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(40, 36, 40, 36)
        layout.setSpacing(32)

        # 1. Hero Welcome Banner
        hero_frame = QFrame()
        hero_frame.setStyleSheet(
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e1b4b, stop:1 {Theme.BG_CARD}); "
            f"border: 1px solid {Theme.BORDER}; border-radius: 12px; padding: 24px;"
        )
        hero_layout = QHBoxLayout(hero_frame)
        hero_layout.setContentsMargins(12, 12, 12, 12)
        hero_layout.setSpacing(24)

        hero_text_layout = QVBoxLayout()
        hero_text_layout.setSpacing(6)

        hero_title = QLabel("KDP Book Production Studio")
        hero_title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        hero_title.setStyleSheet("color: #ffffff; background: transparent;")

        hero_subtitle = QLabel(
            "Rapidly generate, edit, validate, and export print-ready children's coloring and activity books for Amazon KDP."
        )
        hero_subtitle.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 14px; background: transparent;")
        hero_subtitle.setWordWrap(True)

        hero_text_layout.addWidget(hero_title)
        hero_text_layout.addWidget(hero_subtitle)
        hero_layout.addLayout(hero_text_layout, 1)

        # Hero Action Buttons
        hero_btn_layout = QHBoxLayout()
        hero_btn_layout.setSpacing(12)

        open_btn = QPushButton("Open Project...")
        open_btn.setStyleSheet(f"padding: 12px 20px; font-size: 14px;")
        open_btn.clicked.connect(self._open_project_dialog)

        new_book_btn = QPushButton("✨ Create New Book")
        new_book_btn.setProperty("primary", True)
        new_book_btn.setStyleSheet(f"padding: 12px 24px; font-size: 14px; font-weight: bold;")
        new_book_btn.clicked.connect(lambda: self._start_new_project(BookType.COLORING_BOOK))

        hero_btn_layout.addWidget(open_btn)
        hero_btn_layout.addWidget(new_book_btn)
        hero_layout.addLayout(hero_btn_layout)

        layout.addWidget(hero_frame)

        # 2. Book Types Quick Start Grid
        types_section = QVBoxLayout()
        types_section.setSpacing(14)

        section_title = QLabel("Book Production Modules")
        section_title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        section_title.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")
        types_section.addWidget(section_title)

        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(16)
        grid_layout.setVerticalSpacing(16)

        modules = self.module_registry.get_all_modules()
        for idx, mod in enumerate(modules):
            card = self._create_module_card(mod)
            r = idx // 3
            c = idx % 3
            grid_layout.addWidget(card, r, c)

        types_section.addLayout(grid_layout)
        layout.addLayout(types_section)

        # 3. Recent Projects Section
        recents_section = QVBoxLayout()
        recents_section.setSpacing(14)

        recents_header = QHBoxLayout()
        recents_title = QLabel("Recent Projects")
        recents_title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        recents_title.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setStyleSheet("padding: 4px 10px; font-size: 11px;")
        self.refresh_btn.clicked.connect(self.refresh_recent_projects)

        recents_header.addWidget(recents_title)
        recents_header.addStretch(1)
        recents_header.addWidget(self.refresh_btn)
        recents_section.addLayout(recents_header)

        # Recent Projects List Container
        self.recents_container = QVBoxLayout()
        self.recents_container.setSpacing(8)
        self.no_recents_lbl = QLabel("No recent projects found. Click 'Create New Book' to get started!")
        self.no_recents_lbl.setStyleSheet(f"color: {Theme.TEXT_MUTED}; font-style: italic; padding: 24px;")
        self.no_recents_lbl.setAlignment(Qt.AlignCenter)
        self.recents_container.addWidget(self.no_recents_lbl)

        recents_section.addLayout(self.recents_container)
        layout.addLayout(recents_section)

        layout.addStretch(1)
        scroll_area.setWidget(scroll_content)
        root_layout.addWidget(scroll_area)

    def _create_module_card(self, module) -> QFrame:
        card = QFrame()
        card.setCursor(QCursor(Qt.PointingHandCursor))
        card.setStyleSheet(
            f"QFrame {{"
            f"  background-color: {Theme.BG_CARD};"
            f"  border: 1px solid {Theme.BORDER};"
            f"  border-radius: 10px;"
            f"  padding: 16px;"
            f"}}"
            f"QFrame:hover {{"
            f"  background-color: {Theme.BG_CARD_HOVER};"
            f"  border-color: {Theme.PRIMARY};"
            f"}}"
        )
        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(14, 14, 14, 14)
        c_layout.setSpacing(8)

        # Top row: Name + Badge
        top_row = QHBoxLayout()
        name_lbl = QLabel(module.display_name)
        name_lbl.setFont(QFont("Segoe UI", 13, QFont.Bold))
        name_lbl.setStyleSheet("color: #ffffff; background: transparent; border: none;")

        top_row.addWidget(name_lbl)
        top_row.addStretch(1)

        badge_lbl = QLabel("Active V1" if module.is_available_in_v1 else "Coming Soon")
        badge_bg = Theme.PRIMARY if module.is_available_in_v1 else Theme.TEXT_DISABLED
        badge_lbl.setStyleSheet(
            f"background-color: {badge_bg}; color: #ffffff; font-size: 10px; font-weight: bold; "
            f"padding: 2px 8px; border-radius: 4px; border: none;"
        )
        top_row.addWidget(badge_lbl)
        c_layout.addLayout(top_row)

        desc_lbl = QLabel(module.description)
        desc_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 11px; background: transparent; border: none;")
        desc_lbl.setWordWrap(True)
        c_layout.addWidget(desc_lbl)

        # Action Button inside card
        card_btn = QPushButton("Launch Studio" if module.is_available_in_v1 else "Preview Architecture")
        card_btn.setEnabled(module.is_available_in_v1)
        if module.is_available_in_v1:
            card_btn.setProperty("primary", True)
            try:
                b_type = BookType(module.module_id)
            except ValueError:
                b_type = BookType.COLORING_BOOK
            card_btn.clicked.connect(lambda: self._start_new_project(b_type))
        else:
            card_btn.clicked.connect(lambda: QMessageBox.information(
                self,
                f"{module.display_name} - Coming Soon",
                f"The '{module.display_name}' module is part of the modular plugin roadmap.\n"
                "In V1, please select 'Coloring Book' for full production.",
            ))
        c_layout.addWidget(card_btn)

        return card

    def refresh_recent_projects(self):
        # Clear existing items in container
        while self.recents_container.count():
            item = self.recents_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        recent_list = self.settings_manager.get_recent_projects()
        if not recent_list:
            lbl = QLabel("No recent projects found. Click 'Create New Book' to get started!")
            lbl.setStyleSheet(f"color: {Theme.TEXT_MUTED}; font-style: italic; padding: 24px;")
            lbl.setAlignment(Qt.AlignCenter)
            self.recents_container.addWidget(lbl)
            return

        for p_info in recent_list:
            item_card = self._create_recent_project_item(p_info)
            self.recents_container.addWidget(item_card)

    def _create_recent_project_item(self, p_info: dict) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet(
            f"QFrame {{"
            f"  background-color: {Theme.BG_SURFACE};"
            f"  border: 1px solid {Theme.BORDER};"
            f"  border-radius: 8px;"
            f"  padding: 8px 14px;"
            f"}}"
            f"QFrame:hover {{"
            f"  background-color: {Theme.BG_CARD};"
            f"  border-color: {Theme.BORDER_FOCUS};"
            f"}}"
        )
        f_layout = QHBoxLayout(frame)
        f_layout.setContentsMargins(12, 10, 12, 10)
        f_layout.setSpacing(16)

        # Icon / Type indicator
        type_icon = QLabel("🎨" if p_info.get("book_type") == "coloring_book" else "📖")
        type_icon.setFont(QFont("Segoe UI Emoji", 16))
        type_icon.setStyleSheet("background: transparent; border: none;")
        f_layout.addWidget(type_icon)

        # Project Info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        name_lbl = QLabel(p_info.get("name", "Untitled Project"))
        name_lbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
        name_lbl.setStyleSheet("color: #ffffff; background: transparent; border: none;")

        path_lbl = QLabel(p_info.get("path", ""))
        path_lbl.setStyleSheet(f"color: {Theme.TEXT_MUTED}; font-size: 11px; background: transparent; border: none;")

        info_layout.addWidget(name_lbl)
        info_layout.addWidget(path_lbl)
        f_layout.addLayout(info_layout, 1)

        # Page count & date
        pages = p_info.get("page_count", 0)
        pages_lbl = QLabel(f"{pages} pages" if pages > 0 else "New")
        pages_lbl.setStyleSheet(
            f"background-color: {Theme.BG_INPUT}; color: {Theme.TEXT_SECONDARY}; "
            f"padding: 3px 8px; border-radius: 4px; font-size: 11px; border: 1px solid {Theme.BORDER};"
        )
        f_layout.addWidget(pages_lbl)

        # Buttons
        open_btn = QPushButton("Open")
        open_btn.setProperty("primary", True)
        open_btn.setStyleSheet("padding: 6px 14px; font-size: 12px;")
        path_str = p_info.get("path")
        open_btn.clicked.connect(lambda: self._open_project_path(Path(path_str)))
        f_layout.addWidget(open_btn)

        remove_btn = QPushButton("✕")
        remove_btn.setToolTip("Remove from recent list")
        remove_btn.setStyleSheet(f"color: {Theme.TEXT_MUTED}; padding: 6px 10px; font-size: 12px;")
        remove_btn.clicked.connect(lambda: self._remove_recent_project(path_str))
        f_layout.addWidget(remove_btn)

        return frame

    def _start_new_project(self, book_type: BookType = BookType.COLORING_BOOK):
        dlg = ProjectSetupDialog(self, initial_book_type=book_type)
        if dlg.exec():
            doc = self.project_manager.current_document
            if doc:
                self.project_opened.emit(doc)

    def _open_project_dialog(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select KDP Project Folder",
            str(self.settings_manager.default_project_dir),
        )
        if folder:
            self._open_project_path(Path(folder))

    def _open_project_path(self, path: Path):
        try:
            doc = self.project_manager.open_project(path)
            self.project_opened.emit(doc)
        except Exception as ex:
            QMessageBox.critical(
                self,
                "Unable to Open Project",
                f"Failed to open project at:\n{path}\n\nError: {str(ex)}",
            )

    def _remove_recent_project(self, path_str: str):
        self.settings_manager.remove_recent_project(path_str)
        self.refresh_recent_projects()
