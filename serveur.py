"""Serveur local de la maquette C (dist/ sur le port 8785), avec les bons types de fichiers et sans cache."""
import functools
import http.server
from pathlib import Path

TYPES = {".webp": "image/webp", ".glb": "model/gltf-binary", ".js": "text/javascript", ".woff2": "font/woff2", ".vtt": "text/vtt"}


class SansCache(http.server.SimpleHTTPRequestHandler):
    """Maquette en cours de travail : le navigateur redemande toujours la dernière version."""
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, **TYPES}

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *args):
        pass


Gestion = functools.partial(SansCache, directory=str(Path(__file__).parent / "dist"))
http.server.ThreadingHTTPServer(("127.0.0.1", 8785), Gestion).serve_forever()
