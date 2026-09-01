"""
KDP Book Production Studio - Main Application Entry Point.
Initializes PySide6 application lifecycle, High-DPI attributes, theme, and main window.
"""

import os
import sys
from pathlib import Path

# Ensure root workspace directory is in python path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.ui.theme import Theme
from app.ui.main_window import MainWindow


def main():
    # Enable High DPI pixmaps and scaling
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)
    app.setApplicationName("KDP Book Production Studio")
    app.setOrganizationName("KDPStudio")

    # Apply modern global typography and stylesheet
    app_font = QFont("Segoe UI", 10)
    app.setFont(app_font)
    app.setStyleSheet(Theme.get_stylesheet())

    # Instantiate and display Main Window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
