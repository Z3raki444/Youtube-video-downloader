import tkinter as tk
from tkinter import messagebox, filedialog
import yt_dlp
import os

def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', d.get('total_bytes_estimate', 1))
        percent = downloaded / total * 100
        status_label.config(text=f"Downloading... {percent:.2f}% completed")
        root.update()
    elif d['status'] == 'finished':
        status_label.config(text=f"Download complete: {d['filename']}")
        root.update()
        messagebox.showinfo("Success", f"Download complete:\n{d['filename']}")

def download_video():
    url = url_entry.get().strip()
    save_path = save_entry.get().strip()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return
    if not save_path:
        messagebox.showerror("Error", "Please select a download folder.")
        return

    audio_only = option_var.get() == "Audio"

    ydl_opts = {
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
    }

    if audio_only:
        # Audio-only download
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        # Video + audio download (requires FFmpeg)
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['merge_output_format'] = 'mp4'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        messagebox.showerror("Error", f"Download failed:\n{e}")

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        save_entry.delete(0, tk.END)
        save_entry.insert(0, folder)

# ----------------- GUI -----------------
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("500x250")

tk.Label(root, text="YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

tk.Label(root, text="Save Folder:").pack(pady=5)
save_frame = tk.Frame(root)
save_frame.pack(pady=5)
save_entry = tk.Entry(save_frame, width=45)
save_entry.pack(side=tk.LEFT, padx=5)
browse_btn = tk.Button(save_frame, text="Browse", command=browse_folder)
browse_btn.pack(side=tk.LEFT)

tk.Label(root, text="Download Option:").pack(pady=5)
option_var = tk.StringVar(value="Video")
video_radio = tk.Radiobutton(root, text="Video", variable=option_var, value="Video")
audio_radio = tk.Radiobutton(root, text="Audio-only", variable=option_var, value="Audio")
video_radio.pack()
audio_radio.pack()

download_btn = tk.Button(root, text="Download", command=download_video, bg="green", fg="white")
download_btn.pack(pady=10)

status_label = tk.Label(root, text="", fg="blue")
status_label.pack(pady=5)

root.mainloop()
