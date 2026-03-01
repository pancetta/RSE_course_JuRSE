# Lecture 4: Python Project Structure and Scientific Libraries

## Overview
This lecture teaches you how to organize research code into professional Python projects and introduces essential scientific computing libraries. You'll learn best practices for structuring projects and gain hands-on experience with NumPy and Matplotlib, the foundational tools for numerical computing and visualization.

**Duration**: ~90 minutes

## Topics Covered

### Part 1: Python Project Structure (30 minutes)
- Why project structure matters for research software
- Anatomy of a research Python project
- Understanding modules and packages
- The `__init__.py` file and its uses
- Managing dependencies with `requirements.txt` and `environment.yml`
- Virtual environments: why they matter and how to use them
- `setup.py` basics for making installable packages

### Part 2: Working with NumPy (30 minutes)
- Why NumPy for scientific computing
- Creating arrays: `np.array()`, `np.arange()`, `np.linspace()`, `np.zeros()`, `np.ones()`
- Vectorized array operations
- Indexing and slicing techniques
- Boolean indexing for filtering data
- Statistical operations: mean, std, min, max, median, percentiles
- 2D arrays and multi-dimensional operations
- Practical examples with experimental data

### Part 3: Visualization with Matplotlib (30 minutes)
- Why visualization matters in research
- Basic plots: line plots and scatter plots
- Customizing plots: colors, markers, line styles
- Multiple lines and legends
- Creating subplots for complex figures
- Different plot types: bar, histogram, box plot, heatmap
- Saving figures in various formats (PNG, PDF, SVG)
- Best practices for publication-quality figures

## Files
- `lecture_04.py` - Main lecture content in Jupytext format

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
cd lecture_04
jupytext --to notebook lecture_04.py
jupyter notebook lecture_04.ipynb
```

Or from the main repository directory:
```bash
make convert
jupyter notebook
```

## Practice Exercises

1. **Project Structure**: Create a research project with proper structure including `src/`, `tests/`, `data/`, and `notebooks/` directories

2. **NumPy Practice**: Analyze a matrix of experimental data:
   - Load or create a 10×5 matrix (10 samples, 5 measurements)
   - Calculate statistics per sample and per measurement
   - Identify outliers using boolean indexing
   - Normalize data to mean=0, std=1

3. **Matplotlib Practice**: Create a publication-quality figure:
   - Generate synthetic data with noise
   - Create subplots showing raw data, processed data, and distribution
   - Add proper labels, legends, and styling
   - Save as both PNG (300 DPI) and PDF

4. **Integrated Project**: Build a complete analysis pipeline:
   - Structure: Organize into proper package
   - Data: Generate or load experimental data (NumPy)
   - Analysis: Calculate statistics, fit models
   - Visualization: Create comprehensive figures (Matplotlib)
   - Documentation: Add README and docstrings

## Additional Resources

### Documentation
- [NumPy Documentation](https://numpy.org/doc/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [Python Packaging Guide](https://packaging.python.org/)

### Tutorials
- [NumPy Tutorial on SciPy Lectures](http://scipy-lectures.org/intro/numpy/)
- [Matplotlib Tutorial](https://matplotlib.org/stable/tutorials/index.html)
- [Real Python: NumPy](https://realpython.com/numpy-tutorial/)
