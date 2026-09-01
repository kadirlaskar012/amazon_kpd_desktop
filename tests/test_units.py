"""
Unit tests for physical units conversions and KDP calculations.
"""

import pytest
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
    calculate_spine_width_pt,
    format_dimension,
)


def test_inches_to_points():
    assert in_to_pt(1.0) == 72.0
    assert in_to_pt(8.5) == 612.0
    assert in_to_pt(11.0) == 792.0
    assert pt_to_in(72.0) == 1.0
    assert pt_to_in(612.0) == 8.5
    assert pt_to_in(792.0) == 11.0


def test_mm_cm_conversions():
    # 25.4 mm = 1 inch = 72 pt
    assert pytest.approx(mm_to_pt(25.4), 0.001) == 72.0
    assert pytest.approx(pt_to_mm(72.0), 0.001) == 25.4

    # 2.54 cm = 1 inch = 72 pt
    assert pytest.approx(cm_to_pt(2.54), 0.001) == 72.0
    assert pytest.approx(pt_to_cm(72.0), 0.001) == 2.54


def test_pixels_dpi_conversions():
    # 300 px @ 300 DPI = 1 inch = 72 pt
    assert px_to_pt(300, 300) == 72.0
    assert pt_to_px(72.0, 300) == 300.0

    # 150 px @ 150 DPI = 1 inch = 72 pt
    assert px_to_pt(150, 150) == 72.0
    assert pt_to_px(72.0, 150) == 150.0


def test_convert_to_and_from_points():
    assert convert_to_points(8.5, Unit.INCHES) == 612.0
    assert convert_from_points(612.0, Unit.INCHES) == 8.5
    assert pytest.approx(convert_to_points(25.4, Unit.MILLIMETERS), 0.001) == 72.0


def test_format_dimension():
    assert format_dimension(72.0, Unit.INCHES) == "1.00 in"
    assert format_dimension(612.0, Unit.INCHES) == "8.50 in"
    assert "mm" in format_dimension(72.0, Unit.MILLIMETERS)
    assert "pt" in format_dimension(72.0, Unit.POINTS)
    assert "px" in format_dimension(72.0, Unit.PIXELS, dpi=300)


def test_kdp_gutter_calculation():
    # 50 pages -> 0.375 in (27 pt)
    assert calculate_kdp_gutter(50) == in_to_pt(0.375)
    # 200 pages -> 0.500 in (36 pt)
    assert calculate_kdp_gutter(200) == in_to_pt(0.500)
    # 400 pages -> 0.625 in (45 pt)
    assert calculate_kdp_gutter(400) == in_to_pt(0.625)


def test_kdp_spine_width():
    # 100 pages white paper = 100 * 0.002252 in = 0.2252 in
    spine_pt = calculate_spine_width_pt(100, "white")
    assert pytest.approx(pt_to_in(spine_pt), 0.0001) == 0.2252
