@echo off
echo ========================================
echo YouTube Downloader - Quick Build
echo ========================================
echo.

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Building executable...
python build_executable.py

echo.
echo Done! Check the dist folder for YouTubeDownloader.exe
pause
