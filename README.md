# EasyReader V1.0 Release

EasyReader 是一个 Windows 中文离线朗读工具。程序启动后会驻留在系统托盘，用户用鼠标选中文字后，程序自动读取并使用本地 Piper 中文语音进行朗读。

## Release 版特点

- 鼠标选中文本后自动朗读
- 优先使用 Windows UI Automation，失败时自动模拟 `Ctrl+C` 获取选中文字
- 支持多数可复制文本的 Word、TXT、浏览器、PDF 阅读器和普通文本窗口
- Piper 中文离线语音
- Release 包直接携带 `zh_CN-huayan-medium` 模型
- 用户下载 ZIP、解压后即可运行，不需要安装 Python
- 系统托盘后台运行
- 长文本自动分段朗读

## 快捷键

| 快捷键 | 功能 |
| --- | --- |
| `ESC` | 暂停 / 继续 |
| `Ctrl + ESC` | 停止当前朗读 |
| `Ctrl + Shift + E` | 退出 EasyReader |

## 直接使用 Release 包

从 GitHub Releases 下载：

`EasyReader-V1.0-Windows-x64.zip`

解压后保持目录结构不变：

```text
EasyReader-V1.0/
├── EasyReader/
│   ├── EasyReader.exe
│   ├── _internal/
│   └── models/
│       ├── zh_CN-huayan-medium.onnx
│       └── zh_CN-huayan-medium.onnx.json
├── README.md
└── LICENSE
```

然后双击：

```text
EasyReader/EasyReader.exe
```

程序不会显示主窗口，会在 Windows 系统托盘中运行。

## 使用方法

1. 启动 EasyReader。
2. 打开 Word、TXT、网页或其他可选择文字的程序。
3. 鼠标拖动选择一段文字。
4. 松开鼠标后，EasyReader 自动开始朗读。
5. 按 `ESC` 暂停或继续。

如果某个程序无法自动读取选中文字，请确认该程序允许普通的 `Ctrl+C` 复制操作。

## 从源码运行

### 环境

- Windows 10 / Windows 11
- Python 3.10 或更高版本

### 安装依赖

```bash
python -m pip install -r requirements.txt
```

### 下载模型

```bash
python models/download_model.py
```

下载完成后必须存在：

```text
models/
├── zh_CN-huayan-medium.onnx
└── zh_CN-huayan-medium.onnx.json
```

### 启动

```bash
python main.py
```

## 构建 Windows Release 包

Windows 下直接双击：

```text
build/build_release.bat
```

脚本会自动：

1. 安装项目依赖。
2. 下载 Piper 中文模型。
3. 使用 PyInstaller 构建 Windows 程序。
4. 将模型复制到最终 Release 目录。
5. 生成 ZIP 发布包。

最终文件：

```text
release/EasyReader-V1.0-Windows-x64.zip
```

这个 ZIP 包携带 TTS 模型，因此目标电脑解压后可以离线运行。

## GitHub 自动构建 Release

仓库已经包含 GitHub Actions 工作流：

```text
.github/workflows/release.yml
```

你可以在 GitHub 的 Actions 页面手动运行 `Build EasyReader Release`，构建完成后下载 Artifact。

如果推送一个 `v` 开头的版本标签，例如：

```bash
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions 会在 Windows 环境自动下载模型、构建 EXE、打包 ZIP，并尝试创建对应的 GitHub Release。

## 当前限制

EasyReader 读取的是 Windows 应用程序中“当前可选的文本”。图片、扫描版 PDF 和无法复制的文字暂时不会自动 OCR。后续版本可以增加截图 OCR 模式。

## 项目目录

```text
easyReader/
├── main.py
├── config.py
├── requirements.txt
├── capture/
│   ├── selection.py
│   ├── auto_copy.py
│   └── clipboard.py
├── control/
│   └── hotkey.py
├── tts/
│   ├── piper_engine.py
│   ├── player.py
│   └── splitter.py
├── ui/
│   └── tray.py
├── models/
│   └── download_model.py
├── build/
│   └── build_release.bat
└── .github/workflows/
    └── release.yml
```
