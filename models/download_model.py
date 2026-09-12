from pathlib import Path
import json
import sys

BASE = Path(__file__).resolve().parent

SUPPORTED_MODELS = {
    "zh_CN": "zh_CN-huayan-medium.onnx",
    "en_US": "en_US-lessac-medium.onnx",
}


def list_models():
    return [p.name for p in BASE.glob("*.onnx")]


def model_info():
    return {
        "available": list_models(),
        "supported": SUPPORTED_MODELS,
    }


def check_models():
    info = model_info()
    print(json.dumps(info, ensure_ascii=False, indent=2))

    # Offline build mode: models are optional.
    # Models are external files and should not break EXE packaging.
    if not info["available"]:
        print("No local Piper model found.")
        print("This is OK. Models can be added later under models/piper/")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(check_models())
