@echo off
title KrishiNetra AI Launcher
echo ========================================================
echo   Starting KrishiNetra AI (Frontend + Backend)
echo ========================================================
echo.

echo [1/2] Starting FastAPI Backend on http://localhost:8000 ...
start "KrishiNetra Backend (Port 8000)" cmd /k "cd /d %~dp0Backend && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

echo [2/2] Starting Vite Frontend on http://localhost:5173 ...
start "KrishiNetra Frontend (Port 5173)" cmd /k "cd /d %~dp0Frontend && npm run dev"

echo.
echo ========================================================
echo   Services are booting up!
echo   - Frontend: http://localhost:5173
echo   - Backend Docs: http://localhost:8000/docs
echo ========================================================
timeout /t 3 >nul
start http://localhost:5173
