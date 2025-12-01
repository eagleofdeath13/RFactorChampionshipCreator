@echo off
title rFactor Championship Creator - React Edition
cls
echo.
echo ====================================================
echo    rFactor Championship Creator - React Edition
echo ====================================================
echo.

:: Kill processes using ports 3000, 3001, 5000
echo [0/4] Liberation des ports...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3000" ^| findstr "LISTENING"') do (
    echo   - Port 3000 occupe, liberation...
    taskkill /PID %%a /F >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3001" ^| findstr "LISTENING"') do (
    echo   - Port 3001 occupe, liberation...
    taskkill /PID %%a /F >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5000" ^| findstr "LISTENING"') do (
    echo   - Port 5000 occupe, liberation...
    taskkill /PID %%a /F >nul 2>&1
)
echo   Ports liberes!
echo.

:: Verifier Python
echo [1/4] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    pause
    exit /b 1
)
echo   Python OK!

:: Verifier Node/NPM
echo [2/4] Verification de Node.js/NPM...
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Node.js/NPM n'est pas installe ou n'est pas dans le PATH
    pause
    exit /b 1
)
echo   Node.js/NPM OK!

:: Verifier et installer les dependances Python avec uv
echo [3/4] Verification des dependances Python...
python -c "import uvicorn" >nul 2>&1
if errorlevel 1 (
    echo   Installation des dependances Python avec uv...
    uv sync
    if errorlevel 1 (
        echo [ERREUR] Echec de l'installation des dependances
        pause
        exit /b 1
    )
    echo   Dependances installees avec succes!
) else (
    echo   Dependances Python OK!
)

:: Verifier et installer les dependances npm
echo [4/4] Verification des dependances npm...
if not exist "frontend\node_modules" (
    echo   Installation des dependances npm...
    cd frontend
    npm install
    cd ..
    if errorlevel 1 (
        echo [ERREUR] Echec de l'installation des dependances npm
        pause
        exit /b 1
    )
    echo   Dependances npm installees!
) else (
    echo   Dependances npm OK!
)

:: Verifier configuration
if not exist config.json (
    echo Configuration initiale...
    python setup_config.py
    if errorlevel 1 (
        echo [ERREUR] Echec de la configuration
        pause
        exit /b 1
    )
)

echo.
echo ====================================================
echo    Demarrage des serveurs...
echo ====================================================
echo.

:: Start Backend in new window
echo [1/2] Demarrage du Backend FastAPI (port 5000)...
start "Backend - FastAPI" cmd /k "python -m uvicorn src.web.app:app --reload --port 5000"

:: Wait for backend to start (important for proxy)
echo [2/2] Attente du backend (5 secondes)...
ping -n 6 127.0.0.1 >nul

:: Start Frontend in new window
echo [3/3] Demarrage du Frontend React (port 3000)...
start "Frontend - React" cmd /k "cd frontend && npm run dev"

echo.
echo ====================================================
echo    Both servers are starting in new windows
echo ====================================================
echo.
echo  Frontend (React):  http://localhost:3000
echo  Backend (API):     http://localhost:5000
echo  API Docs:          http://localhost:5000/api/docs
echo.
echo ====================================================
echo.
echo Open your browser at: http://localhost:3000
echo.
echo Press any key to close this window...
pause >nul
