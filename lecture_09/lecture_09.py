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
# # Lecture 9: Containerization and Reproducibility
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
#     <img src="lecture_09_qr_code.png" alt="This Lecture QR Code" width="150"/>
#     <p><strong>This Lecture</strong></p>
#   </div>
# </div>
#
# ## Overview
# This lecture explores how containers enable truly reproducible research by packaging
# not just your code and Python dependencies, but the entire computational environment.
# We'll examine why traditional dependency management (conda, venv) sometimes falls short,
# and how containerization tools like Docker, Podman, and Apptainer solve these challenges.
# You'll learn practical strategies for containerizing research software and understand
# when each tool is most appropriate for your needs.
#
# **Duration**: ~90 minutes
#
# ## Prerequisites
#
# Before starting this lecture, you should be familiar with:
# - Python virtual environments and dependency management (covered in Lecture 4)
# - Running Python scripts and installing packages
# - Basic command-line usage
# - Git basics for version control
#
# This lecture introduces containerization as the next step beyond virtual environments for reproducibility.
#
# ## Learning Objectives
# - Understand the limitations of virtual environments for reproducibility
# - Learn what containers are and how they differ from virtual machines
# - Write Dockerfiles to containerize research software
# - Use Docker to build and run reproducible environments
# - Understand alternatives: Podman (rootless) and Apptainer (HPC-focused)
# - Apply containerization to non-Python research software
# - Choose the right containerization tool for your use case

# %% [markdown]
# ## Part 1: The Reproducibility Crisis - When Virtual Environments Aren't Enough
#
# ### A Familiar Story
#
# Dr. Maria Rodriguez published a groundbreaking computational biology paper analyzing
# protein folding patterns. Her GitHub repository included:
# - Well-documented Python code
# - A `requirements.txt` with pinned versions
# - Clear installation instructions
# - Comprehensive tests (from Lecture 5!)
# - CI/CD pipeline (from Lecture 6!)
#
# Three months later, a colleague at another institution tried to reproduce her results.
#
# **On Maria's computer (Ubuntu 22.04):**
# ```bash
# conda create -n protein python=3.10
# conda activate protein
# pip install -r requirements.txt
# python analyze_proteins.py
# # ✅ Works perfectly! Results match the paper.
# ```
#
# **On colleague's computer (macOS 14):**
# ```bash
# conda create -n protein python=3.10
# conda activate protein
# pip install -r requirements.txt
# python analyze_proteins.py
# # ❌ Error: "ImportError: cannot import name 'compute_energies'"
# ```
#
# ### What Went Wrong?
#
# The Python packages installed fine, but Maria's code relied on:
# - **System libraries**: `libgsl` (GNU Scientific Library) version 2.7
# - **Compiled extensions**: NumPy built against specific BLAS libraries
# - **OS-specific tools**: `ffmpeg` for video generation
#
# Even though `requirements.txt` specified exact Python package versions, it couldn't
# capture:
# - System-level dependencies
# - Compiler versions used to build packages
# - Underlying C/C++ libraries
# - OS-specific configurations
#
# ### The Conda/Venv Limitation
#
# Virtual environments (`venv`, `conda`) are excellent for managing **Python** dependencies,
# but they have inherent limitations:
#
# **What they DO provide:**
# - Isolated Python environments
# - Reproducible Python package versions
# - Cross-platform package management (conda does better here)
#
# **What they DON'T provide:**
# - System library versions (except conda, partially)
# - Operating system consistency
# - Non-Python tools and dependencies
# - Binary compatibility guarantees
# - Complete filesystem isolation
#
# ### Real-World Reproducibility Challenges
#
# **Challenge 1: System Dependencies**
# ```python
# # This code works if you have the right system libraries
# import cv2  # Needs libopencv-dev, but which version?
# import gdal # Needs GDAL libraries, but system-installed
# ```
#
# **Challenge 2: Different OS Behaviors**
# ```python
# # File paths work differently
# data_path = "C:\\Users\\maria\\data"  # Windows
# data_path = "/home/maria/data"        # Linux
# data_path = "/Users/maria/data"       # macOS
# ```
#
# **Challenge 3: Hardware Differences**
# ```python
# # CPU architectures affect compiled code
# # Intel x86_64 vs ARM (Apple M1/M2) vs AMD64
# ```
#
# ### The Solution: Containers
#
# Containers package **everything** your code needs to run:
# - The operating system (lightweight Linux)
# - System libraries (specific versions)
# - Python/R/Julia and packages
# - Your code and data
# - Configuration files
#
# **Result**: If it works in the container on your machine, it works in the
# container on any machine (Linux, macOS, Windows, HPC cluster, cloud).

# %% [markdown]
# ## Part 2: Understanding Containers
#
# ### Containers vs. Virtual Machines
#
# **Virtual Machines (VMs):**
# - Full OS virtualization
# - Each VM runs complete OS kernel
# - Heavy (GBs per VM)
# - Slower startup (minutes)
# - Strong isolation
#
# **Containers:**
# - Process-level isolation
# - Share host OS kernel
# - Lightweight (MBs per container)
# - Fast startup (seconds)
# - Good isolation
#
# <img src="figures/vm_vs_container_architecture.svg" alt="Side-by-side architecture: VMs stack a full guest OS under every app on a hypervisor, while containers share one host kernel through a container runtime with no guest OS layer" width="760"/>
#
# *The height difference is the point: a VM needs a full guest OS under every app, while
# containers share one host kernel through the runtime layer. That missing layer is where
# the weight (and startup time) goes.*
#
# ### Key Container Concepts
#
# **1. Container Image**
# - Read-only template with your application and dependencies
# - Built from a Dockerfile (recipe)
# - Can be shared via registries (Docker Hub, GitHub Container Registry)
# - Layered filesystem (efficient storage and transfer)
#
# **2. Container**
# - Running instance of an image
# - Isolated filesystem, network, processes
# - Can be started, stopped, deleted
# - Ephemeral by default (changes lost when deleted)
#
# **3. Registry**
# - Storage and distribution system for images
# - Docker Hub: public registry
# - GitHub Container Registry (ghcr.io)
# - Institutional registries
#
# ### Why Containers for Research?
#
# **Reproducibility:**
# - Exact environment can be recreated years later
# - Works on any platform (laptop, HPC, cloud)
# - Eliminates "works on my machine" problems
#
# **Portability:**
# - Run the same container on different systems
# - Easy deployment to cloud platforms
# - Share complete environment with collaborators
#
# **Isolation:**
# - No conflicts with system packages
# - Test different versions without breaking your system
# - Safe experimentation
#
# **Documentation:**
# - Dockerfile serves as executable documentation
# - Shows exactly how environment is built
# - More reliable than written instructions

# %% [markdown]
# ## Part 3: Docker - The Industry Standard
#
# ### Docker Basics
#
# Docker is the most widely-used containerization platform. While it requires
# administrative privileges and runs a daemon, it has excellent documentation,
# broad ecosystem support, and is well-integrated with most platforms.

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Ready to get hands-on with containers? Here are some ways to deepen your understanding:</p>
#     <ul>
#         <li><strong>Write your first Dockerfile</strong>: Take one of your existing
#         Python scripts and create a Dockerfile for it. Start simple - just Python,
#         dependencies, and the script.</li>
#         <li><strong>Test on a colleague's machine</strong>: Build your container and
#         share the image. Does it run identically on their system? Experience the "it
#         works everywhere" moment!</li>
#         <li><strong>Compare installation methods</strong>: Time how long it takes to set up your project manually vs. using a
#         container. Which is more reliable?</li>
#     </ul>
# </div>

# %% [markdown]
# ### Writing a Dockerfile
#
# A Dockerfile is a text file with instructions to build a container image.
# Let's create one for a typical Python research project.
#
# **Basic Dockerfile for Python Research:**
#
# ```dockerfile
# # Start from official Python image
# FROM python:3.10-slim
#
# # Set metadata (good practice!)
# LABEL maintainer="maria.rodriguez@university.edu"
# LABEL description="Protein folding analysis tool"
# LABEL version="1.0"
#
# # Set working directory
# WORKDIR /app
#
# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     libgsl-dev \
#     ffmpeg \
#     && rm -rf /var/lib/apt/lists/*
#
# # Copy requirements first (better caching)
# COPY requirements.txt .
#
# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt
#
# # Copy application code
# COPY . .
#
# # Default command
# CMD ["python", "analyze_proteins.py"]
# ```
#
# ### Understanding Dockerfile Instructions
#
# **FROM**: Base image to start from
# - `python:3.10-slim`: Official Python image (Debian-based, minimal)
# - `continuumio/miniconda3`: If you prefer conda
# - `ubuntu:22.04`: Start from Ubuntu
#
# **RUN**: Execute commands during build
# - Install packages: `apt-get install`, `pip install`, `conda install`
# - Set up environment
# - Each RUN creates a new layer
#
# **COPY**: Copy files from host to container
# - `COPY requirements.txt .`: Copy one file
# - `COPY . .`: Copy entire directory
#
# **WORKDIR**: Set working directory (like `cd`)
#
# **CMD**: Default command when container starts
# - Can be overridden at runtime
#
# **ENV**: Set environment variables
# ```dockerfile
# ENV PYTHONUNBUFFERED=1
# ENV DATA_PATH=/data
# ```
#
# ### Layer Caching and Best Practices
#
# Docker builds images in layers. Each instruction creates a layer.
# Layers are cached and reused if nothing changed.
#
# **Bad practice** (slow rebuilds):
# ```dockerfile
# COPY . .                           # Copy everything first
# RUN pip install -r requirements.txt  # Reinstalls if ANY file changes
# ```
#
# **Good practice** (fast rebuilds):
# ```dockerfile
# COPY requirements.txt .            # Copy requirements first
# RUN pip install -r requirements.txt  # Only rebuilds if requirements change
# COPY . .                           # Then copy code
# ```

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Want to master container debugging? Try these exploration activities:</p>
#     <ul>
#         <li><strong>Inspect layer sizes</strong>: Use <code>docker history
#         &lt;image&gt;</code> to see how much each instruction adds to your image. What
#         surprised you?</li>
#         <li><strong>Debug a failing build</strong>: Intentionally break your Dockerfile
#         (wrong package name, missing file). Practice using <code>docker run -it &lt;image&gt;
#         /bin/bash</code> to investigate.</li>
#         <li><strong>Experiment with layer caching</strong>: Make small changes to your
#         Dockerfile and rebuild. Which layers are cached? Which rebuild? Understanding this
#         saves hours of build time!</li>
#     </ul>
# </div>

# %% [markdown]
# ### Building and Running Containers
#
# **Build an image:**
# ```bash
# # Basic build
# docker build -t protein-analysis .
#
# # Build with specific Dockerfile
# docker build -f Dockerfile.research -t protein-analysis:v1.0 .
#
# # See build progress
# docker build --progress=plain -t protein-analysis .
# ```
#
# **Run a container:**
# ```bash
# # Run interactively
# docker run -it protein-analysis /bin/bash
#
# # Run with volume mount (access host files)
# docker run -v /path/to/data:/data protein-analysis
#
# # Run with current directory mounted
# docker run -v $(pwd):/app protein-analysis
#
# # Run with environment variables
# docker run -e DATA_PATH=/data -e N_CORES=4 protein-analysis
# ```
#
# **Manage containers and images:**
# ```bash
# # List running containers
# docker ps
#
# # List all containers (including stopped)
# docker ps -a
#
# # List images
# docker images
#
# # Remove container
# docker rm container_id
#
# # Remove image
# docker rmi image_name
#
# # Clean up unused images/containers
# docker system prune
# ```

# %% [markdown]
# ## Part 4: A Realistic Research Example
#
# Let's containerize a complete research project that analyzes climate data.
#
# ### Project Structure
# ```
# climate-analysis/
# ├── Dockerfile
# ├── requirements.txt
# ├── environment.yml          # Alternative: conda environment
# ├── analyze_climate.py
# ├── process_data.py
# ├── tests/
# │   └── test_analysis.py
# └── README.md
# ```
#
# ### Step 1: Create Dockerfile
#
# ```dockerfile
# # Dockerfile for climate data analysis
# FROM python:3.10-slim
#
# # Metadata
# LABEL maintainer="researcher@university.edu"
# LABEL description="Climate data analysis pipeline"
# LABEL org.opencontainers.image.source="https://github.com/user/climate-analysis"
#
# # Install system dependencies needed by scientific packages
# RUN apt-get update && apt-get install -y \
#     gcc \
#     g++ \
#     gfortran \
#     libhdf5-dev \
#     libnetcdf-dev \
#     libproj-dev \
#     && rm -rf /var/lib/apt/lists/*
#
# # Create non-root user (security best practice)
# RUN useradd -m -s /bin/bash researcher
# WORKDIR /home/researcher/app
#
# # Install Python dependencies as root
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
#
# # Copy application
# COPY --chown=researcher:researcher . .
#
# # Switch to non-root user
# USER researcher
#
# # Run tests on build (fail fast if tests fail)
# RUN python -m pytest tests/
#
# # Default: start interactive Python
# CMD ["python"]
# ```
#
# ### Step 2: Create requirements.txt
# ```txt
# numpy==1.24.3
# pandas==2.0.2
# xarray==2023.5.0
# netCDF4==1.6.4
# matplotlib==3.7.1
# scipy==1.10.1
# pytest==7.3.1
# ```
#
# ### Step 3: Build and Test
# ```bash
# # Build the image
# docker build -t climate-analysis:latest .
#
# # Run analysis with mounted data
# docker run -v ./data:/home/researcher/app/data \
#            -v ./results:/home/researcher/app/results \
#            climate-analysis:latest \
#            python analyze_climate.py --input data/climate.nc --output results/
#
# # Interactive session for exploration
# docker run -it -v ./data:/home/researcher/app/data \
#            climate-analysis:latest /bin/bash
# ```
#
# ### Step 4: Share via Registry
# ```bash
# # Tag for GitHub Container Registry
# docker tag climate-analysis:latest ghcr.io/username/climate-analysis:v1.0
#
# # Login to registry
# echo $GITHUB_TOKEN | docker login ghcr.io -u username --password-stdin
#
# # Push image
# docker push ghcr.io/username/climate-analysis:v1.0
# ```
#
# ### Step 5: Document Usage
# Add to README.md:
# ```markdown
# ## Running with Docker
#
# ### Quick Start
# ```bash
# docker pull ghcr.io/username/climate-analysis:v1.0
# docker run -v ./data:/home/researcher/app/data \
#            ghcr.io/username/climate-analysis:v1.0 \
#            python analyze_climate.py
# ```
#
# ### For Development
# ```bash
# docker run -it -v $(pwd):/home/researcher/app \
#            ghcr.io/username/climate-analysis:v1.0 /bin/bash
# ```
# ```
#
# ### Why This Works
#
# **For the original researcher:**
# - Documents the complete environment
# - Ensures analysis runs consistently
# - Easy to share with collaborators
#
# **For other researchers:**
# - No installation headaches
# - Guaranteed to work as intended
# - Can build on the work immediately
#
# **For journals and reviewers:**
# - Can verify results exactly
# - Meets reproducibility requirements
# - Published container provides long-term record

# %% [markdown]
# ## Part 5: Podman - The Daemonless Alternative
#
# ### What is Podman?
#
# Podman is a Docker alternative that is:
# - **Daemonless**: No background service required
# - **Rootless**: Runs without administrator privileges
# - **Compatible**: Uses same command syntax as Docker
# - **Secure**: Better default security posture
#
# ### Why Podman?
#
# **Docker's daemon architecture:**
# - Runs `dockerd` as root
# - Security concern: root daemon = large attack surface
# - Can be inconvenient: requires administrator setup
#
# **Podman's approach:**
# - No daemon; each command runs directly
# - Rootless containers (more secure)
# - Fork-exec model (traditional Unix)
#
# ### Key Differences from Docker
#
# **1. No Daemon**
# ```bash
# # Docker requires daemon
# sudo systemctl start docker  # Not needed with Podman
#
# # Podman commands run directly
# podman run hello-world       # Just works
# ```
#
# **2. Rootless by Default**
# ```bash
# # Docker typically needs root
# sudo docker run ...
#
# # Podman runs as regular user
# podman run ...               # No sudo needed
# ```
#
# **3. Command Compatibility**
# ```bash
# # Almost identical syntax
# docker build -t myimage .
# podman build -t myimage .
#
# docker run -it myimage
# podman run -it myimage
#
# # Can even alias
# alias docker=podman
# ```
#
# ### When to Use Podman
#
# **Choose Podman if:**
# - You don't have root access (shared systems)
# - Security is paramount (rootless containers)
# - You want simpler architecture (no daemon)
# - Your IT policy restricts Docker
#
# **Choose Docker if:**
# - You need Docker Desktop features (GUI)
# - You're using Docker Compose heavily
# - Your tools require Docker specifically
# - You need maximum ecosystem compatibility
#
# ### Podman Example
# ```bash
# # Same Dockerfile works!
# podman build -t climate-analysis .
#
# # Run rootless container
# podman run -v ./data:/data climate-analysis
#
# # Save/load images (no registry needed)
# podman save -o climate-analysis.tar climate-analysis
# podman load -i climate-analysis.tar
#
# # Generate Kubernetes YAML
# podman generate kube climate-analysis > deployment.yaml
# ```

# %% [markdown]
# ## Part 6: Apptainer - Containers for HPC
#
# ### What is Apptainer (formerly Singularity)?
#
# Apptainer is designed specifically for **high-performance computing (HPC)** environments:
# - No root daemon (like Podman)
# - Integrates with HPC schedulers (SLURM, PBS)
# - Supports MPI and GPU workloads
# - Uses single-file container format (.sif)
# - Can run Docker images
#
# ### Why Apptainer for Research?
#
# **HPC-Specific Challenges:**
# - Shared systems: thousands of users
# - No root access for users
# - Need MPI across containers
# - GPU acceleration required
# - Batch job schedulers
#
# **Apptainer Solutions:**
# - Runs without privileges
# - Seamless MPI integration
# - Native GPU support
# - Works with job schedulers
# - Security model fits HPC
#
# ### Key Differences from Docker/Podman
#
# **1. Single File Format**
# ```bash
# # Docker: multiple layers in directory
# /var/lib/docker/overlay2/...
#
# # Apptainer: single .sif file
# climate-analysis.sif
# ```
#
# **2. No Build-Time Privileges Needed**
# ```bash
# # Build from Docker image (no root required)
# apptainer build climate.sif docker://python:3.10-slim
#
# # Build from definition file (may need root or --fakeroot)
# apptainer build --fakeroot climate.sif climate.def
# ```
#
# **3. Different Default Behavior**
# ```bash
# # Docker: isolated by default
# docker run myimage           # Can't see host files
#
# # Apptainer: integrated by default
# apptainer run myimage.sif    # Can access /home automatically
# ```
#
# ### Apptainer Definition File
#
# Similar to Dockerfile but different syntax:
#
# ```apptainer
# Bootstrap: docker
# From: python:3.10-slim
#
# %labels
#     Author researcher@university.edu
#     Version v1.0
#
# %post
#     # Runs during build
#     apt-get update && apt-get install -y \
#         libhdf5-dev \
#         libnetcdf-dev
#
#     pip install numpy pandas xarray netCDF4
#
# %environment
#     export DATA_PATH=/data
#     export PYTHONUNBUFFERED=1
#
# %runscript
#     # Runs when 'apptainer run' is executed
#     exec python analyze_climate.py "$@"
#
# %files
#     # Copy files into container
#     requirements.txt /app/
#     analyze_climate.py /app/
#
# %test
#     # Runs at end of build
#     python -m pytest /app/tests
# ```
#
# ### Building and Running with Apptainer
#
# **Build from Docker Hub:**
# ```bash
# # Convert Docker image to Apptainer
# apptainer build climate.sif docker://ghcr.io/user/climate-analysis:v1.0
# ```
#
# **Build from definition:**
# ```bash
# # With fakeroot (no sudo needed)
# apptainer build --fakeroot climate.sif climate.def
# ```
#
# **Run on HPC:**
# ```bash
# # Interactive
# apptainer shell climate.sif
#
# # Execute command
# apptainer exec climate.sif python analyze_climate.py
#
# # Run default runscript
# apptainer run climate.sif --input data.nc
#
# # With GPU
# apptainer exec --nv climate.sif python gpu_analysis.py
#
# # With MPI (parallel across nodes)
# mpirun -n 128 apptainer exec climate.sif python mpi_analysis.py
# ```
#
# ### HPC Batch Job Example
# ```bash
# !/bin/bash
# #SBATCH --job-name=climate-analysis
# #SBATCH --nodes=4
# #SBATCH --ntasks-per-node=32
# #SBATCH --time=02:00:00
#
# module load mpi/openmpi
#
# # Container already built
# CONTAINER=/scratch/containers/climate.sif
#
# # Run MPI job across 4 nodes
# mpirun -n 128 apptainer exec $CONTAINER \
#     python mpi_climate_analysis.py \
#     --input /scratch/data/climate_global.nc \
#     --output /scratch/results/
# ```
#
# ### When to Use Apptainer
#
# **Choose Apptainer if:**
# - Running on HPC clusters
# - Need MPI parallelization
# - Need GPU acceleration
# - Must work with job schedulers
# - Institution provides Apptainer (many HPC centers do)
#
# **Choose Docker/Podman if:**
# - Local development
# - Cloud deployment
# - CI/CD pipelines
# - Need Docker ecosystem tools

# %% [markdown]
# ## Part 7: Cross-Language Considerations
#
# Containers are language-agnostic! The same principles apply to all research software.
#
# ### R Research Project
#
# ```dockerfile
# FROM rocker/tidyverse:4.3.0
#
# # Rocker provides R + RStudio + tidyverse
# LABEL maintainer="researcher@university.edu"
#
# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     libgdal-dev \
#     libudunits2-dev
#
# # Install R packages
# RUN R -e "install.packages(c('sf', 'raster', 'terra'), \
#                            repos='http://cran.rstudio.com/')"
#
# # Copy R scripts
# COPY analysis.R /app/
# COPY data_processing.R /app/
#
# WORKDIR /app
# CMD ["R"]
# ```
#
# **Run R analysis:**
# ```bash
# docker run -v ./data:/data rocker-analysis Rscript analysis.R
# ```
#
# ### Julia Research Project
#
# ```dockerfile
# FROM julia:1.9
#
# # Create project environment
# WORKDIR /app
# COPY Project.toml Manifest.toml ./
#
# # Precompile packages
# RUN julia --project=. -e 'using Pkg; Pkg.instantiate()'
#
# COPY . .
#
# CMD ["julia"]
# ```
#
# **Run Julia code:**
# ```bash
# docker run -v ./data:/data julia-analysis julia --project=. analysis.jl
# ```
#
# ### C++ with Dependencies
#
# ```dockerfile
# FROM ubuntu:22.04
#
# # Install compilers and libraries
# RUN apt-get update && apt-get install -y \
#     g++ \
#     cmake \
#     libboost-all-dev \
#     libeigen3-dev \
#     libopenblas-dev
#
# WORKDIR /app
# COPY . .
#
# # Build during image creation
# RUN mkdir build && cd build && \
#     cmake .. && \
#     make -j$(nproc)
#
# CMD ["./build/climate_simulation"]
# ```
#
# ### Mixed-Language Project
#
# Many research projects use multiple languages:
#
# ```dockerfile
# FROM ubuntu:22.04
#
# # Install Python, R, and Julia
# RUN apt-get update && apt-get install -y \
#     python3 python3-pip \
#     r-base \
#     wget
#
# # Install Julia
# RUN wget https://julialang-s3.julialang.org/bin/linux/x64/1.9/julia-1.9.0-linux-x86_64.tar.gz && \
#     tar xzf julia-1.9.0-linux-x86_64.tar.gz -C /opt && \
#     ln -s /opt/julia-1.9.0/bin/julia /usr/local/bin/julia
#
# # Install language-specific packages
# RUN pip3 install numpy pandas
# RUN R -e "install.packages('ggplot2')"
# RUN julia -e 'using Pkg; Pkg.add("DataFrames")'
#
# COPY . /app
# WORKDIR /app
# ```
#
# ### Language-Specific Base Images
#
# Use official images for best practices:
# - **Python**: `python:3.10-slim`, `continuumio/miniconda3`
# - **R**: `rocker/r-ver:4.3.0`, `rocker/tidyverse`, `rocker/rstudio`
# - **Julia**: `julia:1.9`, `julia:1.9-alpine`
# - **Java**: `openjdk:17`, `eclipse-temurin:17`
# - **Node.js**: `node:18-alpine`
# - **Go**: `golang:1.20`
# - **Rust**: `rust:1.70`

# %% [markdown]
# ## Part 8: Best Practices for Research Containers
#
# ### 1. Make Containers Reproducible
#
# **Pin all versions:**
# ```dockerfile
# # Bad: versions may change
# FROM python:3
# RUN pip install numpy
#
# # Good: explicit versions
# FROM python:3.10.11-slim
# RUN pip install numpy==1.24.3
# ```
#
# **Use specific base image tags:**
# - Avoid: `FROM python:latest` (changes over time)
# - Use: `FROM python:3.10.11-slim` (immutable)
#
# ### 2. Keep Images Small
#
# **Use minimal base images:**
# ```dockerfile
# # Full: ~900 MB
# FROM python:3.10
#
# # Slim: ~150 MB
# FROM python:3.10-slim
#
# # Alpine: ~50 MB (but may have compatibility issues)
# FROM python:3.10-alpine
# ```
#
# **Clean up in same layer:**
# ```dockerfile
# # Creates 2 layers (unnecessary)
# RUN apt-get update && apt-get install -y gcc
# RUN apt-get clean
#
# # Single layer (smaller image)
# RUN apt-get update && apt-get install -y gcc \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*
# ```
#
# ### 3. Security Best Practices
#
# **Don't run as root:**
# ```dockerfile
# # Create non-root user
# RUN useradd -m -s /bin/bash researcher
# WORKDIR /home/researcher/app
#
# # Copy files with correct ownership
# COPY --chown=researcher:researcher . .
#
# # Switch to non-root
# USER researcher
# ```
#
# **Don't include secrets:**
# ```dockerfile
# # BAD - secrets in image
# ENV API_KEY=secret123
# COPY .env .
#
# # GOOD - secrets at runtime
# # Pass via: docker run -e API_KEY=$API_KEY ...
# ```
#
# ### 4. Document Everything
#
# **Add metadata labels:**
# ```dockerfile
# LABEL maintainer="researcher@university.edu"
# LABEL version="1.0.0"
# LABEL description="Climate analysis for Nature paper"
# LABEL org.opencontainers.image.source="https://github.com/user/repo"
# LABEL org.opencontainers.image.licenses="MIT"
# ```
#
# **Include usage in README:**
# ```markdown
# ## Running with Docker
#
# 1. Pull the image:
#    ```bash
#    docker pull ghcr.io/user/climate-analysis:v1.0
#    ```
#
# 2. Run analysis:
#    ```bash
#    docker run -v ./data:/data ghcr.io/user/climate-analysis:v1.0
#    ```
# ```
#
# ### 5. Version Your Containers
#
# **Tag with semantic versions:**
# ```bash
# docker build -t myproject:1.0.0 .
# docker build -t myproject:1.0 .    # minor version
# docker build -t myproject:1 .      # major version
# docker build -t myproject:latest . # latest (use carefully!)
# ```
#
# **Match code versions:**
# - Git tag: `v1.0.0` → Container tag: `1.0.0`
# - Helps trace container back to code version
#
# ### 6. Test Your Containers
#
# **Run tests during build:**
# ```dockerfile
# COPY tests/ tests/
# RUN python -m pytest tests/
# ```
#
# **Include CI/CD for containers:**
# ```yaml
# # .github/workflows/docker.yml
# name: Build Container
# on: [push]
# jobs:
#   build:
#     runs-on: ubuntu-latest
#     steps:
#       - uses: actions/checkout@v3
#       - name: Build image
#         run: docker build -t test .
#       - name: Test image
#         run: docker run test python -m pytest
# ```

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Curious about different containerization approaches? Explore these comparisons:</p>
#     <ul>
#         <li><strong>Conda environment vs. container</strong>: Create both for the same
#         project. Which is easier to share? Which is more reproducible? When would you
#         choose each?</li>
#         <li><strong>Compare Docker and Podman</strong>: If you have access to both, try
#         running the same container with each tool. Notice the differences in commands and
#         permissions.</li>
#         <li><strong>Test portability</strong>: Build a container on your laptop and run
#         it on a cluster or cloud instance. Does it truly work everywhere? What challenges
#         arise?</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 9: Choosing the Right Tool
#
# ### Decision Matrix
#
# | Use Case | Docker | Podman | Apptainer |
# |----------|--------|--------|-----------|
# | **Local development** | ✅ Best | ✅ Good | ❌ Overkill |
# | **Shared server (no root)** | ❌ Needs root | ✅ Best | ✅ Good |
# | **HPC cluster** | ❌ Rare | ⚠️ Possible | ✅ Best |
# | **Cloud deployment** | ✅ Best | ✅ Good | ❌ Limited |
# | **CI/CD pipelines** | ✅ Best | ✅ Good | ⚠️ Possible |
# | **GPU workloads** | ✅ Good | ✅ Good | ✅ Best |
# | **MPI parallel** | ⚠️ Tricky | ⚠️ Tricky | ✅ Best |
# | **Windows/Mac** | ✅ Desktop | ⚠️ VM needed | ❌ Limited |
#
# ### Practical Recommendations
#
# **For most researchers:**
# 1. Start with **Docker** (easiest learning curve, most resources)
# 2. Use **Podman** if you don't have root or prefer security
# 3. Switch to **Apptainer** when moving to HPC
#
# **For HPC users:**
# 1. Develop locally with Docker
# 2. Convert to Apptainer for cluster: `apptainer build app.sif docker://...`
# 3. Submit batch jobs with Apptainer
#
# **For collaborative projects:**
# 1. Provide Dockerfile (works with all tools)
# 2. Publish to Docker Hub or GitHub Container Registry
# 3. Document how to use with each tool
#
# ### Interoperability
#
# **Good news**: These tools are largely interoperable!
#
# ```bash
# # Build with Docker
# docker build -t myproject .
# docker save myproject -o myproject.tar
#
# # Load into Podman
# podman load -i myproject.tar
#
# # Convert to Apptainer
# apptainer build myproject.sif docker-archive://myproject.tar
# # Or directly:
# apptainer build myproject.sif docker-daemon://myproject:latest
# ```

# %% [markdown]
# ## Part 10: Containers in the Research Workflow
#
# ### Integration with Previous Lectures
#
# Containers complement everything we've learned:
#
# **Lecture 5 (Testing):**
# ```dockerfile
# # Run tests in container
# COPY tests/ tests/
# RUN pytest tests/ --cov=.
# ```
#
# **Lecture 6 (CI/CD):**
# ```yaml
# # .github/workflows/container.yml
# jobs:
#   build-and-test:
#     runs-on: ubuntu-latest
#     steps:
#       - uses: actions/checkout@v3
#       - name: Build container
#         run: docker build -t test .
#       - name: Run tests in container
#         run: docker run test pytest
# ```
#
# **Lecture 8 (Documentation):**
# - Container image IS documentation
# - Dockerfile shows exact build process
# - README explains container usage
#
# ### Publishing Research with Containers
#
# **Step 1: Freeze your environment**
# ```bash
# # Create Dockerfile from working environment
# docker build -t paper-analysis:v1.0 .
# ```
#
# **Step 2: Archive on registry**
# ```bash
# # Push to GitHub Container Registry
# docker push ghcr.io/user/paper-analysis:v1.0
# ```
#
# **Step 3: Get permanent identifier**
# - Use Zenodo to archive container
# - Get DOI for long-term reference
# - Link from paper
#
# **Step 4: Document in paper**
# ```markdown
# ## Reproducibility Statement
#
# All analyses can be reproduced using the containerized environment:
#
# ```bash
# docker pull ghcr.io/user/paper-analysis:v1.0
# docker run -v ./data:/data ghcr.io/user/paper-analysis:v1.0
# ```
#
# Archived at: https://doi.org/10.5281/zenodo.XXXXXXX
# ```
#
# ### Long-Term Reproducibility
#
# **Containers provide:**
# - Snapshot of entire computational environment
# - Work years or decades later (if base OS still runs)
# - Better than "install these packages" (which versions?)
#
# **Limitations:**
# - Container size (may be GBs)
# - Storage costs
# - Base OS compatibility (old containers on new systems)
#
# **Best practices:**
# - Archive containers for published papers
# - Document base system requirements
# - Consider minimal containers (smaller = longer life)
# - Use standard base images (better maintained)

# %% [markdown]
# ## Summary
#
# ### Key Takeaways
#
# **1. Virtual environments (conda, venv) are great but limited:**
# - Handle Python packages well
# - Can't guarantee system-level reproducibility
# - OS differences still cause problems
#
# **2. Containers solve the reproducibility problem:**
# - Package entire computational environment
# - Work consistently across platforms
# - Are the gold standard for computational reproducibility
#
# **3. Three main containerization tools:**
# - **Docker**: Industry standard, great for development and deployment
# - **Podman**: Rootless alternative, better security, Docker-compatible
# - **Apptainer**: HPC-focused, MPI/GPU support, single-file format
#
# **4. Containers are language-agnostic:**
# - Work for Python, R, Julia, C++, mixed projects
# - Same principles across all languages
# - Official base images available
#
# **5. Best practices:**
# - Pin all versions (base image, packages, system libraries)
# - Use minimal base images
# - Run as non-root user
# - Document usage clearly
# - Version your containers
# - Test during build
#
# ### The Reproducibility Hierarchy
#
# From weakest to strongest reproducibility:
#
# 1. **"Install these packages"** - Will probably break
# 2. **requirements.txt / environment.yml** - Better, but incomplete
# 3. **Locked dependencies (conda-lock)** - Good for Python layer
# 4. **Containers** - Best: captures everything
# 5. **Containers + DOI** - Perfect: permanent archived environment
#
# ### Next Steps
#
# **Start small:**
# 1. Write a simple Dockerfile for a current project
# 2. Build and test it locally
# 3. Share with a colleague - does it work for them?
#
# **Level up:**
# 1. Add container building to your CI/CD
# 2. Publish containers to a registry
# 3. Use containers for paper reproducibility
#
# **Advanced:**
# 1. Learn Apptainer for HPC work
# 2. Explore Podman for security-sensitive projects
# 3. Create container templates for your research group
#
# ### The Big Picture
#
# Containers represent the current state-of-the-art for computational reproducibility.
# They're not perfect (still evolving), but they're the best tool we have for ensuring
# that "it works on my machine" means "it works on every machine."
#
# Combined with version control (Lecture 1-2), testing (Lecture 5), CI/CD (Lecture 6),
# and documentation (Lecture 8), containers complete the toolkit for producing
# truly reproducible research software.
#
# Your future self - and the entire research community - will thank you for
# containerizing your work!

# %% [markdown]
# ## Additional Resources
#
# ### Docker Documentation
# - Official Docker documentation: https://docs.docker.com/
# - Docker Hub (image registry): https://hub.docker.com/
# - Dockerfile best practices: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
#
# ### Podman Resources
# - Podman official site: https://podman.io/
# - Podman documentation: https://docs.podman.io/
# - Rootless containers guide: https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md
#
# ### Apptainer/Singularity Resources
# - Apptainer documentation: https://apptainer.org/docs/
# - Apptainer user guide: https://apptainer.org/docs/user/latest/
# - Converting Docker to Apptainer: https://apptainer.org/docs/user/latest/docker_and_oci.html
#
# ### Research-Specific Guides
# - Rocker Project (R containers): https://rocker-project.org/
# - Bioconda containers: https://bioconda.github.io/
# - Neurodocker (neuroscience): https://github.com/ReproNim/neurodocker
#
# ### Container Registries
# - Docker Hub: https://hub.docker.com/
# - GitHub Container Registry: https://ghcr.io/
# - Quay.io: https://quay.io/
# - GitLab Container Registry: https://docs.gitlab.com/ee/user/packages/container_registry/
#
# **Note**: This lecture provides practical introduction to containerization.
# All references are to official documentation and established tools in the
# research software engineering community.
