@echo off
REM Quick run script for Kreggscode GPT (Windows)

echo Starting Kreggscode GPT...
echo.

REM Try py launcher first (recommended for Windows)
py -3 main.py
if %errorlevel% equ 0 goto :end

REM Try python3
python3 main.py
if %errorlevel% equ 0 goto :end

REM Try python
python main.py
if %errorlevel% equ 0 goto :end

REM No Python found
echo.
echo ========================================
echo ERROR: Python 3 not found!
echo ========================================
echo.
echo Please install Python 3.8+ from:
echo https://www.python.org/downloads/
echo.
echo IMPORTANT: Check "Add Python to PATH" during installation
echo.

:end
pause
