"""
Modern Creative Studio Design System & Qt Stylesheet.
Dark / Light Theme palettes, modern typography, card styling, and custom widget tokens.
"""

from typing import Dict


class Theme:
    # Modern Dark Palette
    BG_DARK = "#12131c"
    BG_SURFACE = "#1a1b26"
    BG_CARD = "#212336"
    BG_CARD_HOVER = "#2a2d45"
    BG_INPUT = "#161722"
    BORDER = "#2e324d"
    BORDER_FOCUS = "#6366f1"
    
    PRIMARY = "#6366f1"         # Indigo
    PRIMARY_HOVER = "#4f46e5"
    PRIMARY_PRESSED = "#4338ca"
    
    SECONDARY = "#22c55e"       # Emerald / Success
    SECONDARY_HOVER = "#16a34a"
    
    ACCENT = "#f59e0b"          # Amber / Warning
    DANGER = "#ef4444"          # Rose / Error
    INFO = "#0ea5e9"            # Sky
    
    TEXT_PRIMARY = "#f8fafc"
    TEXT_SECONDARY = "#94a3b8"
    TEXT_MUTED = "#64748b"
    TEXT_DISABLED = "#475569"

    @classmethod
    def get_stylesheet(cls) -> str:
        return f"""
        /* Global Reset & Base */
        QMainWindow, QDialog, QWidget {{
            background-color: {cls.BG_DARK};
            color: {cls.TEXT_PRIMARY};
            font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
            font-size: 13px;
        }}

        /* Tooltip */
        QToolTip {{
            background-color: {cls.BG_CARD};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER};
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 12px;
        }}

        /* Menubar & Menus */
        QMenuBar {{
            background-color: {cls.BG_SURFACE};
            color: {cls.TEXT_PRIMARY};
            border-bottom: 1px solid {cls.BORDER};
            padding: 4px;
        }}
        QMenuBar::item {{
            background: transparent;
            padding: 6px 12px;
            border-radius: 4px;
        }}
        QMenuBar::item:selected {{
            background-color: {cls.BG_CARD};
        }}
        QMenu {{
            background-color: {cls.BG_SURFACE};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER};
            border-radius: 8px;
            padding: 6px;
        }}
        QMenu::item {{
            padding: 6px 24px 6px 12px;
            border-radius: 4px;
        }}
        QMenu::item:selected {{
            background-color: {cls.PRIMARY};
            color: #ffffff;
        }}
        QMenu::separator {{
            height: 1px;
            background-color: {cls.BORDER};
            margin: 4px 6px;
        }}

        /* PushButtons */
        QPushButton {{
            background-color: {cls.BG_CARD};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER};
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 500;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background-color: {cls.BG_CARD_HOVER};
            border-color: {cls.BORDER_FOCUS};
        }}
        QPushButton:pressed {{
            background-color: {cls.BG_INPUT};
        }}
        QPushButton:disabled {{
            background-color: {cls.BG_DARK};
            color: {cls.TEXT_DISABLED};
            border-color: {cls.BG_INPUT};
        }}

        /* Primary Button */
        QPushButton.primary-btn, QPushButton[primary="true"] {{
            background-color: {cls.PRIMARY};
            color: #ffffff;
            border: 1px solid {cls.PRIMARY};
            font-weight: 600;
        }}
        QPushButton.primary-btn:hover, QPushButton[primary="true"]:hover {{
            background-color: {cls.PRIMARY_HOVER};
            border-color: {cls.PRIMARY_HOVER};
        }}
        QPushButton.primary-btn:pressed, QPushButton[primary="true"]:pressed {{
            background-color: {cls.PRIMARY_PRESSED};
        }}

        /* Success / Create Button */
        QPushButton.success-btn, QPushButton[success="true"] {{
            background-color: {cls.SECONDARY};
            color: #ffffff;
            border: 1px solid {cls.SECONDARY};
            font-weight: 600;
        }}
        QPushButton.success-btn:hover, QPushButton[success="true"]:hover {{
            background-color: {cls.SECONDARY_HOVER};
            border-color: {cls.SECONDARY_HOVER};
        }}

        /* Input Controls */
        QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
            background-color: {cls.BG_INPUT};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER};
            border-radius: 6px;
            padding: 7px 10px;
            selection-background-color: {cls.PRIMARY};
        }}
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
            border: 1px solid {cls.PRIMARY};
            background-color: {cls.BG_SURFACE};
        }}
        QLineEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled, QComboBox:disabled {{
            background-color: {cls.BG_DARK};
            color: {cls.TEXT_DISABLED};
            border-color: {cls.BG_CARD};
        }}

        /* SpinBoxes Buttons */
        QSpinBox::up-button, QDoubleSpinBox::up-button,
        QSpinBox::down-button, QDoubleSpinBox::down-button {{
            background-color: {cls.BG_CARD};
            border: none;
            border-radius: 3px;
            width: 16px;
            margin: 1px;
        }}
        QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
        QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
            background-color: {cls.PRIMARY};
        }}

        /* ComboBox */
        QComboBox::drop-down {{
            border: none;
            width: 24px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {cls.BG_SURFACE};
            border: 1px solid {cls.BORDER};
            border-radius: 6px;
            selection-background-color: {cls.PRIMARY};
            selection-color: #ffffff;
            padding: 4px;
        }}

        /* CheckBox & RadioButton */
        QCheckBox, QRadioButton {{
            color: {cls.TEXT_PRIMARY};
            spacing: 8px;
            font-size: 13px;
        }}
        QCheckBox::indicator, QRadioButton::indicator {{
            width: 18px;
            height: 18px;
            border: 1px solid {cls.BORDER};
            background-color: {cls.BG_INPUT};
            border-radius: 4px;
        }}
        QRadioButton::indicator {{
            border-radius: 9px;
        }}
        QCheckBox::indicator:hover, QRadioButton::indicator:hover {{
            border-color: {cls.PRIMARY};
        }}
        QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
            background-color: {cls.PRIMARY};
            border-color: {cls.PRIMARY};
        }}

        /* GroupBox */
        QGroupBox {{
            background-color: {cls.BG_SURFACE};
            border: 1px solid {cls.BORDER};
            border-radius: 8px;
            margin-top: 18px;
            padding-top: 14px;
            font-weight: 600;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 12px;
            padding: 0 6px;
            color: {cls.TEXT_SECONDARY};
            background-color: {cls.BG_SURFACE};
        }}

        /* ScrollBar */
        QScrollBar:vertical {{
            background-color: {cls.BG_DARK};
            width: 10px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {cls.BG_CARD_HOVER};
            min-height: 24px;
            border-radius: 5px;
            margin: 2px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {cls.PRIMARY};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        QScrollBar:horizontal {{
            background-color: {cls.BG_DARK};
            height: 10px;
            margin: 0px;
        }}
        QScrollBar::handle:horizontal {{
            background-color: {cls.BG_CARD_HOVER};
            min-width: 24px;
            border-radius: 5px;
            margin: 2px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background-color: {cls.PRIMARY};
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}

        /* Tabs */
        QTabWidget::pane {{
            border: 1px solid {cls.BORDER};
            background-color: {cls.BG_SURFACE};
            border-radius: 8px;
        }}
        QTabBar::tab {{
            background-color: {cls.BG_DARK};
            color: {cls.TEXT_SECONDARY};
            border: 1px solid {cls.BORDER};
            border-bottom: none;
            padding: 8px 16px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            margin-right: 4px;
        }}
        QTabBar::tab:selected {{
            background-color: {cls.BG_SURFACE};
            color: {cls.TEXT_PRIMARY};
            border-color: {cls.BORDER};
            font-weight: 600;
        }}
        QTabBar::tab:hover:!selected {{
            background-color: {cls.BG_CARD};
            color: {cls.TEXT_PRIMARY};
        }}

        /* List & Tree Views */
        QListWidget, QTreeWidget, QTableWidget {{
            background-color: {cls.BG_SURFACE};
            border: 1px solid {cls.BORDER};
            border-radius: 8px;
            padding: 4px;
        }}
        QListWidget::item, QTreeWidget::item, QTableWidget::item {{
            padding: 8px;
            border-radius: 6px;
            margin: 2px 0px;
        }}
        QListWidget::item:hover, QTreeWidget::item:hover, QTableWidget::item:hover {{
            background-color: {cls.BG_CARD};
        }}
        QListWidget::item:selected, QTreeWidget::item:selected, QTableWidget::item:selected {{
            background-color: {cls.PRIMARY};
            color: #ffffff;
        }}

        /* Status Bar */
        QStatusBar {{
            background-color: {cls.BG_SURFACE};
            color: {cls.TEXT_SECONDARY};
            border-top: 1px solid {cls.BORDER};
            font-size: 12px;
            padding: 4px 8px;
        }}
        """
