"""
Asset data models for tracking raw & processed images, dimensions, DPI, and assignments.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid


class AssetStatus(str, Enum):
    READY = "ready"
    PROCESSING = "processing"
    WARNING = "warning"
    ERROR = "error"
    MISSING = "missing"


@dataclass
class AssetModel:
    asset_id: str = field(default_factory=lambda: f"asset_{uuid.uuid4().hex[:8]}")
    filename: str = ""
    rel_path: str = ""  # Relative to project assets/ folder
    width_px: int = 0
    height_px: int = 0
    dpi: float = 300.0
    file_size_bytes: int = 0
    file_format: str = "PNG"
    status: AssetStatus = AssetStatus.READY
    assigned_page_indices: List[int] = field(default_factory=list)
    sha256_hash: Optional[str] = None
    processed_line_art_rel_path: Optional[str] = None

    @property
    def is_used(self) -> bool:
        return len(self.assigned_page_indices) > 0

    @property
    def aspect_ratio(self) -> float:
        if self.height_px == 0:
            return 1.0
        return float(self.width_px) / float(self.height_px)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "filename": self.filename,
            "rel_path": self.rel_path,
            "width_px": self.width_px,
            "height_px": self.height_px,
            "dpi": self.dpi,
            "file_size_bytes": self.file_size_bytes,
            "file_format": self.file_format,
            "status": self.status.value if isinstance(self.status, AssetStatus) else str(self.status),
            "assigned_page_indices": self.assigned_page_indices,
            "sha256_hash": self.sha256_hash,
            "processed_line_art_rel_path": self.processed_line_art_rel_path,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AssetModel":
        status_raw = data.get("status", "ready")
        try:
            status = AssetStatus(status_raw)
        except ValueError:
            status = AssetStatus.READY

        return cls(
            asset_id=str(data.get("asset_id", f"asset_{uuid.uuid4().hex[:8]}")),
            filename=str(data.get("filename", "")),
            rel_path=str(data.get("rel_path", "")),
            width_px=int(data.get("width_px", 0)),
            height_px=int(data.get("height_px", 0)),
            dpi=float(data.get("dpi", 300.0)),
            file_size_bytes=int(data.get("file_size_bytes", 0)),
            file_format=str(data.get("file_format", "PNG")),
            status=status,
            assigned_page_indices=list(data.get("assigned_page_indices", [])),
            sha256_hash=data.get("sha256_hash"),
            processed_line_art_rel_path=data.get("processed_line_art_rel_path"),
        )
