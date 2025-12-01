@echo off
title Kill Ports 3000, 3001, 5000
cls

echo.
echo ====================================================
echo    Nettoyage des ports 3000, 3001, 5000
echo ====================================================
echo.

:: Port 3000
echo Verification du port 3000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3000" ^| findstr "LISTENING"') do (
    echo Port 3000 occupe par le processus %%a - Fermeture...
    taskkill /PID %%a /F >nul 2>&1
)

:: Port 3001
echo Verification du port 3001...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3001" ^| findstr "LISTENING"') do (
    echo Port 3001 occupe par le processus %%a - Fermeture...
    taskkill /PID %%a /F >nul 2>&1
)

:: Port 5000
echo Verification du port 5000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5000" ^| findstr "LISTENING"') do (
    echo Port 5000 occupe par le processus %%a - Fermeture...
    taskkill /PID %%a /F >nul 2>&1
)

echo.
echo Tous les ports sont liberes!
echo.
pause
