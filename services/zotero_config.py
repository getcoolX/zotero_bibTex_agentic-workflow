import json
import shutil
from pathlib import Path


class ZoteroConfigManager:
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
        self.local_config_path.write_text("{}", encoding="utf-8")

    def get_config(self):
        self._ensure_local_file()
        data = json.loads(self.local_config_path.read_text(encoding="utf-8"))
        return {
            "user_id": str(data.get("user_id", "")).strip(),
            "api_key": str(data.get("api_key", "")).strip(),
            "library_type": str(data.get("library_type", "user")).strip() or "user",
            "collection_key": str(data.get("collection_key", "")).strip(),
        }

    def update_config(self, config):
        cleaned = {
            "user_id": str(config.get("user_id", "")).strip(),
            "api_key": str(config.get("api_key", "")).strip(),
            "library_type": str(config.get("library_type", "user")).strip() or "user",
            "collection_key": str(config.get("collection_key", "")).strip(),
        }
        self.local_config_path.write_text(json.dumps(cleaned, ensure_ascii=False, indent=2), encoding="utf-8")
        return cleaned
