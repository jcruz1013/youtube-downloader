#!/usr/bin/env python3
"""
Build script for creating executables for Windows, Mac, and Linux
Run this on each platform to create the respective executable
"""

import subprocess
import sys
import platform

def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        print("✓ PyInstaller already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")

def build_executable():
    """Build the executable for the current platform."""
    system = platform.system()
    print(f"\nBuilding for {system}...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable
        "--windowed",  # No console window (GUI only)
        "--name=YouTubeDownloader",
        "--icon=NONE",  # Add icon file path if you have one
        "youtube_downloader_optimized.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print(f"\n✓ Build successful!")
        print(f"Executable location: dist/YouTubeDownloader{'.exe' if system == 'Windows' else ''}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 60)
    print("YouTube Downloader - Executable Builder")
    print("=" * 60)
    
    install_pyinstaller()
    build_executable()
    
    print("\nNote: Run this script on each platform to create executables:")
    print("  - Windows: Creates .exe file")
    print("  - Mac: Creates macOS app bundle")
    print("  - Linux: Creates Linux executable")
