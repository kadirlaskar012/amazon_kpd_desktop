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
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.storage.project_storage import ProjectStorage
from app.core.pdf_exporter import KDPPdfExporter
from app.core.cover_exporter import KDPCoverExporter
from app.generators.sudoku_generator import SudokuGenerator
from app.generators.tic_tac_toe_generator import TicTacToeGenerator
from app.generators.maze_generator import MazeGenerator
from app.generators.word_search_generator import WordSearchGenerator

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

        elif req_path == "/api/projects":
            # List all valid project directories in DEFAULT_PROJECTS_DIR
            projects = []
            if DEFAULT_PROJECTS_DIR.exists():
                for item in DEFAULT_PROJECTS_DIR.iterdir():
                    if item.is_dir() and (item / "project.json").exists():
                        try:
                            with open(item / "project.json", "r", encoding="utf-8") as f:
                                data = json.load(f)
                            projects.append({
                                "name": data.get("name", item.name),
                                "folder_name": item.name,
                                "path": str(item),
                                "is_locked": bool(data.get("is_locked", False)),
                                "page_count": len(data.get("pages", [])),
                                "media_count": len(data.get("media", [])),
                                "created_at": data.get("created_at", ""),
                                "updated_at": data.get("updated_at", "")
                            })
                        except Exception:
                            pass
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"projects": projects}).encode("utf-8"))
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

        elif req_path.startswith("/api/exports/") or req_path == "/api/exports":
            query_params = urllib.parse.parse_qs(parsed.query)
            raw_file = query_params.get("path", [""])[0]
            if raw_file and Path(raw_file).exists():
                pdf_file = Path(raw_file)
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Disposition", f"inline; filename=\"{pdf_file.name}\"")
                self.send_header("Content-Length", str(pdf_file.stat().st_size))
                self.end_headers()
                with open(pdf_file, "rb") as f:
                    shutil.copyfileobj(f, self.wfile)
                return
            else:
                self.send_response(404)
                self.end_headers()
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

        if req_path == "/api/projects/create":
            proj_name = req_data.get("name", "Untitled Project").strip()
            folder_name = req_data.get("folder_name") or proj_name.replace(" ", "_")
            root_dir = Path(req_data.get("root_path") or DEFAULT_PROJECTS_DIR)
            project_dir = (root_dir / folder_name).resolve()

            ProjectStorage.initialize_project_directory(project_dir)

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

            proj_name = req_data.get("name", "KDP_Book").replace(" ", "_")
            out_pdf = exports_dir / f"{proj_name}_KDP_Print_Ready.pdf"

            single_sided = req_data.get("single_sided", True)
            blank_page_note = req_data.get("blank_page_note", False)
            include_front_matter = req_data.get("include_front_matter", True)

            try:
                KDPPdfExporter.generate_pdf(
                    req_data, 
                    out_pdf, 
                    include_front_matter=include_front_matter, 
                    single_sided=single_sided, 
                    blank_page_note=blank_page_note
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

            proj_name = req_data.get("name", "KDP_Book").replace(" ", "_")
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

        elif req_path == "/api/projects/upload_asset":
            project_dir = Path(req_data.get("project_dir", DEFAULT_PROJECTS_DIR / "Default")).resolve()
            assets_dir = project_dir / "assets"
            assets_dir.mkdir(parents=True, exist_ok=True)

            filename = req_data.get("filename", "image.png")
            data_url = req_data.get("data_url", "")

            if "," in data_url:
                header, encoded = data_url.split(",", 1)
                file_bytes = base64.b64decode(encoded)
                target_path = assets_dir / filename
                with open(target_path, "wb") as f:
                    f.write(file_bytes)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "uploaded", "asset_path": str(assets_dir / filename)}).encode("utf-8"))
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
