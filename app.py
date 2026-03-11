import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from services.bibtex import export_acm_bibtex
from services.llm_config import LLMConfigManager
from services.paper_parser import extract_papers
from services.zotero import ZoteroClient
from storage import PaperStore

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


class AppHandler(BaseHTTPRequestHandler):
    store = PaperStore(BASE_DIR / "data.sqlite3")
    llm_manager = LLMConfigManager(BASE_DIR / "config" / "default_llms.json")

    def _json_response(self, payload, status=HTTPStatus.OK):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8") or "{}")

    def _serve_static(self, file_name="index.html"):
        path = STATIC_DIR / file_name
        if not path.exists() or not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return
        mime = "text/plain"
        if path.suffix == ".html":
            mime = "text/html; charset=utf-8"
        elif path.suffix == ".js":
            mime = "application/javascript; charset=utf-8"
        elif path.suffix == ".css":
            mime = "text/css; charset=utf-8"
        content = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            return self._serve_static("index.html")
        if parsed.path.startswith("/static/"):
            return self._serve_static(parsed.path.replace("/static/", "", 1))
        if parsed.path == "/api/papers":
            return self._json_response({"papers": self.store.list_papers()})
        if parsed.path == "/api/llm-config":
            return self._json_response({"providers": self.llm_manager.list_providers()})
        if parsed.path == "/api/export-bibtex":
            query = parse_qs(parsed.query)
            ids = [int(x) for x in query.get("ids", [""])[0].split(",") if x.strip().isdigit()]
            papers = self.store.get_papers(ids)
            bibtex = export_acm_bibtex(papers)
            return self._json_response({"bibtex": bibtex})
        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self):
        parsed = urlparse(self.path)
        payload = self._read_json()
        if parsed.path == "/api/import-papers":
            extracted = extract_papers(payload.get("input", ""))
            imported = self.store.save_papers(extracted)
            return self._json_response({"imported": imported, "count": len(imported)})
        if parsed.path == "/api/llm-config":
            updated = self.llm_manager.update_providers(payload.get("providers", []))
            return self._json_response({"providers": updated})
        if parsed.path == "/api/import-to-zotero":
            zotero = payload.get("zotero", {})
            ids = payload.get("paper_ids", [])
            papers = self.store.get_papers(ids)
            client = ZoteroClient(
                user_id=zotero.get("user_id", ""),
                api_key=zotero.get("api_key", ""),
                library_type=zotero.get("library_type", "user"),
                collection_key=zotero.get("collection_key", ""),
            )
            result = client.import_papers(papers)
            return self._json_response(result)
        self.send_error(HTTPStatus.NOT_FOUND, "Not found")


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8080), AppHandler)
    print("Server running at http://0.0.0.0:8080")
    server.serve_forever()
