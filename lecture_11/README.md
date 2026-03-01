# Lecture 11: Working with Research Data - File Formats and Databases

## Overview
Research data is at the heart of scientific discovery. How you store, access, and share your data can make the difference between reproducible science and lost knowledge. This lecture explores best practices for managing research data through appropriate file formats and storage solutions. We'll ground our discussion in the FAIR principles (Findable, Accessible, Interoperable, Reusable) and demonstrate practical implementations with real-world examples.

**Duration**: ~90 minutes

## Topics Covered
- FAIR principles and their application to research data
- Research Data Management (RDM) best practices
- FAIR4RS principles for research software
- Choosing appropriate file formats for different data types
- Working with scientific file formats (HDF5, NetCDF)
- Using databases effectively for structured research data
- Data validation and integrity checking
- Applying these concepts across different programming languages

## Key Concepts
- **FAIR Principles**: Findable, Accessible, Interoperable, Reusable
- **Research Data Management (RDM)**: Systematic organization and maintenance of data
- **FAIR4RS**: FAIR principles adapted for research software
- **HDF5**: Hierarchical data format for large numerical datasets
- **NetCDF**: Network Common Data Form for array-oriented scientific data
- **Data Management Plan (DMP)**: Structured approach to data lifecycle
- **Persistent identifiers**: DOIs and other permanent references

## Prerequisites

Before starting this lecture, you should be familiar with:
- Python file I/O operations (covered in Lecture 3)
- NumPy for numerical data (covered in Lecture 4)
- Basic understanding of data analysis workflows
- Pandas basics (helpful but not required)

This lecture introduces research data management best practices and specialized file formats.

## Learning Objectives
- Understand FAIR principles and their application to research data
- Learn about Research Data Management (RDM) best practices
- Recognize FAIR4RS principles for research software
- Choose appropriate file formats for different data types
- Work with scientific file formats (HDF5, NetCDF)
- Use databases effectively for structured research data
- Implement data validation and integrity checking
- Apply these concepts across different programming languages

## Files
- `lecture_11.py` - Main lecture content in Jupytext format

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
cd lecture_11
jupytext --to notebook lecture_11.py
jupyter notebook lecture_11.ipynb
```

Or from the main repository directory:
```bash
make convert
jupyter notebook
```

## The Cautionary Tale
The lecture opens with a story about lost research data, illustrating why proper data management practices are critical for reproducible science.

## Practical Examples
The lecture includes hands-on examples with:
- CSV, JSON, and Excel files
- HDF5 for large numerical datasets
- NetCDF for climate and atmospheric data
- SQLite databases for structured data
- Pandas DataFrames for data manipulation
