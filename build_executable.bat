@echo off
title Build rFactor Championship Creator Executable
cls
echo.
echo ====================================================================
echo    rFactor Championship Creator - Build Executable
echo ====================================================================
echo.
echo This will create a standalone executable package that can be
echo distributed to other users without requiring Python or Node.js.
echo.
echo ====================================================================
echo.

:: Step 1: Build React Frontend
echo [1/4] Building React Frontend...
echo.
call build_frontend.bat
if errorlevel 1 (
    echo [ERROR] Frontend build failed
    pause
    exit /b 1
)
echo.

:: Step 2: Install/Update Python dependencies
echo [2/4] Installing/Updating Python dependencies...
echo.
call uv sync
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies
    pause
    exit /b 1
)
echo   Dependencies installed successfully!
echo.

:: Step 3: Clean previous build
echo [3/4] Cleaning previous build...
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

:: Step 4: Run PyInstaller
echo [4/4] Building executable with PyInstaller...
echo   This may take several minutes...
echo.
uv run pyinstaller rfactor_app.spec --clean
if errorlevel 1 (
    echo [ERROR] PyInstaller build failed
    echo.
    echo Trying with direct Python call...
    python -m PyInstaller rfactor_app.spec --clean
    if errorlevel 1 (
        echo [ERROR] PyInstaller build failed with both methods
        pause
        exit /b 1
    )
)
echo.

:: Success message
echo.
echo ====================================================================
echo    BUILD SUCCESSFUL!
echo ====================================================================
echo.
echo The standalone application has been created in:
echo   dist\rfactor_championship_creator\
echo.
echo To distribute the application:
echo   1. Copy the entire 'dist\rfactor_championship_creator\' folder
echo   2. Make sure config.json is configured for the target system
echo   3. Run 'rfactor_championship_creator.exe' to start the app
echo.
echo ====================================================================
echo.
pause
