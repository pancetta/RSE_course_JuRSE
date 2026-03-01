.PHONY: help install install-dev register-kernel install-lecture1 install-lecture2 install-lecture3 install-lecture4 install-lecture5 install-lecture6 install-lecture7 install-lecture8 install-lecture9 install-lecture10 install-lecture11 install-lecture12 install-lecture13 install-lecture14 convert clean notebooks build-website serve-website clean-website build-pdf clean-pdf update-deps test-deps create-locks ci-local lint format generate-qr-codes

help:
	@echo "Research Software Engineering Lectures - Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install          - Create base micromamba environment for all lectures"
	@echo "  install-dev      - Create development environment with all dependencies and dev tools"
	@echo "  register-kernel  - Register ipykernel for the rse_lecture environment in Jupyter"
	@echo "  install-lecture1 - Create environment with lecture 1 dependencies"
	@echo "  install-lecture2 - Create environment with lecture 2 dependencies"
	@echo "  install-lecture3 - Create environment with lecture 3 dependencies"
	@echo "  install-lecture4 - Create environment with lecture 4 dependencies (includes matplotlib)"
	@echo "  install-lecture5 - Create environment with lecture 5 dependencies (includes pytest, coverage)"
	@echo "  install-lecture6 - Create environment with lecture 6 dependencies"
	@echo "  install-lecture7 - Create environment with lecture 7 dependencies"
	@echo "  install-lecture8 - Create environment with lecture 8 dependencies"
	@echo "  install-lecture9 - Create environment with lecture 9 dependencies"
	@echo "  install-lecture10 - Create environment with lecture 10 dependencies"
	@echo "  install-lecture11 - Create environment with lecture 11 dependencies (includes h5py, netCDF4, pandas)"
	@echo "  install-lecture12 - Create environment with lecture 12 dependencies"
	@echo "  install-lecture13 - Create environment with lecture 13 dependencies"
	@echo "  install-lecture14 - Create environment with lecture 14 dependencies"
	@echo "  convert          - Convert all Python lectures to Jupyter notebooks (includes QR code generation)"
	@echo "  notebooks        - Alias for convert"
	@echo "  generate-qr-codes - Generate QR codes for course website and all lectures"
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
	@echo "  lint             - Run black formatting check and ruff linting on all Python files"
	@echo "  format           - Auto-format all Python files with black"
	@echo "  help             - Show this help message"

register-kernel:
	@echo "Registering ipykernel for rse_lecture environment..."
	micromamba run -n rse_lecture python -m ipykernel install --user --name rse_lecture --display-name "Python 3 (RSE Lecture)"
	@echo "Kernel registered. You can now use 'Python 3 (RSE Lecture)' in Jupyter."

install:
	micromamba env create -f environment.yml -y
	$(MAKE) register-kernel
	@echo "Base environment created. Activate with: micromamba activate rse_lecture"

install-dev:
	micromamba env create -f environment-dev.yml -y
	$(MAKE) register-kernel
	@echo "Development environment created with all dependencies and dev tools."
	@echo "Activate with: micromamba activate rse_lecture"

install-lecture1:
	@echo "Creating base environment..."
	micromamba env create -f environment.yml -y
	@echo "Adding lecture 1 specific dependencies..."
	micromamba env update -f lecture_01/environment.yml -y
	$(MAKE) register-kernel
	@echo "Environment created for lecture 1."
	@echo "Activate with: micromamba activate rse_lecture"

install-lecture2:
	@echo "Creating base environment..."
	micromamba env create -f environment.yml -y
	@echo "Adding lecture 2 specific dependencies..."
	micromamba env update -f lecture_02/environment.yml -y
	$(MAKE) register-kernel
	@echo "Environment created for lecture 2."
	@echo "Activate with: micromamba activate rse_lecture"

install-lecture3:
	@echo "Creating base environment..."
	micromamba env create -f environment.yml -y
	@echo "Adding lecture 3 specific dependencies..."
	micromamba env update -f lecture_03/environment.yml -y
	$(MAKE) register-kernel
	@echo "Environment created for lecture 3."
	@echo "Activate with: micromamba activate rse_lecture"

install-lecture4:
	@echo "Creating base environment..."
	micromamba env create -f environment.yml -y
	@echo "Adding lecture 4 specific dependencies..."
	micromamba env update -f lecture_04/environment.yml -y
	$(MAKE) register-kernel
	@echo "Environment created for lecture 4 (base + matplotlib)."
	@echo "Activate with: micromamba activate rse_lecture"

install-lecture5:
	@echo "Creating base environment..."
	micromamba env create -f environment.yml -y
	@echo "Adding lecture 5 specific dependencies..."
	micromamba env update -f lecture_05/environment.yml -y
	$(MAKE) register-kernel
	@echo "Environment created for lecture 5 (base + pytest, pytest-cov)."
	@echo "Activate with: micromamba activate rse_lecture"

install-lecture6:
	@echo "Creating base environment..."
	micromamba env create -f environment.yml -y
	@echo "Adding lecture 6 specific dependencies..."
	micromamba env update -f lecture_06/environment.yml -y
	$(MAKE) register-kernel
	@echo "Environment created for lecture 6."
	@echo "Activate with: micromamba activate rse_lecture"

install-lecture7:
	@echo "Creating base environment..."
	micromamba env create -f environment.yml -y
	@echo "Adding lecture 7 specific dependencies..."
	micromamba env update -f lecture_07/environment.yml -y
	$(MAKE) register-kernel
	@echo "Environment created for lecture 7."
	@echo "Activate with: micromamba activate rse_lecture"

install-lecture8:
	@echo "Creating base environment..."
	micromamba env create -f environment.yml -y
	@echo "Adding lecture 8 specific dependencies..."
	micromamba env update -f lecture_08/environment.yml -y
	$(MAKE) register-kernel
	@echo "Environment created for lecture 8."
	@echo "Activate with: micromamba activate rse_lecture"

install-lecture9:
	@echo "Creating base environment..."
	micromamba env create -f environment.yml -y
	@echo "Adding lecture 9 specific dependencies..."
	micromamba env update -f lecture_09/environment.yml -y
	$(MAKE) register-kernel
	@echo "Environment created for lecture 9."
	@echo "Activate with: micromamba activate rse_lecture"

install-lecture10:
	@echo "Creating base environment..."
	micromamba env create -f environment.yml -y
	@echo "Adding lecture 10 specific dependencies..."
	micromamba env update -f lecture_10/environment.yml -y
	$(MAKE) register-kernel
	@echo "Environment created for lecture 10."
	@echo "Activate with: micromamba activate rse_lecture"

install-lecture11:
	@echo "Creating base environment..."
	micromamba env create -f environment.yml -y
	@echo "Adding lecture 11 specific dependencies..."
	micromamba env update -f lecture_11/environment.yml -y
	$(MAKE) register-kernel
	@echo "Environment created for lecture 11 (base + h5py, netCDF4, pandas)."
	@echo "Activate with: micromamba activate rse_lecture"

install-lecture12:
	@echo "Creating base environment..."
	micromamba env create -f environment.yml -y
	@echo "Adding lecture 12 specific dependencies..."
	micromamba env update -f lecture_12/environment.yml -y
	$(MAKE) register-kernel
	@echo "Environment created for lecture 12."
	@echo "Activate with: micromamba activate rse_lecture"

install-lecture13:
	@echo "Creating base environment..."
	micromamba env create -f environment.yml -y
	@echo "Adding lecture 13 specific dependencies..."
	micromamba env update -f lecture_13/environment.yml -y
	$(MAKE) register-kernel
	@echo "Environment created for lecture 13."
	@echo "Activate with: micromamba activate rse_lecture"

install-lecture14:
	@echo "Creating base environment..."
	micromamba env create -f environment.yml -y
	@echo "Adding lecture 14 specific dependencies..."
	micromamba env update -f lecture_14/environment.yml -y
	$(MAKE) register-kernel
	@echo "Environment created for lecture 14."
	@echo "Activate with: micromamba activate rse_lecture"

convert: notebooks

notebooks:
	python scripts/convert_to_notebooks.py

generate-qr-codes:
	python scripts/generate_qr_codes.py

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

