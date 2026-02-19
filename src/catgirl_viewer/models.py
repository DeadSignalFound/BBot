from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    endpoint: str
    response_path: str


@dataclass(frozen=True)
class AppConfig:
    app_title: str
    window_width: int
    window_height: int
    min_width: int
    min_height: int
    request_timeout_seconds: int
    image_timeout_seconds: int
    default_random_provider: bool
    image_padding: int
    save_default_extension: str
    providers: list[ProviderConfig]
