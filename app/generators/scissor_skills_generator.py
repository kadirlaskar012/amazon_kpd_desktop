"""
Scissor Skills & Cut-and-Paste Activity Book Generator
Generates progressive paper cutting exercises (straight, zigzag, wavy, curved, geometric)
and interactive cut-and-paste matching puzzles for preschool and kindergarten kids.
"""

from typing import Dict, List, Any, Optional


class ScissorSkillsGenerator:
    """Parametric Scissor Cutting Lines & Cut-and-Paste Activity Generator."""

    LINE_PATTERNS = ["straight", "zigzag", "wavy", "curved", "castle", "shapes"]

    @staticmethod
    def generate_cutting_practice_page(
        pattern_type: str = "zigzag",
        line_count: int = 5,
        title: str = "Cutting Practice"
    ) -> Dict[str, Any]:
        """Generate a page of cutting practice lines with scissor markers."""
        pattern = pattern_type.lower() if pattern_type.lower() in ScissorSkillsGenerator.LINE_PATTERNS else "zigzag"
        
        lines = []
        for i in range(line_count):
            lines.append({
                "index": i + 1,
                "pattern": pattern,
                "start_x": 40,
                "end_x": 470,
                "y": 100 + (i * 100),
                "scissor_icon": "✂",
                "stroke_dash": [8, 6],
                "target_icon": "⭐" if i % 2 == 0 else "🎯"
            })

        return {
            "type": "scissor_cutting",
            "pattern_type": pattern,
            "title": title or f"Fun {pattern.title()} Cutting Practice",
            "line_count": line_count,
            "instructions": "Carefully cut along the dotted lines from the scissors to the stars!",
            "lines": lines
        }

    @staticmethod
    def generate_cut_and_paste_page(
        theme_title: str = "Match & Paste the Jungle Animals",
        item_count: int = 4
    ) -> Dict[str, Any]:
        """Generate a cut-and-paste matching activity page."""
        items = [
            {"id": "cp_1", "name": "Lion", "icon": "🦁", "label": "King of the Jungle"},
            {"id": "cp_2", "name": "Elephant", "icon": "🐘", "label": "Gentle Giant"},
            {"id": "cp_3", "name": "Monkey", "icon": "🐒", "label": "Playful Climber"},
            {"id": "cp_4", "name": "Giraffe", "icon": "🦒", "label": "Tall & Friendly"}
        ][:item_count]

        return {
            "type": "cut_and_paste",
            "title": theme_title,
            "instructions": "1. Color the pictures. 2. Cut out the pieces at the bottom. 3. Paste them into the correct matching boxes above!",
            "target_boxes": [
                {"id": f"tb_{it['id']}", "label": it["label"], "expected_id": it["id"]} for it in items
            ],
            "cutout_pieces": items
        }
