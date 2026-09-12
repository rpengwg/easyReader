from pathlib import Path
import subprocess
import shutil

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
RELEASE = ROOT / "release"


def prepare_release():
    if RELEASE.exists():
        shutil.rmtree(RELEASE)

    RELEASE.mkdir(parents=True)
    (RELEASE / "models" / "piper").mkdir(parents=True)
    (RELEASE / "config").mkdir(parents=True)
    (RELEASE / "logs").mkdir(parents=True)

    readme = RELEASE / "models" / "piper" / "README.txt"
    readme.write_text(
        "Place Piper voice models here.\n\n"
        "Example:\n"
        "zh_CN-huayan-medium.onnx\n"
        "zh_CN-huayan-medium.onnx.json\n",
        encoding="utf-8"
    )


def build():
    subprocess.check_call([
        "pyinstaller",
        "EasyReader.spec",
        "--clean",
    ])

    exe_dir = DIST / "EasyReader"
    if exe_dir.exists():
        shutil.copytree(exe_dir, RELEASE, dirs_exist_ok=True)

    prepare_release()


if __name__ == "__main__":
    build()
