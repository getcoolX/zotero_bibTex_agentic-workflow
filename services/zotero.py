import json
from urllib import request


class ZoteroClient:
    def __init__(self, user_id, api_key, library_type="user", collection_key=""):
        self.user_id = user_id
        self.api_key = api_key
        self.library_type = library_type
        self.collection_key = collection_key

    def _to_zotero_item(self, paper):
        return {
            "itemType": "journalArticle",
            "title": paper.get("title", "Untitled"),
            "creators": [
                {"creatorType": "author", "name": author}
                for author in paper.get("authors", [])
            ],
            "date": paper.get("year", ""),
            "DOI": paper.get("doi", ""),
            "url": paper.get("url", ""),
            "collections": [self.collection_key] if self.collection_key else [],
        }

    def import_papers(self, papers):
        if not self.user_id or not self.api_key:
            return {"ok": False, "message": "缺少 Zotero user_id/api_key", "imported": 0}

        endpoint = f"https://api.zotero.org/{self.library_type}s/{self.user_id}/items"
        payload = json.dumps([self._to_zotero_item(p) for p in papers]).encode("utf-8")
        req = request.Request(endpoint, data=payload, method="POST")
        req.add_header("Zotero-API-Key", self.api_key)
        req.add_header("Content-Type", "application/json")
        req.add_header("Zotero-Write-Token", "agentic-workflow")
        try:
            with request.urlopen(req, timeout=20) as resp:
                return {"ok": True, "status": resp.status, "imported": len(papers)}
        except Exception as exc:
            return {"ok": False, "message": str(exc), "imported": 0}
