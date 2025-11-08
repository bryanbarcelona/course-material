"""Doctopus configuration loader."""

from typing import Any, Dict, Optional
from ..utils.config_loader import ConfigLoader as _ConfigLoader

def _load_doctopus_config(
    config_path: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Return merged doctopus JSON configs."""
    if config is not None:
        return config
    config_path = config_path or "configs"
    return _ConfigLoader.load_configs(
        config_path=config_path,
        config_files={
            "categories": "doctopus_sorting_rules.json",
            "extraction_rules": "extraction_rules.json",
            "metadata_triggers": "metadata_triggers.json"
        }
    )