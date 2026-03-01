# Developer Guide

This guide contains detailed information for contributors and developers working on the RSE course repository.

## Repository Structure

```
RSE_course_JuRSE/
├── lecture_01/ through lecture_14/  # Individual lecture directories
│   ├── lecture_XX.py                # Lecture content (Jupytext format)
│   └── environment.yml              # Lecture-specific dependencies
├── scripts/                         # Automation scripts
│   ├── convert_to_notebooks.py     # Convert .py to .ipynb
│   ├── generate_qr_codes.py        # Generate QR codes
│   └── update_dependencies.py      # Dependency management
├── docs/                           # Detailed documentation
├── .github/workflows/              # CI/CD pipelines
├── environment.yml                 # All dependencies for all lectures
├── Makefile                        # Build automation
└── myst.yml                        # Jupyter Book configuration
```

## Development Workflow

### Environment Setup

Install the environment with all dependencies:

```bash
make install
micromamba activate rse_lecture
```

### Editing Lectures

**ALWAYS edit the `.py` files, never the `.ipynb` files directly.**

Lectures are written in Jupytext percent format:
- Cell markers: `# %%`
- Markdown cells: `# %% [markdown]`
- Code cells: `# %%` followed by Python code

### Testing Changes

Before committing, always run local CI checks:

```bash
make ci-local
```

This runs:
1. Python syntax validation
2. flake8 linting (strict and full)
3. Notebook conversion
4. Notebook verification

### Building the Website

The course uses [Jupyter Book v2](https://jupyterbook.org/) (MyST) for the website.

**Local development:**
```bash
make serve-website
```

This builds and serves at `http://localhost:8000` with:
- Interactive navigation with sidebar and search
- Formatted code cells with syntax highlighting
- Live content updates during development
- Modern MyST theme with responsive design

**Build only:**
```bash
make build-website
```

Output is in `_build/site/` directory.

### Converting Lectures

Convert all lectures to notebooks:
```bash
make convert
# or
python scripts/convert_to_notebooks.py
```

This automatically:
- Generates QR codes for the course website and each lecture
- Converts all Python lecture files to Jupyter notebooks
- Embeds QR codes in notebooks for quick access

### QR Codes

Each lecture includes QR codes at the beginning for easy access to:
- **Course Website**: The main course website
- **This Lecture**: Direct link to the specific lecture page

Generate QR codes separately:
```bash
make generate-qr-codes
# or
python scripts/generate_qr_codes.py
```

## Dependency Management

### Environment Files

The repository uses a single environment file with all dependencies:

- **`environment.yml`**: All dependencies for all lectures

### Installation

```bash
make install
micromamba activate rse_lecture
```

### Automated Updates

The repository includes an automated dependency update system:
- Runs weekly (Mondays at 9:00 UTC)
- Tests dependencies with CI checks
- Creates lock files for reproducibility
- Opens PR if updates pass tests

**Manual dependency testing:**
```bash
# Test current dependencies
make test-deps

# Test and create lock files
make update-deps

# Just create lock files
make create-locks
```

For details, see [DEPENDENCY_MANAGEMENT.md](DEPENDENCY_MANAGEMENT.md).

## CI/CD Pipeline

### Continuous Integration (`.github/workflows/ci.yml`)

Runs on every push and PR:
1. Lints code with flake8
2. Checks Python syntax
3. Converts lectures to notebooks
4. Executes all notebooks to verify they run
5. Tests on Linux, macOS 15, macOS 26, and Windows

### Deployment (`.github/workflows/deploy.yml`)

Deploys to GitHub Pages after CI succeeds:
1. Converts lectures to notebooks
2. Executes notebooks to generate plots
3. Builds static HTML with Jupyter Book
4. Deploys to GitHub Pages

### Dependency Updates (`.github/workflows/conda-dependency-update.yml`)

Weekly automated dependency testing:
1. Creates lock files for reproducibility
2. Tests updated dependencies
3. Opens PR if tests pass

### Link Checking (`.github/workflows/link-checker.yml`)

Checks all links in markdown and lecture files:
- Weekly on Mondays at 10:00 UTC (scheduled)
- Can be manually triggered via workflow_dispatch
- Uses [Lychee](https://github.com/lycheeverse/lychee)
- Reports broken links but does not fail the build (informational only)

Configuration in `.lycherc.toml` includes:
- Excluded URLs for sites that block automated checkers
- 30-second timeout per request
- 3 retries with 5-second wait time between retries
- Accepts status codes including redirects and rate limiting (429)

## Adding a New Lecture

1. **Create directory:**
   ```bash
   mkdir lecture_XX
   ```

2. **Create lecture file:**
   - Copy template from existing lecture
   - Name it `lecture_XX/lecture_XX.py`
   - Use Jupytext percent format

3. **Add any new dependencies** to `environment.yml` if needed

4. **Add Makefile target:** (no additional target needed - `make install` works for all lectures)

5. **Update myst.yml:**
   Add lecture to table of contents.

6. **Update README:**
   Add lecture to course overview.

7. **Ensure content is exactly 90 minutes**

8. **Test:**
   ```bash
   make install
   python scripts/convert_to_notebooks.py
   make ci-local
   ```

## Modifying Existing Lectures

1. **Edit the `.py` file** (never edit `.ipynb` directly)
2. **Test locally:**
   ```bash
   python -m py_compile lecture_XX/lecture_XX.py
   flake8 lecture_XX/lecture_XX.py
   python scripts/convert_to_notebooks.py
   jupyter nbconvert --to notebook --execute --inplace lecture_XX/lecture_XX.ipynb
   ```
3. **Verify lecture duration remains 90 minutes**
4. **Update documentation if needed**
5. **Run CI checks:**
   ```bash
   make ci-local
   ```
6. **Clean up:**
   ```bash
   make clean
   ```

## Why Jupytext?

Jupytext allows us to:
- **Version control**: Python files are easier to track in Git than notebooks
- **Code review**: Easier to review changes in pull requests
- **Collaboration**: Multiple people can work without merge conflicts
- **Flexibility**: Edit in your favorite Python IDE or as notebooks

You can also pair files for synchronized editing:
```bash
jupytext --set-formats py:percent,ipynb lecture_XX/lecture_XX.py
```

## Code Quality Standards

- **Linting**: All code must pass flake8 checks
- **Style**: Follow PEP 8 (enforced by `.flake8` config)
- **Syntax**: All Python files must have valid syntax
- **Execution**: All notebooks must execute without errors

Configuration in `.flake8`:
- Max line length: 127 characters
- Max complexity: 10
- Ignored errors: E402, W293, W291, E302, E305, F401, F841, E226, F541

## Platform Compatibility

All code must work on:
- Linux (Ubuntu)
- macOS 15 (Sequoia) and later
- macOS 26 (Tahoe)
- Windows 10/11 (with Git Bash)

Test on multiple platforms or ensure code is platform-agnostic.

## Git Workflow

1. Create feature branch
2. Make changes
3. Run `make ci-local`
4. Fix any issues
5. Commit with clear message
6. Push and create PR
7. Wait for CI to pass
8. Merge after review

## Make Targets Reference

| Target | Description |
|--------|-------------|
| `install` | Create environment with all dependencies |
| `convert` | Convert lectures to notebooks |
| `notebooks` | Alias for convert |
| `generate-qr-codes` | Generate QR codes |
| `build-website` | Build Jupyter Book website |
| `serve-website` | Build and serve website locally |
| `clean` | Remove generated notebooks |
| `clean-website` | Remove website build files |
| `update-deps` | Test and update dependencies |
| `test-deps` | Test current dependencies |
| `create-locks` | Create conda-lock files |
| `ci-local` | Run local CI checks |
| `lint` | Run flake8 linting |
| `help` | Show help message |

## Troubleshooting

### "jupytext not found"

Install the environment:
```bash
make install
```

### "flake8 not found"

Install the environment:
```bash
make install
```

### CI failing but local tests pass

- Check platform differences (workflow runs on Linux)
- Ensure you're testing with `environment.yml`
- Check workflow logs for specific errors

### Notebooks won't execute

- Check syntax errors in the `.py` file
- Ensure all dependencies are installed
- Try executing cell by cell to find the problem

## Additional Resources

- [Jupytext Documentation](https://jupytext.readthedocs.io/)
- [Jupyter Book Documentation](https://jupyterbook.org/)
- [MyST Documentation](https://mystmd.org/)
- [flake8 Documentation](https://flake8.pycqa.org/)
- [conda-lock Documentation](https://conda.github.io/conda-lock/)

## Getting Help

- Check this guide first
- Look at existing lectures for examples
- Check [CONTRIBUTING.md](../CONTRIBUTING.md)
- Open an issue on GitHub
- Ask in the RSE community forums
