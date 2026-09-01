"""
Smoke test for PySide6 UI views, widgets, and signal wiring.
"""

import os
from pathlib import Path
import tempfile
import pytest

from PySide6.QtWidgets import QApplication
from app.ui.theme import Theme
from app.ui.main_window import MainWindow
from app.ui.dashboard import DashboardView
from app.ui.book_settings import BookSettingsPanel
from app.ui.project_setup import ProjectSetupDialog
from app.core.project_manager import ProjectManager
from app.core.document_model import BookType, KDP_TRIM_PRESETS


@pytest.fixture(scope="session")
def qapp():
    # Set offscreen platform for reliable CI/headless execution
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def test_ui_components_instantiation(qapp):
    pm = ProjectManager.get_instance()

    with tempfile.TemporaryDirectory() as tmp_dir:
        proj_dir = Path(tmp_dir) / "TestProject"
        doc = pm.create_new_project(
            name="Smoke Test Book",
            location_dir=proj_dir,
            author="Author Name",
            book_type=BookType.COLORING_BOOK,
            trim_preset=KDP_TRIM_PRESETS[0],
            has_bleed=True,
        )

        window = MainWindow()
        assert window is not None
        assert window.windowTitle() == "KDP Book Production Studio"

        # Check that steps are switchable
        for i in range(len(window.step_buttons)):
            window._switch_step(i)
            assert window.stack.currentIndex() == i

        # Test Book Settings Panel controls
        panel = window.book_settings_view
        assert panel.isEnabled()
        assert panel.bleed_chk.isChecked() is True

        # Test Project Setup Dialog
        setup_dlg = ProjectSetupDialog()
        assert setup_dlg is not None
        assert setup_dlg.name_edit.text() != ""

        window.close()
