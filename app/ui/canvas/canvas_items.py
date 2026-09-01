"""
Interactive canvas items for images, text, and shapes with 8-point resize handles,
rotation, aspect ratio locking, and physical point coordinates.
"""

import math
from typing import Optional, Tuple, Dict, Any

from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsRectItem,
    QStyleOptionGraphicsItem,
    QWidget,
)
from PySide6.QtCore import Qt, QRectF, QPointF, Signal, QSizeF
from PySide6.QtGui import (
    QPainter,
    QPen,
    QBrush,
    QColor,
    QFont,
    QFontMetricsF,
    QPixmap,
    QImage,
    QPainterPath,
    QCursor,
)

from app.core.page_model import ElementModel, ElementType
from app.core.units import in_to_pt, pt_to_in, format_dimension, Unit
from app.ui.theme import Theme


class HandleType:
    NONE = 0
    TOP_LEFT = 1
    TOP = 2
    TOP_RIGHT = 3
    RIGHT = 4
    BOTTOM_RIGHT = 5
    BOTTOM = 6
    BOTTOM_LEFT = 7
    LEFT = 8
    ROTATE = 9


HANDLE_SIZE = 8.0  # Points in canvas space


class CanvasElementItem(QGraphicsObject):
    """
    Base interactive canvas item with 8-point resize handles and selection bounds.
    """
    geometry_changed = Signal(object)  # Emits self
    selection_changed = Signal(object)

    def __init__(self, model: ElementModel, parent: Optional[QGraphicsItem] = None):
        super().__init__(parent)
        self.model = model

        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)

        self._active_handle = HandleType.NONE
        self._drag_start_pos = QPointF()
        self._initial_rect = QRectF(model.x_pt, model.y_pt, model.width_pt, model.height_pt)
        self._initial_pos = QPointF(model.x_pt, model.y_pt)

        # Apply initial model coordinates
        self.setPos(model.x_pt, model.y_pt)
        self.setRotation(model.rotation_deg)
        self.setOpacity(model.opacity)
        self.setVisible(model.visible)
        if model.locked:
            self.setFlag(QGraphicsItem.ItemIsMovable, False)

    def boundingRect(self) -> QRectF:
        pad = HANDLE_SIZE
        return QRectF(
            -pad,
            -pad - 16.0,  # Room for top rotation handle
            self.model.width_pt + (pad * 2),
            self.model.height_pt + (pad * 2) + 16.0,
        )

    def get_element_rect(self) -> QRectF:
        return QRectF(0, 0, self.model.width_pt, self.model.height_pt)

    def get_handle_rect(self, handle_type: int) -> QRectF:
        w = self.model.width_pt
        h = self.model.height_pt
        hs = HANDLE_SIZE
        half = hs / 2.0

        if handle_type == HandleType.TOP_LEFT:
            return QRectF(-half, -half, hs, hs)
        elif handle_type == HandleType.TOP:
            return QRectF((w / 2.0) - half, -half, hs, hs)
        elif handle_type == HandleType.TOP_RIGHT:
            return QRectF(w - half, -half, hs, hs)
        elif handle_type == HandleType.RIGHT:
            return QRectF(w - half, (h / 2.0) - half, hs, hs)
        elif handle_type == HandleType.BOTTOM_RIGHT:
            return QRectF(w - half, h - half, hs, hs)
        elif handle_type == HandleType.BOTTOM:
            return QRectF((w / 2.0) - half, h - half, hs, hs)
        elif handle_type == HandleType.BOTTOM_LEFT:
            return QRectF(-half, h - half, hs, hs)
        elif handle_type == HandleType.LEFT:
            return QRectF(-half, (h / 2.0) - half, hs, hs)
        elif handle_type == HandleType.ROTATE:
            return QRectF((w / 2.0) - half, -16.0 - half, hs, hs)
        return QRectF()

    def get_handle_at(self, pt: QPointF) -> int:
        if not self.isSelected() or self.model.locked:
            return HandleType.NONE

        for h_type in range(1, 10):
            rect = self.get_handle_rect(h_type)
            if rect.contains(pt):
                return h_type
        return HandleType.NONE

    def hoverMoveEvent(self, event):
        if self.isSelected() and not self.model.locked:
            handle = self.get_handle_at(event.pos())
            cursor = self._get_cursor_for_handle(handle)
            self.setCursor(cursor)
        else:
            self.setCursor(Qt.ArrowCursor if self.model.locked else Qt.SizeAllCursor)
        super().hoverMoveEvent(event)

    def _get_cursor_for_handle(self, handle: int) -> Qt.CursorShape:
        if handle in (HandleType.TOP_LEFT, HandleType.BOTTOM_RIGHT):
            return Qt.SizeFDiagCursor
        elif handle in (HandleType.TOP_RIGHT, HandleType.BOTTOM_LEFT):
            return Qt.SizeBDiagCursor
        elif handle in (HandleType.TOP, HandleType.BOTTOM):
            return Qt.SizeVerCursor
        elif handle in (HandleType.LEFT, HandleType.RIGHT):
            return Qt.SizeHorCursor
        elif handle == HandleType.ROTATE:
            return Qt.CrossCursor
        return Qt.SizeAllCursor

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.model.locked:
            handle = self.get_handle_at(event.pos())
            if handle != HandleType.NONE:
                self._active_handle = handle
                self._drag_start_pos = event.scenePos()
                self._initial_rect = QRectF(self.pos().x(), self.pos().y(), self.model.width_pt, self.model.height_pt)
                event.accept()
                return
        self._active_handle = HandleType.NONE
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._active_handle != HandleType.NONE and not self.model.locked:
            delta = event.scenePos() - self._drag_start_pos
            dx = delta.x()
            dy = delta.y()

            init_x = self._initial_rect.x()
            init_y = self._initial_rect.y()
            init_w = self._initial_rect.width()
            init_h = self._initial_rect.height()

            min_size = 12.0

            if self._active_handle == HandleType.BOTTOM_RIGHT:
                new_w = max(min_size, init_w + dx)
                new_h = max(min_size, init_h + dy)
                if self.model.maintain_aspect_ratio and init_h > 0:
                    aspect = init_w / init_h
                    new_h = new_w / aspect
                self.model.width_pt = new_w
                self.model.height_pt = new_h

            elif self._active_handle == HandleType.RIGHT:
                self.model.width_pt = max(min_size, init_w + dx)

            elif self._active_handle == HandleType.BOTTOM:
                self.model.height_pt = max(min_size, init_h + dy)

            elif self._active_handle == HandleType.LEFT:
                new_w = max(min_size, init_w - dx)
                new_x = init_x + (init_w - new_w)
                self.model.width_pt = new_w
                self.setPos(new_x, self.y())
                self.model.x_pt = new_x

            elif self._active_handle == HandleType.TOP:
                new_h = max(min_size, init_h - dy)
                new_y = init_y + (init_h - new_h)
                self.model.height_pt = new_h
                self.setPos(self.x(), new_y)
                self.model.y_pt = new_y

            elif self._active_handle == HandleType.TOP_LEFT:
                new_w = max(min_size, init_w - dx)
                new_h = max(min_size, init_h - dy)
                if self.model.maintain_aspect_ratio and init_h > 0:
                    aspect = init_w / init_h
                    new_h = new_w / aspect
                new_x = init_x + (init_w - new_w)
                new_y = init_y + (init_h - new_h)
                self.model.width_pt = new_w
                self.model.height_pt = new_h
                self.setPos(new_x, new_y)
                self.model.x_pt = new_x
                self.model.y_pt = new_y

            elif self._active_handle == HandleType.ROTATE:
                # Calculate angle between item center and current mouse
                center = self.mapToScene(QPointF(init_w / 2.0, init_h / 2.0))
                diff = event.scenePos() - center
                angle_deg = math.degrees(math.atan2(diff.y(), diff.x())) + 90.0
                # Snap to 0, 90, 180, 270 if close
                for snap_angle in (0.0, 90.0, 180.0, 270.0, 360.0):
                    if abs(angle_deg - snap_angle) < 4.0:
                        angle_deg = snap_angle % 360.0
                        break
                self.setRotation(angle_deg)
                self.model.rotation_deg = angle_deg

            self.prepareGeometryChange()
            self.update()
            self.geometry_changed.emit(self)
            event.accept()
            return

        super().mouseMoveEvent(event)
        # Update model position from item pos
        if self.pos().x() != self.model.x_pt or self.pos().y() != self.model.y_pt:
            self.model.x_pt = self.pos().x()
            self.model.y_pt = self.pos().y()
            self.geometry_changed.emit(self)

    def mouseReleaseEvent(self, event):
        self._active_handle = HandleType.NONE
        super().mouseReleaseEvent(event)
        self.geometry_changed.emit(self)

    def paint_selection_handles(self, painter: QPainter):
        """Draw interactive selection rectangle and 8-point resize handles."""
        if not self.isSelected():
            return

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)

        w = self.model.width_pt
        h = self.model.height_pt

        # Selection border (Primary accent color)
        sel_pen = QPen(QColor(Theme.PRIMARY), 1.5, Qt.SolidLine)
        sel_pen.setCosmetic(True)
        painter.setPen(sel_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(QRectF(0, 0, w, h))

        # Rotate guide line
        painter.setPen(QPen(QColor(Theme.PRIMARY), 1.0, Qt.DashLine))
        painter.drawLine(QPointF(w / 2.0, 0), QPointF(w / 2.0, -16.0))

        # Handles (White filled squares with primary stroke)
        handle_pen = QPen(QColor(Theme.PRIMARY), 1.5)
        handle_pen.setCosmetic(True)
        handle_brush = QBrush(QColor("#ffffff"))
        painter.setPen(handle_pen)
        painter.setBrush(handle_brush)

        for h_type in range(1, 9):
            rect = self.get_handle_rect(h_type)
            painter.drawRect(rect)

        # Rotate handle (Circle)
        rot_rect = self.get_handle_rect(HandleType.ROTATE)
        painter.drawEllipse(rot_rect)

        painter.restore()


class ImageCanvasItem(CanvasElementItem):
    """
    Renders bitmap images (reference previews & coloring illustrations).
    """

    def __init__(self, model: ElementModel, pixmap: Optional[QPixmap] = None, parent: Optional[QGraphicsItem] = None):
        super().__init__(model, parent)
        self._pixmap = pixmap

    def set_pixmap(self, pixmap: Optional[QPixmap]):
        self._pixmap = pixmap
        self.update()

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = None):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        w = self.model.width_pt
        h = self.model.height_pt
        rect = QRectF(0, 0, w, h)

        if self._pixmap and not self._pixmap.isNull():
            painter.drawPixmap(rect.toRect(), self._pixmap)
        else:
            # Placeholder styling for image slot
            painter.setPen(QPen(QColor(Theme.BORDER), 1.5, Qt.DashLine))
            painter.setBrush(QBrush(QColor(Theme.BG_CARD)))
            painter.drawRoundedRect(rect, 4.0, 4.0)

            # Draw camera / image icon placeholder
            painter.setPen(QPen(QColor(Theme.TEXT_MUTED), 1.0))
            painter.setFont(QFont("Segoe UI", 10))
            text = "📷 Drop or Assign Image" if not self.model.asset_id else f"🖼 {self.model.asset_id}"
            painter.drawText(rect, Qt.AlignCenter, text)

        self.paint_selection_handles(painter)
        painter.restore()


class TextCanvasItem(CanvasElementItem):
    """
    Renders vector typography with bold, font size, alignment, and auto-wrapping.
    """

    def __init__(self, model: ElementModel, parent: Optional[QGraphicsItem] = None):
        super().__init__(model, parent)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = None):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)

        w = self.model.width_pt
        h = self.model.height_pt
        rect = QRectF(0, 0, w, h)

        text = self.model.text or "Double Click to Edit Text"
        font_family = self.model.font_family or "Segoe UI"
        font_size = self.model.font_size_pt or 24.0

        font = QFont(font_family)
        font.setPointSizeF(font_size)
        font.setBold(self.model.bold)
        font.setItalic(self.model.italic)
        painter.setFont(font)

        # Text Color
        try:
            color = QColor(self.model.color or "#000000")
        except Exception:
            color = QColor("#000000")
        painter.setPen(QPen(color))

        # Alignment
        align_map = {
            "left": Qt.AlignLeft | Qt.AlignVCenter,
            "center": Qt.AlignHCenter | Qt.AlignVCenter,
            "right": Qt.AlignRight | Qt.AlignVCenter,
        }
        align_flags = align_map.get(self.model.alignment, Qt.AlignCenter)

        painter.drawText(rect, align_flags | Qt.TextWordWrap, text)

        self.paint_selection_handles(painter)
        painter.restore()


class ShapeCanvasItem(CanvasElementItem):
    """
    Renders vector borders, frames, and shapes.
    """

    def __init__(self, model: ElementModel, parent: Optional[QGraphicsItem] = None):
        super().__init__(model, parent)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = None):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)

        w = self.model.width_pt
        h = self.model.height_pt
        rect = QRectF(0, 0, w, h)

        # Stroke Pen
        stroke_color = QColor(self.model.stroke_color or "#000000")
        pen = QPen(stroke_color, max(0.5, self.model.stroke_width_pt))
        painter.setPen(pen)

        # Fill Brush
        if self.model.fill_color:
            painter.setBrush(QBrush(QColor(self.model.fill_color)))
        else:
            painter.setBrush(Qt.NoBrush)

        radius = self.model.corner_radius_pt
        if radius > 0:
            painter.drawRoundedRect(rect, radius, radius)
        else:
            painter.drawRect(rect)

        self.paint_selection_handles(painter)
        painter.restore()
