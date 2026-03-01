# Lecture 13: AI-Assisted Coding for Research Software

## Overview
Artificial Intelligence coding assistants have rapidly become widespread tools in software development, offering to help write, debug, and document code. For research software engineers, these tools present both exciting opportunities and serious risks. This lecture explores how to use AI coding assistants effectively and safely, understanding their capabilities and limitations, and navigating the legal and ethical considerations specific to research software.

**Duration**: ~90 minutes

## Topics Covered
- What AI coding assistants are and how they work
- Comparing different types of AI assistance (integrated vs chat-based)
- Using GitHub Copilot and ChatGPT effectively for research coding
- Recognizing common pitfalls and security risks
- Navigating legal implications (licensing, copyright, data protection)
- Understanding self-hosted options for sensitive research code
- Applying best practices for AI-assisted research software development

## Key Concepts
- **AI coding assistants**: Tools that suggest or generate code using machine learning
- **GitHub Copilot**: Integrated AI assistant in code editors
- **ChatGPT/Claude**: Chat-based AI for code generation and debugging
- **Licensing concerns**: AI-generated code may have unclear copyright
- **Security risks**: AI suggestions may contain vulnerabilities or bugs
- **Self-hosted models**: Running AI assistants on your own infrastructure
- **Verification**: Always understanding and testing AI-generated code

## Prerequisites

Before starting this lecture, you should be familiar with:
- Python programming (covered in Lectures 2-4)
- Writing functions and classes
- Basic software development practices
- All previous RSE concepts (testing, documentation, version control)

This lecture assumes you're comfortable writing code and introduces AI tools to enhance your workflow.

## Learning Objectives
- Understand what AI coding assistants are and how they work
- Compare different types of AI assistance (integrated vs chat-based)
- Use GitHub Copilot and ChatGPT effectively for research coding
- Recognize common pitfalls and security risks
- Navigate legal implications (licensing, copyright, data protection)
- Understand self-hosted options for sensitive research code
- Apply best practices for AI-assisted research software development

## Files
- `lecture_13.py` - Main lecture content in Jupytext format

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
cd lecture_13
jupytext --to notebook lecture_13.py
jupyter notebook lecture_13.ipynb
```

Or from the main repository directory:
```bash
make convert
jupyter notebook
```

## The Copy-Paste Catastrophe
The lecture opens with a cautionary tale about a researcher who blindly trusted AI-generated code, leading to incorrect scientific results. This demonstrates the critical importance of understanding and verifying AI suggestions.

## Practical Guidance
The lecture provides:
- Hands-on examples of effective AI assistant use
- Common failure modes and how to avoid them
- Legal and ethical frameworks for AI in research
- Evaluation criteria for AI-generated code
- Self-hosted alternatives for sensitive projects
- Integration with existing RSE practices (testing, review)
