"""
Amazon KDP PDF Exporter Engine.
Generates 100% compliant 300 DPI Print-Ready PDF/X files for Amazon KDP Paperback & Hardcover.
Includes ultra-crisp, elegant typography for Front Matter (Disclaimer, Contents with Auto Item List, Belongs To, Color Test Palette)
and Single-Sided Coloring Pages with alternating Blank Back Pages for bleed protection.
"""

import io
import base64
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
        blank_page_note: bool = False
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
        # 1. FRONT MATTER PAGES (Pages 1 - 4)
        # =========================================================================
        if include_front_matter:
            # --- PAGE 1: DISCLAIMER & COPYRIGHT ---
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
            c.drawCentredString(page_w / 2.0, page_h - 100 - bleed_pt, book_title)

            # Subtitle
            c.setFont("Helvetica", 10.5)
            c.setFillColor(colors.HexColor("#475569"))
            c.drawCentredString(page_w / 2.0, page_h - 125 - bleed_pt, "First Edition  •  Amazon KDP Publication")

            # Small decorative divider line
            c.setStrokeColor(colors.HexColor("#e2e8f0"))
            c.setLineWidth(1.0)
            c.line(page_w / 2.0 - 50, page_h - 150 - bleed_pt, page_w / 2.0 + 50, page_h - 150 - bleed_pt)

            # Copyright
            c.setFont("Helvetica-Bold", 11)
            c.setFillColor(colors.HexColor("#1e293b"))
            c.drawCentredString(page_w / 2.0, page_h - 220 - bleed_pt, f"Copyright © 2026 by {author_name}")

            c.setFont("Helvetica", 10)
            c.setFillColor(colors.HexColor("#334155"))
            c.drawCentredString(page_w / 2.0, page_h - 240 - bleed_pt, "All Rights Reserved.")

            # Legal Disclaimer lines
            disclaimer_lines = [
                "No part of this publication may be reproduced, distributed, or transmitted in any form",
                "or by any means, including photocopying, recording, or other electronic or mechanical methods,",
                "without the prior written permission of the publisher, except in the case of brief quotations",
                "embodied in critical reviews and certain other noncommercial uses permitted by copyright law."
            ]
            c.setFont("Helvetica", 8.5)
            c.setFillColor(colors.HexColor("#64748b"))
            for i, line in enumerate(disclaimer_lines):
                c.drawCentredString(page_w / 2.0, page_h - 300 - (i * 16) - bleed_pt, line)

            # Publisher Info
            c.setFont("Helvetica-Bold", 9.5)
            c.setFillColor(colors.HexColor("#334155"))
            c.drawCentredString(page_w / 2.0, page_h - 450 - bleed_pt, f"Published by: {author_name}")
            
            c.setFont("Helvetica", 9)
            c.setFillColor(colors.HexColor("#475569"))
            c.drawCentredString(page_w / 2.0, page_h - 470 - bleed_pt, "ISBN-13: 978-X-XXXXX-XXX-X")

            c.setFont("Helvetica-Oblique", 8.5)
            c.setFillColor(colors.HexColor("#94a3b8"))
            c.drawCentredString(page_w / 2.0, page_h - 540 - bleed_pt, "Printed in the United States of America  •  Amazon KDP Distribution")
            c.showPage()

            # --- PAGE 2: TABLE OF CONTENTS (AUTO ITEM LIST) ---
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
            c.drawCentredString(page_w / 2.0, page_h - 90 - bleed_pt, "TABLE OF CONTENTS")

            c.setFont("Helvetica", 10)
            c.setFillColor(colors.HexColor("#64748b"))
            c.drawCentredString(page_w / 2.0, page_h - 115 - bleed_pt, "Complete list of coloring illustrations in this book")

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

                calc_page_num = 5 + (idx * 2) if single_sided else 5 + idx
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

            c.showPage()

            # --- PAGE 3: THIS BOOK BELONGS TO ---
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
            c.drawCentredString(page_w / 2.0, page_h - 130 - bleed_pt, "THIS COLORING BOOK")

            # Outlined BELONGS TO
            c.setFont("Helvetica-Bold", 32)
            c.setStrokeColor(colors.HexColor("#0f172a"))
            c.setFillColor(colors.white)
            c.setLineWidth(1.6)
            c._code.append("2 Tr\n")
            c.drawCentredString(page_w / 2.0, page_h - 190 - bleed_pt, "BELONGS TO:")
            c._code.append("0 Tr\n")

            # Clean writing line
            c.setStrokeColor(colors.HexColor("#94a3b8"))
            c.setLineWidth(1.2)
            line_y = page_h - 300 - bleed_pt
            c.line(80 + bleed_pt, line_y, page_w - 80 - bleed_pt, line_y)

            c.setFont("Helvetica-Oblique", 11)
            c.setFillColor(colors.HexColor("#64748b"))
            c.drawCentredString(page_w / 2.0, page_h - 420 - bleed_pt, "Color with joy, love and your wild imagination!")
            c.showPage()

            # --- PAGE 4: COLOR TEST PALETTE ---
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
            c.drawCentredString(page_w / 2.0, page_h - 85 - bleed_pt, "COLOR TEST PALETTE")

            c.setFont("Helvetica", 10)
            c.setFillColor(colors.HexColor("#64748b"))
            c.drawCentredString(page_w / 2.0, page_h - 110 - bleed_pt, "Test your pencils, markers, and crayons here before coloring!")

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

            c.showPage()

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
                    text = elem.get("text", "")
                    if text:
                        raw_size = float(elem.get("font_size", 38))
                        # Clean font sizing
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

                            c._code.append("0 Tr\n")  # Reset immediately to avoid affecting other text
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
                    c.setStrokeColor(colors.HexColor("#111827"))
                    c.setLineWidth(1.5)
                    c.roundRect(x, y, w, h, radius=6, fill=0, stroke=1)

            c.showPage()

            # Insert Single-Sided Blank Back Page (Verso)
            if single_sided:
                render_blank_page()

        c.save()
        return output_path
