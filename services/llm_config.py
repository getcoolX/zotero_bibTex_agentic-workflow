import json
import shutil
from pathlib import Path


class LLMConfigManager:
    def __init__(self, local_config_path: Path, example_config_path: Path):
        self.local_config_path = local_config_path
        self.example_config_path = example_config_path
        self.local_config_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_local_file()

    def _ensure_local_file(self):
        if self.local_config_path.exists():
            return
        if self.example_config_path.exists():
            shutil.copyfile(self.example_config_path, self.local_config_path)
            return
        self.local_config_path.write_text("[]", encoding="utf-8")

    def list_providers(self):
        self._ensure_local_file()
        return json.loads(self.local_config_path.read_text(encoding="utf-8"))

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
        self.local_config_path.write_text(json.dumps(cleaned, ensure_ascii=False, indent=2), encoding="utf-8")
        return cleaned
