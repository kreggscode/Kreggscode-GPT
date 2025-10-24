@echo off
REM Installation script for Kreggscode GPT (Windows)

echo ========================================
echo Kreggscode GPT - Installation Script
echo ========================================
echo.

REM Try to find Python 3 using py launcher first
py -3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Found Python 3 via py launcher
    py -3 --version
    echo.
    echo Installing dependencies...
    py -3 -m pip install --upgrade pip
    py -3 -m pip install -r requirements.txt
    goto :success
)

REM Try python3 command
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Found Python 3
    python3 --version
    echo.
    echo Installing dependencies...
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    goto :success
)

REM Check if python command points to Python 3
python --version 2>&1 | findstr /C:"Python 3" >nul
if %errorlevel% equ 0 (
    echo Found Python 3
    python --version
    echo.
    echo Installing dependencies...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    goto :success
)

REM No Python 3 found
echo ERROR: Python 3.8+ is not installed or not in PATH
echo.
echo Your system has an old Python 2.7 from MGLTools
echo Please install Python 3.8+ from https://www.python.org/downloads/
echo.
echo IMPORTANT: During installation, check "Add Python to PATH"
echo.
pause
exit /b 1

:success

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo To run the application, use:
echo   py -3 main.py
echo   or
echo   python main.py
echo.
goto :end

:end

pause
