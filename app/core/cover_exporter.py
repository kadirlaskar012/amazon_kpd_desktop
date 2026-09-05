"""
Amazon KDP Cover PDF Exporter Engine.
Generates 100% Amazon KDP compliant 300 DPI Full Wrap Cover PDF (Back Cover + Spine + Front Cover + 0.125 in Bleed).
Calculates exact spine thickness based on page count and paper type (white vs cream).
"""

import io
import base64
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib import colors


class KDPCoverExporter:
    # Amazon KDP Official Thickness Multipliers (in inches per page)
    WHITE_PAPER_PAGE_THICKNESS = 0.002252  # Black & white or standard color on white paper
    CREAM_PAPER_PAGE_THICKNESS = 0.002500  # Black & white on cream paper
    COLOR_PAPER_PAGE_THICKNESS = 0.002347  # Premium color on white paper

    @classmethod
    def calculate_spine_width_in(cls, page_count: int, paper_type: str = "white") -> float:
        """Calculates spine width in inches based on Amazon KDP formula."""
        if paper_type == "cream":
            multiplier = cls.CREAM_PAPER_PAGE_THICKNESS
        elif paper_type == "premium_color":
            multiplier = cls.COLOR_PAPER_PAGE_THICKNESS
        else:
            multiplier = cls.WHITE_PAPER_PAGE_THICKNESS
        
        # Amazon KDP calculates spine width based on total page count
        return max(0.06, page_count * multiplier)

    @classmethod
    def generate_cover_pdf(
        cls,
        project_data: dict,
        output_path: Path,
        cover_config: dict = None
    ) -> Path:
        """
        Generates full-spread Amazon KDP Paperback cover PDF (Back + Spine + Front + Bleed).
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cover_config = cover_config or {}

        settings = project_data.get("settings", {})
        trim_w_pt = float(settings.get("trim_width_pt", 612.0))   # 8.5 in * 72
        trim_h_pt = float(settings.get("trim_height_pt", 792.0))  # 11.0 in * 72
        bleed_pt = 9.0  # Amazon KDP standard 0.125 in bleed on all 4 outer edges

        pages = project_data.get("pages", [])
        page_count = max(24, len(pages))
        paper_type = cover_config.get("paper_type", "white")

        spine_w_in = cls.calculate_spine_width_in(page_count, paper_type)
        spine_w_pt = spine_w_in * 72.0

        # Total Cover Spread Width = Bleed + Back Cover + Spine + Front Cover + Bleed
        total_w_pt = (bleed_pt * 2) + (trim_w_pt * 2) + spine_w_pt
        total_h_pt = trim_h_pt + (bleed_pt * 2)

        c = canvas.Canvas(str(output_path), pagesize=(total_w_pt, total_h_pt))

        # 1. Fill Background
        bg_color_hex = cover_config.get("bg_color", "#1e1b4b")
        c.setFillColor(colors.HexColor(bg_color_hex))
        c.rect(0, 0, total_w_pt, total_h_pt, fill=1, stroke=0)

        # 2. Compute Zones in pt:
        # Back Cover: from bleed_pt to (bleed_pt + trim_w_pt)
        back_x = bleed_pt
        back_w = trim_w_pt
        # Spine: from (bleed_pt + trim_w_pt) to (bleed_pt + trim_w_pt + spine_w_pt)
        spine_x = bleed_pt + trim_w_pt
        # Front Cover: from (spine_x + spine_w_pt) to (spine_x + spine_w_pt + trim_w_pt)
        front_x = spine_x + spine_w_pt
        front_w = trim_w_pt

        # 3. Draw Spine Area
        spine_bg = cover_config.get("spine_color", bg_color_hex)
        c.setFillColor(colors.HexColor(spine_bg))
        c.rect(spine_x, 0, spine_w_pt, total_h_pt, fill=1, stroke=0)

        # Spine Text (Only allowed if page count >= 79 per Amazon KDP rules)
        if page_count >= 79 and spine_w_in >= 0.2:
            c.saveState()
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", min(14.0, spine_w_pt * 0.7))
            # Rotate for spine text reading top-to-bottom
            c.translate(spine_x + (spine_w_pt / 2.0), total_h_pt / 2.0)
            c.rotate(-90)
            spine_title = (project_data.get("name") or "COLORING BOOK").upper()
            author = project_data.get("author") or ""
            full_spine_text = f"{spine_title}   •   {author}" if author else spine_title
            c.drawCentredString(0, -4, full_spine_text)
            c.restoreState()

        # 4. Draw Front Cover Elements
        proj_title = (cover_config.get("title") or project_data.get("name") or "JUNGLE COLORING BOOK").upper()
        subtitle = cover_config.get("subtitle") or "50+ Fun & Easy Coloring Pages For Kids"
        author_name = cover_config.get("author") or project_data.get("author") or "Creative Kids Studio"

        # Front Title Box
        c.setFont("Helvetica-Bold", 36)
        c.setFillColor(colors.HexColor("#fbbf24"))  # Warm gold / vibrant yellow
        c.drawCentredString(front_x + (front_w / 2.0), total_h_pt - bleed_pt - 90, proj_title)

        # Front Subtitle
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.white)
        c.drawCentredString(front_x + (front_w / 2.0), total_h_pt - bleed_pt - 130, subtitle)

        # Front Cover Main Artwork Image (if provided)
        front_art = cover_config.get("front_image")
        if not front_art:
            # Pick first available image from project media or pages
            for p in pages:
                for el in p.get("elements", []):
                    if el.get("type") in ("main_image", "ref_image") and el.get("image_src"):
                        front_art = el.get("image_src")
                        break
                if front_art:
                    break

        if front_art and isinstance(front_art, str):
            try:
                if "," in front_art:
                    header, encoded = front_art.split(",", 1)
                    img_bytes = base64.b64decode(encoded)
                    img = Image.open(io.BytesIO(img_bytes))
                elif Path(front_art).exists():
                    img = Image.open(front_art)
                else:
                    img = None

                if img:
                    if img.mode in ("RGBA", "LA", "P"):
                        bg = Image.new("RGB", img.size, (255, 255, 255))
                        if img.mode == "P":
                            img = img.convert("RGBA")
                        bg.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
                        img = bg

                    img_buf = io.BytesIO()
                    img.save(img_buf, format="JPEG", quality=95, dpi=(300, 300))
                    img_buf.seek(0)

                    from reportlab.lib.utils import ImageReader
                    art_w = front_w * 0.75
                    art_h = art_w
                    art_x = front_x + ((front_w - art_w) / 2.0)
                    art_y = (total_h_pt / 2.0) - (art_h / 2.0) - 20
                    
                    # White decorative rounded card behind image
                    c.setFillColor(colors.white)
                    c.roundRect(art_x - 10, art_y - 10, art_w + 20, art_h + 20, radius=16, fill=1, stroke=0)
                    c.drawImage(ImageReader(img_buf), art_x, art_y, width=art_w, height=art_h, preserveAspectRatio=True, anchor='c')
            except Exception as e:
                print(f"Error drawing cover artwork: {e}")

        # Front Author Name
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.HexColor("#e2e8f0"))
        c.drawCentredString(front_x + (front_w / 2.0), bleed_pt + 45, f"By {author_name}")

        # 5. Draw Back Cover Elements
        back_heading = cover_config.get("back_heading", "WHY YOUR CHILD WILL LOVE THIS BOOK")
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(colors.HexColor(cover_config.get("accent_color", "#fbbf24")))
        c.drawCentredString(back_x + (back_w / 2.0), total_h_pt - bleed_pt - 90, back_heading)

        # Back Features List (Dynamic from AI or project configuration)
        features = cover_config.get("back_features") or cover_config.get("features") or [
            f"• {page_count}+ High-Quality Hand-Drawn Illustrations",
            "• Single-Sided Bleed-Safe Pages (No Marker Bleed)",
            "• Color by Reference Guides For Extra Fun",
            f"• Large {project_data.get('settings', {}).get('trim_width_in', 8.5)}x{project_data.get('settings', {}).get('trim_height_in', 11)} in Format for Little Hands",
            "• Wonderful Screen-Free Gift for Toddlers & Kids"
        ]
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.white)
        start_feat_y = total_h_pt - bleed_pt - 140
        for i, feat in enumerate(features[:6]):
            safe_feat = feat
            for symbol in ["✨", "🛡️", "🐾", "🎯", "🎁", "🧠", "⭐", "🚀", "🎉", "📘", "🌟"]:
                safe_feat = safe_feat.replace(symbol, "•")
            safe_feat = safe_feat.strip()
            if not safe_feat.startswith("•"):
                safe_feat = f"• {safe_feat}"
            c.drawString(back_x + 50, start_feat_y - (i * 28), safe_feat)

        # Amazon KDP Barcode Reservation Box on Back Cover (Bottom Right)
        # KDP automatically places ISBN barcode in a 2.0 x 1.2 in zone
        barcode_box_w = 2.0 * 72.0
        barcode_box_h = 1.2 * 72.0
        barcode_x = back_x + back_w - barcode_box_w - 36
        barcode_y = bleed_pt + 28
        
        c.setFillColor(colors.HexColor("#f8fafc"))
        c.setStrokeColor(colors.HexColor("#cbd5e1"))
        c.setLineWidth(1)
        c.roundRect(barcode_x, barcode_y, barcode_box_w, barcode_box_h, radius=4, fill=1, stroke=1)
        c.setFillColor(colors.HexColor("#94a3b8"))
        c.setFont("Helvetica", 8)
        c.drawCentredString(barcode_x + (barcode_box_w / 2.0), barcode_y + (barcode_box_h / 2.0) - 3, "[ Amazon KDP Barcode Zone ]")

        c.showPage()
        c.save()
        return output_path

    @classmethod
    def generate_cover_image(
        cls,
        project_data: dict,
        output_path: Path,
        cover_config: dict = None
    ) -> Path:
        """
        Generates 300 DPI High-Resolution Full-Wrap Cover Image (PNG).
        Converts the official KDP Cover PDF directly using PyMuPDF if available,
        or renders pixel-perfect full spread layout using Pillow.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cover_config = cover_config or {}

        # 1. First generate PDF to a temp file to attempt pixel-perfect PDF conversion
        temp_pdf = output_path.with_suffix(".temp.pdf")
        pdf_rendered = False
        try:
            cls.generate_cover_pdf(project_data, temp_pdf, cover_config=cover_config)
            pdf_rendered = True
            
            # Attempt conversion via pymupdf
            try:
                import pymupdf
                doc = pymupdf.open(str(temp_pdf))
                page = doc[0]
                pix = page.get_pixmap(dpi=300)
                pix.save(str(output_path))
                doc.close()
                if temp_pdf.exists():
                    temp_pdf.unlink()
                return output_path
            except Exception as pdf_err:
                print(f"PyMuPDF not available in current python ({pdf_err}), falling back to Pillow 300 DPI renderer")
        except Exception as e:
            print(f"PDF pre-render notice: {e}")

        # 2. High-Resolution Pillow 300 DPI Fallback Engine
        settings = project_data.get("settings", {})
        trim_w_pt = float(settings.get("trim_width_pt", 612.0))
        trim_h_pt = float(settings.get("trim_height_pt", 792.0))
        bleed_pt = 9.0

        pages = project_data.get("pages", [])
        page_count = max(24, len(pages))
        paper_type = cover_config.get("paper_type", "white")

        spine_w_in = cls.calculate_spine_width_in(page_count, paper_type)
        spine_w_pt = spine_w_in * 72.0

        total_w_pt = (bleed_pt * 2) + (trim_w_pt * 2) + spine_w_pt
        total_h_pt = trim_h_pt + (bleed_pt * 2)

        # Scale from 72 pt/in to 300 DPI
        scale = 300.0 / 72.0
        w_px = int(total_w_pt * scale)
        h_px = int(total_h_pt * scale)

        bg_hex = cover_config.get("bg_color", "#1e1b4b")
        accent_hex = cover_config.get("accent_color", "#fbbf24")

        from PIL import ImageDraw, ImageFont

        img = Image.new("RGB", (w_px, h_px), bg_hex)
        draw = ImageDraw.Draw(img)

        bleed_px = int(bleed_pt * scale)
        trim_w_px = int(trim_w_pt * scale)
        spine_w_px = int(spine_w_pt * scale)

        back_x = bleed_px
        spine_x = back_x + trim_w_px
        front_x = spine_x + spine_w_px

        # Spine highlight line
        draw.rectangle([spine_x, 0, spine_x + spine_w_px, h_px], fill=cover_config.get("spine_color", bg_hex))

        # Fonts
        font_title = None
        font_sub = None
        font_back_h = None
        font_text = None
        font_small = None
        for font_name in ["arialbd.ttf", "segoeuib.ttf", "calibrib.ttf", "DejaVuSans-Bold.ttf"]:
            try:
                font_title = ImageFont.truetype(font_name, int(28 * scale))
                font_sub = ImageFont.truetype(font_name, int(14 * scale))
                font_back_h = ImageFont.truetype(font_name, int(16 * scale))
                font_text = ImageFont.truetype("arial.ttf", int(11 * scale))
                font_small = ImageFont.truetype("arial.ttf", int(8 * scale))
                break
            except Exception:
                continue

        if not font_title:
            font_title = ImageFont.load_default()
            font_sub = font_title
            font_back_h = font_title
            font_text = font_title
            font_small = font_title

        # Front Cover Content
        proj_title = (cover_config.get("title") or project_data.get("name") or "COLORING BOOK").upper()
        subtitle = cover_config.get("subtitle") or f"{page_count}+ Fun & Easy Activities For Kids"
        author_name = cover_config.get("author") or project_data.get("author") or "Creative Kids Studio"

        draw.text((front_x + (trim_w_px // 2), bleed_px + int(60 * scale)), proj_title, fill=accent_hex, font=font_title, anchor="mt")
        draw.text((front_x + (trim_w_px // 2), bleed_px + int(100 * scale)), subtitle, fill="#ffffff", font=font_sub, anchor="mt")

        # Front Artwork
        front_art = cover_config.get("front_image")
        if not front_art:
            for p in pages:
                for el in p.get("elements", []):
                    if el.get("type") in ("main_image", "ref_image") and el.get("image_src"):
                        front_art = el.get("image_src")
                        break
                if front_art:
                    break

        if front_art and isinstance(front_art, str):
            try:
                if "," in front_art:
                    header, encoded = front_art.split(",", 1)
                    art_img = Image.open(io.BytesIO(base64.b64decode(encoded)))
                elif Path(front_art).exists():
                    art_img = Image.open(front_art)
                else:
                    art_img = None

                if art_img:
                    art_size = int(trim_w_px * 0.70)
                    art_img = art_img.convert("RGB")
                    art_img.thumbnail((art_size, art_size), Image.Resampling.LANCZOS)
                    art_card_x = front_x + ((trim_w_px - art_size) // 2)
                    art_card_y = (h_px // 2) - (art_size // 2) - int(10 * scale)

                    draw.rounded_rectangle(
                        [art_card_x - int(8 * scale), art_card_y - int(8 * scale),
                         art_card_x + art_size + int(8 * scale), art_card_y + art_size + int(8 * scale)],
                        radius=int(14 * scale),
                        fill="#ffffff"
                    )
                    paste_x = art_card_x + ((art_size - art_img.width) // 2)
                    paste_y = art_card_y + ((art_size - art_img.height) // 2)
                    img.paste(art_img, (paste_x, paste_y))
            except Exception as e:
                print(f"Error drawing Pillow cover art: {e}")

        # Front Author
        draw.text((front_x + (trim_w_px // 2), h_px - bleed_px - int(45 * scale)), f"By {author_name}", fill="#e2e8f0", font=font_sub, anchor="mb")

        # Back Cover Elements
        back_heading = cover_config.get("back_heading", "WHY YOUR CHILD WILL LOVE THIS BOOK")
        draw.text((back_x + (trim_w_px // 2), bleed_px + int(60 * scale)), back_heading, fill=accent_hex, font=font_back_h, anchor="mt")

        features = cover_config.get("back_features") or cover_config.get("features") or [
            f"• {page_count}+ High-Quality Hand-Drawn Illustrations",
            "• Single-Sided Pages (No Marker Bleed-Through)",
            "• Large Format Perfect for Little Hands",
            "• Builds Fine Motor Skills & Pencil Control",
            "• Wonderful Screen-Free Gift for Kids"
        ]

        feat_y = bleed_px + int(120 * scale)
        for feat in features[:6]:
            safe_feat = feat
            for symbol in ["✨", "🛡️", "🐾", "🎯", "🎁", "🧠", "⭐", "🚀", "🎉"]:
                safe_feat = safe_feat.replace(symbol, "•")
            safe_feat = safe_feat.strip()
            if not safe_feat.startswith("•"):
                safe_feat = f"• {safe_feat}"
            draw.text((back_x + int(45 * scale), feat_y), safe_feat, fill="#ffffff", font=font_text)
            feat_y += int(28 * scale)

        # Barcode Box (Bottom Right of Back Cover)
        bc_w = int(2.0 * 300)
        bc_h = int(1.2 * 300)
        bc_x = back_x + trim_w_px - bc_w - int(30 * scale)
        bc_y = h_px - bleed_px - bc_h - int(25 * scale)

        draw.rounded_rectangle([bc_x, bc_y, bc_x + bc_w, bc_y + bc_h], radius=int(4 * scale), fill="#f8fafc", outline="#cbd5e1", width=int(1 * scale))
        draw.text((bc_x + (bc_w // 2), bc_y + (bc_h // 2)), "[ Amazon KDP Barcode Zone ]", fill="#94a3b8", font=font_small, anchor="mm")

        img.save(str(output_path), format="PNG", dpi=(300, 300))
        if temp_pdf.exists():
            try:
                temp_pdf.unlink()
            except Exception:
                pass
        return output_path
