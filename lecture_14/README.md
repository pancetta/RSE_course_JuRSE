# Lecture 14: Course Summary and the RSE Community

## Overview
This final half-lecture wraps up our Research Software Engineering journey by reviewing what we've learned, exploring important topics we didn't cover, and connecting you with the broader RSE community. This session provides perspective on how the course content fits together and how you can continue growing as a research software engineer.

**Duration**: 45-60 minutes (half-lecture)

**Note**: This lecture will be augmented later with information about the course exam, further educational offers, and a Q&A session.

## Topics Covered
- Comprehensive review of Lectures 1-13
- How all course concepts fit together
- Advanced topics beyond this course
- The international RSE community
- German RSE community and local resources
- Continuing education opportunities
- Where to find ongoing support and resources

## Key Concepts
- **Course integration**: How version control, testing, CI/CD, and documentation work together
- **RSE community**: Society of Research Software Engineering and local chapters
- **Career paths**: Academic, industry, and hybrid RSE roles
- **Continuous learning**: Staying current with evolving best practices
- **Community support**: Conferences, working groups, and online resources

## Prerequisites

Before starting this lecture, you should have:
- Completed Lectures 1-13
- Hands-on experience with the RSE tools and practices covered
- Basic understanding of all major topics: version control, Python, testing, CI/CD, documentation, containers, collaboration, data management, workflows, and AI tools

This final lecture synthesizes everything you've learned into a cohesive whole.

## Learning Objectives
- Review and integrate knowledge from all 13 lectures
- Understand advanced topics beyond this course and how to learn them
- Connect with the international and German RSE communities
- Know where to find ongoing support and resources
- Feel confident continuing your RSE journey

## Files
- `lecture_14.py` - Main lecture content in Jupytext format

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
cd lecture_14
jupytext --to notebook lecture_14.py
jupyter notebook lecture_14.ipynb
```

Or from the main repository directory:
```bash
make convert
jupyter notebook
```

## Course Synthesis
This lecture provides a comprehensive review of:
- Foundational tools (Lectures 1-2): Shell, Git, Python basics
- Python programming (Lectures 3-4): Language features and project structure
- Code quality (Lectures 5-7): Testing, CI/CD, debugging
- Professional practices (Lectures 8-10): Documentation, containers, collaboration
- Advanced topics (Lectures 11-13): Data management, workflows, AI tools

## Beyond This Course
Topics not covered in depth that you may want to explore:
- Advanced performance optimization and parallel computing
- Machine learning infrastructure and MLOps
- Specific domain tools (bioinformatics, climate modeling, etc.)
- Grant writing and project management for RSE

## Community Resources
- Society of Research Software Engineering (https://society-rse.org/)
- de-RSE (German chapter): https://de-rse.org/
- International RSE conferences
- Local RSE groups and meetups
