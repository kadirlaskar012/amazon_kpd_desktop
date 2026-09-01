"""
Global application settings and user preferences manager.
Persists recent projects, default units, default DPI, theme, and UI states.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

from app.core.units import Unit


class SettingsManager:
    _instance: Optional["SettingsManager"] = None

    def __init__(self, config_dir: Optional[Path] = None):
        if config_dir is None:
            config_dir = Path.home() / ".kdp_studio"
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "app_settings.json"
        self.recent_projects_file = self.config_dir / "recent_projects.json"

        self._settings: Dict[str, Any] = self._load_settings()
        self._recent_projects: List[Dict[str, Any]] = self._load_recent_projects()

    @classmethod
    def get_instance(cls) -> "SettingsManager":
        if cls._instance is None:
            cls._instance = SettingsManager()
        return cls._instance

    def _get_defaults(self) -> Dict[str, Any]:
        return {
            "default_project_dir": str(Path.home() / "Documents" / "KDP_Projects"),
            "default_units": "inches",
            "default_dpi": 300,
            "theme": "dark",  # "dark" or "light"
            "autosave_interval_sec": 3,
            "autosave_enabled": True,
            "max_recent_projects": 15,
            "render_quality": "high",
            "show_guides": True,
            "snap_to_guides": True,
            "snap_threshold_pt": 4.0,
        }

    def _load_settings(self) -> Dict[str, Any]:
        defaults = self._get_defaults()
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    defaults.update(saved)
            except Exception:
                pass
        return defaults

    def save_settings(self) -> None:
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=2)
        except Exception:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._settings[key] = value
        self.save_settings()

    # Convenience properties
    @property
    def default_units(self) -> Unit:
        return Unit.from_string(self.get("default_units", "inches"))

    @default_units.setter
    def default_units(self, unit: Unit) -> None:
        self.set("default_units", unit.value)

    @property
    def default_dpi(self) -> int:
        return int(self.get("default_dpi", 300))

    @property
    def default_project_dir(self) -> Path:
        p = Path(self.get("default_project_dir", str(Path.home() / "Documents" / "KDP_Projects")))
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def theme(self) -> str:
        return str(self.get("theme", "dark"))

    @theme.setter
    def theme(self, val: str) -> None:
        self.set("theme", val)

    # Recent projects management
    def _load_recent_projects(self) -> List[Dict[str, Any]]:
        if self.recent_projects_file.exists():
            try:
                with open(self.recent_projects_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def _save_recent_projects(self) -> None:
        try:
            with open(self.recent_projects_file, "w", encoding="utf-8") as f:
                json.dump(self._recent_projects, f, indent=2)
        except Exception:
            pass

    def get_recent_projects(self) -> List[Dict[str, Any]]:
        """Returns list of valid existing recent projects."""
        valid_projects = []
        for item in self._recent_projects:
            path_str = item.get("path")
            if path_str and Path(path_str).exists():
                valid_projects.append(item)
        if len(valid_projects) != len(self._recent_projects):
            self._recent_projects = valid_projects
            self._save_recent_projects()
        return valid_projects

    def add_recent_project(self, project_info: Dict[str, Any]) -> None:
        """Add or move project to top of recents."""
        path_str = project_info.get("path")
        if not path_str:
            return

        # Remove existing if present
        self._recent_projects = [p for p in self._recent_projects if p.get("path") != path_str]
        # Insert at front
        self._recent_projects.insert(0, project_info)

        max_count = self.get("max_recent_projects", 15)
        self._recent_projects = self._recent_projects[:max_count]
        self._save_recent_projects()

    def remove_recent_project(self, path_str: str) -> None:
        self._recent_projects = [p for p in self._recent_projects if p.get("path") != path_str]
        self._save_recent_projects()
