@echo off
cd c:\python\SitoOmar\dmonaco90.github.io\
start cmd /k python main.py
timeout /T 5 /NOBREAK
start chrome "http://localhost:5000"