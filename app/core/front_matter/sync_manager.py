"""
Contents Synchronization Manager for KDP Studio.
Keeps Table of Contents pages in sync with document changes when auto_sync is ON.
"""

from typing import Dict, Any, List, Optional
from .front_matter_models import FrontMatterConfig
from .contents_generator import ContentsGenerator


class ContentsSyncManager:
    @staticmethod
    def sync_contents_page(project_data: Dict[str, Any], config: Optional[FrontMatterConfig] = None) -> bool:
        """
        Synchronizes the contents page with the actual pages in the project.
        Returns True if a contents page was found and updated.
        """
        if config is None:
            config_dict = project_data.get("front_matter_config", {})
            config = FrontMatterConfig.from_dict(config_dict)

        if not config.auto_sync_contents:
            return False

        pages: List[Dict[str, Any]] = project_data.get("pages", [])
        contents_page_idx = -1

        for idx, p in enumerate(pages):
            if p.get("page_type") == "front_matter_contents" or p.get("layout") == "contents_standard":
                contents_page_idx = idx
                break

        if contents_page_idx == -1:
            return False

        current_contents_page = pages[contents_page_idx]
        if current_contents_page.get("is_locked", False):
            return False

        # Generate fresh synchronized contents elements
        updated_contents = ContentsGenerator.generate_contents_page(
            project_data=project_data,
            config=config,
            page_num=current_contents_page.get("page_number", contents_page_idx + 1)
        )

        current_contents_page["elements"] = updated_contents["elements"]
        return True
