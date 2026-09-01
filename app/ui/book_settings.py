"""
Book Settings Configuration Panel & Dialog.
Handles Trim Sizes, Custom Dimensions, Bleed, Margins, Gutter calculations, DPI, and Units.
"""

from typing import Optional

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QComboBox,
    QCheckBox,
    QDoubleSpinBox,
    QSpinBox,
    QPushButton,
    QGroupBox,
    QFrame,
    QMessageBox,
    QScrollArea,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from app.core.units import (
    Unit,
    in_to_pt,
    pt_to_in,
    mm_to_pt,
    pt_to_mm,
    cm_to_pt,
    pt_to_cm,
    px_to_pt,
    pt_to_px,
    convert_to_points,
    convert_from_points,
    calculate_kdp_gutter,
    format_dimension,
)
from app.core.document_model import (
    BookSettings,
    MarginSettings,
    PageNumberingSettings,
    KDP_TRIM_PRESETS,
    TrimPreset,
)
from app.core.project_manager import ProjectManager
from app.ui.theme import Theme


class BookSettingsPanel(QWidget):
    settings_applied = Signal(object)  # Emits updated BookSettings

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_manager = ProjectManager.get_instance()
        self._is_updating_ui = False

        self._init_ui()
        self._load_from_active_project()

        # Connect to project manager events
        self.project_manager.register_project_changed_listener(lambda doc: self._load_from_active_project())

    def _init_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll Area for clean overflow handling
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(24)

        # Header Title
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        title_lbl = QLabel("Book & Print Settings")
        title_lbl.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_lbl.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")
        subtitle_lbl = QLabel("Configure trim dimensions, bleed allowance, safe margins, and print resolution for Amazon KDP.")
        subtitle_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 13px;")
        header_layout.addWidget(title_lbl)
        header_layout.addWidget(subtitle_lbl)
        layout.addLayout(header_layout)

        # Section 1: Measurement Units & Preset
        unit_group = QGroupBox("Measurement Units & Dimensions")
        unit_grid = QGridLayout(unit_group)
        unit_grid.setContentsMargins(20, 20, 20, 20)
        unit_grid.setVerticalSpacing(14)
        unit_grid.setHorizontalSpacing(16)
        row = 0

        # Unit Selector
        unit_lbl = QLabel("Display Units:")
        unit_lbl.setStyleSheet("font-weight: 600;")
        self.unit_combo = QComboBox()
        self.unit_combo.addItem("Inches (in)", Unit.INCHES.value)
        self.unit_combo.addItem("Millimeters (mm)", Unit.MILLIMETERS.value)
        self.unit_combo.addItem("Centimeters (cm)", Unit.CENTIMETERS.value)
        self.unit_combo.addItem("Points (pt - 72/in)", Unit.POINTS.value)
        self.unit_combo.addItem("Pixels (px)", Unit.PIXELS.value)
        self.unit_combo.currentIndexChanged.connect(self._on_unit_changed)
        unit_grid.addWidget(unit_lbl, row, 0, Qt.AlignRight)
        unit_grid.addWidget(self.unit_combo, row, 1)
        row += 1

        # Trim Presets
        trim_lbl = QLabel("Trim Size Preset:")
        trim_lbl.setStyleSheet("font-weight: 600;")
        self.trim_combo = QComboBox()
        for preset in KDP_TRIM_PRESETS:
            desc = f" ({preset.description})" if preset.description else ""
            self.trim_combo.addItem(f"{preset.name}{desc}", preset.id)
        self.trim_combo.currentIndexChanged.connect(self._on_trim_preset_changed)
        unit_grid.addWidget(trim_lbl, row, 0, Qt.AlignRight)
        unit_grid.addWidget(self.trim_combo, row, 1)
        row += 1

        # Custom Dimensions
        dim_lbl = QLabel("Trim Width x Height:")
        dim_lbl.setStyleSheet("font-weight: 600;")
        dim_layout = QHBoxLayout()
        dim_layout.setSpacing(8)

        self.width_spin = QDoubleSpinBox()
        self.width_spin.setRange(2.0, 30.0)
        self.width_spin.setDecimals(3)
        self.width_spin.setSingleStep(0.125)
        self.width_spin.valueChanged.connect(self._on_custom_dim_changed)

        times_lbl = QLabel("×")
        times_lbl.setStyleSheet("font-weight: bold; font-size: 14px;")

        self.height_spin = QDoubleSpinBox()
        self.height_spin.setRange(2.0, 30.0)
        self.height_spin.setDecimals(3)
        self.height_spin.setSingleStep(0.125)
        self.height_spin.valueChanged.connect(self._on_custom_dim_changed)

        self.unit_suffix_lbl = QLabel("in")
        self.unit_suffix_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")

        dim_layout.addWidget(self.width_spin)
        dim_layout.addWidget(times_lbl)
        dim_layout.addWidget(self.height_spin)
        dim_layout.addWidget(self.unit_suffix_lbl)
        dim_layout.addStretch(1)

        unit_grid.addWidget(dim_lbl, row, 0, Qt.AlignRight)
        unit_grid.addLayout(dim_layout, row, 1)
        row += 1

        # Orientation
        orient_lbl = QLabel("Orientation:")
        orient_lbl.setStyleSheet("font-weight: 600;")
        self.orient_combo = QComboBox()
        self.orient_combo.addItem("Portrait", False)
        self.orient_combo.addItem("Landscape", True)
        self.orient_combo.currentIndexChanged.connect(self._on_orientation_changed)
        unit_grid.addWidget(orient_lbl, row, 0, Qt.AlignRight)
        unit_grid.addWidget(self.orient_combo, row, 1)
        row += 1

        layout.addWidget(unit_group)

        # Section 2: Bleed & Resolution
        bleed_group = QGroupBox("Bleed & Print Resolution")
        bleed_grid = QGridLayout(bleed_group)
        bleed_grid.setContentsMargins(20, 20, 20, 20)
        bleed_grid.setVerticalSpacing(14)
        bleed_grid.setHorizontalSpacing(16)
        brow = 0

        # Bleed Checkbox
        self.bleed_chk = QCheckBox("Enable Full Page Bleed (+0.125 in / 3.2 mm to top, bottom, and outside)")
        self.bleed_chk.setStyleSheet("font-weight: 600;")
        self.bleed_chk.toggled.connect(self._on_bleed_toggled)
        bleed_grid.addWidget(self.bleed_chk, brow, 0, 1, 2)
        brow += 1

        self.bleed_info_lbl = QLabel("No Bleed: Page elements stay strictly within cut boundaries.")
        self.bleed_info_lbl.setStyleSheet(f"color: {Theme.TEXT_MUTED}; font-size: 11px; margin-left: 26px;")
        bleed_grid.addWidget(self.bleed_info_lbl, brow, 0, 1, 2)
        brow += 1

        # Resolution DPI
        dpi_lbl = QLabel("Target Print DPI:")
        dpi_lbl.setStyleSheet("font-weight: 600;")
        self.dpi_combo = QComboBox()
        self.dpi_combo.addItem("300 DPI (KDP Standard - Recommended for Print)", 300)
        self.dpi_combo.addItem("600 DPI (Ultra High Precision Line Art)", 600)
        self.dpi_combo.addItem("150 DPI (Fast Draft Preview Only)", 150)
        bleed_grid.addWidget(dpi_lbl, brow, 0, Qt.AlignRight)
        bleed_grid.addWidget(self.dpi_combo, brow, 1)
        brow += 1

        layout.addWidget(bleed_group)

        # Section 3: Margins & Gutter
        margin_group = QGroupBox("Safe Margins & Inside Binding Gutter")
        margin_grid = QGridLayout(margin_group)
        margin_grid.setContentsMargins(20, 20, 20, 20)
        margin_grid.setVerticalSpacing(14)
        margin_grid.setHorizontalSpacing(16)
        mrow = 0

        # Top Margin
        top_lbl = QLabel("Top Margin:")
        self.top_m_spin = QDoubleSpinBox()
        self.top_m_spin.setRange(0.1, 5.0)
        self.top_m_spin.setDecimals(3)
        self.top_m_spin.setSingleStep(0.05)
        margin_grid.addWidget(top_lbl, mrow, 0, Qt.AlignRight)
        margin_grid.addWidget(self.top_m_spin, mrow, 1)

        # Bottom Margin
        bot_lbl = QLabel("Bottom Margin:")
        self.bot_m_spin = QDoubleSpinBox()
        self.bot_m_spin.setRange(0.1, 5.0)
        self.bot_m_spin.setDecimals(3)
        self.bot_m_spin.setSingleStep(0.05)
        margin_grid.addWidget(bot_lbl, mrow, 2, Qt.AlignRight)
        margin_grid.addWidget(self.bot_m_spin, mrow, 3)
        mrow += 1

        # Inside Gutter Margin
        inside_lbl = QLabel("Inside Gutter (Binding):")
        inside_lbl.setToolTip("Safety margin next to the spine. KDP requires at least 0.375 in (24-150 pages).")
        self.inside_m_spin = QDoubleSpinBox()
        self.inside_m_spin.setRange(0.25, 5.0)
        self.inside_m_spin.setDecimals(3)
        self.inside_m_spin.setSingleStep(0.05)
        margin_grid.addWidget(inside_lbl, mrow, 0, Qt.AlignRight)
        margin_grid.addWidget(self.inside_m_spin, mrow, 1)

        # Outside Margin
        outside_lbl = QLabel("Outside Margin:")
        self.outside_m_spin = QDoubleSpinBox()
        self.outside_m_spin.setRange(0.25, 5.0)
        self.outside_m_spin.setDecimals(3)
        self.outside_m_spin.setSingleStep(0.05)
        margin_grid.addWidget(outside_lbl, mrow, 2, Qt.AlignRight)
        margin_grid.addWidget(self.outside_m_spin, mrow, 3)
        mrow += 1

        # Gutter recommendation banner
        self.gutter_hint_lbl = QLabel("ℹ Amazon KDP Standard: 0.375 in (24-150 pages) / 0.500 in (151-300 pages)")
        self.gutter_hint_lbl.setStyleSheet(f"color: {Theme.INFO}; font-size: 11px;")
        margin_grid.addWidget(self.gutter_hint_lbl, mrow, 0, 1, 4)

        layout.addWidget(margin_group)

        # Section 4: Page Numbering
        num_group = QGroupBox("Page Numbering")
        num_grid = QGridLayout(num_group)
        num_grid.setContentsMargins(20, 20, 20, 20)
        num_grid.setVerticalSpacing(14)
        num_grid.setHorizontalSpacing(16)
        nrow = 0

        self.num_enabled_chk = QCheckBox("Enable Automatic Page Numbering")
        num_grid.addWidget(self.num_enabled_chk, nrow, 0, 1, 2)
        nrow += 1

        pos_lbl = QLabel("Position:")
        self.num_pos_combo = QComboBox()
        self.num_pos_combo.addItem("Bottom Center", "bottom_center")
        self.num_pos_combo.addItem("Bottom Outside", "bottom_outside")
        self.num_pos_combo.addItem("Top Center", "top_center")
        self.num_pos_combo.addItem("Top Outside", "top_outside")
        num_grid.addWidget(pos_lbl, nrow, 0, Qt.AlignRight)
        num_grid.addWidget(self.num_pos_combo, nrow, 1)

        start_lbl = QLabel("Start Number:")
        self.num_start_spin = QSpinBox()
        self.num_start_spin.setRange(1, 9999)
        self.num_start_spin.setValue(1)
        num_grid.addWidget(start_lbl, nrow, 2, Qt.AlignRight)
        num_grid.addWidget(self.num_start_spin, nrow, 3)
        nrow += 1

        layout.addWidget(num_group)
        layout.addStretch(1)

        # Action Buttons
        btn_bar = QHBoxLayout()
        btn_bar.setSpacing(12)

        self.revert_btn = QPushButton("Reset to Project Defaults")
        self.revert_btn.clicked.connect(self._load_from_active_project)

        self.apply_btn = QPushButton("Apply & Save Settings")
        self.apply_btn.setProperty("primary", True)
        self.apply_btn.clicked.connect(self._apply_settings)

        btn_bar.addStretch(1)
        btn_bar.addWidget(self.revert_btn)
        btn_bar.addWidget(self.apply_btn)
        layout.addLayout(btn_bar)

        scroll_area.setWidget(scroll_content)
        root_layout.addWidget(scroll_area)

    def _get_current_unit(self) -> Unit:
        return Unit.from_string(self.unit_combo.currentData())

    def _load_from_active_project(self):
        doc = self.project_manager.current_document
        if not doc:
            self.setEnabled(False)
            return

        self.setEnabled(True)
        self._is_updating_ui = True

        st = doc.settings
        unit = st.units

        # Set unit dropdown
        for i in range(self.unit_combo.count()):
            if self.unit_combo.itemData(i) == unit.value:
                self.unit_combo.setCurrentIndex(i)
                break

        # Set trim preset
        found_preset = False
        for i in range(self.trim_combo.count()):
            if self.trim_combo.itemData(i) == st.trim_preset_id:
                self.trim_combo.setCurrentIndex(i)
                found_preset = True
                break
        if not found_preset:
            # Set to custom
            self.trim_combo.setCurrentIndex(self.trim_combo.count() - 1)

        # Set width / height in current units
        self.width_spin.setValue(convert_from_points(st.trim_width_pt, unit, st.target_dpi))
        self.height_spin.setValue(convert_from_points(st.trim_height_pt, unit, st.target_dpi))

        # Orientation
        self.orient_combo.setCurrentIndex(1 if st.is_landscape else 0)

        # Bleed
        self.bleed_chk.setChecked(st.has_bleed)
        self._update_bleed_info_label(st.has_bleed)

        # DPI
        for i in range(self.dpi_combo.count()):
            if self.dpi_combo.itemData(i) == st.target_dpi:
                self.dpi_combo.setCurrentIndex(i)
                break

        # Margins in current units
        self.top_m_spin.setValue(convert_from_points(st.margins.top_pt, unit, st.target_dpi))
        self.bot_m_spin.setValue(convert_from_points(st.margins.bottom_pt, unit, st.target_dpi))
        self.inside_m_spin.setValue(convert_from_points(st.margins.inside_pt, unit, st.target_dpi))
        self.outside_m_spin.setValue(convert_from_points(st.margins.outside_pt, unit, st.target_dpi))

        # Page Numbering
        num = st.page_numbering
        self.num_enabled_chk.setChecked(num.enabled)
        for i in range(self.num_pos_combo.count()):
            if self.num_pos_combo.itemData(i) == num.position:
                self.num_pos_combo.setCurrentIndex(i)
                break
        self.num_start_spin.setValue(num.start_number)

        self._update_unit_labels()
        self._is_updating_ui = False

    def _update_bleed_info_label(self, has_bleed: bool):
        if has_bleed:
            self.bleed_info_lbl.setText(
                "✓ Full Bleed Active: Page trimmed document extends by +0.125 in (9.0 pt) on outside, top, and bottom."
            )
            self.bleed_info_lbl.setStyleSheet(f"color: {Theme.SECONDARY}; font-size: 11px; margin-left: 26px;")
        else:
            self.bleed_info_lbl.setText(
                "No Bleed: Page elements stay strictly within cut trim boundaries."
            )
            self.bleed_info_lbl.setStyleSheet(f"color: {Theme.TEXT_MUTED}; font-size: 11px; margin-left: 26px;")

    def _on_unit_changed(self):
        if self._is_updating_ui:
            return
        # Refresh inputs with converted unit values
        doc = self.project_manager.current_document
        if not doc:
            return
        unit = self._get_current_unit()
        doc.settings.units = unit
        self._load_from_active_project()

    def _update_unit_labels(self):
        unit = self._get_current_unit()
        suffix_map = {
            Unit.INCHES: "in",
            Unit.MILLIMETERS: "mm",
            Unit.CENTIMETERS: "cm",
            Unit.POINTS: "pt",
            Unit.PIXELS: "px",
        }
        suffix = suffix_map.get(unit, "in")
        self.unit_suffix_lbl.setText(suffix)

        # Update spinbox range limits according to unit
        if unit == Unit.INCHES:
            self.width_spin.setRange(2.0, 30.0)
            self.height_spin.setRange(2.0, 30.0)
            self.width_spin.setSingleStep(0.125)
            self.height_spin.setSingleStep(0.125)
        elif unit == Unit.MILLIMETERS:
            self.width_spin.setRange(50.0, 800.0)
            self.height_spin.setRange(50.0, 800.0)
            self.width_spin.setSingleStep(1.0)
            self.height_spin.setSingleStep(1.0)
        elif unit == Unit.CENTIMETERS:
            self.width_spin.setRange(5.0, 80.0)
            self.height_spin.setRange(5.0, 80.0)
            self.width_spin.setSingleStep(0.1)
            self.height_spin.setSingleStep(0.1)
        elif unit == Unit.POINTS:
            self.width_spin.setRange(150.0, 2500.0)
            self.height_spin.setRange(150.0, 2500.0)
            self.width_spin.setSingleStep(1.0)
            self.height_spin.setSingleStep(1.0)
        elif unit == Unit.PIXELS:
            self.width_spin.setRange(600.0, 10000.0)
            self.height_spin.setRange(600.0, 10000.0)
            self.width_spin.setSingleStep(10.0)
            self.height_spin.setSingleStep(10.0)

    def _on_trim_preset_changed(self):
        if self._is_updating_ui:
            return
        preset_id = self.trim_combo.currentData()
        if preset_id == "custom":
            return

        preset = next((p for p in KDP_TRIM_PRESETS if p.id == preset_id), None)
        if not preset:
            return

        unit = self._get_current_unit()
        is_landscape = self.orient_combo.currentData()

        w_pt = preset.height_pt if is_landscape else preset.width_pt
        h_pt = preset.width_pt if is_landscape else preset.height_pt

        self._is_updating_ui = True
        self.width_spin.setValue(convert_from_points(w_pt, unit, self.dpi_combo.currentData()))
        self.height_spin.setValue(convert_from_points(h_pt, unit, self.dpi_combo.currentData()))
        self._is_updating_ui = False

    def _on_custom_dim_changed(self):
        if self._is_updating_ui:
            return
        # If dimension changed manually, set preset to custom
        self._is_updating_ui = True
        self.trim_combo.setCurrentIndex(self.trim_combo.count() - 1)
        self._is_updating_ui = False

    def _on_orientation_changed(self):
        if self._is_updating_ui:
            return
        # Swap width and height
        w = self.width_spin.value()
        h = self.height_spin.value()
        is_landscape = self.orient_combo.currentData()

        if (is_landscape and w < h) or (not is_landscape and w > h):
            self._is_updating_ui = True
            self.width_spin.setValue(h)
            self.height_spin.setValue(w)
            self._is_updating_ui = False

    def _on_bleed_toggled(self, checked: bool):
        self._update_bleed_info_label(checked)

    def _apply_settings(self):
        doc = self.project_manager.current_document
        if not doc:
            return

        unit = self._get_current_unit()
        dpi = int(self.dpi_combo.currentData())

        # Convert values to physical typographic points
        w_pt = convert_to_points(self.width_spin.value(), unit, dpi)
        h_pt = convert_to_points(self.height_spin.value(), unit, dpi)

        top_pt = convert_to_points(self.top_m_spin.value(), unit, dpi)
        bot_pt = convert_to_points(self.bot_m_spin.value(), unit, dpi)
        inside_pt = convert_to_points(self.inside_m_spin.value(), unit, dpi)
        outside_pt = convert_to_points(self.outside_m_spin.value(), unit, dpi)

        # KDP Minimum Margin Safety Validation
        min_outside_pt = in_to_pt(0.375) if self.bleed_chk.isChecked() else in_to_pt(0.25)
        if outside_pt < min_outside_pt:
            reply = QMessageBox.warning(
                self,
                "Margin Warning for KDP",
                f"Your outside margin ({format_dimension(outside_pt, unit, dpi)}) is below KDP's recommended minimum "
                f"({format_dimension(min_outside_pt, unit, dpi)}).\n\nContent placed close to the edge may be cut off.\n\nDo you want to proceed?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                return

        # Update ProjectDocument
        doc.settings.units = unit
        doc.settings.trim_preset_id = self.trim_combo.currentData()
        doc.settings.trim_width_pt = w_pt
        doc.settings.trim_height_pt = h_pt
        doc.settings.is_landscape = self.orient_combo.currentData()
        doc.settings.has_bleed = self.bleed_chk.isChecked()
        doc.settings.target_dpi = dpi

        doc.settings.margins = MarginSettings(
            top_pt=top_pt,
            bottom_pt=bot_pt,
            inside_pt=inside_pt,
            outside_pt=outside_pt,
        )

        doc.settings.page_numbering = PageNumberingSettings(
            enabled=self.num_enabled_chk.isChecked(),
            position=self.num_pos_combo.currentData(),
            start_number=self.num_start_spin.value(),
        )

        # Save project
        self.project_manager.save_current_project()
        self.settings_applied.emit(doc.settings)

        QMessageBox.information(
            self,
            "Settings Saved",
            f"Book settings successfully updated:\n• Trim: {format_dimension(w_pt, unit, dpi)} × {format_dimension(h_pt, unit, dpi)}\n"
            f"• Bleed: {'Enabled' if doc.settings.has_bleed else 'Disabled'}\n"
            f"• DPI: {dpi} DPI\n"
            f"• Units: {unit.value.title()}",
        )
