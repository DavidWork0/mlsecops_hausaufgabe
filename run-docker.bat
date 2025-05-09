
@echo off
REM filepath: c:\Users\T440\Documents\GitHub\mlsecops_haufaufgabe\run-docker.bat
REM Advanced script to build and run the MLSecOps docker container on Windows

SETLOCAL EnableDelayedExpansion

REM Default to interactive mode
SET run_mode=interactive

REM Parse command line arguments
IF "%1"=="--detach" (
    SET run_mode=detached
) ELSE IF "%1"=="-d" (
    SET run_mode=detached
) ELSE IF "%1"=="--help" (
    GOTO :show_help
) ELSE IF "%1"=="-h" (
    GOTO :show_help
) ELSE IF "%1"=="--stop" (
    GOTO :stop_containers
)

IF "%run_mode%"=="interactive" (
    echo Building and starting the MLSecOps application container...
    echo Services will be available at:
    echo - MLflow UI: http://localhost:5000
    echo - FastAPI: http://localhost:8000/docs
    echo - Streamlit Dashboard: http://localhost:8501
    echo.
    echo Press Ctrl+C to stop the containers
    docker-compose up --build
) ELSE (
    echo Starting containers in detached mode...
    docker-compose up --build -d
    echo.
    echo Services are now running in the background:
    echo - MLflow UI: http://localhost:5000
    echo - FastAPI: http://localhost:8000/docs
    echo - Streamlit Dashboard: http://localhost:8501
    echo.
    echo To stop the containers, run: run-docker.bat --stop
)

GOTO :end

:show_help
echo.
echo MLSecOps Docker Runner
echo Usage: run-docker.bat [OPTIONS]
echo.
echo Options:
echo   --detach, -d       Run containers in detached mode (background)
echo   --stop             Stop running containers
echo   --help, -h         Show this help message
echo.
GOTO :end

:stop_containers
echo Stopping MLSecOps containers...
docker-compose down
echo Containers stopped.
GOTO :end

:end
ENDLOCAL
