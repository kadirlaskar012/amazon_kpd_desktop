"""
Word Search Puzzle & Solution Generator Engine.
Places custom word lists in 8 directions, fills empty cells with random letters,
and tracks exact start/end coordinates for the solution key.
"""

import random
import string
from typing import List, Dict, Any, Tuple, Optional


class WordSearchGenerator:
    # 8 Search directions (dx, dy)
    DIRECTIONS = [
        (1, 0),   # Horizontal Right
        (-1, 0),  # Horizontal Left
        (0, 1),   # Vertical Down
        (0, -1),  # Vertical Up
        (1, 1),   # Diagonal Down-Right
        (-1, 1),  # Diagonal Down-Left
        (1, -1),  # Diagonal Up-Right
        (-1, -1), # Diagonal Up-Left
    ]

    @classmethod
    def generate_puzzle(
        cls,
        words: List[str],
        grid_size: int = 12,
        puzzle_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a Word Search grid containing all provided words.
        """
        clean_words = [w.strip().upper() for w in words if w.strip()]
        # Sort words longest to shortest for better placement success
        clean_words.sort(key=len, reverse=True)

        grid = [["" for _ in range(grid_size)] for _ in range(grid_size)]
        placed_words = []

        for word in clean_words:
            if len(word) > grid_size:
                continue

            placed = False
            attempts = 0
            while not placed and attempts < 100:
                attempts += 1
                dx, dy = random.choice(cls.DIRECTIONS)
                
                # Determine valid start ranges
                min_x = 0 if dx >= 0 else len(word) - 1
                max_x = grid_size - len(word) if dx > 0 else grid_size - 1
                min_y = 0 if dy >= 0 else len(word) - 1
                max_y = grid_size - len(word) if dy > 0 else grid_size - 1

                if max_x < min_x or max_y < min_y:
                    continue

                start_x = random.randint(min_x, max_x)
                start_y = random.randint(min_y, max_y)

                # Check if word fits without collisions
                can_place = True
                for i, ch in enumerate(word):
                    cx = start_x + (i * dx)
                    cy = start_y + (i * dy)
                    if grid[cy][cx] != "" and grid[cy][cx] != ch:
                        can_place = False
                        break

                if can_place:
                    for i, ch in enumerate(word):
                        cx = start_x + (i * dx)
                        cy = start_y + (i * dy)
                        grid[cy][cx] = ch
                    
                    end_x = start_x + ((len(word) - 1) * dx)
                    end_y = start_y + ((len(word) - 1) * dy)
                    placed_words.append({
                        "word": word,
                        "start": (start_x, start_y),
                        "end": (end_x, end_y)
                    })
                    placed = True

        # Fill remaining empty cells with random letters
        for r in range(grid_size):
            for c in range(grid_size):
                if grid[r][c] == "":
                    grid[r][c] = random.choice(string.ascii_uppercase)

        p_id = puzzle_id or f"ws_{random.randint(1000, 9999)}"

        return {
            "id": p_id,
            "grid_size": grid_size,
            "grid": grid,
            "words": [pw["word"] for pw in placed_words],
            "placed_details": placed_words
        }

    THEMES = [
        ("ANIMALS", ["LION", "TIGER", "BEAR", "ZEBRA", "GIRAFFE", "ELEPHANT", "MONKEY", "PANDA"]),
        ("FRUITS", ["APPLE", "BANANA", "ORANGE", "MANGO", "GRAPES", "CHERRY", "PEACH", "BERRY"]),
        ("SPACE", ["SUN", "MOON", "STAR", "PLANET", "COMET", "GALAXY", "ROCKET", "ORBIT"]),
        ("OCEAN", ["SHARK", "WHALE", "DOLPHIN", "OCTOPUS", "CORAL", "TURTLE", "JELLYFISH"]),
        ("SPORTS", ["SOCCER", "TENNIS", "HOCKEY", "CRICKET", "RUNNING", "SWIMMING", "BOXING"]),
        ("WEATHER", ["RAIN", "STORM", "CLOUDS", "SUNNY", "WINDY", "SNOW", "THUNDER", "FOG"]),
        ("COLORS", ["RED", "BLUE", "GREEN", "YELLOW", "PURPLE", "ORANGE", "VIOLET", "PINK"]),
        ("NATURE", ["FOREST", "RIVER", "VALLEY", "DESERT", "ISLAND", "CANYON", "MOUNTAIN"]),
        ("BIRDS", ["EAGLE", "PARROT", "FALCON", "ROBIN", "OWL", "SWAN", "HAWK", "PIGEON"]),
        ("VEHICLES", ["TRUCK", "AIRPLANE", "TRAIN", "BICYCLE", "SUBWAY", "BOAT", "SCOOTER"])
    ]

    @classmethod
    def generate_bulk(
        cls,
        count: int = 10,
        grid_size: int = 12
    ) -> List[Dict[str, Any]]:
        """Generates a batch of unique word search puzzles with rotating themes."""
        puzzles = []
        for i in range(count):
            theme_name, words = cls.THEMES[i % len(cls.THEMES)]
            p_id = f"ws_{i + 1:04d}"
            puzzle = cls.generate_puzzle(words=words, grid_size=grid_size, puzzle_id=p_id)
            puzzle["theme"] = theme_name
            puzzle["title"] = f"Word Search #{i + 1:03d}: {theme_name.title()}"
            puzzles.append(puzzle)
        return puzzles

