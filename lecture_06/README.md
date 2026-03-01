# Lecture 6: Automation and Continuous Integration

## Overview
This lecture teaches you how to automate testing and ensure code quality through Continuous Integration (CI). Building on the testing knowledge from Lecture 5, you'll learn how to set up automated testing that would have prevented the research disaster from the previous lecture.

**Duration**: ~90 minutes

## Topics Covered
- What Continuous Integration (CI) is and why it matters
- Setting up automated testing with GitHub Actions
- Configuring CI workflows for GitLab
- Building reproducible research pipelines
- Automating code quality checks
- Best practices for CI in research software
- Complete workflow examples for research projects

## Key Concepts
- **Continuous Integration (CI)**: Automated testing on every code change
- **GitHub Actions**: GitHub's built-in CI/CD platform
- **GitLab CI**: GitLab's CI/CD system
- **Workflows**: Automated processes triggered by events
- **Matrix builds**: Testing across multiple Python versions and operating systems
- **Research pipelines**: Automating data validation and analysis

## GitHub Actions vs GitLab CI
The lecture covers both platforms:
- **GitHub Actions**: For public repositories on GitHub
- **GitLab CI**: For GitLab and self-hosted instances (common in universities)

Both are covered with practical examples and comparisons.

## Files
- `lecture_06.py` - Main lecture content in Jupytext format

## Running the Lecture

1. Create and activate the environment:
```bash
cd /path/to/RSE_lecture
make install
micromamba activate rse_lecture
```

Or manually:
```bash
micromamba env create -f environment.yml
micromamba activate rse_lecture
```

2. Convert to notebook and run:
```bash
cd lecture_06
jupytext --to notebook lecture_06.py
jupyter notebook lecture_06.ipynb
```

Or from the main repository directory:
```bash
make convert
jupyter notebook
```

## Workflow Examples
The lecture includes complete, production-ready workflow examples:
- Basic test automation
- Multi-platform testing (Linux, Windows, macOS)
- Multi-version testing (Python 3.9-3.12)
- Code quality checks (linting, formatting)
- Research-specific pipelines (notebook execution, data validation)
- GitLab CI equivalents for all GitHub Actions examples

## No Exercises
Like Lecture 5, this lecture does not include separate exercises. Instead, it provides comprehensive, copy-paste-ready workflow configurations that students can adapt for their own projects.

## Connection to Lecture 5
This lecture directly builds on Lecture 5's cautionary tale, showing how CI automation would have prevented the temperature conversion disaster. The same example code is used to demonstrate CI workflows.
