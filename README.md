# Research Software Engineering Lectures

[![CI - Lecture Scripts](https://github.com/pancetta/RSE_course_JuRSE/workflows/CI%20-%20Lecture%20Scripts/badge.svg)](https://github.com/pancetta/RSE_course_JuRSE/actions)

Welcome to the Research Software Engineering (RSE) lecture series! This repository contains materials for learning best practices in developing high-quality research software.

## Course Positioning

This course is:

- A semester-long introduction to Research Software Engineering (RSE)
- Targeted at late Bachelor / early Master STEM students
- Designed for students with scientific background but not necessarily prior software engineering training

The course uses Python as an example implementation language, but the principles generalize to other research computing environments.

## Learning Outcomes

After completing this course, students will be able to:

- Design reproducible research software workflows
- Use version control effectively in collaborative research
- Structure Python projects for maintainability
- Write automated tests for scientific code
- Set up continuous integration for research software
- Package and document research software professionally
- Containerize computational environments
- Critically evaluate AI-assisted coding tools in research contexts
- Understand sustainability and credit mechanisms in research software

## Course Philosophy

**This is not a classical Software Engineering course.**

The focus is not on large-scale system architecture or formal methods, but on pragmatic, reproducible, sustainable research software practices.

## Course Overview

This lecture series covers 14 lectures (~90 minutes each) on Research Software Engineering fundamentals:

- **Lecture 1**: Introduction to RSE, Shell Basics, and Git Fundamentals
- **Lecture 2**: Advanced Git, GitHub & GitLab Collaboration, and Python Basics
- **Lecture 3**: Python Fundamentals and Advanced Concepts
- **Lecture 4**: Python Project Structure and Scientific Libraries (NumPy, Matplotlib)
- **Lecture 5**: Testing Research Software
- **Lecture 6**: Automation and Continuous Integration
- **Lecture 7**: Debugging and Profiling Research Software
- **Lecture 8**: Documenting and Publishing Research Software
- **Lecture 9**: Containerization and Reproducibility
- **Lecture 10**: Collaboration and Code Review in Research Software
- **Lecture 11**: Working with Research Data - File Formats and Databases
- **Lecture 12**: Scientific Workflows and Automation
- **Lecture 13**: AI-Assisted Coding for Research Software
- **Lecture 14**: Course Summary and the RSE Community

**Integrated Topics:** Throughout the course, we cover software architecture and design principles including DRY, Single Responsibility, code smells, refactoring strategies, and architectural code review.

## Getting Started

### Quick Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pancetta/RSE_course_JuRSE.git
   cd RSE_course_JuRSE
   ```

2. **Install dependencies:**
   
   Install [micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html), then create the environment:
   
   ```bash
   make install
   micromamba activate rse_lecture
   ```

3. **View the lectures:**
   
   ```bash
   # Start the interactive website
   make serve-website
   ```
   
   Then open your browser to `http://localhost:8000`

### Working with Notebooks

Convert lecture files to Jupyter notebooks:
```bash
make convert
jupyter notebook
```

## Platform Support

- ✅ Linux (Ubuntu and other distributions)
- ✅ macOS 15 (Sequoia) and later
- ✅ Windows 10/11 (with Git Bash)

## Documentation

- **[Getting Started Guide](docs/QUICKSTART.md)** - Quick reference for common tasks
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the course
- **[Dependency Management](docs/DEPENDENCY_MANAGEMENT.md)** - How dependencies are managed
- **[Publishing Guide](docs/PUBLISHING.md)** - Citation and publishing information

## Citation

If you use this course material in your teaching or research, please cite it as:

```bibtex
@misc{speck2026rse,
  author       = {Speck, Robert},
  title        = {Research Software Engineering Lectures},
  year         = {2026},
  publisher    = {GitHub},
  url          = {https://github.com/pancetta/RSE_course_JuRSE},
  note         = {Version 1.0.0}
}
```

For a citable DOI, see our [Publishing Guide](docs/PUBLISHING.md).

## License

**Dual licensing for proper attribution:**

- **Educational content** (lectures, documentation): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) - Attribution required
- **Code examples**: MIT License

See [LICENSE](LICENSE) for complete details.

## Credits

This course draws on excellent resources from the Research Software Engineering community:

- [Research Software Engineering with Python](https://alan-turing-institute.github.io/rse-course/html/) by The Alan Turing Institute
- [Research Software Engineering with Python](https://third-bit.com/py-rse/) by Irving et al. (2022)
- Official documentation from Git, GitHub, GitLab, NumPy, Matplotlib, pytest, and Python

For complete bibliographic information, see [references.bib](references.bib).

## Contact

For questions or suggestions, please [open an issue](https://github.com/pancetta/RSE_course_JuRSE/issues) on GitHub.
