import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


class SettingsWindow:
    def __init__(self, app):
        self.app = app
        self.window = None

    def show(self):
        if self.window and self.window.winfo_exists():
            self.window.deiconify()
            self.window.lift()
            self.window.focus_force()
            return

        settings = self.app.settings.tts
        self.window = tk.Tk()
        self.window.title("EasyReader 设置")
        self.window.geometry("560x300")
        self.window.resizable(False, False)

        frame = ttk.Frame(self.window, padding=18)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="当前声音").grid(row=0, column=0, sticky="w", pady=8)
        self.voice_var = tk.StringVar(value=settings.get("voice", ""))
        self.voice_box = ttk.Combobox(frame, textvariable=self.voice_var, state="readonly", width=48)
        self.voice_box.grid(row=0, column=1, sticky="ew", padx=(12, 0))
        self.refresh_voices()

        ttk.Label(frame, text="语速").grid(row=1, column=0, sticky="w", pady=8)
        self.speed_var = tk.DoubleVar(value=float(settings.get("speed", 1.0)))
        self.speed = ttk.Scale(frame, from_=0.5, to=2.0, variable=self.speed_var, orient="horizontal")
        self.speed.grid(row=1, column=1, sticky="ew", padx=(12, 0))
        self.speed_value = ttk.Label(frame, text="1.00x")
        self.speed_value.grid(row=1, column=2, padx=(8, 0))
        self.speed_var.trace_add("write", lambda *_: self.speed_value.configure(text=f"{self.speed_var.get():.2f}x"))

        ttk.Label(frame, text="音量").grid(row=2, column=0, sticky="w", pady=8)
        self.volume_var = tk.DoubleVar(value=float(settings.get("volume", 1.0)))
        self.volume = ttk.Scale(frame, from_=0.0, to=2.0, variable=self.volume_var, orient="horizontal")
        self.volume.grid(row=2, column=1, sticky="ew", padx=(12, 0))
        self.volume_value = ttk.Label(frame, text="100%")
        self.volume_value.grid(row=2, column=2, padx=(8, 0))
        self.volume_var.trace_add("write", lambda *_: self.volume_value.configure(text=f"{self.volume_var.get() * 100:.0f}%"))

        ttk.Label(frame, text="模型路径").grid(row=3, column=0, sticky="w", pady=8)
        self.path_var = tk.StringVar(value=settings.get("model_dir", str(self.app.tts.loader.model_dir)))
        ttk.Entry(frame, textvariable=self.path_var).grid(row=3, column=1, sticky="ew", padx=(12, 6))
        ttk.Button(frame, text="选择…", command=self.choose_path).grid(row=3, column=2)

        buttons = ttk.Frame(frame)
        buttons.grid(row=4, column=0, columnspan=3, sticky="e", pady=(22, 0))
        ttk.Button(buttons, text="应用", command=self.save).pack(side="left", padx=5)
        ttk.Button(buttons, text="关闭", command=self.close).pack(side="left", padx=5)

        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.window.mainloop()

    def refresh_voices(self):
        model_dir = Path(self.path_var.get() if hasattr(self, "path_var") else self.app.tts.loader.model_dir).expanduser()
        voices = sorted(p.name for p in model_dir.glob("*.onnx")) if model_dir.exists() else []
        self.voice_box["values"] = voices
        if self.voice_var.get() not in voices and voices:
            self.voice_var.set(voices[0])

    def choose_path(self):
        selected = filedialog.askdirectory(title="选择 Piper 模型目录", initialdir=self.path_var.get() or str(Path.home()))
        if selected:
            self.path_var.set(selected)
            self.refresh_voices()

    def save(self):
        model_dir = Path(self.path_var.get()).expanduser()
        voices = list(model_dir.glob("*.onnx")) if model_dir.exists() else []
        voice = self.voice_var.get()
        if voice and not (model_dir / voice).exists():
            messagebox.showerror("EasyReader", "选择的声音模型不存在。")
            return
        if not voices:
            messagebox.showwarning("EasyReader", "该目录没有 .onnx Piper 模型，设置仍可保存。")
        self.app.settings.update_tts(str(model_dir), voice, self.speed_var.get(), self.volume_var.get())
        self.app.tts.configure(model_dir, voice, self.speed_var.get(), self.volume_var.get())
        messagebox.showinfo("EasyReader", "设置已保存。")

    def close(self):
        if self.window:
            self.window.destroy()
            self.window = None
