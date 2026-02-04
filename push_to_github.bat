@echo off
echo ========================================
echo GitHub Setup ^& Push Script
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed!
    echo.
    echo Please install Git from:
    echo https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo Git is installed
echo.

REM Check if already a git repository
if exist .git (
    echo This is already a Git repository
    echo Existing remotes:
    git remote -v
    echo.
    set /p continue_push="Do you want to continue and push? (y/n): "
    if /i not "%continue_push%"=="y" exit /b 0
) else (
    echo Initializing Git repository...
    git init
    echo Repository initialized
    echo.
)

REM Check git configuration
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo Git user not configured. Let's set it up:
    set /p git_name="Enter your name: "
    set /p git_email="Enter your email: "
    git config --global user.name "%git_name%"
    git config --global user.email "%git_email%"
    echo Git configured
    echo.
)

REM Get GitHub repository URL
echo Enter your GitHub repository details:
set /p github_user="GitHub username: "
set /p repo_name="Repository name (e.g., youtube-downloader): "

set REPO_URL=https://github.com/%github_user%/%repo_name%.git

echo.
echo Repository URL: %REPO_URL%
set /p confirm="Is this correct? (y/n): "

if /i not "%confirm%"=="y" (
    echo Aborted.
    exit /b 0
)

REM Add remote
git remote | findstr "origin" >nul
if %errorlevel% neq 0 (
    echo Adding remote origin...
    git remote add origin "%REPO_URL%"
    echo Remote added
) else (
    echo Remote 'origin' already exists. Updating URL...
    git remote set-url origin "%REPO_URL%"
)

echo.

REM Add all files
echo Adding files...
git add .
echo Files added
echo.

REM Show status
echo Files to be committed:
git status --short
echo.

REM Create commit
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Initial commit: Multi-platform YouTube Downloader

echo Creating commit...
git commit -m "%commit_msg%"
echo Commit created
echo.

REM Push to GitHub
echo Pushing to GitHub...
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo Successfully pushed to GitHub!
    echo.
    echo Your repository is now live at:
    echo    %REPO_URL%
    echo.
    echo Next steps:
    echo   1. Visit your repository on GitHub
    echo   2. GitHub Actions will automatically build executables
    echo   3. Create a release: git tag v1.0.0 ^&^& git push origin v1.0.0
) else (
    echo.
    echo Push failed!
    echo.
    echo Common issues:
    echo   1. Repository doesn't exist - Create it on GitHub first
    echo   2. Authentication failed - Check your credentials
    echo   3. Permission denied - Ensure you own the repository
    echo.
    echo Try visiting: https://github.com/%github_user%/%repo_name%
)

echo.
pause
