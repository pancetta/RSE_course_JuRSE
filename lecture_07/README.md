# Lecture 7: Debugging and Profiling Research Software

This lecture teaches systematic debugging techniques and performance profiling for research software.

## Overview

Learn how to:
- Use Python's debugger (pdb) to find and fix bugs
- Implement effective logging strategies
- Profile code to identify performance bottlenecks
- Optimize research code based on profiling data

## Topics Covered

### Part 1-3: Debugging
- Systematic debugging process
- Python debugger (pdb) basics and commands
- Practical debugging examples

### Part 4: Logging
- Why logging beats print statements
- Python's logging module
- Best practices for logging in research code

### Part 5-9: Profiling
- The golden rule of optimization
- Time profiling with cProfile
- Line-by-line and memory profiling
- Real-world profiling examples

### Part 10-11: Best Practices
- Complete debugging and profiling workflow
- Common research software bugs
- Debugging strategies and tips
- Distinguishing an AI-suggested fix that addresses the root cause from one that just silences
  the error

## Duration

~90 minutes

## Prerequisites

- Completion of Lectures 1-6
- Understanding of Python basics
- Familiarity with testing concepts

## Learning Objectives

By the end of this lecture, you will be able to:
1. Apply systematic approaches to debugging research software
2. Use pdb to inspect and debug running code
3. Implement professional logging in your code
4. Profile code to identify performance bottlenecks
5. Make data-driven optimization decisions
6. Balance code performance with readability and correctness

## Key Tools

- **pdb**: Python's built-in debugger
- **logging**: Python's logging module
- **cProfile**: Built-in time profiler
- **line_profiler**: Line-by-line profiling (optional)
- **memory_profiler**: Memory usage profiling (optional)

## Running the Lecture

Convert to Jupyter notebook and run:

```bash
cd lecture_07
jupytext --to notebook lecture_07.py
jupyter notebook lecture_07.ipynb
```

Or use the conversion script from the repository root:

```bash
python scripts/convert_to_notebooks.py
jupyter notebook lecture_07/lecture_07.ipynb
```

## Additional Resources

- [Python pdb documentation](https://docs.python.org/3/library/pdb.html)
- [Python logging documentation](https://docs.python.org/3/library/logging.html)
- [Python profilers documentation](https://docs.python.org/3/library/profile.html)
- [line_profiler on GitHub](https://github.com/pyutils/line_profiler)
- [memory_profiler on GitHub](https://github.com/pythonprofilers/memory_profiler)

## Notes

This lecture uses only Python's standard library for core concepts (pdb, logging, cProfile). Optional advanced tools like line_profiler and memory_profiler are mentioned but not required.

All examples use realistic climate data analysis scenarios to demonstrate debugging and profiling in research contexts.
