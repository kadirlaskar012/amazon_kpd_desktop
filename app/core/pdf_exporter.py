"""
KDP PDF Exporter Engine.
Generates Amazon KDP Print-Ready 300 DPI PDF files with exact trim, bleed, vector text, and images.
"""

import io
import base64
from pathlib import Path
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors


class KDPPdfExporter:
    @staticmethod
    def generate_pdf(project_data: dict, output_path: Path) -> Path:
        """
        Generates a multi-page PDF/X ready document matching KDP specification.
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

        pages = project_data.get("pages", [])
        if not pages:
            # Fallback single blank page
            c.showPage()
            c.save()
            return output_path

        for page in pages:
            # 1. Fill page with pure white
            c.setFillColor(colors.white)
            c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

            # 2. Draw Elements
            elements = page.get("elements", [])
            for elem in elements:
                elem_type = elem.get("type", "")
                x = (float(elem.get("x", 0)) * scale_x) + bleed_pt
                # Canvas (0,0) is top-left; PDF (0,0) is bottom-left
                w = float(elem.get("w", 50)) * scale_x
                h = float(elem.get("h", 50)) * scale_y
                y = page_h - (float(elem.get("y", 0)) * scale_y) - h - bleed_pt

                if elem_type in ("ref_image", "main_image"):
                    img_src = elem.get("image_src")
                    if img_src and isinstance(img_src, str):
                        try:
                            # Handle base64 DataURL
                            if "," in img_src:
                                header, encoded = img_src.split(",", 1)
                                img_bytes = base64.b64decode(encoded)
                                img = Image.open(io.BytesIO(img_bytes))
                            elif Path(img_src).exists():
                                img = Image.open(img_src)
                            else:
                                img = None

                            if img:
                                # Convert RGBA to RGB for standard PDF printing
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

                elif elem_type == "title":
                    text = elem.get("text", "")
                    font_size = float(elem.get("font_size", 24)) * scale_y
                    alignment = elem.get("alignment", "center")
                    c.setFont("Helvetica-Bold", font_size)
                    c.setFillColor(colors.HexColor(elem.get("color", "#111827")))
                    text_y = y + (h / 2.0) - (font_size / 3.0)
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

                elif elem_type == "tracing":
                    c.setStrokeColor(colors.HexColor("#9ca3af"))
                    c.setLineWidth(0.8)
                    # Top guide line
                    c.line(x, y + h, x + w, y + h)
                    # Mid dashed guide line
                    c.setDash(4, 3)
                    c.line(x, y + (h / 2.0), x + w, y + (h / 2.0))
                    # Bottom guide line
                    c.setDash()
                    c.line(x, y, x + w, y)

            c.showPage()

        c.save()
        return output_path
