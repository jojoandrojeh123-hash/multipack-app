# ⬡ SubScribe — Local AI Subtitle Generator

> Generate subtitles from any video or audio file — 100% offline, no API key, no subscription. Powered by OpenAI Whisper running entirely on your machine.

**Part of:** [Multipack App](https://github.com/jojoandrojeh123-hash/multipack-app)  
**Developer:** [jojoandrojeh123-hash](https://github.com/jojoandrojeh123-hash) · [Jonathan1005Magdy](https://github.com/Jonathan1005Magdy)  
**Platform:** Windows 10 / 11 (64-bit)  
**License:** MIT

---

## ⬇️ Download

| Version | Contents | Size |
|---------|----------|------|
| [SubScribe (No Models)](https://your-netlify-url.netlify.app) | App only — download models inside the app | ~120 MB |
| [SubScribe (Tiny + Base)](https://your-netlify-url.netlify.app) | App + tiny.pt + base.pt ready to use | ~410 MB |

> **Not sure which to pick?** Download the Tiny + Base version — it works out of the box with no extra steps.

---

## ✨ Features

- **100% Offline** — Whisper runs on your CPU/GPU, nothing is sent to any server
- **5 model sizes** — from tiny (fast, 75MB) to large (most accurate, 3GB)
- **14 languages** — or auto-detect from audio
- **Translate mode** — transcribe any language and output English subtitles
- **Multiple export formats** — `.srt`, `.vtt`, `.txt`, `.json`, `.tsv`
- **Burn-in subtitles** — bake captions permanently into video via FFmpeg
- **Built-in Model Manager** — download, switch, or delete models from inside the app
- **Models saved locally** — stored in `models/` next to the app, not hidden in system folders
- **Non-blocking UI** — transcription runs in background, UI never freezes

---

## 🚀 Getting Started

### 1. Download and extract

Download the ZIP from the link above and extract it. Keep the folder structure intact:

```
SubScribe/
├── SubScribe.exe       ← launch this
├── models/             ← AI models stored here
│   ├── tiny.pt         ← (included in the Tiny+Base version)
│   └── base.pt         ← (included in the Tiny+Base version)
└── ffmpeg/
    └── ffmpeg.exe      ← bundled, no install needed
```

### 2. Run SubScribe.exe

Double-click `SubScribe.exe` to launch.

> **Windows SmartScreen warning?** Click **"More info"** → **"Run anyway"**. This appears because the app isn't code-signed, not because it's harmful.

### 3. Download a model (if needed)

If you downloaded the No Models version, open the **Model Manager** panel at the bottom of the app and click **⬇ Download** next to your preferred model.

### 4. Select a file and generate

1. Click **Browse** and select your video or audio file
2. Choose your language and output format
3. Click **▶ Generate Subtitles**
4. Find your subtitle file in the same folder as the video

---

## 🎛️ Model Guide

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| tiny | ~75 MB | Very fast | Basic | Quick drafts, clear speech |
| base | ~145 MB | Fast | Good | **Recommended starting point** |
| small | ~460 MB | Moderate | Great | Better accuracy, still fast |
| medium | ~1.5 GB | Slow | Excellent | High-quality transcription |
| large | ~3 GB | Very slow | Best | Professional results, GPU recommended |

> **Tip:** Start with `base`. Only go larger if you need better accuracy on noisy or accented audio.

---

## 📤 Output Formats

| Format | Use Case |
|--------|----------|
| `.srt` | Standard subtitles — works in VLC, MPC-HC, video editors |
| `.vtt` | Web subtitles — YouTube, HTML5 video players |
| `.txt` | Plain transcript — copy into documents |
| `.json` | Full data with timestamps — for developers |
| `.tsv` | Spreadsheet-friendly — open in Excel |

---

## 🔥 Burn-in Subtitles

Enable the **"Burn subtitles into video"** checkbox before generating. SubScribe will use the bundled FFmpeg to render the subtitles permanently into the video, creating a new file called `filename_subtitled.mp4`.

---

## 💻 System Requirements

| Requirement | Minimum |
|-------------|---------|
| OS | Windows 10 / 11 (64-bit) |
| RAM | 4 GB (8 GB for medium/large models) |
| Disk | 120 MB + model size |
| GPU | Optional — NVIDIA CUDA speeds up large models significantly |
| Internet | Only needed to download models |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| UI | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) |
| AI transcription | [OpenAI Whisper](https://github.com/openai/whisper) |
| Media processing | [FFmpeg](https://ffmpeg.org) |
| Packaging | [PyInstaller](https://pyinstaller.org) |
| Icon | Generated with [Google Gemini](https://gemini.google.com) |

---

## 📄 License

MIT — free to use, modify, and distribute.

---

*Part of [Multipack App](https://github.com/jojoandrojeh123-hash/multipack-app) · Made by [jojoandrojeh123-hash](https://github.com/jojoandrojeh123-hash) · [Jonathan1005Magdy](https://github.com/Jonathan1005Magdy)*
