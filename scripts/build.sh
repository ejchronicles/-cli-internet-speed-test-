#!/bin/bash
set -e

echo "🔨 Building netspeed-cli package..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Install build dependencies
echo "📦 Installing build dependencies..."
python -m pip install --upgrade pip
pip install build twine

# Build package
echo "🏗️ Building package..."
python -m build

# Check package
echo "✅ Checking package..."
twine check dist/*

echo "🎉 Build completed successfully!"
echo "📦 Packages created:"
ls -la dist/
