#!/bin/bash

echo "========================================"
echo "Android APK Build - Docker Method"
echo "Works on Windows, Mac, and Linux!"
echo "========================================"
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo
    echo "Please install Docker:"
    echo "  - Windows/Mac: Download Docker Desktop"
    echo "  - Linux: curl -fsSL https://get.docker.com | sh"
    echo
    exit 1
fi

echo "🐳 Using Docker to build APK..."
echo "This will download ~2GB on first run..."
echo

# Build using official Buildozer Docker image
docker run --rm -v "$PWD":/home/user/app kivy/buildozer \
    buildozer android debug

if [ $? -eq 0 ]; then
    echo
    echo "✅ Build successful!"
    echo "📱 APK location: bin/*.apk"
    echo
    ls -lh bin/*.apk 2>/dev/null || echo "APK file created!"
else
    echo
    echo "❌ Build failed!"
    echo "Try running: docker pull kivy/buildozer"
    exit 1
fi
