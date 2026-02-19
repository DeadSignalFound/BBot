import json
from pathlib import Path

from catgirl_viewer.models import AppConfig, ProviderConfig


DEFAULT_CONFIG_PATH = Path("config/default.json")


def _extract_by_path(data: dict, path: str):
    current = data
    for token in path.split("."):
        if isinstance(current, list):
            if not token.isdigit():
                return None
            index = int(token)
            if index >= len(current):
                return None
            current = current[index]
            continue

        if not isinstance(current, dict) or token not in current:
            return None
        current = current[token]
    return current


def load_config(config_path: str | None = None) -> AppConfig:
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    with path.open("r", encoding="utf-8") as file:
        raw = json.load(file)

    providers = [
        ProviderConfig(
            name=item["name"],
            endpoint=item["endpoint"],
            response_path=item["response_path"],
        )
        for item in raw["providers"]
    ]

    return AppConfig(
        app_title=raw["app"]["title"],
        window_width=raw["window"]["width"],
        window_height=raw["window"]["height"],
        min_width=raw["window"]["min_width"],
        min_height=raw["window"]["min_height"],
        request_timeout_seconds=raw["network"]["request_timeout_seconds"],
        image_timeout_seconds=raw["network"]["image_timeout_seconds"],
        default_random_provider=raw["runtime"]["default_random_provider"],
        image_padding=raw["runtime"]["image_padding"],
        save_default_extension=raw["runtime"]["save_default_extension"],
        providers=providers,
    )


def get_path_value(data: dict, path: str):
    value = _extract_by_path(data, path)
    if value is None:
        raise ValueError(f"Path '{path}' not found in provider response.")
    return value
