# Lecture 3: Python Fundamentals and Advanced Concepts

## Overview
This lecture deepens your Python knowledge by covering advanced function concepts,
error handling, file I/O, and functional programming techniques. These skills are
essential for writing robust, maintainable research software.

**Duration**: ~90 minutes

## Topics Covered
- Advanced function concepts (default parameters, keyword arguments, lambda functions)
- Comprehensive function documentation (NumPy docstring style)
- Error handling with try/except blocks
- Raising and catching different exception types
- File input/output (text files, CSV data)
- List comprehensions and dictionary comprehensions
- Command-line scripts with argparse
- Functional programming concepts (map, filter, lambda)
- Practical examples for research software

## Files
- `lecture_03.py` - Main lecture content in Jupytext format

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
cd lecture_03
jupytext --to notebook lecture_03.py
jupyter notebook lecture_03.ipynb
```

Or from the main repository directory:
```bash
make convert
jupyter notebook
```
