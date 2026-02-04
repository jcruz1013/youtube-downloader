"""
YouTube Downloader - Android Version
Built with Kivy for Android APK compilation
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.utils import platform
import threading
import os

# Android-specific imports
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
    request_permissions([
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.INTERNET
    ])

import yt_dlp


class YouTubeDownloaderApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_downloading = False
        self.download_paths = []
        
    def build(self):
        self.title = "YouTube Downloader"
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='YouTube to Storage Downloader',
            size_hint=(1, 0.1),
            font_size='20sp',
            bold=True
        )
        layout.add_widget(title)
        
        # URL Input
        url_label = Label(text='YouTube URL:', size_hint=(1, 0.08))
        layout.add_widget(url_label)
        
        self.url_input = TextInput(
            hint_text='Paste YouTube URL here',
            multiline=False,
            size_hint=(1, 0.1),
            font_size='16sp'
        )
        layout.add_widget(self.url_input)
        
        # Storage location spinner
        storage_label = Label(text='Save Location:', size_hint=(1, 0.08))
        layout.add_widget(storage_label)
        
        self.storage_spinner = Spinner(
            text='Select Storage',
            values=self.get_storage_locations(),
            size_hint=(1, 0.1),
            font_size='16sp'
        )
        layout.add_widget(self.storage_spinner)
        
        # Refresh button
        refresh_btn = Button(
            text='Refresh Storage',
            size_hint=(1, 0.1),
            on_press=self.refresh_storage
        )
        layout.add_widget(refresh_btn)
        
        # Download button
        self.download_btn = Button(
            text='Download',
            size_hint=(1, 0.12),
            background_color=(0.2, 0.6, 1, 1),
            on_press=self.start_download
        )
        layout.add_widget(self.download_btn)
        
        # Status label
        self.status_label = Label(
            text='Status: Ready',
            size_hint=(1, 0.1),
            color=(0.2, 0.6, 1, 1)
        )
        layout.add_widget(self.status_label)
        
        # Progress bar
        self.progress_bar = ProgressBar(
            max=100,
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.progress_bar)
        
        # Info label
        info = Label(
            text='Download videos to your device storage',
            size_hint=(1, 0.1),
            font_size='12sp',
            color=(0.5, 0.5, 0.5, 1)
        )
        layout.add_widget(info)
        
        return layout
    
    def get_storage_locations(self):
        """Get available storage locations on Android."""
        locations = []
        
        if platform == 'android':
            try:
                # Primary external storage (internal storage on most devices)
                primary = primary_external_storage_path()
                downloads = os.path.join(primary, 'Download')
                movies = os.path.join(primary, 'Movies')
                dcim = os.path.join(primary, 'DCIM')
                
                if os.path.exists(downloads):
                    locations.append(downloads)
                if os.path.exists(movies):
                    locations.append(movies)
                if os.path.exists(dcim):
                    locations.append(dcim)
                    
                # Add primary storage root
                locations.append(primary)
            except Exception as e:
                locations.append('/storage/emulated/0/Download')
        else:
            # For desktop testing
            locations = [os.path.expanduser('~/Downloads')]
        
        self.download_paths = locations
        return locations if locations else ['No storage found']
    
    def refresh_storage(self, instance):
        """Refresh available storage locations."""
        locations = self.get_storage_locations()
        self.storage_spinner.values = locations
        if locations and locations[0] != 'No storage found':
            self.storage_spinner.text = locations[0]
            self.update_status('Storage refreshed', (0, 1, 0, 1))
        else:
            self.update_status('No storage found', (1, 0, 0, 1))
    
    def update_status(self, message, color=(0.2, 0.6, 1, 1)):
        """Update status label thread-safely."""
        def update(dt):
            self.status_label.text = f'Status: {message}'
            self.status_label.color = color
        Clock.schedule_once(update)
    
    def update_progress(self, value):
        """Update progress bar thread-safely."""
        def update(dt):
            self.progress_bar.value = value
        Clock.schedule_once(update)
    
    def progress_hook(self, d):
        """Handle download progress updates."""
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            
            if total and total > 0:
                progress = (downloaded / total) * 100
                self.update_progress(progress)
                
                speed = d.get('speed', 0)
                if speed:
                    speed_mb = speed / (1024 * 1024)
                    self.update_status(f'Downloading... {progress:.1f}% ({speed_mb:.2f} MB/s)')
                else:
                    self.update_status(f'Downloading... {progress:.1f}%')
                    
        elif d['status'] == 'finished':
            self.update_status('Processing...', (0.2, 0.6, 1, 1))
    
    def download_video(self, url, output_path):
        """Download video in background thread."""
        try:
            ydl_opts = {
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'format': 'best[ext=mp4]/best',  # Android-optimized format
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self.progress_hook],
            }
            
            self.update_status(f'Starting download...')
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.update_status('Download completed!', (0, 1, 0, 1))
            self.update_progress(100)
            
        except Exception as e:
            error_msg = str(e).split('\n')[0]
            self.update_status(f'Error: {error_msg}', (1, 0, 0, 1))
            
        finally:
            self.is_downloading = False
            def enable_btn(dt):
                self.download_btn.disabled = False
                self.download_btn.text = 'Download'
            Clock.schedule_once(enable_btn)
            
            # Reset progress after 3 seconds
            def reset_progress(dt):
                self.update_progress(0)
            Clock.schedule_once(reset_progress, 3)
    
    def start_download(self, instance):
        """Validate inputs and start download."""
        if self.is_downloading:
            self.update_status('Download in progress...', (1, 0.5, 0, 1))
            return
        
        url = self.url_input.text.strip()
        if not url:
            self.update_status('Please enter a URL', (1, 0, 0, 1))
            return
        
        # Basic URL validation
        if not any(domain in url.lower() for domain in ['youtube.com', 'youtu.be']):
            self.update_status('Invalid YouTube URL', (1, 0, 0, 1))
            return
        
        storage_path = self.storage_spinner.text
        if storage_path == 'Select Storage' or storage_path == 'No storage found':
            self.update_status('Please select storage location', (1, 0, 0, 1))
            return
        
        # Check write permissions
        if not os.access(storage_path, os.W_OK):
            self.update_status('No write permission', (1, 0, 0, 1))
            return
        
        # Start download
        self.is_downloading = True
        self.download_btn.disabled = True
        self.download_btn.text = 'Downloading...'
        
        thread = threading.Thread(
            target=self.download_video,
            args=(url, storage_path),
            daemon=True
        )
        thread.start()


if __name__ == '__main__':
    YouTubeDownloaderApp().run()
