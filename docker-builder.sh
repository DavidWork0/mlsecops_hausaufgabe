#!/bin/bash
# Docker Builder Utility for MLSecOps project
# This script provides advanced Docker build options and utilities

DOCKER_IMAGE_NAME=mlsecops-app
DOCKER_IMAGE_VERSION=latest

# Function to show help message
show_help() {
    echo
    echo "MLSecOps Docker Builder Utility"
    echo "Usage: ./docker-builder.sh [COMMAND]"
    echo
    echo "Commands:"
    echo "  build       Build Docker image"
    echo "  clean       Clean up Docker resources"
    echo "  prune       Deep clean of Docker resources (all unused containers, networks, images, volumes)"
    echo "  push        Push Docker image to a registry (requires registry URL as parameter)"
    echo "  scan        Scan Docker image for vulnerabilities"
    echo "  help        Show this help message"
    echo
    echo "Examples:"
    echo "  ./docker-builder.sh build"
    echo "  ./docker-builder.sh push myregistry.com/username"
    echo
    exit 0
}

# Function to build Docker image
build_image() {
    echo "Building Docker image: $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_VERSION..."
    echo
    docker build -t $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_VERSION -f src/Dockerfile .
    echo
    echo "Build completed."
}

# Function to clean Docker resources
clean_resources() {
    echo "Cleaning Docker resources..."
    echo
    echo "Stopping and removing containers..."
    docker-compose down
    echo "Removing unused images..."
    docker image prune -f
    echo
    echo "Clean completed."
}

# Function to deep clean Docker resources
prune_resources() {
    echo "Performing deep clean (prune) of Docker resources..."
    echo "This will remove all unused containers, networks, images, and volumes."
    echo
    read -p "Are you sure you want to continue? [Y/n] " confirm
    if [[ $confirm == "Y" || $confirm == "y" || $confirm == "" ]]; then
        echo
        echo "Removing all unused containers, networks, images and volumes..."
        docker system prune -a --volumes -f
        echo
        echo "Prune completed."
    else
        echo
        echo "Prune operation cancelled."
    fi
}

# Function to push Docker image to registry
push_image() {
    if [ -z "$1" ]; then
        echo "Error: Please specify a target registry."
        echo "Example: ./docker-builder.sh push myregistry.com/username"
        exit 1
    fi
    
    TARGET_REGISTRY=$1
    echo "Tagging and pushing image to $TARGET_REGISTRY/$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_VERSION..."
    echo
    docker tag $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_VERSION $TARGET_REGISTRY/$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_VERSION
    docker push $TARGET_REGISTRY/$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_VERSION
    echo
    echo "Push completed."
}

# Function to scan Docker image for vulnerabilities
scan_image() {
    echo "Scanning Docker image for vulnerabilities..."
    echo
    echo "NOTE: This requires Docker Scout or another scanning tool to be installed."
    echo
    
    if [ "$DOCKER_SCOUT_ENABLED" == "true" ]; then
        docker scout cves $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_VERSION
    else
        echo "Docker Scout not enabled. Please install Docker Scout or another scanning tool."
        echo "You can enable Docker Scout by setting DOCKER_SCOUT_ENABLED=true environment variable."
    fi
}

# Main script logic
case "$1" in
    build)
        build_image
        ;;
    clean)
        clean_resources
        ;;
    prune)
        prune_resources
        ;;
    push)
        push_image "$2"
        ;;
    scan)
        scan_image
        ;;
    help|"")
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        echo "Run './docker-builder.sh help' for usage information."
        exit 1
        ;;
esac
