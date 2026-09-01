"""
Tic-Tac-Toe Game Book Module implementation.
Generates printable game books with 1, 2, 4, or 6 games per page.
"""

from typing import List, Optional, Dict, Any
from PySide6.QtWidgets import QWidget

from app.core.document_model import BookType, BookSettings
from app.core.template_model import TemplateModel
from app.core.page_model import PageModel, ElementModel, ElementType
from app.core.asset_model import AssetModel
from app.modules.base_module import BookModule
from app.generators.tic_tac_toe_generator import TicTacToeGenerator


class TicTacToeBookModule(BookModule):
    @property
    def module_id(self) -> str:
        return BookType.TIC_TAC_TOE.value

    @property
    def display_name(self) -> str:
        return "Tic-Tac-Toe Book"

    @property
    def description(self) -> str:
        return "Printable 3x3 game pages with custom headers, scores, player tags, and multiple grids per page."

    @property
    def is_available_in_v1(self) -> bool:
        return True

    def get_default_templates(self) -> List[TemplateModel]:
        return [
            TemplateModel(
                template_id="ttt_4_per_page",
                name="4 Games Per Page (2x2 Grid)",
                category="tic_tac_toe",
                description="Four 3x3 Tic-Tac-Toe games with player lines and score boxes."
            ),
            TemplateModel(
                template_id="ttt_2_per_page",
                name="2 Games Per Page (Medium)",
                category="tic_tac_toe",
                description="Two medium sized game grids stacked vertically."
            ),
            TemplateModel(
                template_id="ttt_1_per_page",
                name="1 Game Per Page (Giant Grid)",
                category="tic_tac_toe",
                description="Single giant game grid for toddlers & large print."
            ),
            TemplateModel(
                template_id="ttt_6_per_page",
                name="6 Games Per Page (Compact)",
                category="tic_tac_toe",
                description="Six compact game grids in a 3x2 grid layout."
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
        total_games: int = 100,
        games_per_page: int = 4,
        grid_size: int = 3
    ) -> List[PageModel]:
        """Generates full pages populated with structured Tic-Tac-Toe game grids."""
        raw_pages = TicTacToeGenerator.generate_bulk(
            total_games=total_games,
            games_per_page=games_per_page,
            grid_size=grid_size
        )
        pages: List[PageModel] = []

        for p_data in raw_pages:
            p_num = p_data.get("page_number", len(pages) + 1)
            first_g = p_data["games"][0]["game_number"]
            last_g = p_data["games"][-1]["game_number"]
            
            page = PageModel(
                page_number=p_num,
                title=f"Tic-Tac-Toe Games #{first_g:03d} - #{last_g:03d}" if first_g != last_g else f"Tic-Tac-Toe Game #{first_g:03d}"
            )
            page.elements.append(
                ElementModel(
                    type=ElementType.TEXT,
                    x_pt=50,
                    y_pt=40,
                    width_pt=512,
                    height_pt=30,
                    text="TIC-TAC-TOE",
                    font_size=18,
                    bold=True,
                    alignment="center"
                )
            )
            page.metadata["tic_tac_toe"] = p_data
            pages.append(page)

        return pages
