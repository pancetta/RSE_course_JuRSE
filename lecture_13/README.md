# Lecture 13: Software Architecture and Design for Research Software

## Overview
This lecture is about the code-level design decisions that determine whether research software
stays maintainable as it grows — how you shape functions and modules, not the large-scale
architecture of distributed systems. It follows a single running example, the StationWatch
weather-station pipeline, through a cautionary tale, the design principles that would have
prevented it, the code smells that would have flagged it, the refactor-vs-rewrite decision once
technical debt has accumulated, and the architectural code review practice that stops it from
recurring.

**Duration**: ~90 minutes

## Topics Covered
- Design principles for maintainable code: DRY, Single Responsibility, Separation of Concerns
- Code smells: god functions, duplicated code, magic numbers, tight coupling, global state
- Why hard-to-test code is usually a symptom of a design problem
- Deciding when to refactor versus rewrite, using a practical risk-based framework
- Refactoring incrementally and safely, guided by tests
- Technical debt as a deliberate, sometimes-acceptable trade-off
- Reviewing pull requests for architectural quality, not just correctness
- Giving constructive, prioritized design feedback in code review

## Key Concepts
- **DRY (Don't Repeat Yourself)**: Write logic once, reuse it everywhere
- **Single Responsibility Principle**: Each function or module should do one thing well
- **Separation of Concerns**: Keep data access, computation, and presentation apart
- **Code smell**: A sign of a design problem, not necessarily a bug
- **Technical debt**: The cost of a quick solution now that requires more work later
- **Refactoring**: Improving code structure without changing behavior, in small, tested steps
- **Architectural code review**: Reviewing a PR for maintainability and design, not just
  correctness

## Prerequisites

Before starting this lecture, you should be familiar with:
- Python functions, classes, and modules (Lectures 2 and 4)
- Writing and running tests with pytest, and what makes code "testable" (Lecture 5)
- Reading a git diff and participating in pull request review (Lecture 10)
- AI-assisted coding basics, including reviewing AI suggestions like a diff (Lecture 3)

## Learning Objectives
- Apply DRY, Single Responsibility, and Separation of Concerns to keep research code
  maintainable as it grows
- Recognize common code smells and explain why they make code hard to test
- Decide when to refactor versus rewrite using a practical, risk-based framework
- Refactor incrementally, using tests to keep each step safe
- Review a pull request for architectural quality and give constructive design feedback
- Recognize when the same design problem is recurring across multiple pull requests

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

## The StationWatch Story
The lecture opens with a cautionary tale about a weather-station analysis pipeline whose pull
requests all "worked perfectly"—correct, reviewed, and merged—until tightly coupled, duplicated
code turned a three-day feature into a three-week untangling. The rest of the lecture follows
that same project through the principles, smells, decisions, and review practices that would
have kept it maintainable.

## Practical Guidance
The lecture provides:
- Runnable code examples for each design principle and code smell
- A profiling-driven refactoring case study, taken step by step
- An architectural code review checklist you can apply to your own pull requests
- Try It Yourself exercises for refactoring, spotting smells, and reviewing for design
