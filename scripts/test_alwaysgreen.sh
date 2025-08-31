#!/usr/bin/env bash
set -euo pipefail

# AlwaysGreen CI-Rescue Demo Test Script
# This tests the demo version of AlwaysGreen with a simple broken calculator

# Unset potentially conflicting environment variables
unset PYTHONPATH
unset VIRTUAL_ENV
unset ALWAYSGREEN_API_KEY
unset ALWAYSGREEN_CONFIG
unset GIT_PYTHON_REFRESH

echo "🧪 Testing AlwaysGreen CI-Rescue Demo Version"
echo "======================================"
echo

# Use consistent venv directory
VENV_DIR=".venv"

# Determine script and repo root, and ensure we run from repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

# Always run setup to ensure AlwaysGreen is installed and up-to-date
if [ -f "$SCRIPT_DIR/setup_alwaysgreen.sh" ]; then
  echo "📦 Running setup_alwaysgreen.sh to ensure AlwaysGreen is installed..."
  bash "$SCRIPT_DIR/setup_alwaysgreen.sh" "$VENV_DIR"
  echo
else
  echo "❌ setup_alwaysgreen.sh not found!"
  exit 1
fi

# Activate venv
if [ -d "$VENV_DIR" ]; then
  source "$VENV_DIR/bin/activate"
  echo "✅ Using venv: $VENV_DIR"
else
  echo "❌ Failed to create venv!"
  exit 1
fi

# Verify AlwaysGreen is available
if ! command -v alwaysgreen &> /dev/null; then
  echo "❌ AlwaysGreen command not found after setup!"
  exit 1
fi

echo "AlwaysGreen version:"
alwaysgreen version 2>/dev/null || echo "AlwaysGreen CI-Rescue (demo version)"
echo

# Create a test bug in calculator
echo "🐛 Introducing bug in calculator.py..."
# Use different sed syntax for macOS vs Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
  sed -i '' 's/return a - b/return a + b  # BUG: Using addition instead of subtraction/' src/calculator.py
else
  sed -i 's/return a - b/return a + b  # BUG: Using addition instead of subtraction/' src/calculator.py
fi

# Run AlwaysGreen to fix it (whole-file is now default, no need to specify)
echo "🚀 Running AlwaysGreen to fix ALL bugs in calculator.py..."
echo
alwaysgreen fix . --pytest-args "tests/test_calculator.py"

# Check if tests pass
echo
echo "✅ Verifying fix..."
pytest tests/ -v

echo
echo "🎉 AlwaysGreen successfully fixed the bug!"
