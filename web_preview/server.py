"""
KDP Book Production Studio - Web Preview Server.
Serves the interactive web preview studio on http://localhost:8080.
"""

import http.server
import socketserver
import os
import sys
import json
from pathlib import Path

# Ensure UTF-8 output encoding for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PORT = 8080
web_dir = Path(__file__).resolve().parent


class StudioRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(web_dir), **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()


def run_server(port=PORT):
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", port), StudioRequestHandler) as httpd:
            print("==================================================")
            print(f"KDP Studio Live Web Preview Server Running!")
            print(f"URL: http://localhost:{port}")
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
