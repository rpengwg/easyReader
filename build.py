from pathlib import Path
import subprocess
import shutil

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
MODELS = ROOT / "models"


def build():
    cmd = [
        "pyinstaller",
        "EasyReader.spec",
        "--clean",
    ]
    subprocess.check_call(cmd)

    target = DIST / "EasyReader"
    if target.exists():
        model_target = target / "models"
        if model_target.exists():
            shutil.rmtree(model_target)
        if MODELS.exists():
            shutil.copytree(MODELS, model_target)


if __name__ == "__main__":
    build()
