@echo off
call .venv\Scripts\activate.bat
git add .
git commit -m "auto update"
git push
pause
