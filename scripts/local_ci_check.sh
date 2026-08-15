#!/bin/bash
# Local CI check script - runs the same checks as CI before committing
# This helps catch issues before pushing to remote

set -e  # Exit on error

echo "=========================================="
echo "Running Local CI Checks"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "scripts/convert_to_notebooks.py" ]; then
    echo "Error: Must be run from repository root"
    exit 1
fi

echo "1. Checking Python syntax errors..."
echo "-----------------------------------"
python -m py_compile scripts/convert_to_notebooks.py
for lecture_file in lecture_*/lecture_*.py; do
    echo "  Checking: $lecture_file"
    python -m py_compile "$lecture_file"
done
echo "✓ All Python syntax checks passed"
echo ""

echo "2. Running smoke tests for automation scripts..."
echo "--------------------------------------------------"
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest not found. Please install the development environment:"
    echo "   make install-dev"
    echo "   or: micromamba env create -f environment-dev.yml -y"
    exit 1
fi
if pytest tests/; then
    echo "✓ All script smoke tests passed"
else
    echo ""
    echo "❌ Script smoke tests failed. Please fix them before committing."
    exit 1
fi
echo ""

echo "3. Checking code formatting with black..."
echo "-----------------------------------------"
if ! command -v black &> /dev/null; then
    echo "❌ black not found. Please install the development environment:"
    echo "   make install-dev"
    echo "   or: micromamba env create -f environment-dev.yml -y"
    exit 1
fi
if black --check .; then
    echo "✓ All black formatting checks passed"
else
    echo ""
    echo "❌ black found formatting issues. Run 'make format' or 'black .' to fix them."
    exit 1
fi
echo ""

echo "4. Linting with ruff..."
echo "------------------------"
if ! command -v ruff &> /dev/null; then
    echo "❌ ruff not found. Please install the development environment:"
    echo "   make install-dev"
    echo "   or: micromamba env create -f environment-dev.yml -y"
    exit 1
fi
if ruff check .; then
    echo "✓ All ruff linting checks passed"
else
    echo ""
    echo "❌ ruff found issues. Please fix them before committing."
    exit 1
fi
echo ""

echo "5. Converting lectures to notebooks..."
echo "---------------------------------------"
python scripts/convert_to_notebooks.py
echo "✓ Notebooks converted successfully"
echo ""

echo "6. Verifying notebooks were created..."
echo "---------------------------------------"
for lecture_file in lecture_*/lecture_*.py; do
    notebook_file="${lecture_file%.py}.ipynb"
    if [ ! -f "$notebook_file" ]; then
        echo "❌ Notebook not found: $notebook_file"
        exit 1
    fi
done
echo "✓ All notebooks verified"
echo ""

echo "=========================================="
echo "✓ All local CI checks passed!"
echo "=========================================="
echo ""
echo "Safe to commit and push. CI should pass."
echo ""
