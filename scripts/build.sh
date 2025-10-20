#!/bin/bash

# CLI Internet Speed Test Tool - Build Script
# This script handles building, testing, and packaging the application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to display help
show_help() {
    echo "Usage: $0 [OPTION]"
    echo "Build script for CLI Internet Speed Test Tool"
    echo ""
    echo "Options:"
    echo "  all         Run all build steps (default)"
    echo "  test        Run tests only"
    echo "  build       Build package only"
    echo "  clean       Clean build artifacts"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 all      # Run complete build process"
    echo "  $0 test     # Run tests only"
    echo "  $0 clean    # Clean build files"
}

# Function to clean build artifacts
clean() {
    log_info "Cleaning build artifacts..."
    
    # Remove build directories
    rm -rf build/
    rm -rf dist/
    rm -rf *.egg-info/
    
    # Remove Python cache files
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete
    
    # Remove coverage reports
    rm -rf htmlcov/
    rm -f .coverage
    rm -f coverage.xml
    
    log_info "Clean completed!"
}

# Function to run tests
run_tests() {
    log_info "Running tests..."
    
    # Install test dependencies if not present
    if ! pip show pytest > /dev/null 2>&1; then
        pip install pytest pytest-cov
    fi
    
    # Run tests with coverage
    python -m pytest tests/ -v --cov=src --cov-report=html --cov-report=xml
    
    # Check if tests passed
    if [ $? -eq 0 ]; then
        log_info "All tests passed!"
    else
        log_error "Tests failed!"
        exit 1
    fi
}

# Function to run linting
run_linting() {
    log_info "Running code linting..."
    
    # Install linters if not present
    if ! pip show flake8 > /dev/null 2>&1; then
        pip install flake8 black
    fi
    
    # Run flake8
    log_info "Running flake8..."
    flake8 src/ tests/ --max-line-length=100 --statistics
    
    # Run black check (without modifying files)
    log_info "Running black check..."
    black --check src/ tests/
    
    log_info "Linting completed!"
}

# Function to build package
build_package() {
    log_info "Building package..."
    
    # Install build tools if not present
    if ! pip show build > /dev/null 2>&1; then
        pip install build
    fi
    
    # Build the package
    python -m build
    
    # Verify the built package
    if [ -f "dist/netspeed-cli-0.1.0.tar.gz" ]; then
        log_info "Package built successfully: dist/netspeed-cli-0.1.0.tar.gz"
    else
        log_error "Package build failed!"
        exit 1
    fi
}

# Function to run security checks
run_security_checks() {
    log_info "Running security checks..."
    
    # Install security tools if not present
    if ! pip show safety > /dev/null 2>&1; then
        pip install safety bandit
    fi
    
    # Check for known vulnerabilities
    log_info "Running safety check..."
    safety check --short-report
    
    # Run bandit security linter
    log_info "Running bandit..."
    bandit -r src/ -f json -o bandit-report.json || true
    
    log_info "Security checks completed!"
}

# Function to run complete build process
build_all() {
    log_info "Starting complete build process..."
    
    # Clean first
    clean
    
    # Run tests
    run_tests
    
    # Run linting
    run_linting
    
    # Run security checks
    run_security_checks
    
    # Build package
    build_package
    
    log_info "Build process completed successfully!"
    log_info "Generated files in dist/:"
    ls -la dist/
}

# Main script logic
main() {
    local command="${1:-all}"
    
    case "$command" in
        "all")
            build_all
            ;;
        "test")
            run_tests
            ;;
        "lint")
            run_linting
            ;;
        "build")
            build_package
            ;;
        "security")
            run_security_checks
            ;;
        "clean")
            clean
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
