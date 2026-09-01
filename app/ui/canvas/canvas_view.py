"""
CanvasView: QGraphicsView supporting smooth pan/zoom, keyboard shortcuts (nudge, duplicate, delete),
and drag-and-drop image import.
"""

from pathlib import Path
from typing import Optional, List

from PySide6.QtWidgets import QGraphicsView, QGraphicsItem
from PySide6.QtCore import Qt, QPointF, Signal, QRectF, QMimeData
from PySide6.QtGui import (
    QPainter,
    QWheelEvent,
    QMouseEvent,
    QKeyEvent,
    QDragEnterEvent,
    QDropEvent,
    QCursor,
)

from app.core.units import convert_from_points, Unit
from app.core.page_model import ElementModel, ElementType
from app.ui.canvas.canvas_scene import CanvasScene
from app.ui.canvas.canvas_items import CanvasElementItem, ImageCanvasItem


class CanvasView(QGraphicsView):
    cursor_position_changed = Signal(float, float)  # Emits (x_pt, y_pt)
    zoom_changed = Signal(float)                    # Emits zoom factor (1.0 = 100%)
    asset_dropped = Signal(str, float, float)       # Emits (file_path, x_pt, y_pt)

    def __init__(self, scene: CanvasScene, parent=None):
        super().__init__(scene, parent)
        self.canvas_scene = scene

        # Render options for ultra crisp vector graphics & anti-aliased bitmap scaling
        self.setRenderHints(
            QPainter.Antialiasing
            | QPainter.SmoothPixmapTransform
            | QPainter.TextAntialiasing
        )
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setAcceptDrops(True)
        self.setFocusPolicy(Qt.StrongFocus)

        self._zoom_level: float = 1.0
        self._is_panning: bool = False
        self._pan_start_pos = QPointF()
        self._space_pressed: bool = False

        # Clipboard for copy/paste
        self._copied_element: Optional[ElementModel] = None

    @property
    def zoom_level(self) -> float:
        return self._zoom_level

    def set_zoom(self, zoom: float):
        zoom = max(0.1, min(10.0, zoom))
        factor = zoom / self._zoom_level
        self._zoom_level = zoom
        self.scale(factor, factor)
        self.zoom_changed.emit(self._zoom_level)

    def zoom_in(self):
        self.set_zoom(self._zoom_level * 1.2)

    def zoom_out(self):
        self.set_zoom(self._zoom_level / 1.2)

    def zoom_to_fit(self):
        """Fit the entire page bounding rectangle inside viewport."""
        page_rect = QRectF(
            0,
            0,
            self.canvas_scene.settings.trim_width_pt,
            self.canvas_scene.settings.trim_height_pt,
        )
        self.fitInView(page_rect.adjusted(-20, -20, 20, 20), Qt.KeepAspectRatio)
        # Compute zoom level from transform
        self._zoom_level = self.transform().m11()
        self.zoom_changed.emit(self._zoom_level)

    def zoom_to_actual_size(self):
        self.set_zoom(1.0)

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.ControlModifier:
            # Ctrl + Wheel: Zoom
            delta = event.angleDelta().y()
            factor = 1.15 if delta > 0 else 1.0 / 1.15
            self.set_zoom(self._zoom_level * factor)
            event.accept()
        else:
            super().wheelEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MiddleButton or (event.button() == Qt.LeftButton and self._space_pressed):
            self._is_panning = True
            self._pan_start_pos = event.position()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        scene_pos = self.mapToScene(event.pos())
        self.cursor_position_changed.emit(scene_pos.x(), scene_pos.y())

        if self._is_panning:
            delta = event.position() - self._pan_start_pos
            self._pan_start_pos = event.position()
            self.horizontalScrollBar().setValue(int(self.horizontalScrollBar().value() - delta.x()))
            self.verticalScrollBar().setValue(int(self.verticalScrollBar().value() - delta.y()))
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self._is_panning:
            self._is_panning = False
            self.setCursor(Qt.ArrowCursor if not self._space_pressed else Qt.OpenHandCursor)
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space and not self._space_pressed:
            self._space_pressed = True
            self.setCursor(Qt.OpenHandCursor)
            event.accept()
            return

        selected_items = self.canvas_scene.selectedItems()
        if selected_items:
            item = selected_items[0]
            if isinstance(item, CanvasElementItem) and not item.model.locked:
                step = 10.0 if event.modifiers() & Qt.ShiftModifier else 1.0

                # Nudge with arrow keys
                if event.key() == Qt.Key_Left:
                    item.setPos(item.x() - step, item.y())
                    item.model.x_pt = item.x()
                    self.canvas_scene._on_item_geometry_changed(item)
                    event.accept()
                    return
                elif event.key() == Qt.Key_Right:
                    item.setPos(item.x() + step, item.y())
                    item.model.x_pt = item.x()
                    self.canvas_scene._on_item_geometry_changed(item)
                    event.accept()
                    return
                elif event.key() == Qt.Key_Up:
                    item.setPos(item.x(), item.y() - step)
                    item.model.y_pt = item.y()
                    self.canvas_scene._on_item_geometry_changed(item)
                    event.accept()
                    return
                elif event.key() == Qt.Key_Down:
                    item.setPos(item.x(), item.y() + step)
                    item.model.y_pt = item.y()
                    self.canvas_scene._on_item_geometry_changed(item)
                    event.accept()
                    return

                # Delete / Backspace
                elif event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
                    self._delete_selected_element()
                    event.accept()
                    return

                # Ctrl + D: Duplicate
                elif event.key() == Qt.Key_D and event.modifiers() & Qt.ControlModifier:
                    self._duplicate_selected_element()
                    event.accept()
                    return

                # Ctrl + C: Copy
                elif event.key() == Qt.Key_C and event.modifiers() & Qt.ControlModifier:
                    self._copied_element = ElementModel.from_dict(item.model.to_dict())
                    event.accept()
                    return

        # Ctrl + V: Paste
        if event.key() == Qt.Key_V and event.modifiers() & Qt.ControlModifier:
            self._paste_copied_element()
            event.accept()
            return

        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space:
            self._space_pressed = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
        super().keyReleaseEvent(event)

    def _delete_selected_element(self):
        selected_items = self.canvas_scene.selectedItems()
        if not selected_items or not self.canvas_scene.current_page:
            return

        for item in selected_items:
            if isinstance(item, CanvasElementItem):
                elem_id = item.model.element_id
                # Remove from page layers
                for layer in self.canvas_scene.current_page.layers:
                    layer.elements = [e for e in layer.elements if e.element_id != elem_id]
                self.canvas_scene.removeItem(item)

        self.canvas_scene.page_modified.emit(self.canvas_scene.current_page)

    def _duplicate_selected_element(self):
        selected_items = self.canvas_scene.selectedItems()
        if not selected_items or not self.canvas_scene.current_page:
            return

        item = selected_items[0]
        if isinstance(item, CanvasElementItem):
            # Create clone model offset by +18 pt
            clone_dict = item.model.to_dict()
            clone_dict["element_id"] = f"elem_dup_{int(item.x())}"
            clone_dict["x_pt"] = item.model.x_pt + 18.0
            clone_dict["y_pt"] = item.model.y_pt + 18.0
            new_model = ElementModel.from_dict(clone_dict)

            # Add to first unlocked layer or create one
            target_layer = next((l for l in self.canvas_scene.current_page.layers if not l.locked), None)
            if target_layer:
                target_layer.elements.append(new_model)
                new_item = self.canvas_scene._create_item_for_element(new_model)
                if new_item:
                    new_item.geometry_changed.connect(self.canvas_scene._on_item_geometry_changed)
                    self.canvas_scene.addItem(new_item)
                    self.canvas_scene.clearSelection()
                    new_item.setSelected(True)
                    self.canvas_scene.page_modified.emit(self.canvas_scene.current_page)

    def _paste_copied_element(self):
        if not self._copied_element or not self.canvas_scene.current_page:
            return
        clone_dict = self._copied_element.to_dict()
        clone_dict["x_pt"] += 18.0
        clone_dict["y_pt"] += 18.0
        new_model = ElementModel.from_dict(clone_dict)

        target_layer = next((l for l in self.canvas_scene.current_page.layers if not l.locked), None)
        if target_layer:
            target_layer.elements.append(new_model)
            new_item = self.canvas_scene._create_item_for_element(new_model)
            if new_item:
                new_item.geometry_changed.connect(self.canvas_scene._on_item_geometry_changed)
                self.canvas_scene.addItem(new_item)
                self.canvas_scene.clearSelection()
                new_item.setSelected(True)
                self.canvas_scene.page_modified.emit(self.canvas_scene.current_page)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if Path(file_path).suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"):
                    scene_pos = self.mapToScene(event.position().toPoint())
                    self.asset_dropped.emit(file_path, scene_pos.x(), scene_pos.y())
            event.acceptProposedAction()
        else:
            super().dropEvent(event)
