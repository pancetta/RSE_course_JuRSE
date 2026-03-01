# Lecture 8: Documenting and Publishing Research Software

## Overview
This lecture teaches you how to document research software effectively and share it with the scientific community. You'll learn about documentation tools, licensing, and how to make your research software citable and reusable.

**Duration**: ~90 minutes

## Topics Covered
- Why documentation matters for research impact
- Writing effective README files
- NumPy-style docstrings for Python
- Generating API documentation with Sphinx
- Choosing software licenses
- Publishing Python packages to PyPI
- Making software citable with DOIs (Zenodo)
- Submitting to Journal of Open Source Software (JOSS)
- Documentation tools for other programming languages

## Key Concepts
- **Documentation hierarchy**: README, docstrings, API docs, tutorials, citation
- **NumPy-style docstrings**: Standard format for scientific Python
- **Sphinx**: Documentation generator used by NumPy, SciPy, pandas
- **Read the Docs**: Free hosting for open-source documentation
- **Software licenses**: MIT, Apache, GPL, BSD explained
- **PyPI**: Python Package Index for distribution
- **DOI**: Digital Object Identifier for permanent citations
- **CITATION.cff**: Standard format for software citation

## Real-World Example
The lecture follows the story of Dr. Sarah Chen, who transformed her research software from having zero external users to becoming widely cited by adding comprehensive documentation. This illustrates the concrete impact of good documentation on research.

## Documentation Tools Covered

### For Python
- **Sphinx**: API documentation generation
- **Read the Docs**: Documentation hosting
- **PyPI**: Package distribution
- **Zenodo**: DOI assignment

### For Other Languages
- **C/C++**: Doxygen
- **Java**: Javadoc
- **R**: roxygen2, pkgdown
- **Julia**: Documenter.jl
- **Fortran**: FORD
- **Rust**: rustdoc
- **JavaScript/TypeScript**: JSDoc, TypeDoc
- **Go**: godoc
- **MATLAB**: Built-in help system

## License Selection Tools
The lecture introduces practical tools for choosing appropriate licenses:
- **Choose a License** (https://choosealicense.com/) - GitHub's decision guide
- **TL;DR Legal** (https://www.tldrlegal.com/) - Plain English summaries
- **OSI License List** (https://opensource.org/licenses/) - Official open source licenses

Recommendation: **MIT License** for most research software (maximum reuse and impact)

## Files
- `lecture_08.py` - Main lecture content in Jupytext format

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
cd lecture_08
jupytext --to notebook lecture_08.py
jupyter notebook lecture_08.ipynb
```

Or from the main repository directory:
```bash
make convert
jupyter notebook
```

## No Exercises
This lecture does not include separate exercises. Instead, it provides comprehensive examples and templates that can be directly applied to students' own research projects.

## Complete Examples Included
- README template for research software
- NumPy-style docstring examples with all sections
- Sphinx configuration (conf.py)
- pyproject.toml for modern Python packaging
- CITATION.cff example
- License selection guidance

## Connection to Previous Lectures
- **Lecture 5**: Testing - now you know how to document tested code
- **Lecture 6**: CI/CD - documentation builds can be automated
- **Lecture 7**: Debugging - good docs help others debug your code

## Learning Outcomes
After this lecture, students will be able to:
- Write comprehensive README files
- Add NumPy-style docstrings to Python functions
- Choose appropriate open-source licenses
- Understand how to publish packages to PyPI
- Make software citable with DOIs
- Apply documentation principles in other programming languages

## References
This lecture draws on:
- Write the Docs community best practices
- Sphinx and Read the Docs documentation
- Python Packaging User Guide
- FORCE11 Software Citation Principles
- Language-specific documentation tools (Doxygen, roxygen2, etc.)

All references are real and cited in the lecture acknowledgements.
