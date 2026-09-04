"""
Amazon KDP PDF Exporter Engine.
Generates 100% compliant 300 DPI Print-Ready PDF/X files for Amazon KDP Paperback & Hardcover.
Includes ultra-crisp, elegant typography for Front Matter (Disclaimer, Contents with Auto Item List, Belongs To, Color Test Palette)
and Single-Sided Coloring Pages with alternating Blank Back Pages for bleed protection.
"""

import io
import base64
import textwrap
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib import colors


class KDPPdfExporter:
    @staticmethod
    def generate_pdf(
        project_data: dict, 
        output_path: Path, 
        include_front_matter: bool = True,
        single_sided: bool = True,
        blank_page_note: bool = False,
        include_page_numbers: bool = False
    ) -> Path:
        """
        Generates a complete multi-page Amazon KDP Interior PDF.
        Compiles Front Matter + Content Drawings + Blank Verso Pages.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        settings = project_data.get("settings", {})
        trim_w = float(settings.get("trim_width_pt", 612.0))   # 8.5 in * 72
        trim_h = float(settings.get("trim_height_pt", 792.0))  # 11.0 in * 72
        has_bleed = bool(settings.get("has_bleed", True))
        bleed_pt = float(settings.get("bleed_pt", 9.0)) if has_bleed else 0.0

        b_type = project_data.get("book_type", "coloring_book")
        if "single_sided" in settings:
            single_sided = bool(settings["single_sided"])
        elif b_type in ("sudoku", "tic_tac_toe", "maze", "word_search", "puzzle_book", "activity_book"):
            single_sided = False

        if "include_page_numbers" in project_data:
            include_page_numbers = bool(project_data["include_page_numbers"])

        # Physical page dimensions including bleed
        page_w = trim_w + (bleed_pt * 2)
        page_h = trim_h + (bleed_pt * 2)

        c = canvas.Canvas(str(output_path), pagesize=(page_w, page_h))
        
        # Web canvas reference coordinate space: 510 x 660 pt
        canvas_ref_w = 510.0
        canvas_ref_h = 660.0

        scale_x = trim_w / canvas_ref_w
        scale_y = trim_h / canvas_ref_h

        # Extract only the actual working drawing/content pages (ignore front matter or blank keys)
        raw_pages = project_data.get("pages", [])
        content_pages = []
        for p in raw_pages:
            p_type = p.get("page_type", "content")
            p_title = (p.get("title") or "").lower()
            if p_type in ("blank_verso", "front_matter_disclaimer", "front_matter_contents", "front_matter_belongs_to", "front_matter_color_test"):
                continue
            if "disclaimer" in p_title or "table of contents" in p_title or "belongs to" in p_title or "color test" in p_title:
                continue
            content_pages.append(p)
        
        if not content_pages and raw_pages:
            content_pages = raw_pages

        book_title = (project_data.get("name") or "COLORING BOOK").upper()
        author_name = project_data.get("author") or "Creative Kids Studio"

        def render_blank_page():
            """Renders a pure blank KDP back page to prevent color bleed-through."""
            c.setFillColor(colors.white)
            c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
            if blank_page_note:
                c.setFont("Helvetica-Oblique", 8.5)
                c.setFillColor(colors.HexColor("#94a3b8"))
                c.drawCentredString(page_w / 2.0, 35 + bleed_pt, "[ Blank page to protect against color bleed-through ]")
            c.showPage()

        # =========================================================================
        # 1. FRONT MATTER PAGES (Customizable & Selectable)
        # =========================================================================
        fm_opts = project_data.get("front_matter_options", {})
        inc_disclaimer = fm_opts.get("include_disclaimer", True) if include_front_matter else False
        inc_contents = fm_opts.get("include_contents", True) if (include_front_matter and b_type == "coloring_book") else False
        inc_belongs = fm_opts.get("include_belongs", True) if (include_front_matter and b_type == "coloring_book") else False
        inc_color_test = fm_opts.get("include_color_test", True) if (include_front_matter and b_type == "coloring_book") else False
        inc_custom_page = fm_opts.get("include_custom_page", False) if include_front_matter else False
        custom_page_pos = fm_opts.get("custom_page_pos", "back")

        custom_author = fm_opts.get("author") or author_name
        custom_publisher = fm_opts.get("publisher") or author_name
        custom_book_title = fm_opts.get("book_title") or book_title
        custom_edition = fm_opts.get("edition_text") or "First Edition  •  Amazon KDP Publication"
        custom_copyright = fm_opts.get("copyright_text") or f"Copyright © 2026 by {custom_author}"
        custom_isbn = fm_opts.get("isbn") or "ISBN-13: 978-X-XXXXX-XXX-X"
        custom_extra_note = fm_opts.get("disclaimer_extra_note") or ""

        custom_toc_heading = fm_opts.get("toc_heading") or "TABLE OF CONTENTS"
        custom_toc_subtitle = fm_opts.get("toc_subtitle") or "Complete list of coloring illustrations in this book"
        custom_toc_footer = fm_opts.get("toc_footer") or ""

        custom_belongs_title = fm_opts.get("belongs_title") or "THIS COLORING BOOK"
        custom_belongs_header = fm_opts.get("belongs_header") or "BELONGS TO:"
        custom_subtext = fm_opts.get("subtext") or "Color with joy, love and your wild imagination!"
        custom_belongs_gift = fm_opts.get("belongs_gift_note") or ""

        custom_color_title = fm_opts.get("color_test_title") or "COLOR TEST PALETTE"
        custom_color_subtext = fm_opts.get("color_test_subtext") or "Test your pencils, markers, and crayons here before coloring!"
        custom_color_note = fm_opts.get("color_test_note") or ""

        def render_custom_text_page():
            """Renders a fully custom, elegant text page (e.g. Introduction or Back-matter Thank You page)."""
            c.setFillColor(colors.white)
            c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

            # Elegant decorative double inner border
            c.setStrokeColor(colors.HexColor("#0f172a"))
            c.setLineWidth(1.5)
            c.roundRect(35 + bleed_pt, 35 + bleed_pt, trim_w - 70, trim_h - 70, radius=8, fill=0, stroke=1)
            c.setStrokeColor(colors.HexColor("#cbd5e1"))
            c.setLineWidth(0.75)
            c.roundRect(39 + bleed_pt, 39 + bleed_pt, trim_w - 78, trim_h - 78, radius=6, fill=0, stroke=1)

            c_title = fm_opts.get("custom_page_title") or "A NOTE FROM THE AUTHOR"
            c_subtitle = fm_opts.get("custom_page_subtitle") or "Thank you for supporting our work!"
            c_body = fm_opts.get("custom_page_body") or (
                "Thank you so much for choosing our coloring book!\n\n"
                "We poured our hearts into creating each illustration, designed to spark creativity, "
                "relaxation, and endless joy. Whether you are coloring with colored pencils, markers, "
                "or crayons, remember that in art, there are no mistakes—only unique masterpieces!\n\n"
                "If you enjoyed this book, please consider leaving a review on Amazon. "
                "Your kind feedback helps independent creators like us continue to make beautiful books!"
            )
            c_signoff = fm_opts.get("custom_page_signoff") or f"Happy Coloring!  •  {custom_author}"

            c.setFont("Helvetica-Bold", 20)
            c.setFillColor(colors.HexColor("#0f172a"))
            c.drawCentredString(page_w / 2.0, page_h - 95 - bleed_pt, c_title.upper())

            if c_subtitle:
                c.setFont("Helvetica", 10.5)
                c.setFillColor(colors.HexColor("#475569"))
                c.drawCentredString(page_w / 2.0, page_h - 120 - bleed_pt, c_subtitle)

            c.setStrokeColor(colors.HexColor("#e2e8f0"))
            c.setLineWidth(1.0)
            c.line(page_w / 2.0 - 60, page_h - 140 - bleed_pt, page_w / 2.0 + 60, page_h - 140 - bleed_pt)

            cur_y = page_h - 180 - bleed_pt
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.HexColor("#334155"))

            paras = c_body.split("\n")
            for p in paras:
                p = p.strip()
                if not p:
                    cur_y -= 14
                    continue
                w_lines = textwrap.wrap(p, width=66)
                for line in w_lines:
                    if cur_y < 120 + bleed_pt:
                        break
                    c.drawCentredString(page_w / 2.0, cur_y, line)
                    cur_y -= 18
                cur_y -= 8

            if c_signoff:
                c.setFont("Helvetica-Bold", 10.5)
                c.setFillColor(colors.HexColor("#0f172a"))
                c.drawCentredString(page_w / 2.0, max(65 + bleed_pt, min(cur_y - 20, 100 + bleed_pt)), c_signoff)

            c.showPage()
            if single_sided:
                render_blank_page()

        # Calculate actual starting page number for content pages
        fm_count = sum([1 for flag in [inc_disclaimer, inc_contents, inc_belongs, inc_color_test, (inc_custom_page and custom_page_pos == "front")] if flag])
        needs_fm_pad = single_sided and (fm_count % 2 != 0)
        if needs_fm_pad:
            fm_count += 1
        start_content_page_num = fm_count + 1

        # --- PAGE 1: DISCLAIMER & COPYRIGHT ---
        if inc_disclaimer:
            c.setFillColor(colors.white)
            c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

            # Elegant decorative double inner border
            c.setStrokeColor(colors.HexColor("#0f172a"))
            c.setLineWidth(1.5)
            c.roundRect(35 + bleed_pt, 35 + bleed_pt, trim_w - 70, trim_h - 70, radius=8, fill=0, stroke=1)
            c.setStrokeColor(colors.HexColor("#cbd5e1"))
            c.setLineWidth(0.75)
            c.roundRect(39 + bleed_pt, 39 + bleed_pt, trim_w - 78, trim_h - 78, radius=6, fill=0, stroke=1)

            # Book Title
            c.setFont("Helvetica-Bold", 20)
            c.setFillColor(colors.HexColor("#0f172a"))
            c.drawCentredString(page_w / 2.0, page_h - 100 - bleed_pt, custom_book_title)

            # Subtitle / Edition
            c.setFont("Helvetica", 10.5)
            c.setFillColor(colors.HexColor("#475569"))
            c.drawCentredString(page_w / 2.0, page_h - 125 - bleed_pt, custom_edition)

            # Small decorative divider line
            c.setStrokeColor(colors.HexColor("#e2e8f0"))
            c.setLineWidth(1.0)
            c.line(page_w / 2.0 - 50, page_h - 150 - bleed_pt, page_w / 2.0 + 50, page_h - 150 - bleed_pt)

            # Copyright
            c.setFont("Helvetica-Bold", 11)
            c.setFillColor(colors.HexColor("#1e293b"))
            c.drawCentredString(page_w / 2.0, page_h - 200 - bleed_pt, custom_copyright)

            c.setFont("Helvetica", 10)
            c.setFillColor(colors.HexColor("#334155"))
            c.drawCentredString(page_w / 2.0, page_h - 220 - bleed_pt, "All Rights Reserved.")

            # Legal Disclaimer lines (multi-line word-wrapped or custom)
            raw_disclaimer = fm_opts.get("disclaimer_text")
            if raw_disclaimer:
                disclaimer_paras = raw_disclaimer.strip().split("\n")
                disclaimer_lines = []
                for p in disclaimer_paras:
                    p = p.strip()
                    if p:
                        disclaimer_lines.extend(textwrap.wrap(p, width=72))
                    else:
                        disclaimer_lines.append("")
            else:
                disclaimer_lines = [
                    "No part of this publication may be reproduced, distributed, or transmitted in any form",
                    "or by any means, including photocopying, recording, or other electronic or mechanical methods,",
                    "without the prior written permission of the publisher, except in the case of brief quotations",
                    "embodied in critical reviews and certain other noncommercial uses permitted by copyright law."
                ]

            c.setFont("Helvetica", 8.5)
            c.setFillColor(colors.HexColor("#64748b"))
            disc_y = page_h - 265 - bleed_pt
            for line in disclaimer_lines[:10]:
                if line:
                    c.drawCentredString(page_w / 2.0, disc_y, line)
                disc_y -= 15

            # Publisher Info
            c.setFont("Helvetica-Bold", 9.5)
            c.setFillColor(colors.HexColor("#334155"))
            c.drawCentredString(page_w / 2.0, page_h - 430 - bleed_pt, f"Published by: {custom_publisher}")
            
            c.setFont("Helvetica", 9)
            c.setFillColor(colors.HexColor("#475569"))
            c.drawCentredString(page_w / 2.0, page_h - 450 - bleed_pt, custom_isbn)

            # Extra note or dedication if provided
            if custom_extra_note:
                c.setFont("Helvetica-Oblique", 9)
                c.setFillColor(colors.HexColor("#64748b"))
                c.drawCentredString(page_w / 2.0, page_h - 490 - bleed_pt, custom_extra_note)

            c.setFont("Helvetica-Oblique", 8.5)
            c.setFillColor(colors.HexColor("#94a3b8"))
            c.drawCentredString(page_w / 2.0, page_h - 540 - bleed_pt, "Printed in the United States of America  •  Amazon KDP Distribution")
            c.showPage()

        # --- PAGE 2: TABLE OF CONTENTS (AUTO ITEM LIST) ---
        if inc_contents:
            c.setFillColor(colors.white)
            c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

            # Outer border
            c.setStrokeColor(colors.HexColor("#0f172a"))
            c.setLineWidth(1.5)
            c.roundRect(35 + bleed_pt, 35 + bleed_pt, trim_w - 70, trim_h - 70, radius=8, fill=0, stroke=1)
            c.setStrokeColor(colors.HexColor("#cbd5e1"))
            c.setLineWidth(0.75)
            c.roundRect(39 + bleed_pt, 39 + bleed_pt, trim_w - 78, trim_h - 78, radius=6, fill=0, stroke=1)

            # Header
            c.setFont("Helvetica-Bold", 18)
            c.setFillColor(colors.HexColor("#0f172a"))
            c.drawCentredString(page_w / 2.0, page_h - 90 - bleed_pt, custom_toc_heading)

            c.setFont("Helvetica", 10)
            c.setFillColor(colors.HexColor("#64748b"))
            c.drawCentredString(page_w / 2.0, page_h - 115 - bleed_pt, custom_toc_subtitle)

            c.setStrokeColor(colors.HexColor("#e2e8f0"))
            c.setLineWidth(1.0)
            c.line(page_w / 2.0 - 60, page_h - 135 - bleed_pt, page_w / 2.0 + 60, page_h - 135 - bleed_pt)

            # Item List
            start_y = page_h - 170 - bleed_pt
            max_items_to_print = min(22, len(content_pages))
            
            left_margin = 65 + bleed_pt
            right_margin = page_w - 65 - bleed_pt

            for idx in range(max_items_to_print):
                cp = content_pages[idx]
                item_title = cp.get("title") or f"Illustration {idx + 1}"
                
                # Check for explicit title element
                for el in cp.get("elements", []):
                    if el.get("type") == "title" and el.get("text"):
                        item_title = el.get("text").title()
                        break

                calc_page_num = start_content_page_num + (idx * 2) if single_sided else start_content_page_num + idx
                item_y = start_y - (idx * 22)

                # Draw Left Text
                c.setFont("Helvetica-Bold", 9.5)
                c.setFillColor(colors.HexColor("#1e293b"))
                left_str = f"{idx + 1}.  {item_title}"
                c.drawString(left_margin, item_y, left_str)

                # Draw Right Text
                c.setFont("Helvetica-Bold", 9.5)
                c.setFillColor(colors.HexColor("#475569"))
                right_str = f"Page {calc_page_num}"
                c.drawRightString(right_margin, item_y, right_str)

                # Crisp Dot Leader between left and right
                c.setFont("Helvetica", 8)
                c.setFillColor(colors.HexColor("#94a3b8"))
                
                name_w = c.stringWidth(left_str, "Helvetica-Bold", 9.5)
                page_w_num = c.stringWidth(right_str, "Helvetica-Bold", 9.5)
                
                dot_start = left_margin + name_w + 12
                dot_end = right_margin - page_w_num - 12
                
                if dot_end > dot_start:
                    dot_unit_w = c.stringWidth(" . ", "Helvetica", 8)
                    num_dots = int((dot_end - dot_start) / dot_unit_w)
                    if num_dots > 0:
                        c.drawString(dot_start, item_y, " . " * num_dots)

            if custom_toc_footer:
                c.setFont("Helvetica-Oblique", 9)
                c.setFillColor(colors.HexColor("#64748b"))
                c.drawCentredString(page_w / 2.0, 50 + bleed_pt, custom_toc_footer)

            c.showPage()

        # --- PAGE 3: THIS BOOK BELONGS TO ---
        if inc_belongs:
            c.setFillColor(colors.white)
            c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

            c.setStrokeColor(colors.HexColor("#0f172a"))
            c.setLineWidth(1.5)
            c.roundRect(35 + bleed_pt, 35 + bleed_pt, trim_w - 70, trim_h - 70, radius=8, fill=0, stroke=1)
            c.setStrokeColor(colors.HexColor("#cbd5e1"))
            c.setLineWidth(0.75)
            c.roundRect(39 + bleed_pt, 39 + bleed_pt, trim_w - 78, trim_h - 78, radius=6, fill=0, stroke=1)

            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(colors.HexColor("#334155"))
            c.drawCentredString(page_w / 2.0, page_h - 130 - bleed_pt, custom_belongs_title)

            # Outlined BELONGS TO
            c.setFont("Helvetica-Bold", 32)
            c.setStrokeColor(colors.HexColor("#0f172a"))
            c.setFillColor(colors.white)
            c.setLineWidth(1.6)
            c._code.append("2 Tr\n")
            c.drawCentredString(page_w / 2.0, page_h - 190 - bleed_pt, custom_belongs_header)
            c._code.append("0 Tr\n")

            # Clean writing line
            c.setStrokeColor(colors.HexColor("#94a3b8"))
            c.setLineWidth(1.2)
            line_y = page_h - 300 - bleed_pt
            c.line(80 + bleed_pt, line_y, page_w - 80 - bleed_pt, line_y)

            c.setFont("Helvetica-Oblique", 11)
            c.setFillColor(colors.HexColor("#64748b"))
            c.drawCentredString(page_w / 2.0, page_h - 380 - bleed_pt, custom_subtext)

            # Extra gift dedication line if provided
            if custom_belongs_gift:
                c.setFont("Helvetica-Bold", 10)
                c.setFillColor(colors.HexColor("#475569"))
                c.drawCentredString(page_w / 2.0, page_h - 430 - bleed_pt, custom_belongs_gift)
                c.setStrokeColor(colors.HexColor("#cbd5e1"))
                c.setLineWidth(1.0)
                c.line(120 + bleed_pt, page_h - 455 - bleed_pt, page_w - 120 - bleed_pt, page_h - 455 - bleed_pt)

            c.showPage()

        # --- PAGE 4: COLOR TEST PALETTE ---
        if inc_color_test:
            c.setFillColor(colors.white)
            c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

            c.setStrokeColor(colors.HexColor("#0f172a"))
            c.setLineWidth(1.5)
            c.roundRect(35 + bleed_pt, 35 + bleed_pt, trim_w - 70, trim_h - 70, radius=8, fill=0, stroke=1)
            c.setStrokeColor(colors.HexColor("#cbd5e1"))
            c.setLineWidth(0.75)
            c.roundRect(39 + bleed_pt, 39 + bleed_pt, trim_w - 78, trim_h - 78, radius=6, fill=0, stroke=1)

            c.setFont("Helvetica-Bold", 22)
            c.setFillColor(colors.HexColor("#0f172a"))
            c.drawCentredString(page_w / 2.0, page_h - 85 - bleed_pt, custom_color_title)

            c.setFont("Helvetica", 10)
            c.setFillColor(colors.HexColor("#64748b"))
            c.drawCentredString(page_w / 2.0, page_h - 110 - bleed_pt, custom_color_subtext)

            c.setStrokeColor(colors.HexColor("#e2e8f0"))
            c.setLineWidth(1.0)
            c.line(page_w / 2.0 - 60, page_h - 125 - bleed_pt, page_w / 2.0 + 60, page_h - 125 - bleed_pt)

            # 12 Swatch Boxes Grid (4 rows x 3 cols)
            grid_cols = 3
            grid_rows = 4
            swatch_w = 120
            swatch_h = 85
            spacing_x = 24
            spacing_y = 24
            grid_total_w = (grid_cols * swatch_w) + ((grid_cols - 1) * spacing_x)
            grid_start_x = (page_w - grid_total_w) / 2.0
            grid_start_y = page_h - 160 - bleed_pt - swatch_h

            box_idx = 1
            for r in range(grid_rows):
                for col in range(grid_cols):
                    bx = grid_start_x + (col * (swatch_w + spacing_x))
                    by = grid_start_y - (r * (swatch_h + spacing_y))

                    c.setStrokeColor(colors.HexColor("#94a3b8"))
                    c.setLineWidth(1.0)
                    c.setDash(4, 3)
                    c.roundRect(bx, by, swatch_w, swatch_h, radius=6, fill=0, stroke=1)
                    c.setDash()

                    c.setFont("Helvetica", 8)
                    c.setFillColor(colors.HexColor("#94a3b8"))
                    c.drawString(bx + 8, by + swatch_h - 12, f"Color {box_idx}")
                    box_idx += 1

            if custom_color_note:
                c.setFont("Helvetica-Oblique", 9)
                c.setFillColor(colors.HexColor("#64748b"))
                c.drawCentredString(page_w / 2.0, 48 + bleed_pt, custom_color_note)

            c.showPage()

        # --- OPTIONAL FRONT MATTER CUSTOM PAGE ---
        if inc_custom_page and custom_page_pos == "front":
            render_custom_text_page()

        # If single-sided and front-matter had an odd number of pages, insert a blank verso page
        # so that Drawing 1 is guaranteed to start on an ODD page (RIGHT side) with Blank on LEFT
        if needs_fm_pad:
            render_blank_page()

        # =========================================================================
        # 2. CONTENT DRAWING PAGES (Pages 5+) + BLANK VERSO PAGES
        # =========================================================================
        for page_idx, page in enumerate(content_pages):
            # 1. Fill page with pure white
            c.setFillColor(colors.white)
            c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

            # 2. Draw Elements on this page
            elements = page.get("elements", [])
            for elem in elements:
                elem_type = elem.get("type", "")
                elem_x = float(elem.get("x", 0))
                elem_y = float(elem.get("y", 0))
                elem_w = float(elem.get("w", 50))
                elem_h = float(elem.get("h", 50))

                x = (elem_x * scale_x) + bleed_pt
                w = elem_w * scale_x
                h = elem_h * scale_y
                y = page_h - (elem_y * scale_y) - h - bleed_pt

                if elem_type in ("ref_image", "main_image"):
                    img_src = elem.get("image_src")
                    if img_src and isinstance(img_src, str):
                        try:
                            if "," in img_src:
                                header, encoded = img_src.split(",", 1)
                                img_bytes = base64.b64decode(encoded)
                                img = Image.open(io.BytesIO(img_bytes))
                            elif Path(img_src).exists():
                                img = Image.open(img_src)
                            else:
                                img = None

                            if img:
                                if img.mode in ("RGBA", "LA", "P"):
                                    bg = Image.new("RGB", img.size, (255, 255, 255))
                                    if img.mode == "P":
                                        img = img.convert("RGBA")
                                    bg.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
                                    img = bg

                                # In Coloring Books: Drawing Area is 100% Black & White Line Art, Ref Thumbnail is Color
                                if elem_type == "main_image" and b_type == "coloring_book":
                                    from PIL import ImageEnhance
                                    gray = img.convert("L")
                                    enhancer = ImageEnhance.Contrast(gray)
                                    img = enhancer.enhance(2.8).convert("RGB")

                                # Apply inner image zoom, pan, and fit mode
                                zoom = float(elem.get("image_zoom") or 1.0)
                                pan_x = float(elem.get("image_pan_x") or 0.0)
                                pan_y = float(elem.get("image_pan_y") or 0.0)
                                fit_mode = elem.get("image_fit", "contain")

                                if zoom != 1.0 or pan_x != 0.0 or pan_y != 0.0 or fit_mode == "cover":
                                    orig_w, orig_h = img.size
                                    if fit_mode == "cover":
                                        target_ratio = (w / h) if h > 0 else 1.0
                                        current_ratio = orig_w / orig_h if orig_h > 0 else 1.0
                                        if current_ratio > target_ratio:
                                            new_w = int(orig_h * target_ratio)
                                            crop_x = int((orig_w - new_w) / 2)
                                            img = img.crop((crop_x, 0, crop_x + new_w, orig_h))
                                        else:
                                            new_h = int(orig_w / target_ratio)
                                            crop_y = int((orig_h - new_h) / 2)
                                            img = img.crop((0, crop_y, orig_w, crop_y + new_h))
                                        orig_w, orig_h = img.size

                                    if zoom > 1.0:
                                        crop_w = int(orig_w / zoom)
                                        crop_h = int(orig_h / zoom)
                                        offset_x = int((pan_x / 100.0) * (orig_w - crop_w))
                                        offset_y = int((pan_y / 100.0) * (orig_h - crop_h))
                                        cx = int((orig_w - crop_w) / 2) - offset_x
                                        cy = int((orig_h - crop_h) / 2) - offset_y
                                        cx = max(0, min(orig_w - crop_w, cx))
                                        cy = max(0, min(orig_h - crop_h, cy))
                                        img = img.crop((cx, cy, cx + crop_w, cy + crop_h))
                                    elif zoom < 1.0:
                                        scaled_w = max(10, int(orig_w * zoom))
                                        scaled_h = max(10, int(orig_h * zoom))
                                        resized = img.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
                                        new_bg = Image.new("RGB", (orig_w, orig_h), (255, 255, 255))
                                        paste_x = int((orig_w - scaled_w) / 2)
                                        paste_y = int((orig_h - scaled_h) / 2)
                                        new_bg.paste(resized, (paste_x, paste_y))
                                        img = new_bg

                                img_buffer = io.BytesIO()
                                img.save(img_buffer, format="JPEG", quality=95, dpi=(300, 300))
                                img_buffer.seek(0)

                                from reportlab.lib.utils import ImageReader
                                c.drawImage(ImageReader(img_buffer), x, y, width=w, height=h, preserveAspectRatio=True, anchor='c')
                        except Exception as e:
                            print(f"Error rendering image to PDF: {e}")
                    else:
                        c.setStrokeColor(colors.HexColor("#cbd5e1"))
                        c.setLineWidth(1.0)
                        c.setDash(4, 3)
                        c.roundRect(x, y, w, h, radius=6, fill=0, stroke=1)
                        c.setDash()
                        txt_label = elem.get("text") or ("Ref Image" if elem_type == "ref_image" else "Coloring Drawing")
                        if txt_label and "click to" not in txt_label.lower():
                            c.setFont("Helvetica", 10 * scale_y)
                            c.setFillColor(colors.HexColor("#94a3b8"))
                            c.drawCentredString(x + (w / 2.0), y + (h / 2.0) - 4, txt_label)

                elif elem_type == "title":
                    # If this is a specialized activity page (sudoku, maze, etc.), skip redundant canvas title to prevent overlap
                    is_special_page = bool(
                        page.get("puzzles") or page.get("games") or page.get("maze") or 
                        page.get("word_search") or page.get("tracing") or page.get("scissor_skills") or 
                        page.get("shadow_matching") or page.get("ispy") or page.get("grid_drawing") or
                        page.get("dot_to_dot")
                    )
                    if is_special_page:
                        continue

                    text = elem.get("text", "")
                    if text:
                        raw_size = float(elem.get("font_size", 38))
                        font_size = raw_size * scale_y * 0.95
                        alignment = elem.get("alignment", "center")
                        is_outline = elem.get("is_outline", True)
                        text_y = y + (h / 2.0) - (font_size / 3.0)

                        if is_outline:
                            c.setFont("Helvetica-Bold", font_size)
                            c.setStrokeColor(colors.HexColor(elem.get("stroke_color", "#0f172a")))
                            c.setFillColor(colors.white)
                            c.setLineWidth(1.5 * scale_y)
                            c._code.append("2 Tr\n")  # Fill and stroke outline

                            if alignment == "left":
                                c.drawString(x, text_y, text)
                            elif alignment == "right":
                                c.drawRightString(x + w, text_y, text)
                            else:
                                c.drawCentredString(x + (w / 2.0), text_y, text)

                            c._code.append("0 Tr\n")
                        else:
                            c.setFont("Helvetica-Bold", font_size)
                            c.setFillColor(colors.HexColor(elem.get("color", "#111827")))
                            if alignment == "left":
                                c.drawString(x, text_y, text)
                            elif alignment == "right":
                                c.drawRightString(x + w, text_y, text)
                            else:
                                c.drawCentredString(x + (w / 2.0), text_y, text)

                elif elem_type == "border":
                    is_special_page = bool(
                        page.get("puzzles") or page.get("games") or page.get("maze") or 
                        page.get("word_search") or page.get("tracing") or page.get("scissor_skills") or 
                        page.get("shadow_matching") or page.get("ispy") or page.get("grid_drawing") or
                        page.get("dot_to_dot")
                    )
                    if is_special_page:
                        continue
                    c.setStrokeColor(colors.HexColor("#111827"))
                    c.setLineWidth(1.5)
                    c.roundRect(x, y, w, h, radius=6, fill=0, stroke=1)

            # 3. If page has Sudoku Puzzles attached, render vector Sudoku grids
            puzzles = page.get("puzzles", [])
            if puzzles:
                num_p = len(puzzles)
                p = puzzles[0]
                p_id_str = p.get("id", f"sudoku_{page_idx + 1}").replace("sudoku_", "#")
                
                # Single clean crisp Centered Title
                c.setFont("Helvetica-Bold", 20)
                c.setFillColor(colors.HexColor("#0f172a"))
                c.drawCentredString(page_w / 2.0, page_h - 48 - bleed_pt, f"SUDOKU PUZZLE {p_id_str}")

                # Difficulty Subtitle
                diff_text = f"Difficulty: {p.get('difficulty', 'Medium')}"
                c.setFont("Helvetica", 10.5)
                c.setFillColor(colors.HexColor("#64748b"))
                c.drawCentredString(page_w / 2.0, page_h - 68 - bleed_pt, diff_text)

                grid = p.get("puzzle_grid", [])
                grid_sz = min(trim_w - 90, trim_h - 160)
                gx = (page_w - grid_sz) / 2.0
                gy = page_h - 95 - bleed_pt - grid_sz

                # Draw 9x9 Sudoku Grid
                cell_sz = grid_sz / 9.0
                for r in range(9):
                    for col in range(9):
                        cx = gx + (col * cell_sz)
                        cy = gy + ((8 - r) * cell_sz)
                        c.setStrokeColor(colors.HexColor("#cbd5e1"))
                        c.setLineWidth(0.6)
                        c.rect(cx, cy, cell_sz, cell_sz, fill=0, stroke=1)

                        val = grid[r][col] if r < len(grid) and col < len(grid[r]) else 0
                        if val != 0:
                            c.setFont("Helvetica-Bold", cell_sz * 0.55)
                            c.setFillColor(colors.HexColor("#0f172a"))
                            c.drawCentredString(cx + (cell_sz / 2.0), cy + (cell_sz / 2.0) - (cell_sz * 0.18), str(val))

                # Thick 3x3 block borders
                c.setStrokeColor(colors.HexColor("#0f172a"))
                c.setLineWidth(2.0)
                for b_row in range(3):
                    for b_col in range(3):
                        bx = gx + (b_col * cell_sz * 3)
                        by = gy + (b_row * cell_sz * 3)
                        c.rect(bx, by, cell_sz * 3, cell_sz * 3, fill=0, stroke=1)

            # 4. If page has Tic-Tac-Toe games attached, render vector game grids
            games = page.get("games", [])
            if games:
                c.setFont("Helvetica-Bold", 18)
                c.setFillColor(colors.HexColor("#0f172a"))
                c.drawCentredString(page_w / 2.0, page_h - 55 - bleed_pt, "TIC-TAC-TOE")

                cols = 2 if len(games) >= 2 else 1
                rows = 2 if len(games) >= 3 else (len(games) if len(games) <= 2 else 1)
                
                margin_x = 40 + bleed_pt
                margin_y = 75 + bleed_pt
                spacing = 16.0
                
                avail_w = page_w - (margin_x * 2) - ((cols - 1) * spacing)
                avail_h = page_h - margin_y - 45 - bleed_pt - ((rows - 1) * spacing)
                
                card_w = avail_w / cols
                card_h = avail_h / rows

                for idx, g in enumerate(games[:cols * rows]):
                    r = idx // cols
                    col = idx % cols
                    
                    gx = margin_x + (col * (card_w + spacing))
                    gy = page_h - margin_y - ((r + 1) * card_h) - (r * spacing)

                    # Draw Card Frame
                    c.setStrokeColor(colors.HexColor("#cbd5e1"))
                    c.setLineWidth(1.0)
                    c.roundRect(gx, gy, card_w, card_h, radius=8, fill=0, stroke=1)

                    # Header
                    c.setFont("Helvetica-Bold", 11)
                    c.setFillColor(colors.HexColor("#0f172a"))
                    c.drawString(gx + 12, gy + card_h - 20, g.get("title", f"Game #{idx+1:03d}"))

                    # Player Tags
                    c.setFont("Helvetica", 8)
                    c.setFillColor(colors.HexColor("#475569"))
                    c.drawString(gx + 12, gy + card_h - 36, g.get("player_x_label", "Player X: ________"))
                    c.drawString(gx + 12, gy + card_h - 50, g.get("player_o_label", "Player O: ________"))

                    # 3x3 Grid
                    grid_box_sz = min(card_w * 0.65, card_h * 0.52)
                    grid_x = gx + (card_w - grid_box_sz) / 2.0
                    grid_y = gy + 28
                    cell_s = grid_box_sz / 3.0

                    c.setStrokeColor(colors.HexColor("#0f172a"))
                    c.setLineWidth(1.8)
                    # Vertical lines
                    c.line(grid_x + cell_s, grid_y, grid_x + cell_s, grid_y + grid_box_sz)
                    c.line(grid_x + (cell_s * 2), grid_y, grid_x + (cell_s * 2), grid_y + grid_box_sz)
                    # Horizontal lines
                    c.line(grid_x, grid_y + cell_s, grid_x + grid_box_sz, grid_y + cell_s)
                    c.line(grid_x, grid_y + (cell_s * 2), grid_x + grid_box_sz, grid_y + (cell_s * 2))

                    # Winner box
                    c.setFont("Helvetica-Bold", 7.5)
                    c.setFillColor(colors.HexColor("#334155"))
                    c.drawCentredString(gx + (card_w / 2.0), gy + 12, g.get("winner_label", "Winner: [ X ]  [ O ]  [ Tie ]"))

            # 5. If page has Maze attached, render vector labyrinth
            maze = page.get("maze")
            if maze:
                m_id_str = maze.get("id", "maze_1").replace("maze_", "#")
                c.setFont("Helvetica-Bold", 18)
                c.setFillColor(colors.HexColor("#0f172a"))
                c.drawCentredString(page_w / 2.0, page_h - 55 - bleed_pt, f"MAZE PUZZLE {m_id_str}")

                mw = maze.get("width", 15)
                mh = maze.get("height", 20)
                grid = maze.get("grid", [])

                avail_w = trim_w - 90
                avail_h = trim_h - 150
                cell_s = min(avail_w / mw, avail_h / mh)
                
                maze_box_w = cell_s * mw
                maze_box_h = cell_s * mh
                
                mx = (page_w - maze_box_w) / 2.0
                my = page_h - 85 - bleed_pt - maze_box_h

                c.setStrokeColor(colors.HexColor("#0f172a"))
                c.setLineWidth(1.8)

                for r in range(mh):
                    for col in range(mw):
                        cx = mx + (col * cell_s)
                        cy = my + ((mh - 1 - r) * cell_s)
                        cell_mask = grid[r][col] if r < len(grid) and col < len(grid[r]) else 0

                        # Top wall: if not North (1)
                        if (cell_mask & 1) == 0:
                            c.line(cx, cy + cell_s, cx + cell_s, cy + cell_s)
                        # Right wall: if not East (2)
                        if (cell_mask & 2) == 0:
                            c.line(cx + cell_s, cy, cx + cell_s, cy + cell_s)
                        # Bottom wall: if not South (4)
                        if (cell_mask & 4) == 0:
                            c.line(cx, cy, cx + cell_s, cy)
                        # Left wall: if not West (8)
                        if (cell_mask & 8) == 0:
                            c.line(cx, cy, cx, cy + cell_s)

                # Start & Finish markers
                c.setFont("Helvetica-Bold", 9)
                c.setFillColor(colors.HexColor("#16a34a"))
                c.drawString(mx + 4, my + maze_box_h - cell_s + 4, "START")
                c.setFillColor(colors.HexColor("#dc2626"))
                c.drawRightString(mx + maze_box_w - 4, my + 4, "FINISH")

            # 6. If page has Word Search attached, render 12x12 grid and word bank
            ws = page.get("word_search")
            if ws:
                theme = ws.get("theme", "Vocabulary").title()
                ws_id = ws.get("id", "ws_1").replace("ws_", "#")
                
                c.setFont("Helvetica-Bold", 18)
                c.setFillColor(colors.HexColor("#0f172a"))
                c.drawCentredString(page_w / 2.0, page_h - 50 - bleed_pt, f"WORD SEARCH {ws_id}")

                c.setFont("Helvetica", 11)
                c.setFillColor(colors.HexColor("#475569"))
                c.drawCentredString(page_w / 2.0, page_h - 70 - bleed_pt, f"Topic: {theme}")

                g_size = ws.get("grid_size", 12)
                grid = ws.get("grid", [])
                
                grid_sz = min(trim_w - 80, 360)
                cell_sz = grid_sz / g_size
                gx = (page_w - grid_sz) / 2.0
                gy = page_h - 100 - bleed_pt - grid_sz

                # Draw outer frame
                c.setStrokeColor(colors.HexColor("#cbd5e1"))
                c.setLineWidth(1.0)
                c.roundRect(gx - 8, gy - 8, grid_sz + 16, grid_sz + 16, radius=6, fill=0, stroke=1)

                # Draw Letters
                for r in range(g_size):
                    for col in range(g_size):
                        cx = gx + (col * cell_sz)
                        cy = gy + ((g_size - 1 - r) * cell_sz)
                        ch = grid[r][col] if r < len(grid) and col < len(grid[r]) else ""
                        if ch:
                            c.setFont("Helvetica-Bold", cell_sz * 0.55)
                            c.setFillColor(colors.HexColor("#0f172a"))
                            c.drawCentredString(cx + (cell_sz / 2.0), cy + (cell_sz / 2.0) - (cell_sz * 0.18), ch)

                # Word Bank below
                words = ws.get("words", [])
                if words:
                    c.setFont("Helvetica-Bold", 10)
                    c.setFillColor(colors.HexColor("#0f172a"))
                    c.drawCentredString(page_w / 2.0, gy - 28, "FIND THESE WORDS:")

                    num_w = len(words)
                    cols = 4 if num_w >= 8 else 3
                    w_col_w = (page_w - 80) / cols
                    
                    c.setFont("Helvetica-Bold", 9)
                    c.setFillColor(colors.HexColor("#334155"))
                    for i, w in enumerate(words):
                        wc = i % cols
                        wr = i // cols
                        wx = 40 + (wc * w_col_w) + (w_col_w / 2.0)
                        wy = gy - 48 - (wr * 16)
                        c.drawCentredString(wx, wy, f"[  ] {w}")

            # 7. If page has Dot-to-Dot attached, render vector points and number labels
            dot_data = page.get("dot_to_dot")
            if dot_data and dot_data.get("dots"):
                dots = dot_data.get("dots", [])
                pz_w = dot_data.get("canvas_w", 420)
                pz_h = dot_data.get("canvas_h", 460)

                target_w = trim_w - 90
                target_h = trim_h - 180
                scale_dot = min(target_w / pz_w, target_h / pz_h)

                origin_x = (page_w - (pz_w * scale_dot)) / 2.0
                origin_y = page_h - 130 - bleed_pt - (pz_h * scale_dot)

                # Draw dots and numbers
                for d in dots:
                    num = d.get("num", 1)
                    dx = origin_x + (d.get("x", 0) * scale_dot)
                    dy = origin_y + ((pz_h - d.get("y", 0)) * scale_dot)
                    
                    lbl_x = origin_x + (d.get("label_x", d.get("x", 0)) * scale_dot)
                    lbl_y = origin_y + ((pz_h - d.get("label_y", d.get("y", 0))) * scale_dot) - 3

                    if num == 1:
                        c.setFillColor(colors.HexColor("#0f172a"))
                        c.circle(dx, dy, 3.8, fill=1, stroke=0)
                        c.setFont("Helvetica-Bold", 9.0)
                        c.setFillColor(colors.HexColor("#0f172a"))
                        c.drawCentredString(dx, dy + 8, "START 1")
                    else:
                        c.setFillColor(colors.HexColor("#0f172a"))
                        c.circle(dx, dy, 2.5, fill=1, stroke=0)
                        c.setFont("Helvetica-Bold", 7.5)
                        c.setFillColor(colors.HexColor("#1e293b"))
                        c.drawCentredString(lbl_x, lbl_y, str(num))

            # 8. If page has Tracing data, render 3-line penmanship guidelines & letters
            tracing_data = page.get("tracing")
            if tracing_data:
                target_char = tracing_data.get("target_char", "A")
                target_lower = tracing_data.get("target_lower", "a")
                sample_word = tracing_data.get("sample_word", "APPLE")
                
                c.setFont("Helvetica-Bold", 18)
                c.setFillColor(colors.HexColor("#0f172a"))
                c.drawCentredString(page_w / 2.0, page_h - 45 - bleed_pt, f"LETTER TRACING: {target_char} {target_lower}")

                c.setFont("Helvetica", 10)
                c.setFillColor(colors.HexColor("#64748b"))
                c.drawCentredString(page_w / 2.0, page_h - 62 - bleed_pt, f"Trace the letters and practice writing the word '{sample_word}'")

                lines = tracing_data.get("lines", [])
                start_y = page_h - 110 - bleed_pt
                row_h = 75.0
                guideline_w = page_w - 80

                for r_idx, row in enumerate(lines[:6]):
                    gy = start_y - (r_idx * row_h)
                    
                    # Top line (Solid)
                    c.setStrokeColor(colors.HexColor("#0f172a"))
                    c.setLineWidth(1.2)
                    c.line(40, gy + 36, 40 + guideline_w, gy + 36)

                    # Mid line (Dashed)
                    c.setStrokeColor(colors.HexColor("#94a3b8"))
                    c.setLineWidth(0.8)
                    c.setDash(4, 3)
                    c.line(40, gy + 18, 40 + guideline_w, gy + 18)
                    c.setDash()

                    # Base line (Solid)
                    c.setStrokeColor(colors.HexColor("#0f172a"))
                    c.setLineWidth(1.2)
                    c.line(40, gy, 40 + guideline_w, gy)

                    # Render sample letters
                    r_type = row.get("type", "uppercase_trace")
                    if r_type == "headline":
                        c.setFont("Helvetica-Bold", 32)
                        c.setFillColor(colors.HexColor("#0f172a"))
                        c.drawString(60, gy + 4, f"{target_char}  {target_lower}")
                        c.setFont("Helvetica-Bold", 18)
                        c.drawString(200, gy + 8, f"➔  {sample_word}")
                    elif r_type == "uppercase_trace":
                        c.setFont("Helvetica", 28)
                        c.setFillColor(colors.HexColor("#cbd5e1"))
                        for slot in range(5):
                            c.drawString(60 + (slot * 80), gy + 4, target_char)
                    elif r_type == "lowercase_trace":
                        c.setFont("Helvetica", 26)
                        c.setFillColor(colors.HexColor("#cbd5e1"))
                        for slot in range(5):
                            c.drawString(60 + (slot * 80), gy + 4, target_lower)
                    elif r_type == "word_trace":
                        c.setFont("Helvetica", 20)
                        c.setFillColor(colors.HexColor("#cbd5e1"))
                        for slot in range(2):
                            c.drawString(60 + (slot * 180), gy + 4, sample_word)

            # 9. If page has Scissor Skills cutting data, render cutting lines & cut-paste boxes
            scissor_data = page.get("scissor_skills")
            if scissor_data:
                stype = scissor_data.get("type", "scissor_cutting")
                title_txt = scissor_data.get("title", "Scissor Cutting Practice")

                c.setFont("Helvetica-Bold", 18)
                c.setFillColor(colors.HexColor("#0f172a"))
                c.drawCentredString(page_w / 2.0, page_h - 45 - bleed_pt, title_txt.upper())

                c.setFont("Helvetica", 9.5)
                c.setFillColor(colors.HexColor("#64748b"))
                c.drawCentredString(page_w / 2.0, page_h - 65 - bleed_pt, scissor_data.get("instructions", "Carefully cut along the dotted lines!"))

                if stype == "scissor_cutting":
                    lines = scissor_data.get("lines", [])
                    for l in lines:
                        ly = page_h - 80 - bleed_pt - (l.get("index", 1) * 85)
                        pattern = l.get("pattern", "zigzag")

                        # Draw Scissor Text Icon
                        c.setFont("Helvetica-Bold", 16)
                        c.setFillColor(colors.HexColor("#0f172a"))
                        c.drawString(38, ly - 4, "✂")

                        # Draw Target Star Icon
                        c.drawString(page_w - 55, ly - 4, "★")

                        # Draw Dotted Cut Path
                        c.setStrokeColor(colors.HexColor("#0f172a"))
                        c.setLineWidth(1.5)
                        c.setDash(6, 4)
                        if pattern == "zigzag":
                            p = c.beginPath()
                            p.moveTo(65, ly)
                            step_x = 30.0
                            for step in range(12):
                                sx = 65 + (step * step_x)
                                sy = ly + (18 if step % 2 == 1 else -18)
                                p.lineTo(sx, sy)
                            p.lineTo(page_w - 65, ly)
                            c.drawPath(p, fill=0, stroke=1)
                        elif pattern == "wavy":
                            p = c.beginPath()
                            p.moveTo(65, ly)
                            step_x = 40.0
                            for step in range(9):
                                sx = 65 + (step * step_x)
                                sy = ly + (14 if step % 2 == 1 else -14)
                                p.curveTo(sx - 15, sy, sx + 15, sy, sx + step_x, ly)
                            p.lineTo(page_w - 65, ly)
                            c.drawPath(p, fill=0, stroke=1)
                        else:  # Straight
                            c.line(65, ly, page_w - 65, ly)
                        c.setDash()

            # 10. If page has Shadow Matching data, render pairs matching lines
            shadow_data = page.get("shadow_matching")
            if shadow_data:
                c.setFont("Helvetica-Bold", 18)
                c.setFillColor(colors.HexColor("#0f172a"))
                c.drawCentredString(page_w / 2.0, page_h - 45 - bleed_pt, shadow_data.get("title", "SHADOW MATCHING").upper())

                c.setFont("Helvetica", 10)
                c.setFillColor(colors.HexColor("#64748b"))
                c.drawCentredString(page_w / 2.0, page_h - 65 - bleed_pt, shadow_data.get("instructions", "Draw a line to connect each item with its shadow!"))

                left_items = shadow_data.get("left_items", [])
                right_shadows = shadow_data.get("right_shadows", [])

                for idx, item in enumerate(left_items):
                    iy = page_h - 130 - bleed_pt - (idx * 115)
                    # Left Item Box
                    c.setStrokeColor(colors.HexColor("#cbd5e1"))
                    c.setLineWidth(1.0)
                    c.roundRect(45, iy, 140, 95, radius=8, fill=0, stroke=1)
                    c.setFont("Helvetica-Bold", 12)
                    c.setFillColor(colors.HexColor("#0f172a"))
                    c.drawCentredString(115, iy + 40, item.get("name", "Animal"))

                    # Left Connect Node
                    c.setFillColor(colors.HexColor("#0f172a"))
                    c.circle(195, iy + 47, 4, fill=1, stroke=0)

                for idx, item in enumerate(right_shadows):
                    iy = page_h - 130 - bleed_pt - (idx * 115)
                    # Right Shadow Box
                    c.setStrokeColor(colors.HexColor("#0f172a"))
                    c.setFillColor(colors.HexColor("#1e293b"))
                    c.roundRect(page_w - 185, iy, 140, 95, radius=8, fill=1, stroke=1)
                    c.setFont("Helvetica-Bold", 12)
                    c.setFillColor(colors.HexColor("#ffffff"))
                    c.drawCentredString(page_w - 115, iy + 40, "SHADOW")

                    # Right Connect Node
                    c.setFillColor(colors.HexColor("#0f172a"))
                    c.circle(page_w - 195, iy + 47, 4, fill=1, stroke=0)

            # 11. If page has I-SPY Counting data, render frame & checklist boxes
            ispy_data = page.get("ispy")
            if ispy_data:
                c.setFont("Helvetica-Bold", 18)
                c.setFillColor(colors.HexColor("#0f172a"))
                c.drawCentredString(page_w / 2.0, page_h - 45 - bleed_pt, ispy_data.get("title", "I SPY & COUNT").upper())

                c.setFont("Helvetica", 9.5)
                c.setFillColor(colors.HexColor("#64748b"))
                c.drawCentredString(page_w / 2.0, page_h - 65 - bleed_pt, ispy_data.get("instructions", "Find, count, and write the numbers in the boxes!"))

                # Main Search Area Border
                c.setStrokeColor(colors.HexColor("#0f172a"))
                c.setLineWidth(1.5)
                c.roundRect(40, 160 + bleed_pt, page_w - 80, page_h - 240 - (bleed_pt * 2), radius=10, fill=0, stroke=1)

                # Render Scattered Items Text
                scattered = ispy_data.get("scattered_objects", [])
                for obj in scattered:
                    ox = 45 + (obj.get("x", 50) * 0.95)
                    oy = 170 + bleed_pt + (obj.get("y", 100) * 0.85)
                    c.setFont("Helvetica-Bold", 14)
                    c.setFillColor(colors.HexColor("#0f172a"))
                    c.drawCentredString(ox, oy, obj.get("name", "Item"))

                # Bottom Checklist Boxes
                checklist = ispy_data.get("checklist", [])
                ch_w = (page_w - 80) / max(1, len(checklist))
                for c_idx, ch in enumerate(checklist):
                    cx = 40 + (c_idx * ch_w)
                    cy = 80 + bleed_pt
                    c.setFont("Helvetica-Bold", 11)
                    c.setFillColor(colors.HexColor("#0f172a"))
                    c.drawString(cx + 8, cy + 30, ch.get("name", "Item"))
                    c.setStrokeColor(colors.HexColor("#0f172a"))
                    c.setLineWidth(1.5)
                    c.rect(cx + 8, cy, 40, 24, fill=0, stroke=1)

            # 12. If page has Grid Drawing data, render 2-grid (reference + empty copy)
            grid_data = page.get("grid_drawing")
            if grid_data:
                dim = grid_data.get("grid_dimension", 4)
                c.setFont("Helvetica-Bold", 18)
                c.setFillColor(colors.HexColor("#0f172a"))
                c.drawCentredString(page_w / 2.0, page_h - 45 - bleed_pt, grid_data.get("title", "LEARN TO DRAW: GRID COPY").upper())

                c.setFont("Helvetica", 10)
                c.setFillColor(colors.HexColor("#64748b"))
                c.drawCentredString(page_w / 2.0, page_h - 65 - bleed_pt, grid_data.get("instructions", "Copy the drawing square-by-square into the empty grid!"))

                grid_px = 190.0
                cell_s = grid_px / dim
                gy = page_h - 110 - bleed_pt - grid_px

                # Left Grid (Reference)
                gx1 = 45.0
                c.setFont("Helvetica-Bold", 12)
                c.setFillColor(colors.HexColor("#0f172a"))
                c.drawCentredString(gx1 + (grid_px / 2.0), gy + grid_px + 10, "1. REFERENCE GRID")
                c.setStrokeColor(colors.HexColor("#cbd5e1"))
                c.setLineWidth(0.8)
                for r in range(dim + 1):
                    c.line(gx1, gy + (r * cell_s), gx1 + grid_px, gy + (r * cell_s))
                    c.line(gx1 + (r * cell_s), gy, gx1 + (r * cell_s), gy + grid_px)
                c.setStrokeColor(colors.HexColor("#0f172a"))
                c.setLineWidth(1.5)
                c.rect(gx1, gy, grid_px, grid_px, fill=0, stroke=1)

                # Right Grid (Empty Drawing Box)
                gx2 = page_w - 45.0 - grid_px
                c.setFont("Helvetica-Bold", 12)
                c.setFillColor(colors.HexColor("#0f172a"))
                c.drawCentredString(gx2 + (grid_px / 2.0), gy + grid_px + 10, "2. YOUR DRAWING GRID")
                c.setStrokeColor(colors.HexColor("#cbd5e1"))
                c.setLineWidth(0.8)
                for r in range(dim + 1):
                    c.line(gx2, gy + (r * cell_s), gx2 + grid_px, gy + (r * cell_s))
                    c.line(gx2 + (r * cell_s), gy, gx2 + (r * cell_s), gy + grid_px)
                c.setStrokeColor(colors.HexColor("#0f172a"))
                c.setLineWidth(1.5)
                c.rect(gx2, gy, grid_px, grid_px, fill=0, stroke=1)

            # Optional Bottom-Center Page Number
            if include_page_numbers:
                page_display_num = fm_count + 1 + (page_idx * 2 if single_sided else page_idx)
                c.setFont("Helvetica-Bold", 10)
                c.setFillColor(colors.HexColor("#334155"))
                c.drawCentredString(page_w / 2.0, 18 + bleed_pt, str(page_display_num))

            c.showPage()

            # Insert Single-Sided Blank Back Page (Verso)
            if single_sided:
                render_blank_page()

        # =========================================================================
        # 4. SUDOKU AUTOMATIC SOLUTIONS SECTION (DIVIDER + 2x2 MULTI-GRID SOLUTION PAGES)
        # =========================================================================
        all_sudoku_puzzles = []
        for p_idx, cp in enumerate(content_pages):
            p_num = fm_count + 1 + p_idx
            for pz in cp.get("puzzles", []):
                all_sudoku_puzzles.append({
                    "puzzle": pz,
                    "page_num": p_num
                })

        if all_sudoku_puzzles:
            # 1. Interval Divider / Title Page (e.g. Page 11 after 10 puzzle pages)
            c.setStrokeColor(colors.HexColor("#0f172a"))
            c.setLineWidth(2.0)
            c.roundRect(35 + bleed_pt, 35 + bleed_pt, page_w - 70 - (bleed_pt * 2), page_h - 70 - (bleed_pt * 2), radius=12, fill=0, stroke=1)
            c.setLineWidth(0.8)
            c.roundRect(42 + bleed_pt, 42 + bleed_pt, page_w - 84 - (bleed_pt * 2), page_h - 84 - (bleed_pt * 2), radius=8, fill=0, stroke=1)

            c.setFont("Helvetica-Bold", 32)
            c.setFillColor(colors.HexColor("#0f172a"))
            c.drawCentredString(page_w / 2.0, page_h / 2.0 + 40, "PUZZLE SOLUTIONS")

            c.setFont("Helvetica", 14)
            c.setFillColor(colors.HexColor("#475569"))
            first_id = all_sudoku_puzzles[0]["puzzle"].get("id", "sudoku_1").replace("sudoku_", "#")
            last_id = all_sudoku_puzzles[-1]["puzzle"].get("id", f"sudoku_{len(all_sudoku_puzzles)}").replace("sudoku_", "#")
            c.drawCentredString(page_w / 2.0, page_h / 2.0, f"Answers for Puzzles {first_id} to {last_id}")

            c.setFont("Helvetica-Oblique", 11)
            c.setFillColor(colors.HexColor("#94a3b8"))
            c.drawCentredString(page_w / 2.0, page_h / 2.0 - 30, "Check your work and verify your answers below!")

            c.showPage()
            if single_sided:
                render_blank_page()

            # 2. Multi-Grid Solution Pages (4 per page in 2x2 grid)
            SOLS_PER_PAGE = 4
            for chunk_start in range(0, len(all_sudoku_puzzles), SOLS_PER_PAGE):
                chunk = all_sudoku_puzzles[chunk_start:chunk_start + SOLS_PER_PAGE]
                
                # Header
                ch_first = chunk[0]["puzzle"].get("id", "").replace("sudoku_", "#")
                ch_last = chunk[-1]["puzzle"].get("id", "").replace("sudoku_", "#")
                c.setFont("Helvetica-Bold", 16)
                c.setFillColor(colors.HexColor("#0f172a"))
                c.drawCentredString(page_w / 2.0, page_h - 45 - bleed_pt, f"SOLUTIONS: {ch_first} - {ch_last}")

                margin_x = 40 + bleed_pt
                margin_top = 70 + bleed_pt
                grid_sz = (page_w - (margin_x * 2) - 30) / 2.0

                for idx, item in enumerate(chunk):
                    pz = item["puzzle"]
                    orig_page = item["page_num"]
                    p_id = pz.get("id", f"sudoku_{chunk_start + idx + 1}").replace("sudoku_", "#")

                    col = idx % 2
                    row = idx // 2

                    gx = margin_x + (col * (grid_sz + 30))
                    gy = page_h - margin_top - ((row + 1) * (grid_sz + 45)) + 20

                    # Draw 9x9 Solution Board
                    sol_grid = pz.get("solution_grid", [])
                    cell_sz = grid_sz / 9.0
                    for r in range(9):
                        for c_idx in range(9):
                            cx = gx + (c_idx * cell_sz)
                            cy = gy + ((8 - r) * cell_sz)
                            c.setStrokeColor(colors.HexColor("#cbd5e1"))
                            c.setLineWidth(0.4)
                            c.rect(cx, cy, cell_sz, cell_sz, fill=0, stroke=1)

                            val = sol_grid[r][c_idx] if r < len(sol_grid) and c_idx < len(sol_grid[r]) else 0
                            if val != 0:
                                c.setFont("Helvetica-Bold", cell_sz * 0.55)
                                c.setFillColor(colors.HexColor("#0f172a"))
                                c.drawCentredString(cx + (cell_sz / 2.0), cy + (cell_sz / 2.0) - (cell_sz * 0.18), str(val))

                    # Thick 3x3 block borders
                    c.setStrokeColor(colors.HexColor("#0f172a"))
                    c.setLineWidth(1.4)
                    for b_row in range(3):
                        for b_col in range(3):
                            bx = gx + (b_col * cell_sz * 3)
                            by = gy + (b_row * cell_sz * 3)
                            c.rect(bx, by, cell_sz * 3, cell_sz * 3, fill=0, stroke=1)

                    # Clear Solution Label underneath with Page Number cross-reference
                    c.setFont("Helvetica-Bold", 10.5)
                    c.setFillColor(colors.HexColor("#0f172a"))
                    c.drawCentredString(gx + (grid_sz / 2.0), gy - 16, f"Puzzle {p_id} (Page {orig_page}) Solution")

                c.showPage()
                if single_sided:
                    render_blank_page()

        # =========================================================================
        # 5. BACK MATTER CUSTOM PAGE (e.g. Author Note, Thank You, Review Request)
        # =========================================================================
        if inc_custom_page and custom_page_pos == "back":
            render_custom_text_page()

        c.save()
        return output_path

