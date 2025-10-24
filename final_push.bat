@echo off
echo Pushing final updates to GitHub...
git add .
git commit -m "Add copy feature documentation and visual panel"
git push origin main
echo Done!
pause
