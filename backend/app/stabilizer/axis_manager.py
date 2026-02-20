import yaml
from pathlib import Path
from typing import Dict, Any

_DEFAULT_CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "ci_axis.yaml"


class AxisManager:
    def __init__(self, config_path=None):
        self.config_path = Path(config_path) if config_path else _DEFAULT_CONFIG_PATH
        self.active_profile = "default"
        self._config: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Axis config not found: {self.config_path}")
        with open(self.config_path, 'r') as f:
            self._config = yaml.safe_load(f) or {}

    def get_active(self) -> Dict[str, Any]:
        profiles = self._config.get("profiles", {})
        return profiles.get(self.active_profile, profiles.get("default", {}))

    def activate(self, profile: str) -> bool:
        if profile in self._config.get("profiles", {}):
            self.active_profile = profile
            return True
        return False

    def get_limits(self, mode: str) -> Dict[str, int]:
        active = self.get_active()
        modes = active.get("modes", {})
        return modes.get(mode, modes.get("normal", {}))
