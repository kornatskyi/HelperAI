import json
from typing import Any, Dict


class Config:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.config_data: Dict[str, Any] = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_config(self):
        with open(self.file_path, "w") as f:
            json.dump(self.config_data, f, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        return self.config_data.get(key, default)

    def set(self, key: str, value: Any):
        self.config_data[key] = value
        self.save_config()
