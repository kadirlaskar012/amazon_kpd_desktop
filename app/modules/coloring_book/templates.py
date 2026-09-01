"""
Standard layout templates for Coloring Books.
Slots define relative positions (0.0 to 1.0) within the safe printable page margins.
"""

from typing import List
from app.core.template_model import TemplateModel, LayoutSlot, SlotType, TemplateCategory


def get_coloring_book_templates() -> List[TemplateModel]:
    return [
        TemplateModel(
            template_id="coloring_standard_with_ref",
            name="Reference Top + Main + Title Bottom",
            category=TemplateCategory.COLORING,
            description="Small color reference thumbnail at top, large black-and-white coloring area, bold animal/object title at bottom.",
            slots=[
                LayoutSlot(
                    slot_id="slot_ref_img",
                    slot_type=SlotType.REFERENCE_IMAGE,
                    name="Reference Preview Image",
                    x_percent=0.35,
                    y_percent=0.02,
                    width_percent=0.30,
                    height_percent=0.18,
                    maintain_aspect_ratio=True,
                    is_required=False,
                ),
                LayoutSlot(
                    slot_id="slot_main_img",
                    slot_type=SlotType.MAIN_IMAGE,
                    name="Main Coloring Illustration",
                    x_percent=0.05,
                    y_percent=0.22,
                    width_percent=0.90,
                    height_percent=0.66,
                    maintain_aspect_ratio=True,
                    is_required=True,
                ),
                LayoutSlot(
                    slot_id="slot_title",
                    slot_type=SlotType.TITLE,
                    name="Animal / Object Title",
                    x_percent=0.05,
                    y_percent=0.90,
                    width_percent=0.90,
                    height_percent=0.08,
                    font_family="Segoe UI",
                    font_size_pt=26.0,
                    alignment="center",
                    is_required=True,
                ),
            ],
            has_border=False,
        ),
        TemplateModel(
            template_id="coloring_full_page_title",
            name="Full Page Coloring + Title",
            category=TemplateCategory.COLORING,
            description="Large central coloring image with object/character title at the bottom.",
            slots=[
                LayoutSlot(
                    slot_id="slot_main_img",
                    slot_type=SlotType.MAIN_IMAGE,
                    name="Main Coloring Illustration",
                    x_percent=0.02,
                    y_percent=0.02,
                    width_percent=0.96,
                    height_percent=0.86,
                    maintain_aspect_ratio=True,
                    is_required=True,
                ),
                LayoutSlot(
                    slot_id="slot_title",
                    slot_type=SlotType.TITLE,
                    name="Animal / Object Title",
                    x_percent=0.05,
                    y_percent=0.90,
                    width_percent=0.90,
                    height_percent=0.08,
                    font_family="Segoe UI",
                    font_size_pt=28.0,
                    alignment="center",
                    is_required=True,
                ),
            ],
            has_border=False,
        ),
        TemplateModel(
            template_id="coloring_framed_classic",
            name="Framed Classic with Border",
            category=TemplateCategory.COLORING,
            description="Clean framed coloring layout with decorative border.",
            slots=[
                LayoutSlot(
                    slot_id="slot_main_img",
                    slot_type=SlotType.MAIN_IMAGE,
                    name="Main Coloring Illustration",
                    x_percent=0.05,
                    y_percent=0.08,
                    width_percent=0.90,
                    height_percent=0.80,
                    maintain_aspect_ratio=True,
                    is_required=True,
                ),
                LayoutSlot(
                    slot_id="slot_title",
                    slot_type=SlotType.TITLE,
                    name="Page Title",
                    x_percent=0.05,
                    y_percent=0.90,
                    width_percent=0.90,
                    height_percent=0.07,
                    font_family="Segoe UI",
                    font_size_pt=24.0,
                    alignment="center",
                    is_required=False,
                ),
            ],
            has_border=True,
            border_style="simple",
            border_inset_pt=6.0,
        ),
    ]
