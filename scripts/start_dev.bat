@echo off
title rFactor Championship Creator - Dev Mode
cls
echo.
echo ====================================================
echo    rFactor Championship Creator - Dev Mode
echo ====================================================
echo.

:: 1. Lancer le backend
echo [1/2] Starting Backend (FastAPI)...
start "Backend - FastAPI" cmd /k "python -m uvicorn src.web.app:app --reload --port 5000"

:: 2. Attendre que le backend démarre (5 secondes)
echo Waiting for backend to start...
ping -n 6 127.0.0.1 >nul

:: 3. Lancer le frontend
echo [2/2] Starting Frontend (React/Vite)...
start "Frontend - React" cmd /k "cd frontend && npm run dev"

echo.
echo ====================================================
echo    Servers started in order:
echo ====================================================
echo.
echo  1. Backend (FastAPI):  http://localhost:5000
echo  2. Frontend (React):   http://localhost:3000
echo.
echo  Backend started FIRST (important for proxy)
echo  Wait 5-10 seconds, then open: http://localhost:3000
echo.
echo ====================================================
echo.
pause
