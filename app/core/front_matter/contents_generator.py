"""
Table of Contents / Book List Page Generator for KDP Book Studio.
Generates fully editable vector canvas pages listing all content items, titles, and exact page numbers.
"""

from typing import Dict, Any, List, Optional
from .front_matter_models import FrontMatterConfig, ContentsListStyle
from .title_resolver import TitleResolver


class ContentsGenerator:
    @staticmethod
    def generate_contents_page(
        project_data: Dict[str, Any],
        config: Optional[FrontMatterConfig] = None,
        page_num: int = 2
    ) -> Dict[str, Any]:
        """
        Generates a standard editable Table of Contents / Book List Page.
        """
        if config is None:
            config = FrontMatterConfig()

        all_pages = project_data.get("pages", [])
        
        # Filter content pages (ignoring front matter pages if already present)
        content_pages = [p for p in all_pages if p.get("page_type") not in ("front_matter_disclaimer", "front_matter_contents")]
        
        elements: List[Dict[str, Any]] = []

        # 1. Outer Border Frame
        elements.append({
            "id": "contents_frame",
            "type": "border",
            "x": 35,
            "y": 30,
            "w": 440,
            "h": 600,
            "locked": False
        })

        # 2. Main Heading
        elements.append({
            "id": "contents_heading",
            "type": "title",
            "x": 45,
            "y": 60,
            "w": 420,
            "h": 40,
            "text": config.contents_heading or "TABLE OF CONTENTS",
            "font_size": 22,
            "color": "#0f172a",
            "alignment": "center"
        })

        # 3. Subtitle
        elements.append({
            "id": "contents_sub",
            "type": "title",
            "x": 45,
            "y": 95,
            "w": 420,
            "h": 20,
            "text": "Explore all the illustrations and coloring pages in this book",
            "font_size": 11,
            "color": "#64748b",
            "alignment": "center"
        })

        # 4. Generate Content List Items
        # If no content pages exist yet, supply placeholder demo list
        if not content_pages:
            content_items = [
                ("Cute Lion", 3),
                ("Playful Puppy", 4),
                ("Happy Cat", 5),
                ("Gentle Elephant", 6),
                ("Forest Deer", 7),
                ("Wise Owl", 8),
            ]
        else:
            content_items = []
            for idx, p in enumerate(content_pages):
                resolved_title = TitleResolver.resolve_page_title(p, idx + 1)
                actual_doc_page = p.get("page_number", idx + 3)
                content_items.append((resolved_title, actual_doc_page))

        start_y = 140
        row_height = 28
        max_rows_per_col = 14

        if len(content_items) <= max_rows_per_col:
            # Single Column Layout
            for i, (title, page_no) in enumerate(content_items):
                current_y = start_y + (i * row_height)
                
                # Format prefix
                if config.contents_style == "numbered":
                    prefix = f"{i + 1}."
                elif config.contents_style == "bullet":
                    prefix = "•"
                else:
                    prefix = ""

                # Title Text
                full_text = f"{prefix} {title}".strip()
                if config.show_page_numbers:
                    # Dotted leader
                    dots_count = max(4, 28 - len(title))
                    dots = "." * dots_count
                    display_line = f"{full_text} {dots} Page {page_no}"
                else:
                    display_line = full_text

                elements.append({
                    "id": f"contents_item_{i + 1}",
                    "type": "title",
                    "x": 65,
                    "y": current_y,
                    "w": 380,
                    "h": 24,
                    "text": display_line,
                    "font_size": 12,
                    "color": "#1e293b",
                    "alignment": "left"
                })
        else:
            # Dynamic Dual Column Layout: Fits ALL items strictly onto 1 single page
            num_rows = (len(content_items) + 1) // 2
            dyn_row_h = max(12, min(24, int(450 / max(1, num_rows))))
            dyn_font_sz = 8.5 if num_rows > 22 else (9.5 if num_rows > 14 else 10)

            col1 = content_items[:num_rows]
            col2 = content_items[num_rows:]

            for i, (title, page_no) in enumerate(col1):
                current_y = start_y + (i * dyn_row_h)
                line = f"{i + 1}. {title}" + (f" (p.{page_no})" if config.show_page_numbers else "")
                elements.append({
                    "id": f"contents_item_c1_{i + 1}",
                    "type": "title",
                    "x": 50,
                    "y": current_y,
                    "w": 200,
                    "h": dyn_row_h,
                    "text": line,
                    "font_size": dyn_font_sz,
                    "color": "#1e293b",
                    "alignment": "left"
                })

            for i, (title, page_no) in enumerate(col2):
                idx = i + num_rows
                current_y = start_y + (i * dyn_row_h)
                line = f"{idx + 1}. {title}" + (f" (p.{page_no})" if config.show_page_numbers else "")
                elements.append({
                    "id": f"contents_item_c2_{idx + 1}",
                    "type": "title",
                    "x": 260,
                    "y": current_y,
                    "w": 200,
                    "h": dyn_row_h,
                    "text": line,
                    "font_size": dyn_font_sz,
                    "color": "#1e293b",
                    "alignment": "left"
                })

        return {
            "page_number": page_num,
            "page_type": "front_matter_contents",
            "title": "Table of Contents",
            "layout": "contents_standard",
            "is_locked": False,
            "elements": elements
        }
