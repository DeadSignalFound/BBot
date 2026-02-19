from dataclasses import dataclass, field
from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    endpoint: str
    response_path: str
    enabled: bool = True
    headers: dict[str, str] = field(default_factory=dict)


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
