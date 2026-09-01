"""
Grid Drawing & How to Draw Step-by-Step Generator
Generates square grid-copy worksheets with numbered columns (A, B, C, D)
and rows (1, 2, 3, 4) for developing proportion awareness and drawing skills.
"""

from typing import Dict, List, Any, Optional


class GridDrawingGenerator:
    """Parametric Grid Drawing & Copy-the-Grid Activity Generator."""

    @staticmethod
    def generate_grid_drawing_page(
        grid_size: int = 4,
        title: str = "Learn to Draw: Grid Copy",
        reference_image_src: Optional[str] = None,
        animal_name: str = "Lion"
    ) -> Dict[str, Any]:
        """Generate a complete 2-grid (reference + empty copy) worksheet."""
        size = 4 if grid_size not in (3, 4, 5, 6) else grid_size
        
        cols = [chr(65 + i) for i in range(size)]  # ['A', 'B', 'C', 'D']
        rows = [str(i + 1) for i in range(size)]   # ['1', '2', '3', '4']

        return {
            "type": "grid_drawing",
            "title": title or f"How to Draw a {animal_name}: Grid Copy",
            "instructions": "Copy the drawing square-by-square into the empty grid on the right!",
            "grid_dimension": size,
            "columns": cols,
            "rows": rows,
            "animal_name": animal_name,
            "reference_image_src": reference_image_src,
            "grid_config": {
                "cell_line_color": "#cbd5e1",
                "outer_border_color": "#0f172a",
                "label_color": "#475569"
            }
        }
