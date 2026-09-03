"""
Physical disk storage, atomic project serialization, and directory scaffolding.
"""

import json
import os
from pathlib import Path
import shutil
import tempfile
from typing import Dict, Any, Optional

from app.core.document_model import ProjectDocument


class ProjectStorage:
    PROJECT_FILE_NAME = "project.json"
    TMP_EXT = ".tmp"
    BAK_EXT = ".bak"

    SUBDIRECTORIES = [
        "media",
        "assets",
        "pages",
        "previews",
        "exports",
        "cover",
        "cache",
    ]

    @classmethod
    def initialize_project_directory(cls, base_dir: Path) -> Path:
        """Create project folder structure and subdirectories."""
        base_dir = Path(base_dir).resolve()
        base_dir.mkdir(parents=True, exist_ok=True)

        for sub in cls.SUBDIRECTORIES:
            (base_dir / sub).mkdir(parents=True, exist_ok=True)

        return base_dir

    @classmethod
    def save_project(cls, project_dir: Path, doc: ProjectDocument) -> Path:
        """
        Atomically save ProjectDocument to project.json.
        1. Write to project.json.tmp
        2. Backup existing project.json to project.json.bak if it exists
        3. Atomically replace project.json with .tmp
        """
        project_dir = Path(project_dir).resolve()
        cls.initialize_project_directory(project_dir)

        target_file = project_dir / cls.PROJECT_FILE_NAME
        tmp_file = project_dir / f"{cls.PROJECT_FILE_NAME}{cls.TMP_EXT}"
        bak_file = project_dir / f"{cls.PROJECT_FILE_NAME}{cls.BAK_EXT}"

        doc.mark_updated()
        data = doc.to_dict()

        # 1. Write to temporary file with UTF-8 encoding
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())

        # 2. Make backup of existing file
        if target_file.exists():
            try:
                shutil.copy2(target_file, bak_file)
            except Exception:
                pass

        # 3. Atomic replacement
        if target_file.exists():
            target_file.unlink()
        tmp_file.rename(target_file)

        return target_file

    @classmethod
    def load_project(cls, project_dir: Path) -> ProjectDocument:
        """Load project.json from directory."""
        project_dir = Path(project_dir).resolve()
        target_file = project_dir / cls.PROJECT_FILE_NAME

        if not target_file.exists():
            # Check for backup file in case of power loss during previous write
            bak_file = project_dir / f"{cls.PROJECT_FILE_NAME}{cls.BAK_EXT}"
            if bak_file.exists():
                target_file = bak_file
            else:
                raise FileNotFoundError(f"No {cls.PROJECT_FILE_NAME} found in {project_dir}")

        with open(target_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        return ProjectDocument.from_dict(data)

    @classmethod
    def is_valid_project_dir(cls, directory: Path) -> bool:
        """Check if directory contains a readable project.json."""
        p = Path(directory)
        return (p / cls.PROJECT_FILE_NAME).is_file() or (p / f"{cls.PROJECT_FILE_NAME}{cls.BAK_EXT}").is_file()
