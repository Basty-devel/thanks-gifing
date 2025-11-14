#!/bin/bash
# GIF Injector Pro Installation Script

echo "🖼️  GIF Injector Pro - Installation"
echo "===================================="

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Create virtual environment
echo "📦 Setting up Python virtual environment..."
python3 -m venv gif_injector_env
source gif_injector_env/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install flask

# Make scripts executable
chmod +x gif_injector.py
chmod +x web_interface.py

# Create necessary directories
mkdir -p templates
mkdir -p logs

echo ""
echo "✅ Installation completed!"
echo ""
echo "🚀 Usage:"
echo "   CLI Tool: ./gif_injector.py --help"
echo "   Web Interface: ./web_interface.py"
echo ""
echo "⚠️  Remember: This tool is for authorized security testing only!"
