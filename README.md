# EasyReader V1.0

EasyReader is an offline Chinese screen reading assistant based on Piper TTS.

## Features

- Mouse select text and automatically read
- Windows UI Automation text capture
- Piper offline Chinese TTS
- ESC pause/resume
- Long text segmentation
- CPU friendly

## Installation

Requirements:

- Windows 10/11
- Python 3.10+

Install dependencies:

```bash
pip install -r requirements.txt
```

Download Chinese voice model:

```bash
python models/download_model.py
```

Start:

```bash
python main.py
```

## Build EXE

Install PyInstaller:

```bash
pip install pyinstaller
```

Run:

```bash
build\\build.bat
```

The generated program will be in the dist directory.

## Controls

| Key | Action |
|-|-|
| ESC | Pause / Resume |

## Model

Default voice:

`zh_CN-huayan-medium`

The model runs locally and does not require network access after download.
