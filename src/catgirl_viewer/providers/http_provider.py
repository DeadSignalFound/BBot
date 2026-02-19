from __future__ import annotations

from dataclasses import dataclass

import requests

from catgirl_viewer.models import ProviderConfig
from catgirl_viewer.utils.config_loader import get_path_value


@dataclass
class ProviderImage:
    provider_name: str
    image_url: str
    image_bytes: bytes


class ProviderClient:
    def __init__(self, timeout_seconds: int, image_timeout_seconds: int):
        self.timeout_seconds = timeout_seconds
        self.image_timeout_seconds = image_timeout_seconds

    def fetch(self, provider: ProviderConfig) -> ProviderImage:
        response = requests.get(
            provider.endpoint,
            headers=provider.headers,
            timeout=self.timeout_seconds,
        )
        response = requests.get(provider.endpoint, timeout=self.timeout_seconds)
        response.raise_for_status()

        payload = response.json()
        image_url = get_path_value(payload, provider.response_path)

        image_response = requests.get(image_url, timeout=self.image_timeout_seconds)
        image_response.raise_for_status()

        return ProviderImage(
            provider_name=provider.name,
            image_url=image_url,
            image_bytes=image_response.content,
        )
