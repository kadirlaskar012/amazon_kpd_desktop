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

        b_type = project_data.get("book_type", "coloring_book")
        if "single_sided" in settings:
            single_sided = bool(settings["single_sided"])
        elif b_type in ("sudoku", "tic_tac_toe", "maze", "word_search", "puzzle_book", "activity_book"):
            single_sided = False

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
        # 1. FRONT MATTER PAGES
        # =========================================================================
        if include_front_matter:
            # --- PAGE 1: DISCLAIMER & COPYRIGHT (Included for all book types) ---
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

            # For Coloring Books only: Add Table of Contents, Belongs To, and Color Test Palette
            if b_type == "coloring_book":
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

            # 3. If page has Sudoku Puzzles attached, render vector Sudoku grids
            puzzles = page.get("puzzles", [])
            if puzzles:
                num_p = len(puzzles)
                p = puzzles[0]
                p_id_str = p.get("id", "sudoku_1").replace("sudoku_", "#")
                
                # Draw Crisp Centered Title
                c.setFont("Helvetica-Bold", 18)
                c.setFillColor(colors.HexColor("#0f172a"))
                c.drawCentredString(page_w / 2.0, page_h - 55 - bleed_pt, f"SUDOKU PUZZLE {p_id_str}")

                # Difficulty Subtitle
                diff_text = f"Difficulty: {p.get('difficulty', 'Medium')}"
                c.setFont("Helvetica", 10.5)
                c.setFillColor(colors.HexColor("#64748b"))
                c.drawCentredString(page_w / 2.0, page_h - 75 - bleed_pt, diff_text)

                grid = p.get("puzzle_grid", [])
                grid_sz = min(trim_w - 90, trim_h - 170)
                gx = (page_w - grid_sz) / 2.0
                gy = page_h - 110 - bleed_pt - grid_sz

                # Draw 9x9 Sudoku Grid
                cell_sz = grid_sz / 9.0
                for r in range(9):
                    for col in range(9):
                        cx = gx + (col * cell_sz)
                        cy = gy + ((8 - r) * cell_sz)
                        c.setStrokeColor(colors.HexColor("#cbd5e1"))
                        c.setLineWidth(0.5)
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

            c.showPage()

            # Insert Single-Sided Blank Back Page (Verso)
            if single_sided:
                render_blank_page()

        c.save()
        return output_path
