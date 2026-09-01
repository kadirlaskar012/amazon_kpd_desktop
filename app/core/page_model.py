"""
Page, Layer, and Canvas Element data models.
Supports precise physical positioning (pt), stacking, locking, and visibility.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid


class ElementType(str, Enum):
    IMAGE = "image"
    TEXT = "text"
    SHAPE = "shape"
    BORDER = "border"


@dataclass
class ElementModel:
    element_id: str = field(default_factory=lambda: f"elem_{uuid.uuid4().hex[:8]}")
    type: ElementType = ElementType.IMAGE
    x_pt: float = 0.0
    y_pt: float = 0.0
    width_pt: float = 100.0
    height_pt: float = 100.0
    rotation_deg: float = 0.0
    opacity: float = 1.0
    locked: bool = False
    visible: bool = True

    # Image-specific properties
    asset_id: Optional[str] = None
    maintain_aspect_ratio: bool = True
    crop_x: float = 0.0
    crop_y: float = 0.0
    crop_w: float = 1.0
    crop_h: float = 1.0

    # Text-specific properties
    text: Optional[str] = None
    font_family: Optional[str] = "Segoe UI"
    font_size_pt: Optional[float] = 24.0
    bold: bool = False
    italic: bool = False
    alignment: str = "center"  # left, center, right, justify
    color: str = "#000000"
    letter_spacing_pt: float = 0.0
    line_spacing_multiplier: float = 1.2

    # Shape / Border specific properties
    fill_color: Optional[str] = None
    stroke_color: Optional[str] = "#000000"
    stroke_width_pt: float = 1.0
    corner_radius_pt: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "element_id": self.element_id,
            "type": self.type.value if isinstance(self.type, ElementType) else str(self.type),
            "x_pt": self.x_pt,
            "y_pt": self.y_pt,
            "width_pt": self.width_pt,
            "height_pt": self.height_pt,
            "rotation_deg": self.rotation_deg,
            "opacity": self.opacity,
            "locked": self.locked,
            "visible": self.visible,
            "asset_id": self.asset_id,
            "maintain_aspect_ratio": self.maintain_aspect_ratio,
            "crop_x": self.crop_x,
            "crop_y": self.crop_y,
            "crop_w": self.crop_w,
            "crop_h": self.crop_h,
            "text": self.text,
            "font_family": self.font_family,
            "font_size_pt": self.font_size_pt,
            "bold": self.bold,
            "italic": self.italic,
            "alignment": self.alignment,
            "color": self.color,
            "letter_spacing_pt": self.letter_spacing_pt,
            "line_spacing_multiplier": self.line_spacing_multiplier,
            "fill_color": self.fill_color,
            "stroke_color": self.stroke_color,
            "stroke_width_pt": self.stroke_width_pt,
            "corner_radius_pt": self.corner_radius_pt,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ElementModel":
        el_type_raw = data.get("type", "image")
        try:
            el_type = ElementType(el_type_raw)
        except ValueError:
            el_type = ElementType.IMAGE

        return cls(
            element_id=str(data.get("element_id", f"elem_{uuid.uuid4().hex[:8]}")),
            type=el_type,
            x_pt=float(data.get("x_pt", 0.0)),
            y_pt=float(data.get("y_pt", 0.0)),
            width_pt=float(data.get("width_pt", 100.0)),
            height_pt=float(data.get("height_pt", 100.0)),
            rotation_deg=float(data.get("rotation_deg", 0.0)),
            opacity=float(data.get("opacity", 1.0)),
            locked=bool(data.get("locked", False)),
            visible=bool(data.get("visible", True)),
            asset_id=data.get("asset_id"),
            maintain_aspect_ratio=bool(data.get("maintain_aspect_ratio", True)),
            crop_x=float(data.get("crop_x", 0.0)),
            crop_y=float(data.get("crop_y", 0.0)),
            crop_w=float(data.get("crop_w", 1.0)),
            crop_h=float(data.get("crop_h", 1.0)),
            text=data.get("text"),
            font_family=data.get("font_family", "Segoe UI"),
            font_size_pt=float(data.get("font_size_pt", 24.0)) if data.get("font_size_pt") is not None else None,
            bold=bool(data.get("bold", False)),
            italic=bool(data.get("italic", False)),
            alignment=str(data.get("alignment", "center")),
            color=str(data.get("color", "#000000")),
            letter_spacing_pt=float(data.get("letter_spacing_pt", 0.0)),
            line_spacing_multiplier=float(data.get("line_spacing_multiplier", 1.2)),
            fill_color=data.get("fill_color"),
            stroke_color=data.get("stroke_color", "#000000"),
            stroke_width_pt=float(data.get("stroke_width_pt", 1.0)),
            corner_radius_pt=float(data.get("corner_radius_pt", 0.0)),
        )


@dataclass
class LayerModel:
    layer_id: str = field(default_factory=lambda: f"layer_{uuid.uuid4().hex[:6]}")
    name: str = "Layer"
    visible: bool = True
    locked: bool = False
    elements: List[ElementModel] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "layer_id": self.layer_id,
            "name": self.name,
            "visible": self.visible,
            "locked": self.locked,
            "elements": [e.to_dict() for e in self.elements],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LayerModel":
        elements = [ElementModel.from_dict(e) for e in data.get("elements", [])]
        return cls(
            layer_id=str(data.get("layer_id", f"layer_{uuid.uuid4().hex[:6]}")),
            name=str(data.get("name", "Layer")),
            visible=bool(data.get("visible", True)),
            locked=bool(data.get("locked", False)),
            elements=elements,
        )


@dataclass
class PageModel:
    page_id: str = field(default_factory=lambda: f"page_{uuid.uuid4().hex[:8]}")
    page_number: int = 1
    title: str = ""
    template_id: Optional[str] = None
    section: Optional[str] = None
    layers: List[LayerModel] = field(default_factory=list)

    def get_all_elements(self) -> List[ElementModel]:
        """Flatten elements across all layers."""
        elems = []
        for layer in self.layers:
            elems.extend(layer.elements)
        return elems

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_id": self.page_id,
            "page_number": self.page_number,
            "title": self.title,
            "template_id": self.template_id,
            "section": self.section,
            "layers": [l.to_dict() for l in self.layers],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PageModel":
        layers = [LayerModel.from_dict(l) for l in data.get("layers", [])]
        return cls(
            page_id=str(data.get("page_id", f"page_{uuid.uuid4().hex[:8]}")),
            page_number=int(data.get("page_number", 1)),
            title=str(data.get("title", "")),
            template_id=data.get("template_id"),
            section=data.get("section"),
            layers=layers,
        )
