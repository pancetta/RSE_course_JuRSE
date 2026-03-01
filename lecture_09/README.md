# Lecture 9: Containerization and Reproducibility

This lecture covers containerization technologies (Docker, Podman, Apptainer) for achieving true reproducibility in research software.

## Topics Covered

- Limitations of virtual environments
- Container fundamentals
- Docker for research software
- Podman (rootless alternative)
- Apptainer/Singularity (HPC-focused)
- Cross-language containerization
- Best practices

## Practical Example

The `container-demo/` subdirectory contains a working example that demonstrates:
- Building a Docker container following best practices
- Running containerized analysis
- Integration with CI/CD (automatically tested in GitHub Actions)

See `container-demo/README.md` for instructions on building and running the example.

## Installation

This lecture uses only base dependencies. No additional packages required.

```bash
make install
micromamba activate rse_lecture
```

## Converting to Notebook

```bash
python scripts/convert_to_notebooks.py
jupyter notebook lecture_09/lecture_09.ipynb
```
