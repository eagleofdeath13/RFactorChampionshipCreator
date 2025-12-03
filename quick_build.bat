@echo off
title Quick Build (Executable Only)
cls
echo.
echo ====================================================================
echo    Quick Build - Executable Only (No Frontend Build)
echo ====================================================================
echo.
echo This script builds ONLY the Python executable, without rebuilding
echo the React frontend. Use this for faster testing.
echo.
echo For a complete build, use: create_distribution.bat
echo.
echo ====================================================================
echo.

:: Clean previous build
echo [1/2] Cleaning previous build...
if exist "dist\rfactor_championship_creator" (
    echo   Removing old build directory...
    rmdir /s /q "dist\rfactor_championship_creator"
)
if exist "build" (
    echo   Removing build cache...
    rmdir /s /q "build"
)
echo   Clean complete!
echo.

:: Run PyInstaller
echo [2/2] Building executable with PyInstaller...
echo   This may take several minutes...
echo.
uv run pyinstaller rfactor_app.spec --clean
if errorlevel 1 (
    echo [ERROR] PyInstaller build failed
    pause
    exit /b 1
)
echo.

:: Success message
echo.
echo ====================================================================
echo    BUILD SUCCESSFUL!
echo ====================================================================
echo.
echo The executable has been created in:
echo   dist\rfactor_championship_creator\
echo.
echo To test it:
echo   cd dist\rfactor_championship_creator
echo   rfactor_championship_creator.exe
echo.
echo ====================================================================
echo.
pause
