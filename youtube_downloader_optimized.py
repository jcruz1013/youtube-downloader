import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp
import psutil
import os
import platform
import threading
from pathlib import Path
from typing import List, Optional

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube to USB Downloader")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        self.is_downloading = False
        self._setup_ui()
        self.refresh_usb_drives()

    def _setup_ui(self):
        """Initialize all UI components."""
        # URL Section
        tk.Label(self.root, text="YouTube URL:").pack(pady=5)
        self.url_entry = tk.Entry(self.root, width=60)
        self.url_entry.pack(pady=5)
        
        # USB Drive Section
        tk.Label(self.root, text="Detected USB Drives:").pack(pady=5)
        self.usb_combo = ttk.Combobox(self.root, width=57, state="readonly")
        self.usb_combo.pack(pady=5)
        
        # Buttons Frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Refresh USB Drives", 
                 command=self.refresh_usb_drives).pack(side=tk.LEFT, padx=5)
        self.download_btn = tk.Button(btn_frame, text="Download", 
                                      command=self.start_download)
        self.download_btn.pack(side=tk.LEFT, padx=5)
        
        # Status and Progress
        self.status_label = tk.Label(self.root, text="Status: Ready", fg="blue")
        self.status_label.pack(pady=5)
        
        self.progress = ttk.Progressbar(self.root, orient="horizontal", 
                                       length=400, mode="determinate")
        self.progress.pack(pady=10)

    def get_removable_drives(self) -> List[str]:
        """Detect removable drives cross-platform with caching."""
        drives = []
        system = platform.system().lower()
        
        try:
            partitions = psutil.disk_partitions(all=False)
        except Exception:
            return drives
        
        for partition in partitions:
            mountpoint = partition.mountpoint
            
            try:
                # Quick existence check
                if not Path(mountpoint).exists():
                    continue
                
                # Platform-specific detection
                if system == 'linux':
                    if any(opt in partition.opts.lower() for opt in ['removable', 'usb']) or \
                       partition.fstype.lower() in {'vfat', 'exfat', 'ntfs', 'fat32'}:
                        drives.append(mountpoint)
                        
                elif system == 'windows':
                    # Skip system drive and check accessibility
                    if mountpoint != 'C:\\' and partition.device.startswith(('D:', 'E:', 'F:', 'G:')):
                        if psutil.disk_usage(mountpoint).total > 0:
                            drives.append(mountpoint)
                            
                elif system == 'darwin':
                    if partition.fstype.lower() in {'msdos', 'exfat', 'ntfs'} and \
                       '/Volumes/' in mountpoint:
                        drives.append(mountpoint)
            except (PermissionError, OSError):
                continue
        
        return drives

    def refresh_usb_drives(self):
        """Refresh USB drive list in UI."""
        drives = self.get_removable_drives()
        
        if drives:
            self.usb_combo['values'] = drives
            self.usb_combo.current(0)
            self._update_status(f"{len(drives)} USB drive(s) detected", "green")
        else:
            self.usb_combo['values'] = []
            self._update_status("No USB drives detected", "orange")

    def _update_status(self, message: str, color: str = "blue"):
        """Update status label thread-safely."""
        self.status_label.config(text=f"Status: {message}", fg=color)
        self.root.update_idletasks()

    def progress_hook(self, d):
        """Handle download progress updates."""
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            
            if total and total > 0:
                progress = (downloaded / total) * 100
                self.progress['value'] = progress
                
                # Update status with download info
                speed = d.get('speed', 0)
                if speed:
                    speed_mb = speed / (1024 * 1024)
                    self._update_status(f"Downloading... {progress:.1f}% ({speed_mb:.2f} MB/s)")
                
        elif d['status'] == 'finished':
            self._update_status("Processing downloaded file...")

    def download_video(self, url: str, output_path: str):
        """Download video with optimized settings."""
        try:
            ydl_opts = {
                'outtmpl': str(Path(output_path) / '%(title)s.%(ext)s'),
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self.progress_hook],
                'concurrent_fragment_downloads': 4,  # Faster downloads
            }
            
            self._update_status(f"Starting download to {Path(output_path).name}...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self._update_status("Download completed!", "green")
            self.root.after(0, lambda: messagebox.showinfo("Success", 
                           "Video downloaded successfully!"))
            
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e).split('\n')[0]  # Get first line only
            self._update_status(f"Download error", "red")
            self.root.after(0, lambda: messagebox.showerror("Download Error", 
                           f"Failed to download video:\n{error_msg}"))
            
        except Exception as e:
            self._update_status(f"Error: {type(e).__name__}", "red")
            self.root.after(0, lambda: messagebox.showerror("Error", 
                           f"An error occurred:\n{str(e)}"))
        finally:
            self.progress['value'] = 0
            self.is_downloading = False
            self.download_btn.config(state=tk.NORMAL)

    def start_download(self):
        """Validate inputs and start download thread."""
        if self.is_downloading:
            messagebox.showwarning("Busy", "A download is already in progress.")
            return
        
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a YouTube URL.")
            return
        
        # Basic URL validation
        if not any(domain in url.lower() for domain in ['youtube.com', 'youtu.be']):
            messagebox.showwarning("Invalid URL", 
                                 "Please enter a valid YouTube URL.")
            return
        
        usb_path = self.usb_combo.get()
        if not usb_path:
            messagebox.showwarning("Selection Error", "Please select a USB drive.")
            return
        
        # Check write permissions
        if not os.access(usb_path, os.W_OK):
            messagebox.showerror("Permission Error", 
                               f"Cannot write to {usb_path}.\nCheck permissions.")
            return
        
        # Disable download button during download
        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED)
        
        # Start download in separate thread
        thread = threading.Thread(target=self.download_video, 
                                 args=(url, usb_path), daemon=True)
        thread.start()

def main():
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
