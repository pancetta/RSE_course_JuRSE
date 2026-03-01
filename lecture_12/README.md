# Lecture 12: Scientific Workflows and Automation

## Overview
Scientific research often involves complex, multi-step data analysis pipelines: download data, preprocess it, run simulations, analyze results, generate figures, and compile reports. As projects grow, manually executing these steps becomes error-prone, time-consuming, and difficult to reproduce. This lecture introduces scientific workflow management systems that automate these pipelines, track dependencies between steps, and ensure reproducibility. We'll explore how workflow systems differ from simple shell scripts and Makefiles, when to use each tool, and demonstrate practical examples using both Make and modern workflow managers like Snakemake.

**Duration**: ~90 minutes

## Topics Covered
- Challenges of managing complex research pipelines
- When to use scripts, Make, or workflow management systems
- Fundamentals of dependency-based execution
- Writing basic Snakemake workflows for data analysis
- Understanding alternatives (Nextflow, CWL, Galaxy) and their use cases
- Applying workflow concepts across different programming languages
- Integrating workflows with version control and containerization

## Key Concepts
- **Workflow**: Automated sequence of steps with dependencies
- **Dependency-based execution**: Running only what needs updating
- **Make**: Build automation tool for file dependencies
- **Snakemake**: Python-based workflow management system
- **Targets and prerequisites**: What to build and what it depends on
- **Parallel execution**: Running independent steps simultaneously
- **Reproducibility**: Documenting exact steps for re-running analyses

## Prerequisites

Before starting this lecture, you should be familiar with:
- Basic shell commands and scripting
- Python programming and file I/O (covered in Lectures 2-4)
- Understanding of research data workflows
- Containerization concepts (covered in Lecture 9, helpful but not required)

This lecture builds on your programming skills and introduces workflow automation tools.

## Learning Objectives
- Understand the challenges of managing complex research pipelines
- Recognize when to use scripts, Make, or workflow management systems
- Learn the fundamentals of dependency-based execution
- Write basic Snakemake workflows for data analysis
- Understand alternatives (Nextflow, CWL, Galaxy) and their use cases
- Apply workflow concepts across different programming languages
- Integrate workflows with version control and containerization

## Files
- `lecture_12.py` - Main lecture content in Jupytext format

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
cd lecture_12
jupytext --to notebook lecture_12.py
jupyter notebook lecture_12.ipynb
```

Or from the main repository directory:
```bash
make convert
jupyter notebook
```

## The Pipeline Problem
The lecture opens with a researcher's struggles managing a weekly analysis pipeline, illustrating why automation tools are essential for reproducible research.

## Practical Examples
The lecture includes complete examples:
- Shell scripts and their limitations
- Makefiles for simple pipelines
- Snakemake workflows for complex analysis
- Comparison of workflow systems (Nextflow, CWL, Galaxy)
- Integration with containers and version control
