#!/bin/bash
# Build and test the alwaysgreen package locally

set -e

echo "🔨 Building alwaysgreen package..."

# Clean up old builds
rm -rf dist/ build/ *.egg-info src/*.egg-info

# Build the package
python -m pip install --upgrade pip build
python -m build

echo "📦 Package built successfully!"
echo "Contents of dist/:"
ls -la dist/

echo ""
echo "To test the package locally:"
echo "  pip install dist/alwaysgreen-*.whl"
echo ""
echo "To upload to PyPI:"
echo "  python -m twine upload dist/*"
echo ""
echo "To upload to GitHub Packages:"
echo "  See .github/workflows/publish-package.yml"
