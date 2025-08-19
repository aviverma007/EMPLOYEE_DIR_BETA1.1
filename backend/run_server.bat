@echo off
echo Starting Employee Directory Backend Server...

REM Activate virtual environment
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo ✓ Virtual environment activated
) else (
    echo WARNING: Virtual environment not found, using global Python
)

REM Set force reload to ensure Excel data loads
set FORCE_EXCEL_RELOAD=true

echo.
echo Starting server with Excel force reload...
echo Backend will be available at: http://localhost:8001
echo API docs will be available at: http://localhost:8001/docs
echo.

uvicorn server:app --reload --host 0.0.0.0 --port 8001

pause