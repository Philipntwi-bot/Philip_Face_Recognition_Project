@echo off
title Philip Face AI - Mobile App Server
cd /d "%~dp0"
echo ========================================================
echo   LAUNCHING PHILIP FACE AI MOBILE SERVER
echo   Local URL: http://localhost:8080/mobile_simulator.html
echo ========================================================
python serve_mobile.py
pause
