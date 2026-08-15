.PHONY: help install convert clean notebooks build-website serve-website clean-website build-pdf clean-pdf update-deps test-deps create-locks ci-local lint format generate-qr-codes start-notebook test

help:
	@echo "Research Software Engineering Lectures - Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install          - Create micromamba environment with all dependencies for all lectures"
	@echo "  convert          - Convert all Python lectures to Jupyter notebooks (includes QR code generation)"
	@echo "  notebooks        - Alias for convert"
	@echo "  generate-qr-codes - Generate QR codes for course website and all lectures"
	@echo "  start-notebook   - Start Jupyter with Jupytext syncing enabled (edits sync back to .py files)"
	@echo "  build-website    - Build the Jupyter Book website"
	@echo "  serve-website    - Build and serve the website locally"
	@echo "  build-pdf        - Build the course as a PDF document"
	@echo "  clean            - Remove generated notebook files"
	@echo "  clean-website    - Remove generated website files"
	@echo "  clean-pdf        - Remove generated PDF files"
	@echo "  update-deps      - Test and update conda dependencies with lock files"
	@echo "  test-deps        - Test current dependencies without creating lock files"
	@echo "  create-locks     - Create conda-lock files for all platforms"
	@echo "  ci-local         - Run local CI checks (lint, syntax, convert) before committing"
	@echo "  test             - Run smoke tests for the automation scripts in scripts/"
	@echo "  lint             - Run black formatting check and ruff linting on all Python files"
	@echo "  format           - Auto-format all Python files with black"
	@echo "  help             - Show this help message"

install:
	micromamba env create -f environment.yml -y
	@echo "Environment created. Activate with: micromamba activate rse_lecture"

convert: notebooks

notebooks:
	python scripts/convert_to_notebooks.py

generate-qr-codes:
	python scripts/generate_qr_codes.py

start-notebook:
	@echo "Starting Jupyter Notebook with Jupytext syncing enabled..."
	@echo "Edits in the browser will sync back to the .py source files."
	jupyter notebook --ServerApp.contents_manager_class=jupytext.TextFileContentsManager

build-website: notebooks
	@echo "Building Jupyter Book v2 static HTML site..."
	@jupyter-book build --html
	@echo "✅ Static HTML site built in _build/html/"

serve-website: notebooks
	@echo "Starting Jupyter Book development server..."
	@echo "Press Ctrl+C to stop the server"
	@jupyter-book start --port 8000

clean:
	find . -name "*.ipynb" -not -path "./.git/*" -not -path "./_build/*" -delete
	@echo "Cleaned all generated notebooks"

clean-website:
	jupyter-book clean .
	@echo "Cleaned website build files"

build-pdf: notebooks
	@echo "Building PDF version of the course..."
	@mkdir -p exports
	@# Build PDF using myst.yml export configuration
	@set -e; \
	jupyter-book build --pdf; \
	if [ -f exports/book.pdf ]; then \
		echo "✅ PDF built successfully in exports/book.pdf"; \
	else \
		echo "❌ PDF build failed - output file not created"; \
		exit 1; \
	fi

clean-pdf:
	rm -rf exports
	@echo "Cleaned PDF export files"

update-deps:
	python scripts/update_dependencies.py
	@echo "Dependencies tested and lock files updated"

test-deps:
	python scripts/update_dependencies.py --test-only
	@echo "Dependency testing complete"

create-locks:
	python scripts/update_dependencies.py --create-locks
	@echo "Lock files created for all platforms"

ci-local:
	@echo "Running local CI checks (same as GitHub Actions)..."
	@bash scripts/local_ci_check.sh

test:
	@echo "Running smoke tests for automation scripts..."
	pytest tests/

lint:
	@echo "Running black formatting check..."
	@black --check .
	@echo ""
	@echo "Running ruff linting..."
	@ruff check .
	@echo ""
	@echo "✓ All checks passed"

format:
	@echo "Auto-formatting all Python files with black..."
	@black .
	@echo ""
	@echo "✓ All Python files formatted"

