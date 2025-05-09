@echo off
REM Local execution script for MLSecOps project without Docker
REM This will run the project locally using Python directly

echo MLSecOps Local Runner
echo ====================

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python and try again.
    goto :end
)

echo Checking Python version...
python --version

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment.
        goto :end
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    goto :end
)

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install requirements.
    goto :end
)

REM Run the application
echo Starting application...
echo Services will be available at:
echo - MLflow UI: http://localhost:5000
echo - FastAPI: http://localhost:8000/docs
echo - Streamlit Dashboard: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
python src/run_all.py

:end
echo Done