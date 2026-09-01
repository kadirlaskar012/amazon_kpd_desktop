"""
I-SPY & How Many? Counting Activity Generator
Generates engaging search-and-find visual puzzle pages with scattered items
and target counting checklist boxes for kindergarten and early math learners.
"""

import random
from typing import Dict, List, Any, Optional


class ISpyCountingGenerator:
    """Parametric I-SPY / How Many? Counting Puzzle Generator."""

    PRESET_THEMES = {
        "jungle": [
            {"id": "lion", "name": "Lion", "icon": "🦁"},
            {"id": "monkey", "name": "Monkey", "icon": "🐒"},
            {"id": "elephant", "name": "Elephant", "icon": "🐘"},
            {"id": "giraffe", "name": "Giraffe", "icon": "🦒"}
        ],
        "space": [
            {"id": "rocket", "name": "Rocket", "icon": "🚀"},
            {"id": "star", "name": "Star", "icon": "⭐"},
            {"id": "planet", "name": "Planet", "icon": "🪐"},
            {"id": "astronaut", "name": "Astronaut", "icon": "👨‍🚀"}
        ],
        "sweet_treats": [
            {"id": "cupcake", "name": "Cupcake", "icon": "🧁"},
            {"id": "icecream", "name": "Ice Cream", "icon": "🍦"},
            {"id": "donut", "name": "Donut", "icon": "🍩"},
            {"id": "cookie", "name": "Cookie", "icon": "🍪"}
        ]
    }

    @staticmethod
    def generate_ispy_page(
        theme: str = "jungle",
        title: str = "I Spy With My Little Eye!",
        target_counts: Optional[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        """Generate a complete scattered I-SPY activity puzzle with count key."""
        items_meta = ISpyCountingGenerator.PRESET_THEMES.get(theme, ISpyCountingGenerator.PRESET_THEMES["jungle"])
        
        # Determine randomized counts (between 3 and 8 per item)
        counts = target_counts or {}
        if not counts:
            for item in items_meta:
                counts[item["id"]] = random.randint(3, 7)

        # Place scattered objects inside frame (bounding box 40x80 to 460x420)
        scattered_objects = []
        grid_positions = []
        
        # Create non-overlapping grid cells (5 cols x 5 rows)
        for r in range(5):
            for c in range(5):
                grid_positions.append((50 + (c * 80) + random.randint(-10, 10), 100 + (r * 65) + random.randint(-8, 8)))
        
        random.shuffle(grid_positions)

        pos_idx = 0
        checklist = []
        for item in items_meta:
            count = counts.get(item["id"], 4)
            checklist.append({
                "id": item["id"],
                "name": item["name"],
                "icon": item["icon"],
                "count": count
            })

            for _ in range(count):
                if pos_idx < len(grid_positions):
                    px, py = grid_positions[pos_idx]
                    pos_idx += 1
                else:
                    px = random.randint(50, 430)
                    py = random.randint(100, 420)

                scattered_objects.append({
                    "id": item["id"],
                    "name": item["name"],
                    "icon": item["icon"],
                    "x": px,
                    "y": py,
                    "rotation_deg": random.choice([-15, -10, 0, 10, 15, 20]),
                    "scale": round(random.uniform(0.9, 1.15), 2)
                })

        return {
            "type": "ispy_counting",
            "title": title or "I Spy & Count Animals!",
            "instructions": "Find all the hidden pictures, count how many there are, and write your answers in the boxes below!",
            "total_objects": len(scattered_objects),
            "scattered_objects": scattered_objects,
            "checklist": checklist
        }
