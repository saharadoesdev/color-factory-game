@echo off

:: This script sets up and runs the Color Factory Game on Windows.
:: It creates a virtual environment, installs dependencies, and starts the game.

:: Navigate to the directory where the script is located
cd /d "%~dp0"

:: Check if the virtual environment directory exists
if not exist "venv" (
    echo "Creating virtual environment..."
    python -m venv venv
    if %errorlevel% neq 0 (
        echo "Error: Failed to create virtual environment. Please ensure you have python and venv installed."
        exit /b 1
    )
)

:: Activate the virtual environment
call "venv\Scripts\activate.bat"

:: Install dependencies
echo "Installing dependencies..."
pip install pygame
if %errorlevel% neq 0 (
    echo "Error: Failed to install dependencies. Please check your internet connection and pip installation."
    exit /b 1
)

:: Run the game in the background
echo "Starting the game..."
start "Color Factory" /b pythonw main.py

:: Deactivate the virtual environment
deactivate
