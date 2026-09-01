"""
Sudoku Book Module implementation.
Generates complete Sudoku puzzle books with automated puzzle numbering and linked solution pages.
"""

from typing import List, Optional, Dict, Any
from PySide6.QtWidgets import QWidget

from app.core.document_model import BookType, BookSettings
from app.core.template_model import TemplateModel
from app.core.page_model import PageModel, ElementModel, ElementType
from app.core.asset_model import AssetModel
from app.modules.base_module import BookModule
from app.generators.sudoku_generator import SudokuGenerator


class SudokuBookModule(BookModule):
    @property
    def module_id(self) -> str:
        return BookType.SUDOKU.value

    @property
    def display_name(self) -> str:
        return "Sudoku Puzzle Book"

    @property
    def description(self) -> str:
        return "Generate 9x9 Sudoku puzzle books (Easy, Medium, Hard, Expert) with customizable grids, titles, and automatic solution sections."

    @property
    def is_available_in_v1(self) -> bool:
        return True

    def get_default_templates(self) -> List[TemplateModel]:
        return [
            TemplateModel(
                template_id="sudoku_1_per_page",
                name="1 Sudoku Per Page (Large Print)",
                category="sudoku",
                description="Single large 9x9 Sudoku grid centered on the page with difficulty header."
            ),
            TemplateModel(
                template_id="sudoku_2_per_page",
                name="2 Sudokus Per Page (Standard)",
                category="sudoku",
                description="Two medium 9x9 Sudoku grids stacked vertically with headers."
            ),
            TemplateModel(
                template_id="sudoku_4_per_page",
                name="4 Sudokus Per Page (Compact)",
                category="sudoku",
                description="Four 9x9 Sudoku grids in a 2x2 grid layout."
            ),
            TemplateModel(
                template_id="sudoku_solutions_6_per_page",
                name="Solution Section (6 Per Page)",
                category="sudoku",
                description="Compact 3x2 solution grid for end-of-book solutions."
            )
        ]

    def generate_pages_from_assets(
        self,
        assets: List[AssetModel],
        template: TemplateModel,
        settings: BookSettings,
        auto_title: bool = True,
    ) -> List[PageModel]:
        return []

    def generate_bulk_book(
        self,
        total_puzzles: int = 100,
        difficulty: str = "medium",
        puzzles_per_page: int = 1,
        include_solutions: bool = True,
        solutions_per_page: int = 6
    ) -> List[PageModel]:
        """
        Generates full book pages containing puzzles and linked solutions.
        """
        puzzles = SudokuGenerator.generate_bulk(count=total_puzzles, difficulty=difficulty)
        pages: List[PageModel] = []

        # 1. Generate Puzzle Pages
        current_idx = 0
        while current_idx < len(puzzles):
            chunk = puzzles[current_idx : current_idx + puzzles_per_page]
            page = PageModel(
                page_number=len(pages) + 1,
                title=f"Sudoku Puzzles {chunk[0]['id'].replace('sudoku_', '#')} - {chunk[-1]['id'].replace('sudoku_', '#')}" if len(chunk) > 1 else f"Sudoku #{chunk[0]['id'].replace('sudoku_', '')}"
            )
            
            # Add header element
            page.elements.append(
                ElementModel(
                    type=ElementType.TEXT,
                    x_pt=50,
                    y_pt=50,
                    width_pt=512,
                    height_pt=35,
                    text=f"SUDOKU PUZZLE {chunk[0]['id'].replace('sudoku_', '#')}",
                    font_size_pt=18,
                    bold=True,
                    alignment="center"
                )
            )

            # Store puzzle payload in metadata
            page.metadata["puzzles"] = chunk
            pages.append(page)
            current_idx += puzzles_per_page

        # 2. Generate Solutions Pages
        if include_solutions:
            sol_idx = 0
            while sol_idx < len(puzzles):
                sol_chunk = puzzles[sol_idx : sol_idx + solutions_per_page]
                sol_page = PageModel(
                    page_number=len(pages) + 1,
                    title=f"Solutions {sol_chunk[0]['id'].replace('sudoku_', '#')} - {sol_chunk[-1]['id'].replace('sudoku_', '#')}"
                )
                sol_page.elements.append(
                    ElementModel(
                        type=ElementType.TEXT,
                        x_pt=50,
                        y_pt=40,
                        width_pt=512,
                        height_pt=30,
                        text="SOLUTIONS",
                        font_size=16,
                        bold=True,
                        alignment="center"
                    )
                )
                sol_page.metadata["solutions"] = sol_chunk
                pages.append(sol_page)
                sol_idx += solutions_per_page

        return pages
