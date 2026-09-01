"""
Automated Unit Tests for Tracing, Scissor Skills, Shadow Matching, I-SPY, and Grid Drawing Generators
"""

import os
from pathlib import Path
import pytest
from app.generators.tracing_generator import TracingGenerator
from app.generators.scissor_skills_generator import ScissorSkillsGenerator
from app.generators.shadow_matching_generator import ShadowMatchingGenerator
from app.generators.ispy_counting_generator import ISpyCountingGenerator
from app.generators.grid_drawing_generator import GridDrawingGenerator
from app.core.pdf_exporter import KDPPdfExporter


def test_tracing_generator():
    res = TracingGenerator.generate_letter_tracing_page(letter_or_number="B", repeat_count=5, include_word="BALL")
    assert res["type"] == "tracing"
    assert res["target_char"] == "B"
    assert res["target_lower"] == "b"
    assert res["sample_word"] == "BALL"
    assert len(res["lines"]) >= 5


def test_scissor_skills_generator():
    res = ScissorSkillsGenerator.generate_cutting_practice_page(pattern_type="zigzag", line_count=5)
    assert res["type"] == "scissor_cutting"
    assert res["pattern_type"] == "zigzag"
    assert len(res["lines"]) == 5
    for line in res["lines"]:
        assert line["scissor_icon"] == "✂"


def test_shadow_matching_generator():
    res = ShadowMatchingGenerator.generate_shadow_matching_page(theme="jungle_animals", pair_count=4)
    assert res["type"] == "shadow_matching"
    assert len(res["left_items"]) == 4
    assert len(res["right_shadows"]) == 4
    assert len(res["solutions"]) == 4


def test_ispy_counting_generator():
    res = ISpyCountingGenerator.generate_ispy_page(theme="jungle", title="I Spy Animals")
    assert res["type"] == "ispy_counting"
    assert len(res["checklist"]) >= 3
    assert len(res["scattered_objects"]) >= 10


def test_grid_drawing_generator():
    res = GridDrawingGenerator.generate_grid_drawing_page(grid_size=4, animal_name="Lion")
    assert res["type"] == "grid_drawing"
    assert res["grid_dimension"] == 4
    assert len(res["columns"]) == 4
    assert len(res["rows"]) == 4


def test_pdf_export_with_new_activity_types(tmp_path):
    output_pdf = str(tmp_path / "test_master_activity_suite.pdf")
    
    mock_doc = {
        "name": "Master Activity Book",
        "settings": {
            "trim_width_pt": 612.0,
            "trim_height_pt": 792.0,
            "has_bleed": True,
            "bleed_pt": 9.0,
            "margins": {"top_pt": 27.0, "bottom_pt": 27.0, "inside_pt": 36.0, "outside_pt": 27.0},
            "target_dpi": 300
        },
        "pages": [
            {
                "page_number": 1,
                "page_type": "content",
                "title": "Tracing Letter A",
                "tracing": TracingGenerator.generate_letter_tracing_page("A", 5, "APPLE"),
                "elements": []
            },
            {
                "page_number": 2,
                "page_type": "content",
                "title": "Cutting Zigzag",
                "scissor_skills": ScissorSkillsGenerator.generate_cutting_practice_page("zigzag", 5),
                "elements": []
            },
            {
                "page_number": 3,
                "page_type": "content",
                "title": "Shadow Match",
                "shadow_matching": ShadowMatchingGenerator.generate_shadow_matching_page("jungle_animals", 4),
                "elements": []
            },
            {
                "page_number": 4,
                "page_type": "content",
                "title": "I Spy Count",
                "ispy": ISpyCountingGenerator.generate_ispy_page("jungle"),
                "elements": []
            },
            {
                "page_number": 5,
                "page_type": "content",
                "title": "Grid Drawing Lion",
                "grid_drawing": GridDrawingGenerator.generate_grid_drawing_page(4, animal_name="Lion"),
                "elements": []
            }
        ]
    }

    result_path = KDPPdfExporter.generate_pdf(mock_doc, Path(output_pdf), single_sided=False)
    assert os.path.exists(str(result_path))
    assert os.path.getsize(str(result_path)) > 1000
