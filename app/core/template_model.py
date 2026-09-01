"""
Template data models for standardized reusable layouts.
Defines layout slots for reference image, main coloring image, title, borders, etc.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid

from app.core.units import in_to_pt


class SlotType(str, Enum):
    REFERENCE_IMAGE = "reference_image"
    MAIN_IMAGE = "main_image"
    TITLE = "title"
    DECORATION = "decoration"
    BORDER = "border"
    PAGE_NUMBER = "page_number"


class TemplateCategory(str, Enum):
    COLORING = "coloring"
    TRACING = "tracing"
    ACTIVITY = "activity"
    PUZZLE = "puzzle"
    CUSTOM = "custom"


@dataclass
class LayoutSlot:
    slot_id: str
    slot_type: SlotType
    name: str
    x_percent: float  # Percentage of safe width (0.0 - 1.0)
    y_percent: float  # Percentage of safe height (0.0 - 1.0)
    width_percent: float
    height_percent: float
    font_family: Optional[str] = "Segoe UI"
    font_size_pt: Optional[float] = 24.0
    alignment: str = "center"
    maintain_aspect_ratio: bool = True
    is_required: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "slot_id": self.slot_id,
            "slot_type": self.slot_type.value if isinstance(self.slot_type, SlotType) else str(self.slot_type),
            "name": self.name,
            "x_percent": self.x_percent,
            "y_percent": self.y_percent,
            "width_percent": self.width_percent,
            "height_percent": self.height_percent,
            "font_family": self.font_family,
            "font_size_pt": self.font_size_pt,
            "alignment": self.alignment,
            "maintain_aspect_ratio": self.maintain_aspect_ratio,
            "is_required": self.is_required,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LayoutSlot":
        st_raw = data.get("slot_type", "main_image")
        try:
            st = SlotType(st_raw)
        except ValueError:
            st = SlotType.MAIN_IMAGE

        return cls(
            slot_id=str(data.get("slot_id", f"slot_{uuid.uuid4().hex[:6]}")),
            slot_type=st,
            name=str(data.get("name", "Slot")),
            x_percent=float(data.get("x_percent", 0.0)),
            y_percent=float(data.get("y_percent", 0.0)),
            width_percent=float(data.get("width_percent", 1.0)),
            height_percent=float(data.get("height_percent", 1.0)),
            font_family=data.get("font_family", "Segoe UI"),
            font_size_pt=float(data.get("font_size_pt", 24.0)) if data.get("font_size_pt") is not None else None,
            alignment=str(data.get("alignment", "center")),
            maintain_aspect_ratio=bool(data.get("maintain_aspect_ratio", True)),
            is_required=bool(data.get("is_required", True)),
        )


@dataclass
class TemplateModel:
    template_id: str
    name: str
    category: TemplateCategory = TemplateCategory.COLORING
    description: str = ""
    thumbnail_rel_path: Optional[str] = None
    slots: List[LayoutSlot] = field(default_factory=list)
    has_border: bool = False
    border_style: str = "simple"  # simple, rounded, decorative
    border_inset_pt: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "template_id": self.template_id,
            "name": self.name,
            "category": self.category.value if isinstance(self.category, TemplateCategory) else str(self.category),
            "description": self.description,
            "thumbnail_rel_path": self.thumbnail_rel_path,
            "slots": [s.to_dict() for s in self.slots],
            "has_border": self.has_border,
            "border_style": self.border_style,
            "border_inset_pt": self.border_inset_pt,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TemplateModel":
        cat_raw = data.get("category", "coloring")
        try:
            cat = TemplateCategory(cat_raw)
        except ValueError:
            cat = TemplateCategory.COLORING

        slots = [LayoutSlot.from_dict(s) for s in data.get("slots", [])]
        return cls(
            template_id=str(data.get("template_id", f"tpl_{uuid.uuid4().hex[:6]}")),
            name=str(data.get("name", "Template")),
            category=cat,
            description=str(data.get("description", "")),
            thumbnail_rel_path=data.get("thumbnail_rel_path"),
            slots=slots,
            has_border=bool(data.get("has_border", False)),
            border_style=str(data.get("border_style", "simple")),
            border_inset_pt=float(data.get("border_inset_pt", 0.0)),
        )
