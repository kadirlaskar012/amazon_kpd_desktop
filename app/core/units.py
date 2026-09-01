"""
Physical unit conversion and precision coordinate calculations for KDP Book Production Studio.
Standard typographic points: 1 inch = 72 points = 25.4 mm.
"""

from enum import Enum
from typing import Tuple


class Unit(str, Enum):
    INCHES = "inches"
    MILLIMETERS = "mm"
    CENTIMETERS = "cm"
    POINTS = "pt"
    PIXELS = "px"

    @classmethod
    def from_string(cls, val: str) -> "Unit":
        val_lower = val.lower().strip()
        if val_lower in ("in", "inch", "inches", "in."):
            return cls.INCHES
        elif val_lower in ("mm", "millimeter", "millimeters"):
            return cls.MILLIMETERS
        elif val_lower in ("cm", "centimeter", "centimeters"):
            return cls.CENTIMETERS
        elif val_lower in ("pt", "point", "points"):
            return cls.POINTS
        elif val_lower in ("px", "pixel", "pixels"):
            return cls.PIXELS
        return cls.INCHES


# Conversion factors relative to points (72 pt = 1 inch = 25.4 mm)
POINTS_PER_INCH = 72.0
MM_PER_INCH = 25.4
POINTS_PER_MM = POINTS_PER_INCH / MM_PER_INCH  # ~2.83464567 pt/mm
POINTS_PER_CM = POINTS_PER_MM * 10.0          # ~28.3464567 pt/cm


def in_to_pt(inches: float) -> float:
    """Convert inches to typographic points."""
    return float(inches) * POINTS_PER_INCH


def pt_to_in(points: float) -> float:
    """Convert typographic points to inches."""
    return float(points) / POINTS_PER_INCH


def mm_to_pt(mm: float) -> float:
    """Convert millimeters to typographic points."""
    return float(mm) * POINTS_PER_MM


def pt_to_mm(points: float) -> float:
    """Convert typographic points to millimeters."""
    return float(points) / POINTS_PER_MM


def cm_to_pt(cm: float) -> float:
    """Convert centimeters to typographic points."""
    return float(cm) * POINTS_PER_CM


def pt_to_cm(points: float) -> float:
    """Convert typographic points to centimeters."""
    return float(points) / POINTS_PER_CM


def px_to_pt(px: float, dpi: int = 300) -> float:
    """Convert pixels at given DPI to typographic points."""
    if dpi <= 0:
        dpi = 300
    return (float(px) / float(dpi)) * POINTS_PER_INCH


def pt_to_px(points: float, dpi: int = 300) -> float:
    """Convert typographic points to pixels at given DPI."""
    if dpi <= 0:
        dpi = 300
    return (float(points) / POINTS_PER_INCH) * float(dpi)


def convert_to_points(value: float, from_unit: Unit, dpi: int = 300) -> float:
    """Convert any supported unit to typographic points."""
    if from_unit == Unit.INCHES:
        return in_to_pt(value)
    elif from_unit == Unit.MILLIMETERS:
        return mm_to_pt(value)
    elif from_unit == Unit.CENTIMETERS:
        return cm_to_pt(value)
    elif from_unit == Unit.POINTS:
        return float(value)
    elif from_unit == Unit.PIXELS:
        return px_to_pt(value, dpi)
    return float(value)


def convert_from_points(points: float, to_unit: Unit, dpi: int = 300) -> float:
    """Convert typographic points to target display unit."""
    if to_unit == Unit.INCHES:
        return pt_to_in(points)
    elif to_unit == Unit.MILLIMETERS:
        return pt_to_mm(points)
    elif to_unit == Unit.CENTIMETERS:
        return pt_to_cm(points)
    elif to_unit == Unit.POINTS:
        return float(points)
    elif to_unit == Unit.PIXELS:
        return pt_to_px(points, dpi)
    return float(points)


def format_dimension(points: float, unit: Unit, dpi: int = 300, decimals: int = 2) -> str:
    """Format dimension for clean UI display with unit suffix."""
    val = convert_from_points(points, unit, dpi)
    if unit == Unit.INCHES:
        return f"{val:.{decimals}f} in"
    elif unit == Unit.MILLIMETERS:
        return f"{val:.1f} mm"
    elif unit == Unit.CENTIMETERS:
        return f"{val:.2f} cm"
    elif unit == Unit.POINTS:
        return f"{val:.1f} pt"
    elif unit == Unit.PIXELS:
        return f"{int(round(val))} px"
    return f"{val:.{decimals}f}"


def calculate_kdp_gutter(page_count: int) -> float:
    """
    Returns recommended inside gutter margin in points based on KDP official specs:
    24-150 pages: 0.375 in (27.0 pt)
    151-300 pages: 0.500 in (36.0 pt)
    301-500 pages: 0.625 in (45.0 pt)
    501-700 pages: 0.750 in (54.0 pt)
    701-828 pages: 0.875 in (63.0 pt)
    """
    if page_count <= 150:
        return in_to_pt(0.375)
    elif page_count <= 300:
        return in_to_pt(0.500)
    elif page_count <= 500:
        return in_to_pt(0.625)
    elif page_count <= 700:
        return in_to_pt(0.750)
    else:
        return in_to_pt(0.875)


def calculate_spine_width_pt(page_count: int, paper_type: str = "white") -> float:
    """
    Calculates KDP spine width in points.
    KDP Formula:
    Black and white interior with white paper: page count * 0.002252 in
    Black and white interior with cream paper: page count * 0.0025 in
    Color interior with white paper: page count * 0.002347 in
    """
    paper_type_lower = paper_type.lower()
    if "cream" in paper_type_lower:
        thickness_per_page = 0.0025
    elif "color" in paper_type_lower:
        thickness_per_page = 0.002347
    else:
        thickness_per_page = 0.002252
    spine_inches = max(0.0, page_count * thickness_per_page)
    return in_to_pt(spine_inches)
