import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

PORT = 8080
DIRECTORY = Path(__file__).resolve().parent

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def do_GET(self):
        # Redirect root to mobile simulator by default if requested
        if self.path == "/" or self.path == "":
            self.path = "/mobile_simulator.html"
        return super().do_GET()

def main():
    os.chdir(DIRECTORY)
    url = f"http://localhost:{PORT}/mobile_simulator.html"
    print("=" * 60)
    print("  🚀 PHILIP FACE AI - MOBILE SERVER IS LIVE!")
    print(f"  👉 MOBILE APP URL: {url}")
    print(f"  👉 DESKTOP WEB APP: http://localhost:{PORT}/index.html")
    print(f"  👉 ANDROID APK:     http://localhost:{PORT}/Philip_Face_AI.apk")
    print("=" * 60)

    # Open browser directly to mobile simulator
    webbrowser.open(url)

    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    main()
