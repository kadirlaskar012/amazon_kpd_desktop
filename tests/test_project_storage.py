"""
Unit tests for ProjectStorage atomic save/load and directory scaffolding.
"""

from pathlib import Path
import tempfile
import pytest

from app.core.document_model import ProjectDocument, BookSettings
from app.storage.project_storage import ProjectStorage


def test_project_storage_scaffolding_and_save():
    with tempfile.TemporaryDirectory() as tmp_dir:
        proj_dir = Path(tmp_dir) / "MyColoringBook"

        doc = ProjectDocument(
            name="My Coloring Book",
            author="Test Author",
            settings=BookSettings(),
        )

        saved_path = ProjectStorage.save_project(proj_dir, doc)
        assert saved_path.exists()
        assert (proj_dir / "project.json").is_file()

        # Check subdirectories
        for sub in ["assets", "pages", "previews", "exports", "cover", "cache"]:
            assert (proj_dir / sub).is_dir()

        # Reload
        loaded_doc = ProjectStorage.load_project(proj_dir)
        assert loaded_doc.name == "My Coloring Book"
        assert loaded_doc.author == "Test Author"
        assert loaded_doc.settings.trim_width_pt == doc.settings.trim_width_pt


def test_atomic_backup_creation():
    with tempfile.TemporaryDirectory() as tmp_dir:
        proj_dir = Path(tmp_dir) / "BackupTest"

        doc1 = ProjectDocument(name="Version 1")
        ProjectStorage.save_project(proj_dir, doc1)

        # Save Version 2
        doc2 = ProjectDocument(name="Version 2")
        ProjectStorage.save_project(proj_dir, doc2)

        assert (proj_dir / "project.json.bak").is_file()
        loaded_doc = ProjectStorage.load_project(proj_dir)
        assert loaded_doc.name == "Version 2"


def test_invalid_project_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        empty_dir = Path(tmp_dir) / "Empty"
        empty_dir.mkdir()
        assert not ProjectStorage.is_valid_project_dir(empty_dir)

        with pytest.raises(FileNotFoundError):
            ProjectStorage.load_project(empty_dir)
