@echo off
python "%~dp0git_gui_app.py"
if errorlevel 1 (
    pause
)
