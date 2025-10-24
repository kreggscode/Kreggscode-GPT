@echo off
REM Push to GitHub script

echo ========================================
echo Pushing to GitHub
echo ========================================
echo.

REM Configure git (if needed)
git config user.name "kreggscode"
git config user.email "kreggscode@example.com"

REM Add remote
git remote add origin https://github.com/kreggscode/Kreggscode-GPT.git

REM Rename branch to main
git branch -M main

REM Push to GitHub
git push -u origin main

echo.
echo ========================================
echo Done! Check https://github.com/kreggscode/Kreggscode-GPT
echo ========================================
pause
