@echo off
cd /d %~dp0\..

if not exist .venv (
    echo Please install project dependencies first.
)

pyinstaller --noconfirm --clean --onefile --windowed ^
  --name EasyReader ^
  --add-data "models;models" ^
  main.py

pause
