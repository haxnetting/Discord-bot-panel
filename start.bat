@echo off
title Starting your Python Bot

color 0A

echo.
echo ============================================
echo     Starting Hax Bot Panel
echo ============================================
echo.

python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python is not installed. Please install Python and try again.
    echo Press any key to exit...
    pause
    exit /b
)

pip --version > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] pip is not installed. Please install pip and try again.
    echo Press any key to exit...
    pause
    exit /b
)

pip show nextcord > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [INFO] nextcord is not installed. Installing it now...
    pip install nextcord
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Failed to install nextcord. Please check your internet connection or permissions.
        echo Press any key to exit...
        pause
        exit /b
    )
)

pip show asyncio > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [INFO] asyncio is not installed. Installing it now...
    pip install asyncio
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Failed to install asyncio. Please check your internet connection or permissions.
        echo Press any key to exit...
        pause
        exit /b
    )
)

echo.
echo ============================================
echo     All dependencies installed successfully!
echo     Running bot...
echo ============================================
echo.

python app.py

echo.
echo ============================================
echo     Bot has finished running.
echo ============================================
