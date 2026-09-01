"""
KDP Book Production Studio - Web Preview Server with Project & File System API.
Serves the interactive web preview studio on http://localhost:8080 and handles local project persistence.
"""

import http.server
import socketserver
import os
import sys
import json
import base64
import urllib.parse
from pathlib import Path

# Add project root to sys.path so we can use app.storage.project_storage
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.storage.project_storage import ProjectStorage

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
        
        if parsed.path == "/api/default_location":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            resp = {
                "default_root": str(DEFAULT_PROJECTS_DIR),
                "home": str(Path.home())
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        elif parsed.path == "/api/projects":
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
                                "path": str(item),
                                "page_count": len(data.get("pages", [])),
                                "media_count": len(data.get("media", [])),
                                "created_at": data.get("created_at", "")
                            })
                        except Exception:
                            pass
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"projects": projects}).encode("utf-8"))
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len)

        try:
            req_data = json.loads(post_body.decode("utf-8")) if post_body else {}
        except Exception:
            req_data = {}

        if parsed.path == "/api/projects/create":
            # Create physical project folder & subdirectories
            proj_name = req_data.get("name", "Untitled Project").strip()
            folder_name = req_data.get("folder_name") or proj_name.replace(" ", "_")
            root_dir = Path(req_data.get("root_path") or DEFAULT_PROJECTS_DIR)
            project_dir = root_dir / folder_name

            ProjectStorage.initialize_project_directory(project_dir)

            # Save initial project.json
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

        elif parsed.path == "/api/projects/save":
            # Save project state to disk
            project_dir = Path(req_data.get("project_dir", DEFAULT_PROJECTS_DIR / "My_Project"))
            project_dir.mkdir(parents=True, exist_ok=True)
            project_file = project_dir / "project.json"

            with open(project_file, "w", encoding="utf-8") as f:
                json.dump(req_data, f, indent=2, ensure_ascii=False)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "saved", "path": str(project_file)}).encode("utf-8"))
            return

        elif parsed.path == "/api/projects/upload_asset":
            # Save binary/base64 asset into project's assets/ folder
            project_dir = Path(req_data.get("project_dir", DEFAULT_PROJECTS_DIR / "Default"))
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

        self.send_response(404)
        self.end_headers()


def run_server(port=PORT):
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", port), StudioRequestHandler) as httpd:
            print("==================================================")
            print("KDP Studio Live Web Preview & File API Running!")
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
