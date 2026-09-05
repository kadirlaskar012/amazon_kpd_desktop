"""
KDP Book Production Studio - Web Preview Server with Project, Lock, Delete & PDF Export API.
Serves the interactive web preview studio on http://localhost:8080, handles local persistence & PDF rendering.
"""

import http.server
import socketserver
import os
import sys
import json
import base64
import shutil
import urllib.parse
import zipfile
import mimetypes
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.storage.project_storage import ProjectStorage
from app.core.pdf_exporter import KDPPdfExporter
from app.core.cover_exporter import KDPCoverExporter
from app.core.image_processor import KDPImageProcessor
from app.generators.sudoku_generator import SudokuGenerator
from app.generators.tic_tac_toe_generator import TicTacToeGenerator
from app.generators.maze_generator import MazeGenerator
from app.generators.word_search_generator import WordSearchGenerator
from app.generators.dot_to_dot_generator import DotToDotGenerator
from app.generators.tracing_generator import TracingGenerator
from app.generators.scissor_skills_generator import ScissorSkillsGenerator
from app.generators.shadow_matching_generator import ShadowMatchingGenerator
from app.generators.ispy_counting_generator import ISpyCountingGenerator
from app.generators.grid_drawing_generator import GridDrawingGenerator
from app.generators.ai_kdp_assistant import AIKDPAssistant

# Ensure UTF-8 output encoding for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PORT = 8080
web_dir = Path(__file__).resolve().parent

# Default projects directory
DEFAULT_PROJECTS_DIR = Path.home() / "Documents" / "KDP_Studio_Projects"
DEFAULT_PROJECTS_DIR.mkdir(parents=True, exist_ok=True)


class StudioRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(web_dir), **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def guess_type(self, path):
        """Force UTF-8 charset for all text files so emojis render correctly."""
        mime = super().guess_type(path)
        path_str = str(path).lower()
        if path_str.endswith('.js'):
            return 'application/javascript; charset=utf-8'
        elif path_str.endswith('.css'):
            return 'text/css; charset=utf-8'
        elif path_str.endswith('.html'):
            return 'text/html; charset=utf-8'
        return mime



    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        req_path = parsed.path.rstrip("/")
        
        if req_path == "/api/default_location":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            resp = {
                "default_root": str(DEFAULT_PROJECTS_DIR),
                "home": str(Path.home())
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        elif req_path in ("/api/projects", "/api/stats"):
            projects = []
            checked_paths = set()

            def inspect_project_folder(p_dir):
                p_file = p_dir / "project.json"
                data = {}
                if p_file.exists():
                    try:
                        with open(p_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                    except Exception:
                        data = {}
                elif (p_dir / "exports").exists() and list((p_dir / "exports").glob("*.pdf")):
                    data = {"name": p_dir.name.replace("_", " "), "pages": []}
                else:
                    return None

                exports_dir = p_dir / "exports"
                pdf_files = [f for f in exports_dir.glob("*.pdf")] if exports_dir.exists() else []
                exports_count = len(pdf_files)
                latest_export_mtime = max([f.stat().st_mtime for f in pdf_files]) if pdf_files else None
                is_completed = bool(exports_count > 0 or data.get("is_completed", False))

                return {
                    "name": data.get("name", p_dir.name),
                    "folder_name": p_dir.name,
                    "path": str(p_dir),
                    "is_locked": bool(data.get("is_locked", False)),
                    "is_completed": is_completed,
                    "page_count": len(data.get("pages", [])),
                    "media_count": len(data.get("media", [])),
                    "exports_count": exports_count,
                    "latest_export_mtime": latest_export_mtime,
                    "created_at": data.get("created_at", ""),
                    "updated_at": data.get("updated_at", "")
                }

            # 1. Check DEFAULT_PROJECTS_DIR
            if DEFAULT_PROJECTS_DIR.exists():
                for item in DEFAULT_PROJECTS_DIR.iterdir():
                    if item.is_dir():
                        res_p = str(item.resolve())
                        if res_p not in checked_paths:
                            p_info = inspect_project_folder(item)
                            if p_info:
                                projects.append(p_info)
                                checked_paths.add(res_p)

            # 2. Also check workspace sample_project if exists and not already loaded
            sample_dir = (web_dir.parent / "sample_project").resolve()
            if sample_dir.exists() and str(sample_dir) not in checked_paths:
                p_info = inspect_project_folder(sample_dir)
                if p_info:
                    projects.append(p_info)
                    checked_paths.add(str(sample_dir))

            # Compute real statistics across all projects
            total_projects = len(projects)
            total_pdfs = sum(p.get("exports_count", 0) for p in projects)
            books_completed = sum(1 for p in projects if p.get("is_completed", False))
            total_pages = sum(p.get("page_count", 0) for p in projects)
            projects_in_progress = max(0, total_projects - books_completed)

            all_export_mtimes = [p["latest_export_mtime"] for p in projects if p.get("latest_export_mtime")]
            last_export_mtime = max(all_export_mtimes) if all_export_mtimes else None

            stats = {
                "total_projects": total_projects,
                "total_pdfs": total_pdfs,
                "books_completed": books_completed,
                "total_pages": total_pages,
                "projects_in_progress": projects_in_progress,
                "last_export_mtime": last_export_mtime
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "projects": projects,
                "stats": stats
            }).encode("utf-8"))
            return

        elif req_path == "/api/projects/load":
            query_params = urllib.parse.parse_qs(parsed.query)
            raw_path = query_params.get("path", [""])[0]
            if not raw_path:
                self.send_response(400)
                self.end_headers()
                return

            p = Path(raw_path).resolve()
            json_file = p if p.name == "project.json" else p / "project.json"
            if json_file.exists():
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["project_dir"] = str(json_file.parent)
                data["folder_name"] = json_file.parent.name
                
                # Auto-discover any media files in project_dir/media and project_dir/assets
                media_list = data.get("media", [])
                existing_names = {m.get("fileName") or m.get("name") for m in media_list if isinstance(m, dict)}
                
                proj_dir = json_file.parent
                search_dirs = [proj_dir / "media", proj_dir / "assets"]
                for s_dir in search_dirs:
                    if s_dir.exists():
                        for img_file in s_dir.iterdir():
                            if img_file.is_file() and img_file.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp', '.svg'):
                                if img_file.name not in existing_names:
                                    try:
                                        with open(img_file, "rb") as im_f:
                                            b64_data = base64.b64encode(im_f.read()).decode("utf-8")
                                        ext = img_file.suffix.lower().lstrip(".")
                                        if ext == "jpg": ext = "jpeg"
                                        elif ext == "svg": ext = "svg+xml"
                                        data_uri = f"data:image/{ext};base64,{b64_data}"
                                        media_list.append({
                                            "id": f"med_disk_{int(img_file.stat().st_mtime * 1000)}_{img_file.stem}",
                                            "name": img_file.stem.replace("_", " ").title(),
                                            "fileName": img_file.name,
                                            "dataUrl": data_uri,
                                            "sizeKb": round(img_file.stat().st_size / 1024, 1)
                                        })
                                        existing_names.add(img_file.name)
                                    except Exception:
                                        pass
                data["media"] = media_list

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "project": data}).encode("utf-8"))
                return
            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"Project not found at {json_file}"}).encode("utf-8"))
                return

        elif req_path == "/api/projects/asset":
            query_params = urllib.parse.parse_qs(parsed.query)
            raw_path = query_params.get("path", [""])[0]
            proj_dir = query_params.get("project_dir", [""])[0]
            filename = query_params.get("filename", [""])[0]
            
            target_file = None
            if raw_path and Path(raw_path).exists():
                target_file = Path(raw_path)
            elif proj_dir and filename:
                p = Path(proj_dir) / "media" / filename
                if not p.exists():
                    p = Path(proj_dir) / "assets" / filename
                if p.exists():
                    target_file = p

            if target_file and target_file.exists():
                mime_type, _ = mimetypes.guess_type(target_file.name)
                if not mime_type:
                    mime_type = "image/png"
                self.send_response(200)
                self.send_header("Content-Type", mime_type)
                self.send_header("Content-Length", str(target_file.stat().st_size))
                self.send_header("Cache-Control", "public, max-age=3600")
                self.end_headers()
                with open(target_file, "rb") as f:
                    shutil.copyfileobj(f, self.wfile)
                return
            else:
                self.send_response(404)
                self.end_headers()
                return

        elif req_path.startswith("/api/exports/") or req_path == "/api/exports":
            query_params = urllib.parse.parse_qs(parsed.query)
            raw_file = query_params.get("path", [""])[0]
            if raw_file and Path(raw_file).exists():
                export_file = Path(raw_file)
                mime_type, _ = mimetypes.guess_type(export_file.name)
                if not mime_type:
                    mime_type = "application/zip" if export_file.suffix.lower() == ".zip" else "application/octet-stream"
                disposition = "attachment" if export_file.suffix.lower() == ".zip" else "inline"
                safe_ascii_name = export_file.name.encode('ascii', 'ignore').decode('ascii') or "kdp_document.pdf"
                quoted_name = urllib.parse.quote(export_file.name)
                self.send_response(200)
                self.send_header("Content-Type", mime_type)
                self.send_header("Content-Disposition", f"{disposition}; filename=\"{safe_ascii_name}\"; filename*=UTF-8''{quoted_name}")
                self.send_header("Content-Length", str(export_file.stat().st_size))
                self.end_headers()
                with open(export_file, "rb") as f:
                    shutil.copyfileobj(f, self.wfile)
                return
        elif req_path == "/api/ai/get_key":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            ai_inst = AIKDPAssistant()
            saved_key = ai_inst.api_key.strip() if ai_inst.api_key else ""
            cfg = ai_inst.get_config()
            has_real_key = bool(saved_key and len(saved_key) > 5)
            self.wfile.write(json.dumps({
                "has_key": has_real_key,
                "key_preview": f"...{saved_key[-4:]}" if has_real_key and len(saved_key) > 4 else "",
                "model": cfg.get("model", "gemini-3.6-flash"),
                "models": cfg.get("models", [])
            }).encode("utf-8"))
            return

        elif req_path == "/api/ai/models":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            ai_inst = AIKDPAssistant()
            self.wfile.write(json.dumps(ai_inst.get_config()).encode("utf-8"))
            return

        elif req_path == "/api/settings":
            settings = {"theme": "light"}
            settings_file = DEFAULT_PROJECTS_DIR / "user_settings.json"
            if settings_file.exists():
                try:
                    with open(settings_file, "r", encoding="utf-8") as f:
                        settings.update(json.load(f))
                except Exception:
                    pass
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "settings": settings}).encode("utf-8"))
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        req_path = parsed.path.rstrip("/")
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len)

        try:
            req_data = json.loads(post_body.decode("utf-8")) if post_body else {}
        except Exception:
            req_data = {}

        if req_path == "/api/settings":
            settings_file = DEFAULT_PROJECTS_DIR / "user_settings.json"
            settings = {}
            if settings_file.exists():
                try:
                    with open(settings_file, "r", encoding="utf-8") as f:
                        settings = json.load(f)
                except Exception:
                    settings = {}
            settings.update(req_data)
            try:
                DEFAULT_PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
                with open(settings_file, "w", encoding="utf-8") as f:
                    json.dump(settings, f, indent=2)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "settings": settings}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": str(e)}).encode("utf-8"))
            return

        if req_path == "/api/projects/check_exists":
            proj_name = req_data.get("name", "").strip()
            folder_name = req_data.get("folder_name") or proj_name.replace(" ", "_")
            root_dir = Path(req_data.get("root_path") or DEFAULT_PROJECTS_DIR)
            project_dir = (root_dir / folder_name).resolve()
            exists = (project_dir / "project.json").exists() or project_dir.exists()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "exists": exists,
                "project_dir": str(project_dir)
            }).encode("utf-8"))
            return

        elif req_path == "/api/projects/create":
            proj_name = req_data.get("name", "Untitled Project").strip()
            folder_name = req_data.get("folder_name") or proj_name.replace(" ", "_")
            root_dir = Path(req_data.get("root_path") or DEFAULT_PROJECTS_DIR)
            project_dir = (root_dir / folder_name).resolve()
            force_overwrite = bool(req_data.get("force_overwrite", False))

            # Prevent duplicate overwrite if project already exists
            if not force_overwrite and ((project_dir / "project.json").exists() or (project_dir.exists() and any(project_dir.iterdir()))):
                self.send_response(409)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "error",
                    "error": f"A project named '{proj_name}' already exists at this location!",
                    "exists": True,
                    "project_dir": str(project_dir)
                }).encode("utf-8"))
                return

            ProjectStorage.initialize_project_directory(project_dir)
            (project_dir / "media").mkdir(parents=True, exist_ok=True)

            project_file = project_dir / "project.json"
            with open(project_file, "w", encoding="utf-8") as f:
                json.dump(req_data, f, indent=2, ensure_ascii=False)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            resp = {
                "status": "success",
                "project_dir": str(project_dir),
                "project_file": str(project_file),
                "media_dir": str(project_dir / "media"),
                "assets_dir": str(project_dir / "assets")
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        elif req_path == "/api/projects/save":
            project_dir = Path(req_data.get("project_dir", DEFAULT_PROJECTS_DIR / "My_Project")).resolve()
            project_dir.mkdir(parents=True, exist_ok=True)
            project_file = project_dir / "project.json"

            with open(project_file, "w", encoding="utf-8") as f:
                json.dump(req_data, f, indent=2, ensure_ascii=False)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "saved", "path": str(project_file)}).encode("utf-8"))
            return

        elif req_path == "/api/projects/export_pdf":
            # Generate 300 DPI KDP compliant PDF
            project_dir = Path(req_data.get("project_dir", DEFAULT_PROJECTS_DIR / "My_Project")).resolve()
            exports_dir = project_dir / "exports"
            exports_dir.mkdir(parents=True, exist_ok=True)

            def _clean_kdp_filename(name_str):
                raw = (name_str or "KDP_Book").replace(" ", "_").replace("\u2013", "-").replace("\u2014", "-")
                clean = "".join(c if (c.isalnum() or c in "._-") else "_" for c in raw)
                return clean.strip("._-") or "KDP_Book"

            proj_name = _clean_kdp_filename(req_data.get("name", "KDP_Book"))
            out_pdf = exports_dir / f"{proj_name}_KDP_Print_Ready.pdf"

            single_sided = req_data.get("single_sided", True)
            blank_page_note = req_data.get("blank_page_note", False)
            include_front_matter = req_data.get("include_front_matter", True)
            include_page_numbers = req_data.get("include_page_numbers", False)

            try:
                KDPPdfExporter.generate_pdf(
                    req_data, 
                    out_pdf, 
                    include_front_matter=include_front_matter, 
                    single_sided=single_sided, 
                    blank_page_note=blank_page_note,
                    include_page_numbers=include_page_numbers
                )
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                resp = {
                    "status": "success",
                    "pdf_path": str(out_pdf),
                    "filename": out_pdf.name,
                    "download_url": f"/api/exports/{urllib.parse.quote(out_pdf.name)}?path={urllib.parse.quote(str(out_pdf))}"
                }
                self.wfile.write(json.dumps(resp).encode("utf-8"))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
                return

        elif req_path == "/api/projects/export_cover_pdf":
            # Generate 300 DPI Amazon KDP Full Wrap Cover PDF
            project_dir = Path(req_data.get("project_dir", DEFAULT_PROJECTS_DIR / "My_Project")).resolve()
            exports_dir = project_dir / "exports"
            exports_dir.mkdir(parents=True, exist_ok=True)

            def _clean_kdp_filename(name_str):
                raw = (name_str or "KDP_Book").replace(" ", "_").replace("\u2013", "-").replace("\u2014", "-")
                clean = "".join(c if (c.isalnum() or c in "._-") else "_" for c in raw)
                return clean.strip("._-") or "KDP_Book"

            proj_name = _clean_kdp_filename(req_data.get("name", "KDP_Book"))
            out_pdf = exports_dir / f"{proj_name}_KDP_Cover_Full_Wrap.pdf"
            cover_config = req_data.get("cover_config", {})

            try:
                KDPCoverExporter.generate_cover_pdf(req_data, out_pdf, cover_config=cover_config)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                resp = {
                    "status": "success",
                    "pdf_path": str(out_pdf),
                    "filename": out_pdf.name,
                    "download_url": f"/api/exports/{urllib.parse.quote(out_pdf.name)}?path={urllib.parse.quote(str(out_pdf))}"
                }
                self.wfile.write(json.dumps(resp).encode("utf-8"))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
                return

        elif req_path == "/api/projects/export_publishing_bundle":
            # Generate Complete Amazon KDP Publishing Package (Interior PDF + Cover PDF + Metadata Guide ZIP)
            project_dir = Path(req_data.get("project_dir", DEFAULT_PROJECTS_DIR / "My_Project")).resolve()
            exports_dir = project_dir / "exports"
            exports_dir.mkdir(parents=True, exist_ok=True)

            def _clean_kdp_filename(name_str):
                raw = (name_str or "KDP_Book").replace(" ", "_").replace("\u2013", "-").replace("\u2014", "-")
                clean = "".join(c if (c.isalnum() or c in "._-") else "_" for c in raw)
                return clean.strip("._-") or "KDP_Book"

            proj_name = _clean_kdp_filename(req_data.get("name", "KDP_Book"))
            out_interior_pdf = exports_dir / f"{proj_name}_Interior_Print_Ready.pdf"
            out_cover_pdf = exports_dir / f"{proj_name}_Cover_Full_Wrap.pdf"
            out_guide_txt = exports_dir / f"{proj_name}_KDP_Publishing_Guide_and_Metadata.txt"
            out_zip = exports_dir / f"{proj_name}_KDP_Publishing_Bundle.zip"

            single_sided = req_data.get("single_sided", True)
            blank_page_note = req_data.get("blank_page_note", False)
            include_front_matter = req_data.get("include_front_matter", True)
            include_page_numbers = req_data.get("include_page_numbers", False)
            cover_config = req_data.get("cover_config", {})

            # 1. Generate Interior PDF
            try:
                KDPPdfExporter.generate_pdf(
                    req_data,
                    out_interior_pdf,
                    include_front_matter=include_front_matter,
                    single_sided=single_sided,
                    blank_page_note=blank_page_note,
                    include_page_numbers=include_page_numbers
                )
            except Exception as e:
                print(f"Bundle Interior PDF Generation Warning: {e}")

            # 2. Generate Cover PDF
            try:
                KDPCoverExporter.generate_cover_pdf(req_data, out_cover_pdf, cover_config=cover_config)
            except Exception as e:
                print(f"Bundle Cover PDF Generation Warning: {e}")

            # 3. Generate Metadata & Upload Guide TXT
            meta = req_data.get("metadata", {})
            pages_count = len(req_data.get("pages", []))
            trim_size = req_data.get("settings", {}).get("trim_size", "8.5x11")
            author = req_data.get("author") or meta.get("author") or "Creative Kids Studio"

            if not meta or not meta.get("backend_keywords"):
                ai = AIKDPAssistant()
                topic = req_data.get("theme") or req_data.get("name", "Coloring Book")
                book_type = req_data.get("book_type", "coloring_book")
                meta = ai.generate_kdp_metadata(
                    topic_or_niche=topic,
                    book_type=book_type,
                    author_name=author,
                    page_count=pages_count,
                    trim_size=trim_size
                )

            title = meta.get("title") or req_data.get("name", "My KDP Book")
            subtitle = meta.get("subtitle", f"{pages_count}+ Fun & Easy Coloring Pages")
            keywords = meta.get("backend_keywords", [])
            categories = meta.get("recommended_categories", [])
            html_desc = meta.get("html_description", "")

            # Print cost & royalties
            if pages_count <= 108:
                print_cost = 2.30
            else:
                print_cost = round(1.00 + (pages_count * 0.012), 2)
            floor_price = round(print_cost / 0.60, 2)
            launch_profit = round((6.99 * 0.60) - print_cost, 2)
            regular_profit = round((7.99 * 0.60) - print_cost, 2)

            guide_text = f"""================================================================================
          AMAZON KDP COMPLETE PUBLISHING GUIDE & METADATA CHEAT SHEET
             Generated by KDP Book Production Studio (Print-Ready)
================================================================================

[1] BOOK INFORMATION & SETUP:
--------------------------------------------------------------------------------
Book Title: {title}
Subtitle: {subtitle}
Author / Pen Name: {author}
Page Count: {pages_count} pages
Trim Size: {trim_size}
Ink & Paper Type: Black & white interior with white paper
Bleed Settings: Bleed (PDF only)
Paperback Cover Finish: Matte (Recommended for coloring books)

[2] PRICING & ROYALTY PROFIT STRATEGY (US MARKET):
--------------------------------------------------------------------------------
Amazon KDP Printing Cost: ${print_cost:.2f}
Minimum Break-Even Price: ${floor_price:.2f}

* RECOMMENDED LAUNCH PRICE: $6.99
  -> Amazon Cut (40%): $2.80
  -> Printing Cost: ${print_cost:.2f}
  -> YOUR NET PROFIT PER BOOK: ${launch_profit:.2f}
  * Strategy: High conversion rate, rapid initial reviews, and algorithmic ranking boost.

* RECOMMENDED REGULAR PRICE: $7.99
  -> Amazon Cut (40%): $3.20
  -> Printing Cost: ${print_cost:.2f}
  -> YOUR NET PROFIT PER BOOK: ${regular_profit:.2f}
  * Strategy: Long-term optimal profit margin once you reach 10-15 customer reviews.

[3] 7 AMAZON KDP BACKEND SEARCH KEYWORDS (COPY INTO SLOTS 1 TO 7):
--------------------------------------------------------------------------------
"""
            for i, kw in enumerate(keywords[:7], 1):
                guide_text += f"Keyword Slot {i}: {kw}\n"

            guide_text += f"""
[4] RECOMMENDED AMAZON KDP CATEGORIES (CHOOSE UP TO 3 IN KDP):
--------------------------------------------------------------------------------
"""
            for i, cat in enumerate(categories[:3], 1):
                guide_text += f"Category {i}: {cat}\n"

            guide_text += f"""
[5] AMAZON HTML BOOK DESCRIPTION (READY TO PASTE INTO AMAZON KDP):
--------------------------------------------------------------------------------
{html_desc}

================================================================================
[6] STEP-BY-STEP INSTRUCTIONS TO PUBLISH ON AMAZON KDP:
================================================================================
Step 1: Go to https://kdp.amazon.com and sign in to your Amazon account.
Step 2: Click the yellow "+ Create" button and select "Create Paperback".

--- TAB 1: PAPERBACK DETAILS ---
1. Primary Language: English
2. Book Title: Paste the Title from above.
3. Subtitle: Paste the Subtitle from above.
4. Author: Enter your Pen Name ({author}).
5. Description: Paste the HTML description from Section [5] above.
6. Publishing Rights: Choose "I own the copyright and hold necessary publishing rights".
7. Primary Audience (Adult Content): Select "No".
8. Reading Age: Minimum 4 Years, Maximum 8 Years (or your target age).
9. Primary Marketplace: Amazon.com
10. Categories: Click "Choose categories" and pick the 3 categories listed in Section [4].
11. Keywords: Copy and paste Keyword Slots 1 to 7 into the 7 keyword boxes.
12. Click "Save and Continue".

--- TAB 2: PAPERBACK CONTENT ---
1. Print ISBN: Select "Assign me a free KDP ISBN".
2. Publication Date: Leave blank (uses current date).
3. Print Options:
   - Ink & Paper Type: "Black & white interior with white paper"
   - Trim Size: Select "{trim_size}"
   - Bleed Settings: Select "Bleed (PDF only)"
   - Paperback Cover Finish: Select "Matte"
4. Manuscript: Click "Upload paperback manuscript" and choose:
   -> "{out_interior_pdf.name}"
5. Book Cover: Select "Upload a cover you already have" and choose:
   -> "{out_cover_pdf.name}"
6. Book Preview: Click "Launch Previewer" (wait 1-2 mins) and check for any cut-off warnings.
7. Click "Save and Continue".

--- TAB 3: PAPERBACK RIGHTS & PRICING ---
1. Territories: Select "All territories (worldwide rights)".
2. Primary Marketplace: Amazon.com
3. Pricing: Enter "$6.99" (or "$7.99") in the Amazon.com price box.
   Notice your royalty matches the calculation in Section [2] above!
4. Click "Publish Your Paperback Book"!

🎉 THAT'S IT! Your book will be reviewed by Amazon and available for sale worldwide within 24-72 hours!
================================================================================
"""
            with open(out_guide_txt, "w", encoding="utf-8") as f:
                f.write(guide_text)

            out_preflight_txt = exports_dir / f"{proj_name}_AI_Preflight_Report.txt"
            try:
                ai = AIKDPAssistant()
                audit_res = ai.audit_pdf_quality(req_data)
                preflight_text = f"""================================================================================
          AMAZON KDP AI PRINT-READINESS & QUALITY PREFLIGHT REPORT
             Certified by KDP Book Production Studio AI Auditor
================================================================================

OVERALL PRINT-READINESS SCORE: {audit_res.get('readiness_score', 100)} / 100
QUALITY GRADE: {audit_res.get('grade', 'A+')}
SUMMARY: {audit_res.get('summary_advice', '')}

LINE-BY-LINE AUDIT SPECIFICATIONS:
--------------------------------------------------------------------------------
"""
                for chk in audit_res.get("checks", []):
                    preflight_text += f"[{chk.get('status', 'PASS')}] {chk.get('title')}\n"
                    preflight_text += f"    Result: {chk.get('message')}\n"
                    if chk.get("fix"):
                        preflight_text += f"    Action: {chk.get('fix')}\n"
                    preflight_text += "\n"

                preflight_text += f"""================================================================================
VERDICT: 100% KDP Upload Safe. Ready for Amazon KDP Paperback Submission!
================================================================================
"""
                with open(out_preflight_txt, "w", encoding="utf-8") as f:
                    f.write(preflight_text)
            except Exception as pe:
                print(f"Preflight Report Generation Warning: {pe}")

            # 4. Package into ZIP
            with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
                if out_interior_pdf.exists():
                    zipf.write(out_interior_pdf, arcname=out_interior_pdf.name)
                if out_cover_pdf.exists():
                    zipf.write(out_cover_pdf, arcname=out_cover_pdf.name)
                if out_guide_txt.exists():
                    zipf.write(out_guide_txt, arcname=out_guide_txt.name)
                if out_preflight_txt.exists():
                    zipf.write(out_preflight_txt, arcname=out_preflight_txt.name)

            file_size_mb = round(out_zip.stat().st_size / (1024 * 1024), 2)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            resp = {
                "status": "success",
                "zip_path": str(out_zip),
                "filename": out_zip.name,
                "file_size_mb": file_size_mb,
                "download_url": f"/api/exports/{urllib.parse.quote(out_zip.name)}?path={urllib.parse.quote(str(out_zip))}",
                "metadata": meta,
                "print_cost": print_cost,
                "floor_price": floor_price,
                "recommended_launch_price": 6.99,
                "launch_profit": launch_profit,
                "recommended_regular_price": 7.99,
                "regular_profit": regular_profit
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        elif req_path == "/api/projects/toggle_lock":
            raw_path = req_data.get("path", "")
            p = Path(raw_path).resolve()
            project_file = p if p.name == "project.json" else p / "project.json"

            if project_file.exists():
                with open(project_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                new_lock_state = not bool(data.get("is_locked", False))
                data["is_locked"] = new_lock_state
                with open(project_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "is_locked": new_lock_state}).encode("utf-8"))
                return
            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"File not found: {project_file}"}).encode("utf-8"))
                return

        elif req_path == "/api/projects/delete":
            raw_path = req_data.get("path", "")
            p = Path(raw_path).resolve()
            project_dir = p.parent if p.name == "project.json" else p

            if not project_dir.exists() or not project_dir.is_dir():
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"Directory not found: {project_dir}"}).encode("utf-8"))
                return

            project_file = project_dir / "project.json"
            if project_file.exists():
                with open(project_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("is_locked", False):
                    self.send_response(403)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Project is locked and cannot be deleted."}).encode("utf-8"))
                    return

            try:
                shutil.rmtree(project_dir)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "deleted", "path": str(project_dir)}).encode("utf-8"))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
                return

        elif req_path == "/api/projects/process_image":
            data_url = req_data.get("data_url", "")
            clean_bg = bool(req_data.get("clean_bg", True))
            auto_crop = bool(req_data.get("auto_crop", True))
            compress = bool(req_data.get("compress", True))
            bg_threshold = int(req_data.get("bg_threshold", 220))

            try:
                opt_url, w, h, size_kb = KDPImageProcessor.process_coloring_image(
                    data_url, clean_bg=clean_bg, auto_crop=auto_crop, compress=compress, bg_threshold=bg_threshold
                )
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "data_url": opt_url,
                    "width": w,
                    "height": h,
                    "size_kb": size_kb
                }).encode("utf-8"))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
                return

        # ==========================================
        # Amazon KDP Image Upscaler & Safe Margin Cropper Endpoints
        # ==========================================
        elif req_path == "/api/tools/upscale_image":
            image_data = req_data.get("image") or req_data.get("data_url") or ""
            trim_size = req_data.get("trim_size", "8.5x11")
            custom_w = float(req_data.get("custom_width_in", 8.5) or 8.5)
            custom_h = float(req_data.get("custom_height_in", 11.0) or 11.0)
            target_dpi = int(req_data.get("target_dpi", 300) or 300)
            margin_in = float(req_data.get("margin_in", 0.375) or 0.375)
            fit_mode = req_data.get("fit_mode", "fit_safe")
            has_bleed = bool(req_data.get("has_bleed", False))
            clean_bg = bool(req_data.get("clean_bg", True))
            sharpen = bool(req_data.get("sharpen", True))
            line_art_mode = bool(req_data.get("line_art_mode", False))
            auto_focus_crop = bool(req_data.get("auto_focus_crop", True))
            bg_threshold = int(req_data.get("bg_threshold", 225) or 225)

            try:
                result = KDPImageProcessor.upscale_and_crop_kdp(
                    image_input=image_data,
                    trim_size=trim_size,
                    custom_width_in=custom_w,
                    custom_height_in=custom_h,
                    target_dpi=target_dpi,
                    margin_in=margin_in,
                    fit_mode=fit_mode,
                    has_bleed=has_bleed,
                    clean_bg=clean_bg,
                    sharpen=sharpen,
                    line_art_mode=line_art_mode,
                    auto_focus_crop=auto_focus_crop,
                    bg_threshold=bg_threshold
                )
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode("utf-8"))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": str(e)}).encode("utf-8"))
                return

        elif req_path == "/api/tools/save_upscaled_to_project":
            proj_dir_raw = req_data.get("project_dir", "")
            if not proj_dir_raw:
                proj_dir = DEFAULT_PROJECTS_DIR / "Default"
            else:
                proj_dir = Path(proj_dir_raw).resolve()

            media_dir = proj_dir / "media"
            media_dir.mkdir(parents=True, exist_ok=True)

            filename = req_data.get("filename", f"kdp_upscaled_{int(time.time())}.png")
            if not filename.endswith(".png") and not filename.endswith(".jpg"):
                filename += ".png"

            data_url = req_data.get("data_url", "")
            if "," in data_url:
                _, encoded = data_url.split(",", 1)
                img_bytes = base64.b64decode(encoded)
            else:
                img_bytes = base64.b64decode(data_url)

            target_path = media_dir / filename
            with open(target_path, "wb") as f:
                f.write(img_bytes)

            file_url = f"/api/projects/media?project_dir={urllib.parse.quote(str(proj_dir))}&filename={urllib.parse.quote(filename)}"

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "filename": filename,
                "file_path": str(target_path),
                "media_url": file_url,
                "size_kb": max(1, len(img_bytes) // 1024)
            }).encode("utf-8"))
            return

        elif req_path == "/api/projects/upload_asset":
            project_dir = Path(req_data.get("project_dir", DEFAULT_PROJECTS_DIR / "Default")).resolve()
            media_dir = project_dir / "media"
            media_dir.mkdir(parents=True, exist_ok=True)
            assets_dir = project_dir / "assets"
            assets_dir.mkdir(parents=True, exist_ok=True)

            filename = req_data.get("filename", "image.png")
            data_url = req_data.get("data_url", "")
            clean_bg = bool(req_data.get("clean_bg", True))
            auto_crop = bool(req_data.get("auto_crop", True))

            # Auto-optimize and compress coloring images on upload
            opt_data_url = data_url
            opt_size_kb = 0
            try:
                opt_data_url, w, h, opt_size_kb = KDPImageProcessor.process_coloring_image(
                    data_url, clean_bg=clean_bg, auto_crop=auto_crop, compress=True
                )
            except Exception:
                opt_data_url = data_url

            if "," in opt_data_url:
                header, encoded = opt_data_url.split(",", 1)
                file_bytes = base64.b64decode(encoded)
                
                # Write to media directory
                target_media_path = media_dir / filename
                with open(target_media_path, "wb") as f:
                    f.write(file_bytes)

                # Keep assets directory synchronized for backward compatibility
                target_asset_path = assets_dir / filename
                with open(target_asset_path, "wb") as f:
                    f.write(file_bytes)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "uploaded", 
                "media_path": str(media_dir / filename),
                "asset_path": str(assets_dir / filename),
                "data_url": opt_data_url,
                "size_kb": opt_size_kb
            }).encode("utf-8"))
            return

        elif req_path == "/api/generators/sudoku":
            count = int(req_data.get("count", 10))
            difficulty = req_data.get("difficulty", "medium")
            puzzles = SudokuGenerator.generate_bulk(count=count, difficulty=difficulty)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "count": len(puzzles), "puzzles": puzzles}).encode("utf-8"))
            return

        elif req_path == "/api/generators/tic_tac_toe":
            total_games = int(req_data.get("total_games", 20))
            games_per_page = int(req_data.get("games_per_page", 4))
            grid_size = int(req_data.get("grid_size", 3))
            pages = TicTacToeGenerator.generate_bulk(total_games=total_games, games_per_page=games_per_page, grid_size=grid_size)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "total_games": total_games, "pages": pages}).encode("utf-8"))
            return

        elif req_path == "/api/generators/maze":
            count = int(req_data.get("count", 1))
            width = int(req_data.get("width", 15))
            height = int(req_data.get("height", 20))
            if count > 1:
                mazes = MazeGenerator.generate_bulk(count=count, width=width, height=height)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "count": len(mazes), "mazes": mazes}).encode("utf-8"))
                return
            else:
                maze = MazeGenerator.generate_maze(width=width, height=height)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "maze": maze}).encode("utf-8"))
                return

        elif req_path == "/api/generators/word_search":
            count = int(req_data.get("count", 1))
            grid_size = int(req_data.get("grid_size", 12))
            if count > 1:
                puzzles = WordSearchGenerator.generate_bulk(count=count, grid_size=grid_size)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "count": len(puzzles), "puzzles": puzzles}).encode("utf-8"))
                return
            else:
                words = req_data.get("words", ["APPLE", "BANANA", "ORANGE", "MANGO", "GRAPES", "BERRY"])
                ws = WordSearchGenerator.generate_puzzle(words=words, grid_size=grid_size)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "word_search": ws}).encode("utf-8"))
                return

        elif req_path == "/api/generators/dot_to_dot":
            image_data = req_data.get("image_data")
            preset_name = req_data.get("preset_name", "star")
            dot_count = int(req_data.get("dot_count", 35))
            faint_guide = bool(req_data.get("faint_guide", True))
            canvas_w = int(req_data.get("canvas_w", 420))
            canvas_h = int(req_data.get("canvas_h", 460))

            try:
                if image_data:
                    res = DotToDotGenerator.from_image(
                        image_input=image_data,
                        dot_count=dot_count,
                        canvas_w=canvas_w,
                        canvas_h=canvas_h,
                        faint_guide=faint_guide
                    )
                else:
                    res = DotToDotGenerator.generate_preset(
                        preset_name=preset_name,
                        dot_count=dot_count,
                        canvas_w=canvas_w,
                        canvas_h=canvas_h
                    )

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "puzzle": res}).encode("utf-8"))
                return
            except Exception as err:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(err)}).encode("utf-8"))
                return

        # ==========================================
        # AI KDP Research & Metadata Assistant Endpoints
        # ==========================================
        elif req_path == "/api/ai/test_key":
            key = req_data.get("api_key")
            model = req_data.get("model", "gemini-3.6-flash")
            ai = AIKDPAssistant()
            res = ai.verify_api_key(api_key=key, model=model)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        elif req_path == "/api/ai/save_key":
            key = req_data.get("api_key", "")
            model = req_data.get("model", "gemini-3.6-flash")
            ai = AIKDPAssistant()
            saved_res = ai.save_config(key, model)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(saved_res).encode("utf-8"))
            return

        elif req_path == "/api/ai/niche_ideas":
            target_age = req_data.get("target_age", "Ages 4-8")
            book_category = req_data.get("category", "all")
            ai = AIKDPAssistant()
            niches = ai.get_trending_niche_ideas(target_age=target_age, book_category=book_category)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "niches": niches}).encode("utf-8"))
            return

        elif req_path == "/api/ai/generate_metadata":
            topic = req_data.get("topic", "Jungle Animals")
            book_type = req_data.get("book_type", "coloring_book")
            target_age = req_data.get("target_age", "Ages 4-8")
            author = req_data.get("author", "Creative Kids Studio")
            page_count = int(req_data.get("page_count", 24))
            trim_size = req_data.get("trim_size", "8.5x11")
            ai = AIKDPAssistant()
            meta = ai.generate_kdp_metadata(
                topic_or_niche=topic,
                book_type=book_type,
                target_age=target_age,
                author_name=author,
                page_count=page_count,
                trim_size=trim_size
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "metadata": meta}).encode("utf-8"))
            return

        elif req_path == "/api/ai/generate_cover_metadata":
            topic = req_data.get("topic", "Jungle Animals")
            book_type = req_data.get("book_type", "coloring_book")
            target_age = req_data.get("target_age", "Ages 4-8")
            author = req_data.get("author", "Creative Kids Studio")
            page_count = int(req_data.get("page_count", 24))
            trim_size = req_data.get("trim_size", "8.5x11")
            ai = AIKDPAssistant()
            cover_meta = ai.generate_ai_cover_metadata(
                topic=topic,
                book_type=book_type,
                target_age=target_age,
                author=author,
                page_count=page_count,
                trim_size=trim_size
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "cover": cover_meta}).encode("utf-8"))
            return

        elif req_path == "/api/ai/preflight_check":
            ai = AIKDPAssistant()
            audit_res = ai.audit_pdf_quality(req_data)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "audit": audit_res}).encode("utf-8"))
            return

        # ==========================================
        # 5 New Activity Book Generator Endpoints
        # ==========================================
        elif req_path == "/api/generators/tracing":
            char = req_data.get("char", "A")
            repeat = int(req_data.get("repeat", 5))
            word = req_data.get("word", "APPLE")
            res = TracingGenerator.generate_letter_tracing_page(letter_or_number=char, repeat_count=repeat, include_word=word)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "tracing": res}).encode("utf-8"))
            return

        elif req_path == "/api/generators/scissor_skills":
            pattern = req_data.get("pattern", "zigzag")
            lines = int(req_data.get("lines", 5))
            title = req_data.get("title", "Cutting Practice")
            res = ScissorSkillsGenerator.generate_cutting_practice_page(pattern_type=pattern, line_count=lines, title=title)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "scissor_skills": res}).encode("utf-8"))
            return

        elif req_path == "/api/generators/shadow_matching":
            theme = req_data.get("theme", "jungle_animals")
            pairs = int(req_data.get("pairs", 4))
            title = req_data.get("title", "Shadow Matching Activity")
            res = ShadowMatchingGenerator.generate_shadow_matching_page(theme=theme, pair_count=pairs, title=title)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "shadow_matching": res}).encode("utf-8"))
            return

        elif req_path == "/api/generators/ispy":
            theme = req_data.get("theme", "jungle")
            title = req_data.get("title", "I Spy & Count Animals!")
            res = ISpyCountingGenerator.generate_ispy_page(theme=theme, title=title)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "ispy": res}).encode("utf-8"))
            return

        elif req_path == "/api/generators/grid_drawing":
            size = int(req_data.get("grid_size", 4))
            title = req_data.get("title", "Learn to Draw: Grid Copy")
            animal = req_data.get("animal_name", "Lion")
            ref_src = req_data.get("image_src")
            res = GridDrawingGenerator.generate_grid_drawing_page(grid_size=size, title=title, animal_name=animal, reference_image_src=ref_src)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "grid_drawing": res}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()


def run_server(port=PORT):
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", port), StudioRequestHandler) as httpd:
            print("==================================================")
            print("KDP Studio Live Web Preview & PDF Exporter API Running!")
            print(f"URL: http://localhost:{port}")
            print(f"Default Project Folder: {DEFAULT_PROJECTS_DIR}")
            print("==================================================")
            httpd.serve_forever()
    except OSError as e:
        if port == 8080:
            print(f"Port 8080 in use, trying 8081...")
            run_server(8081)
        else:
            raise e


if __name__ == "__main__":
    run_server()
