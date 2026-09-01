"""
Front Matter Engine for KDP Book Creation Studio.
Orchestrates automated disclaimer, copyright, and contents creation for any book project.
"""

from typing import Dict, Any, List, Optional
from .front_matter_models import FrontMatterConfig, DisclaimerFieldsConfig, PageType
from .disclaimer_generator import DisclaimerGenerator
from .contents_generator import ContentsGenerator
from .title_resolver import TitleResolver
from .sync_manager import ContentsSyncManager


class FrontMatterEngine:
    @classmethod
    def apply_front_matter_to_project(
        cls,
        project_data: Dict[str, Any],
        config: Optional[FrontMatterConfig] = None
    ) -> Dict[str, Any]:
        """
        Inserts Disclaimer and Contents pages at the start of the project if enabled.
        """
        if config is None:
            config_dict = project_data.get("front_matter_config", {})
            config = FrontMatterConfig.from_dict(config_dict)

        if not config.auto_front_matter:
            return project_data

        existing_pages = project_data.get("pages", [])

        # Remove previous front matter pages if regenerating
        content_pages = [
            p for p in existing_pages 
            if p.get("page_type") not in ("front_matter_disclaimer", "front_matter_contents")
        ]

        front_pages = []

        # 1. Generate Disclaimer Page
        if config.create_disclaimer:
            disclaimer_page = DisclaimerGenerator.generate_disclaimer_page(project_data, config)
            front_pages.append(disclaimer_page)

        # 2. Generate Contents Page
        if config.create_contents:
            contents_page_num = len(front_pages) + 1
            contents_page = ContentsGenerator.generate_contents_page(
                project_data={"name": project_data.get("name"), "pages": content_pages},
                config=config,
                page_num=contents_page_num
            )
            front_pages.append(contents_page)

        # Re-number content pages sequentially after front matter
        start_idx = len(front_pages) + 1
        for idx, page in enumerate(content_pages):
            page["page_number"] = start_idx + idx
            page["page_type"] = "content"

        project_data["pages"] = front_pages + content_pages
        project_data["front_matter_config"] = config.to_dict()
        return project_data

    @classmethod
    def sync_project_contents(cls, project_data: Dict[str, Any]) -> bool:
        """
        Synchronizes the contents page with the latest project state.
        """
        return ContentsSyncManager.sync_contents_page(project_data)
