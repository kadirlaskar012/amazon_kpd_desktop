"""
Unit tests for CanvasScene, CanvasView, CanvasElementItem, snapping, and property inspector.
"""

import os
from pathlib import Path
import tempfile
import pytest

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QPointF, QRectF

from app.core.document_model import BookSettings, MarginSettings
from app.core.page_model import PageModel, LayerModel, ElementModel, ElementType
from app.core.units import in_to_pt
from app.ui.canvas.canvas_scene import CanvasScene
from app.ui.canvas.canvas_items import CanvasElementItem, ImageCanvasItem, TextCanvasItem, ShapeCanvasItem, HandleType
from app.ui.canvas.canvas_view import CanvasView
from app.ui.properties_panel import PropertiesPanel
from app.ui.pages_panel import PagesPanel


@pytest.fixture(scope="session")
def qapp():
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def test_canvas_scene_initialization(qapp):
    settings = BookSettings(
        trim_width_pt=in_to_pt(8.5),
        trim_height_pt=in_to_pt(11.0),
        has_bleed=True,
    )
    scene = CanvasScene(settings)
    assert scene.settings.trim_width_pt == 612.0
    assert scene.settings.trim_height_pt == 792.0
    assert scene.show_guides is True
    assert scene.snap_to_guides is True


def test_canvas_scene_load_page_and_items(qapp):
    settings = BookSettings()
    scene = CanvasScene(settings)

    page = PageModel(
        page_id="p1",
        page_number=1,
        title="Test Lion",
        layers=[
            LayerModel(
                layer_id="l1",
                name="Main",
                elements=[
                    ElementModel(
                        element_id="img_1",
                        type=ElementType.IMAGE,
                        x_pt=100.0,
                        y_pt=100.0,
                        width_pt=300.0,
                        height_pt=300.0,
                    ),
                    ElementModel(
                        element_id="txt_1",
                        type=ElementType.TEXT,
                        x_pt=100.0,
                        y_pt=450.0,
                        width_pt=300.0,
                        height_pt=40.0,
                        text="Test Lion",
                    ),
                ],
            )
        ],
    )

    scene.load_page(page, 0)
    assert len(scene.items()) == 2
    assert "img_1" in scene._element_items
    assert "txt_1" in scene._element_items

    img_item = scene._element_items["img_1"]
    assert isinstance(img_item, ImageCanvasItem)
    assert img_item.pos().x() == 100.0
    assert img_item.pos().y() == 100.0


def test_canvas_item_handle_detection(qapp):
    model = ElementModel(
        element_id="e1",
        type=ElementType.IMAGE,
        x_pt=50.0,
        y_pt=50.0,
        width_pt=200.0,
        height_pt=200.0,
    )
    item = ImageCanvasItem(model)
    item.setSelected(True)

    # Test handle detection at corners
    # Top-Left handle at (0, 0) in item space
    h_tl = item.get_handle_at(QPointF(0, 0))
    assert h_tl == HandleType.TOP_LEFT

    # Bottom-Right handle at (200, 200)
    h_br = item.get_handle_at(QPointF(200, 200))
    assert h_br == HandleType.BOTTOM_RIGHT


def test_canvas_snapping(qapp):
    settings = BookSettings(
        trim_width_pt=612.0,
        trim_height_pt=792.0,
        margins=MarginSettings(inside_pt=36.0, outside_pt=27.0, top_pt=27.0, bottom_pt=27.0),
    )
    scene = CanvasScene(settings)
    scene.snap_to_guides = True
    scene.snap_threshold_pt = 4.0

    # Point near inside margin (36.0) -> (37.5, 100) should snap to 36.0
    snapped = scene.snap_coordinate(QPointF(37.5, 100.0))
    assert snapped.x() == 36.0

    # Point far from any guide -> should remain unchanged
    far = scene.snap_coordinate(QPointF(150.0, 150.0))
    assert far.x() == 150.0
    assert far.y() == 150.0


def test_properties_panel_binding(qapp):
    settings = BookSettings()
    panel = PropertiesPanel(settings)

    model = ElementModel(
        element_id="txt_test",
        type=ElementType.TEXT,
        x_pt=72.0,
        y_pt=144.0,
        width_pt=288.0,
        height_pt=36.0,
        text="Hello World",
        bold=True,
    )

    panel.set_element(model)
    assert panel.isEnabled()
    assert panel.text_content_edit.text() == "Hello World"
    assert panel.bold_btn.isChecked() is True

    # Change text in panel
    panel.text_content_edit.setText("Updated Title")
    assert model.text == "Updated Title"
