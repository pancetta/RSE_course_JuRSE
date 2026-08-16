# Lecture 10: Collaboration and Code Review in Research Software

## Overview
This lecture explores how to work effectively in research software teams, from code reviews and pull requests to onboarding new collaborators. Research is increasingly collaborative, and your software needs to support multiple contributors while maintaining quality and reproducibility. You'll learn practical workflows for team collaboration, effective code review practices, and how to build a welcoming community around your research software.

**Duration**: ~90 minutes

## Topics Covered
- Why collaboration requires deliberate processes and practices
- The pull request workflow for collaborative development
- Conducting effective and constructive code reviews
- Handling merge conflicts and coordinating with team members
- Onboarding new contributors to research projects
- Collaboration practices across different version control platforms
- Team dynamics and communication challenges
- Adapting collaboration practices for different programming languages
- Reviewing AI-assisted and agentic pull requests, including attribution norms for AI-authored
  commits

## Key Concepts
- **Pull Requests (PRs)**: Formal requests to merge changes with built-in review processes
- **Code Review**: Systematic examination of code before merging
- **Branch-based workflow**: Using feature branches instead of direct commits to main
- **Merge conflicts**: When multiple changes affect the same code, requiring manual resolution
- **Onboarding**: Process of helping new contributors become productive
- **Communication protocols**: Clear expectations and feedback mechanisms

## Prerequisites

Before starting this lecture, you should be familiar with:
- Git branching and merging (covered in Lecture 2)
- GitHub/GitLab basics including pull/merge requests
- Writing and testing Python code (covered in Lectures 2-5)
- Code review concepts from earlier lectures

This lecture builds on your Git knowledge and introduces systematic collaboration practices.

## Learning Objectives
- Understand why collaboration requires deliberate processes and practices
- Master the pull request workflow for collaborative development
- Conduct effective and constructive code reviews
- Handle merge conflicts and coordinate with team members
- Onboard new contributors to research projects
- Apply collaboration practices across different version control platforms
- Navigate team dynamics and communication challenges
- Adapt collaboration practices for different programming languages

## Files
- `lecture_10.py` - Main lecture content in Jupytext format

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
cd lecture_10
jupytext --to notebook lecture_10.py
jupyter notebook lecture_10.ipynb
```

Or from the main repository directory:
```bash
make convert
jupyter notebook
```

## The Cautionary Tale
The lecture opens with a realistic story of a research lab that struggled with collaboration until they adopted systematic processes. This demonstrates why good practices matter even in small teams.

## Practical Examples
The lecture includes:
- Complete pull request workflows for GitHub and GitLab
- Code review checklists and templates
- Merge conflict resolution examples
- Communication guidelines for distributed teams
- Onboarding documentation templates
