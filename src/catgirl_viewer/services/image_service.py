from __future__ import annotations

import io
import random
from typing import Optional

from PIL import Image

from catgirl_viewer.models import ProviderConfig
from catgirl_viewer.providers.http_provider import ProviderClient, ProviderImage


class ImageService:
    def __init__(self, providers: list[ProviderConfig], client: ProviderClient):
        self.providers = providers
        self.client = client
        self.current_provider_index = 0

    def get_current_provider(self) -> ProviderConfig:
        return self.providers[self.current_provider_index]

    def switch_provider(self) -> ProviderConfig:
        self.current_provider_index = (self.current_provider_index + 1) % len(self.providers)
        return self.get_current_provider()

    def fetch_image(self, random_provider: bool = False) -> ProviderImage:
        provider = random.choice(self.providers) if random_provider else self.get_current_provider()
        return self.client.fetch(provider)

    @staticmethod
    def decode_image(image_bytes: bytes) -> Image.Image:
        return Image.open(io.BytesIO(image_bytes)).convert("RGB")

    @staticmethod
    def resize_for_panel(image: Image.Image, panel_w: int, panel_h: int, padding: int) -> Image.Image:
        resized = image.copy()
        resized.thumbnail((max(panel_w - padding, 32), max(panel_h - padding, 32)), Image.Resampling.LANCZOS)
        return resized

    @staticmethod
    def save_image(image_bytes: bytes, file_path: str, image_format: Optional[str] = None) -> None:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image.save(file_path, format=image_format)
