# ⬡ Multipack App

> A collection of free, offline-first desktop tools for Windows — built with Python, CustomTkinter, and compiled to standalone `.exe` files. No installation, no subscriptions, no cloud.

**Live site:** [your-netlify-url.netlify.app](https://your-netlify-url.netlify.app)  
**GitHub:** [github.com/jojoandrojeh123-hash/multipack-app](https://github.com/jojoandrojeh123-hash/multipack-app)  
**Developer:** [jojoandrojeh123-hash](https://github.com/jojoandrojeh123-hash) · [Jonathan1005Magdy](https://github.com/Jonathan1005Magdy)

---

## 📦 Apps Included

| App | Description | Size |
|-----|-------------|------|
| [📥 Universal Media Downloader](#-universal-media-downloader) | Download from YouTube, TikTok, Instagram & 1000+ sites | ~35 MB |
| [⬡ SubScribe](#-subscribe) | Local AI subtitle generator using OpenAI Whisper | ~120 MB+ |

---

## 📥 Universal Media Downloader

Download videos and audio from over 1000 websites — YouTube, Facebook, Instagram, TikTok, Twitter and more. Supports playlist downloads, MP3 extraction, and quality selection.

**Key features:**
- Powered by `yt-dlp` — the most maintained downloader available
- FFmpeg bundled — no extra installs needed
- Chakra JS engine to bypass YouTube signature protection
- MP3 audio extraction at 192kbps
- Playlist support with auto-numbered filenames
- Real-time progress bar with speed and ETA

[→ Full README](./README_downloader.md)

---

## ⬡ SubScribe

Generate accurate subtitles from any video or audio file — fully offline, no API key, no internet connection required after model download. Powered by OpenAI Whisper running locally on your machine.

**Key features:**
- 5 model sizes from tiny (75MB) to large (3GB)
- Exports to `.srt`, `.vtt`, `.txt`, `.json`, `.tsv`
- Burn subtitles permanently into video via FFmpeg
- Translate any language to English in one step
- Built-in Model Manager — download/delete models from inside the app
- Models saved next to the app, not hidden in system folders

[→ Full README](./README_subscribe.md)

---

## 🛠️ Built With

- [Python 3.11](https://python.org)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — modern dark UI
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — media downloading engine
- [OpenAI Whisper](https://github.com/openai/whisper) — local AI transcription
- [FFmpeg](https://ffmpeg.org) — media processing
- [PyInstaller](https://pyinstaller.org) — compiled to `.exe`
- Icons generated with [Google Gemini](https://gemini.google.com)

---

## 📄 License

MIT — free to use, modify, and distribute.

---

*Made by [jojoandrojeh123-hash](https://github.com/jojoandrojeh123-hash) · [Jonathan1005Magdy](https://github.com/Jonathan1005Magdy)*
