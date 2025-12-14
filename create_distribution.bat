
@echo off
title Create Distribution Package
cls
echo.
echo ====================================================================
echo    Create Distribution Package
echo ====================================================================
echo.
echo This script will create a ready-to-distribute ZIP package
echo containing everything needed to run the application.
echo.
echo ====================================================================
echo.

:: Step 0: Get version number
for /f %%i in ('uv run python scripts/get_version.py') do set APP_VERSION=%%i
echo Version: %APP_VERSION%
echo.

:: Step 1: Build the executable
echo [1/3] Building executable...
echo.
call build_executable.bat
if errorlevel 1 (
    echo [ERROR] Executable build failed
    pause
    exit /b 1
)
echo.

:: Step 2: Prepare distribution directory
echo [2/3] Preparing distribution package...
echo.

set DIST_DIR=dist\rfactor_championship_creator_v%APP_VERSION%
set BUILD_DIR=dist\rfactor_championship_creator

if exist "%DIST_DIR%" (
    echo   Removing old distribution directory...
    rmdir /s /q "%DIST_DIR%"
)

echo   Creating distribution directory...
mkdir "%DIST_DIR%"

echo   Copying executable files...
xcopy "%BUILD_DIR%\*" "%DIST_DIR%\" /E /I /Y >nul

echo   Copying launcher script...
copy "RUN_APP.bat" "%DIST_DIR%\" >nul

echo   Copying configuration template...
copy "config.template.json" "%DIST_DIR%\config.json" >nul

echo   Copying documentation...
if exist "README.md" copy "README.md" "%DIST_DIR%\" >nul
if exist "INSTALL.md" copy "INSTALL.md" "%DIST_DIR%\" >nul

echo   Package prepared!
echo.

:: Step 3: Create ZIP archive
echo [3/3] Creating ZIP archive...
echo.

:: Check if 7-Zip or PowerShell is available
set ZIP_FILE=dist\rFactor_Championship_Creator_v%APP_VERSION%.zip
where 7z >nul 2>&1
if %errorlevel% == 0 (
    echo   Using 7-Zip to create archive...
    7z a -tzip "%ZIP_FILE%" "%DIST_DIR%\*" >nul
    echo   Archive created with 7-Zip!
) else (
    echo   Using PowerShell to create archive...
    powershell -command "Compress-Archive -Path '%DIST_DIR%\*' -DestinationPath '%ZIP_FILE%' -Force"
    if errorlevel 1 (
        echo   [WARNING] Failed to create ZIP archive
        echo   You can manually ZIP the folder: %DIST_DIR%
    ) else (
        echo   Archive created with PowerShell!
    )
)
echo.

:: Success message
echo.
echo ====================================================================
echo    DISTRIBUTION PACKAGE READY!
echo ====================================================================
echo.
echo Version:             %APP_VERSION%
echo Distribution folder: %DIST_DIR%\
echo ZIP archive:         %ZIP_FILE%
echo.
echo To distribute:
echo   - Share the ZIP file, OR
echo   - Share the entire folder: %DIST_DIR%\
echo.
echo Users should:
echo   1. Extract the ZIP (if applicable)
echo   2. Edit config.json with their rFactor path
echo   3. Run RUN_APP.bat
echo.
echo ====================================================================
echo.
pause
