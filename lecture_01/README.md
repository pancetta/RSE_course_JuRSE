# Lecture 1: Introduction to Research Software Engineering

## Overview
This introductory lecture provides an overview of Research Software Engineering (RSE) and sets the stage for the entire course. You'll learn what RSE is, why it's important for modern research, and how to get started with this course.

**Duration**: ~90 minutes

## Topics Covered
- What is Research Software Engineering (RSE)?
- Why RSE is important for modern research
- Structure and content of this course
- How to access and install course materials
- Introduction to essential tools:
  - Working with the shell/command line
  - Version control with Git
  - Collaboration with GitHub

## Files
- `lecture_01.py` - Main lecture content in Jupytext format

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
cd lecture_01
jupytext --to notebook lecture_01.py
jupyter notebook lecture_01.ipynb
```

Or from the main repository directory:
```bash
make convert
jupyter notebook
```
