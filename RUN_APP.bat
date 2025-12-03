@echo off
title rFactor Championship Creator
cls

:: This is the launcher script that will be distributed with the executable
:: It provides a clean interface and handles basic error checking

echo.
echo ====================================================================
echo    rFactor Championship Creator
echo ====================================================================
echo.

:: Check if executable exists
if not exist "rfactor_championship_creator.exe" (
    echo ERROR: rfactor_championship_creator.exe not found!
    echo.
    echo Please make sure you are running this script from the correct directory.
    echo.
    pause
    exit /b 1
)

:: Check if config.json exists
if not exist "config.json" (
    echo WARNING: config.json not found!
    echo.
    echo Creating a default config.json file...
    echo {
    echo   "rfactor_path": "C:/Program Files (x86)/Steam/steamapps/common/rFactor"
    echo } > config.json
    echo.
    echo A default configuration file has been created.
    echo Please edit config.json with your actual rFactor installation path.
    echo.
    pause
)

:: Start the application
echo Starting application...
echo.
start "" rfactor_championship_creator.exe

:: Wait a moment
timeout /t 2 /nobreak >nul

echo.
echo The application is now running!
echo A browser window should open automatically in a few seconds.
echo.
echo If the browser doesn't open automatically, go to:
echo   http://localhost:5000
echo.
echo To stop the application, close the console window that opened.
echo.
echo ====================================================================
echo.
