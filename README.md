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
```

#### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
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
