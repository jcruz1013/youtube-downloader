#!/bin/bash

echo "========================================"
echo "YouTube Downloader - Quick Build"
echo "========================================"
echo

echo "Installing dependencies..."
pip3 install -r requirements.txt

echo
echo "Building executable..."
python3 build_executable.py

echo
echo "Done! Check the dist folder for YouTubeDownloader"
echo "Run: chmod +x dist/YouTubeDownloader"
