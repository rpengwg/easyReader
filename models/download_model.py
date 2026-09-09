from pathlib import Path
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent
MODEL_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main/zh/zh_CN/huayan/medium"
FILES = ["zh_CN-huayan-medium.onnx", "zh_CN-huayan-medium.onnx.json"]


def download(url, target):
    request = Request(url, headers={"User-Agent": "EasyReader/1.0"})
    with urlopen(request, timeout=60) as response, open(target, "wb") as output:
        total = int(response.headers.get("Content-Length", 0))
        downloaded = 0
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            output.write(chunk)
            downloaded += len(chunk)
            if total:
                print(f"{target.name}: {downloaded * 100 // total}%", end="\r")
    print(f"{target.name}: complete")


for name in FILES:
    target = BASE / name
    if target.exists() and target.stat().st_size > 0:
        print(f"Already exists: {name}")
        continue
    print(f"Downloading: {name}")
    download(f"{MODEL_BASE}/{name}", target)

print("Piper Chinese model is ready.")
