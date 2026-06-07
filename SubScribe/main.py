import customtkinter as ctk
import threading
import subprocess
import os
import sys
import json
import time
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk

# ── App config ──────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

APP_NAME  = "SubScribe"
APP_VER   = "1.0.0"
WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]
LANGUAGES = {
    "Auto Detect": None,
    "English": "en",
    "Arabic": "ar",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Japanese": "ja",
    "Chinese": "zh",
    "Portuguese": "pt",
    "Russian": "ru",
    "Korean": "ko",
    "Turkish": "tr",
    "Hindi": "hi",
}
OUTPUT_FORMATS = ["srt", "vtt", "txt", "json", "tsv"]


# ── Helpers ──────────────────────────────────────────────────────────────────
def resource_path(relative_path):
    """Works for dev and PyInstaller."""
    try:
        base = sys._MEIPASS
    except AttributeError:
        base = os.path.abspath(".")
    return os.path.join(base, relative_path)


def app_dir():
    """Root folder next to the exe (PyInstaller) or next to main.py (dev)."""
    if getattr(sys, "frozen", False):
        # Running as compiled .exe — use the folder containing the exe
        return Path(sys.executable).parent
    else:
        # Running as plain Python script
        return Path(__file__).parent


def models_dir():
    """Always: <app_folder>/models/  — created on first use."""
    d = app_dir() / "models"
    d.mkdir(exist_ok=True)
    return d


# Whisper model file names on disk
WHISPER_MODEL_FILES = {
    "tiny":   "tiny.pt",
    "base":   "base.pt",
    "small":  "small.pt",
    "medium": "medium.pt",
    "large":  "large-v3.pt",
}
# Approx download sizes (MB) for display
WHISPER_MODEL_SIZES = {
    "tiny":   75,
    "base":   145,
    "small":  460,
    "medium": 1500,
    "large":  3100,
}


def model_is_cached(name: str) -> bool:
    """Return True if the model .pt file exists in our models/ folder."""
    fname = WHISPER_MODEL_FILES.get(name)
    if not fname:
        return False
    return (models_dir() / fname).exists()


def ffmpeg_path():
    """Return ffmpeg binary path."""
    bundled = resource_path("ffmpeg/ffmpeg.exe" if sys.platform == "win32" else "ffmpeg/ffmpeg")
    if os.path.exists(bundled):
        return bundled
    return "ffmpeg"  # rely on system PATH


def check_whisper():
    try:
        import whisper
        return True, whisper.__version__ if hasattr(whisper, "__version__") else "installed"
    except ImportError:
        return False, None


def check_ffmpeg():
    try:
        result = subprocess.run(
            [ffmpeg_path(), "-version"],
            capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def seconds_to_srt_time(seconds):
    hours   = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs    = int(seconds % 60)
    millis  = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def segments_to_srt(segments):
    lines = []
    for i, seg in enumerate(segments, 1):
        start = seconds_to_srt_time(seg["start"])
        end   = seconds_to_srt_time(seg["end"])
        text  = seg["text"].strip()
        lines.append(f"{i}\n{start} --> {end}\n{text}\n")
    return "\n".join(lines)


def segments_to_vtt(segments):
    lines = ["WEBVTT\n"]
    for seg in segments:
        start = seconds_to_srt_time(seg["start"]).replace(",", ".")
        end   = seconds_to_srt_time(seg["end"]).replace(",", ".")
        text  = seg["text"].strip()
        lines.append(f"{start} --> {end}\n{text}\n")
    return "\n".join(lines)


# ── Main Window ───────────────────────────────────────────────────────────────
class SubScribeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"{APP_NAME} v{APP_VER} — Local AI Subtitle Generator")
        self.geometry("820x700")
        self.minsize(700, 600)
        self.resizable(True, True)

        self.video_path     = tk.StringVar()
        self.output_dir     = tk.StringVar()
        self.model_var      = tk.StringVar(value="base")
        self.language_var   = tk.StringVar(value="Auto Detect")
        self.format_var     = tk.StringVar(value="srt")
        self.burn_var       = tk.BooleanVar(value=False)
        self.task_var       = tk.StringVar(value="transcribe")  # or translate
        self.progress_var   = tk.DoubleVar(value=0)

        self._segments      = []
        self._is_running    = False
        self._cancel_flag   = False
        self._whisper_ok, _ = check_whisper()
        self._ffmpeg_ok     = check_ffmpeg()

        self._build_ui()
        self._check_dependencies()

    # ── UI build ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # ── Header ──
        header = ctk.CTkFrame(self, corner_radius=0, fg_color=("#1a1a2e", "#0d0d1a"))
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            header,
            text="⬡ SubScribe",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#7c6fff",
        ).grid(row=0, column=0, padx=20, pady=14, sticky="w")

        self.dep_label = ctk.CTkLabel(
            header,
            text="",
            font=ctk.CTkFont(size=12),
        )
        self.dep_label.grid(row=0, column=1, padx=20, pady=14, sticky="e")

        # ── File picker ──
        file_frame = ctk.CTkFrame(self, corner_radius=10)
        file_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(12, 0))
        file_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(file_frame, text="Video / Audio File", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=3, sticky="w", padx=14, pady=(10, 4)
        )

        self.file_entry = ctk.CTkEntry(
            file_frame, textvariable=self.video_path,
            placeholder_text="Drop a file or click Browse…",
            height=36,
        )
        self.file_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(14, 6), pady=(0, 10))

        ctk.CTkButton(
            file_frame, text="Browse", width=90, height=36,
            command=self._browse_file,
            fg_color="#7c6fff", hover_color="#5c4fcc",
        ).grid(row=1, column=2, padx=(0, 14), pady=(0, 10))

        # Drag & drop hint
        self.file_entry.drop_target_register = lambda *a: None
        self._setup_drag_drop()

        # ── Output dir ──
        out_frame = ctk.CTkFrame(self, corner_radius=10)
        out_frame.grid(row=2, column=0, sticky="ew", padx=16, pady=(8, 0))
        out_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(out_frame, text="Output Folder", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=3, sticky="w", padx=14, pady=(10, 4)
        )

        self.out_entry = ctk.CTkEntry(
            out_frame, textvariable=self.output_dir,
            placeholder_text="Same as input file (default)",
            height=36,
        )
        self.out_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(14, 6), pady=(0, 10))

        ctk.CTkButton(
            out_frame, text="Browse", width=90, height=36,
            command=self._browse_output,
            fg_color="#555", hover_color="#444",
        ).grid(row=1, column=2, padx=(0, 14), pady=(0, 10))

        # ── Options ──
        opts_frame = ctk.CTkFrame(self, corner_radius=10)
        opts_frame.grid(row=3, column=0, sticky="nsew", padx=16, pady=(8, 0))
        opts_frame.grid_columnconfigure((0,1,2,3), weight=1)
        opts_frame.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(opts_frame, text="Settings", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=14, pady=(10, 6)
        )

        # Whisper model
        ctk.CTkLabel(opts_frame, text="Whisper Model", text_color="gray70", font=ctk.CTkFont(size=12)).grid(
            row=1, column=0, sticky="w", padx=14
        )
        ctk.CTkOptionMenu(opts_frame, values=WHISPER_MODELS, variable=self.model_var, width=130).grid(
            row=2, column=0, padx=14, pady=(2, 10), sticky="w"
        )

        # Language
        ctk.CTkLabel(opts_frame, text="Language", text_color="gray70", font=ctk.CTkFont(size=12)).grid(
            row=1, column=1, sticky="w", padx=8
        )
        ctk.CTkOptionMenu(opts_frame, values=list(LANGUAGES.keys()), variable=self.language_var, width=140).grid(
            row=2, column=1, padx=8, pady=(2, 10), sticky="w"
        )

        # Format
        ctk.CTkLabel(opts_frame, text="Output Format", text_color="gray70", font=ctk.CTkFont(size=12)).grid(
            row=1, column=2, sticky="w", padx=8
        )
        ctk.CTkOptionMenu(opts_frame, values=OUTPUT_FORMATS, variable=self.format_var, width=100).grid(
            row=2, column=2, padx=8, pady=(2, 10), sticky="w"
        )

        # Task
        ctk.CTkLabel(opts_frame, text="Task", text_color="gray70", font=ctk.CTkFont(size=12)).grid(
            row=1, column=3, sticky="w", padx=8
        )
        ctk.CTkOptionMenu(
            opts_frame,
            values=["transcribe", "translate (→ English)"],
            variable=self.task_var,
            width=160
        ).grid(row=2, column=3, padx=8, pady=(2, 10), sticky="w")

        # Separator
        ctk.CTkFrame(opts_frame, height=1, fg_color="gray25").grid(
            row=3, column=0, columnspan=4, sticky="ew", padx=14, pady=4
        )

        # Burn-in option
        burn_row = ctk.CTkFrame(opts_frame, fg_color="transparent")
        burn_row.grid(row=4, column=0, columnspan=4, sticky="w", padx=14, pady=(6, 0))

        self.burn_check = ctk.CTkCheckBox(
            burn_row,
            text="Burn subtitles into video  (creates a new video file via FFmpeg)",
            variable=self.burn_var,
            checkbox_width=18, checkbox_height=18,
            onvalue=True, offvalue=False,
        )
        self.burn_check.pack(side="left")

        if not self._ffmpeg_ok:
            self.burn_check.configure(state="disabled")

        # Model size info
        model_info = ctk.CTkLabel(
            opts_frame,
            text="Model sizes: tiny≈75MB  base≈145MB  small≈460MB  medium≈1.5GB  large≈3GB",
            text_color="gray55",
            font=ctk.CTkFont(size=11),
        )
        model_info.grid(row=5, column=0, columnspan=4, sticky="w", padx=14, pady=(8, 10))

        # ── Log / progress ──
        log_frame = ctk.CTkFrame(self, corner_radius=10)
        log_frame.grid(row=4, column=0, sticky="ew", padx=16, pady=(8, 0))
        log_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(log_frame, text="Log", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, sticky="w", padx=14, pady=(10, 4)
        )

        self.log_box = ctk.CTkTextbox(log_frame, height=110, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_box.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 6))
        self.log_box.configure(state="disabled")

        self.progress_bar = ctk.CTkProgressBar(log_frame, variable=self.progress_var)
        self.progress_bar.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 10))
        self.progress_var.set(0)

        # ── Model Manager ──
        mm_frame = ctk.CTkFrame(self, corner_radius=10)
        mm_frame.grid(row=5, column=0, sticky="ew", padx=16, pady=(8, 0))
        mm_frame.grid_columnconfigure(0, weight=1)

        mm_header = ctk.CTkFrame(mm_frame, fg_color="transparent")
        mm_header.grid(row=0, column=0, sticky="ew", padx=14, pady=(10, 6))
        mm_header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(mm_header, text="Model Manager", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, sticky="w"
        )
        self.mm_folder_label = ctk.CTkLabel(
            mm_header, text="", font=ctk.CTkFont(size=11), text_color="gray55"
        )
        self.mm_folder_label.grid(row=0, column=1, sticky="e")

        self.mm_rows_frame = ctk.CTkFrame(mm_frame, fg_color="transparent")
        self.mm_rows_frame.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 10))
        for col in range(5):
            self.mm_rows_frame.grid_columnconfigure(col, weight=1)

        self._mm_widgets = {}   # name → {status_lbl, btn}
        self._build_model_manager_rows()

        # ── Action buttons ──
        btn_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        btn_frame.grid(row=6, column=0, sticky="ew", padx=16, pady=12)
        btn_frame.grid_columnconfigure(1, weight=1)

        self.run_btn = ctk.CTkButton(
            btn_frame,
            text="▶  Generate Subtitles",
            height=44,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#7c6fff",
            hover_color="#5c4fcc",
            command=self._start_generation,
        )
        self.run_btn.grid(row=0, column=0, sticky="w")

        self.cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            height=44,
            width=100,
            fg_color="#444",
            hover_color="#333",
            command=self._cancel,
            state="disabled",
        )
        self.cancel_btn.grid(row=0, column=1, padx=(10, 0), sticky="w")

        self.open_btn = ctk.CTkButton(
            btn_frame,
            text="📂 Open Output",
            height=44,
            width=130,
            fg_color="#2a5c45",
            hover_color="#1e4433",
            command=self._open_output_folder,
            state="disabled",
        )
        self.open_btn.grid(row=0, column=2, padx=(10, 0), sticky="w")

        self.status_label = ctk.CTkLabel(
            btn_frame,
            text="Ready",
            font=ctk.CTkFont(size=12),
            text_color="gray60",
        )
        self.status_label.grid(row=0, column=3, padx=(16, 0), sticky="e")

    # ── Drag & drop ───────────────────────────────────────────────────────────
    def _setup_drag_drop(self):
        try:
            self.drop_target_register("*")
            self.dnd_bind("<<Drop>>", self._on_drop)
        except Exception:
            pass

    def _on_drop(self, event):
        path = event.data.strip().strip("{}")
        self.video_path.set(path)

    # ── File browsing ─────────────────────────────────────────────────────────
    def _browse_file(self):
        path = filedialog.askopenfilename(
            title="Select video or audio file",
            filetypes=[
                ("Media files", "*.mp4 *.mkv *.avi *.mov *.webm *.mp3 *.wav *.m4a *.flac *.ogg *.aac"),
                ("All files", "*.*"),
            ]
        )
        if path:
            self.video_path.set(path)

    def _browse_output(self):
        path = filedialog.askdirectory(title="Select output folder")
        if path:
            self.output_dir.set(path)

    def _open_output_folder(self):
        folder = self.output_dir.get() or str(Path(self.video_path.get()).parent)
        if os.path.isdir(folder):
            if sys.platform == "win32":
                os.startfile(folder)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", folder])
            else:
                subprocess.Popen(["xdg-open", folder])

    # ── Model Manager ────────────────────────────────────────────────────────
    def _build_model_manager_rows(self):
        mdir = models_dir()
        self.mm_folder_label.configure(text=f"📁 {mdir}")

        # Header row
        for col, txt in enumerate(["Model", "Size", "Status", "Action", ""]):
            ctk.CTkLabel(
                self.mm_rows_frame, text=txt,
                font=ctk.CTkFont(size=11), text_color="gray55"
            ).grid(row=0, column=col, sticky="w", padx=(0, 10), pady=(0, 4))

        for i, name in enumerate(WHISPER_MODELS, 1):
            size_mb = WHISPER_MODEL_SIZES[name]
            size_txt = f"{size_mb} MB" if size_mb < 1000 else f"{size_mb/1000:.1f} GB"

            ctk.CTkLabel(
                self.mm_rows_frame, text=name.capitalize(),
                font=ctk.CTkFont(size=13, weight="bold")
            ).grid(row=i, column=0, sticky="w", padx=(0, 10), pady=3)

            ctk.CTkLabel(
                self.mm_rows_frame, text=size_txt,
                font=ctk.CTkFont(size=12), text_color="gray60"
            ).grid(row=i, column=1, sticky="w", padx=(0, 10), pady=3)

            status_lbl = ctk.CTkLabel(
                self.mm_rows_frame, text="",
                font=ctk.CTkFont(size=12)
            )
            status_lbl.grid(row=i, column=2, sticky="w", padx=(0, 10), pady=3)

            btn = ctk.CTkButton(
                self.mm_rows_frame, text="", width=100, height=28,
                font=ctk.CTkFont(size=12),
            )
            btn.grid(row=i, column=3, sticky="w", padx=(0, 6), pady=3)

            del_btn = ctk.CTkButton(
                self.mm_rows_frame, text="🗑", width=34, height=28,
                font=ctk.CTkFont(size=12),
                fg_color="#5a1a1a", hover_color="#7a2a2a",
            )
            del_btn.grid(row=i, column=4, sticky="w", pady=3)

            self._mm_widgets[name] = {
                "status": status_lbl,
                "btn":    btn,
                "del":    del_btn,
            }

        self._refresh_model_manager()

    def _refresh_model_manager(self):
        for name in WHISPER_MODELS:
            cached  = model_is_cached(name)
            widgets = self._mm_widgets[name]

            if cached:
                widgets["status"].configure(text="✓ Downloaded", text_color="#4caf50")
                widgets["btn"].configure(
                    text="✓ Ready", fg_color="#2a5c45", hover_color="#2a5c45",
                    state="disabled", command=lambda: None
                )
                widgets["del"].configure(
                    state="normal",
                    command=lambda n=name: self._delete_model(n)
                )
            else:
                widgets["status"].configure(text="Not downloaded", text_color="gray55")
                widgets["btn"].configure(
                    text="⬇ Download", fg_color="#7c6fff", hover_color="#5c4fcc",
                    state="normal",
                    command=lambda n=name: self._download_model(n)
                )
                widgets["del"].configure(state="disabled", command=lambda: None)

    def _download_model(self, name):
        widgets = self._mm_widgets[name]
        widgets["btn"].configure(text="Downloading…", state="disabled", fg_color="#555")
        widgets["status"].configure(text="⬇ Downloading…", text_color="#e0a000")

        def do_download():
            try:
                import whisper
                mdir = models_dir()
                self._log(f"[Model] Downloading '{name}' → {mdir}")
                whisper.load_model(name, download_root=str(mdir))
                self._log(f"[Model] '{name}' saved to {mdir}")
            except Exception as e:
                self._log(f"[Model] Download failed: {e}")
            finally:
                self.after(0, self._refresh_model_manager)

        threading.Thread(target=do_download, daemon=True).start()

    def _delete_model(self, name):
        fname = WHISPER_MODEL_FILES.get(name)
        fpath = models_dir() / fname
        if fpath.exists():
            from tkinter import messagebox
            if messagebox.askyesno("Delete model", f"Delete '{name}' model ({fpath.name})?"):
                fpath.unlink()
                self._log(f"[Model] Deleted {fpath}")
                self._refresh_model_manager()

    # ── Dependency check ──────────────────────────────────────────────────────
    def _check_dependencies(self):
        parts = []
        if self._whisper_ok:
            parts.append("✓ Whisper")
        else:
            parts.append("✗ Whisper (not installed)")
        if self._ffmpeg_ok:
            parts.append("✓ FFmpeg")
        else:
            parts.append("⚠ FFmpeg (not found)")
        self.dep_label.configure(
            text="  |  ".join(parts),
            text_color="gray60",
        )

    # ── Logging helpers ───────────────────────────────────────────────────────
    def _log(self, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

    def _set_status(self, text, color="gray60"):
        self.status_label.configure(text=text, text_color=color)

    # ── Main generation flow ──────────────────────────────────────────────────
    def _start_generation(self):
        video = self.video_path.get().strip()
        if not video or not os.path.isfile(video):
            messagebox.showerror("No file", "Please select a valid video or audio file.")
            return
        if not self._whisper_ok:
            messagebox.showerror(
                "Whisper not installed",
                "Run:\n  pip install openai-whisper\n\nThen restart the app."
            )
            return

        self._is_running  = True
        self._cancel_flag = False
        self._segments    = []
        self._clear_log()
        self.progress_var.set(0)

        self.run_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.open_btn.configure(state="disabled")
        self._set_status("Running…", "#7c6fff")

        thread = threading.Thread(target=self._run_pipeline, daemon=True)
        thread.start()

    def _cancel(self):
        self._cancel_flag = True
        self._log("⚠ Cancellation requested…")
        self._set_status("Cancelling…", "#e0a000")

    def _finish(self, success=True, message="Done"):
        self._is_running = False
        self.run_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        if success:
            self.open_btn.configure(state="normal")
            self._set_status(message, "#4caf50")
            self.progress_var.set(1.0)
        else:
            self._set_status(message, "#f44336")

    # ── Pipeline (runs in thread) ─────────────────────────────────────────────
    def _run_pipeline(self):
        try:
            import whisper

            video      = self.video_path.get().strip()
            model_name = self.model_var.get()
            lang_name  = self.language_var.get()
            language   = LANGUAGES[lang_name]
            fmt        = self.format_var.get()
            task       = "translate" if "translate" in self.task_var.get() else "transcribe"
            burn       = self.burn_var.get()

            out_dir = self.output_dir.get().strip() or str(Path(video).parent)
            stem    = Path(video).stem

            # ── Step 1: Load model ──
            self._log(f"[1/3] Loading Whisper model '{model_name}'…")
            self._set_status(f"Loading model '{model_name}'…", "#7c6fff")
            self.progress_var.set(0.05)

            mdir = models_dir()
            if model_is_cached(model_name):
                self._log(f"      Using cached model from: {mdir}")
            else:
                self._log(f"      Downloading model to: {mdir} (one-time only)")
            model = whisper.load_model(model_name, download_root=str(mdir))

            if self._cancel_flag:
                self.after(0, self._finish, False, "Cancelled")
                return

            # ── Step 2: Transcribe ──
            self._log(f"[2/3] Transcribing '{Path(video).name}'…")
            if language:
                self._log(f"      Language: {lang_name}  |  Task: {task}")
            else:
                self._log(f"      Language: auto-detect  |  Task: {task}")
            self.progress_var.set(0.15)
            self._set_status("Transcribing (this may take a while)…", "#7c6fff")

            result = model.transcribe(
                video,
                language=language,
                task=task,
                verbose=False,
            )

            if self._cancel_flag:
                self.after(0, self._finish, False, "Cancelled")
                return

            self._segments = result["segments"]
            detected_lang  = result.get("language", "unknown")
            self._log(f"      Detected language: {detected_lang}")
            self._log(f"      Segments: {len(self._segments)}")
            self.progress_var.set(0.65)

            # ── Step 3: Write subtitle file ──
            self._log(f"[3/3] Writing subtitle file (.{fmt})…")
            self._set_status(f"Writing .{fmt}…", "#7c6fff")

            out_file = os.path.join(out_dir, f"{stem}.{fmt}")

            if fmt == "srt":
                content = segments_to_srt(self._segments)
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(content)

            elif fmt == "vtt":
                content = segments_to_vtt(self._segments)
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(content)

            elif fmt == "txt":
                content = result["text"]
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(content)

            elif fmt == "json":
                with open(out_file, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)

            elif fmt == "tsv":
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write("start\tend\ttext\n")
                    for seg in self._segments:
                        f.write(f"{seg['start']:.3f}\t{seg['end']:.3f}\t{seg['text'].strip()}\n")

            self._log(f"      Saved: {out_file}")
            self.progress_var.set(0.85)

            # ── Step 4: Burn-in (optional) ──
            if burn and self._ffmpeg_ok:
                if fmt not in ("srt",):
                    # need SRT for burn-in; write a temp one
                    srt_tmp = os.path.join(out_dir, f"{stem}_tmp.srt")
                    with open(srt_tmp, "w", encoding="utf-8") as f:
                        f.write(segments_to_srt(self._segments))
                    srt_for_burn = srt_tmp
                else:
                    srt_for_burn = out_file

                burned_out = os.path.join(out_dir, f"{stem}_subtitled.mp4")
                self._log(f"[4/4] Burning subtitles into video…")
                self._set_status("Burning subtitles (FFmpeg)…", "#7c6fff")

                # Escape path for ffmpeg filter
                srt_escaped = srt_for_burn.replace("\\", "/").replace(":", "\\:")
                cmd = [
                    ffmpeg_path(),
                    "-y",
                    "-i", video,
                    "-vf", f"subtitles='{srt_escaped}'",
                    "-c:a", "copy",
                    burned_out,
                ]
                proc = subprocess.run(cmd, capture_output=True, text=True)
                if proc.returncode == 0:
                    self._log(f"      Burned video: {burned_out}")
                else:
                    self._log(f"      FFmpeg error: {proc.stderr[-300:]}")

                if fmt not in ("srt",) and os.path.exists(srt_tmp):
                    os.remove(srt_tmp)

            self.progress_var.set(1.0)
            self._log("─" * 50)
            self._log("✓ All done!")
            self.after(0, self._finish, True, "✓ Done")

        except Exception as e:
            self._log(f"✗ Error: {e}")
            import traceback
            self._log(traceback.format_exc())
            self.after(0, self._finish, False, f"Error: {e}")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = SubScribeApp()
    app.mainloop()