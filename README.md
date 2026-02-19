# Catgirl Viewer (Production-Ready, Linux + Windows)

A customizable desktop GUI for browsing **catgirl/neko-only** images from a large, configurable API catalog.

## Highlights

- Production-friendly `src/` package structure
- Fully configurable JSON runtime (no code edits needed for most changes)
- Multiple provider support with rotation + random mode
- Expandable provider catalog with `enabled` flags
- Optional per-provider HTTP headers for APIs that require custom headers
- Cross-platform usage on Linux and Windows

## Project structure

```text
BBot/
├── app.py
├── config/
│   └── default.json
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

### Linux/macOS

```bash
PYTHONPATH=src python app.py
```

### Windows (PowerShell)

```powershell
$env:PYTHONPATH = "src"
py app.py
```

### Use a custom config file

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

## Controls

- **Next (N)**: Load next image
- **Switch API (A)**: Move to next provider and load image
- **Save (S)**: Save current image to disk
- **Random provider (R)**: Toggle random source per fetch

## Troubleshooting

### Tkinter missing on Linux

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

## License

MIT
