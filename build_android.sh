#!/bin/bash

echo "========================================"
echo "YouTube Downloader - Android APK Build"
echo "========================================"
echo

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "⚠️  Warning: This script is designed for Linux"
    echo "For Windows/Mac, use Docker or GitHub Actions"
    echo
fi

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "📦 Installing Buildozer..."
    pip3 install --upgrade buildozer
    pip3 install --upgrade cython==0.29.33
fi

echo "🔨 Building Android APK..."
echo "This may take 30-60 minutes on first build..."
echo

# Build debug APK
buildozer android debug

if [ $? -eq 0 ]; then
    echo
    echo "✅ Build successful!"
    echo "📱 APK location: bin/*.apk"
    echo
    echo "To install on device:"
    echo "  adb install bin/*.apk"
    echo
    ls -lh bin/*.apk
else
    echo
    echo "❌ Build failed!"
    echo "Check ANDROID_BUILD_GUIDE.md for troubleshooting"
    exit 1
fi
