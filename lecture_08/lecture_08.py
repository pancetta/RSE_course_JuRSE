# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Lecture 8: Documenting and Publishing Research Software
#
#
# ## Quick Access
#
# Scan the QR codes below for quick access to course materials:
#
# <div style="display: flex; gap: 20px; align-items: flex-start;">
#   <div style="text-align: center;">
#     <img src="../course_qr_code.png" alt="Course Website QR Code" width="150"/>
#     <p><strong>Course Website</strong></p>
#   </div>
#   <div style="text-align: center;">
#     <img src="lecture_08_qr_code.png" alt="This Lecture QR Code" width="150"/>
#     <p><strong>This Lecture</strong></p>
#   </div>
# </div>
#
# ## Overview
# This lecture teaches you how to document research software effectively and share it with
# the scientific community. Good documentation makes your research reproducible, your software
# reusable, and your work citable. We'll explore documentation tools, best practices, and how
# to publish research software so others can build upon your work.
#
# **Duration**: ~90 minutes
#
# ## Prerequisites
#
# Before starting this lecture, you should be familiar with:
# - Python programming and project structure (covered in Lectures 2 and 4)
# - Git and GitHub basics (covered in Lectures 1-2)
# - Writing functions and docstrings (covered in Lecture 2)
# - Organizing code into packages and modules
# - AI-assisted coding basics, including reviewing AI suggestions like a diff (covered in
#   Lecture 3)
#
# This lecture builds on your programming knowledge by teaching how to document and share it effectively.
#
# ## Learning Objectives
# - Understand why documentation is critical for research impact
# - Write effective README files and docstrings
# - Generate API documentation with Sphinx
# - Choose appropriate software licenses
# - Publish Python packages to PyPI
# - Make research software citable with DOIs
# - Learn documentation tools for other programming languages
# - Verify AI-drafted documentation against actual code behavior, not just against what the
#   function name suggests

# %% [markdown]
# ## Part 1: Why Documentation Matters - A Real Research Story
#
# ### The Problem: Great Code, Zero Impact
#
# Dr. Sarah Chen spent two years developing a novel algorithm for analyzing genomic sequences.
# Her method was 10x faster than existing approaches and produced more accurate results. She
# published a paper describing the algorithm in a prestigious journal.
#
# Six months later, she had received:
# - **3 citations** - all from her own research group
# - **2 emails** - asking "where is the code?"
# - **0 external users** - nobody could figure out how to use it
#
# She had published the code on GitHub, but the repository contained:
# - No README file explaining what the code does
# - No installation instructions
# - Function names like `proc_data_v3_final_ACTUAL()`
# - No docstrings or comments
# - No examples of how to use it
# - No license file
#
# **Result**: Her breakthrough work had nearly zero impact because nobody could use it.
#
# ### The Transformation
#
# After attending a research software engineering workshop, Sarah spent **one week** adding:
# - A comprehensive README with installation steps
# - Google-style docstrings for all functions
# - Sphinx-generated API documentation hosted on Read the Docs
# - A tutorial Jupyter notebook with examples
# - A clear license (MIT)
# - A DOI from Zenodo for citation
#
# One year later:
# - **47 citations** - from researchers worldwide
# - **12 contributors** - improving and extending her code
# - **3 follow-up papers** - building on her work
# - **1 job offer** - from a biotech company impressed by her code quality
#
# **The lesson**: Good documentation transforms code from "works on my machine" to "works for science."

# %% [markdown]
# ## Part 2: The Documentation Hierarchy
#
# ### Different Documentation for Different Audiences
#
# Research software needs multiple types of documentation:
#
# **1. README** - First impression (5 minutes to convince someone to try your code)
# - What does this software do?
# - Why should I use it?
# - How do I install it?
# - Quick example of basic usage
#
# **2. Installation Guide** - Getting started (detailed setup instructions)
# - Prerequisites and dependencies
# - Step-by-step installation
# - Verification that it works
# - Troubleshooting common issues
#
# **3. Tutorials** - Learning by doing (complete examples)
# - Real-world use cases
# - Step-by-step walkthroughs
# - Expected output shown
# - Jupyter notebooks work great here!
#
# **4. API Documentation** - Reference material (what each function does)
# - Function parameters and return values
# - Examples for each function
# - Auto-generated from docstrings
#
# **5. Contributing Guide** - For collaborators
# - How to contribute code
# - Coding standards
# - How to run tests
# - Pull request process
#
# **6. Citation Guide** - For academic users
# - How to cite your software
# - BibTeX entry
# - DOI for specific versions

# %% [markdown]
# ## Part 3: Writing an Effective README
#
# ### The README is Your Software's First Impression
#
# A good README answers these questions in order:
# 1. **What** is this?
# 2. **Why** should I care?
# 3. **How** do I use it?
# 4. **Where** can I learn more?
#
# ### README Template for Research Software

# %% [markdown]
# ```markdown
# # GenomeAnalyzer - Fast Genomic Sequence Analysis
#
# [![Tests](https://github.com/username/genomeanalyzer/workflows/Tests/badge.svg)](https://github.com/username/genomeanalyzer/actions)
# [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.1234567)
# [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
#
# ## Overview
#
# GenomeAnalyzer provides fast, accurate analysis of genomic sequences using
# a novel algorithm based on wavelet transforms. It's 10x faster than existing
# tools while maintaining 99.9% accuracy.
#
# **Key Features:**
# - Process genome sequences in minutes, not hours
# - Handles FASTA, FASTQ, and custom formats
# - Parallel processing for multi-core systems
# - Extensive validation on 1000+ genomes
#
# ## Installation
#
# ### Using pip (recommended)
# ```bash
# pip install genomeanalyzer
# ```
#
# ### From source
# ```bash
# git clone https://github.com/username/genomeanalyzer.git
# cd genomeanalyzer
# pip install -e .
# ```
#
# ## Quick Start
#
# ```python
# from genomeanalyzer import analyze_sequence
#
# # Analyze a sequence
# result = analyze_sequence('genome.fasta')
# print(f"Found {result.num_variants} variants")
# ```
#
# ## Documentation
#
# Full documentation available at: https://genomeanalyzer.readthedocs.io
#
# ## Citation
#
# If you use this software in your research, please cite:
#
# ```bibtex
# @software{chen2024genome,
#   author = {Chen, Sarah},
#   title = {GenomeAnalyzer: Fast Genomic Sequence Analysis},
#   year = {2024},
#   doi = {10.5281/zenodo.1234567},
#   url = {https://github.com/username/genomeanalyzer}
# }
# ```
#
# ## License
#
# This project is licensed under the MIT License - see LICENSE file for details.
#
# ## Contact
#
# - Issues: https://github.com/username/genomeanalyzer/issues
# - Email: sarah.chen@university.edu
# ```

# %% [markdown]
# ### Key README Elements Explained
#
# **Badges at the top** - Show project status at a glance
# - CI/CD status (tests passing?)
# - Code coverage (how much is tested?)
# - DOI (citable version?)
# - License (can I use it?)
# - Version (what's the latest?)
#
# **Clear description** - Don't assume people know your field
# - What problem does this solve?
# - Why is it better than alternatives?
# - Who is it for?
#
# **Installation that works** - Test these instructions!
# - Multiple installation methods
# - Prerequisites clearly stated
# - OS-specific notes if needed
#
# **Working example** - Show success quickly
# - Copy-paste ready code
# - Uses realistic data
# - Shows actual output

# %% [markdown]
# ## Part 4: Writing Good Docstrings
#
# ### What is a Docstring?
#
# A **docstring** is documentation embedded in your code that explains what a function,
# class, or module does. Python docstrings go in triple quotes right after the definition.
#
# ### Why Docstrings Matter
#
# - **Self-documenting code**: The documentation lives with the code
# - **IDE support**: Editors can show docstrings as help text
# - **Auto-generation**: Tools like Sphinx can generate API docs from docstrings
# - **Helps future you**: You'll forget what your code does in 6 months
#
# ### Docstring Styles
#
# Three popular styles in Python:
#
# **1. NumPy/SciPy Style** - Popular in scientific computing
#
# **2. Google Style** - Clean, readable, less verbose
#
# **3. reStructuredText (Sphinx)** - More detailed, complex syntax
#
# **We'll focus on NumPy style** - it's standard in scientific Python.

# %% [markdown]
# ## Part 5: NumPy-Style Docstrings - A Complete Example
#
# ### Example: Temperature Analysis Module
#
# Let's document a realistic research code using NumPy-style docstrings:

# %%
"""
Temperature Analysis Module

This module provides functions for analyzing temperature data from climate models.
It includes unit conversion, anomaly calculation, and statistical analysis.

Examples
--------
>>> import numpy as np
>>> from temperature_analysis import calculate_anomaly
>>> temps = np.array([32.5, 33.0, 34.2, 35.1])
>>> baseline = 32.0
>>> anomalies = calculate_anomaly(temps, baseline)
"""


def celsius_to_fahrenheit(celsius):
    """
    Convert temperature from Celsius to Fahrenheit.

    Parameters
    ----------
    celsius : float or array_like
        Temperature in degrees Celsius.

    Returns
    -------
    float or ndarray
        Temperature in degrees Fahrenheit.

    Examples
    --------
    >>> celsius_to_fahrenheit(0)
    32.0
    >>> celsius_to_fahrenheit(100)
    212.0
    >>> celsius_to_fahrenheit(-40)
    -40.0

    Notes
    -----
    The conversion formula is: F = C × 9/5 + 32

    See Also
    --------
    fahrenheit_to_celsius : Inverse conversion
    """
    return celsius * 9 / 5 + 32


def calculate_anomaly(temperatures, baseline, method="mean"):
    """
    Calculate temperature anomalies relative to a baseline.

    Temperature anomalies represent deviations from a reference temperature,
    commonly used in climate science to track warming or cooling trends.

    Parameters
    ----------
    temperatures : array_like
        Temperature measurements in the same units as baseline.
        Must be 1-D array.
    baseline : float
        Reference temperature for anomaly calculation.
        Must be in same units as temperatures.
    method : {'mean', 'median'}, optional
        Method for calculating baseline anomaly. Default is 'mean'.

        - 'mean' : Use arithmetic mean of temperatures
        - 'median' : Use median of temperatures

    Returns
    -------
    ndarray
        Temperature anomalies (temperatures - baseline).
        Same shape as input temperatures.

    Raises
    ------
    ValueError
        If temperatures is empty or method is invalid.
    TypeError
        If temperatures cannot be converted to array.

    Examples
    --------
    >>> import numpy as np
    >>> temps = np.array([32.5, 33.0, 34.2, 35.1])
    >>> calculate_anomaly(temps, 32.0)
    array([0.5, 1. , 2.2, 3.1])

    >>> calculate_anomaly(temps, 33.0, method='median')
    array([-0.5,  0. ,  1.2,  2.1])

    Notes
    -----
    This function is commonly used in climate analysis to identify
    warming or cooling trends relative to a historical baseline period.

    The anomaly is calculated as:

    .. math:: A_i = T_i - T_{baseline}

    where :math:`A_i` is the anomaly for measurement i, and
    :math:`T_i` is the temperature measurement.

    References
    ----------
    .. [1] Jones, P.D., et al. "Surface air temperature and its changes
           over the past 150 years." Reviews of Geophysics, 1999.

    See Also
    --------
    numpy.mean : Calculate arithmetic mean
    numpy.median : Calculate median value
    """
    import numpy as np

    # Input validation
    temps = np.asarray(temperatures)
    if temps.size == 0:
        raise ValueError("temperatures array cannot be empty")

    if method not in ["mean", "median"]:
        raise ValueError(f"method must be 'mean' or 'median', got '{method}'")

    # Calculate anomalies
    anomalies = temps - baseline

    return anomalies


# Test the functions
print("Testing temperature functions:")
print(f"0°C = {celsius_to_fahrenheit(0)}°F")
print(f"100°C = {celsius_to_fahrenheit(100)}°F")

temps = [32.5, 33.0, 34.2, 35.1]
anomalies = calculate_anomaly(temps, 32.0)
print(f"Anomalies: {anomalies}")

# %% [markdown]
# ### NumPy Docstring Sections Explained
#
# A complete NumPy-style docstring includes:
#
# **1. Short Summary** (one line)
# - Imperative mood: "Calculate..." not "Calculates..."
# - Complete sentence with period
# - Fits in one line (< 80 characters)
#
# **2. Extended Summary** (optional, after blank line)
# - More detailed explanation
# - Context and use cases
# - Multiple paragraphs OK
#
# **3. Parameters Section**
# ```
# Parameters
# ----------
# param_name : type
#     Description of parameter.
#     Can span multiple lines.
# ```
#
# **4. Returns Section**
# ```
# Returns
# -------
# type
#     Description of return value.
# ```
#
# **5. Examples Section** - Most important!
# ```
# Examples
# --------
# >>> function_call()
# expected_output
# ```
#
# **6. Other Useful Sections**
# - **Raises**: What exceptions can be raised
# - **See Also**: Related functions
# - **Notes**: Additional details, algorithms, math
# - **References**: Academic citations
# - **Warnings**: Important caveats

# %% [markdown]
# ### Docstring Best Practices for Research Code
#
# **Do:**
# - ✅ Include working examples with expected output
# - ✅ Document scientific assumptions and limitations
# - ✅ Cite papers for algorithms implemented
# - ✅ Explain mathematical notation used
# - ✅ Note units for physical quantities
# - ✅ Keep examples copy-paste ready
#
# **Don't:**
# - ❌ Just restate the function name
# - ❌ Leave out units (temperature in what? Celsius? Kelvin?)
# - ❌ Assume domain knowledge
# - ❌ Use jargon without explanation
# - ❌ Write docstrings that lie about what code does

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Documentation is a gift to your future self—invest in it now!</p>
#     <ul>
#         <li><strong>Document your research functions:</strong> Pick 5 key functions from
#         your current project and write complete NumPy-style docstrings with parameters,
#         returns, examples, and scientific references—see how it clarifies your own
#         thinking.</li>
#         <li><strong>Build Sphinx documentation:</strong> Set up Sphinx for your project,
#         configure autodoc to extract docstrings, add a tutorial page, and deploy to Read
#         the Docs—create professional documentation website for free.</li>
#         <li><strong>Add usage examples:</strong> Write docstring examples that users can
#         copy-paste and run immediately—test them with doctest to ensure they stay
#         up-to-date as code evolves.</li>
#     </ul>
# </div>

# %% [markdown]
# ### AI and Documentation
#
# AI assistants are genuinely good at drafting documentation—a first-pass README section or
# docstring is one of the safer, higher-value things to ask for, usually lower-risk than asking
# for the logic itself. What they're not automatically good at is checking the draft against
# reality: an AI assistant tends to describe what a function's name and structure *suggest* it
# does, not necessarily what the code *actually* does. If there's a mismatch, the AI won't spot
# it—it has no way to know your code has a bug.
#
# Consider a function that filters out invalid sensor readings:


# %%
def get_valid_readings(readings):
    """Return all valid (non-negative) sensor readings."""
    return [r for r in readings if r > 0]


# %% [markdown]
# That docstring is exactly the kind of plausible, well-formatted summary an AI assistant might
# generate from the function's name and code—"non-negative" is a reasonable reading of
# `if r > 0`. Let's check it against a case that includes a boundary value:

# %%
readings = [0.0, -1.5, 5.2, 10.0]
print(f"Input:  {readings}")
print(f"Output: {get_valid_readings(readings)}")

# %% [markdown]
# `0.0` is non-negative, but it's missing from the output—the code checks `r > 0`, not
# `r >= 0`, so it silently excludes exactly the boundary case the docstring claims to include.
# The docstring isn't lying, exactly; it's describing the *intent* the name suggests, not the
# *behavior* the code delivers. The same review habit from Lecture 3 applies to documentation
# just as much as to code: check what's claimed against what actually happens, especially at
# the boundaries.
#
# **How prompting helps (but doesn't replace review)**: giving the AI a boundary case
# explicitly—"write a docstring for this function, and confirm what it returns when a reading
# is exactly 0"—forces it to check the behavior instead of paraphrasing the name. That catches
# more mismatches than a bare "document this function" request. It still won't catch every
# discrepancy, so the check above is worth doing regardless of how the prompt was written.

# %% [markdown]
# ## Part 6: Generating Documentation with Sphinx
#
# ### What is Sphinx?
#
# **Sphinx** is the standard tool for generating beautiful documentation from Python code.
# It reads your docstrings and creates a professional website automatically.
#
# **Used by**: NumPy, SciPy, pandas, matplotlib, scikit-learn, and thousands more.
#
# ### Sphinx Features
#
# - **Auto-generation**: Extracts docstrings from your code
# - **Cross-references**: Links between functions and classes
# - **Math support**: LaTeX equations in documentation
# - **Code highlighting**: Beautiful syntax highlighting
# - **Multiple formats**: HTML, PDF, ePub
# - **Themes**: Professional-looking templates
# - **Extensions**: Plots, bibliography, todo lists, more
#
# ### Setting Up Sphinx for a Project
#
# Here's a complete example of setting up documentation:

# %% [markdown]
# ```bash
# # Create a new project structure
# my_research_package/
# ├── src/
# │   └── my_package/
# │       ├── __init__.py
# │       └── analysis.py
# ├── docs/
# │   ├── source/
# │   │   ├── conf.py          # Sphinx configuration
# │   │   ├── index.rst        # Documentation home page
# │   │   └── api.rst          # API reference
# │   └── Makefile
# ├── tests/
# ├── README.md
# └── setup.py
#
# # Install Sphinx
# pip install sphinx sphinx-rtd-theme
#
# # Initialize Sphinx documentation
# cd docs
# sphinx-quickstart
#
# # Build documentation
# make html
#
# # View in browser
# open build/html/index.html
# ```

# %% [markdown]
# ### Example Sphinx Configuration (conf.py)
#
# ```python
# # docs/source/conf.py
#
# # Project information
# project = 'GenomeAnalyzer'
# copyright = '2024, Sarah Chen'
# author = 'Sarah Chen'
# version = '1.0'
# release = '1.0.0'
#
# # Extensions for auto-documentation
# extensions = [
#     'sphinx.ext.autodoc',      # Auto-generate from docstrings
#     'sphinx.ext.napoleon',     # Support NumPy/Google docstrings
#     'sphinx.ext.viewcode',     # Add source code links
#     'sphinx.ext.mathjax',      # Render math equations
#     'sphinx.ext.intersphinx',  # Link to other projects
# ]
#
# # Napoleon settings for NumPy-style docstrings
# napoleon_google_docstring = False
# napoleon_numpy_docstring = True
# napoleon_include_init_with_doc = True
# napoleon_use_param = True
# napoleon_use_rtype = True
#
# # HTML theme
# html_theme = 'sphinx_rtd_theme'  # Read the Docs theme
#
# # Paths
# import os
# import sys
# sys.path.insert(0, os.path.abspath('../..'))
# ```

# %% [markdown]
# ### Example Documentation Structure (index.rst)
#
# ```rst
# GenomeAnalyzer Documentation
# =============================
#
# Welcome to GenomeAnalyzer's documentation!
#
# .. toctree::
#    :maxdepth: 2
#    :caption: Contents:
#
#    installation
#    quickstart
#    tutorial
#    api
#    citing
#
# Overview
# --------
#
# GenomeAnalyzer provides fast genomic sequence analysis using
# novel wavelet transform algorithms.
#
# Key Features
# ------------
#
# * 10x faster than existing tools
# * Handles multiple file formats
# * Parallel processing support
# * Extensively validated
#
# Quick Example
# -------------
#
# .. code-block:: python
#
#    from genomeanalyzer import analyze_sequence
#
#    result = analyze_sequence('genome.fasta')
#    print(f"Found {result.num_variants} variants")
#
# Indices and tables
# ==================
#
# * :ref:`genindex`
# * :ref:`modindex`
# * :ref:`search`
# ```

# %% [markdown]
# ### Hosting Documentation on Read the Docs
#
# **Read the Docs** (https://readthedocs.org) provides free hosting for open-source documentation.
#
# **Setup steps:**
#
# 1. **Push code to GitHub** (or GitLab/Bitbucket)
#
# 2. **Create `.readthedocs.yml` in your repository:**
#    ```yaml
#    version: 2
#
#    build:
#      os: ubuntu-22.04
#      tools:
#        python: "3.11"
#
#    sphinx:
#      configuration: docs/source/conf.py
#
#    python:
#      install:
#        - requirements: docs/requirements.txt
#        - method: pip
#          path: .
#    ```
#
# 3. **Sign up at readthedocs.org** with your GitHub account
#
# 4. **Import your project** - automatic builds on every commit
#
# 5. **Your docs are live** at `https://your-project.readthedocs.io`
#
# **Benefits:**
# - Automatic rebuilds when you push code
# - Versioned documentation (different docs for each release)
# - Search functionality
# - PDF downloads
# - Free for open-source projects

# %% [markdown]
# ## Part 7: Choosing a Software License
#
# ### Why Your Code Needs a License
#
# **Without a license, your code is unusable by others** - even if it's on GitHub!
#
# Copyright law by default means:
# - **Nobody can use your code** (legally)
# - **Nobody can modify it**
# - **Nobody can distribute it**
# - **Nobody can build on it**
#
# This defeats the purpose of sharing research software. **Always add a license.**
#
# ### Common Licenses for Research Software
#
# **Permissive Licenses** - Minimal restrictions, maximum reuse
#
# **MIT License** ⭐ Most popular, simplest
# - ✅ Commercial use allowed
# - ✅ Modification allowed
# - ✅ Distribution allowed
# - ✅ Private use allowed
# - ⚠️ Must include license in copies
# - ⚠️ No warranty
# - **Good for**: Research software you want widely adopted
#
# **Apache 2.0** - Like MIT, but includes patent protection
# - ✅ Everything MIT allows
# - ✅ Explicit patent grant
# - ✅ Trademark protection
# - ⚠️ More complex than MIT
# - **Good for**: Projects involving patents or trademarks
#
# **BSD 3-Clause** - Similar to MIT, used by NumPy, SciPy
# - ✅ Very permissive
# - ✅ Name protection clause
# - **Good for**: Academic projects
#
# **Copyleft Licenses** - Require derivatives to be open source
#
# **GNU GPL v3** - Strong copyleft
# - ✅ Derivatives must be open source
# - ✅ Must use same license
# - ❌ Can't be combined with proprietary software
# - **Good for**: Ensuring all derivatives remain open
#
# **LGPL** - Lesser GPL, allows linking with proprietary code
# - **Good for**: Libraries used by both open and closed software
#
# **Public Domain**
#
# **CC0 / Unlicense** - Dedicate to public domain
# - ✅ No restrictions whatsoever
# - ❌ No legal protection for you
# - **Good for**: Reference implementations, data

# %% [markdown]
# ### How to Choose a License
#
# **Use these tools to help decide:**
#
# **1. Choose a License** (https://choosealicense.com/)
# - GitHub's official guide
# - Simple decision tree
# - Plain English explanations
# - Shows exactly what each license means
#
# **2. TL;DR Legal** (https://www.tldrlegal.com/)
# - License summaries in plain English
# - What you CAN, CANNOT, and MUST do
# - Compare licenses side-by-side
#
# **3. OSI License List** (https://opensource.org/licenses/)
# - Official list of open source licenses
# - Only licenses meeting Open Source Definition
#
# ### Recommendation for Research Software
#
# **For most research software, use MIT:**
# - Simple and well-understood
# - Maximum reuse and impact
# - Accepted by journals and funders
# - Compatible with nearly everything
# - Used by NumPy, scikit-learn, pandas
#
# **Use GPL if:**
# - You want to ensure derivatives stay open
# - Your funding requires it
# - You're extending GPL software
#
# ### Adding a License to Your Project
#
# **1. Create LICENSE file in repository root:**
# ```
# MIT License
#
# Copyright (c) 2024 Sarah Chen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# [... rest of MIT license text ...]
# ```
#
# **2. Add license badge to README:**
# ```markdown
# [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# ```
#
# **3. Include license in package metadata** (setup.py or pyproject.toml):
# ```python
# setup(
#     name='genomeanalyzer',
#     license='MIT',
#     # ...
# )
# ```

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Choosing the right license protects you and empowers others!</p>
#     <ul>
#         <li><strong>License your research code:</strong> Review your GitHub
#         repositories, choose appropriate licenses (MIT for permissive, GPL for copyleft,
#         or CC0 for public domain data), add LICENSE files, and update READMEs with
#         license badges.</li>
#         <li><strong>Understand license compatibility:</strong> Research which licenses can
#         be combined—learn why you can use MIT libraries in GPL projects but not vice
#         versa, and how this affects your research software dependencies.</li>
#         <li><strong>Add citation metadata:</strong> Create a CITATION.cff file for your
#         main project specifying how you want to be cited—make it easy for others to give
#         you proper academic credit.</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 8: Publishing Python Packages to PyPI
#
# ### What is PyPI?
#
# **PyPI** (Python Package Index, https://pypi.org) is the official repository for Python packages.
# It's where `pip install` gets packages from.
#
# **Why publish to PyPI?**
# - ✅ Users can install with `pip install your-package`
# - ✅ Automatic dependency management
# - ✅ Version control for releases
# - ✅ Increases visibility and citations
# - ✅ Professional presentation
#
# ### Package Structure
#
# A publishable package needs this structure:

# %% [markdown]
# ```
# genomeanalyzer/
# ├── src/
# │   └── genomeanalyzer/
# │       ├── __init__.py
# │       ├── analysis.py
# │       └── utils.py
# ├── tests/
# │   └── test_analysis.py
# ├── docs/
# ├── README.md
# ├── LICENSE
# ├── pyproject.toml          # Modern packaging config
# └── setup.py                # Traditional config (optional)
# ```

# %% [markdown]
# ### Modern Packaging with pyproject.toml
#
# ```toml
# [build-system]
# requires = ["setuptools>=61.0", "wheel"]
# build-backend = "setuptools.build_meta"
#
# [project]
# name = "genomeanalyzer"
# version = "1.0.0"
# description = "Fast genomic sequence analysis"
# readme = "README.md"
# authors = [
#     {name = "Sarah Chen", email = "sarah.chen@university.edu"}
# ]
# license = {text = "MIT"}
# classifiers = [
#     "Development Status :: 4 - Beta",
#     "Intended Audience :: Science/Research",
#     "License :: OSI Approved :: MIT License",
#     "Programming Language :: Python :: 3",
#     "Programming Language :: Python :: 3.8",
#     "Programming Language :: Python :: 3.9",
#     "Programming Language :: Python :: 3.10",
#     "Topic :: Scientific/Engineering :: Bio-Informatics",
# ]
# keywords = ["genomics", "bioinformatics", "sequence-analysis"]
# dependencies = [
#     "numpy>=1.20",
#     "scipy>=1.7",
# ]
# requires-python = ">=3.8"
#
# [project.optional-dependencies]
# dev = [
#     "pytest>=7.0",
#     "pytest-cov>=3.0",
#     "sphinx>=4.0",
# ]
#
# [project.urls]
# Homepage = "https://github.com/username/genomeanalyzer"
# Documentation = "https://genomeanalyzer.readthedocs.io"
# Repository = "https://github.com/username/genomeanalyzer"
# ```

# %% [markdown]
# ### Publishing to PyPI - Step by Step
#
# **1. Install build tools:**
# ```bash
# pip install build twine
# ```
#
# **2. Build your package:**
# ```bash
# python -m build
# ```
# This creates:
# - `dist/genomeanalyzer-1.0.0.tar.gz` (source distribution)
# - `dist/genomeanalyzer-1.0.0-py3-none-any.whl` (wheel)
#
# **3. Test on TestPyPI first** (test server):
# ```bash
# # Create account at test.pypi.org
# python -m twine upload --repository testpypi dist/*
#
# # Test installation
# pip install --index-url https://test.pypi.org/simple/ genomeanalyzer
# ```
#
# **4. Upload to real PyPI:**
# ```bash
# # Create account at pypi.org
# python -m twine upload dist/*
# ```
#
# **5. Now anyone can install:**
# ```bash
# pip install genomeanalyzer
# ```
#
# ### Best Practices for PyPI Packages
#
# - ✅ Use semantic versioning (1.2.3 = MAJOR.MINOR.PATCH)
# - ✅ Write a detailed README (it appears on PyPI page)
# - ✅ Include classifiers for discoverability
# - ✅ Pin dependencies conservatively (`>=1.0` not `==1.0.0`)
# - ✅ Test before uploading (use TestPyPI)
# - ✅ Tag releases in Git
# - ✅ Keep a CHANGELOG.md

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Publishing to PyPI makes your code accessible to the world—share your work!</p>
#     <ul>
#         <li><strong>Package your research tool:</strong> Take a useful script or module
#         from your work, create proper package structure with setup.py/pyproject.toml, and
#         publish to TestPyPI first—practice the full release workflow safely.</li>
#         <li><strong>Automate releases with CI:</strong> Set up GitHub Actions to
#         automatically build, test, and publish to PyPI when you create a new Git
#         tag—eliminate manual release steps and ensure consistency.</li>
#         <li><strong>Create a complete package:</strong> Build a small but complete package
#         with documentation, tests, examples, CLI entry points, and proper
#         versioning—experience what production-ready Python packages require.</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 9: Making Your Software Citable
#
# ### Why Software Needs DOIs
#
# **Problem**: GitHub repositories can disappear, URLs can change, citations break.
#
# **Solution**: Digital Object Identifiers (DOIs) - permanent, citable references.
#
# **Benefits:**
# - ✅ Permanent link that won't break
# - ✅ Proper academic citation
# - ✅ Track impact (who cited your software)
# - ✅ Required by some journals
# - ✅ Counts as research output
#
# ### Using Zenodo for DOIs
#
# **Zenodo** (https://zenodo.org) is a free repository for research outputs, including software.
# Integrated with GitHub for automatic archiving.
#
# **Setup steps:**
#
# **1. Connect GitHub to Zenodo:**
# - Log in to Zenodo with GitHub account
# - Go to https://zenodo.org/account/settings/github/
# - Enable your repository
#
# **2. Create a release on GitHub:**
# ```bash
# git tag -a v1.0.0 -m "First release"
# git push origin v1.0.0
# ```
#
# **3. Zenodo automatically:**
# - Archives the release
# - Generates a DOI
# - Creates a permanent snapshot
#
# **4. Get your DOI** (looks like: `10.5281/zenodo.1234567`)
#
# ### Adding Citation Information
#
# **1. Create CITATION.cff** (Citation File Format):
# ```yaml
# cff-version: 1.2.0
# message: "If you use this software, please cite it as below."
# authors:
#   - family-names: Chen
#     given-names: Sarah
#     orcid: https://orcid.org/0000-0001-2345-6789
# title: "GenomeAnalyzer: Fast Genomic Sequence Analysis"
# version: 1.0.0
# doi: 10.5281/zenodo.1234567
# date-released: 2024-02-10
# url: "https://github.com/username/genomeanalyzer"
# license: MIT
# ```
#
# **2. Add to README:**
# ```markdown
# ## Citation
#
# If you use GenomeAnalyzer in your research, please cite:
#
# Chen, S. (2024). GenomeAnalyzer: Fast Genomic Sequence Analysis (Version 1.0.0)
# [Computer software]. https://doi.org/10.5281/zenodo.1234567
#
# BibTeX:
#
# ```bibtex
# @software{chen2024genome,
#   author = {Chen, Sarah},
#   title = {GenomeAnalyzer: Fast Genomic Sequence Analysis},
#   year = {2024},
#   version = {1.0.0},
#   doi = {10.5281/zenodo.1234567},
#   url = {https://github.com/username/genomeanalyzer}
# }
# ```
# ```
#
# ### Journal of Open Source Software (JOSS)
#
# **JOSS** (https://joss.theoj.org) publishes short papers about research software.
#
# **Benefits:**
# - Academic publication for your software
# - Peer review of code and documentation
# - Citable journal article
# - Increases visibility
# - Free and open access
#
# **Requirements:**
# - Open source license
# - README with installation/usage
# - Tests and continuous integration
# - Documentation
# - Contribution guidelines
# - Clear research application
#
# **Submission:**
# - Write a 1-2 page paper describing the software
# - Reviewers check functionality and documentation
# - Fast review process (weeks, not months)
# - Published with DOI

# %% [markdown]
# ## Part 10: Documentation Tools for Other Languages
#
# Documentation is important regardless of your programming language. Each language has
# its own tools and conventions, but the principles remain the same.
#
# ### C/C++
#
# **Documentation Generator:**
# - **Doxygen** - Most popular, extracts comments from code
#   - Website: https://www.doxygen.nl/
#   - Supports JavaDoc-style comments (`/** */`)
#   - Generates HTML, LaTeX, man pages
#   - Example:
#     ```c++
#     /**
#      * @brief Converts Celsius to Fahrenheit
#      * @param celsius Temperature in Celsius
#      * @return Temperature in Fahrenheit
#      */
#     double celsius_to_fahrenheit(double celsius);
#     ```
#
# **Alternative: Sphinx with Breathe** - Use Sphinx for C++ via Breathe extension
#
# **Hosting:** Read the Docs supports C++ via Doxygen
#
# ### Java
#
# **Documentation Generator:**
# - **Javadoc** - Built into Java, standard tool
#   - Included with JDK
#   - Uses `/** */` comments
#   - Generates HTML documentation
#   - Example:
#     ```java
#     /**
#      * Converts temperature from Celsius to Fahrenheit.
#      *
#      * @param celsius temperature in degrees Celsius
#      * @return temperature in degrees Fahrenheit
#      * @throws IllegalArgumentException if celsius below absolute zero
#      */
#     public static double celsiusToFahrenheit(double celsius) {
#         if (celsius < -273.15) {
#             throw new IllegalArgumentException("Below absolute zero");
#         }
#         return celsius * 9.0 / 5.0 + 32.0;
#     }
#     ```
#
# **Build:** `javadoc -d docs src/*.java`
#
# ### R
#
# **Documentation Generator:**
# - **roxygen2** - Standard for R packages
#   - Installed via CRAN: `install.packages("roxygen2")`
#   - Uses `#'` special comments
#   - Generates `.Rd` files automatically
#   - Example:
#     ```r
#     #' Convert Celsius to Fahrenheit
#     #'
#     #' @param celsius Numeric vector of temperatures in Celsius
#     #' @return Numeric vector of temperatures in Fahrenheit
#     #' @examples
#     #' celsius_to_fahrenheit(0)
#     #' celsius_to_fahrenheit(c(0, 100, -40))
#     #' @export
#     celsius_to_fahrenheit <- function(celsius) {
#       fahrenheit <- celsius * 9/5 + 32
#       return(fahrenheit)
#     }
#     ```
#
# **Package Documentation:**
# - **pkgdown** - Creates beautiful websites from R package documentation
#   - Website: https://pkgdown.r-lib.org/
#   - Reads roxygen2 documentation
#   - Generates polished website
#   - Hosts on GitHub Pages
#
# **Build:** In RStudio: `devtools::document()` or `pkgdown::build_site()`
#
# ### Julia
#
# **Documentation Generator:**
# - **Documenter.jl** - Official Julia documentation tool
#   - Install: `] add Documenter`
#   - Markdown-based docstrings
#   - Integrated with Julia's help system
#   - Example:
#     ```julia
#     """
#         celsius_to_fahrenheit(celsius)
#
#     Convert temperature from Celsius to Fahrenheit.
#
#     # Arguments
#     - `celsius::Real`: Temperature in degrees Celsius
#
#     # Returns
#     - Temperature in degrees Fahrenheit
#
#     # Examples
#     ```jldoctest
#     julia> celsius_to_fahrenheit(0)
#     32.0
#
#     julia> celsius_to_fahrenheit(100)
#     212.0
#     ```
#     """
#     function celsius_to_fahrenheit(celsius::Real)
#         return celsius * 9/5 + 32
#     end
#     ```
#
# **Hosting:** Documentation deployed to GitHub Pages automatically
#
# ### MATLAB
#
# **Documentation:**
# - **Built-in help** - Use `help function_name`
#   - First comment block becomes help text
#   - Example:
#     ```matlab
#     function fahrenheit = celsius_to_fahrenheit(celsius)
#     % CELSIUS_TO_FAHRENHEIT Convert Celsius to Fahrenheit
#     %
#     %   fahrenheit = CELSIUS_TO_FAHRENHEIT(celsius) converts temperature
#     %   from degrees Celsius to degrees Fahrenheit.
#     %
#     %   Inputs:
#     %       celsius - Temperature in degrees Celsius (numeric)
#     %
#     %   Outputs:
#     %       fahrenheit - Temperature in degrees Fahrenheit (numeric)
#     %
#     %   Example:
#     %       >> celsius_to_fahrenheit(0)
#     %       ans = 32
#     %
#     %   See also FAHRENHEIT_TO_CELSIUS
#
#     fahrenheit = celsius * 9/5 + 32;
#     end
#     ```
#
# **Publishing:**
# - MATLAB File Exchange for sharing code
# - Generate reports with MATLAB Publisher
#
# ### Fortran
#
# **Documentation Generator:**
# - **FORD** (FORtran Documenter) - Modern documentation tool
#   - Website: https://github.com/Fortran-FOSS-Programmers/ford
#   - Install: `pip install ford`
#   - Markdown-based documentation
#   - Example:
#     ```fortran
#     !> Convert temperature from Celsius to Fahrenheit
#     !!
#     !! Converts a temperature value from degrees Celsius
#     !! to degrees Fahrenheit.
#     !!
#     !! @param[in] celsius Temperature in Celsius
#     !! @return Temperature in Fahrenheit
#     function celsius_to_fahrenheit(celsius) result(fahrenheit)
#         real, intent(in) :: celsius
#         real :: fahrenheit
#
#         fahrenheit = celsius * 9.0 / 5.0 + 32.0
#     end function celsius_to_fahrenheit
#     ```
#
# **Alternative: Doxygen** also supports Fortran
#
# ### Rust
#
# **Documentation Generator:**
# - **rustdoc** - Built into Rust, official tool
#   - Integrated with cargo: `cargo doc`
#   - Markdown docstrings with `///`
#   - Automatic linking and examples
#   - Example:
#     ```rust
#     /// Converts temperature from Celsius to Fahrenheit.
#     ///
#     /// # Arguments
#     ///
#     /// * `celsius` - Temperature in degrees Celsius
#     ///
#     /// # Returns
#     ///
#     /// Temperature in degrees Fahrenheit
#     ///
#     /// # Examples
#     ///
#     /// ```
#     /// let fahrenheit = celsius_to_fahrenheit(0.0);
#     /// assert_eq!(fahrenheit, 32.0);
#     /// ```
#     pub fn celsius_to_fahrenheit(celsius: f64) -> f64 {
#         celsius * 9.0 / 5.0 + 32.0
#     }
#     ```
#
# **Hosting:** docs.rs automatically builds and hosts documentation for crates.io packages
#
# ### JavaScript/TypeScript
#
# **Documentation Generators:**
# - **JSDoc** - Standard for JavaScript
#   - Install: `npm install -g jsdoc`
#   - Uses `/** */` comments
#   - Example:
#     ```javascript
#     /**
#      * Convert Celsius to Fahrenheit
#      * @param {number} celsius - Temperature in Celsius
#      * @returns {number} Temperature in Fahrenheit
#      * @example
#      * celsiusToFahrenheit(0)
#      * // returns 32
#      */
#     function celsiusToFahrenheit(celsius) {
#       return celsius * 9 / 5 + 32;
#     }
#     ```
#
# - **TypeDoc** - For TypeScript
#   - Install: `npm install --save-dev typedoc`
#   - Uses TypeScript types
#   - Generates from type annotations
#
# - **Documentation.js** - Modern alternative
#
# **Publishing:** GitHub Pages, Vercel, Netlify
#
# ### Go
#
# **Documentation:**
# - **godoc** - Built-in documentation tool
#   - Comments before declarations become docs
#   - Served at pkg.go.dev automatically for public packages
#   - Example:
#     ```go
#     // CelsiusToFahrenheit converts temperature from Celsius to Fahrenheit.
#     //
#     // It takes a temperature in degrees Celsius and returns the equivalent
#     // temperature in degrees Fahrenheit.
#     //
#     // Example:
#     //     f := CelsiusToFahrenheit(0)
#     //     // f == 32
#     func CelsiusToFahrenheit(celsius float64) float64 {
#         return celsius*9/5 + 32
#     }
#     ```
#
# **Hosting:** pkg.go.dev automatically generates documentation for all Go packages
#
# ### Common Patterns Across Languages
#
# Despite different tools, documentation best practices are universal:
#
# **1. Write documentation in code** - Keep it close to what it documents
#
# **2. Use standard formats** - Each language has conventions; follow them
#
# **3. Include examples** - Show how to actually use the code
#
# **4. Generate automatically** - Use tools, don't write HTML manually
#
# **5. Host publicly** - Make documentation discoverable
#
# **6. Version your docs** - Match documentation to code versions
#
# **7. Test examples** - Ensure code examples actually work
#
# **The language changes, but good documentation principles remain constant!**

# %% [markdown]
# ## Summary
#
# ### Key Takeaways
#
# **Documentation transforms research software from "works for me" to "works for science"**
#
# **Essential documentation components:**
# 1. **README** - First impression; installation and quick start
# 2. **Docstrings** - Embedded documentation in code
# 3. **API docs** - Generated reference material (Sphinx)
# 4. **Examples** - Working code that demonstrates usage
# 5. **License** - Legal permission to use (choose one!)
# 6. **Citation** - How to cite your work (DOI via Zenodo)
#
# **The Documentation Workflow:**
# - Write good docstrings while coding
# - Create comprehensive README
# - Choose appropriate license (MIT recommended)
# - Generate API docs with Sphinx
# - Host on Read the Docs
# - Publish to PyPI for easy installation
# - Archive on Zenodo for DOI/citation
# - Consider JOSS for academic publication
#
# **Impact of good documentation:**
# - **More citations** - People can use and cite your work
# - **More collaborators** - Others can contribute
# - **More impact** - Your research reaches further
# - **Career benefits** - Shows professionalism
# - **Better science** - Reproducible and verifiable
#
# ### Documentation Checklist for Research Software
#
# Before releasing research software, ensure you have:
#
# - [ ] README with clear installation instructions
# - [ ] NumPy-style docstrings for all public functions
# - [ ] Working examples in documentation
# - [ ] LICENSE file (MIT recommended)
# - [ ] Citation information (CITATION.cff)
# - [ ] Sphinx documentation (optional but recommended)
# - [ ] Package on PyPI (for Python)
# - [ ] DOI from Zenodo
# - [ ] Tests and CI badges
# - [ ] Contributing guidelines (if accepting contributions)
#
# ### What We Learned
#
# - Why documentation is essential for research impact
# - How to write effective README files
# - NumPy-style docstrings with complete examples
# - Generating beautiful docs with Sphinx
# - Choosing software licenses (choosealicense.com)
# - Publishing packages to PyPI
# - Making software citable with Zenodo DOIs
# - Documentation tools for other languages
#
# ### Remember Dr. Chen's Story
#
# One week of documentation effort transformed:
# - 3 citations → 47 citations
# - 0 users → researchers worldwide
# - Hidden code → published, citable software
# - Limited impact → field-changing contribution
#
# **Good documentation amplifies your research impact!**

# %% [markdown]
# ### What's Next?
#
# In **Lecture 9**, we'll explore containerization and reproducibility. You'll learn:
# - Understanding the limitations of virtual environments for reproducibility
# - What containers are and how they differ from virtual machines
# - Writing Dockerfiles to containerize research software
# - Using Docker, Podman, and Apptainer for reproducible environments
# - Choosing the right containerization tool for your use case
#
# Documentation is the first step toward making your research reproducible. Containers take
# it further by capturing the entire computational environment, ensuring your documented
# software runs identically anywhere.
#
# **Ready to continue? Move on to Lecture 9: Containerization and Reproducibility!**

# %% [markdown]
# ## Acknowledgements and References
#
# This lecture draws on best practices from the research software engineering community
# and official documentation from various tools and platforms.
#
# ### Primary Sources
#
# - **Research Software Engineering with Python** by The Alan Turing Institute
#   <https://alan-turing-institute.github.io/rse-course/html/>
#   Documentation practices, packaging workflows, and community standards.
#
# - **Research Software Engineering with Python** by Damien Irving, Kate Hertweck,
#   Luke Johnston, Joel Ostblom, Charlotte Wickham, and Greg Wilson (2022)
#   <https://third-bit.com/py-rse/>
#   Chapters on "Publishing" and "Packaging" provided foundational concepts for
#   making research software reusable.
#
# - **Write the Docs**
#   <https://www.writethedocs.org/>
#   Community resources on technical writing, documentation best practices, and
#   documentation-driven development. The "Beginner's Guide to Docs" and style
#   guides informed our approach to research software documentation.
#
# ### Documentation Tools
#
# - **Sphinx Documentation Generator**
#   <https://www.sphinx-doc.org/>
#   Official documentation for Python's standard documentation tool.
#
# - **NumPy Documentation Guide**
#   <https://numpydoc.readthedocs.io/>
#   Standard for NumPy-style docstrings used throughout scientific Python.
#
# - **Read the Docs**
#   <https://docs.readthedocs.io/>
#   Documentation hosting platform widely used in research software.
#
# ### Packaging and Publishing
#
# - **Python Packaging User Guide**
#   <https://packaging.python.org/>
#   Official guide for packaging and distributing Python projects.
#
# - **PyPI - Python Package Index**
#   <https://pypi.org/>
#   Official repository for Python packages.
#
# - **Zenodo**
#   <https://zenodo.org/>
#   Research data repository integrated with GitHub for software archiving.
#
# - **Journal of Open Source Software (JOSS)**
#   <https://joss.theoj.org/>
#   Peer-reviewed journal for research software papers.
#
# ### Licensing Resources
#
# - **Choose a License**
#   <https://choosealicense.com/>
#   GitHub's guide to selecting appropriate open source licenses.
#
# - **Open Source Initiative (OSI)**
#   <https://opensource.org/>
#   Definitive resource on open source licenses.
#
# - **TL;DR Legal**
#   <https://www.tldrlegal.com/>
#   Plain-English summaries of software licenses.
#
# ### Citation and Metadata
#
# - **Citation File Format (CFF)**
#   <https://citation-file-format.github.io/>
#   Standard format for software citation metadata.
#
# - **Software Heritage**
#   <https://www.softwareheritage.org/>
#   Universal archive of software source code.
#
# ### Community Standards
#
# - **The Turing Way**
#   <https://the-turing-way.netlify.app/>
#   Handbook on reproducible research, including software documentation.
#
# - **FORCE11 Software Citation Principles**
#   <https://doi.org/10.7717/peerj-cs.86>
#   Smith AM, Katz DS, Niemeyer KE, FORCE11 Software Citation Working Group (2016).
#   "Software citation principles." PeerJ Computer Science 2:e86.
#
# ### Language-Specific Documentation Tools
#
# References for documentation tools mentioned in the "Other Languages" section:
#
# - **Doxygen** (C/C++): <https://www.doxygen.nl/>
# - **Javadoc** (Java): <https://docs.oracle.com/javase/8/docs/technotes/tools/windows/javadoc.html>
# - **roxygen2** (R): <https://roxygen2.r-lib.org/>
# - **pkgdown** (R): <https://pkgdown.r-lib.org/>
# - **Documenter.jl** (Julia): <https://documenter.juliadocs.org/>
# - **FORD** (Fortran): <https://github.com/Fortran-FOSS-Programmers/ford>
# - **rustdoc** (Rust): <https://doc.rust-lang.org/rustdoc/>
# - **JSDoc** (JavaScript): <https://jsdoc.app/>
# - **TypeDoc** (TypeScript): <https://typedoc.org/>
# - **godoc** (Go): <https://pkg.go.dev/>
#
# ### Notes
#
# The example of "Dr. Sarah Chen" is a fictional composite character created for
# pedagogical purposes to illustrate the importance of documentation. The scenario
# is inspired by real patterns observed in research software development but does
# not represent any specific individual or project.
