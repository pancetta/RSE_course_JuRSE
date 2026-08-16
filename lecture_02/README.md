# Lecture 2: Advanced Git, GitHub, GitLab, and Python Concepts for RSE

## Overview
This lecture builds on Git fundamentals from Lecture 1 and introduces collaboration with GitHub
and GitLab. It then reviews the Python concepts—error handling, the `with` statement,
comprehensions, and classes—that you'll need to follow the rest of this course. This is not a
Python introduction: the course assumes you can already read Python and have written at least a
little of it before (see the [course prerequisites](../README.md)).

**Duration**: ~90 minutes

## Topics Covered
- Advanced Git: branching, merging, and conflict resolution
- .gitignore patterns and file management
- GitHub collaboration: forking, pull requests, and remotes
- GitLab collaboration: forking, merge requests, and GitHub/GitLab comparison
- Error handling: exception types, try/except, raising exceptions
- The `with` statement and context managers
- List and dictionary comprehensions
- Classes and object-oriented programming basics

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
