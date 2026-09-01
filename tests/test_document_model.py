"""
Unit tests for document and page models serialization round-trip.
"""

from app.core.document_model import (
    BookSettings,
    MarginSettings,
    PageNumberingSettings,
    CoverModel,
    ProjectDocument,
    BookType,
)
from app.core.page_model import PageModel, LayerModel, ElementModel, ElementType
from app.core.units import in_to_pt


def test_book_settings_roundtrip():
    settings = BookSettings(
        trim_preset_id="8.5x11",
        trim_width_pt=in_to_pt(8.5),
        trim_height_pt=in_to_pt(11.0),
        has_bleed=True,
        margins=MarginSettings(
            top_pt=in_to_pt(0.375),
            bottom_pt=in_to_pt(0.375),
            inside_pt=in_to_pt(0.500),
            outside_pt=in_to_pt(0.375),
        ),
        target_dpi=300,
        page_numbering=PageNumberingSettings(enabled=True, start_number=1),
    )

    data = settings.to_dict()
    reloaded = BookSettings.from_dict(data)

    assert reloaded.trim_width_pt == in_to_pt(8.5)
    assert reloaded.trim_height_pt == in_to_pt(11.0)
    assert reloaded.has_bleed is True
    assert reloaded.margins.inside_pt == in_to_pt(0.500)
    assert reloaded.page_numbering.enabled is True


def test_project_document_roundtrip():
    doc = ProjectDocument(
        name="Test Coloring Book",
        author="KDP Studio Author",
        publisher="Studio Publishing",
        module_type=BookType.COLORING_BOOK.value,
        settings=BookSettings(),
    )

    # Add a page with an element
    page = PageModel(
        page_id="p1",
        page_number=1,
        title="Cute Puppy",
        layers=[
            LayerModel(
                layer_id="l1",
                name="Main",
                elements=[
                    ElementModel(
                        element_id="e1",
                        type=ElementType.IMAGE,
                        x_pt=50.0,
                        y_pt=50.0,
                        width_pt=200.0,
                        height_pt=200.0,
                        asset_id="asset_123",
                    ),
                    ElementModel(
                        element_id="e2",
                        type=ElementType.TEXT,
                        x_pt=50.0,
                        y_pt=260.0,
                        width_pt=200.0,
                        height_pt=30.0,
                        text="Cute Puppy",
                    ),
                ],
            )
        ],
    )
    doc.pages.append(page.to_dict())

    data = doc.to_dict()
    reloaded = ProjectDocument.from_dict(data)

    assert reloaded.name == "Test Coloring Book"
    assert reloaded.author == "KDP Studio Author"
    assert len(reloaded.pages) == 1
    page_data = reloaded.pages[0]
    p_obj = PageModel.from_dict(page_data)
    assert p_obj.title == "Cute Puppy"
    assert len(p_obj.layers) == 1
    assert len(p_obj.layers[0].elements) == 2
    assert p_obj.layers[0].elements[1].text == "Cute Puppy"
