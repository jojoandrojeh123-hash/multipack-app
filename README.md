# 📥 Universal Media Downloader

> Download videos and audio from YouTube, Facebook, Instagram, TikTok, Twitter and 1000+ other sites — with a clean desktop GUI, no terminal needed.

**Part of:** [Multipack App](https://github.com/jojoandrojeh123-hash/multipack-app)  
**Developer:** [jojoandrojeh123-hash](https://github.com/jojoandrojeh123-hash) · [Jonathan1005Magdy](https://github.com/Jonathan1005Magdy)  
**Platform:** Windows 10 / 11 (64-bit)  
**License:** MIT

---

## ⬇️ Download

| Version | Size |
|---------|------|
| [Universal Media Downloader.exe](https://your-netlify-url.netlify.app) | ~35 MB |

> Just download and run — no Python, no pip, no terminal required.

---

## ✨ Features

- **1000+ supported sites** — YouTube, Facebook, Instagram, TikTok, Twitter, Twitch, SoundCloud and more via yt-dlp
- **3 quality modes** — Highest quality, Standard (720p), MP3 audio only
- **Playlist support** — detects playlist URLs and auto-numbers files
- **FFmpeg bundled** — no separate install needed for stream merging
- **Chakra JS engine** — bypasses YouTube's JS signature protection
- **MP3 extraction** — exports audio at 192kbps
- **Real-time progress** — live speed and ETA display during download
- **Folder picker** — choose exactly where files are saved each time
- **Non-blocking UI** — downloads run in background, UI stays responsive

---

## 🚀 Getting Started

### 1. Download the app

Download `UniversalMediaDownloader.exe` from the link above.

### 2. Run it

Double-click the `.exe` to launch. No installation needed.

> **Windows SmartScreen warning?** Click **"More info"** → **"Run anyway"**. This appears because the app isn't code-signed, not because it's harmful.

### 3. Paste a URL and download

1. Copy any video or playlist URL
2. Paste it into the URL field
3. Select your preferred quality
4. Click **Download Media**
5. Choose your save folder when prompted

---

## 🌐 Supported Sites

Any site supported by `yt-dlp` works — here are the most popular:

| Site | Videos | Playlists | Audio |
|------|--------|-----------|-------|
| YouTube | ✅ | ✅ | ✅ |
| Instagram | ✅ | ✅ | ✅ |
| TikTok | ✅ | ✅ | ✅ |
| Facebook | ✅ | — | ✅ |
| Twitter / X | ✅ | — | ✅ |
| Twitch | ✅ | — | ✅ |
| SoundCloud | ✅ | ✅ | ✅ |
| Vimeo | ✅ | ✅ | ✅ |
| Reddit | ✅ | — | ✅ |
| 1000+ more | ✅ | varies | ✅ |

---

## 🎛️ Quality Options

| Option | What it downloads |
|--------|-------------------|
| **Highest Quality Video** | Best video + best audio merged via FFmpeg |
| **Standard Quality (Faster)** | Up to 720p — smaller file, faster download |
| **MP3 Audio Only** | Extracts audio as 192kbps MP3 |

---

## 📁 Output File Naming

| URL type | Filename format |
|----------|----------------|
| Single video | `Video Title.mp4` |
| Playlist | `01 - Video Title.mp4`, `02 - Video Title.mp4`, ... |

---

## 💻 System Requirements

| Requirement | Minimum |
|-------------|---------|
| OS | Windows 10 / 11 (64-bit) |
| RAM | 2 GB |
| Disk | ~50 MB for the app + space for downloaded files |
| Internet | Required for downloading media |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| UI | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) |
| Download engine | [yt-dlp](https://github.com/yt-dlp/yt-dlp) |
| Media processing | [FFmpeg](https://ffmpeg.org) |
| JS bypass | Chakra JS engine |
| Packaging | [PyInstaller](https://pyinstaller.org) |
| Icon | Generated with [Google Gemini](https://gemini.google.com) |

---

## ⚠️ Legal Notice

This tool is intended for downloading content you have the right to download — such as your own uploads, Creative Commons content, or content explicitly permitted for download. Respect copyright law and the terms of service of each platform.

---

## 📄 License

MIT — free to use, modify, and distribute.

---

*Part of [Multipack App](https://github.com/jojoandrojeh123-hash/multipack-app) · Made by [jojoandrojeh123-hash](https://github.com/jojoandrojeh123-hash) · [Jonathan1005Magdy](https://github.com/Jonathan1005Magdy)*
