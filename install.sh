#!/bin/bash
# Installation script for Kreggscode GPT (Linux/macOS)

echo "========================================"
echo "Kreggscode GPT - Installation Script"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager or https://www.python.org/downloads/"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Check if pip is available
if ! python3 -m pip --version &> /dev/null; then
    echo "ERROR: pip is not installed"
    echo "Please install pip for Python 3"
    exit 1
fi

echo "Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Installation completed successfully!"
    echo "========================================"
    echo ""
    echo "To run the application, use:"
    echo "  python3 main.py"
    echo "  or"
    echo "  ./main.py"
    echo ""
    
    # Make main.py executable
    chmod +x main.py
    echo "main.py is now executable"
else
    echo ""
    echo "ERROR: Installation failed"
    echo "Please check the error messages above"
    echo ""
    exit 1
fi
