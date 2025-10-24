@echo off
REM Git push script for Kreggscode GPT

echo ========================================
echo Pushing to GitHub
echo ========================================
echo.

REM Configure git user
git config user.name "kreggscode"
git config user.email "kreggscode@users.noreply.github.com"

REM Commit changes
git commit -m "Complete: Beautiful banner, copy feature, cross-platform support"

REM Add remote if not exists
git remote remove origin 2>nul
git remote add origin https://github.com/kreggscode/Kreggscode-GPT.git

REM Rename branch to main
git branch -M main

REM Push to GitHub
git push -u origin main --force

echo.
echo ========================================
echo Done! Check: https://github.com/kreggscode/Kreggscode-GPT
echo ========================================
pause
