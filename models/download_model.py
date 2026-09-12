from pathlib import Path
import json

BASE = Path(__file__).resolve().parent / "piper"

SUPPORTED_MODELS = {
    "zh_CN": "zh_CN-huayan-medium.onnx",
    "en_US": "en_US-lessac-medium.onnx",
}


def list_models():
    if not BASE.exists():
        return []
    return [p.name for p in BASE.glob("*.onnx")]


def model_info():
    return {
        "available": list_models(),
        "supported": SUPPORTED_MODELS,
    }


def check_models():
    info = model_info()
    print(json.dumps(info, ensure_ascii=False, indent=2))

    if not info["available"]:
        print("No local Piper model found.")
        print("This is normal for lightweight builds.")
        print("Models can be added later under models/piper/")

    # Never fail CI/CD build because models are external resources.
    return


if __name__ == "__main__":
    check_models()
