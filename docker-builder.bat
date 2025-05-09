@echo off
REM Docker Builder Utility for MLSecOps project
REM This script provides advanced Docker build options and utilities

SET DOCKER_IMAGE_NAME=mlsecops-app
SET DOCKER_IMAGE_VERSION=latest

IF "%1"=="" GOTO help
IF "%1"=="build" GOTO build
IF "%1"=="clean" GOTO clean
IF "%1"=="prune" GOTO prune
IF "%1"=="push" GOTO push
IF "%1"=="scan" GOTO scan
IF "%1"=="help" GOTO help

:build
echo Building Docker image: %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_VERSION%...
echo.
docker build -t %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_VERSION% -f src/Dockerfile .
echo.
echo Build completed.
GOTO end

:clean
echo Cleaning Docker resources...
echo.
echo Stopping and removing containers...
docker-compose down
echo Removing unused images...
docker image prune -f
echo.
echo Clean completed.
GOTO end

:prune
echo Performing deep clean (prune) of Docker resources...
echo This will remove all unused containers, networks, images, and volumes.
echo.
SET /P CONFIRM=Are you sure you want to continue? [Y/N]: 
IF /I "%CONFIRM%"=="Y" (
    echo.
    echo Removing all unused containers, networks, images and volumes...
    docker system prune -a --volumes -f
    echo.
    echo Prune completed.
) ELSE (
    echo.
    echo Prune operation cancelled.
)
GOTO end

:push
IF "%2"=="" (
    echo Error: Please specify a target registry.
    echo Example: docker-builder.bat push myregistry.com/username
    GOTO end
)
SET TARGET_REGISTRY=%2
echo Tagging and pushing image to %TARGET_REGISTRY%/%DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_VERSION%...
echo.
docker tag %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_VERSION% %TARGET_REGISTRY%/%DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_VERSION%
docker push %TARGET_REGISTRY%/%DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_VERSION%
echo.
echo Push completed.
GOTO end

:scan
echo Scanning Docker image for vulnerabilities...
echo.
echo NOTE: This requires Docker Scout or another scanning tool to be installed.
echo.
IF "%DOCKER_SCOUT_ENABLED%"=="true" (
    docker scout cves %DOCKER_IMAGE_NAME%:%DOCKER_IMAGE_VERSION%
) ELSE (
    echo Docker Scout not enabled. Please install Docker Scout or another scanning tool.
    echo You can enable Docker Scout by setting DOCKER_SCOUT_ENABLED=true environment variable.
)
GOTO end

:help
echo.
echo MLSecOps Docker Builder Utility
echo Usage: docker-builder.bat [COMMAND]
echo.
echo Commands:
echo   build       Build Docker image
echo   clean       Clean up Docker resources
echo   prune       Deep clean of Docker resources (all unused containers, networks, images, volumes)
echo   push        Push Docker image to a registry (requires registry URL as parameter)
echo   scan        Scan Docker image for vulnerabilities
echo   help        Show this help message
echo.
echo Examples:
echo   docker-builder.bat build
echo   docker-builder.bat push myregistry.com/username
echo.
GOTO end

:end
