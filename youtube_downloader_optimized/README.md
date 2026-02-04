# YouTube to USB Downloader

A simple, cross-platform GUI application to download YouTube videos directly to USB drives.

## Features

- 🎥 Download videos from YouTube
- 💾 Direct save to USB drives
- 🖥️ Cross-platform (Windows, Mac, Linux)
- 📊 Real-time download progress
- ⚡ Optimized for speed with concurrent downloads
- 🔍 Automatic USB drive detection

## Quick Start

### Download Pre-built Executable
1. Go to the [Releases](../../releases) page
2. Download for your platform:
   - Windows: `YouTubeDownloader-Windows.exe`
   - macOS: `YouTubeDownloader-macOS`
   - Linux: `YouTubeDownloader-Linux`
3. Run the executable

### Run from Source
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python youtube_downloader_optimized.py
```

## Building Executables

### Simple Build (All Platforms)
```bash
python build_executable.py
```

### Using Spec File (Advanced)
```bash
pyinstaller YouTubeDownloader.spec
```

See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) for detailed instructions.

## Usage

1. **Insert USB drive** into your computer
2. **Click "Refresh USB Drives"** to detect available drives
3. **Paste YouTube URL** into the text field
4. **Select USB drive** from the dropdown
5. **Click "Download"** and wait for completion

## Requirements

- Python 3.8+
- Internet connection
- USB drive with write permissions

## Dependencies

- `yt-dlp` - YouTube video downloader
- `psutil` - System utilities for drive detection
- `tkinter` - GUI framework (included with Python)

## Troubleshooting

### No USB drives detected
- Ensure USB drive is properly connected
- Check if drive is mounted/formatted
- Click "Refresh USB Drives" button

### Permission errors
- Run as administrator (Windows)
- Check USB drive permissions
- Ensure drive is not write-protected

### Download fails
- Verify YouTube URL is valid
- Check internet connection
- Ensure sufficient space on USB drive

## License

This project is provided as-is for personal use.

## Disclaimer

Please respect YouTube's Terms of Service and copyright laws when downloading videos.
