"""
ProjectManager coordinates project lifecycle, current document state, autosaving,
and recent project updates.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable

from app.core.document_model import (
    ProjectDocument,
    BookSettings,
    BookType,
    TrimPreset,
    KDP_TRIM_PRESETS,
    MarginSettings,
)
from app.core.settings_manager import SettingsManager
from app.storage.project_storage import ProjectStorage


class ProjectManager:
    _instance: Optional["ProjectManager"] = None

    def __init__(self):
        self.current_project_dir: Optional[Path] = None
        self.current_document: Optional[ProjectDocument] = None
        self.is_dirty: bool = False
        self.settings_manager = SettingsManager.get_instance()

        # Callbacks / event listeners (can be connected to PySide6 signals in UI)
        self._on_project_changed_callbacks: List[Callable[[Optional[ProjectDocument]], None]] = []
        self._on_saved_callbacks: List[Callable[[Path], None]] = []
        self._on_dirty_changed_callbacks: List[Callable[[bool], None]] = []

    @classmethod
    def get_instance(cls) -> "ProjectManager":
        if cls._instance is None:
            cls._instance = ProjectManager()
        return cls._instance

    def register_project_changed_listener(self, cb: Callable[[Optional[ProjectDocument]], None]) -> None:
        self._on_project_changed_callbacks.append(cb)

    def register_saved_listener(self, cb: Callable[[Path], None]) -> None:
        self._on_saved_callbacks.append(cb)

    def register_dirty_listener(self, cb: Callable[[bool], None]) -> None:
        self._on_dirty_changed_callbacks.append(cb)

    def _notify_project_changed(self) -> None:
        for cb in self._on_project_changed_callbacks:
            try:
                cb(self.current_document)
            except Exception:
                pass

    def _notify_saved(self, path: Path) -> None:
        for cb in self._on_saved_callbacks:
            try:
                cb(path)
            except Exception:
                pass

    def _notify_dirty_changed(self, dirty: bool) -> None:
        for cb in self._on_dirty_changed_callbacks:
            try:
                cb(dirty)
            except Exception:
                pass

    def create_new_project(
        self,
        name: str,
        location_dir: Path,
        author: str = "",
        publisher: str = "",
        book_type: BookType = BookType.COLORING_BOOK,
        trim_preset: Optional[TrimPreset] = None,
        has_bleed: bool = False,
    ) -> ProjectDocument:
        """Create a new project folder, scaffold directories, and save initial project.json."""
        project_dir = Path(location_dir).resolve()
        ProjectStorage.initialize_project_directory(project_dir)

        if trim_preset is None:
            trim_preset = KDP_TRIM_PRESETS[0]  # 8.5 x 11 in default

        settings = BookSettings(
            units=self.settings_manager.default_units,
            trim_preset_id=trim_preset.id,
            trim_width_pt=trim_preset.width_pt,
            trim_height_pt=trim_preset.height_pt,
            has_bleed=has_bleed,
            margins=MarginSettings(),
            target_dpi=self.settings_manager.default_dpi,
        )

        doc = ProjectDocument(
            name=name.strip() or "Untitled Book Project",
            author=author.strip(),
            publisher=publisher.strip(),
            module_type=book_type.value,
            settings=settings,
        )

        ProjectStorage.save_project(project_dir, doc)

        self.current_project_dir = project_dir
        self.current_document = doc
        self.set_dirty(False)

        # Update recents
        self._record_recent(project_dir, doc)
        self._notify_project_changed()
        return doc

    def open_project(self, project_dir: Path) -> ProjectDocument:
        """Load an existing project directory."""
        project_dir = Path(project_dir).resolve()
        doc = ProjectStorage.load_project(project_dir)

        self.current_project_dir = project_dir
        self.current_document = doc
        self.set_dirty(False)

        self._record_recent(project_dir, doc)
        self._notify_project_changed()
        return doc

    def save_current_project(self) -> Optional[Path]:
        """Save active document to disk."""
        if not self.current_document or not self.current_project_dir:
            return None

        saved_path = ProjectStorage.save_project(self.current_project_dir, self.current_document)
        self.set_dirty(False)
        self._record_recent(self.current_project_dir, self.current_document)
        self._notify_saved(saved_path)
        return saved_path

    def close_current_project(self) -> None:
        """Close active document."""
        self.current_document = None
        self.current_project_dir = None
        self.set_dirty(False)
        self._notify_project_changed()

    def set_dirty(self, dirty: bool = True) -> None:
        if self.is_dirty != dirty:
            self.is_dirty = dirty
            self._notify_dirty_changed(dirty)

    def _record_recent(self, project_dir: Path, doc: ProjectDocument) -> None:
        self.settings_manager.add_recent_project({
            "name": doc.name,
            "path": str(project_dir),
            "book_type": doc.module_type,
            "page_count": len(doc.pages),
            "last_modified": datetime.now(timezone.utc).isoformat(),
        })
