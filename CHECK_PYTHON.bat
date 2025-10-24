@echo off
echo ========================================
echo Python Version Check
echo ========================================
echo.

echo Checking Python versions...
echo.

echo [1] python command:
python --version
echo.

echo [2] python3 command:
python3 --version 2>nul
if %errorlevel% neq 0 echo Not found
echo.

echo [3] py launcher:
py --version 2>nul
if %errorlevel% neq 0 echo Not found
echo.

echo [4] py -3 launcher:
py -3 --version 2>nul
if %errorlevel% neq 0 echo Not found
echo.

echo ========================================
echo IMPORTANT:
echo You need Python 3.8 or higher!
echo Download from: https://www.python.org/downloads/
echo.
echo During installation, CHECK "Add Python to PATH"
echo ========================================
pause
