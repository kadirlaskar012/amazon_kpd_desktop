"""
Data models for KDP Project Documents, Settings, Trims, and Metadata.
All internal dimensions are stored in typographic points (72 pt/in).
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid

from app.core.units import Unit, in_to_pt, pt_to_in


class BookType(str, Enum):
    COLORING_BOOK = "coloring_book"
    SUDOKU = "sudoku"
    TIC_TAC_TOE = "tic_tac_toe"
    ACTIVITY_BOOK = "activity_book"
    PUZZLE_BOOK = "puzzle_book"
    MAZE = "maze"
    DOT_TO_DOT = "dot_to_dot"
    TRACING = "tracing"
    WORD_SEARCH = "word_search"
    LEARNING = "learning"

    @property
    def display_name(self) -> str:
        names = {
            BookType.COLORING_BOOK: "Coloring Book",
            BookType.SUDOKU: "Sudoku Book",
            BookType.TIC_TAC_TOE: "Tic-Tac-Toe Book",
            BookType.ACTIVITY_BOOK: "Activity Book",
            BookType.PUZZLE_BOOK: "Puzzle Book",
            BookType.MAZE: "Maze Book",
            BookType.DOT_TO_DOT: "Dot-to-Dot Book",
            BookType.TRACING: "Tracing Book",
            BookType.WORD_SEARCH: "Word Search Book",
            BookType.LEARNING: "Kids Learning Workbook",
        }
        return names.get(self, self.value.replace("_", " ").title())


@dataclass
class TrimPreset:
    id: str
    name: str
    width_in: float
    height_in: float
    description: str = ""

    @property
    def width_pt(self) -> float:
        return in_to_pt(self.width_in)

    @property
    def height_pt(self) -> float:
        return in_to_pt(self.height_in)


# Standard Amazon KDP Trim Sizes for Children's and Activity Books
KDP_TRIM_PRESETS: List[TrimPreset] = [
    TrimPreset("8.5x11", "8.5 x 11 in", 8.5, 11.0, "Standard Children's Coloring Book"),
    TrimPreset("8x10", "8 x 10 in", 8.0, 10.0, "Popular Activity & Workbook Format"),
    TrimPreset("8.5x8.5", "8.5 x 8.5 in", 8.5, 8.5, "Square Children's Picture/Coloring Book"),
    TrimPreset("7x10", "7 x 10 in", 7.0, 10.0, "Medium Activity Book"),
    TrimPreset("6x9", "6 x 9 in", 6.0, 9.0, "Standard Trade / Compact Activity Book"),
    TrimPreset("custom", "Custom Size", 8.5, 11.0, "User-defined Dimensions"),
]


@dataclass
class MarginSettings:
    top_pt: float = field(default_factory=lambda: in_to_pt(0.375))
    bottom_pt: float = field(default_factory=lambda: in_to_pt(0.375))
    inside_pt: float = field(default_factory=lambda: in_to_pt(0.500))  # Gutter (binding side)
    outside_pt: float = field(default_factory=lambda: in_to_pt(0.375))

    def to_dict(self) -> Dict[str, float]:
        return {
            "top": self.top_pt,
            "bottom": self.bottom_pt,
            "inside": self.inside_pt,
            "outside": self.outside_pt,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MarginSettings":
        return cls(
            top_pt=float(data.get("top", in_to_pt(0.375))),
            bottom_pt=float(data.get("bottom", in_to_pt(0.375))),
            inside_pt=float(data.get("inside", in_to_pt(0.500))),
            outside_pt=float(data.get("outside", in_to_pt(0.375))),
        )


@dataclass
class PageNumberingSettings:
    enabled: bool = False
    start_number: int = 1
    start_page_index: int = 0
    position: str = "bottom_center"  # bottom_center, bottom_outside, top_center, top_outside
    font_family: str = "Segoe UI"
    font_size_pt: float = 10.0
    format_pattern: str = "{number}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "enabled": self.enabled,
            "start_number": self.start_number,
            "start_page_index": self.start_page_index,
            "position": self.position,
            "font_family": self.font_family,
            "font_size_pt": self.font_size_pt,
            "format": self.format_pattern,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PageNumberingSettings":
        return cls(
            enabled=bool(data.get("enabled", False)),
            start_number=int(data.get("start_number", 1)),
            start_page_index=int(data.get("start_page_index", 0)),
            position=str(data.get("position", "bottom_center")),
            font_family=str(data.get("font_family", "Segoe UI")),
            font_size_pt=float(data.get("font_size_pt", 10.0)),
            format_pattern=str(data.get("format", "{number}")),
        )


@dataclass
class BookSettings:
    units: Unit = Unit.INCHES
    trim_preset_id: str = "8.5x11"
    trim_width_pt: float = field(default_factory=lambda: in_to_pt(8.5))
    trim_height_pt: float = field(default_factory=lambda: in_to_pt(11.0))
    is_landscape: bool = False
    has_bleed: bool = False
    bleed_pt: float = field(default_factory=lambda: in_to_pt(0.125))  # 9 pt bleed standard
    margins: MarginSettings = field(default_factory=MarginSettings)
    target_dpi: int = 300
    page_numbering: PageNumberingSettings = field(default_factory=PageNumberingSettings)

    @property
    def width_in(self) -> float:
        return pt_to_in(self.trim_width_pt)

    @property
    def height_in(self) -> float:
        return pt_to_in(self.trim_height_pt)

    @property
    def total_width_with_bleed_pt(self) -> float:
        """KDP Bleed: Add bleed to outside edge."""
        if not self.has_bleed:
            return self.trim_width_pt
        return self.trim_width_pt + self.bleed_pt

    @property
    def total_height_with_bleed_pt(self) -> float:
        """KDP Bleed: Add bleed to top and bottom edges."""
        if not self.has_bleed:
            return self.trim_height_pt
        return self.trim_height_pt + (self.bleed_pt * 2.0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "units": self.units.value,
            "trim_preset_id": self.trim_preset_id,
            "trim_width_pt": self.trim_width_pt,
            "trim_height_pt": self.trim_height_pt,
            "is_landscape": self.is_landscape,
            "has_bleed": self.has_bleed,
            "bleed_pt": self.bleed_pt,
            "margins_pt": self.margins.to_dict(),
            "target_dpi": self.target_dpi,
            "page_numbering": self.page_numbering.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BookSettings":
        units = Unit.from_string(data.get("units", "inches"))
        margins = MarginSettings.from_dict(data.get("margins_pt", {}))
        page_num = PageNumberingSettings.from_dict(data.get("page_numbering", {}))

        return cls(
            units=units,
            trim_preset_id=str(data.get("trim_preset_id", "8.5x11")),
            trim_width_pt=float(data.get("trim_width_pt", in_to_pt(8.5))),
            trim_height_pt=float(data.get("trim_height_pt", in_to_pt(11.0))),
            is_landscape=bool(data.get("is_landscape", False)),
            has_bleed=bool(data.get("has_bleed", False)),
            bleed_pt=float(data.get("bleed_pt", in_to_pt(0.125))),
            margins=margins,
            target_dpi=int(data.get("target_dpi", 300)),
            page_numbering=page_num,
        )


@dataclass
class CoverModel:
    page_count: int = 50
    paper_type: str = "white"
    spine_width_pt: float = field(default_factory=lambda: in_to_pt(0.1126))
    front_cover_asset_id: Optional[str] = None
    back_cover_asset_id: Optional[str] = None
    title: str = ""
    subtitle: str = ""
    author: str = ""
    spine_text: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_count": self.page_count,
            "paper_type": self.paper_type,
            "spine_width_pt": self.spine_width_pt,
            "front_cover_asset_id": self.front_cover_asset_id,
            "back_cover_asset_id": self.back_cover_asset_id,
            "title": self.title,
            "subtitle": self.subtitle,
            "author": self.author,
            "spine_text": self.spine_text,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CoverModel":
        return cls(
            page_count=int(data.get("page_count", 50)),
            paper_type=str(data.get("paper_type", "white")),
            spine_width_pt=float(data.get("spine_width_pt", in_to_pt(0.1126))),
            front_cover_asset_id=data.get("front_cover_asset_id"),
            back_cover_asset_id=data.get("back_cover_asset_id"),
            title=str(data.get("title", "")),
            subtitle=str(data.get("subtitle", "")),
            author=str(data.get("author", "")),
            spine_text=str(data.get("spine_text", "")),
        )


@dataclass
class ProjectDocument:
    schema_version: str = "1.0.0"
    project_id: str = field(default_factory=lambda: f"proj_{uuid.uuid4().hex[:12]}")
    name: str = "Untitled Book Project"
    author: str = ""
    publisher: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    module_type: str = BookType.COLORING_BOOK.value
    settings: BookSettings = field(default_factory=BookSettings)
    assets: List[Dict[str, Any]] = field(default_factory=list)
    pages: List[Dict[str, Any]] = field(default_factory=list)
    cover: CoverModel = field(default_factory=CoverModel)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def mark_updated(self) -> None:
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "project_id": self.project_id,
            "name": self.name,
            "author": self.author,
            "publisher": self.publisher,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "module_type": self.module_type,
            "settings": self.settings.to_dict(),
            "assets": self.assets,
            "pages": self.pages,
            "cover": self.cover.to_dict(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectDocument":
        settings_data = data.get("settings", {})
        settings = BookSettings.from_dict(settings_data)
        cover_data = data.get("cover", {})
        cover = CoverModel.from_dict(cover_data)

        return cls(
            schema_version=str(data.get("schema_version", "1.0.0")),
            project_id=str(data.get("project_id", f"proj_{uuid.uuid4().hex[:12]}")),
            name=str(data.get("name", "Untitled Book Project")),
            author=str(data.get("author", "")),
            publisher=str(data.get("publisher", "")),
            created_at=str(data.get("created_at", datetime.now(timezone.utc).isoformat())),
            updated_at=str(data.get("updated_at", datetime.now(timezone.utc).isoformat())),
            module_type=str(data.get("module_type", BookType.COLORING_BOOK.value)),
            settings=settings,
            assets=list(data.get("assets", [])),
            pages=list(data.get("pages", [])),
            cover=cover,
            metadata=dict(data.get("metadata", {})),
        )
