#!/bin/bash

# Move to the script's folder
cd "$(dirname "$0")"

PYTHON=$(which python3)

# Set up virtual environment if needed
if [ ! -d "env" ]; then
  echo "🔧 Creating environment..."
  $PYTHON -m venv env
  ./env/bin/pip install --upgrade pip
  ./env/bin/pip install -r "(Do not touch)requirements.txt"
fi

echo "🐍 Using Python: $PYTHON"
echo "📦 Installed packages:"
./env/bin/pip list

echo "🚀 Launching Smart Temp Tool..."
./env/bin/python gui_main.py