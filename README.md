# Catgirl Viewer (Production-Ready, Linux + Windows)

A customizable desktop GUI for browsing **catgirl/neko-only** images from configurable APIs.

## Why this version is production-oriented

- Clean package structure (`src/` layout)
- Config-driven behavior (window size, timeouts, providers, defaults)
- Provider abstraction (easy to add APIs without touching UI logic)
- Service layer separates fetching, decoding, resizing, and saving
- CLI support for alternate config files
- Cross-platform instructions for Linux + Windows

## Project structure

```text
BBot/
├── app.py                          # Simple launcher entrypoint
├── config/
│   └── default.json                # Main runtime + provider configuration
├── requirements.txt
├── README.md
└── src/
    └── catgirl_viewer/
        ├── __init__.py
        ├── main.py                 # CLI + app bootstrap
        ├── models.py               # Dataclasses for app/provider config
        ├── providers/
        │   └── http_provider.py    # Provider HTTP client + payload model
        ├── services/
        │   └── image_service.py    # Core image/business logic
        ├── ui/
        │   └── app.py              # Tkinter GUI layer
        └── utils/
            └── config_loader.py    # JSON config loading + response path parsing
```

## Requirements

- Python 3.9+
- Internet access

## Install

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

### Default config

```bash
PYTHONPATH=src python app.py
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
py app.py
```

### Custom config file

```bash
PYTHONPATH=src python -m catgirl_viewer.main --config config/default.json
```

## Full customization guide

All customization is done in `config/default.json`.

### 1) App metadata

```json
"app": {
  "title": "Catgirl Viewer"
}
```

### 2) Window sizing

```json
"window": {
  "width": 1024,
  "height": 768,
  "min_width": 760,
  "min_height": 580
}
```

### 3) Networking behavior

```json
"network": {
  "request_timeout_seconds": 15,
  "image_timeout_seconds": 20
}
```

### 4) Runtime behavior

```json
"runtime": {
  "default_random_provider": false,
  "image_padding": 20,
  "save_default_extension": ".jpg"
}
```

### 5) API providers (catgirl/neko only)

```json
"providers": [
  {
    "name": "waifu.pics",
    "endpoint": "https://api.waifu.pics/sfw/neko",
    "response_path": "url"
  },
  {
    "name": "nekos.best",
    "endpoint": "https://nekos.best/api/v2/neko",
    "response_path": "results.0.url"
  }
]
```

#### Adding a new provider

1. Add provider object to `providers`.
2. Set `endpoint` to the provider's catgirl/neko route.
3. Set `response_path` to where the direct image URL exists in response JSON.
   - Dot path supports dictionary keys and list indexes.
   - Example: `results.0.url`

## Controls

- **Next (N)**: Load next image
- **Switch API (A)**: Move to next provider and load image
- **Save (S)**: Save current image to disk
- **Random provider (R)**: Toggle random source per fetch

## Troubleshooting

### Tkinter not available (Linux)

```bash
sudo apt-get update
sudo apt-get install -y python3-tk
```

### No images loading

- Check network access
- Verify API provider endpoint in config
- Increase timeout values in `network` settings

### Module import error

Make sure `PYTHONPATH=src` is set when running.

## Security/content notes

- This app is intended for SFW catgirl/neko endpoints only.
- API data is controlled by third-party services and may change.

## License

MIT
