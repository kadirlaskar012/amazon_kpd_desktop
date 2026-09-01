"""
ModuleRegistry discovers, registers, and provides access to all available Book Modules.
"""

from typing import Dict, List, Optional
from app.modules.base_module import BookModule
from app.modules.coloring_book.module import ColoringBookModule
from app.modules.sudoku.module import SudokuBookModule
from app.modules.tic_tac_toe.module import TicTacToeBookModule
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
        # V1 Active Module 1: Coloring Book
        self.register_module(ColoringBookModule())

        # V1 Active Module 2: Sudoku Book
        self.register_module(SudokuBookModule())

        # V1 Active Module 3: Tic-Tac-Toe Book
        self.register_module(TicTacToeBookModule())
        # 4. Activity Book
        self.register_module(
            PlaceholderBookModule(
                BookType.ACTIVITY_BOOK,
                "Activity Book",
                "Mixed activities: Mazes, matching games, spot-the-difference, counting, and pattern worksheets.",
            )
        )
        # 5. Puzzle Book
        self.register_module(
            PlaceholderBookModule(
                BookType.PUZZLE_BOOK,
                "Puzzle Book",
                "Crosswords, word scrambles, logic puzzles, and number grids.",
            )
        )
        # 6. Maze Book
        self.register_module(
            PlaceholderBookModule(
                BookType.MAZE,
                "Maze Book",
                "Algorithmic labyrinth generation with guaranteed single path solutions.",
            )
        )
        # 7. Dot-to-Dot Book
        self.register_module(
            PlaceholderBookModule(
                BookType.DOT_TO_DOT,
                "Dot-to-Dot Book",
                "Numbered point sequences and animal connect-the-dots worksheets.",
            )
        )
        # 8. Tracing Book
        self.register_module(
            PlaceholderBookModule(
                BookType.TRACING,
                "Tracing Book",
                "Alphabet, numbers, dotted words, and handwriting practice lines.",
            )
        )
        # 9. Word Search Book
        self.register_module(
            PlaceholderBookModule(
                BookType.WORD_SEARCH,
                "Word Search Book",
                "Multi-directional word search puzzles with themed vocabulary and solution keys.",
            )
        )
        # 10. Kids Learning Workbook
        self.register_module(
            PlaceholderBookModule(
                BookType.LEARNING,
                "Kids Learning Workbook",
                "Early childhood math, shapes, vocabulary, and handwriting readiness workbooks.",
            )
        )

    def register_module(self, module: BookModule) -> None:
        self._modules[module.module_id] = module

    def get_module(self, module_id: str) -> Optional[BookModule]:
        return self._modules.get(module_id)

    def get_all_modules(self) -> List[BookModule]:
        return list(self._modules.values())
