@echo off
title ScreenLens AI - Stealth Desktop Copilot
cls
echo ========================================================
echo              SCREENLENS AI (ACTIVE)
echo ========================================================
echo.
echo   * Click [Scan Now] ya [Ctrl + Q] : Instant Answer
echo   * Click [Loop]     ya [Ctrl + L] : Auto-Loop Mode
echo   * Click [X]        ya [Ctrl + H] : Hide / Show
echo   * [Ctrl + Shift + X]             : Exit App
echo.
echo ========================================================
echo.
cd /d "%~dp0"
python answer_bubble.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] App exited with code %ERRORLEVEL%. Check app.log for details.
)
pause
