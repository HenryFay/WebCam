@echo off
cd /d %~dp0
call conda activate
python app.py
pause
