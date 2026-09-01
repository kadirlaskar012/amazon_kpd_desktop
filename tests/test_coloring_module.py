"""
Unit tests for Coloring Book module, templates, and batch page generation.
"""

from app.core.document_model import BookSettings
from app.core.asset_model import AssetModel
from app.modules.coloring_book.generator import clean_filename_to_title, generate_coloring_pages
from app.modules.coloring_book.templates import get_coloring_book_templates


def test_clean_filename_to_title():
    assert clean_filename_to_title("01_cute_lion.png") == "Cute Lion"
    assert clean_filename_to_title("002 - baby_elephant_coloring.jpg") == "Baby Elephant"
    assert clean_filename_to_title("funny-monkey_lineart.webp") == "Funny Monkey"
    assert clean_filename_to_title("happy_dolphin_05.png") == "Happy Dolphin"


def test_coloring_page_generation():
    templates = get_coloring_book_templates()
    assert len(templates) >= 2
    template = templates[0]

    assets = [
        AssetModel(asset_id="a1", filename="01_happy_lion.png", width_px=2400, height_px=3000),
        AssetModel(asset_id="a2", filename="02_giant_giraffe.png", width_px=2400, height_px=3000),
    ]

    settings = BookSettings()
    pages = generate_coloring_pages(assets, template, settings, auto_title=True)

    assert len(pages) == 2
    assert pages[0].title == "Happy Lion"
    assert pages[1].title == "Giant Giraffe"
    assert pages[0].page_number == 1
    assert pages[1].page_number == 2

    # Check layers
    all_elems = pages[0].get_all_elements()
    assert any(e.type.value == "image" and e.asset_id == "a1" for e in all_elems)
    assert any(e.type.value == "text" and e.text == "Happy Lion" for e in all_elems)
