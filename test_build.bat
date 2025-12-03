@echo off
title Test PyInstaller Build
cls
echo.
echo ====================================================================
echo    Test PyInstaller Build (Quick Test)
echo ====================================================================
echo.

:: Check PyInstaller
echo [1/2] Checking PyInstaller installation...
uv run pyinstaller --version
if errorlevel 1 (
    echo [ERROR] PyInstaller not found via uv
    pause
    exit /b 1
)
echo   PyInstaller OK!
echo.

:: Check if frontend is built
echo [2/2] Checking frontend build...
if exist "frontend\dist\index.html" (
    echo   Frontend build found!
) else (
    echo   [WARNING] Frontend not built yet
    echo   Run build_frontend.bat first if you want to include the React frontend
)
echo.

echo ====================================================================
echo    Environment Ready for Build
echo ====================================================================
echo.
echo To build the executable, run:
echo   build_executable.bat
echo.
echo Or to build everything (frontend + exe + package):
echo   create_distribution.bat
echo.
pause
