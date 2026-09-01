"""
ModuleRegistry discovers, registers, and provides access to all available Book Modules.
"""

from typing import Dict, List, Optional
from app.modules.base_module import BookModule
from app.modules.coloring_book.module import ColoringBookModule
from app.core.document_model import BookType
from app.core.template_model import TemplateModel


class PlaceholderBookModule(BookModule):
    def __init__(self, book_type: BookType, display_name: str, description: str):
        self._type = book_type
        self._name = display_name
        self._desc = description

    @property
    def module_id(self) -> str:
        return self._type.value

    @property
    def display_name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._desc

    @property
    def is_available_in_v1(self) -> bool:
        return False

    def get_default_templates(self) -> List[TemplateModel]:
        return []

    def generate_pages_from_assets(self, assets, template, settings, auto_title=True):
        return []


class ModuleRegistry:
    _instance: Optional["ModuleRegistry"] = None

    def __init__(self):
        self._modules: Dict[str, BookModule] = {}
        self._register_default_modules()

    @classmethod
    def get_instance(cls) -> "ModuleRegistry":
        if cls._instance is None:
            cls._instance = ModuleRegistry()
        return cls._instance

    def _register_default_modules(self) -> None:
        # V1 Active Module
        self.register_module(ColoringBookModule())

        # Future Plugin Modules
        self.register_module(
            PlaceholderBookModule(
                BookType.TRACING_BOOK,
                "Tracing Book",
                "Alphabet, number, word, and curve line tracing sheets for early childhood education.",
            )
        )
        self.register_module(
            PlaceholderBookModule(
                BookType.ACTIVITY_BOOK,
                "Activity Book",
                "Mazes, matching games, spot-the-difference, and counting worksheets.",
            )
        )
        self.register_module(
            PlaceholderBookModule(
                BookType.PUZZLE_BOOK,
                "Puzzle Book",
                "Word searches, crosswords, sudoku, and logic grid generators.",
            )
        )
        self.register_module(
            PlaceholderBookModule(
                BookType.DOT_TO_DOT,
                "Dot-to-Dot",
                "Numbered sequential connect-the-dots illustration generator.",
            )
        )

    def register_module(self, module: BookModule) -> None:
        self._modules[module.module_id] = module

    def get_module(self, module_id: str) -> Optional[BookModule]:
        return self._modules.get(module_id)

    def get_all_modules(self) -> List[BookModule]:
        return list(self._modules.values())
