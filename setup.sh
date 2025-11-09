#!/bin/bash
# Setup script for Aiwynn's Idea Factory using uv

set -e

echo "╔════════════════════════════════════════╗"
echo "║   Aiwynn's Idea Factory Setup          ║"
echo "╚════════════════════════════════════════╝"
echo

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed!"
    echo
    echo "Install uv with:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo
    echo "Or visit: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

echo "✓ uv is installed"

# Check Python version
echo
echo "Setting up Python 3.12 environment..."

# Create venv with uv using Python 3.12
uv venv --python 3.12

echo "✓ Virtual environment created"

# Activate and install dependencies
echo
echo "Installing dependencies..."

# uv pip install with the venv
uv pip install -e .

echo "✓ Dependencies installed"

echo
echo "╔════════════════════════════════════════╗"
echo "║   Setup Complete!                      ║"
echo "╚════════════════════════════════════════╝"
echo
echo "To activate the virtual environment:"
echo "  source .venv/bin/activate"
echo
echo "Then you can use:"
echo "  ./idea-factory.py --help"
echo "  python idea-factory.py list"
echo "  python idea-factory.py stats"
echo
echo "Or activate and run directly:"
echo "  source .venv/bin/activate && ./idea-factory.py stats"
echo
