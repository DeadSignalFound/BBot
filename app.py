from catgirl_viewer.main import run


if __name__ == "__main__":
    run()
import io
import os
import random
from datetime import datetime

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Tkinter is not available.\n"
        "Install it via your OS package manager (not pip).\n"
        "Examples:\n"
        "  Ubuntu/Debian: sudo apt-get install python3-tk\n"
        "  Fedora: sudo dnf install python3-tkinter\n"
        "  Arch: sudo pacman -S tk\n"
    ) from exc

import requests
from PIL import Image, ImageTk


class CatgirlViewer:
    API_SOURCES = [
        {
            "name": "waifu.pics",
            "url": "https://api.waifu.pics/sfw/neko",
            "image_parser": lambda data: data.get("url"),
        },
        {
            "name": "nekos.best",
            "url": "https://nekos.best/api/v2/neko",
            "image_parser": lambda data: (
                data.get("results", [{}])[0].get("url") if data.get("results") else None
            ),
        },
    ]

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Catgirl Viewer")
        self.root.geometry("980x760")
        self.root.minsize(760, 580)

        self.current_api_index = 0
        self.current_image_bytes = None
        self.current_image_pil = None
        self.current_photo = None
        self.current_image_url = ""
        self.random_api_enabled = tk.BooleanVar(value=False)

        self._build_ui()
        self._bind_shortcuts()
        self.fetch_next_image()

    def _build_ui(self) -> None:
        container = tk.Frame(self.root, padx=12, pady=12)
        container.pack(fill=tk.BOTH, expand=True)

        title = tk.Label(
            container,
            text="Catgirl Image Viewer",
            font=("Segoe UI", 16, "bold"),
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            container,
            text="SFW catgirl/neko feeds only",
            font=("Segoe UI", 10),
            fg="#555",
        )
        subtitle.pack(anchor="w", pady=(0, 10))

        controls = tk.Frame(container)
        controls.pack(fill=tk.X, pady=(0, 10))

        tk.Button(controls, text="Next Catgirl (N)", command=self.fetch_next_image).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        tk.Button(controls, text="Switch API (A)", command=self.switch_api).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        tk.Button(controls, text="Save Image (S)", command=self.save_image).pack(
            side=tk.LEFT, padx=(0, 8)
        )

        tk.Checkbutton(
            controls,
            text="Random API each fetch (R)",
            variable=self.random_api_enabled,
        ).pack(side=tk.LEFT)

        self.status_var = tk.StringVar(value="Ready")
        status = tk.Label(container, textvariable=self.status_var, anchor="w", fg="#333")
        status.pack(fill=tk.X, pady=(0, 8))

        self.image_panel = tk.Label(
            container,
            bg="#121212",
            fg="#f2f2f2",
            text="Loading catgirl image...",
            font=("Segoe UI", 12),
        )
        self.image_panel.pack(fill=tk.BOTH, expand=True)

        footer = tk.Frame(container)
        footer.pack(fill=tk.X, pady=(8, 0))

        self.source_var = tk.StringVar(value="Source: -")
        self.url_var = tk.StringVar(value="URL: -")

        tk.Label(footer, textvariable=self.source_var, anchor="w").pack(fill=tk.X)
        tk.Label(footer, textvariable=self.url_var, anchor="w", fg="#444").pack(fill=tk.X)

        self.root.bind("<Configure>", self._on_resize)

    def _bind_shortcuts(self) -> None:
        self.root.bind("n", lambda _: self.fetch_next_image())
        self.root.bind("N", lambda _: self.fetch_next_image())
        self.root.bind("a", lambda _: self.switch_api())
        self.root.bind("A", lambda _: self.switch_api())
        self.root.bind("s", lambda _: self.save_image())
        self.root.bind("S", lambda _: self.save_image())
        self.root.bind("r", lambda _: self._toggle_random_api())
        self.root.bind("R", lambda _: self._toggle_random_api())

    def _toggle_random_api(self) -> None:
        self.random_api_enabled.set(not self.random_api_enabled.get())
        state = "enabled" if self.random_api_enabled.get() else "disabled"
        self.status_var.set(f"Random API mode {state}.")

    def switch_api(self) -> None:
        self.current_api_index = (self.current_api_index + 1) % len(self.API_SOURCES)
        source = self.API_SOURCES[self.current_api_index]["name"]
        self.status_var.set(f"Switched API to {source}.")
        self.fetch_next_image()

    def fetch_next_image(self) -> None:
        try:
            source = self._choose_source()
            source_name = source["name"]
            self.status_var.set(f"Fetching from {source_name}...")
            self.root.update_idletasks()

            response = requests.get(source["url"], timeout=15)
            response.raise_for_status()
            data = response.json()

            image_url = source["image_parser"](data)
            if not image_url:
                raise ValueError(f"No image URL found in {source_name} response.")

            image_resp = requests.get(image_url, timeout=20)
            image_resp.raise_for_status()

            self.current_image_bytes = image_resp.content
            self.current_image_url = image_url

            self.current_image_pil = Image.open(io.BytesIO(self.current_image_bytes)).convert(
                "RGB"
            )

            self._render_current_image()

            self.source_var.set(f"Source: {source_name}")
            self.url_var.set(f"URL: {image_url}")
            self.status_var.set("Loaded a catgirl image.")
        except Exception as error:
            self.status_var.set(f"Error fetching image: {error}")
            messagebox.showerror("Fetch Error", f"Could not fetch catgirl image.\n\n{error}")

    def _choose_source(self):
        if self.random_api_enabled.get():
            return random.choice(self.API_SOURCES)
        return self.API_SOURCES[self.current_api_index]

    def _render_current_image(self) -> None:
        if self.current_image_pil is None:
            return

        panel_w = max(self.image_panel.winfo_width(), 300)
        panel_h = max(self.image_panel.winfo_height(), 300)

        img = self.current_image_pil.copy()
        img.thumbnail((panel_w - 20, panel_h - 20), Image.Resampling.LANCZOS)
        self.current_photo = ImageTk.PhotoImage(img)

        self.image_panel.config(image=self.current_photo, text="")

    def _on_resize(self, _event) -> None:
        if self.current_image_pil is not None:
            self._render_current_image()

    def save_image(self) -> None:
        if not self.current_image_bytes:
            messagebox.showinfo("No Image", "Load an image first.")
            return

        default_name = f"catgirl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        file_path = filedialog.asksaveasfilename(
            title="Save catgirl image",
            defaultextension=".jpg",
            initialfile=default_name,
            filetypes=[("JPEG Image", "*.jpg"), ("PNG Image", "*.png"), ("All Files", "*.*")],
        )

        if not file_path:
            return

        extension = os.path.splitext(file_path)[1].lower()
        image_format = "PNG" if extension == ".png" else "JPEG"

        try:
            image = Image.open(io.BytesIO(self.current_image_bytes)).convert("RGB")
            image.save(file_path, format=image_format)
            self.status_var.set(f"Saved image to {file_path}")
        except Exception as error:
            messagebox.showerror("Save Error", f"Could not save image.\n\n{error}")


def main() -> None:
    root = tk.Tk()
    CatgirlViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
