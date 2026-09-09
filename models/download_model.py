from pathlib import Path
from urllib.request import urlretrieve

BASE = Path(__file__).resolve().parent
BASE.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main/zh/zh_CN/huayan/medium/"
FILES = [
    "zh_CN-huayan-medium.onnx",
    "zh_CN-huayan-medium.onnx.json",
]

for name in FILES:
    target = BASE / name
    if target.exists():
        print(f"Already exists: {name}")
        continue
    print(f"Downloading: {name}")
    urlretrieve(BASE_URL + name, target)
    print(f"Saved: {target}")

print("Model download complete.")
