# Lecture 2: Advanced Git, GitHub, and Python Basics

## Overview
This lecture builds on Git fundamentals from Lecture 1, introduces collaboration with GitHub,
and begins our journey into Python programming. We'll learn advanced version control workflows
and start writing our first Python code.

**Duration**: ~90 minutes

## Topics Covered
- Advanced Git: branching, merging, and conflict resolution
- .gitignore patterns and file management
- GitHub collaboration: forking, pull requests, and remotes
- Python fundamentals (variables, data types, strings)
- Python collections (lists, dictionaries)
- Control flow (if statements, for loops, while loops)
- Basic functions and documentation
- Practical examples combining Git and Python

## Files
- `lecture_02.py` - Main lecture content in Jupytext format

## Additional Dependencies
This lecture uses only the base dependencies (no additional packages required beyond Python standard library)

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
cd lecture_02
jupytext --to notebook lecture_02.py
jupyter notebook lecture_02.ipynb
```

Or from the main repository directory:
```bash
make convert
jupyter notebook
```
