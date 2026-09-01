"""
Alphabet & Number Handwriting Tracing Generator
Generates standard 3-line / 4-line primary penmanship handwriting worksheets,
dotted letters (A-Z, a-z, 0-9), stroke guidance arrows, and word tracing exercises.
"""

from typing import Dict, List, Any, Optional


class TracingGenerator:
    """Parametric Primary Handwriting & Letter/Number Tracing Generator."""

    @staticmethod
    def generate_letter_tracing_page(
        letter_or_number: str = "A",
        repeat_count: int = 5,
        include_word: str = "APPLE",
        rows_count: int = 6,
        show_stroke_arrows: bool = True
    ) -> Dict[str, Any]:
        """Generate full parametric letter tracing worksheet data."""
        char = (letter_or_number or "A").strip().upper()[:1]
        lower_char = char.lower()
        word = (include_word or "APPLE").strip().upper()

        lines_data = []
        # Row 1: Big Letter with Stroke Arrows & Word
        lines_data.append({
            "row_index": 1,
            "type": "headline",
            "primary_char": char,
            "lowercase_char": lower_char,
            "sample_word": word,
            "show_arrows": show_stroke_arrows
        })

        # Row 2: Uppercase Tracing Practice
        lines_data.append({
            "row_index": 2,
            "type": "uppercase_trace",
            "char": char,
            "repeat": repeat_count,
            "blank_practice_slots": 1
        })

        # Row 3: Lowercase Tracing Practice
        lines_data.append({
            "row_index": 3,
            "type": "lowercase_trace",
            "char": lower_char,
            "repeat": repeat_count,
            "blank_practice_slots": 1
        })

        # Row 4: Upper + Lower Combo Tracing
        lines_data.append({
            "row_index": 4,
            "type": "combo_trace",
            "combo": f"{char}{lower_char}",
            "repeat": max(3, repeat_count - 1),
            "blank_practice_slots": 1
        })

        # Row 5 & 6: Word Tracing Practice
        lines_data.append({
            "row_index": 5,
            "type": "word_trace",
            "word": word,
            "repeat": 2,
            "blank_practice_slots": 1
        })
        lines_data.append({
            "row_index": 6,
            "type": "free_practice",
            "prompt": f"Practice writing letter '{char}' and word '{word}'"
        })

        return {
            "type": "tracing",
            "target_char": char,
            "target_lower": lower_char,
            "sample_word": word,
            "rows_count": rows_count,
            "lines": lines_data,
            "guidelines_config": {
                "top_line_color": "#0f172a",
                "mid_line_color": "#94a3b8",
                "base_line_color": "#0f172a",
                "mid_line_dashed": True
            }
        }

    @staticmethod
    def generate_number_tracing_page(
        number_digit: int = 1,
        repeat_count: int = 6,
        number_word: str = "ONE"
    ) -> Dict[str, Any]:
        """Generate number tracing worksheet (0-20)."""
        num_str = str(number_digit)
        return {
            "type": "number_tracing",
            "target_number": number_digit,
            "number_word": number_word or "ONE",
            "repeat_count": repeat_count,
            "rows": [
                {"type": "number_header", "digit": num_str, "word": number_word},
                {"type": "number_trace", "digit": num_str, "repeat": repeat_count},
                {"type": "word_trace", "word": number_word, "repeat": 3},
                {"type": "counting_dots", "count": number_digit},
                {"type": "free_practice", "digit": num_str}
            ]
        }
