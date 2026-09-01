"""
Abstract Base Class for Book Modules (Coloring, Tracing, Activity, Puzzles, etc.).
Provides a pluggable architecture so new book creators can be added without modifying core files.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
from PySide6.QtWidgets import QWidget

from app.core.document_model import BookType, BookSettings, ProjectDocument
from app.core.template_model import TemplateModel
from app.core.page_model import PageModel
from app.core.asset_model import AssetModel


class BookModule(ABC):
    @property
    @abstractmethod
    def module_id(self) -> str:
        """Unique identifier (e.g. 'coloring_book', 'tracing_book')"""
        pass

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-friendly name"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Short summary of book type capabilities"""
        pass

    @property
    @abstractmethod
    def is_available_in_v1(self) -> bool:
        """True if fully implemented in V1, False if Coming Soon"""
        pass

    @abstractmethod
    def get_default_templates(self) -> List[TemplateModel]:
        """Returns standard templates provided by this module"""
        pass

    @abstractmethod
    def generate_pages_from_assets(
        self,
        assets: List[AssetModel],
        template: TemplateModel,
        settings: BookSettings,
        auto_title: bool = True,
    ) -> List[PageModel]:
        """Automated page batch generation pipeline"""
        pass

    def create_custom_tools_widget(self) -> Optional[QWidget]:
        """Optional custom side panel for module-specific canvas tools"""
        return None
