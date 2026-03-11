import json
from pathlib import Path


class LLMConfigManager:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.config_path.exists():
            self.config_path.write_text("[]", encoding="utf-8")

    def list_providers(self):
        return json.loads(self.config_path.read_text(encoding="utf-8"))

    def update_providers(self, providers):
        cleaned = []
        for p in providers:
            cleaned.append(
                {
                    "name": p.get("name", "").strip(),
                    "base_url": p.get("base_url", "").strip(),
                    "model": p.get("model", "").strip(),
                    "api_key": p.get("api_key", "").strip(),
                    "enabled": bool(p.get("enabled", False)),
                }
            )
        self.config_path.write_text(json.dumps(cleaned, ensure_ascii=False, indent=2), encoding="utf-8")
        return cleaned
