#!/bin/bash

# GoTo Connect Device Location Manager - Docker Build Script
# Usage: ./docker-build.sh [option]

set -e

DOCKER_IMAGE="goto-device-manager"
DOCKER_TAG="latest"

show_help() {
    echo "GoTo Connect Device Location Manager - Docker Build Script"
    echo ""
    echo "Usage: $0 [option]"
    echo ""
    echo "Options:"
    echo "  build     Build the Docker image"
    echo "  run       Run the container with docker-compose"
    echo "  stop      Stop the container"
    echo "  logs      Show container logs"
    echo "  clean     Remove container and image"
    echo "  rebuild   Clean build (remove and rebuild)"
    echo "  help      Show this help message"
    echo ""
    echo "Prerequisites:"
    echo "  1. Copy .env.docker to .env and configure your GoTo Connect credentials"
    echo "  2. Ensure Docker and Docker Compose are installed"
    echo ""
}

build_image() {
    echo "Building Docker image: $DOCKER_IMAGE:$DOCKER_TAG"
    docker build -t $DOCKER_IMAGE:$DOCKER_TAG .
    echo "Build completed successfully!"
}

run_container() {
    echo "Starting container with docker-compose..."
    if [ ! -f ".env" ]; then
        echo "Warning: .env file not found. Copying from .env.docker template..."
        cp .env.docker .env
        echo "Please edit .env file with your GoTo Connect credentials before running again."
        exit 1
    fi
    docker-compose up -d
    echo "Container started! Access the application at: http://localhost:5000"
}

stop_container() {
    echo "Stopping container..."
    docker-compose down
    echo "Container stopped."
}

show_logs() {
    echo "Showing container logs (press Ctrl+C to exit)..."
    docker-compose logs -f
}

clean_all() {
    echo "Cleaning up containers and images..."
    docker-compose down -v 2>/dev/null || true
    docker rmi $DOCKER_IMAGE:$DOCKER_TAG 2>/dev/null || true
    echo "Cleanup completed."
}

rebuild_all() {
    echo "Performing clean rebuild..."
    clean_all
    build_image
    echo "Rebuild completed!"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed or not in PATH"
    exit 1
fi

# Main script logic
case "${1:-help}" in
    "build")
        build_image
        ;;
    "run")
        run_container
        ;;
    "stop")
        stop_container
        ;;
    "logs")
        show_logs
        ;;
    "clean")
        clean_all
        ;;
    "rebuild")
        rebuild_all
        ;;
    "help"|*)
        show_help
        ;;
esac