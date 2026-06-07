import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from yt_dlp import YoutubeDL
import threading
import os
import sys

# Set the theme and color options
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue") 

class UniversalDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Rebranded Application Metadata
        self.title("Universal Media Downloader")
        self.geometry("550x430")  # Tallied up slightly to cleanly fit credits
        self.resizable(False, False)

        # Dynamically set the Window Icon at Runtime
        try:
            icon_path = self.get_resource_path("icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Icon loading skipped: {e}")

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Universal Media Downloader", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.pack(padx=20, pady=(20, 5))

        # Project Credits Subtitle
        self.credits_label = ctk.CTkLabel(
            self, 
            text="Powered by yt-dlp  |  Developed by jojoandrojeh123-hash", 
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="gray"
        )
        self.credits_label.pack(pady=(0, 15))

        # URL Input Section
        self.url_label = ctk.CTkLabel(self, text="Paste Media URL (YouTube, Facebook, Instagram, TikTok...):")
        self.url_label.pack(anchor="w", padx=40, pady=(5, 2))
        
        self.url_entry = ctk.CTkEntry(self, width=470, placeholder_text="Paste link here...")
        self.url_entry.pack(padx=40, pady=(0, 15))

        # Format Selection Dropdown
        self.format_label = ctk.CTkLabel(self, text="Select Download Quality:")
        self.format_label.pack(anchor="w", padx=40, pady=(0, 2))
        
        self.format_options = ["Highest Quality Video", "Standard Quality (Faster)", "MP3 Audio Only"]
        self.format_var = tk.StringVar(value=self.format_options[0])
        self.format_dropdown = ctk.CTkOptionMenu(self, values=self.format_options, variable=self.format_var, width=220)
        self.format_dropdown.pack(anchor="w", padx=40, pady=(0, 20))

        # Download Button
        self.download_btn = ctk.CTkButton(self, text="Download Media", command=self.start_download_thread, font=ctk.CTkFont(weight="bold"))
        self.download_btn.pack(pady=5)

        # Progress Status
        self.status_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.status_label.pack(pady=(5, 2))

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self, width=470)
        self.progress_bar.set(0)
        self.progress_bar.pack(padx=40, pady=5)

    def get_resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(base_path, relative_path)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)
            
            if total_bytes:
                percentage = downloaded_bytes / total_bytes
                self.progress_bar.set(percentage)
                
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')
                self.status_label.configure(text=f"Downloading... Speed: {speed} | ETA: {eta}", text_color="white")
                
        elif d['status'] == 'finished':
            self.progress_bar.set(1.0)
            self.status_label.configure(text="Processing/Merging file streams...", text_color="yellow")

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            self.status_label.configure(text="Please enter a valid URL!", text_color="red")
            return

        self.download_btn.configure(state="disabled")
        self.status_label.configure(text="Choosing download folder...", text_color="white")

        output_dir = filedialog.askdirectory(title="Select Download Folder")
        if not output_dir:
            self.status_label.configure(text="Download canceled.", text_color="orange")
            self.download_btn.configure(state="normal")
            return

        threading.Thread(target=self.download_video, args=(url, output_dir), daemon=True).start()

    def download_video(self, url, output_dir):
        selected_format = self.format_var.get()
        bin_folder = self.get_resource_path("bin")
        
        output_template = os.path.join(
            output_dir, 
            '%(playlist_index)s - %(title)s.%(ext)s' if 'playlist' in url.lower() else '%(title)s.%(ext)s'
        )
        
        ydl_opts = {
            'progress_hooks': [self.progress_hook],
            'outtmpl': output_template,
            'ffmpeg_location': bin_folder,      
            'javascript_converter': 'chakra',   
            'ignoreerrors': True,
        }

        if selected_format == "Highest Quality Video":
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
        elif selected_format == "Standard Quality (Faster)":
            ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]/best'
        elif selected_format == "MP3 Audio Only":
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.configure(text="Download Complete! 🎉", text_color="green")
        except Exception as e:
            self.status_label.configure(text=f"Error: Download Failed", text_color="red")
            print(f"Detailed Error: {e}")
        finally:
            self.download_btn.configure(state="normal")

if __name__ == "__main__":
    app = UniversalDownloaderApp()
    app.mainloop()