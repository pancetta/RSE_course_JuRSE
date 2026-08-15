# Contributing to RSE Course

Thank you for your interest in contributing to the Research Software Engineering course! We welcome contributions that improve the course materials, fix errors, or add new content.

## Quick Start for Contributors

1. **Fork and clone** the repository
2. **Install the environment:**
   ```bash
   make install
   micromamba activate rse_lecture
   ```
3. **Make your changes** (edit `.py` files, not `.ipynb` files)
4. **Test your changes:**
   ```bash
   make ci-local
   ```
5. **Commit and push** to your fork
6. **Open a pull request**

## Before You Commit

**ALWAYS run the local CI checks before committing:**

```bash
make ci-local
```

This runs the same checks as the GitHub Actions CI pipeline:
1. Python syntax validation
2. Black formatting check
3. Ruff linting
4. Notebook conversion
5. Notebook verification

Running these checks locally saves time and prevents CI failures!

## Contribution Guidelines

### Working with Lectures

**Important:** Always edit the `.py` files, never the `.ipynb` files directly.

- Lectures are written in [Jupytext](https://jupytext.readthedocs.io/) percent format
- Cell markers: `# %%` for code cells
- Markdown cells: `# %% [markdown]`
- Convert to notebooks with: `make convert`

### Lecture Duration

**Each lecture MUST be exactly 90 minutes.**

When modifying lectures:
- Include timing estimates for sections
- Consider time for introduction, content, exercises, and Q&A
- If content exceeds 90 minutes, remove or relocate content
- If content is under 90 minutes, add exercises or depth

### Code Quality

All contributions must meet these standards:

- **Pass black formatting** (max line length: 127 characters)
- **Pass ruff linting**
- **Valid Python syntax** (test with `python -m py_compile`)
- **Execute without errors** (all notebooks must run successfully)
- **Platform compatibility** (Linux, macOS, Windows)

Configuration is in `pyproject.toml`.

### Common Formatting/Linting Issues

**Formatting issues:** Black auto-formats code, so most style issues (line length,
spacing, indentation) can be fixed automatically:
```bash
make format
# or
black .
```

**Linting issues:** Ruff checks for the `E`, `F`, and `W` rule sets (with a few
research-notebook-friendly exceptions ignored — see `pyproject.toml`, e.g. unused
imports/variables and line length, since black already handles wrapping). Run it
directly to see what needs fixing:
```bash
ruff check .
```

## Types of Contributions

### Bug Fixes
- Fix typos or errors in lectures
- Correct broken code examples
- Fix broken links

### Content Improvements
- Improve explanations or examples
- Add missing context or details
- Update outdated information

### New Features
- Add new exercises or examples
- Enhance existing content
- Propose new lecture topics (discuss in an issue first)

## Development Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** to `.py` files

3. **Test locally:**
   ```bash
   # Check syntax
   python -m py_compile lecture_XX/lecture_XX.py
   
   # Check formatting and lint
   black --check lecture_XX/lecture_XX.py
   ruff check lecture_XX/lecture_XX.py
   
   # Convert to notebook
   make convert
   
   # Execute notebook
   jupyter nbconvert --to notebook --execute --inplace lecture_XX/lecture_XX.ipynb
   ```

4. **Run full CI checks:**
   ```bash
   make ci-local
   ```

5. **Commit with a clear message:**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

6. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Pull Request Process

1. **Describe your changes** clearly in the PR description
2. **Link related issues** if applicable
3. **Wait for CI checks** to pass (required)
4. **Respond to review feedback** promptly
5. **Squash commits** if requested

All PRs must pass CI checks before merging.

## Adding Dependencies

When adding new dependencies:

1. **Add to `environment.yml`**

2. **Test the dependency:**
   ```bash
   make test-deps
   ```

3. **Document why** the dependency is needed

## Documentation Updates

When making changes, update the relevant documentation:

- **README.md** - High-level changes visible to students
- **docs/DEVELOPER_GUIDE.md** - Technical details for developers
- **docs/DEPENDENCY_MANAGEMENT.md** - Dependency-related changes
- **Lecture docstrings** - Content changes in lectures

## Getting Help

- **For development questions:** See [docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)
- **For dependency issues:** See [docs/QUICKSTART.md](docs/QUICKSTART.md)
- **For other questions:** Open an issue on GitHub

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on improving the course materials

## License

By contributing, you agree that your contributions will be licensed under:
- **CC BY 4.0** for educational content
- **MIT License** for code examples

See [LICENSE](LICENSE) for details.

## Recognition

Contributors are recognized in:
- Git commit history
- Pull request acknowledgments
- Course acknowledgments (for significant contributions)

Thank you for contributing to making research software engineering education better!
