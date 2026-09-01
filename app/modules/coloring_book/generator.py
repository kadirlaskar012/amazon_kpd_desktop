"""
Automatic page generation logic for Coloring Books.
Transforms imported assets and chosen layout templates into PageModels.
"""

import os
from pathlib import Path
import re
from typing import List

from app.core.document_model import BookSettings
from app.core.template_model import TemplateModel, LayoutSlot, SlotType
from app.core.page_model import PageModel, LayerModel, ElementModel, ElementType
from app.core.asset_model import AssetModel


def clean_filename_to_title(filename: str) -> str:
    """
    Clean filename to clean human-readable title.
    Examples:
    '01_cute_lion.png' -> 'Cute Lion'
    'big-elephant-coloring.jpg' -> 'Big Elephant'
    'happy_puppy_02.webp' -> 'Happy Puppy'
    """
    stem = Path(filename).stem
    # Remove leading numbering like '01_', '001 - ', '1.'
    stem = re.sub(r"^\d+[\s_\.\-]+", "", stem)
    # Remove trailing numbering or suffixes like '_01', '-coloring', '_bw'
    stem = re.sub(r"[\s_\-]+(coloring|bw|page|lineart|line_art)[\s_\-]*$", "", stem, flags=re.IGNORECASE)
    stem = re.sub(r"[\s_\-]+\d+$", "", stem)
    # Replace underscores, hyphens, multiple spaces with single space
    cleaned = re.sub(r"[_\-]+", " ", stem).strip()
    return cleaned.title() if cleaned else stem.title()


def generate_coloring_pages(
    assets: List[AssetModel],
    template: TemplateModel,
    settings: BookSettings,
    auto_title: bool = True,
) -> List[PageModel]:
    """
    Constructs PageModels from assets according to template slots and physical margins.
    """
    pages: List[PageModel] = []

    # Safe Area Bounds in Points
    # For interior pages, odd pages have inside gutter on left, even pages on right
    page_w = settings.trim_width_pt
    page_h = settings.trim_height_pt

    top_m = settings.margins.top_pt
    bottom_m = settings.margins.bottom_pt
    inside_m = settings.margins.inside_pt
    outside_m = settings.margins.outside_pt

    for idx, asset in enumerate(assets):
        page_num = idx + 1
        is_odd = (page_num % 2 != 0)

        left_m = inside_m if is_odd else outside_m
        right_m = outside_m if is_odd else inside_m

        safe_x = left_m
        safe_y = top_m
        safe_w = max(10.0, page_w - (left_m + right_m))
        safe_h = max(10.0, page_h - (top_m + bottom_m))

        title_text = clean_filename_to_title(asset.filename) if auto_title else f"Page {page_num}"

        # Initialize Layers: Background, Main/Illustration, Title, Border
        layer_bg = LayerModel(layer_id=f"layer_bg_{page_num}", name="Background", visible=True, locked=True)
        layer_ref = LayerModel(layer_id=f"layer_ref_{page_num}", name="Reference Image", visible=True, locked=False)
        layer_main = LayerModel(layer_id=f"layer_main_{page_num}", name="Coloring Area", visible=True, locked=False)
        layer_title = LayerModel(layer_id=f"layer_title_{page_num}", name="Title", visible=True, locked=False)
        layer_border = LayerModel(layer_id=f"layer_border_{page_num}", name="Border", visible=True, locked=False)

        for slot in template.slots:
            # Physical slot geometry
            sx = safe_x + (slot.x_percent * safe_w)
            sy = safe_y + (slot.y_percent * safe_h)
            sw = slot.width_percent * safe_w
            sh = slot.height_percent * safe_h

            if slot.slot_type == SlotType.REFERENCE_IMAGE:
                # Add reference image element
                elem = ElementModel(
                    element_id=f"elem_ref_{page_num}",
                    type=ElementType.IMAGE,
                    x_pt=sx,
                    y_pt=sy,
                    width_pt=sw,
                    height_pt=sh,
                    asset_id=asset.asset_id,
                    maintain_aspect_ratio=slot.maintain_aspect_ratio,
                )
                layer_ref.elements.append(elem)

            elif slot.slot_type == SlotType.MAIN_IMAGE:
                # Add main coloring image element
                elem = ElementModel(
                    element_id=f"elem_main_{page_num}",
                    type=ElementType.IMAGE,
                    x_pt=sx,
                    y_pt=sy,
                    width_pt=sw,
                    height_pt=sh,
                    asset_id=asset.asset_id,
                    maintain_aspect_ratio=slot.maintain_aspect_ratio,
                )
                layer_main.elements.append(elem)

            elif slot.slot_type == SlotType.TITLE:
                elem = ElementModel(
                    element_id=f"elem_title_{page_num}",
                    type=ElementType.TEXT,
                    x_pt=sx,
                    y_pt=sy,
                    width_pt=sw,
                    height_pt=sh,
                    text=title_text,
                    font_family=slot.font_family or "Segoe UI",
                    font_size_pt=slot.font_size_pt or 26.0,
                    bold=True,
                    alignment=slot.alignment or "center",
                    color="#000000",
                )
                layer_title.elements.append(elem)

        # Handle Template Border
        if template.has_border:
            border_inset = template.border_inset_pt
            elem_border = ElementModel(
                element_id=f"elem_border_{page_num}",
                type=ElementType.BORDER,
                x_pt=safe_x - border_inset,
                y_pt=safe_y - border_inset,
                width_pt=safe_w + (border_inset * 2.0),
                height_pt=safe_h + (border_inset * 2.0),
                stroke_color="#000000",
                stroke_width_pt=1.5,
                fill_color=None,
            )
            layer_border.elements.append(elem_border)

        # Assemble layers into PageModel
        page = PageModel(
            page_id=f"page_{page_num:03d}",
            page_number=page_num,
            title=title_text,
            template_id=template.template_id,
            layers=[layer_bg, layer_ref, layer_main, layer_title, layer_border],
        )
        pages.append(page)

        # Mark asset assigned
        if page_num - 1 not in asset.assigned_page_indices:
            asset.assigned_page_indices.append(page_num - 1)

    return pages
