# Lecture 5: Testing Research Software

## Overview
This lecture introduces software testing practices essential for reliable research software. Following a cautionary tale of a research project that produced incorrect results due to untested code, you'll learn how to prevent such disasters through systematic testing with pytest.

**Duration**: ~90 minutes

## Topics Covered
- Why testing is critical for research software (with a scary cautionary tale)
- Writing unit tests using pytest
- Understanding and using assertions for defensive programming
- Measuring test coverage with pytest-cov
- Applying Test-Driven Development (TDD) principles
- Building comprehensive test suites
- Complete example: from buggy code to full test coverage
- Critically evaluating whether an AI-generated test actually verifies correct behavior

## Key Concepts
- **Unit testing**: Testing individual functions in isolation
- **Test-Driven Development (TDD)**: Write tests before implementation
- **Test coverage**: Measuring which code is tested
- **Assertions**: Preconditions, postconditions, and invariants
- **Defensive programming**: Making code fail fast and clearly

## Files
- `lecture_05.py` - Main lecture content in Jupytext format

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
cd lecture_05
jupytext --to notebook lecture_05.py
jupyter notebook lecture_05.ipynb
```

Or from the main repository directory:
```bash
make convert
jupyter notebook
```

## The Cautionary Tale
The lecture opens with a fictional but realistic story of a climate research team that published incorrect results due to a bug in their temperature conversion code. This serves as motivation for why testing matters in research software.

## No Exercises
Unlike previous lectures, this lecture does not include separate exercises. The entire lecture is structured as a hands-on walkthrough, building from broken code to fully tested, reliable code.
