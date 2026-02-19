from __future__ import annotations

import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox

from PIL import ImageTk

from catgirl_viewer.models import AppConfig
from catgirl_viewer.providers.http_provider import ProviderImage
from catgirl_viewer.services.image_service import ImageService


class CatgirlViewerApp:
    def __init__(self, root: tk.Tk, config: AppConfig, image_service: ImageService):
        self.root = root
        self.config = config
        self.image_service = image_service

        self.current_image_bytes: bytes | None = None
        self.current_image_pil = None
        self.current_photo = None
        self.random_provider_enabled = tk.BooleanVar(value=config.default_random_provider)

        self._configure_window()
        self._build_ui()
        self._bind_shortcuts()
        self.fetch_next_image()

    def _configure_window(self) -> None:
        self.root.title(self.config.app_title)
        self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")
        self.root.minsize(self.config.min_width, self.config.min_height)

    def _build_ui(self) -> None:
        container = tk.Frame(self.root, padx=12, pady=12)
        container.pack(fill=tk.BOTH, expand=True)

        tk.Label(container, text=self.config.app_title, font=("Segoe UI", 16, "bold")).pack(anchor="w")
        tk.Label(container, text="Production-ready catgirl/neko viewer", fg="#555").pack(anchor="w", pady=(0, 10))

        controls = tk.Frame(container)
        controls.pack(fill=tk.X, pady=(0, 10))

        tk.Button(controls, text="Next (N)", command=self.fetch_next_image).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(controls, text="Switch API (A)", command=self.switch_api).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(controls, text="Save (S)", command=self.save_image).pack(side=tk.LEFT, padx=(0, 8))
        tk.Checkbutton(controls, text="Random provider (R)", variable=self.random_provider_enabled).pack(side=tk.LEFT)

        self.status_var = tk.StringVar(value="Ready")
        tk.Label(container, textvariable=self.status_var, anchor="w").pack(fill=tk.X, pady=(0, 8))

        self.image_panel = tk.Label(
            container,
            bg="#141414",
            fg="#eee",
            text="Loading catgirl image...",
            font=("Segoe UI", 12),
        )
        self.image_panel.pack(fill=tk.BOTH, expand=True)

        self.source_var = tk.StringVar(value="Source: -")
        self.url_var = tk.StringVar(value="URL: -")

        tk.Label(container, textvariable=self.source_var, anchor="w").pack(fill=tk.X, pady=(8, 0))
        tk.Label(container, textvariable=self.url_var, anchor="w", fg="#444").pack(fill=tk.X)

        self.root.bind("<Configure>", self._on_resize)

    def _bind_shortcuts(self) -> None:
        self.root.bind("n", lambda _: self.fetch_next_image())
        self.root.bind("N", lambda _: self.fetch_next_image())
        self.root.bind("a", lambda _: self.switch_api())
        self.root.bind("A", lambda _: self.switch_api())
        self.root.bind("s", lambda _: self.save_image())
        self.root.bind("S", lambda _: self.save_image())
        self.root.bind("r", lambda _: self._toggle_random_provider())
        self.root.bind("R", lambda _: self._toggle_random_provider())

    def _toggle_random_provider(self) -> None:
        self.random_provider_enabled.set(not self.random_provider_enabled.get())
        mode = "enabled" if self.random_provider_enabled.get() else "disabled"
        self.status_var.set(f"Random provider mode {mode}.")

    def switch_api(self) -> None:
        provider = self.image_service.switch_provider()
        self.status_var.set(f"Switched provider to {provider.name}.")
        self.fetch_next_image()

    def fetch_next_image(self) -> None:
        try:
            provider_image = self.image_service.fetch_image(
                random_provider=self.random_provider_enabled.get()
            )
            self._apply_provider_image(provider_image)
            self.status_var.set("Loaded a catgirl image.")
        except Exception as error:
            self.status_var.set(f"Error: {error}")
            messagebox.showerror("Fetch Error", f"Could not fetch image.\n\n{error}")

    def _apply_provider_image(self, provider_image: ProviderImage) -> None:
        self.current_image_bytes = provider_image.image_bytes
        self.current_image_pil = self.image_service.decode_image(provider_image.image_bytes)
        self._render_current_image()
        self.source_var.set(f"Source: {provider_image.provider_name}")
        self.url_var.set(f"URL: {provider_image.image_url}")

    def _render_current_image(self) -> None:
        if self.current_image_pil is None:
            return

        panel_w = max(self.image_panel.winfo_width(), 300)
        panel_h = max(self.image_panel.winfo_height(), 300)

        image = self.image_service.resize_for_panel(
            self.current_image_pil, panel_w, panel_h, self.config.image_padding
        )
        self.current_photo = ImageTk.PhotoImage(image)
        self.image_panel.config(image=self.current_photo, text="")

    def _on_resize(self, _event) -> None:
        self._render_current_image()

    def save_image(self) -> None:
        if not self.current_image_bytes:
            messagebox.showinfo("No Image", "Load an image first.")
            return

        default_extension = self.config.save_default_extension
        default_name = f"catgirl_{datetime.now().strftime('%Y%m%d_%H%M%S')}{default_extension}"

        file_path = filedialog.asksaveasfilename(
            title="Save catgirl image",
            defaultextension=default_extension,
            initialfile=default_name,
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("All Files", "*.*")],
        )

        if not file_path:
            return

        extension = os.path.splitext(file_path)[1].lower()
        image_format = "PNG" if extension == ".png" else "JPEG"

        try:
            self.image_service.save_image(self.current_image_bytes, file_path, image_format=image_format)
            self.status_var.set(f"Saved: {file_path}")
        except Exception as error:
            messagebox.showerror("Save Error", f"Could not save image.\n\n{error}")
