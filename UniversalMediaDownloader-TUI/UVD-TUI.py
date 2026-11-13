import yt_dlp
import time
#from tqdm import tqdm

#def loading(download_speed):
#    for i in tqdm(range(1000), desc="Loading"):
#        time.sleep(download_speed)


url = input("Enter url ex: youtube, facebook, instagram, tiktok: ")

ydl_opts = {
    "format": "bestvideo+bestaudio/best",  # Downloads highest quality video and audio
    "outtmpl": "%(title)s.%(ext)s",        # Names the file after the video title
    "merge_output_format": "mp4",
    "cookiefile": "cookies.txt",          # Merges streams into an MP4 container
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
