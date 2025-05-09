#!/bin/bash
# Advanced script to build and run the MLSecOps docker container

# Default to interactive mode
run_mode="interactive"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --detach|-d)
            run_mode="detached"
            shift
            ;;
        --stop)
            run_mode="stop"
            shift
            ;;
        --help|-h)
            run_mode="help"
            shift
            ;;
        *)
            shift
            ;;
    esac
done

show_help() {
    echo
    echo "MLSecOps Docker Runner"
    echo "Usage: ./run-docker.sh [OPTIONS]"
    echo
    echo "Options:"
    echo "  --detach, -d       Run containers in detached mode (background)"
    echo "  --stop             Stop running containers"
    echo "  --help, -h         Show this help message"
    echo
    exit 0
}

if [ "$run_mode" == "help" ]; then
    show_help
elif [ "$run_mode" == "stop" ]; then
    echo "Stopping MLSecOps containers..."
    docker-compose down
    echo "Containers stopped."
elif [ "$run_mode" == "interactive" ]; then
    echo "Building and starting the MLSecOps application container..."
    echo "Services will be available at:"
    echo " - MLflow UI: http://localhost:5000"
    echo " - FastAPI: http://localhost:8000/docs"
    echo " - Streamlit Dashboard: http://localhost:8501"
    echo
    echo "Press Ctrl+C to stop the containers"
    docker-compose up --build
else
    echo "Starting containers in detached mode..."
    docker-compose up --build -d
    echo
    echo "Services are now running in the background:"
    echo " - MLflow UI: http://localhost:5000"
    echo " - FastAPI: http://localhost:8000/docs"
    echo " - Streamlit Dashboard: http://localhost:8501"
    echo
    echo "To stop the containers, run: ./run-docker.sh --stop"
fi
