# Lecture 3: AI-Assisted Coding Foundations

## Overview
This lecture is a foundations-only introduction to AI-assisted coding: what these tools
actually do, the one habit that keeps you safe while using them, and the most common ways
they go wrong. It deliberately stays narrow—deeper AI topics return in context throughout the
rest of the course (testing in Lecture 5, debugging in Lecture 7, code review in Lecture 10,
and legal/ethical/data-protection questions in Lecture 14).

**Duration**: ~90 minutes

## Topics Covered
- A cautionary tale: AI generates plausible code, not necessarily correct code
- Three categories of AI coding tools: autocomplete-style, chat-style, agentic
- How these tools actually work (and why they don't "understand" your code)
- Effective prompting: turning silent assumptions into visible, checkable decisions
- The core habit: review every AI suggestion like a diff, verified against a case you can
  check by hand
- Common pitfalls: hallucinated APIs, outdated/insecure patterns, automation bias
- Where AI-assisted workflows come up again later in the course

## Files
- `lecture_03.py` - Main lecture content in Jupytext format

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
cd lecture_03
jupytext --to notebook lecture_03.py
jupyter notebook lecture_03.ipynb
```

Or from the main repository directory:
```bash
make convert
jupyter notebook
```

## A Note on Tool Names
This lecture deliberately avoids anchoring its teaching to specific AI products—the
"Tools Landscape" box in Part 2 lists current examples, but the categories (not the brands)
are what matter, since this landscape changes faster than any other topic in the course.
