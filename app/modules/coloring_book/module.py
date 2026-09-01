"""
Coloring Book Module implementation.
"""

from typing import List, Optional
from PySide6.QtWidgets import QWidget

from app.core.document_model import BookType, BookSettings
from app.core.template_model import TemplateModel
from app.core.page_model import PageModel
from app.core.asset_model import AssetModel
from app.modules.base_module import BookModule
from app.modules.coloring_book.templates import get_coloring_book_templates
from app.modules.coloring_book.generator import generate_coloring_pages


class ColoringBookModule(BookModule):
    @property
    def module_id(self) -> str:
        return BookType.COLORING_BOOK.value

    @property
    def display_name(self) -> str:
        return "Coloring Book"

    @property
    def description(self) -> str:
        return "Create beautiful children's and adult coloring books with reference thumbnails, bold titles, and standard safe margins."

    @property
    def is_available_in_v1(self) -> bool:
        return True

    def get_default_templates(self) -> List[TemplateModel]:
        return get_coloring_book_templates()

    def generate_pages_from_assets(
        self,
        assets: List[AssetModel],
        template: TemplateModel,
        settings: BookSettings,
        auto_title: bool = True,
    ) -> List[PageModel]:
        return generate_coloring_pages(
            assets=assets,
            template=template,
            settings=settings,
            auto_title=auto_title,
        )

    def create_custom_tools_widget(self) -> Optional[QWidget]:
        # In Milestone 4, this will embed OpenCV non-AI line extraction sliders
        return None
