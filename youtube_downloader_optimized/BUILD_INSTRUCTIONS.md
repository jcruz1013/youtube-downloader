# Building Executables for All Platforms

## Quick Start

### Prerequisites
All platforms need Python 3.8+ installed.

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Build Executable
```bash
python build_executable.py
```

The executable will be created in the `dist/` folder.

---

## Platform-Specific Instructions

### Windows

**Requirements:**
- Python 3.8 or higher
- Windows 10 or higher

**Build Steps:**
1. Open Command Prompt or PowerShell
2. Navigate to the project folder
3. Run:
   ```cmd
   pip install -r requirements.txt
   python build_executable.py
   ```
4. Find executable: `dist\YouTubeDownloader.exe`

**Manual PyInstaller Command:**
```cmd
pyinstaller --onefile --windowed --name=YouTubeDownloader youtube_downloader_optimized.py
```

---

### macOS

**Requirements:**
- Python 3.8 or higher
- macOS 10.13 (High Sierra) or higher

**Build Steps:**
1. Open Terminal
2. Navigate to the project folder
3. Run:
   ```bash
   pip3 install -r requirements.txt
   python3 build_executable.py
   ```
4. Find executable: `dist/YouTubeDownloader`

**Manual PyInstaller Command:**
```bash
pyinstaller --onefile --windowed --name=YouTubeDownloader youtube_downloader_optimized.py
```

**Note:** First run may show security warning. Go to System Preferences > Security & Privacy to allow.

---

### Linux

**Requirements:**
- Python 3.8 or higher
- Ubuntu/Debian: `sudo apt install python3-tk`
- Fedora/RHEL: `sudo dnf install python3-tkinter`

**Build Steps:**
1. Open Terminal
2. Navigate to the project folder
3. Run:
   ```bash
   pip3 install -r requirements.txt
   python3 build_executable.py
   ```
4. Find executable: `dist/YouTubeDownloader`
5. Make executable: `chmod +x dist/YouTubeDownloader`

**Manual PyInstaller Command:**
```bash
pyinstaller --onefile --windowed --name=YouTubeDownloader youtube_downloader_optimized.py
```

---

## Advanced: Build with Custom Icon

### Create builds with custom icon:

**Windows:**
```cmd
pyinstaller --onefile --windowed --name=YouTubeDownloader --icon=icon.ico youtube_downloader_optimized.py
```

**macOS:**
```bash
pyinstaller --onefile --windowed --name=YouTubeDownloader --icon=icon.icns youtube_downloader_optimized.py
```

**Linux:**
```bash
pyinstaller --onefile --windowed --name=YouTubeDownloader --icon=icon.png youtube_downloader_optimized.py
```

---

## Troubleshooting

### "Permission Denied" Error (Linux/Mac)
```bash
chmod +x dist/YouTubeDownloader
```

### "Cannot be opened because developer cannot be verified" (macOS)
Right-click the app → Open → Click "Open"

Or disable Gatekeeper temporarily:
```bash
sudo spctl --master-disable
```

### Missing tkinter (Linux)
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### Antivirus False Positive (Windows)
Add exception for `dist/YouTubeDownloader.exe` in Windows Defender

---

## Distribution

### File Sizes (approximate)
- Windows: 25-30 MB
- macOS: 20-25 MB
- Linux: 20-25 MB

### What to Distribute
Share only the executable from the `dist/` folder:
- Windows: `YouTubeDownloader.exe`
- macOS: `YouTubeDownloader`
- Linux: `YouTubeDownloader`

No additional files needed - everything is bundled!

---

## Building for Distribution on All Platforms

**Best Practice:** Build on each target platform for best compatibility.

### Cross-Platform Build Setup
1. **Windows PC** → Build Windows .exe
2. **Mac** → Build macOS app
3. **Linux VM/PC** → Build Linux executable

**Alternative:** Use GitHub Actions or CI/CD for automated multi-platform builds.
