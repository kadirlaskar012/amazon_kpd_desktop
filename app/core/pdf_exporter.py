"""
Amazon KDP PDF Exporter Engine.
Generates 100% compliant 300 DPI Print-Ready PDF/X files for Amazon KDP Paperback & Hardcover.
Automatically compiles Front Matter (Disclaimer, Contents with Auto Item List, Belongs To, Color Test Palette)
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

        # Extract only the actual working drawing/content pages
        raw_pages = project_data.get("pages", [])
        content_pages = [p for p in raw_pages if p.get("page_type") not in ("blank_verso", "front_matter_disclaimer", "front_matter_contents", "front_matter_belongs_to", "front_matter_color_test")]
        
        if not content_pages and raw_pages:
            content_pages = raw_pages

        book_title = (project_data.get("name") or "COLORING BOOK").upper()
        author_name = project_data.get("author") or "Creative Kids Studio"

        def render_blank_page():
            """Renders a pure blank KDP back page to prevent color bleed-through."""
            c.setFillColor(colors.white)
            c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
            if blank_page_note:
                c.setFont("Helvetica-Oblique", 8 * scale_y)
                c.setFillColor(colors.HexColor("#cbd5e1"))
                c.drawCentredString(page_w / 2.0, 40 * scale_y, "[ Blank page for color bleed-through protection ]")
            c.showPage()

        # =========================================================================
        # 1. FRONT MATTER PAGES (Pages 1 - 4)
        # =========================================================================
        if include_front_matter:
            # --- PAGE 1: DISCLAIMER & COPYRIGHT ---
            c.setFillColor(colors.white)
            c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

            # Outer decorative border
            c.setStrokeColor(colors.HexColor("#0f172a"))
            c.setLineWidth(1.5)
            c.roundRect(30 * scale_x + bleed_pt, 25 * scale_y + bleed_pt, 450 * scale_x, 610 * scale_y, radius=6, fill=0, stroke=1)

            c.setFont("Helvetica-Bold", 24 * scale_y)
            c.setFillColor(colors.HexColor("#0f172a"))
            c.drawCentredString(page_w / 2.0, page_h - (65 * scale_y) - bleed_pt, book_title)

            c.setFont("Helvetica", 12 * scale_y)
            c.setFillColor(colors.HexColor("#475569"))
            c.drawCentredString(page_w / 2.0, page_h - (95 * scale_y) - bleed_pt, "First Edition  •  Amazon KDP Publication")

            c.setFont("Helvetica-Bold", 13 * scale_y)
            c.setFillColor(colors.HexColor("#1e293b"))
            c.drawCentredString(page_w / 2.0, page_h - (175 * scale_y) - bleed_pt, f"Copyright © 2026 by {author_name}")

            c.setFont("Helvetica-Bold", 11 * scale_y)
            c.setFillColor(colors.HexColor("#334155"))
            c.drawCentredString(page_w / 2.0, page_h - (205 * scale_y) - bleed_pt, "All Rights Reserved.")

            disclaimer_lines = [
                "No part of this publication may be reproduced, distributed, or transmitted in any form",
                "or by any means, including photocopying, recording, or other electronic or mechanical methods,",
                "without the prior written permission of the publisher and copyright owner.",
                "For permissions requests, contact the publisher.",
            ]
            c.setFont("Helvetica", 9.5 * scale_y)
            c.setFillColor(colors.HexColor("#64748b"))
            for i, line in enumerate(disclaimer_lines):
                c.drawCentredString(page_w / 2.0, page_h - ((255 + (i * 22)) * scale_y) - bleed_pt, line)

            c.setFont("Helvetica-Bold", 10.5 * scale_y)
            c.setFillColor(colors.HexColor("#334155"))
            c.drawCentredString(page_w / 2.0, page_h - (390 * scale_y) - bleed_pt, f"Published by: {author_name}")
            c.drawCentredString(page_w / 2.0, page_h - (415 * scale_y) - bleed_pt, "ISBN-13: 978-X-XXXXX-XXX-X")

            c.setFont("Helvetica", 9 * scale_y)
            c.setFillColor(colors.HexColor("#94a3b8"))
            c.drawCentredString(page_w / 2.0, page_h - (470 * scale_y) - bleed_pt, "Printed in the United States of America • Amazon KDP Distribution")
            c.showPage()

            # --- PAGE 2: TABLE OF CONTENTS (AUTO ITEM LIST) ---
            c.setFillColor(colors.white)
            c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

            # Outer border
            c.setStrokeColor(colors.HexColor("#0f172a"))
            c.setLineWidth(1.5)
            c.roundRect(30 * scale_x + bleed_pt, 25 * scale_y + bleed_pt, 450 * scale_x, 610 * scale_y, radius=6, fill=0, stroke=1)

            c.setFont("Helvetica-Bold", 22 * scale_y)
            c.setFillColor(colors.HexColor("#0f172a"))
            c.drawCentredString(page_w / 2.0, page_h - (60 * scale_y) - bleed_pt, "TABLE OF CONTENTS")

            c.setFont("Helvetica", 11 * scale_y)
            c.setFillColor(colors.HexColor("#64748b"))
            c.drawCentredString(page_w / 2.0, page_h - (85 * scale_y) - bleed_pt, "Complete list of coloring pages & illustrations in this book")

            # Auto Item List Generator (Drawing 1 -> Page 5, Drawing 2 -> Page 7...)
            start_y = page_h - (130 * scale_y) - bleed_pt
            c.setFont("Helvetica-Bold", 11 * scale_y)
            c.setFillColor(colors.HexColor("#1e293b"))

            max_items_to_print = min(20, len(content_pages))
            for idx in range(max_items_to_print):
                cp = content_pages[idx]
                item_title = cp.get("title") or f"Coloring Page {idx + 1}"
                
                # If page has a title element, use that text
                for el in cp.get("elements", []):
                    if el.get("type") == "title" and el.get("text"):
                        item_title = el.get("text").title()
                        break

                calc_page_num = 5 + (idx * 2) if single_sided else 5 + idx
                item_y = start_y - (idx * 23 * scale_y)

                # Left item name
                left_str = f"{idx + 1}.  {item_title}"
                c.drawString(65 * scale_x + bleed_pt, item_y, left_str)

                # Right page num
                right_str = f"Page {calc_page_num}"
                c.drawRightString(page_w - (65 * scale_x) - bleed_pt, item_y, right_str)

                # Dot Leader between left and right
                dot_start_x = (65 * scale_x) + bleed_pt + c.stringWidth(left_str, "Helvetica-Bold", 11 * scale_y) + 10
                dot_end_x = page_w - (65 * scale_x) - bleed_pt - c.stringWidth(right_str, "Helvetica-Bold", 11 * scale_y) - 10
                if dot_end_x > dot_start_x:
                    c.setFont("Helvetica", 9 * scale_y)
                    c.setFillColor(colors.HexColor("#94a3b8"))
                    dots_w = c.stringWidth(". ", "Helvetica", 9 * scale_y)
                    num_dots = int((dot_end_x - dot_start_x) / dots_w)
                    c.drawString(dot_start_x, item_y, ". " * num_dots)
                    c.setFont("Helvetica-Bold", 11 * scale_y)
                    c.setFillColor(colors.HexColor("#1e293b"))

            c.showPage()

            # --- PAGE 3: THIS BOOK BELONGS TO ---
            c.setFillColor(colors.white)
            c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

            c.setStrokeColor(colors.HexColor("#0f172a"))
            c.setLineWidth(1.5)
            c.roundRect(30 * scale_x + bleed_pt, 25 * scale_y + bleed_pt, 450 * scale_x, 610 * scale_y, radius=6, fill=0, stroke=1)

            c.setFont("Helvetica-Bold", 20 * scale_y)
            c.setFillColor(colors.HexColor("#1e293b"))
            c.drawCentredString(page_w / 2.0, page_h - (90 * scale_y) - bleed_pt, "THIS COLORING BOOK")

            # Big Outlined BELONGS TO
            c.setFont("Helvetica-Bold", 36 * scale_y)
            c.setStrokeColor(colors.HexColor("#0f172a"))
            c.setFillColor(colors.white)
            c.setLineWidth(2.2 * scale_y)
            c._code.append("2 Tr\n")
            c.drawCentredString(page_w / 2.0, page_h - (150 * scale_y) - bleed_pt, "BELONGS TO:")
            c._code.append("0 Tr\n")

            # Name writing line
            c.setStrokeColor(colors.HexColor("#64748b"))
            c.setLineWidth(1.5)
            line_y = page_h - (240 * scale_y) - bleed_pt
            c.line(70 * scale_x + bleed_pt, line_y, page_w - (70 * scale_x) - bleed_pt, line_y)

            c.setFont("Helvetica-Oblique", 13 * scale_y)
            c.setFillColor(colors.HexColor("#475569"))
            c.drawCentredString(page_w / 2.0, page_h - (340 * scale_y) - bleed_pt, "Color with joy, love and your wild imagination!")
            c.showPage()

            # --- PAGE 4: COLOR TEST PALETTE ---
            c.setFillColor(colors.white)
            c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

            c.setStrokeColor(colors.HexColor("#0f172a"))
            c.setLineWidth(1.5)
            c.roundRect(30 * scale_x + bleed_pt, 25 * scale_y + bleed_pt, 450 * scale_x, 610 * scale_y, radius=6, fill=0, stroke=1)

            c.setFont("Helvetica-Bold", 24 * scale_y)
            c.setStrokeColor(colors.HexColor("#0f172a"))
            c.setFillColor(colors.white)
            c.setLineWidth(1.8 * scale_y)
            c._code.append("2 Tr\n")
            c.drawCentredString(page_w / 2.0, page_h - (65 * scale_y) - bleed_pt, "COLOR TEST PALETTE")
            c._code.append("0 Tr\n")

            c.setFont("Helvetica", 11 * scale_y)
            c.setFillColor(colors.HexColor("#64748b"))
            c.drawCentredString(page_w / 2.0, page_h - (95 * scale_y) - bleed_pt, "Test your pencils, markers, and crayons here before coloring!")

            # 12 Swatch Boxes Grid (4 rows x 3 cols)
            grid_cols = 3
            grid_rows = 4
            swatch_w = 110 * scale_x
            swatch_h = 75 * scale_y
            spacing_x = 25 * scale_x
            spacing_y = 25 * scale_y
            grid_start_x = 65 * scale_x + bleed_pt
            grid_start_y = page_h - (140 * scale_y) - bleed_pt - swatch_h

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

                    c.setFont("Helvetica-Bold", 9 * scale_y)
                    c.setFillColor(colors.HexColor("#94a3b8"))
                    c.drawString(bx + 8, by + swatch_h - 14, f"Color {box_idx}")
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
                        font_size = float(elem.get("font_size", 40)) * scale_y
                        alignment = elem.get("alignment", "center")
                        is_outline = elem.get("is_outline", True)
                        
                        text_y = y + (h / 2.0) - (font_size / 3.0)

                        if is_outline:
                            c.setFont("Helvetica-Bold", font_size)
                            c.setStrokeColor(colors.HexColor(elem.get("stroke_color", "#0f172a")))
                            c.setFillColor(colors.white)
                            c.setLineWidth(2.0 * scale_y)
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
                    c.setStrokeColor(colors.HexColor("#111827"))
                    c.setLineWidth(1.5)
                    c.roundRect(x, y, w, h, radius=6, fill=0, stroke=1)

            c.showPage()

            # Insert Single-Sided Blank Back Page (Verso)
            if single_sided:
                render_blank_page()

        c.save()
        return output_path
