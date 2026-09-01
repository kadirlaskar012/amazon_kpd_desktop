"""
CanvasEditorView: Master canvas workspace integrating left toolbox,
center QGraphicsView/Scene, right physical property inspector, top mini-toolbar, and bottom page timeline.
"""

from typing import Optional
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QFrame,
    QButtonGroup,
    QFileDialog,
    QMessageBox,
    QSplitter,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon

from app.core.document_model import BookSettings
from app.core.page_model import PageModel, ElementModel, ElementType, LayerModel
from app.core.project_manager import ProjectManager
from app.core.units import format_dimension
from app.ui.theme import Theme
from app.ui.canvas.canvas_scene import CanvasScene
from app.ui.canvas.canvas_view import CanvasView
from app.ui.properties_panel import PropertiesPanel
from app.ui.pages_panel import PagesPanel


class CanvasEditorView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_manager = ProjectManager.get_instance()

        self._init_ui()
        self._wire_signals()
        self.load_project_state()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top Mini-Toolbar
        top_bar = QFrame()
        top_bar.setStyleSheet(
            f"background-color: {Theme.BG_SURFACE}; border-bottom: 1px solid {Theme.BORDER}; padding: 4px 12px;"
        )
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(8, 4, 8, 4)
        top_layout.setSpacing(10)

        # Left: Active Page Title Display
        self.page_title_lbl = QLabel("Page 1")
        self.page_title_lbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.page_title_lbl.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")
        top_layout.addWidget(self.page_title_lbl)

        top_layout.addWidget(QLabel(" | "))

        # Center Tools: Quick Add Elements
        self.add_img_btn = QPushButton("🖼 Add Image")
        self.add_img_btn.setStyleSheet("padding: 4px 10px; font-size: 11px;")
        self.add_img_btn.clicked.connect(self._on_add_image_clicked)
        top_layout.addWidget(self.add_img_btn)

        self.add_text_btn = QPushButton("🔤 Add Text")
        self.add_text_btn.setStyleSheet("padding: 4px 10px; font-size: 11px;")
        self.add_text_btn.clicked.connect(self._on_add_text_clicked)
        top_layout.addWidget(self.add_text_btn)

        self.add_rect_btn = QPushButton("⬜ Add Shape")
        self.add_rect_btn.setStyleSheet("padding: 4px 10px; font-size: 11px;")
        self.add_rect_btn.clicked.connect(self._on_add_shape_clicked)
        top_layout.addWidget(self.add_rect_btn)

        top_layout.addStretch(1)

        # Snap & Guide Toggles
        self.guide_toggle_btn = QPushButton("👁 Guides: ON")
        self.guide_toggle_btn.setCheckable(True)
        self.guide_toggle_btn.setChecked(True)
        self.guide_toggle_btn.setStyleSheet("padding: 4px 10px; font-size: 11px;")
        self.guide_toggle_btn.clicked.connect(self._toggle_guides)
        top_layout.addWidget(self.guide_toggle_btn)

        self.snap_toggle_btn = QPushButton("🧲 Snap: ON")
        self.snap_toggle_btn.setCheckable(True)
        self.snap_toggle_btn.setChecked(True)
        self.snap_toggle_btn.setStyleSheet("padding: 4px 10px; font-size: 11px;")
        self.snap_toggle_btn.clicked.connect(self._toggle_snap)
        top_layout.addWidget(self.snap_toggle_btn)

        top_layout.addWidget(QLabel(" | "))

        # Zoom Controls
        zoom_out_btn = QPushButton("−")
        zoom_out_btn.setToolTip("Zoom Out (Ctrl+Minus / Ctrl+Wheel)")
        zoom_out_btn.setStyleSheet("padding: 4px 8px; font-weight: bold;")
        zoom_out_btn.clicked.connect(lambda: self.canvas_view.zoom_out())
        top_layout.addWidget(zoom_out_btn)

        self.zoom_lbl = QLabel("100%")
        self.zoom_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; min-width: 44px;")
        self.zoom_lbl.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self.zoom_lbl)

        zoom_in_btn = QPushButton("+")
        zoom_in_btn.setToolTip("Zoom In (Ctrl+Plus / Ctrl+Wheel)")
        zoom_in_btn.setStyleSheet("padding: 4px 8px; font-weight: bold;")
        zoom_in_btn.clicked.connect(lambda: self.canvas_view.zoom_in())
        top_layout.addWidget(zoom_in_btn)

        fit_btn = QPushButton("⛶ Fit")
        fit_btn.setToolTip("Fit page to view")
        fit_btn.setStyleSheet("padding: 4px 8px; font-size: 11px;")
        fit_btn.clicked.connect(lambda: self.canvas_view.zoom_to_fit())
        top_layout.addWidget(fit_btn)

        # Coordinate Tracker
        self.coord_lbl = QLabel("X: 0.00 Y: 0.00")
        self.coord_lbl.setStyleSheet(f"color: {Theme.TEXT_MUTED}; font-size: 11px; margin-left: 12px;")
        top_layout.addWidget(self.coord_lbl)

        main_layout.addWidget(top_bar)

        # 2. Middle Central Splitter (Left Toolbox + Center Canvas + Right Properties)
        mid_splitter = QSplitter(Qt.Horizontal)
        mid_splitter.setStyleSheet(f"QSplitter::handle {{ background-color: {Theme.BORDER}; width: 1px; }}")

        # Center Canvas Scene & View
        self.canvas_scene = CanvasScene()
        self.canvas_view = CanvasView(self.canvas_scene, self)
        mid_splitter.addWidget(self.canvas_view)

        # Right Properties Panel
        self.properties_panel = PropertiesPanel(parent=self)
        mid_splitter.addWidget(self.properties_panel)
        mid_splitter.setStretchFactor(0, 4)
        mid_splitter.setStretchFactor(1, 1)

        main_layout.addWidget(mid_splitter, 1)

        # 3. Bottom Pages Timeline Ribbon
        self.pages_panel = PagesPanel(self)
        main_layout.addWidget(self.pages_panel)

    def _wire_signals(self):
        # Canvas Scene element selection -> Properties Panel
        self.canvas_scene.element_selected.connect(self.properties_panel.set_element)
        self.canvas_scene.page_modified.connect(self._on_page_modified_from_canvas)

        # Properties Panel property changes -> Update canvas item
        self.properties_panel.property_changed.connect(self._on_property_changed_from_panel)

        # Canvas View tracking
        self.canvas_view.cursor_position_changed.connect(self._on_cursor_moved)
        self.canvas_view.zoom_changed.connect(self._on_zoom_changed)
        self.canvas_view.asset_dropped.connect(self._on_asset_dropped_on_canvas)

        # Pages Panel selection
        self.pages_panel.page_selected.connect(self._on_page_selected_from_timeline)
        self.pages_panel.pages_updated.connect(self._on_pages_updated_from_timeline)

        # Project Manager events
        self.project_manager.register_project_changed_listener(lambda doc: self.load_project_state())

    def load_project_state(self):
        doc = self.project_manager.current_document
        if not doc:
            self.canvas_scene.clear()
            self.pages_panel.refresh_pages()
            return

        self.canvas_scene.set_settings(doc.settings)
        self.canvas_scene.set_project_dir(self.project_manager.current_project_dir)
        self.properties_panel.set_settings(doc.settings)

        # If project has no pages, initialize page 1
        if not doc.pages:
            self.pages_panel._add_new_page()
        else:
            self.pages_panel.refresh_pages(0)

        # Automatically fit canvas in view
        self.canvas_view.zoom_to_fit()

    def _on_page_selected_from_timeline(self, page_index: int, page: PageModel):
        self.page_title_lbl.setText(f"Page {page_index + 1}: {page.title if page.title else 'Untitled'}")
        self.canvas_scene.load_page(page, page_index)
        self.properties_panel.set_element(None)

    def _on_pages_updated_from_timeline(self):
        self.project_manager.set_dirty(True)

    def _on_page_modified_from_canvas(self, page: PageModel):
        doc = self.project_manager.current_document
        if doc and 0 <= self.canvas_scene.current_page_index < len(doc.pages):
            doc.pages[self.canvas_scene.current_page_index] = page.to_dict()
            self.project_manager.set_dirty(True)

    def _on_property_changed_from_panel(self, elem: ElementModel):
        # Find item in scene and trigger update
        item = self.canvas_scene._element_items.get(elem.element_id)
        if item:
            item.setPos(elem.x_pt, elem.y_pt)
            item.setRotation(elem.rotation_deg)
            item.setOpacity(elem.opacity)
            item.setVisible(elem.visible)
            item.prepareGeometryChange()
            item.update()
        if self.canvas_scene.current_page:
            self.canvas_scene.page_modified.emit(self.canvas_scene.current_page)

    def _on_cursor_moved(self, x_pt: float, y_pt: float):
        unit = self.canvas_scene.settings.units
        dpi = self.canvas_scene.settings.target_dpi
        x_str = format_dimension(x_pt, unit, dpi)
        y_str = format_dimension(y_pt, unit, dpi)
        self.coord_lbl.setText(f"X: {x_str}  Y: {y_str}")

    def _on_zoom_changed(self, zoom: float):
        self.zoom_lbl.setText(f"{int(round(zoom * 100))}%")

    def _toggle_guides(self):
        active = self.guide_toggle_btn.isChecked()
        self.canvas_scene.show_guides = active
        self.guide_toggle_btn.setText(f"👁 Guides: {'ON' if active else 'OFF'}")
        self.canvas_scene.update()

    def _toggle_snap(self):
        active = self.snap_toggle_btn.isChecked()
        self.canvas_scene.snap_to_guides = active
        self.snap_toggle_btn.setText(f"🧲 Snap: {'ON' if active else 'OFF'}")

    def _on_add_image_clicked(self):
        if not self.canvas_scene.current_page:
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image to Insert",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.tif *.tiff)",
        )
        if file_path:
            self._insert_image_element(file_path, 100.0, 100.0)

    def _on_asset_dropped_on_canvas(self, file_path: str, x_pt: float, y_pt: float):
        self._insert_image_element(file_path, x_pt, y_pt)

    def _insert_image_element(self, file_path: str, x_pt: float, y_pt: float):
        p_name = Path(file_path).stem
        new_elem = ElementModel(
            element_id=f"elem_img_{int(x_pt)}",
            type=ElementType.IMAGE,
            x_pt=x_pt,
            y_pt=y_pt,
            width_pt=300.0,
            height_pt=300.0,
            asset_id=p_name,
        )

        target_layer = next((l for l in self.canvas_scene.current_page.layers if not l.locked), None)
        if not target_layer:
            target_layer = LayerModel(name="Illustrations", locked=False)
            self.canvas_scene.current_page.layers.append(target_layer)

        target_layer.elements.append(new_elem)
        item = self.canvas_scene._create_item_for_element(new_elem)
        if item:
            item.geometry_changed.connect(self.canvas_scene._on_item_geometry_changed)
            self.canvas_scene.addItem(item)
            self.canvas_scene.clearSelection()
            item.setSelected(True)
            self.canvas_scene.page_modified.emit(self.canvas_scene.current_page)

    def _on_add_text_clicked(self):
        if not self.canvas_scene.current_page:
            return

        new_elem = ElementModel(
            element_id=f"elem_txt_{len(self.canvas_scene._element_items) + 1}",
            type=ElementType.TEXT,
            x_pt=72.0,
            y_pt=72.0,
            width_pt=400.0,
            height_pt=40.0,
            text="New Title Text",
            font_family="Segoe UI",
            font_size_pt=26.0,
            bold=True,
            alignment="center",
            color="#000000",
        )

        target_layer = next((l for l in self.canvas_scene.current_page.layers if not l.locked), None)
        if not target_layer:
            target_layer = LayerModel(name="Text Layer", locked=False)
            self.canvas_scene.current_page.layers.append(target_layer)

        target_layer.elements.append(new_elem)
        item = self.canvas_scene._create_item_for_element(new_elem)
        if item:
            item.geometry_changed.connect(self.canvas_scene._on_item_geometry_changed)
            self.canvas_scene.addItem(item)
            self.canvas_scene.clearSelection()
            item.setSelected(True)
            self.canvas_scene.page_modified.emit(self.canvas_scene.current_page)

    def _on_add_shape_clicked(self):
        if not self.canvas_scene.current_page:
            return

        new_elem = ElementModel(
            element_id=f"elem_shp_{len(self.canvas_scene._element_items) + 1}",
            type=ElementType.SHAPE,
            x_pt=54.0,
            y_pt=54.0,
            width_pt=504.0,
            height_pt=684.0,
            stroke_color="#000000",
            stroke_width_pt=1.5,
            fill_color=None,
            corner_radius_pt=8.0,
        )

        target_layer = next((l for l in self.canvas_scene.current_page.layers if not l.locked), None)
        if not target_layer:
            target_layer = LayerModel(name="Shapes", locked=False)
            self.canvas_scene.current_page.layers.append(target_layer)

        target_layer.elements.append(new_elem)
        item = self.canvas_scene._create_item_for_element(new_elem)
        if item:
            item.geometry_changed.connect(self.canvas_scene._on_item_geometry_changed)
            self.canvas_scene.addItem(item)
            self.canvas_scene.clearSelection()
            item.setSelected(True)
            self.canvas_scene.page_modified.emit(self.canvas_scene.current_page)
