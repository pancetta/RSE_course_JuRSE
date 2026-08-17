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
# # Lecture 12: Scientific Workflows and Automation
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
#     <img src="lecture_12_qr_code.png" alt="This Lecture QR Code" width="150"/>
#     <p><strong>This Lecture</strong></p>
#   </div>
# </div>
#
# ## Overview
# Scientific research often involves complex, multi-step data analysis pipelines:
# download data, preprocess it, run simulations, analyze results, generate figures,
# and compile reports. As projects grow, manually executing these steps becomes
# error-prone, time-consuming, and difficult to reproduce. This lecture introduces
# scientific workflow management systems that automate these pipelines, track
# dependencies between steps, and ensure reproducibility.
#
# We'll explore how workflow systems differ from simple shell scripts and Makefiles,
# when to use each tool, and demonstrate practical examples using both Make and
# modern workflow managers like Snakemake. While examples use Python, the concepts
# apply across programming languages.
#
# **Duration**: ~90 minutes
#
# ## Prerequisites
#
# Before starting this lecture, you should be familiar with:
# - Basic shell commands and scripting
# - Python programming and file I/O (covered in Lectures 2-4)
# - Understanding of research data workflows
# - Containerization concepts (covered in Lecture 9, helpful but not required)
#
# This lecture builds on your programming skills and introduces workflow automation tools.
#
# ## Learning Objectives
# - Understand the challenges of managing complex research pipelines
# - Recognize when to use scripts, Make, or workflow management systems
# - Learn the fundamentals of dependency-based execution
# - Write basic Snakemake workflows for data analysis
# - Understand alternatives (Nextflow, CWL, Galaxy) and their use cases
# - Apply workflow concepts across different programming languages
# - Integrate workflows with version control and containerization

# %% [markdown]
# ## Part 1: The Pipeline Problem
#
# ### When Manual Execution Breaks Down
#
# Dr. Elena Rodriguez ran the same analysis every week for her climate research.
# Her workflow involved:
# 1. Download satellite data from three different sources
# 2. Convert formats and merge datasets
# 3. Run quality control checks
# 4. Execute climate model
# 5. Generate 15 different visualizations
# 6. Compile results into a report
#
# Every Monday, she would:
# ```bash
# python download_data.py --source nasa
# python download_data.py --source noaa
# python download_data.py --source esa
# python merge_datasets.py
# python quality_control.py
# python run_model.py --config weekly.json
# python plot_temperature.py
# python plot_precipitation.py
# python plot_wind.py
# # ... 12 more plotting scripts
# python generate_report.py
# ```
#
# **The problems emerged quickly:**
#
# **Problem 1: What if something fails midway?**
# - Download succeeded, but merge failed
# - She reran the entire pipeline
# - Wasted time re-downloading gigabytes of data
# - No way to restart from the failure point
#
# **Problem 2: What changed?**
# - Updated the plotting code
# - Should she rerun everything?
# - Or just the plots?
# - No systematic way to know
#
# **Problem 3: Parallel execution**
# - The 15 plots could run simultaneously
# - But she ran them sequentially
# - Analysis that could take 10 minutes took 90 minutes
#
# **Problem 4: Documentation**
# - Six months later, a collaborator asked: "How do I reproduce this?"
# - The README.md was outdated
# - Some scripts had been renamed
# - Parameters had changed
#
# **Problem 5: Reproducibility**
# - Which version of the code produced Figure 3 in the paper?
# - She couldn't remember the exact order she ran things
# - Some intermediate files had been deleted
#
# **She needed automation. But what kind?**

# %% [markdown]
# ## Part 2: Automation Approaches - From Scripts to Workflows
#
# ### Approach 1: The Shell Script
#
# Elena's first attempt was a simple bash script:

# %% [markdown]
# ```bash
# !/bin/bash
# # run_analysis.sh
#
# python download_data.py --source nasa
# python download_data.py --source noaa
# python download_data.py --source esa
# python merge_datasets.py
# python quality_control.py
# python run_model.py --config weekly.json
# python plot_temperature.py
# python plot_precipitation.py
# # ... more commands
# ```

# %% [markdown]
# **Advantages:**
# - Simple and straightforward
# - Easy to understand
# - Works across all platforms (with Bash available)
# - No additional tools needed
#
# **Limitations:**
# - Runs everything every time (no dependency tracking)
# - No parallelization
# - If step 5 fails, must restart from step 1
# - No automatic detection of what needs rerunning
#
# **When to use:** Simple, linear pipelines that run quickly; one-off analyses

# %% [markdown]
# ### Approach 2: Smarter Shell Scripts
#
# Elena added some logic:

# %% [markdown]
# ```bash
# !/bin/bash
# # run_analysis_smart.sh
#
# # Only download if data doesn't exist
# if [ ! -f "data/nasa.nc" ]; then
#     python download_data.py --source nasa
# fi
#
# # Only merge if inputs are newer than output
# if [ data/nasa.nc -nt data/merged.nc ] || \
#    [ data/noaa.nc -nt data/merged.nc ]; then
#     python merge_datasets.py
# fi
#
# # ... more conditional logic
# ```

# %% [markdown]
# **Improvements:**
# - Skips unnecessary steps
# - Checks file timestamps
# - More efficient
#
# **New Problems:**
# - Complex conditional logic
# - Hard to maintain
# - Error-prone file timestamp checks
# - Still no parallelization
# - Becomes unwieldy for complex dependencies
#
# **When to use:** Moderately complex pipelines where some caching is beneficial
#
# ### The Core Problem: Dependency Management
#
# What Elena really needed was a system that understood:
# - **Dependencies**: Which outputs depend on which inputs?
# - **Freshness**: Which files are up-to-date?
# - **Ordering**: What order must steps execute in?
# - **Parallelization**: Which steps can run simultaneously?
# - **Failure handling**: Which steps to rerun after a failure?
#
# This is exactly what **build systems** and **workflow managers** provide.

# %% [markdown]
# ## Part 3: Make - The Classic Build System
#
# ### Introduction to Make
#
# Make was created in 1976 for compiling software, but it's excellent for research
# workflows. Make uses a `Makefile` that declares:
# - **Targets**: Files to create (outputs)
# - **Prerequisites**: Files needed to create the target (inputs)
# - **Recipes**: Commands to create the target
#
# Make automatically:
# - Determines what needs updating based on file timestamps
# - Runs commands in the correct order
# - Parallelizes independent tasks
# - Stops on errors
#
# ### Basic Make Syntax
#
# A Make rule follows this pattern:
# ```makefile
# target: prerequisites
#     recipe
# ```
#
# **Important**: The recipe line MUST start with a TAB character, not spaces.

# %% [markdown]
# ### Example: A Research Data Pipeline with Make
#
# Let's create a realistic example. Imagine analyzing temperature data:

# %% [markdown]
# ```makefile
# # Makefile for temperature analysis pipeline
#
# # Final output
# report.pdf: results/plots.png results/statistics.txt
#     python generate_report.py
#
# # Generate plots from analyzed data
# results/plots.png: data/processed/temperature_clean.csv
#     python plot_data.py --input $< --output $@
#
# # Compute statistics
# results/statistics.txt: data/processed/temperature_clean.csv
#     python compute_stats.py --input $< --output $@
#
# # Clean and validate data
# data/processed/temperature_clean.csv: data/raw/temperature.csv
#     python clean_data.py --input $< --output $@
#
# # Download raw data
# data/raw/temperature.csv:
#     python download_data.py --output $@
#
# # Utility targets
# .PHONY: clean all
#
# all: report.pdf
#
# clean:
#     rm -rf data/processed data/raw results
# ```

# %% [markdown]
# Drawn as a graph, this Makefile is exactly the DAG `make` builds internally to decide what
# to run and in what order:
#
# <img src="figures/make_dependency_dag.svg" alt="Directed acyclic graph of the Make pipeline: raw temperature data flows through cleaning, then fans out in parallel to plots and statistics, which join into the final report" width="760"/>
#
# *`plots.png` and `statistics.txt` both depend only on `temperature_clean.csv`, not on each
# other—that's what makes them safe to build in parallel with `make -j`.*
#
# **Key Make features demonstrated:**
#
# - `$<`: First prerequisite (input file)
# - `$@`: Target (output file)
# - `.PHONY`: Targets that aren't files (like `clean`, `all`)
# - Dependencies chain automatically: changing raw data triggers everything
#
# **Running Make:**
# ```bash
# make              # Builds the default target (first in file)
# make report.pdf   # Builds specific target
# make -j 4         # Runs with 4 parallel jobs
# make clean        # Runs the clean target
# make -n           # Dry run (shows what would execute)
# ```

# %% [markdown]
# ### Make's Intelligence
#
# When you run `make`, it:
# 1. Checks if `report.pdf` exists and its timestamp
# 2. Checks timestamps of all dependencies (recursively)
# 3. Identifies what's out of date
# 4. Runs only necessary commands
# 5. Executes independent tasks in parallel (with `-j`)
#
# **Example scenario:**
# - You modify `plot_data.py`
# - Run `make report.pdf`
# - Make sees the plot script is newer than `plots.png`
# - Reruns only the plotting and report generation
# - Skips data download, cleaning, and statistics (still up-to-date)

# %% [markdown]
# ### Make Advantages and Limitations
#
# **Advantages:**
# - Ubiquitous (available on all Unix systems)
# - Simple syntax for simple workflows
# - Language-agnostic (works with any command-line tools)
# - Parallel execution built-in
# - Dependency tracking based on file timestamps
# - Well-understood and documented
#
# **Limitations:**
# - Syntax can be cryptic (`$@`, `$<`, etc.)
# - TAB vs. spaces is error-prone
# - File-based only (can't track other dependencies easily)
# - Limited pattern matching
# - No built-in support for:
#   - Remote execution
#   - Resource management (CPU, memory)
#   - Cluster/cloud computing
#   - Complex parameter sweeps
#
# **When to use Make:**
# - Moderate complexity pipelines
# - File-based workflows
# - Need broad compatibility
# - Integration with existing build systems

# %% [markdown]
# ### Make Beyond Python
#
# Make is language-agnostic. Here's the same pipeline in R:
#
# ```makefile
# # Makefile for R-based analysis
#
# report.pdf: results/plots.png results/statistics.txt
#     Rscript generate_report.R
#
# results/plots.png: data/processed/temperature_clean.csv
#     Rscript plot_data.R data/processed/temperature_clean.csv $@
#
# data/processed/temperature_clean.csv: data/raw/temperature.csv
#     Rscript clean_data.R $< $@
# ```
#
# Or mixing languages:
# ```makefile
# # Download with Python, analyze with R, plot with Julia
# data/raw/data.csv:
#     python download.py
#
# data/processed/data.csv: data/raw/data.csv
#     Rscript clean.R $< $@
#
# results/plot.png: data/processed/data.csv
#     julia plot.jl $< $@
# ```

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Want to understand dependency management deeply? Explore these Make concepts:</p>
#     <ul>
#         <li><strong>Visualize your dependencies</strong>: Draw the dependency graph for
#         your research project by hand. Which files depend on which? Where do changes
#         ripple through? Make automates this thinking!</li>
#         <li><strong>Test incremental builds</strong>: Create a simple Makefile with 3-4
#         steps. Run it, change one input file, run again. Which steps re-run? Which are
#         skipped? Understanding this saves computation time.</li>
#         <li><strong>Break something on purpose</strong>: Delete an intermediate file and
#         run <code>make</code>. Does it rebuild just what's needed? Try making a file
#         older with <code>touch -t</code> - what happens?</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 4: Snakemake - Make for the 21st Century
#
# ### Why Snakemake?
#
# Snakemake is a workflow management system that combines Make's core concepts with
# modern features for scientific computing. Created by Johannes Köster in 2012, it's
# widely used in bioinformatics and computational research.
#
# **Key improvements over Make:**
# - Python-based syntax (more intuitive)
# - Pattern matching and wildcards
# - Automatic job submission to clusters
# - Container integration (Docker, Singularity)
# - Conda environment management
# - Remote file handling (S3, HTTP, etc.)
# - Detailed execution reports
#
# **Reference**: Köster, J., & Rahmann, S. (2012). "Snakemake—a scalable
# bioinformatics workflow engine". *Bioinformatics*, 28(19), 2520-2522.
# DOI: 10.1093/bioinformatics/bts480

# %% [markdown]
# ### Basic Snakemake Syntax
#
# A Snakemake workflow is written in a `Snakefile` (similar to `Makefile`).
# Rules follow this pattern:
#
# ```python
# rule rule_name:
#     input:
#         "input_file.txt"
#     output:
#         "output_file.txt"
#     shell:
#         "python process.py {input} {output}"
# ```

# %% [markdown]
# ### Example: Temperature Analysis with Snakemake
#
# Let's recreate Elena's workflow in Snakemake:

# %% [markdown]
# ```python
# # Snakefile for temperature analysis pipeline
#
# # Define the final target
# rule all:
#     input:
#         "report.pdf"
#
# # Download raw data
# rule download_data:
#     output:
#         "data/raw/temperature.csv"
#     shell:
#         "python download_data.py --output {output}"
#
# # Clean and validate data
# rule clean_data:
#     input:
#         "data/raw/temperature.csv"
#     output:
#         "data/processed/temperature_clean.csv"
#     shell:
#         "python clean_data.py --input {input} --output {output}"
#
# # Generate plots
# rule plot_data:
#     input:
#         "data/processed/temperature_clean.csv"
#     output:
#         "results/plots.png"
#     shell:
#         "python plot_data.py --input {input} --output {output}"
#
# # Compute statistics
# rule compute_stats:
#     input:
#         "data/processed/temperature_clean.csv"
#     output:
#         "results/statistics.txt"
#     shell:
#         "python compute_stats.py --input {input} --output {output}"
#
# # Generate final report
# rule generate_report:
#     input:
#         plots="results/plots.png",
#         stats="results/statistics.txt"
#     output:
#         "report.pdf"
#     shell:
#         "python generate_report.py --plots {input.plots} --stats {input.stats}"
# ```

# %% [markdown]
# **Running Snakemake:**
# ```bash
# snakemake              # Runs the first rule (usually 'all')
# snakemake report.pdf   # Runs specific target
# snakemake -n           # Dry run (shows execution plan)
# snakemake -j 4         # Runs with 4 parallel jobs
# snakemake --dag | dot -Tpng > dag.png  # Visualize workflow
# ```

# %% [markdown]
# ### The Power of Wildcards
#
# Snakemake's killer feature is wildcards for pattern matching. Instead of writing
# separate rules for each file, use patterns:

# %% [markdown]
# ```python
# # Process multiple samples with one rule
# SAMPLES = ["sample1", "sample2", "sample3"]
#
# rule all:
#     input:
#         expand("results/{sample}_plot.png", sample=SAMPLES)
#
# # Wildcard rule: processes any sample
# rule process_sample:
#     input:
#         "data/raw/{sample}.csv"
#     output:
#         "data/processed/{sample}_clean.csv"
#     shell:
#         "python clean_data.py --input {input} --output {output}"
#
# rule plot_sample:
#     input:
#         "data/processed/{sample}_clean.csv"
#     output:
#         "results/{sample}_plot.png"
#     shell:
#         "python plot_data.py --input {input} --output {output}"
# ```
#
# Snakemake automatically:
# - Matches the wildcard `{sample}` to actual filenames
# - Creates the dependency graph
# - Runs all three samples (potentially in parallel)

# %% [markdown]
# ### Configuration and Parameters
#
# Snakemake supports configuration files for parameters:

# %% [markdown]
# ```python
# # Snakefile with configuration
# configfile: "config.yaml"
#
# rule process_data:
#     input:
#         "data/raw/{sample}.csv"
#     output:
#         "data/processed/{sample}_clean.csv"
#     params:
#         threshold=config["quality_threshold"],
#         method=config["cleaning_method"]
#     shell:
#         "python clean_data.py --input {input} --output {output} "
#         "--threshold {params.threshold} --method {params.method}"
# ```
#
# With `config.yaml`:
# ```yaml
# quality_threshold: 0.95
# cleaning_method: "interpolation"
# samples:
#   - sample1
#   - sample2
#   - sample3
# ```

# %% [markdown]
# ### Conda Integration
#
# Snakemake can automatically create environments for each rule:

# %% [markdown]
# ```python
# rule analyze_data:
#     input:
#         "data/processed/data.csv"
#     output:
#         "results/analysis.txt"
#     conda:
#         "envs/analysis.yaml"
#     shell:
#         "python analyze.py {input} {output}"
# ```
#
# Where `envs/analysis.yaml` contains:
# ```yaml
# channels:
#   - conda-forge
# dependencies:
#   - python=3.9
#   - pandas=1.3
#   - numpy=1.21
# ```
#
# Snakemake automatically creates and activates this environment before running
# the rule.

# %% [markdown]
# ### Container Support
#
# Snakemake integrates with containers for ultimate reproducibility:

# %% [markdown]
# ```python
# rule analyze_in_container:
#     input:
#         "data/input.csv"
#     output:
#         "results/output.txt"
#     container:
#         "docker://continuumio/miniconda3:latest"
#     shell:
#         "python analyze.py {input} {output}"
# ```
#
# This automatically:
# - Pulls the Docker container (if needed)
# - Runs the command inside the container
# - Maps input/output files appropriately

# %% [markdown]
# ### Cluster Execution
#
# Snakemake can submit jobs to cluster schedulers (SLURM, PBS, SGE):

# %% [markdown]
# ```bash
# # Submit to SLURM cluster
# snakemake --cluster "sbatch --cpus-per-task={threads}" --jobs 100
#
# # With resource specifications in rules
# ```
#
# ```python
# rule intensive_computation:
#     input:
#         "data/large_dataset.csv"
#     output:
#         "results/computation.txt"
#     threads: 8
#     resources:
#         mem_mb=16000,
#         runtime=240
#     shell:
#         "python compute.py --threads {threads} {input} {output}"
# ```

# %% [markdown]
# ### A Complete Realistic Example
#
# Here's a realistic workflow for climate data analysis:

# %% [markdown]
# ```python
# # Snakefile for multi-source climate analysis
#
# SOURCES = ["nasa", "noaa", "esa"]
# VARIABLES = ["temperature", "precipitation", "wind"]
#
# rule all:
#     input:
#         "report/final_report.pdf",
#         "results/combined_analysis.html"
#
# # Download data from multiple sources
# rule download_source:
#     output:
#         "data/raw/{source}_data.nc"
#     params:
#         source="{source}"
#     shell:
#         "python scripts/download_data.py --source {params.source} --output {output}"
#
# # Convert NetCDF to CSV for processing
# rule convert_to_csv:
#     input:
#         "data/raw/{source}_data.nc"
#     output:
#         "data/converted/{source}_data.csv"
#     conda:
#         "envs/netcdf.yaml"
#     shell:
#         "python scripts/convert_netcdf.py {input} {output}"
#
# # Merge all sources
# rule merge_sources:
#     input:
#         expand("data/converted/{source}_data.csv", source=SOURCES)
#     output:
#         "data/merged/all_sources.csv"
#     shell:
#         "python scripts/merge_datasets.py {input} --output {output}"
#
# # Quality control
# rule quality_control:
#     input:
#         "data/merged/all_sources.csv"
#     output:
#         data="data/processed/qc_data.csv",
#         report="results/qc_report.txt"
#     shell:
#         "python scripts/quality_control.py {input} --data {output.data} --report {output.report}"
#
# # Analyze each variable
# rule analyze_variable:
#     input:
#         "data/processed/qc_data.csv"
#     output:
#         "results/analysis_{variable}.json"
#     params:
#         variable="{variable}"
#     threads: 4
#     shell:
#         "python scripts/analyze.py --input {input} --variable {params.variable} "
#         "--output {output} --threads {threads}"
#
# # Create plots for each variable
# rule plot_variable:
#     input:
#         data="data/processed/qc_data.csv",
#         analysis="results/analysis_{variable}.json"
#     output:
#         "figures/{variable}_plot.png"
#     shell:
#         "python scripts/plot_variable.py --data {input.data} "
#         "--analysis {input.analysis} --output {output}"
#
# # Generate HTML summary
# rule create_html_summary:
#     input:
#         plots=expand("figures/{variable}_plot.png", variable=VARIABLES),
#         analyses=expand("results/analysis_{variable}.json", variable=VARIABLES)
#     output:
#         "results/combined_analysis.html"
#     shell:
#         "python scripts/generate_html.py --plots {input.plots} "
#         "--analyses {input.analyses} --output {output}"
#
# # Generate PDF report
# rule generate_report:
#     input:
#         plots=expand("figures/{variable}_plot.png", variable=VARIABLES),
#         analyses=expand("results/analysis_{variable}.json", variable=VARIABLES),
#         qc="results/qc_report.txt"
#     output:
#         "report/final_report.pdf"
#     shell:
#         "python scripts/create_pdf_report.py --plots {input.plots} "
#         "--analyses {input.analyses} --qc {input.qc} --output {output}"
# ```

# %% [markdown]
# This workflow:
# - Downloads data from 3 sources
# - Converts formats
# - Merges datasets
# - Performs quality control
# - Analyzes 3 variables in parallel
# - Creates visualizations
# - Generates both HTML and PDF reports
#
# **Running it:**
# ```bash
# snakemake -j 8       # Uses up to 8 cores
# snakemake --dag | dot -Tpng > workflow.png  # Visualize the DAG
# ```

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Ready to build real workflows? Try these multi-step explorations:</p>
#     <ul>
#         <li><strong>Convert your analysis to Snakemake</strong>: Take a shell script
#         with 3-4 steps (download, process, analyze, plot). Rewrite it as a Snakefile.
#         Notice how Snakemake thinks backwards from outputs!</li>
#         <li><strong>Add wildcards</strong>: If you process multiple similar files, try
#         using <code>{sample}</code> wildcards instead of writing separate rules. One rule
#         to rule them all!</li>
#         <li><strong>Visualize your workflow</strong>: Generate a DAG diagram of your
#         Snakemake workflow. Share it with a colleague - can they understand your pipeline
#         from the diagram alone?</li>
#     </ul>
# </div>

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Curious about parallelization and optimization? Experiment with workflow scaling:</p>
#     <ul>
#         <li><strong>Benchmark parallel execution</strong>: Run your Snakemake workflow
#         with <code>-j 1</code>, <code>-j 2</code>, <code>-j 4</code>, <code>-j 8</code>.
#         Time each run. Does it scale linearly? Why or why not?</li>
#         <li><strong>Find the bottleneck</strong>: Look at your workflow DAG. Which steps
#         can run in parallel? Which must run sequentially? The longest sequential chain
#         determines minimum runtime.</li>
#         <li><strong>Add resource constraints</strong>: Try declaring memory or threads
#         requirements for rules. What happens when you over-subscribe resources? Workflow
#         systems help prevent this!</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 5: Alternative Workflow Systems
#
# While Make and Snakemake are powerful, different research domains and use cases
# may benefit from alternative workflow systems. Here's an overview of the ecosystem.

# %% [markdown]
# ### Nextflow
#
# **Language**: Groovy-based DSL
# **Strengths**: Cloud computing, containerization, scalability
# **Common in**: Genomics, bioinformatics
#
# **Example Nextflow workflow:**
# ```groovy
# // Nextflow workflow (nextflow.nf)
#
# params.input = "data/*.fastq"
# params.outdir = "results"
#
# process qualityControl {
#     publishDir "${params.outdir}/qc"
#
#     input:
#     path(reads)
#
#     output:
#     path("*_qc.html")
#
#     script:
#     """
#     fastqc ${reads}
#     """
# }
#
# process trimReads {
#     input:
#     path(reads)
#
#     output:
#     path("*_trimmed.fastq")
#
#     script:
#     """
#     trimmomatic ${reads} ${reads.baseName}_trimmed.fastq
#     """
# }
#
# workflow {
#     input_ch = Channel.fromPath(params.input)
#     qualityControl(input_ch)
#     trimReads(input_ch)
# }
# ```
#
# **When to use Nextflow:**
# - Cloud-native workflows (AWS, Google Cloud, Azure)
# - Heavy use of containers
# - Large-scale genomics pipelines
# - Need for dataflow programming model
#
# **Reference**: Di Tommaso, P., et al. (2017). "Nextflow enables reproducible
# computational workflows". *Nature Biotechnology*, 35(4), 316-319.
# DOI: 10.1038/nbt.3820

# %% [markdown]
# ### Common Workflow Language (CWL)
#
# **Language**: YAML/JSON specification
# **Strengths**: Portability, standardization, tool interoperability
# **Common in**: Multi-institutional collaborations
#
# **Example CWL workflow:**
# ```yaml
# # workflow.cwl
# cwlVersion: v1.2
# class: Workflow
#
# inputs:
#   input_file: File
#   reference_genome: File
#
# outputs:
#   aligned_bam:
# type: File
#     outputSource: align/output_bam
#
# steps:
#   quality_check:
#     run: fastqc.cwl
#     in:
#       reads: input_file
#     out: [qc_report]
#
#   align:
#     run: bwa-mem.cwl
#     in:
#       reads: input_file
#       reference: reference_genome
#     out: [output_bam]
# ```
#
# **When to use CWL:**
# - Maximum portability across platforms
# - Need strict workflow specification
# - Collaboration across different institutions
# - Long-term workflow preservation
#
# **Reference**: Amstutz, P., et al. (2016). "Common Workflow Language".
# Available at: https://www.commonwl.org/

# %% [markdown]
# ### Galaxy
#
# **Interface**: Web-based GUI
# **Strengths**: User-friendly, no programming required, extensive tool library
# **Common in**: Biomedical research, teaching
#
# Galaxy provides a point-and-click interface for building workflows. Users:
# - Select tools from a catalog
# - Connect outputs to inputs graphically
# - Run workflows through a web browser
# - Share workflows via Galaxy servers
#
# **When to use Galaxy:**
# - Users uncomfortable with command-line
# - Teaching environments
# - Standardized analysis workflows
# - Need for web-based access
#
# **Reference**: Afgan, E., et al. (2018). "The Galaxy platform for accessible,
# reproducible and collaborative biomedical analyses". *Nucleic Acids Research*,
# 46(W1), W537-W544. DOI: 10.1093/nar/gky379

# %% [markdown]
# ### Apache Airflow
#
# **Language**: Python
# **Strengths**: Complex scheduling, monitoring, data engineering
# **Common in**: Data science, production pipelines
#
# **Example Airflow DAG:**
# ```python
# # airflow_dag.py
# from airflow import DAG
# from airflow.operators.bash import BashOperator
# from datetime import datetime, timedelta
#
# default_args = {
#     'owner': 'researcher',
#     'depends_on_past': False,
#     'start_date': datetime(2024, 1, 1),
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }
#
# dag = DAG(
#     'research_pipeline',
#     default_args=default_args,
#     schedule_interval='@daily',
# )
#
# download = BashOperator(
#     task_id='download_data',
#     bash_command='python download_data.py',
#     dag=dag,
# )
#
# process = BashOperator(
#     task_id='process_data',
#     bash_command='python process_data.py',
#     dag=dag,
# )
#
# download >> process  # Set dependency
# ```
#
# **When to use Airflow:**
# - Scheduled/recurring workflows
# - Complex dependencies
# - Need for monitoring dashboard
# - Integration with data engineering tools
#
# **Reference**: Apache Software Foundation. "Apache Airflow Documentation".
# Available at: https://airflow.apache.org/

# %% [markdown]
# ### Comparison Table
#
# | System | Language | Best For | Learning Curve | Cluster Support |
# |--------|----------|----------|----------------|-----------------|
# | **Make** | Makefile syntax | Simple pipelines, compilation | Low | Manual |
# | **Snakemake** | Python-like | Scientific workflows, HPC | Medium | Excellent |
# | **Nextflow** | Groovy | Cloud, containers, genomics | Medium-High | Excellent |
# | **CWL** | YAML/JSON | Portability, standards | Medium | Good |
# | **Galaxy** | GUI | Teaching, non-coders | Low | Good |
# | **Airflow** | Python | Data engineering, scheduling | High | Good |
#
# **Choosing a workflow system:**
# - **Small project, simple pipeline**: Make or shell script
# - **Python-based research, HPC**: Snakemake
# - **Genomics, cloud-first**: Nextflow
# - **Multi-institution, portability**: CWL
# - **Teaching, non-programmers**: Galaxy
# - **Production data pipelines**: Airflow

# %% [markdown]
# ## Part 6: Best Practices for Research Workflows
#
# ### Design Principles
#
# **1. Make workflows modular**
# - Each step should be a distinct, reusable unit
# - One rule/task per logical operation
# - Avoid monolithic scripts that do everything
#
# **2. Document dependencies explicitly**
# - Declare all inputs and outputs
# - Don't hide dependencies in code
# - Make implicit dependencies explicit
#
# **3. Use configuration files**
# - Separate parameters from workflow logic
# - Makes workflows reusable across projects
# - Easier to share and modify
#
# **4. Version control your workflows**
# - Workflows are code—treat them as such
# - Use Git for workflow files
# - Include example configuration files
# - Tag releases used for publications
#
# **5. Test your workflows**
# - Create test datasets (small, fast)
# - Verify outputs are correct
# - Test error handling
#
# **6. Document for reproducibility**
# - Include README with clear instructions
# - Specify software versions
# - Provide example run commands
# - Explain expected outputs

# %% [markdown]
# ### Integrating Workflows with Other Tools
#
# **Version Control (Git)**
# ```
# research_project/
# ├── Snakefile          # Workflow definition
# ├── config.yaml        # Configuration
# ├── envs/              # Conda environments
# │   ├── analysis.yaml
# │   └── plotting.yaml
# ├── scripts/           # Analysis scripts
# │   ├── download.py
# │   ├── process.py
# │   └── plot.py
# ├── README.md          # Documentation
# └── .gitignore         # Ignore data/, results/
# ```
#
# **.gitignore for workflows:**
# ```
# # Ignore data and results (usually too large)
# data/
# results/
#
# # But track workflow components
# !Snakefile
# !config.yaml
# !scripts/
# !envs/
#
# # Snakemake working directories
# .snakemake/
# ```

# %% [markdown]
# **Containers (from Lecture 9)**
# - Use containers for each workflow step
# - Ensures consistent environment
# - Snakemake/Nextflow have built-in container support
#
# **CI/CD (from Lecture 6)**
# - Test workflows on small datasets in CI
# - Verify workflows execute without errors
# - Catch breaking changes early
#
# **Example GitHub Actions workflow for testing:**
# ```yaml
# name: Test Workflow
#
# on: [push, pull_request]
#
# jobs:
#   test:
#     runs-on: ubuntu-latest
#     steps:
#       - uses: actions/checkout@v2
#       - uses: conda-incubator/setup-miniconda@v2
#         with:
#           activate-environment: workflow-env
#           environment-file: environment.yml
#       - name: Install Snakemake
#         run: conda install -c bioconda snakemake
#       - name: Run workflow on test data
#         run: snakemake --cores 2 --use-conda
# ```

# %% [markdown]
# **Data Management (from Lecture 11)**
# - Workflows consume and produce data
# - Apply FAIR principles to workflow outputs
# - Use appropriate file formats (HDF5, NetCDF)
# - Include metadata in outputs

# %% [markdown]
# ## Part 7: Workflows in Different Languages
#
# The concepts we've discussed apply regardless of programming language.

# %% [markdown]
# ### R-based Workflows
#
# **Using targets (R's workflow package):**
# ```r
# # _targets.R
# library(targets)
#
# tar_option_set(packages = c("tidyverse", "arrow"))
#
# list(
#   tar_target(raw_data, read_csv("data/raw.csv")),
#   tar_target(clean_data, clean(raw_data)),
#   tar_target(model, fit_model(clean_data)),
#   tar_target(plot, create_plot(model))
# )
# ```
#
# **Running:**
# ```r
# targets::tar_make()        # Run workflow
# targets::tar_visnetwork()  # Visualize
# ```
#
# **Snakemake with R:**
# ```python
# rule analyze_with_r:
#     input:
#         "data/input.csv"
#     output:
#         "results/output.png"
#     script:
#         "scripts/analyze.R"
# ```

# %% [markdown]
# ### Julia-based Workflows
#
# Julia can be integrated into Make or Snakemake:
#
# **Makefile:**
# ```makefile
# results/output.txt: data/input.txt
#     julia scripts/process.jl $< $@
# ```
#
# **Snakefile:**
# ```python
# rule julia_analysis:
#     input:
#         "data/input.txt"
#     output:
#         "results/output.txt"
#     shell:
#         "julia scripts/process.jl {input} {output}"
# ```

# %% [markdown]
# ### Mixed-Language Workflows
#
# Real research often combines multiple languages:
#
# ```python
# # Snakefile with Python, R, and Julia
#
# rule download_with_python:
#     output:
#         "data/raw.csv"
#     shell:
#         "python scripts/download.py {output}"
#
# rule analyze_with_r:
#     input:
#         "data/raw.csv"
#     output:
#         "data/analyzed.rds"
#     script:
#         "scripts/analyze.R"
#
# rule optimize_with_julia:
#     input:
#         "data/analyzed.rds"
#     output:
#         "results/optimized.csv"
#     shell:
#         "julia scripts/optimize.jl {input} {output}"
#
# rule visualize_with_python:
#     input:
#         "results/optimized.csv"
#     output:
#         "figures/plot.png"
#     conda:
#         "envs/plotting.yaml"
#     shell:
#         "python scripts/plot.py {input} {output}"
# ```

# %% [markdown]
# ## Part 8: Real-World Example - Complete Climate Analysis Pipeline
#
# Let's put it all together with a complete, realistic example that demonstrates
# best practices.

# %% [markdown]
# ### Project Structure
# ```
# climate_analysis/
# ├── Snakefile                 # Main workflow
# ├── config.yaml               # Configuration
# ├── README.md                 # Documentation
# ├── environment.yml           # Main environment
# ├── envs/                     # Rule-specific environments
# │   ├── download.yaml
# │   ├── analysis.yaml
# │   └── plotting.yaml
# ├── scripts/                  # Analysis scripts
# │   ├── download_data.py
# │   ├── quality_control.py
# │   ├── merge_datasets.py
# │   ├── compute_trends.py
# │   ├── generate_plots.py
# │   └── create_report.py
# ├── data/                     # Data (in .gitignore)
# │   ├── raw/
# │   ├── processed/
# │   └── metadata/
# ├── results/                  # Results (in .gitignore)
# │   ├── figures/
# │   ├── tables/
# │   └── reports/
# └── tests/                    # Test data and scripts
#     ├── test_data/
#     └── test_workflow.sh
# ```

# %%
# Example: Simulating a simple workflow execution
import os
import json
from datetime import datetime


def simulate_workflow_execution():
    """
    Demonstrates workflow concepts without requiring actual data files.
    Shows dependency tracking and execution order.
    """

    # Define workflow structure as a dictionary
    workflow = {
        "download_data": {
            "inputs": [],
            "outputs": ["data/raw/temperature.csv"],
            "command": "download_data.py",
            "status": "pending",
        },
        "clean_data": {
            "inputs": ["data/raw/temperature.csv"],
            "outputs": ["data/processed/temperature_clean.csv"],
            "command": "clean_data.py",
            "status": "pending",
        },
        "plot_data": {
            "inputs": ["data/processed/temperature_clean.csv"],
            "outputs": ["results/plots.png"],
            "command": "plot_data.py",
            "status": "pending",
        },
        "compute_stats": {
            "inputs": ["data/processed/temperature_clean.csv"],
            "outputs": ["results/statistics.txt"],
            "command": "compute_stats.py",
            "status": "pending",
        },
        "generate_report": {
            "inputs": ["results/plots.png", "results/statistics.txt"],
            "outputs": ["report.pdf"],
            "command": "generate_report.py",
            "status": "pending",
        },
    }

    print("Workflow Dependency Graph")
    print("=" * 60)

    # Build and display dependency graph
    for step, details in workflow.items():
        print(f"\n{step}:")
        if details["inputs"]:
            print(f"  Depends on: {', '.join(details['inputs'])}")
        else:
            print(f"  Depends on: (no dependencies - can start immediately)")
        print(f"  Produces: {', '.join(details['outputs'])}")
        print(f"  Command: {details['command']}")

    print("\n" + "=" * 60)
    print("\nExecution Order (respecting dependencies):")
    print("-" * 60)

    # Simulate execution order
    execution_order = ["download_data", "clean_data", "plot_data (parallel)", "compute_stats (parallel)", "generate_report"]

    for i, step in enumerate(execution_order, 1):
        print(f"{i}. {step}")

    print("\n" + "=" * 60)
    print("\nWorkflow Metadata:")
    print("-" * 60)

    metadata = {
        "workflow_name": "temperature_analysis",
        "total_steps": len(workflow),
        "parallel_capable_steps": ["plot_data", "compute_stats"],
        "created": datetime.now().isoformat(),
        "version": "1.0.0",
    }

    print(json.dumps(metadata, indent=2))

    return workflow, metadata


# Execute the simulation
workflow_def, metadata = simulate_workflow_execution()

# %% [markdown]
# ### Configuration File (config.yaml)
#
# ```yaml
# # Configuration for climate analysis workflow
#
# # Data sources
# data_sources:
#   - name: "nasa"
#     url: "https://data.nasa.gov/api/climate/temperature"
#     format: "netcdf"
#   - name: "noaa"
#     url: "https://www.noaa.gov/api/climate/temp"
#     format: "csv"
#
# # Analysis parameters
# analysis:
#   start_year: 1980
#   end_year: 2023
#   variables: ["temperature", "precipitation"]
#   quality_threshold: 0.95
#
# # Computational resources
# resources:
#   download_threads: 2
#   analysis_threads: 8
#   memory_gb: 16
#
# # Output settings
# output:
#   figure_format: "png"
#   figure_dpi: 300
#   report_format: "pdf"
# ```

# %% [markdown]
# ### Key Takeaways
#
# **When to use workflows:**
# - Pipeline has >3 steps
# - Steps have complex dependencies
# - Analysis runs repeatedly
# - Need to rerun parts after changes
# - Multiple people collaborate
# - Results must be reproducible
#
# **Start simple, scale up:**
# 1. Begin with shell scripts
# 2. Move to Make for dependency tracking
# 3. Adopt Snakemake/Nextflow for complex projects
# 4. Consider specialized tools for production
#
# **Workflow antipatterns to avoid:**
# - Hardcoded file paths
# - Undocumented parameters
# - No version control
# - Missing intermediate files
# - Unclear execution order
# - No testing on small datasets

# %% [markdown]
# ## Summary and Conclusion
#
# Scientific workflows and automation are essential for:
# - **Reproducibility**: Others can reproduce your analysis
# - **Efficiency**: Don't rerun unnecessary steps
# - **Scalability**: Handle larger datasets and more complex analyses
# - **Collaboration**: Clear, documented pipelines
# - **Error reduction**: Automated execution prevents manual mistakes
#
# **Key concepts:**
# - **Dependency tracking**: Automatically determine what to run
# - **Parallelization**: Run independent tasks simultaneously
# - **Modularity**: Break analysis into reusable steps
# - **Configuration**: Separate parameters from code
# - **Integration**: Combine with version control, containers, and CI/CD
#
# **Tool selection:**
# - **Simple pipelines**: Shell scripts or Make
# - **Python-based research**: Snakemake
# - **Cloud/genomics**: Nextflow
# - **Maximum portability**: CWL
# - **Teaching/non-programmers**: Galaxy
# - **Production data engineering**: Airflow
#
# **Next steps:**
# - Start with Make for your next analysis
# - Try Snakemake for a complex project
# - Explore alternatives for your specific domain
# - Integrate workflows into your reproducibility stack
# - Share your workflows with publications
#
# Workflows transform research from a series of manual steps into a reproducible,
# automated pipeline. As Elena learned, the time invested in creating a workflow
# pays off immediately and grows more valuable over time.

# %% [markdown]
# ### What's Next?
#
# In **Lecture 13**, we'll bring together the software architecture and design threads that have
# been running through this course. You'll learn:
# - Applying DRY, Single Responsibility, and Separation of Concerns to keep research code
#   maintainable
# - Recognizing code smells that signal design problems before they become bugs
# - Deciding when to refactor versus rewrite, and how to refactor safely
# - Reviewing pull requests for architectural quality, not just correctness
#
# The workflows you just built are exactly the kind of code that benefits most from good
# design—pipelines grow, get reused, and get modified by other people. Clean design keeps
# them maintainable as they do.
#
# **Ready to continue? Move on to Lecture 13: Software Architecture and Design for Research
# Software!**

# %% [markdown]
# ## Additional Resources
#
# **Documentation:**
# - GNU Make Manual: https://www.gnu.org/software/make/manual/
# - Snakemake Documentation: https://snakemake.readthedocs.io/
# - Nextflow Documentation: https://www.nextflow.io/docs/latest/
# - CWL User Guide: https://www.commonwl.org/user_guide/
# - Galaxy Training: https://training.galaxyproject.org/
#
# **Tutorials:**
# - Snakemake Tutorial: https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html
# - Nextflow Patterns: https://nextflow-io.github.io/patterns/
#
# **Best Practices:**
# - Wilson, G., et al. (2017). "Good enough practices in scientific computing".
#   *PLOS Computational Biology*, 13(6), e1005510. DOI: 10.1371/journal.pcbi.1005510
#
# **Community:**
# - Snakemake Community: https://snakemake.github.io/
# - Workflow Hub: https://workflowhub.eu/ (repository of scientific workflows)
