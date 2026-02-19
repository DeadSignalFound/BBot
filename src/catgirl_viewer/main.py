from __future__ import annotations

import argparse
import tkinter as tk

from catgirl_viewer.providers.http_provider import ProviderClient
from catgirl_viewer.services.image_service import ImageService
from catgirl_viewer.ui.app import CatgirlViewerApp
from catgirl_viewer.utils.config_loader import load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Catgirl Viewer")
    parser.add_argument(
        "--config",
        default=None,
        help="Path to JSON config file (default: config/default.json)",
    )
    return parser.parse_args()


def run() -> None:
    args = parse_args()
    config = load_config(args.config)

    client = ProviderClient(
        timeout_seconds=config.request_timeout_seconds,
        image_timeout_seconds=config.image_timeout_seconds,
    )
    image_service = ImageService(config.providers, client)

    root = tk.Tk()
    CatgirlViewerApp(root, config, image_service)
    root.mainloop()


if __name__ == "__main__":
    run()
