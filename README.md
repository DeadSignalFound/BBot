# Catgirl Viewer (Production-Ready, Linux + Windows)

A customizable desktop GUI for browsing **catgirl/neko-only** images from a large, configurable API catalog.

## Highlights

- Production-friendly `src/` package structure
- Fully configurable JSON runtime (no code edits needed for most changes)
- Multiple provider support with rotation + random mode
- Expandable provider catalog with `enabled` flags
- Optional per-provider HTTP headers for APIs that require custom headers
- Cross-platform usage on Linux and Windows
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
├── app.py
├── config/
│   └── default.json
├── app.py                          # Simple launcher entrypoint
├── config/
│   └── default.json                # Main runtime + provider configuration
├── requirements.txt
├── README.md
└── src/
    └── catgirl_viewer/
        ├── __init__.py
        ├── main.py
        ├── models.py
        ├── providers/
        │   └── http_provider.py
        ├── services/
        │   └── image_service.py
        ├── ui/
        │   └── app.py
        └── utils/
            └── config_loader.py
```
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
# Catgirl Viewer (Linux + Windows)

A desktop GUI app that fetches and displays **catgirl-only anime images** from multiple APIs.

The viewer is built with Python + Tkinter and works on both Linux and Windows.

## Features

- GUI image viewer with simple controls
- Pulls images from **multiple catgirl-friendly APIs**
- Catgirl-only category enforcement by endpoint/tag selection
- Source visibility (shows where the image came from)
- One-click image save
- Keyboard shortcuts for quick browsing
- Cross-platform support (Linux and Windows)

## APIs Used

The app rotates through these endpoints:

1. **waifu.pics**
   - Endpoint: `https://api.waifu.pics/sfw/neko`
   - Uses the `neko` category for catgirl-style images.
2. **nekos.best**
   - Endpoint: `https://nekos.best/api/v2/neko`
   - Uses the `neko` category for catgirl-style images.

> Note: API content quality and interpretation may vary because data is externally provided. This app enforces catgirl-only intent by only querying catgirl/neko endpoints.

## Requirements

- Python 3.9+
- Internet access

## Install

### Linux
- Internet connection
- Tkinter (provided by your OS, not pip)

## Installation

### 1) Clone/download project

```bash
git clone <your-repo-url>
cd BBot
```

### 2) Create and activate virtual environment (recommended)

#### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows (PowerShell)
```

#### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

### Linux/macOS
### Default config

```bash
PYTHONPATH=src python app.py
```

### Windows (PowerShell)
On Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
py app.py
```

### Use a custom config file
### Custom config file

```bash
PYTHONPATH=src python -m catgirl_viewer.main --config config/default.json
```

## API catalog (catgirl/neko)

`config/default.json` now contains a broad list of API providers.

### Enabled by default

- waifu.pics (`/sfw/neko`)
- nekos.best (`/api/v2/neko`)
- waifu.im (`/search?included_tags=neko`)
- nekos.life (`/api/v2/img/neko`)
- nekobot.xyz (`/api/image?type=neko`)

### Included but disabled (experimental templates)

- nekosia.cat
- nekos.moe
- nekidev

> Experimental entries are included so you can quickly test/enable more providers. Response formats and endpoint stability can change over time.

## Full customization

Everything is controlled in `config/default.json`.

### Provider object schema

```json
{
  "name": "Human-readable provider name",
  "endpoint": "https://provider/endpoint",
  "response_path": "json.path.to.image.url",
  "enabled": true,
  "headers": {
    "Optional-Header": "value"
  }
}
```

### Notes

- `response_path` supports nested dictionary keys and list indexes:
  - `url`
  - `results.0.url`
  - `images.0.url`
- Set `enabled: false` to keep a provider in catalog but skip at runtime.
- At least one provider must be enabled, or startup will fail.
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

### Tkinter missing on Linux
### Tkinter not available (Linux)
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

## Running

### Linux

```bash
python3 app.py
```

### Windows

```powershell
py app.py
```

## GUI Usage

- **Next Catgirl**: Fetches another image from the currently selected API source
- **Switch API**: Rotates to the next API provider
- **Save Image**: Saves the currently displayed image to your local machine
- **Random API each fetch** (checkbox): Randomly chooses provider each time

### Keyboard shortcuts

- `N` => Next Catgirl
- `A` => Switch API
- `S` => Save image
- `R` => Toggle random API mode

## Project Structure

```text
BBot/
├── app.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Troubleshooting

### No image appears

- Check internet connectivity
- API may be temporarily down; click **Switch API** and try again
- Some corporate/firewalled networks block external APIs

### Tkinter error on Linux

Tkinter is not available via pip. Install it from your distro packages, for example:

```bash
sudo apt-get update
sudo apt-get install -y python3-tk
```

### Providers failing

- APIs may be rate-limited, blocked, or temporarily down
- Disable unstable providers in config
- Increase timeout values in `network`

### Import error

Ensure `PYTHONPATH=src` is set before launch.

## Safety/content note

This app is intended for **SFW catgirl/neko-style endpoints only**. Third-party APIs control returned data.
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
Other distros:

```bash
# Fedora
sudo dnf install -y python3-tkinter

# Arch
sudo pacman -S tk
```

### SSL/requests errors

Update pip and certificates:

```bash
python -m pip install --upgrade pip certifi
```

## Safety and content note

This viewer targets **SFW catgirl/neko** endpoints only. External APIs can change over time, and content is controlled by those providers.

## License

MIT (or your preferred license).
