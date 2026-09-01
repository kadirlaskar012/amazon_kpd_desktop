"""
Title Resolver for KDP Book Studio.
Resolves human-friendly page titles with priority:
1. Manually assigned Page Title
2. Canvas/Page Title Element text
3. Cleaned Imported Image Filename
4. Fallback default page number
"""

import re
from typing import Dict, Any, Optional


class TitleResolver:
    @staticmethod
    def clean_filename_to_title(filename: str) -> str:
        """
        Converts messy filenames into beautiful book titles.
        Example: 'cute_lion.png' -> 'Cute Lion'
        Example: '01_big-elephant-coloring-page.jpg' -> 'Big Elephant Coloring Page'
        """
        if not filename or not isinstance(filename, str):
            return "Untitled Artwork"

        # 1. Strip file extension
        name = re.sub(r"\.[a-zA-Z0-9]+$", "", filename)

        # 2. Strip leading numbers or numbering prefixes (e.g., '01_', 'page-2-', '003 ')
        name = re.sub(r"^(page\s*[\-_]*)?\d+[\s_\.\-]+", "", name, flags=re.IGNORECASE)

        # 3. Strip common trailing tags like '-coloring-page', '_lineart', '_bw'
        name = re.sub(r"[\-_](coloring[\-_]?page|lineart|drawing|illustration|vector|bw|art)$", "", name, flags=re.IGNORECASE)

        # 4. Replace underscores, hyphens, and multi-spaces with single space
        name = re.sub(r"[_\-]+", " ", name)
        name = re.sub(r"\s+", " ", name).strip()

        # 5. Title Case conversion
        words = name.split()
        title_words = []
        lower_exceptions = {"a", "an", "the", "and", "but", "or", "for", "nor", "on", "at", "to", "from", "by", "of", "in"}
        for i, w in enumerate(words):
            if i > 0 and w.lower() in lower_exceptions:
                title_words.append(w.lower())
            else:
                title_words.append(w.capitalize())

        result = " ".join(title_words)
        return result if result else "Untitled Artwork"

    @classmethod
    def resolve_page_title(cls, page_dict: Dict[str, Any], page_index: int = 1) -> str:
        """
        Resolves title according to strict 3-tier priority hierarchy.
        """
        # Tier 1: Manually assigned title (if non-empty and not generic 'Page N')
        manual_title = page_dict.get("title", "")
        if manual_title and isinstance(manual_title, str):
            clean_manual = manual_title.strip()
            # If user provided a genuine custom title (not just 'Page 1' or default)
            if clean_manual and not re.match(r"^Page\s*\d+$", clean_manual, flags=re.IGNORECASE):
                return clean_manual

        # Tier 2: Canvas Title element text
        elements = page_dict.get("elements", [])
        for elem in elements:
            if elem.get("type") == "title":
                elem_txt = (elem.get("text") or "").strip()
                if elem_txt and not re.match(r"^PAGE\s*\d+$", elem_txt, flags=re.IGNORECASE):
                    # Convert ALL CAPS canvas title to Title Case for Contents List
                    return cls.clean_filename_to_title(elem_txt)

        # Tier 3: Imported Image filename from main_image or ref_image
        for elem in elements:
            if elem.get("type") in ("main_image", "ref_image"):
                # Check explicit text / label
                img_name = elem.get("text", "")
                if img_name and not "click to select" in img_name.lower():
                    return cls.clean_filename_to_title(img_name)
                # Check filename attribute if present
                img_fname = elem.get("fileName") or elem.get("filename")
                if img_fname:
                    return cls.clean_filename_to_title(img_fname)

        # Tier 4: Fallback
        return f"Page {page_dict.get('page_number', page_index)}"
