from tempfile import mkdtemp
import yt_dlp
from glob import glob
import os


def download_video(url):
    print("Downloading video...")
    temp_dir = mkdtemp(prefix="vk-tg-bot-yt-dlp-")
    ydl_opts = {
        "quiet": True,
        "color": "never",
        "format": "best",
        # this requires ffmpeg cuz + means downloading separate streams and
        # then merging
        # "format": "bestvideo*+bestaudio/best",
        "paths": {"home": temp_dir},
        # selecting smallest file size
        # "format_sort": ["+size", "+br", "+res", "+fps"],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)
        # hack: getting first file in temp directory. We are assuming yt-dlp
        # results in downloading only one file
        result_file_path = glob(temp_dir + "/*")[0]
        return result_file_path
    except Exception as e:
        print("Error during yt-dlp video downloading", e)
        return None


def cleanup_temp_dir_video(file_path):
    os.remove(file_path)
    tmp_dir = os.path.dirname(file_path)
    os.rmdir(tmp_dir)
