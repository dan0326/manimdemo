#!/bin/bash

# Enhanced Setup Script for ManimDemo Project
# Handles personal package modifications and provides better error handling

# Script configuration
VENV_NAME="manimgl"
SOURCE_DIR="manimgl_lib_source"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Personal repositories with modifications
declare -A PERSONAL_REPOS=(
    ["manimPM"]="https://github.com/dan0326/manimPM.git"
    # Add more personal forks here as needed
    # ["package_name"]="https://github.com/youruser/package.git"
)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Error handling
set -e  # Exit on any error

# Functions for better organization
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    log_info "Checking dependencies..."
    
    if ! command -v python &> /dev/null; then
        log_error "Python is not installed or not in PATH"
        exit 1
    fi
    
    if ! command -v git &> /dev/null; then
        log_error "Git is not installed or not in PATH"
        exit 1
    fi
    
    PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
    log_info "Found Python version: $PYTHON_VERSION"
    
    # Check if Python version is 3.8 or higher
    if ! python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
        log_error "Python 3.8 or higher is required"
        exit 1
    fi
    
    log_success "All dependencies check passed"
}

backup_existing_setup() {
    if [ -d "$VENV_NAME" ]; then
        log_warning "Existing virtual environment found"
        read -p "Do you want to remove and recreate it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log_info "Backing up existing setup..."
            if [ -d "${VENV_NAME}_backup" ]; then
                rm -rf "${VENV_NAME}_backup"
            fi
            mv "$VENV_NAME" "${VENV_NAME}_backup"
            log_success "Backup created as ${VENV_NAME}_backup"
        else
            log_info "Using existing virtual environment"
            source "$VENV_NAME/bin/activate"
            return 0
        fi
    fi
    return 1
}

create_venv() {
    log_info "Creating virtual environment '$VENV_NAME'..."
    python -m venv "$VENV_NAME"
    source "$VENV_NAME/bin/activate"
    
    # Upgrade pip to latest version
    log_info "Upgrading pip..."
    pip install --upgrade pip
    
    log_success "Virtual environment created and activated"
}

install_personal_packages() {
    log_info "Installing personal package modifications..."
    
    # Create source directory if it doesn't exist
    mkdir -p "$SOURCE_DIR"
    cd "$SOURCE_DIR"
    
    for package_name in "${!PERSONAL_REPOS[@]}"; do
        repo_url="${PERSONAL_REPOS[$package_name]}"
        log_info "Processing $package_name from $repo_url"
        
        if [ ! -d "$package_name" ]; then
            log_info "Cloning $package_name..."
            git clone "$repo_url" "$package_name"
        else
            log_info "$package_name already exists, updating..."
            cd "$package_name"
            
            # Check if there are uncommitted changes
            if ! git diff-index --quiet HEAD --; then
                log_warning "Uncommitted changes found in $package_name"
                read -p "Stash changes and pull latest? (y/N): " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    git stash
                    git pull
                    log_info "Changes stashed, you can restore them with 'git stash pop'"
                else
                    log_warning "Skipping update for $package_name"
                    cd ..
                    continue
                fi
            else
                git pull
            fi
            cd ..
        fi
        
        # Install in development mode
        log_info "Installing $package_name in development mode..."
        cd "$package_name"
        pip install -e .
        cd "$SCRIPT_DIR"
        source manimgl/bin/activate
        python3 -m pip install build && python3 -m build && python3 -m pip install dist/*.whl
        
        log_success "$package_name installed successfully"
    done
    
}

install_standard_packages() {
    log_info "Installing standard packages from requirements.txt..."
    
    if [ ! -f "requirements.txt" ]; then
        log_error "requirements.txt not found in current directory"
        exit 1
    fi
    
    # Install with progress bar and better output
    pip install -r requirements.txt --progress-bar on
    
    log_success "Standard packages installed successfully"
}

verify_installation() {
    log_info "Verifying installation..."
    
    # Test if manimgl can be imported
    if python -c "import manimlib; print('ManimGL imported successfully')" 2>/dev/null; then
        log_success "ManimGL is working correctly"
    else
        log_error "ManimGL import failed"
        return 1
    fi
    
    # Check if manimgl command is available
    if [ -f "$VENV_NAME/bin/manimgl" ]; then
        log_success "manimgl command is available"
    else
        log_warning "manimgl command not found in virtual environment"
    fi
    
    log_success "Installation verification completed"
}

show_usage_info() {
    echo
    log_success "Setup completed successfully!"
    echo
    echo "To use the environment:"
    echo "  source $VENV_NAME/bin/activate"
    echo
    echo "To run an animation:"
    echo "  $VENV_NAME/bin/manimgl your_script.py YourSceneName"
    echo
    echo "Or use the VS Code tasks (Ctrl+Shift+P -> Tasks: Run Task):"
    echo "  - Run ManimGL"
    echo "  - Test ManimGL"
    echo
}

main() {
    echo "======================================"
    echo "  ManimDemo Project Setup Script"
    echo "======================================"
    echo
    
    # Change to script directory
    cd "$SCRIPT_DIR"
    
    check_dependencies
    
    # Check for existing setup
    if ! backup_existing_setup; then
        create_venv
    fi
    
    install_personal_packages
    install_standard_packages
    verify_installation
    show_usage_info
}

# Parse command line arguments
case "${1:-}" in
    --help|-h)
        echo "Usage: $0 [--help|--clean]"
        echo "  --help    Show this help message"
        echo "  --clean   Remove existing environment and start fresh"
        exit 0
        ;;
    --clean)
        log_info "Cleaning existing setup..."
        rm -rf "$VENV_NAME" "$SOURCE_DIR"
        log_success "Cleanup completed"
        ;;
esac

# Run main function
main