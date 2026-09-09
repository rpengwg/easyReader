@echo off
setlocal
cd /d %~dp0\..

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.10 or newer.
  pause
  exit /b 1
)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Download the exact model required by the release.
python models\download_model.py
if errorlevel 1 (
  echo Model download failed.
  pause
  exit /b 1
)

rmdir /s /q build\pyinstaller 2>nul
rmdir /s /q dist 2>nul
rmdir /s /q release 2>nul

python -m PyInstaller --noconfirm --clean --windowed --onedir --name EasyReader ^
  --collect-all piper ^
  --collect-all pystray ^
  --collect-all pygame ^
  --hidden-import=uiautomation ^
  --add-data "models;models" ^
  --distpath dist ^
  --workpath build\pyinstaller ^
  main.py
if errorlevel 1 (
  echo PyInstaller build failed.
  pause
  exit /b 1
)

mkdir release\EasyReader-V1.0
xcopy /E /I /Y dist\EasyReader release\EasyReader-V1.0\EasyReader
copy /Y README.md release\EasyReader-V1.0\README.md
copy /Y LICENSE release\EasyReader-V1.0\LICENSE

powershell -NoProfile -Command "Compress-Archive -Path 'release\EasyReader-V1.0\*' -DestinationPath 'release\EasyReader-V1.0-Windows-x64.zip' -Force"

echo.
echo ============================================
echo Release created:
echo release\EasyReader-V1.0-Windows-x64.zip
echo ============================================
pause
