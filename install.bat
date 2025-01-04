@echo off
title Installing dependencies and running the app

color 0A

echo.
echo ============================================
echo    Installing required dependencies...
echo ============================================
echo.

pip install nextcord
pip install asyncio

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Something went wrong during installation. Please check the errors above.
    echo Press any key to exit...
    pause
    exit /b
)

echo.
echo ============================================
echo    Dependencies installed successfully!
echo    Running app.py...
echo ============================================
echo.

python app.py

echo.
echo ============================================
echo    App has finished running.
echo ============================================
pause
