#!/bin/bash

# This script sets up and runs the Color Factory Game on macOS.
# It creates a virtual environment, installs dependencies, and starts the game.

# Navigate to the directory where the script is located
cd "$(dirname "$0")"

# Check if the virtual environment directory exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment. Please ensure you have python3 and venv installed."
        exit 1
    fi
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install pygame
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies. Please check your internet connection and pip installation."
    exit 1
fi

# Run the game in the background
echo "Starting the game..."
nohup python3 main.py > /dev/null 2>&1 &

# Deactivate the virtual environment
deactivate
