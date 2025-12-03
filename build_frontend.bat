@echo off
title Build Frontend React
cls
echo.
echo ====================================================
echo    Building React Frontend for Production
echo ====================================================
echo.

cd frontend

echo [1/2] Installing dependencies...
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install npm dependencies
    pause
    exit /b 1
)

echo [2/2] Building React app...
call npm run build
if errorlevel 1 (
    echo [ERROR] Failed to build React app
    pause
    exit /b 1
)

cd ..

echo.
echo ====================================================
echo    Frontend build completed!
echo ====================================================
echo    Output: frontend\dist\
echo ====================================================
echo.
pause
