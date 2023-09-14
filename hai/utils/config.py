import json
from typing import Any, Dict

DEFAULT_CONFIG_PATH = "./hai_config.json"


class Config:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
            # Here, we particularly store the arguments and kwargs of the first call
            cls._file_path_args = args
            cls._file_path_kwargs = kwargs
        return cls._instance

    def __init__(self, file_path: str = ""):
        # Only initialize if we haven't before
        if hasattr(self, "initialized") and self.initialized:
            return
        self.file_path = DEFAULT_CONFIG_PATH if not file_path else file_path
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

    def available_models(self) -> list[str]:
        """
        Get available AI models
        """
        return self.get("available_models", default=[])
