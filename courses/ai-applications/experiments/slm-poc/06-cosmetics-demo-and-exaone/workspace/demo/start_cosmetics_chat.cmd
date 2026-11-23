@echo off
cd /d "%~dp0.."
echo Starting the local chat. Keep this window open.
".venv-train\Scripts\python.exe" -u "demo\cosmetics_chat_server.py" --open
echo Chat stopped. If it is already open, close the other chat first.
pause
