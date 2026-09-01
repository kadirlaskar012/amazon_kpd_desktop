"""
Script to capture pixel-perfect screenshots of the live UI screens:
1. Dashboard View
2. Book Settings View
3. Canvas Editor View with sample coloring page & elements
4. New Project Wizard Dialog
"""

import os
import sys
from pathlib import Path

# Ensure root workspace is in sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Enable offscreen rendering for headless screenshot capture
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont, QPixmap

from app.ui.theme import Theme
from app.ui.main_window import MainWindow
from app.ui.project_setup import ProjectSetupDialog
from app.core.project_manager import ProjectManager
from app.core.document_model import BookType, KDP_TRIM_PRESETS
from app.core.page_model import PageModel, LayerModel, ElementModel, ElementType


def capture_screenshots():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(Theme.get_stylesheet())

    output_dir = root_dir / "docs" / "screenshots"
    output_dir.mkdir(parents=True, exist_ok=True)

    pm = ProjectManager.get_instance()

    # 1. Initialize Sample Project for Realistic Preview
    sample_proj_dir = root_dir / "sample_project"
    sample_doc = pm.create_new_project(
        name="Animal Kingdom Coloring Book",
        location_dir=sample_proj_dir,
        author="Creative Kids Press",
        book_type=BookType.COLORING_BOOK,
        trim_preset=KDP_TRIM_PRESETS[0],  # 8.5 x 11 in
        has_bleed=True,
    )

    # Populate Sample Pages with elements
    page1 = PageModel(
        page_id="page_001",
        page_number=1,
        title="Cute Lion",
        layers=[
            LayerModel(
                layer_id="layer_ref",
                name="Reference Preview",
                elements=[
                    ElementModel(
                        element_id="ref_lion",
                        type=ElementType.IMAGE,
                        x_pt=230.0,
                        y_pt=45.0,
                        width_pt=150.0,
                        height_pt=110.0,
                        asset_id="lion_ref_color.png",
                    )
                ],
            ),
            LayerModel(
                layer_id="layer_main",
                name="Coloring Area",
                elements=[
                    ElementModel(
                        element_id="main_lion",
                        type=ElementType.IMAGE,
                        x_pt=54.0,
                        y_pt=165.0,
                        width_pt=504.0,
                        height_pt=480.0,
                        asset_id="lion_line_art_bw.png",
                    )
                ],
            ),
            LayerModel(
                layer_id="layer_title",
                name="Title",
                elements=[
                    ElementModel(
                        element_id="title_lion",
                        type=ElementType.TEXT,
                        x_pt=54.0,
                        y_pt=665.0,
                        width_pt=504.0,
                        height_pt=40.0,
                        text="CUTE LION",
                        font_family="Segoe UI",
                        font_size_pt=28.0,
                        bold=True,
                        alignment="center",
                        color="#111827",
                    )
                ],
            ),
            LayerModel(
                layer_id="layer_border",
                name="Decorative Frame",
                elements=[
                    ElementModel(
                        element_id="frame_01",
                        type=ElementType.BORDER,
                        x_pt=36.0,
                        y_pt=36.0,
                        width_pt=540.0,
                        height_pt=720.0,
                        stroke_color="#111827",
                        stroke_width_pt=1.5,
                        corner_radius_pt=10.0,
                    )
                ],
            ),
        ],
    )

    page2 = PageModel(
        page_id="page_002",
        page_number=2,
        title="Baby Elephant",
        layers=[
            LayerModel(
                layer_id="layer_main2",
                name="Coloring Area",
                elements=[
                    ElementModel(
                        element_id="main_elephant",
                        type=ElementType.IMAGE,
                        x_pt=54.0,
                        y_pt=100.0,
                        width_pt=504.0,
                        height_pt=520.0,
                        asset_id="elephant_line_art.png",
                    )
                ],
            ),
            LayerModel(
                layer_id="layer_title2",
                name="Title",
                elements=[
                    ElementModel(
                        element_id="title_elephant",
                        type=ElementType.TEXT,
                        x_pt=54.0,
                        y_pt=640.0,
                        width_pt=504.0,
                        height_pt=40.0,
                        text="BABY ELEPHANT",
                        font_family="Segoe UI",
                        font_size_pt=28.0,
                        bold=True,
                        alignment="center",
                    )
                ],
            ),
        ],
    )

    page3 = PageModel(page_id="page_003", page_number=3, title="Playful Monkey")
    page4 = PageModel(page_id="page_004", page_number=4, title="Giant Giraffe")

    sample_doc.pages = [page1.to_dict(), page2.to_dict(), page3.to_dict(), page4.to_dict()]
    pm.save_current_project()

    window = MainWindow()
    window.resize(1360, 880)
    window.show()

    # Capture 1: Dashboard View
    window._switch_step(0)
    app.processEvents()
    pix_dash = window.grab()
    dash_path = output_dir / "01_dashboard.png"
    pix_dash.save(str(dash_path), "PNG")
    print(f"Captured Dashboard: {dash_path}")

    # Capture 2: Book Settings View
    window._switch_step(1)
    app.processEvents()
    pix_settings = window.grab()
    settings_path = output_dir / "02_book_settings.png"
    pix_settings.save(str(settings_path), "PNG")
    print(f"Captured Book Settings: {settings_path}")

    # Capture 3: Canvas Editor View
    window._switch_step(4)
    app.processEvents()
    # Select the title element so the property inspector shows text properties
    if window.canvas_editor_view.canvas_scene._element_items:
        first_item = list(window.canvas_editor_view.canvas_scene._element_items.values())[2]
        first_item.setSelected(True)
    app.processEvents()
    pix_canvas = window.grab()
    canvas_path = output_dir / "03_canvas_editor.png"
    pix_canvas.save(str(canvas_path), "PNG")
    print(f"Captured Canvas Editor: {canvas_path}")

    # Capture 4: Project Setup Dialog
    dlg = ProjectSetupDialog()
    dlg.resize(640, 580)
    dlg.show()
    app.processEvents()
    pix_dlg = dlg.grab()
    dlg_path = output_dir / "04_new_project_dialog.png"
    pix_dlg.save(str(dlg_path), "PNG")
    print(f"Captured New Project Dialog: {dlg_path}")

    dlg.close()
    window.close()
    print("All live screenshots captured successfully!")


if __name__ == "__main__":
    capture_screenshots()
