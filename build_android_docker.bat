@echo off
echo ========================================
echo Android APK Build - Docker Method
echo Works on Windows!
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not installed!
    echo.
    echo Please install Docker Desktop:
    echo https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

echo Building APK with Docker...
echo This may take 30-60 minutes on first build...
echo.

REM Build using Buildozer Docker image
docker run --rm -v "%cd%":/home/user/app kivy/buildozer buildozer android debug

if %errorlevel% equ 0 (
    echo.
    echo Build successful!
    echo APK location: bin\*.apk
    echo.
    dir bin\*.apk
) else (
    echo.
    echo Build failed!
    echo Try: docker pull kivy/buildozer
)

pause
