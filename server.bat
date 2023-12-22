@echo off
start cmd /k python -m http.server
timeout /T 5 /NOBREAK
start chrome "http://localhost:8000"