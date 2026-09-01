"""
PagesPanel: Bottom page timeline / thumbnail ribbon with page reordering,
adding, duplicating, deleting, and active page switching.
"""

from typing import Optional, List

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QInputDialog,
    QMessageBox,
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QBrush, QPixmap

from app.core.document_model import ProjectDocument
from app.core.page_model import PageModel, LayerModel, ElementModel, ElementType
from app.core.project_manager import ProjectManager
from app.ui.theme import Theme


class PageThumbnailCard(QFrame):
    clicked = Signal(int)
    double_clicked = Signal(int)

    def __init__(self, page_index: int, page: PageModel, is_active: bool = False, parent=None):
        super().__init__(parent)
        self.page_index = page_index
        self.page = page
        self.is_active = is_active

        self.setFixedSize(110, 150)
        self.setCursor(Qt.PointingHandCursor)
        self._update_style()
        self._init_ui()

    def _update_style(self):
        border_color = Theme.PRIMARY if self.is_active else Theme.BORDER
        bg_color = Theme.BG_CARD_HOVER if self.is_active else Theme.BG_SURFACE
        self.setStyleSheet(
            f"QFrame {{"
            f"  background-color: {bg_color};"
            f"  border: 2px solid {border_color};"
            f"  border-radius: 8px;"
            f"}}"
            f"QFrame:hover {{"
            f"  border-color: {Theme.PRIMARY};"
            f"}}"
        )

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        # Page Number Badge
        top_row = QHBoxLayout()
        top_row.setSpacing(0)
        badge = QLabel(f"Page {self.page_index + 1}")
        badge.setStyleSheet(
            f"color: {'#ffffff' if self.is_active else Theme.TEXT_MUTED}; "
            f"font-size: 10px; font-weight: bold; background: transparent; border: none;"
        )
        top_row.addWidget(badge)
        top_row.addStretch(1)
        layout.addLayout(top_row)

        # Mini Canvas Preview Area
        self.preview_frame = QFrame()
        self.preview_frame.setStyleSheet(
            "background-color: #ffffff; border: 1px solid #d1d5db; border-radius: 4px;"
        )
        preview_layout = QVBoxLayout(self.preview_frame)
        preview_layout.setContentsMargins(2, 2, 2, 2)
        preview_layout.setAlignment(Qt.AlignCenter)

        # Mini illustration hint
        mini_lbl = QLabel("🎨" if len(self.page.get_all_elements()) > 0 else "📄")
        mini_lbl.setStyleSheet("font-size: 20px; background: transparent; border: none;")
        preview_layout.addWidget(mini_lbl, 0, Qt.AlignCenter)

        layout.addWidget(self.preview_frame, 1)

        # Page Title Label (truncated)
        title_text = self.page.title if self.page.title else f"Page {self.page_index + 1}"
        if len(title_text) > 12:
            title_text = title_text[:11] + "…"
        title_lbl = QLabel(title_text)
        title_lbl.setStyleSheet(
            f"color: {Theme.TEXT_PRIMARY}; font-size: 10px; font-weight: 500; "
            f"background: transparent; border: none;"
        )
        title_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_lbl)

    def set_active(self, active: bool):
        self.is_active = active
        self._update_style()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.page_index)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.double_clicked.emit(self.page_index)
        super().mouseDoubleClickEvent(event)


class PagesPanel(QWidget):
    page_selected = Signal(int, object)  # Emits (page_index, PageModel)
    pages_updated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_manager = ProjectManager.get_instance()
        self.current_page_index: int = 0
        self.thumbnails: List[PageThumbnailCard] = []

        self.setFixedHeight(190)
        self.setStyleSheet(f"background-color: {Theme.BG_DARK}; border-top: 1px solid {Theme.BORDER};")
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 8, 16, 8)
        main_layout.setSpacing(8)

        # Top Action Bar
        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)

        lbl = QLabel("📖 Pages Timeline")
        lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        lbl.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")
        top_bar.addWidget(lbl)

        self.page_count_lbl = QLabel("0 Pages")
        self.page_count_lbl.setStyleSheet(f"color: {Theme.TEXT_MUTED}; font-size: 11px;")
        top_bar.addWidget(self.page_count_lbl)

        top_bar.addStretch(1)

        # Action Buttons
        self.add_page_btn = QPushButton("➕ Add Page")
        self.add_page_btn.setStyleSheet("padding: 4px 10px; font-size: 11px;")
        self.add_page_btn.clicked.connect(self._add_new_page)
        top_bar.addWidget(self.add_page_btn)

        self.dup_page_btn = QPushButton("⎘ Duplicate")
        self.dup_page_btn.setStyleSheet("padding: 4px 10px; font-size: 11px;")
        self.dup_page_btn.clicked.connect(self._duplicate_current_page)
        top_bar.addWidget(self.dup_page_btn)

        self.move_left_btn = QPushButton("◀ Move")
        self.move_left_btn.setStyleSheet("padding: 4px 8px; font-size: 11px;")
        self.move_left_btn.clicked.connect(lambda: self._reorder_page(-1))
        top_bar.addWidget(self.move_left_btn)

        self.move_right_btn = QPushButton("Move ▶")
        self.move_right_btn.setStyleSheet("padding: 4px 8px; font-size: 11px;")
        self.move_right_btn.clicked.connect(lambda: self._reorder_page(1))
        top_bar.addWidget(self.move_right_btn)

        self.del_page_btn = QPushButton("🗑 Delete")
        self.del_page_btn.setStyleSheet(f"color: {Theme.DANGER}; padding: 4px 10px; font-size: 11px;")
        self.del_page_btn.clicked.connect(self._delete_current_page)
        top_bar.addWidget(self.del_page_btn)

        main_layout.addLayout(top_bar)

        # Horizontal Scroll Area for Thumbnails
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.NoFrame)

        self.scroll_content = QWidget()
        self.thumbs_layout = QHBoxLayout(self.scroll_content)
        self.thumbs_layout.setContentsMargins(0, 4, 0, 4)
        self.thumbs_layout.setSpacing(12)
        self.thumbs_layout.setAlignment(Qt.AlignLeft)

        scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(scroll_area, 1)

    def refresh_pages(self, select_index: Optional[int] = None):
        doc = self.project_manager.current_document
        if not doc:
            self._clear_thumbnails()
            self.page_count_lbl.setText("0 Pages")
            return

        # Clear existing cards
        self._clear_thumbnails()

        pages_count = len(doc.pages)
        self.page_count_lbl.setText(f"{pages_count} Pages")

        if select_index is not None:
            self.current_page_index = max(0, min(pages_count - 1, select_index))
        elif self.current_page_index >= pages_count:
            self.current_page_index = max(0, pages_count - 1)

        for idx, page_data in enumerate(doc.pages):
            page = PageModel.from_dict(page_data) if isinstance(page_data, dict) else page_data
            is_active = (idx == self.current_page_index)
            card = PageThumbnailCard(idx, page, is_active=is_active)
            card.clicked.connect(self._on_card_clicked)
            card.double_clicked.connect(self._on_card_double_clicked)
            self.thumbs_layout.addWidget(card)
            self.thumbnails.append(card)

        # Emit selection
        if pages_count > 0:
            current_page_data = doc.pages[self.current_page_index]
            p_obj = PageModel.from_dict(current_page_data) if isinstance(current_page_data, dict) else current_page_data
            self.page_selected.emit(self.current_page_index, p_obj)

    def _clear_thumbnails(self):
        while self.thumbs_layout.count():
            item = self.thumbs_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.thumbnails.clear()

    def _on_card_clicked(self, index: int):
        if 0 <= index < len(self.thumbnails):
            for i, card in enumerate(self.thumbnails):
                card.set_active(i == index)
            self.current_page_index = index

            doc = self.project_manager.current_document
            if doc and index < len(doc.pages):
                page_data = doc.pages[index]
                p_obj = PageModel.from_dict(page_data) if isinstance(page_data, dict) else page_data
                self.page_selected.emit(index, p_obj)

    def _on_card_double_clicked(self, index: int):
        doc = self.project_manager.current_document
        if not doc or index >= len(doc.pages):
            return

        page_data = doc.pages[index]
        current_title = page_data.get("title", "") if isinstance(page_data, dict) else page_data.title

        new_title, ok = QInputDialog.getText(
            self,
            "Rename Page Title",
            f"Enter title for Page {index + 1}:",
            text=current_title,
        )
        if ok and new_title.strip():
            if isinstance(page_data, dict):
                page_data["title"] = new_title.strip()
            else:
                page_data.title = new_title.strip()
            self.project_manager.save_current_project()
            self.refresh_pages(self.current_page_index)
            self.pages_updated.emit()

    def _add_new_page(self):
        doc = self.project_manager.current_document
        if not doc:
            return

        new_idx = len(doc.pages) + 1
        new_page = PageModel(
            page_id=f"page_{new_idx:03d}",
            page_number=new_idx,
            title=f"Page {new_idx}",
            layers=[
                LayerModel(layer_id=f"bg_{new_idx}", name="Background", locked=True),
                LayerModel(layer_id=f"main_{new_idx}", name="Illustration", locked=False),
                LayerModel(layer_id=f"title_{new_idx}", name="Title", locked=False),
            ],
        )

        doc.pages.append(new_page.to_dict())
        self.project_manager.save_current_project()
        self.refresh_pages(len(doc.pages) - 1)
        self.pages_updated.emit()

    def _duplicate_current_page(self):
        doc = self.project_manager.current_document
        if not doc or not doc.pages:
            return

        curr_page = doc.pages[self.current_page_index]
        dup_dict = dict(curr_page) if isinstance(curr_page, dict) else curr_page.to_dict()
        new_idx = len(doc.pages) + 1
        dup_dict["page_id"] = f"page_copy_{new_idx:03d}"
        dup_dict["page_number"] = new_idx
        dup_dict["title"] = f"{dup_dict.get('title', 'Page')} (Copy)"

        doc.pages.insert(self.current_page_index + 1, dup_dict)
        self.project_manager.save_current_project()
        self.refresh_pages(self.current_page_index + 1)
        self.pages_updated.emit()

    def _delete_current_page(self):
        doc = self.project_manager.current_document
        if not doc or not doc.pages:
            return

        if len(doc.pages) <= 1:
            QMessageBox.information(
                self,
                "Cannot Delete Page",
                "A book project must contain at least one page.",
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete Page",
            f"Are you sure you want to delete Page {self.current_page_index + 1}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            del doc.pages[self.current_page_index]
            self.project_manager.save_current_project()
            target_idx = max(0, self.current_page_index - 1)
            self.refresh_pages(target_idx)
            self.pages_updated.emit()

    def _reorder_page(self, delta: int):
        doc = self.project_manager.current_document
        if not doc or not doc.pages:
            return

        old_idx = self.current_page_index
        new_idx = old_idx + delta
        if 0 <= new_idx < len(doc.pages):
            item = doc.pages.pop(old_idx)
            doc.pages.insert(new_idx, item)
            self.project_manager.save_current_project()
            self.refresh_pages(new_idx)
            self.pages_updated.emit()
