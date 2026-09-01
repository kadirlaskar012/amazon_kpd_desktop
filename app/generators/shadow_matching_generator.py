"""
Shadow Matching & Visual Perception Activity Generator
Generates pairs-matching activity worksheets with illustrations on the left
and shuffled solid black silhouette shadows on the right with connection nodes.
"""

import random
from typing import Dict, List, Any, Optional


class ShadowMatchingGenerator:
    """Parametric Shadow Matching & Visual Perception Activity Generator."""

    PRESET_SETS = {
        "jungle_animals": [
            {"id": "sm_lion", "name": "Lion", "icon": "🦁"},
            {"id": "sm_elephant", "name": "Elephant", "icon": "🐘"},
            {"id": "sm_monkey", "name": "Monkey", "icon": "🐒"},
            {"id": "sm_zebra", "name": "Zebra", "icon": "🦓"},
            {"id": "sm_giraffe", "name": "Giraffe", "icon": "🦒"}
        ],
        "vehicles": [
            {"id": "sm_car", "name": "Car", "icon": "🚗"},
            {"id": "sm_airplane", "name": "Airplane", "icon": "✈️"},
            {"id": "sm_rocket", "name": "Rocket", "icon": "🚀"},
            {"id": "sm_ship", "name": "Ship", "icon": "🚢"},
            {"id": "sm_train", "name": "Train", "icon": "🚂"}
        ],
        "farm_animals": [
            {"id": "sm_cow", "name": "Cow", "icon": "🐄"},
            {"id": "sm_horse", "name": "Horse", "icon": "🐎"},
            {"id": "sm_pig", "name": "Pig", "icon": "🐖"},
            {"id": "sm_sheep", "name": "Sheep", "icon": "🐑"},
            {"id": "sm_rooster", "name": "Rooster", "icon": "🐓"}
        ]
    }

    @staticmethod
    def generate_shadow_matching_page(
        theme: str = "jungle_animals",
        pair_count: int = 4,
        title: str = "Shadow Matching Activity"
    ) -> Dict[str, Any]:
        """Generate a complete shadow matching page data."""
        base_items = ShadowMatchingGenerator.PRESET_SETS.get(theme, ShadowMatchingGenerator.PRESET_SETS["jungle_animals"])
        selected_items = base_items[:pair_count]

        # Left items (order 0, 1, 2, 3...)
        left_items = []
        for idx, item in enumerate(selected_items):
            left_items.append({
                "id": item["id"],
                "name": item["name"],
                "icon": item["icon"],
                "slot_index": idx,
                "node_y": 140 + (idx * 110)
            })

        # Right items (shuffled shadows)
        shuffled_shadows = list(selected_items)
        random.shuffle(shuffled_shadows)
        # Ensure at least some items are not in the exact same row index
        if len(shuffled_shadows) > 1 and shuffled_shadows[0]["id"] == left_items[0]["id"]:
            shuffled_shadows[0], shuffled_shadows[1] = shuffled_shadows[1], shuffled_shadows[0]

        right_shadows = []
        for idx, item in enumerate(shuffled_shadows):
            right_shadows.append({
                "id": item["id"],
                "name": item["name"],
                "icon": item["icon"],
                "is_shadow": True,
                "slot_index": idx,
                "node_y": 140 + (idx * 110)
            })

        # Generate solution pairings
        solutions = {}
        for l in left_items:
            for r in right_shadows:
                if l["id"] == r["id"]:
                    solutions[l["id"]] = {
                        "left_slot": l["slot_index"],
                        "right_slot": r["slot_index"]
                    }

        return {
            "type": "shadow_matching",
            "title": title or "Find and Match the Shadows!",
            "instructions": "Draw a line connecting each picture on the left to its matching shadow on the right.",
            "pair_count": len(selected_items),
            "left_items": left_items,
            "right_shadows": right_shadows,
            "solutions": solutions
        }
