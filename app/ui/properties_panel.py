"""
PropertiesPanel: Physical coordinate inspector and typography/styling controls for selected canvas elements.
"""

from typing import Optional

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QDoubleSpinBox,
    QSpinBox,
    QComboBox,
    QCheckBox,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QGroupBox,
    QFrame,
    QScrollArea,
    QColorDialog,
    QSlider,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor

from app.core.page_model import ElementModel, ElementType
from app.core.document_model import BookSettings
from app.core.units import (
    Unit,
    convert_from_points,
    convert_to_points,
    format_dimension,
)
from app.ui.theme import Theme


class PropertiesPanel(QWidget):
    property_changed = Signal(object)  # Emits modified ElementModel

    def __init__(self, settings: Optional[BookSettings] = None, parent=None):
        super().__init__(parent)
        self.settings = settings or BookSettings()
        self.current_element: Optional[ElementModel] = None
        self._is_updating = False

        self.setMinimumWidth(280)
        self.setMaximumWidth(360)
        self._init_ui()
        self.set_element(None)

    def set_settings(self, settings: BookSettings):
        self.settings = settings
        self._update_unit_labels()
        if self.current_element:
            self._load_element_properties()

    def _init_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Header Title
        self.title_lbl = QLabel("Properties")
        self.title_lbl.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.title_lbl.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")
        layout.addWidget(self.title_lbl)

        # 1. Transform / Physical Coordinates Group
        geo_group = QGroupBox("Position & Size")
        geo_grid = QGridLayout(geo_group)
        geo_grid.setContentsMargins(12, 14, 12, 14)
        geo_grid.setVerticalSpacing(10)
        geo_grid.setHorizontalSpacing(10)

        # X
        geo_grid.addWidget(QLabel("X:"), 0, 0, Qt.AlignRight)
        self.x_spin = QDoubleSpinBox()
        self.x_spin.setRange(-2000.0, 5000.0)
        self.x_spin.setDecimals(2)
        self.x_spin.setSingleStep(0.1)
        self.x_spin.valueChanged.connect(self._on_geometry_changed)
        geo_grid.addWidget(self.x_spin, 0, 1)

        # Y
        geo_grid.addWidget(QLabel("Y:"), 0, 2, Qt.AlignRight)
        self.y_spin = QDoubleSpinBox()
        self.y_spin.setRange(-2000.0, 5000.0)
        self.y_spin.setDecimals(2)
        self.y_spin.setSingleStep(0.1)
        self.y_spin.valueChanged.connect(self._on_geometry_changed)
        geo_grid.addWidget(self.y_spin, 0, 3)

        # Width
        geo_grid.addWidget(QLabel("W:"), 1, 0, Qt.AlignRight)
        self.w_spin = QDoubleSpinBox()
        self.w_spin.setRange(0.1, 5000.0)
        self.w_spin.setDecimals(2)
        self.w_spin.setSingleStep(0.1)
        self.w_spin.valueChanged.connect(self._on_geometry_changed)
        geo_grid.addWidget(self.w_spin, 1, 1)

        # Height
        geo_grid.addWidget(QLabel("H:"), 1, 2, Qt.AlignRight)
        self.h_spin = QDoubleSpinBox()
        self.h_spin.setRange(0.1, 5000.0)
        self.h_spin.setDecimals(2)
        self.h_spin.setSingleStep(0.1)
        self.h_spin.valueChanged.connect(self._on_geometry_changed)
        geo_grid.addWidget(self.h_spin, 1, 3)

        # Rotation
        geo_grid.addWidget(QLabel("Rot (°):"), 2, 0, Qt.AlignRight)
        self.rot_spin = QDoubleSpinBox()
        self.rot_spin.setRange(0.0, 360.0)
        self.rot_spin.setSingleStep(15.0)
        self.rot_spin.valueChanged.connect(self._on_geometry_changed)
        geo_grid.addWidget(self.rot_spin, 2, 1)

        # Opacity
        geo_grid.addWidget(QLabel("Opacity:"), 2, 2, Qt.AlignRight)
        self.opacity_spin = QSpinBox()
        self.opacity_spin.setRange(0, 100)
        self.opacity_spin.setValue(100)
        self.opacity_spin.setSuffix("%")
        self.opacity_spin.valueChanged.connect(self._on_geometry_changed)
        geo_grid.addWidget(self.opacity_spin, 2, 3)

        # Aspect Ratio Lock
        self.aspect_chk = QCheckBox("Lock Aspect Ratio")
        self.aspect_chk.toggled.connect(self._on_aspect_toggled)
        geo_grid.addWidget(self.aspect_chk, 3, 0, 1, 4)

        layout.addWidget(geo_group)

        # 2. Quick Alignment Actions
        align_group = QGroupBox("Align to Page")
        align_layout = QVBoxLayout(align_group)
        align_layout.setContentsMargins(10, 12, 10, 12)
        align_layout.setSpacing(6)

        row1 = QHBoxLayout()
        row1.setSpacing(4)
        btn_left = QPushButton("⇤ Left")
        btn_left.clicked.connect(lambda: self._align_element("left"))
        btn_center_h = QPushButton("⇥ Center ⇤")
        btn_center_h.clicked.connect(lambda: self._align_element("center_h"))
        btn_right = QPushButton("Right ⇥")
        btn_right.clicked.connect(lambda: self._align_element("right"))
        row1.addWidget(btn_left)
        row1.addWidget(btn_center_h)
        row1.addWidget(btn_right)
        align_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(4)
        btn_top = QPushButton("⤊ Top")
        btn_top.clicked.connect(lambda: self._align_element("top"))
        btn_center_v = QPushButton("⤋ Middle ⤊")
        btn_center_v.clicked.connect(lambda: self._align_element("center_v"))
        btn_bot = QPushButton("Bottom ⤋")
        btn_bot.clicked.connect(lambda: self._align_element("bottom"))
        row2.addWidget(btn_top)
        row2.addWidget(btn_center_v)
        row2.addWidget(btn_bot)
        align_layout.addLayout(row2)

        # Fit / Fill Safe Area
        row3 = QHBoxLayout()
        row3.setSpacing(4)
        btn_fit = QPushButton("Fit Safe Area")
        btn_fit.clicked.connect(self._fit_to_safe_area)
        btn_fill = QPushButton("Fill Page")
        btn_fill.clicked.connect(self._fill_page)
        row3.addWidget(btn_fit)
        row3.addWidget(btn_fill)
        align_layout.addLayout(row3)

        layout.addWidget(align_group)

        # 3. Typography Group (Visible when Text element selected)
        self.text_group = QGroupBox("Text & Typography")
        text_layout = QVBoxLayout(self.text_group)
        text_layout.setContentsMargins(12, 14, 12, 14)
        text_layout.setSpacing(10)

        # Text Content Field
        self.text_content_edit = QLineEdit()
        self.text_content_edit.setPlaceholderText("Enter text...")
        self.text_content_edit.textChanged.connect(self._on_text_changed)
        text_layout.addWidget(self.text_content_edit)

        # Font Family & Size
        f_row = QHBoxLayout()
        self.font_combo = QComboBox()
        self.font_combo.addItems([
            "Segoe UI", "Comic Sans MS", "Arial", "Impact", "Georgia", "Courier New", "Verdana"
        ])
        self.font_combo.currentIndexChanged.connect(self._on_text_changed)

        self.font_size_spin = QDoubleSpinBox()
        self.font_size_spin.setRange(6.0, 144.0)
        self.font_size_spin.setValue(24.0)
        self.font_size_spin.setSuffix(" pt")
        self.font_size_spin.valueChanged.connect(self._on_text_changed)

        f_row.addWidget(self.font_combo, 2)
        f_row.addWidget(self.font_size_spin, 1)
        text_layout.addLayout(f_row)

        # Bold / Italic / Alignment
        style_row = QHBoxLayout()
        self.bold_btn = QPushButton("B")
        self.bold_btn.setCheckable(True)
        self.bold_btn.setStyleSheet("font-weight: bold; min-width: 32px;")
        self.bold_btn.toggled.connect(self._on_text_changed)

        self.italic_btn = QPushButton("I")
        self.italic_btn.setCheckable(True)
        self.italic_btn.setStyleSheet("font-style: italic; min-width: 32px;")
        self.italic_btn.toggled.connect(self._on_text_changed)

        self.align_combo = QComboBox()
        self.align_combo.addItem("Align Left", "left")
        self.align_combo.addItem("Align Center", "center")
        self.align_combo.addItem("Align Right", "right")
        self.align_combo.currentIndexChanged.connect(self._on_text_changed)

        style_row.addWidget(self.bold_btn)
        style_row.addWidget(self.italic_btn)
        style_row.addWidget(self.align_combo, 1)
        text_layout.addLayout(style_row)

        # Text Color Picker
        color_row = QHBoxLayout()
        color_lbl = QLabel("Color:")
        self.color_preview = QPushButton()
        self.color_preview.setStyleSheet("background-color: #000000; border: 1px solid #ffffff; height: 24px;")
        self.color_preview.clicked.connect(self._pick_text_color)
        color_row.addWidget(color_lbl)
        color_row.addWidget(self.color_preview, 1)
        text_layout.addLayout(color_row)

        layout.addWidget(self.text_group)

        # 4. Layer Ordering & Locking
        layer_group = QGroupBox("Layer & Stacking")
        layer_layout = QVBoxLayout(layer_group)
        layer_layout.setContentsMargins(10, 12, 10, 12)
        layer_layout.setSpacing(6)

        lock_row = QHBoxLayout()
        self.lock_chk = QCheckBox("Lock Position")
        self.lock_chk.toggled.connect(self._on_lock_toggled)
        self.visible_chk = QCheckBox("Visible")
        self.visible_chk.setChecked(True)
        self.visible_chk.toggled.connect(self._on_visible_toggled)
        lock_row.addWidget(self.lock_chk)
        lock_row.addWidget(self.visible_chk)
        layer_layout.addLayout(lock_row)

        layout.addWidget(layer_group)
        layout.addStretch(1)

        scroll_area.setWidget(scroll_content)
        root_layout.addWidget(scroll_area)

    def _update_unit_labels(self):
        unit = self.settings.units
        suffix = " in" if unit == Unit.INCHES else f" {unit.value}"
        self.x_spin.setSuffix(suffix)
        self.y_spin.setSuffix(suffix)
        self.w_spin.setSuffix(suffix)
        self.h_spin.setSuffix(suffix)

    def set_element(self, elem: Optional[ElementModel]):
        self.current_element = elem
        if not elem:
            self.setEnabled(False)
            self.title_lbl.setText("No Selection")
            return

        self.setEnabled(True)
        self.title_lbl.setText(f"Element: {elem.type.value.title()}")
        self._load_element_properties()

    def _load_element_properties(self):
        elem = self.current_element
        if not elem:
            return

        self._is_updating = True
        unit = self.settings.units
        dpi = self.settings.target_dpi

        self.x_spin.setValue(convert_from_points(elem.x_pt, unit, dpi))
        self.y_spin.setValue(convert_from_points(elem.y_pt, unit, dpi))
        self.w_spin.setValue(convert_from_points(elem.width_pt, unit, dpi))
        self.h_spin.setValue(convert_from_points(elem.height_pt, unit, dpi))

        self.rot_spin.setValue(elem.rotation_deg)
        self.opacity_spin.setValue(int(round(elem.opacity * 100)))
        self.aspect_chk.setChecked(elem.maintain_aspect_ratio)
        self.lock_chk.setChecked(elem.locked)
        self.visible_chk.setChecked(elem.visible)

        # Typography visibility
        if elem.type == ElementType.TEXT:
            self.text_group.setVisible(True)
            self.text_content_edit.setText(elem.text or "")
            self.font_size_spin.setValue(elem.font_size_pt or 24.0)
            self.bold_btn.setChecked(elem.bold)
            self.italic_btn.setChecked(elem.italic)

            # Font family
            idx = self.font_combo.findText(elem.font_family or "Segoe UI")
            if idx >= 0:
                self.font_combo.setCurrentIndex(idx)

            # Alignment
            for i in range(self.align_combo.count()):
                if self.align_combo.itemData(i) == elem.alignment:
                    self.align_combo.setCurrentIndex(i)
                    break

            color_hex = elem.color or "#000000"
            self.color_preview.setStyleSheet(f"background-color: {color_hex}; border: 1px solid #ffffff; height: 24px;")
        else:
            self.text_group.setVisible(False)

        self._is_updating = False

    def _on_geometry_changed(self):
        if self._is_updating or not self.current_element:
            return

        unit = self.settings.units
        dpi = self.settings.target_dpi

        self.current_element.x_pt = convert_to_points(self.x_spin.value(), unit, dpi)
        self.current_element.y_pt = convert_to_points(self.y_spin.value(), unit, dpi)
        self.current_element.width_pt = convert_to_points(self.w_spin.value(), unit, dpi)
        self.current_element.height_pt = convert_to_points(self.h_spin.value(), unit, dpi)
        self.current_element.rotation_deg = self.rot_spin.value()
        self.current_element.opacity = self.opacity_spin.value() / 100.0

        self.property_changed.emit(self.current_element)

    def _on_aspect_toggled(self, checked: bool):
        if not self._is_updating and self.current_element:
            self.current_element.maintain_aspect_ratio = checked
            self.property_changed.emit(self.current_element)

    def _on_lock_toggled(self, checked: bool):
        if not self._is_updating and self.current_element:
            self.current_element.locked = checked
            self.property_changed.emit(self.current_element)

    def _on_visible_toggled(self, checked: bool):
        if not self._is_updating and self.current_element:
            self.current_element.visible = checked
            self.property_changed.emit(self.current_element)

    def _on_text_changed(self):
        if self._is_updating or not self.current_element:
            return

        self.current_element.text = self.text_content_edit.text()
        self.current_element.font_family = self.font_combo.currentText()
        self.current_element.font_size_pt = self.font_size_spin.value()
        self.current_element.bold = self.bold_btn.isChecked()
        self.current_element.italic = self.italic_btn.isChecked()
        self.current_element.alignment = self.align_combo.currentData()

        self.property_changed.emit(self.current_element)

    def _pick_text_color(self):
        if not self.current_element:
            return
        initial_color = QColor(self.current_element.color or "#000000")
        color = QColorDialog.getColor(initial_color, self, "Select Text Color")
        if color.isValid():
            hex_color = color.name()
            self.current_element.color = hex_color
            self.color_preview.setStyleSheet(f"background-color: {hex_color}; border: 1px solid #ffffff; height: 24px;")
            self.property_changed.emit(self.current_element)

    def _align_element(self, mode: str):
        if not self.current_element:
            return

        page_w = self.settings.trim_width_pt
        page_h = self.settings.trim_height_pt
        elem_w = self.current_element.width_pt
        elem_h = self.current_element.height_pt

        margins = self.settings.margins
        safe_x = margins.inside_pt
        safe_y = margins.top_pt
        safe_w = max(10.0, page_w - (margins.inside_pt + margins.outside_pt))
        safe_h = max(10.0, page_h - (margins.top_pt + margins.bottom_pt))

        if mode == "left":
            self.current_element.x_pt = safe_x
        elif mode == "center_h":
            self.current_element.x_pt = safe_x + ((safe_w - elem_w) / 2.0)
        elif mode == "right":
            self.current_element.x_pt = safe_x + safe_w - elem_w
        elif mode == "top":
            self.current_element.y_pt = safe_y
        elif mode == "center_v":
            self.current_element.y_pt = safe_y + ((safe_h - elem_h) / 2.0)
        elif mode == "bottom":
            self.current_element.y_pt = safe_y + safe_h - elem_h

        self._load_element_properties()
        self.property_changed.emit(self.current_element)

    def _fit_to_safe_area(self):
        if not self.current_element:
            return

        page_w = self.settings.trim_width_pt
        page_h = self.settings.trim_height_pt
        margins = self.settings.margins

        safe_x = margins.inside_pt
        safe_y = margins.top_pt
        safe_w = max(10.0, page_w - (margins.inside_pt + margins.outside_pt))
        safe_h = max(10.0, page_h - (margins.top_pt + margins.bottom_pt))

        if self.current_element.maintain_aspect_ratio and self.current_element.height_pt > 0:
            aspect = self.current_element.width_pt / self.current_element.height_pt
            if (safe_w / safe_h) > aspect:
                # Constrained by height
                target_h = safe_h
                target_w = target_h * aspect
            else:
                # Constrained by width
                target_w = safe_w
                target_h = target_w / aspect
            self.current_element.width_pt = target_w
            self.current_element.height_pt = target_h
            self.current_element.x_pt = safe_x + ((safe_w - target_w) / 2.0)
            self.current_element.y_pt = safe_y + ((safe_h - target_h) / 2.0)
        else:
            self.current_element.x_pt = safe_x
            self.current_element.y_pt = safe_y
            self.current_element.width_pt = safe_w
            self.current_element.height_pt = safe_h

        self._load_element_properties()
        self.property_changed.emit(self.current_element)

    def _fill_page(self):
        if not self.current_element:
            return
        self.current_element.x_pt = 0.0
        self.current_element.y_pt = 0.0
        self.current_element.width_pt = self.settings.trim_width_pt
        self.current_element.height_pt = self.settings.trim_height_pt
        self._load_element_properties()
        self.property_changed.emit(self.current_element)
