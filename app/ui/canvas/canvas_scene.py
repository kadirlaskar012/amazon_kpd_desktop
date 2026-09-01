"""
CanvasScene: QGraphicsScene managing physical page boundaries, layers,
KDP visual safety guides (Bleed, Trim, Safe Area, Gutter), and snapping.
"""

from typing import Optional, List, Dict, Tuple
from pathlib import Path

from PySide6.QtWidgets import QGraphicsScene, QGraphicsItem
from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPixmap

from app.core.document_model import BookSettings
from app.core.page_model import PageModel, ElementModel, ElementType
from app.core.units import in_to_pt, Unit
from app.ui.theme import Theme
from app.ui.canvas.canvas_items import (
    CanvasElementItem,
    ImageCanvasItem,
    TextCanvasItem,
    ShapeCanvasItem,
)


class CanvasScene(QGraphicsScene):
    element_selected = Signal(object)  # Emits ElementModel or None
    page_modified = Signal(object)      # Emits PageModel

    def __init__(self, settings: Optional[BookSettings] = None, parent=None):
        super().__init__(parent)
        self.settings = settings or BookSettings()
        self.current_page: Optional[PageModel] = None
        self.current_page_index: int = 0
        self.project_dir: Optional[Path] = None

        # Guide visibility & snapping flags
        self.show_guides: bool = True
        self.snap_to_guides: bool = True
        self.snap_threshold_pt: float = 4.0

        self._element_items: Dict[str, CanvasElementItem] = {}
        self.selectionChanged.connect(self._on_selection_changed)

        self._update_scene_rect()

    def set_settings(self, settings: BookSettings):
        self.settings = settings
        self._update_scene_rect()
        self.update()

    def set_project_dir(self, p_dir: Optional[Path]):
        self.project_dir = p_dir

    def _update_scene_rect(self):
        # Scene padding around page for comfortable viewing
        pad = 72.0  # 1 inch margin
        w = self.settings.total_width_with_bleed_pt
        h = self.settings.total_height_with_bleed_pt
        self.setSceneRect(-pad, -pad, w + (pad * 2), h + (pad * 2))

    def load_page(self, page: Optional[PageModel], page_index: int = 0):
        """Clear scene and populate items from PageModel layers."""
        self.clear()
        self._element_items.clear()
        self.current_page = page
        self.current_page_index = page_index

        if not page:
            self.update()
            return

        # Flatten elements from layers in order
        for layer in page.layers:
            if not layer.visible:
                continue
            for elem in layer.elements:
                item = self._create_item_for_element(elem)
                if item:
                    item.geometry_changed.connect(self._on_item_geometry_changed)
                    self.addItem(item)
                    self._element_items[elem.element_id] = item

        self.update()

    def _create_item_for_element(self, elem: ElementModel) -> Optional[CanvasElementItem]:
        if elem.type == ElementType.IMAGE:
            pixmap = None
            if elem.asset_id and self.project_dir:
                # Attempt to load asset image from assets folder
                asset_path = self.project_dir / "assets" / f"{elem.asset_id}"
                if not asset_path.exists():
                    # Check common extensions
                    for ext in [".png", ".jpg", ".jpeg", ".webp"]:
                        cand = self.project_dir / "assets" / f"{elem.asset_id}{ext}"
                        if cand.exists():
                            asset_path = cand
                            break
                if asset_path.exists():
                    pixmap = QPixmap(str(asset_path))

            return ImageCanvasItem(elem, pixmap)

        elif elem.type == ElementType.TEXT:
            return TextCanvasItem(elem)

        elif elem.type in (ElementType.SHAPE, ElementType.BORDER):
            return ShapeCanvasItem(elem)

        return None

    def _on_item_geometry_changed(self, item: CanvasElementItem):
        if self.current_page:
            self.page_modified.emit(self.current_page)

    def _on_selection_changed(self):
        selected_items = self.selectedItems()
        if selected_items and isinstance(selected_items[0], CanvasElementItem):
            self.element_selected.emit(selected_items[0].model)
        else:
            self.element_selected.emit(None)

    def drawBackground(self, painter: QPainter, rect: QRectF):
        painter.save()
        # Workspace background
        painter.fillRect(rect, QColor(Theme.BG_DARK))

        # Page Dimensions
        trim_w = self.settings.trim_width_pt
        trim_h = self.settings.trim_height_pt

        page_rect = QRectF(0, 0, trim_w, trim_h)

        # Draw subtle drop shadow behind page
        shadow_rect = page_rect.translated(4.0, 4.0)
        painter.fillRect(shadow_rect, QColor(0, 0, 0, 80))

        # Draw White Paper Base
        painter.fillRect(page_rect, QColor("#ffffff"))

        # Draw Trim Border (crisp black cut line)
        trim_pen = QPen(QColor("#111827"), 1.0, Qt.SolidLine)
        trim_pen.setCosmetic(True)
        painter.setPen(trim_pen)
        painter.drawRect(page_rect)

        # Draw Bleed Box if active
        if self.settings.has_bleed:
            bleed_pt = self.settings.bleed_pt
            bleed_rect = QRectF(0, -bleed_pt, trim_w + bleed_pt, trim_h + (bleed_pt * 2.0))
            bleed_pen = QPen(QColor("#ef4444"), 1.0, Qt.DashLine)
            bleed_pen.setCosmetic(True)
            painter.setPen(bleed_pen)
            painter.drawRect(bleed_rect)

        # Draw KDP Safety & Gutter Guides
        if self.show_guides:
            self._draw_guides(painter, trim_w, trim_h)

        painter.restore()

    def _draw_guides(self, painter: QPainter, page_w: float, page_h: float):
        margins = self.settings.margins
        is_odd = (self.current_page_index % 2 == 0)  # 0-indexed: Page 1 is odd

        # Inside Gutter alternates left (odd) and right (even)
        left_m = margins.inside_pt if is_odd else margins.outside_pt
        right_m = margins.outside_pt if is_odd else margins.inside_pt
        top_m = margins.top_pt
        bot_m = margins.bottom_pt

        # 1. Inside Binding Gutter (Translucent Blue zone)
        gutter_w = margins.inside_pt
        if is_odd:
            gutter_rect = QRectF(0, 0, gutter_w, page_h)
        else:
            gutter_rect = QRectF(page_w - gutter_w, 0, gutter_w, page_h)

        gutter_brush = QBrush(QColor(14, 165, 233, 28))  # Light Sky Blue 10%
        painter.fillRect(gutter_rect, gutter_brush)

        gutter_pen = QPen(QColor(14, 165, 233, 140), 1.0, Qt.DashDotLine)
        gutter_pen.setCosmetic(True)
        painter.setPen(gutter_pen)
        if is_odd:
            painter.drawLine(QPointF(gutter_w, 0), QPointF(gutter_w, page_h))
        else:
            painter.drawLine(QPointF(page_w - gutter_w, 0), QPointF(page_w - gutter_w, page_h))

        # 2. Safe Area Margin Box (Green dashed)
        safe_x = left_m
        safe_y = top_m
        safe_w = max(0.0, page_w - (left_m + right_m))
        safe_h = max(0.0, page_h - (top_m + bot_m))
        safe_rect = QRectF(safe_x, safe_y, safe_w, safe_h)

        safe_pen = QPen(QColor("#22c55e"), 1.0, Qt.DashLine)
        safe_pen.setCosmetic(True)
        painter.setPen(safe_pen)
        painter.drawRect(safe_rect)

        # 3. Centerlines (Subtle gray crosshair)
        center_pen = QPen(QColor(200, 200, 200, 100), 0.5, Qt.DotLine)
        center_pen.setCosmetic(True)
        painter.setPen(center_pen)
        painter.drawLine(QPointF(page_w / 2.0, 0), QPointF(page_w / 2.0, page_h))
        painter.drawLine(QPointF(0, page_h / 2.0), QPointF(page_w, page_h / 2.0))

    def snap_coordinate(self, point: QPointF) -> QPointF:
        """Snap coordinate to nearby guides (margins, centerlines, page edges)."""
        if not self.snap_to_guides:
            return point

        x = point.x()
        y = point.y()
        thresh = self.snap_threshold_pt

        page_w = self.settings.trim_width_pt
        page_h = self.settings.trim_height_pt
        is_odd = (self.current_page_index % 2 == 0)

        left_m = self.settings.margins.inside_pt if is_odd else self.settings.margins.outside_pt
        right_m = self.settings.margins.outside_pt if is_odd else self.settings.margins.inside_pt

        # X snap targets: 0, left_m, center, page_w - right_m, page_w
        x_targets = [0.0, left_m, page_w / 2.0, page_w - right_m, page_w]
        for tx in x_targets:
            if abs(x - tx) <= thresh:
                x = tx
                break

        # Y snap targets: 0, top_m, center, page_h - bot_m, page_h
        y_targets = [0.0, self.settings.margins.top_pt, page_h / 2.0, page_h - self.settings.margins.bottom_pt, page_h]
        for ty in y_targets:
            if abs(y - ty) <= thresh:
                y = ty
                break

        return QPointF(x, y)
