from pathlib import Path
import json

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


if __name__ == "__main__":
    print(json.dumps(model_info(), ensure_ascii=False, indent=2))
