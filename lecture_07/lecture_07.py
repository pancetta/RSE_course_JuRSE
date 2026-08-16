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
# # Lecture 7: Debugging and Profiling Research Software
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
#     <img src="lecture_07_qr_code.png" alt="This Lecture QR Code" width="150"/>
#     <p><strong>This Lecture</strong></p>
#   </div>
# </div>
#
# ## Overview
# This lecture teaches you how to systematically find and fix bugs in research software,
# and how to identify performance bottlenecks. We'll explore Python's debugging tools
# and profiling techniques that help you write faster, more reliable research code.
#
# **Duration**: ~90 minutes
#
# ## Prerequisites
#
# Before starting this lecture, you should be familiar with:
# - Python functions and error handling (covered in Lecture 2)
# - Writing and running tests with pytest (covered in Lecture 5)
# - Basic command-line usage
# - Scientific computing with NumPy (covered in Lecture 4)
# - AI-assisted coding basics, including reviewing AI suggestions like a diff (covered in
#   Lecture 3)
#
# This lecture introduces debugging and profiling tools that work with the code you've been writing.
#
# ## Learning Objectives
# - Understand systematic approaches to debugging
# - Use Python's debugger (pdb) to inspect running code
# - Apply effective logging strategies for research software
# - Profile code to identify performance bottlenecks
# - Optimize research code based on profiling data
# - Make informed decisions about when and where to optimize
# - Distinguish an AI-suggested fix that addresses the root cause from one that just silences
#   the error

# %% [markdown]
# ## Part 1: The Art of Debugging
#
# ### A New Research Challenge
#
# Dr. Martinez is analyzing climate model output containing millions of temperature readings.
# Her analysis script runs successfully on test data, but crashes mysteriously when processing
# the full dataset. The error message is cryptic, and the bug only appears after 30 minutes
# of computation. Print statements aren't helping - there are too many to track.
#
# She needs systematic debugging tools.
#
# ### What is Debugging?
#
# **Debugging** is the process of finding and fixing errors (bugs) in software. Unlike testing,
# which verifies that code works correctly, debugging helps you understand **why** code fails
# and **how** to fix it.
#
# **Common debugging approaches (from least to most effective):**
#
# 1. **Hope and pray** - Run the code again, maybe it'll work 🤞 (Don't do this!)
# 2. **Print debugging** - Add `print()` statements everywhere
# 3. **Binary search** - Comment out half the code to locate the problem
# 4. **Rubber duck debugging** - Explain the code to an inanimate object
# 5. **Interactive debugging** - Use a debugger to step through code ⭐
# 6. **Logging** - Structured output that persists across runs ⭐
#
# Today we focus on interactive debugging and logging - the professional approaches.

# %% [markdown]
# ## Part 2: The Scientific Method for Debugging
#
# ### Systematic Debugging Process
#
# Debugging is like scientific investigation. Follow these steps:
#
# **1. Reproduce the bug**
# - Can you make it happen reliably?
# - What are the minimal steps to trigger it?
# - Does it happen with smaller data?
#
# **2. Isolate the problem**
# - Which function or module causes it?
# - What input triggers it?
# - When does the state become invalid?
#
# **3. Form a hypothesis**
# - What do you think is wrong?
# - What evidence supports this?
# - How can you test it?
#
# **4. Test your hypothesis**
# - Use the debugger to check your assumptions
# - Add assertions to verify state
# - Try a fix in isolation
#
# **5. Fix and verify**
# - Implement the fix
# - Write a test to prevent regression
# - Verify the bug is actually fixed
#
# <img src="figures/debugging_cycle.svg" alt="Cyclic flowchart of the debugging process: reproduce, isolate, hypothesize, test, fix and verify, then repeat" width="600"/>
#
# Let's see this process in action.

# %% [markdown]
# ## Part 3: Introduction to Python's Debugger (pdb)
#
# ### What is pdb?
#
# **pdb** (Python Debugger) is Python's built-in interactive debugger. It lets you:
# - Pause execution at any point
# - Inspect variable values
# - Step through code line by line
# - Execute Python commands in the current context
# - Set conditional breakpoints
#
# **Think of it as:**
# - A microscope for your code
# - A time machine (step forward/backward)
# - An X-ray machine (see inside running code)
#
# ### A Buggy Research Function
#
# Let's create a function that analyzes temperature anomalies but has a subtle bug:


# %%
def calculate_anomalies(temperatures, baseline):
    """
    Calculate temperature anomalies relative to a baseline.

    Parameters
    ----------
    temperatures : list
        Temperature readings in Celsius
    baseline : float
        Baseline temperature for comparison

    Returns
    -------
    dict
        Statistics about the anomalies
    """
    anomalies = []

    for temp in temperatures:
        anomaly = temp - baseline
        anomalies.append(anomaly)

    # Calculate statistics
    mean_anomaly = sum(anomalies) / len(anomalies)
    max_anomaly = max(anomalies)
    min_anomaly = min(anomalies)

    # BUG: This calculation is wrong when there are negative anomalies
    anomaly_range = max_anomaly - min_anomaly
    positive_anomalies = [a for a in anomalies if a > 0]
    fraction_positive = len(positive_anomalies) / len(anomalies)

    return {
        "mean": mean_anomaly,
        "max": max_anomaly,
        "min": min_anomaly,
        "range": anomaly_range,
        "positive_fraction": fraction_positive,
    }


# Test with sample data
temps = [15.2, 16.8, 14.5, 17.3, 15.9, 16.1]
baseline_temp = 16.0

result = calculate_anomalies(temps, baseline_temp)
print("Temperature Anomaly Analysis:")
print(f"  Mean anomaly: {result['mean']:.2f}°C")
print(f"  Range: {result['range']:.2f}°C")
print(f"  Fraction above baseline: {result['positive_fraction']:.1%}")

# %% [markdown]
# The code runs without errors, but let's verify the results are correct.
#
# **Manual verification:**
# - Temperatures: [15.2, 16.8, 14.5, 17.3, 15.9, 16.1]
# - Baseline: 16.0
# - Anomalies: [-0.8, 0.8, -1.5, 1.3, -0.1, 0.1]
# - Mean: (-0.8 + 0.8 - 1.5 + 1.3 - 0.1 + 0.1) / 6 = -0.2 / 6 ≈ -0.033°C ✓
# - Min: -1.5, Max: 1.3, Range: 2.8°C ✓
# - Positive: [0.8, 1.3, 0.1] = 3 out of 6 = 50% ✓
#
# The function actually works correctly! But what if we had a more complex case?

# %% [markdown]
# ### Using pdb Interactively
#
# There are several ways to start the debugger:
#
# **Method 1: Insert a breakpoint in code**
# ```python
# import pdb
#
# def my_function(data):
#     result = process(data)
#     pdb.set_trace()  # Execution will pause here
#     return result
# ```
#
# **Method 2: Python 3.7+ breakpoint() function**
# ```python
# def my_function(data):
#     result = process(data)
#     breakpoint()  # Modern way - same as pdb.set_trace()
#     return result
# ```
#
# **Method 3: Post-mortem debugging (after a crash)**
# ```python
# import pdb
#
# try:
#     buggy_function()
# except:
#     pdb.post_mortem()  # Start debugger at the crash point
# ```
#
# **Method 4: Run script under debugger**
# ```bash
# python -m pdb my_script.py
# ```

# %% [markdown]
# ### Common pdb Commands
#
# Once in the debugger, you can use these commands:
#
# **Navigation:**
# - `n` (next) - Execute the current line and move to the next
# - `s` (step) - Step into a function call
# - `r` (return) - Continue until the current function returns
# - `c` (continue) - Continue execution until next breakpoint
# - `l` (list) - Show source code around current line
# - `ll` (longlist) - Show source code for entire function
#
# **Inspection:**
# - `p variable` - Print value of a variable
# - `pp variable` - Pretty-print value of a variable
# - `type(variable)` - Check variable type
# - `dir()` - List all variables in current scope
# - `args` - Print arguments of current function
#
# **Breakpoints:**
# - `b line_number` - Set breakpoint at line
# - `b function_name` - Set breakpoint at function
# - `b` - List all breakpoints
# - `cl` - Clear all breakpoints
#
# **Execution:**
# - `q` (quit) - Exit the debugger
# - `h` (help) - Show help message
# - `h command` - Help for specific command

# %% [markdown]
# ### Debugging Example: Finding a Subtle Bug
#
# Let's examine a more complex case where pdb would be invaluable.
# This function processes climate model data, but has a bug that only appears
# with certain input patterns:


# %%
def analyze_temperature_trends(daily_temps, window_size=7):
    """
    Analyze temperature trends using a moving average.

    Parameters
    ----------
    daily_temps : list
        Daily temperature readings
    window_size : int
        Number of days for moving average

    Returns
    -------
    dict
        Trend analysis results
    """
    if len(daily_temps) < window_size:
        raise ValueError(f"Need at least {window_size} days of data")

    # Calculate moving averages
    moving_averages = []
    for i in range(len(daily_temps) - window_size + 1):
        window = daily_temps[i : i + window_size]
        avg = sum(window) / window_size
        moving_averages.append(avg)

    # Calculate trend (slope of moving averages)
    # BUG: This fails when moving_averages has only 1 element
    n = len(moving_averages)
    if n < 2:
        return {"trend": 0.0, "moving_avg": moving_averages[0]}

    # Simple linear regression slope
    x_mean = (n - 1) / 2.0
    y_mean = sum(moving_averages) / n

    numerator = sum((i - x_mean) * (y - y_mean) for i, y in enumerate(moving_averages))
    denominator = sum((i - x_mean) ** 2 for i in range(n))

    trend = numerator / denominator if denominator != 0 else 0.0

    return {"trend": trend, "moving_avg_start": moving_averages[0], "moving_avg_end": moving_averages[-1], "data_points": n}


# Test with different datasets
print("Case 1: Normal dataset (30 days)")
temps_normal = [20 + i * 0.1 for i in range(30)]
result1 = analyze_temperature_trends(temps_normal, window_size=7)
print(f"  Trend: {result1['trend']:.4f}°C/day")

print("\nCase 2: Minimal dataset (exactly window_size)")
temps_minimal = [20, 21, 22, 23, 24, 25, 26]
result2 = analyze_temperature_trends(temps_minimal, window_size=7)
print(f"  Trend: {result2['trend']:.4f}°C/day")

print("\nCase 3: Just above minimal (window_size + 1)")
temps_edge = [20, 21, 22, 23, 24, 25, 26, 27]
result3 = analyze_temperature_trends(temps_edge, window_size=7)
print(f"  Trend: {result3['trend']:.4f}°C/day")

# %% [markdown]
# ### How pdb Would Help Debug This
#
# If this function had a bug (which it doesn't in this version), here's how you'd debug it:
#
# **Debugging session (conceptual):**
# ```python
# # Add breakpoint before the suspicious calculation
# def analyze_temperature_trends(daily_temps, window_size=7):
#     # ... earlier code ...
#
#     breakpoint()  # Pause here
#
#     # Calculate trend
#     n = len(moving_averages)
#     # ...
# ```
#
# **In the debugger:**
# ```
# (Pdb) p moving_averages
# [23.0]  # Only one element!
#
# (Pdb) p len(moving_averages)
# 1
#
# (Pdb) p window_size
# 7
#
# (Pdb) p len(daily_temps)
# 7  # Exactly equal to window_size
#
# (Pdb) # Aha! When len(daily_temps) == window_size, we get only 1 moving average
# (Pdb) # That's why n < 2, so we return early - working as designed!
# ```
#
# **Key insight from debugging:**
# - pdb lets you inspect the actual data values
# - You can see exactly what state your program is in
# - You can test hypotheses interactively
# - You can execute code to see what would happen

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Master pdb and become a debugging wizard—interactive debugging changes everything!</p>
#     <ul>
#         <li><strong>Debug a real bug:</strong> Intentionally introduce a subtle bug in
#         your code (off-by-one error, wrong variable, incorrect condition) and use pdb to
#         hunt it down—practice stepping, inspecting variables, and testing hypotheses.</li>
#         <li><strong>Explore unfamiliar code:</strong> Use pdb to step through a library
#         function you don't understand—see exactly how it processes your data and what
#         intermediate values look like.</li>
#         <li><strong>Set conditional breakpoints:</strong> Use pdb.set_trace() with an if
#         statement to break only when specific conditions occur (like when a variable
#         exceeds a threshold)—debug rare edge cases efficiently.</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 4: Logging for Research Software
#
# ### Why Logging Beats Print Statements
#
# **Problems with print() debugging:**
# - Output mixed with legitimate program output
# - Hard to turn on/off selectively
# - No timestamp or context
# - Lost when program finishes
# - Not suitable for production code
# - Can't filter by importance
#
# **Advantages of proper logging:**
# - Separate log files from output
# - Different levels (DEBUG, INFO, WARNING, ERROR)
# - Timestamps and context automatically
# - Can log to multiple destinations
# - Enable/disable without code changes
# - Production-ready
# - Can filter and search logs
#
# ### Python's logging Module
#
# Python's built-in `logging` module provides professional logging capabilities:

# %%
import logging

# Configure logging (do this once at program start)
logging.basicConfig(
    level=logging.INFO,  # Set minimum level to log
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create a logger for this module
logger = logging.getLogger(__name__)

# Demonstrate different log levels
logger.debug("This is a DEBUG message - very detailed info")
logger.info("This is an INFO message - general information")
logger.warning("This is a WARNING message - something unexpected")
logger.error("This is an ERROR message - something failed")
logger.critical("This is a CRITICAL message - serious problem")

# %% [markdown]
# ### Log Levels Explained
#
# **DEBUG (10)**: Detailed diagnostic information
# - Variable values, loop iterations, intermediate calculations
# - Only needed when diagnosing problems
# - Example: "Processing data point 1523 of 10000"
#
# **INFO (20)**: General informational messages
# - Confirm things are working as expected
# - Major steps in processing
# - Example: "Starting temperature analysis for dataset: arctic_2023"
#
# **WARNING (30)**: Warning about potential issues
# - Something unexpected but not fatal
# - Deprecated features, missing optional data
# - Example: "Missing metadata for 5 stations, using defaults"
#
# **ERROR (40)**: Error occurred, but program continues
# - Part of processing failed
# - Example: "Failed to process file data_corrupt.csv: invalid format"
#
# **CRITICAL (50)**: Serious error, program may crash
# - Fatal errors
# - Example: "Out of memory, cannot continue analysis"
#
# **Key principle:** Only messages at or above the configured level are shown.

# %% [markdown]
# ### Logging in Research Code - Practical Example
#
# Let's add proper logging to our temperature analysis function:

# %%
import logging

# Configure logger for this example
logger = logging.getLogger("climate_analysis")
logger.setLevel(logging.DEBUG)

# Create console handler with formatting
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def process_climate_data(station_data, quality_threshold=0.8):
    """
    Process climate station data with comprehensive logging.

    Parameters
    ----------
    station_data : dict
        Data from climate stations
    quality_threshold : float
        Minimum quality score to accept data

    Returns
    -------
    dict
        Processed results
    """
    logger.info(f"Starting climate data processing for {len(station_data)} stations")

    valid_stations = []
    rejected_stations = []

    for station_id, data in station_data.items():
        logger.debug(f"Processing station {station_id}")

        # Check data quality
        if "quality" not in data:
            logger.warning(f"Station {station_id} missing quality metadata, assuming 1.0")
            data["quality"] = 1.0

        if data["quality"] < quality_threshold:
            logger.warning(
                f"Station {station_id} rejected: quality {data['quality']:.2f} " f"below threshold {quality_threshold:.2f}"
            )
            rejected_stations.append(station_id)
            continue

        # Check for missing data
        if "temperatures" not in data or len(data["temperatures"]) == 0:
            logger.error(f"Station {station_id} has no temperature data, skipping")
            rejected_stations.append(station_id)
            continue

        valid_stations.append(station_id)
        logger.debug(f"Station {station_id} accepted: {len(data['temperatures'])} readings")

    logger.info(f"Processing complete: {len(valid_stations)} valid, " f"{len(rejected_stations)} rejected")

    if len(valid_stations) == 0:
        logger.critical("No valid stations remaining! Cannot proceed with analysis.")
        raise ValueError("No valid data available for analysis")

    return {
        "valid_stations": valid_stations,
        "rejected_stations": rejected_stations,
        "acceptance_rate": len(valid_stations) / len(station_data),
    }


# Test the logging
test_data = {
    "station_001": {"temperatures": [20, 21, 22], "quality": 0.95},
    "station_002": {"temperatures": [18, 19, 20], "quality": 0.75},  # Will be rejected
    "station_003": {"temperatures": [], "quality": 0.99},  # No data
    "station_004": {"temperatures": [22, 23, 24]},  # Missing quality field
}

result = process_climate_data(test_data, quality_threshold=0.8)
print(f"\nAcceptance rate: {result['acceptance_rate']:.1%}")

# %% [markdown]
# ### Best Practices for Logging in Research
#
# **1. Log at the right level**
# - Use INFO for major milestones: "Started processing", "Completed analysis"
# - Use DEBUG for detailed tracking: variable values, iterations
# - Use WARNING for unexpected but handled situations: missing optional data
# - Use ERROR for failures that don't stop execution: one file failed
# - Use CRITICAL for fatal errors: out of memory, all data invalid
#
# **2. Include context**
# ```python
# logger.info(f"Processing dataset: {dataset_name}, {len(data)} records")
# ```
#
# **3. Log to files for long-running analyses**
# ```python
# file_handler = logging.FileHandler('analysis.log')
# logger.addHandler(file_handler)
# ```
#
# **4. Don't log sensitive data**
# ```python
# # BAD
# logger.info(f"User password: {password}")
#
# # GOOD
# logger.info(f"User authenticated: {username}")
# ```
#
# **5. Use meaningful messages**
# ```python
# # BAD
# logger.info("Done")
#
# # GOOD
# logger.info("Temperature analysis complete: 10000 records processed in 2.5s")
# ```
#
# **6. Balance verbosity**
# - Too little logging: can't diagnose problems
# - Too much logging: drowning in noise, slow performance
# - Find the sweet spot for your use case

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Strategic logging transforms debugging from guesswork to science!</p>
#     <ul>
#         <li><strong>Build a comprehensive logging strategy:</strong> Add structured
#         logging to a research pipeline with DEBUG for detailed flow, INFO for progress,
#         WARNING for questionable data, and ERROR for failures—then run it and observe how
#         visibility improves troubleshooting.</li>
#         <li><strong>Log for reproducibility:</strong> Create logs that record all
#         parameters, random seeds, data versions, and environment details—practice
#         reconstructing a computation from log files alone.</li>
#         <li><strong>Implement performance logging:</strong> Add timing logs for each major
#         step in your pipeline, then analyze the logs to identify which stages are slowest
#         and should be optimized first.</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 5: Performance Profiling
#
# ### Dr. Martinez's Performance Problem
#
# Remember Dr. Martinez from the beginning? Her code now runs without crashing,
# but it's *slow*. Processing a full year of climate data takes 6 hours.
# She needs to run it for 50 years of data - that's 12.5 days!
#
# Before optimizing, she needs to know: **Where is the time being spent?**
#
# ### The Golden Rule of Optimization
#
# **"Premature optimization is the root of all evil."** - Donald Knuth
#
# **Why this matters:**
# 1. **You'll probably guess wrong** where the bottleneck is
# 2. **Optimization makes code complex** - harder to read and maintain
# 3. **Development time is expensive** - don't waste it on wrong targets
# 4. **Correctness first** - broken fast code is still broken
#
# **The right approach:**
# 1. Write clear, correct code first
# 2. Test it thoroughly
# 3. Profile to find actual bottlenecks
# 4. Optimize only the slow parts
# 5. Verify optimization didn't break correctness
# 6. Measure improvement
#
# ### What is Profiling?
#
# **Profiling** measures where your program spends time and resources.
#
# **Types of profiling:**
# - **Time profiling**: Which functions take the most time?
# - **Line profiling**: Which specific lines are slow?
# - **Memory profiling**: Which code uses the most memory?
# - **Call profiling**: How many times is each function called?

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Profiling reveals hidden performance bottlenecks—prepare to be surprised!</p>
#     <ul>
#         <li><strong>Profile your slowest code:</strong> Run cProfile on a computation
#         that takes >10 seconds, identify the top 3 time-consuming functions, and focus
#         optimization efforts there—measure the speedup achieved.</li>
#         <li><strong>Find unexpected hotspots:</strong> Profile code where you think you
#         know what's slow, then look for surprises—often the bottleneck is somewhere
#         unexpected like string formatting, file I/O, or data structure operations.</li>
#         <li><strong>Compare algorithms empirically:</strong> Implement the same
#         calculation two ways (nested loops vs. NumPy, list comprehension vs. generator)
#         and profile both—see concrete evidence of which is faster for your data size.</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 6: Time Profiling with cProfile
#
# ### Python's Built-in Profiler: cProfile
#
# **cProfile** is Python's built-in deterministic profiler. It measures:
# - How many times each function is called
# - How much time each function takes
# - Where time is spent in your program
#
# **Two ways to use cProfile:**

# %% [markdown]
# ### Method 1: Profile from Command Line
#
# ```bash
# python -m cProfile -o profile_output.prof my_script.py
# ```
#
# This saves profiling data to a file for later analysis.
#
# **View the results:**
# ```python
# import pstats
#
# stats = pstats.Stats('profile_output.prof')
# stats.strip_dirs()
# stats.sort_stats('cumulative')
# stats.print_stats(10)  # Show top 10 functions
# ```

# %% [markdown]
# ### Method 2: Profile Specific Code
#
# Profile just the code you care about:

# %%
import cProfile
import pstats
from io import StringIO


def slow_temperature_analysis(temperatures):
    """
    Analyze temperature data (intentionally inefficient version).

    This demonstrates common performance issues in research code.
    """
    results = {}

    # Inefficient: Recalculating mean multiple times
    def calculate_mean(temps):
        return sum(temps) / len(temps) if temps else 0

    # Calculate mean anomalies (inefficient)
    mean_temp = calculate_mean(temperatures)
    anomalies = []
    for temp in temperatures:
        anomaly = temp - mean_temp
        anomalies.append(anomaly)

    # Find extreme values (inefficient - recalculating)
    results["mean"] = calculate_mean(temperatures)
    results["max"] = max(temperatures)
    results["min"] = min(temperatures)

    # Calculate percentiles (very inefficient)
    sorted_temps = sorted(temperatures)
    n = len(sorted_temps)
    results["p25"] = sorted_temps[n // 4]
    results["p50"] = sorted_temps[n // 2]
    results["p75"] = sorted_temps[3 * n // 4]

    # Count days above/below mean (inefficient)
    above_mean = sum(1 for t in temperatures if t > results["mean"])
    results["days_above_mean"] = above_mean

    return results


# Create realistic dataset
import random

random.seed(42)
large_dataset = [20 + random.gauss(0, 5) for _ in range(10000)]

# Profile the function
profiler = cProfile.Profile()
profiler.enable()

result = slow_temperature_analysis(large_dataset)

profiler.disable()

# Print profiling results
s = StringIO()
ps = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
ps.print_stats(10)
print(s.getvalue())

# %% [markdown]
# ### Understanding cProfile Output
#
# The output shows columns:
#
# - **ncalls**: Number of times the function was called
# - **tottime**: Total time in function (excluding subcalls)
# - **percall**: tottime / ncalls
# - **cumtime**: Total time including subcalls
# - **percall**: cumtime / ncalls
# - **filename:lineno(function)**: Where the function is defined
#
# **What to look for:**
# 1. Functions with high `cumtime` - these are the bottlenecks
# 2. Functions called many times - optimization candidates
# 3. Surprising slow functions - investigate why
#
# **In our example:**
# - The `sorted()` calls are expensive
# - We're recalculating things multiple times
# - List comprehensions are faster than loops with append

# %% [markdown]
# ### Optimized Version
#
# Based on profiling, here's an optimized version:


# %%
def fast_temperature_analysis(temperatures):
    """
    Analyze temperature data (optimized version).

    Improvements based on profiling:
    - Calculate mean once, reuse it
    - Sort once for all percentiles
    - Use NumPy if available (would be much faster)
    """
    if not temperatures:
        return {}

    # Sort once, use for multiple purposes
    sorted_temps = sorted(temperatures)
    n = len(sorted_temps)

    # Calculate mean once
    mean_temp = sum(temperatures) / n

    # All calculations in one pass where possible
    results = {
        "mean": mean_temp,
        "max": sorted_temps[-1],  # Last element of sorted list
        "min": sorted_temps[0],  # First element of sorted list
        "p25": sorted_temps[n // 4],
        "p50": sorted_temps[n // 2],
        "p75": sorted_temps[3 * n // 4],
    }

    # Count above mean (more efficient)
    results["days_above_mean"] = sum(1 for t in temperatures if t > mean_temp)

    return results


# Compare performance
import time

# Slow version
start = time.time()
result_slow = slow_temperature_analysis(large_dataset)
time_slow = time.time() - start

# Fast version
start = time.time()
result_fast = fast_temperature_analysis(large_dataset)
time_fast = time.time() - start

print(f"Slow version: {time_slow:.4f} seconds")
print(f"Fast version: {time_fast:.4f} seconds")
print(f"Speedup: {time_slow/time_fast:.2f}x faster")

# Verify results are the same
print(f"\nResults match: {result_slow == result_fast}")

# %% [markdown]
# ## Part 7: Line-by-Line Profiling
#
# ### When You Need More Detail
#
# Sometimes function-level profiling isn't enough. You need to know
# which *specific lines* within a function are slow.
#
# **line_profiler** provides line-by-line timing information.
#
# ### Using line_profiler
#
# **Installation:**
# ```bash
# pip install line_profiler
# ```
#
# **Usage:**
# ```python
# from line_profiler import LineProfiler
#
# def my_function():
#     # ... code ...
#     pass
#
# profiler = LineProfiler()
# profiler.add_function(my_function)
# profiler.enable()
#
# my_function()  # Run the function
#
# profiler.disable()
# profiler.print_stats()
# ```
#
# **Output shows:**
# - Time per line
# - Percentage of total time
# - Number of hits (how many times executed)
#
# **Example output (conceptual):**
# ```
# Line #      Hits         Time  Per Hit   % Time  Line Contents
# ==============================================================
#      5         1        100.0    100.0      1.0      for i in range(1000):
#      6      1000       5000.0      5.0     50.0          result += expensive_call()
#      7      1000       4900.0      4.9     49.0          other_work()
# ```
#
# **Interpretation:**
# Line 6 takes 50% of the time - that's where to optimize!

# %% [markdown]
# ## Part 8: Memory Profiling
#
# ### When Memory is the Bottleneck
#
# Sometimes the problem isn't speed but memory usage. Research data can be huge!
#
# **memory_profiler** tracks memory usage line-by-line.
#
# **Installation:**
# ```bash
# pip install memory_profiler
# ```
#
# **Usage:**
# ```python
# from memory_profiler import profile
#
# @profile  # Decorator to mark function for profiling
# def memory_intensive_function():
#     large_list = [i for i in range(10000000)]
#     large_dict = {i: i**2 for i in range(1000000)}
#     return len(large_list) + len(large_dict)
#
# # Run your script with:
# # python -m memory_profiler my_script.py
# ```
#
# **Output shows:**
# - Memory usage before each line
# - Memory increment for each line
# - Identifies memory leaks and large allocations
#
# ### Memory Optimization Strategies
#
# **1. Use generators instead of lists**
# ```python
# # BAD: Loads entire dataset into memory
# data = [process(line) for line in huge_file]
#
# # GOOD: Processes one item at a time
# data = (process(line) for line in huge_file)
# ```
#
# **2. Use appropriate data structures**
# ```python
# # If you need numerical arrays, use NumPy
# import numpy as np
# array = np.array([1, 2, 3])  # Much more memory-efficient than list
# ```
#
# **3. Delete large objects when done**
# ```python
# large_data = load_huge_dataset()
# process(large_data)
# del large_data  # Free memory immediately
# ```
#
# **4. Use chunking for large files**
# ```python
# # Process file in chunks instead of loading all at once
# for chunk in pd.read_csv('huge_file.csv', chunksize=10000):
#     process(chunk)
# ```

# %% [markdown]
# ## Part 9: Practical Profiling Example
#
# ### Real-World Climate Data Processing
#
# Let's put it all together with a realistic example:

# %%
import time


def load_climate_data(n_stations=100, days_per_station=365):
    """Simulate loading climate data."""
    data = {}
    for station in range(n_stations):
        # Simulate temperature readings
        temps = [20 + i * 0.01 for i in range(days_per_station)]
        data[f"station_{station:03d}"] = temps
    return data


def naive_correlation_analysis(data):
    """
    Calculate correlations between all station pairs (naive approach).

    This is O(n²) in number of stations - very slow for many stations!
    """
    stations = list(data.keys())
    n = len(stations)

    correlations = []
    for i in range(n):
        for j in range(i + 1, n):
            # Simple correlation: do temperatures trend together?
            temps_i = data[stations[i]]
            temps_j = data[stations[j]]

            # Very naive correlation calculation
            mean_i = sum(temps_i) / len(temps_i)
            mean_j = sum(temps_j) / len(temps_j)

            cov = sum((temps_i[k] - mean_i) * (temps_j[k] - mean_j) for k in range(len(temps_i)))

            var_i = sum((t - mean_i) ** 2 for t in temps_i)
            var_j = sum((t - mean_j) ** 2 for t in temps_j)

            if var_i > 0 and var_j > 0:
                corr = cov / (var_i * var_j) ** 0.5
                correlations.append((stations[i], stations[j], corr))

    return correlations


# Test with smaller dataset
print("Profiling correlation analysis...")
test_data = load_climate_data(n_stations=50, days_per_station=365)

start = time.time()
result = naive_correlation_analysis(test_data)
elapsed = time.time() - start

print(f"Analyzed {len(result)} station pairs in {elapsed:.3f} seconds")
print(f"First correlation: {result[0]}")

# %% [markdown]
# ### Profiling Reveals the Problem
#
# If we profiled this code with cProfile, we'd see:
#
# **Key findings:**
# - The nested loops create O(n²) complexity
# - For 100 stations: 4,950 pairs to compare
# - For 1,000 stations: 499,500 pairs to compare!
# - We're recalculating means and variances repeatedly
# - NumPy would be 100x faster for these operations
#
# **Optimization strategy based on profiling:**
# 1. Calculate statistics (mean, variance) once per station
# 2. Use NumPy for vectorized operations
# 3. Only calculate correlations for nearby stations
# 4. Parallelize if still too slow
#
# ### Optimized Version
#
# Here's a smarter approach:


# %%
def smart_correlation_analysis(data):
    """
    Calculate correlations more efficiently.

    Optimizations:
    - Pre-calculate statistics for each station
    - Only compare geographically nearby stations (simulated)
    - Use more efficient calculations
    """
    stations = list(data.keys())

    # Pre-calculate statistics once per station
    stats = {}
    for station in stations:
        temps = data[station]
        n = len(temps)
        mean_temp = sum(temps) / n
        variance = sum((t - mean_temp) ** 2 for t in temps)
        stats[station] = {"temps": temps, "mean": mean_temp, "variance": variance, "n": n}

    # Only calculate correlations for "nearby" stations
    # (in real code, this would use actual geographic distance)
    correlations = []
    for i, station_i in enumerate(stations):
        # Only check next 10 stations (simulating geographic proximity)
        for j in range(i + 1, min(i + 11, len(stations))):
            station_j = stations[j]

            si = stats[station_i]
            sj = stats[station_j]

            # Calculate covariance using pre-computed statistics
            cov = sum((si["temps"][k] - si["mean"]) * (sj["temps"][k] - sj["mean"]) for k in range(si["n"]))

            if si["variance"] > 0 and sj["variance"] > 0:
                corr = cov / (si["variance"] * sj["variance"]) ** 0.5
                correlations.append((station_i, station_j, corr))

    return correlations


# Compare performance
start = time.time()
result_smart = smart_correlation_analysis(test_data)
elapsed_smart = time.time() - start

print(f"\nSmart version analyzed {len(result_smart)} pairs in {elapsed_smart:.3f} seconds")
print(f"Speedup: {elapsed/elapsed_smart:.2f}x faster")
print(f"(Analyzed fewer pairs by focusing on nearby stations)")

# %% [markdown]
# ### Lessons from Profiling
#
# **What profiling taught us:**
#
# 1. **Measure, don't guess** - The bottleneck might surprise you
# 2. **Algorithm matters** - O(n²) vs O(n) is huge for large n
# 3. **Pre-compute when possible** - Don't recalculate the same values
# 4. **Know your data** - Geographic locality lets us skip comparisons
# 5. **Use the right tools** - NumPy would make this even faster
#
# **General optimization principles for research code:**
#
# - **Correctness first**: Broken fast code is useless
# - **Profile before optimizing**: Find the real bottlenecks
# - **Start with algorithms**: Better algorithm > micro-optimization
# - **Use libraries**: NumPy, pandas, etc. are highly optimized
# - **Optimize the hot path**: 90% of time is in 10% of code
# - **Measure improvements**: Verify optimization actually helps
# - **Balance speed and clarity**: Readable code is maintainable code

# %% [markdown]
# ## Part 10: Practical Debugging and Profiling Workflow
#
# ### Recommended Workflow for Research Software
#
# **Phase 1: Development**
# 1. Write clear, simple code
# 2. Add assertions for assumptions
# 3. Use descriptive variable names
# 4. Write docstrings
# 5. Add logging at key points
#
# **Phase 2: Testing**
# 1. Write unit tests (Lecture 5)
# 2. Test edge cases
# 3. Use debugger to understand failures
# 4. Achieve good test coverage
#
# **Phase 3: Debugging**
# 1. Reproduce the bug reliably
# 2. Check logs for clues
# 3. Use debugger to inspect state
# 4. Form hypothesis, test it
# 5. Fix and add regression test
#
# **Phase 4: Optimization (only if needed)**
# 1. Profile to find bottlenecks
# 2. Optimize hot paths only
# 3. Verify correctness after optimization
# 4. Measure actual improvement
# 5. Update documentation
#
# ### Tools Summary
#
# **Debugging:**
# - `pdb` / `breakpoint()` - Interactive debugging
# - `logging` - Structured output for diagnosis
# - `assert` statements - Catch invalid state early
#
# **Profiling:**
# - `cProfile` - Function-level time profiling
# - `line_profiler` - Line-by-line time profiling
# - `memory_profiler` - Memory usage profiling
# - `timeit` - Micro-benchmarking for small code snippets
#
# **When to use each:**
# - **pdb**: When code behaves unexpectedly, crashes, or produces wrong results
# - **logging**: Always - it's good practice for any serious code
# - **cProfile**: When code is too slow, to find bottlenecks
# - **line_profiler**: When you know which function is slow but not which line
# - **memory_profiler**: When you run out of memory or suspect memory leaks

# %% [markdown]
# ## Part 11: Debugging Tips for Research Software
#
# ### Common Research Software Bugs
#
# **1. Off-by-one errors in loops**
# ```python
# # BAD: Misses last element
# for i in range(len(data) - 1):
#     process(data[i])
#
# # Use debugger to check: are all elements processed?
# ```
#
# **2. Floating-point comparison**
# ```python
# # BAD: Rarely true due to floating-point precision
# if calculated_value == 0.3:
#     ...
#
# # GOOD: Use tolerance
# if abs(calculated_value - 0.3) < 1e-10:
#     ...
# ```
#
# **3. Mutable default arguments**
# ```python
# # BAD: Default list is shared between calls!
# def add_measurement(value, measurements=[]):
#     measurements.append(value)
#     return measurements
#
# # GOOD: Use None and create new list
# def add_measurement(value, measurements=None):
#     if measurements is None:
#         measurements = []
#     measurements.append(value)
#     return measurements
# ```
#
# **4. Index errors with slicing**
# ```python
# # Check bounds before slicing
# data[start:end]  # What if start >= len(data)?
#
# # Use debugger to check: p start, p end, p len(data)
# ```
#
# **5. Division by zero in calculations**
# ```python
# # Common in normalizations
# normalized = (value - mean) / std_dev  # What if std_dev == 0?
#
# # Add assertion or check
# assert std_dev != 0, f"Standard deviation is zero for {data}"
# ```

# %% [markdown]
# ### Debugging Strategies
#
# **1. Simplify inputs**
# - Use smaller datasets
# - Use simpler test cases
# - Isolate the failing component
#
# **2. Binary search for bugs**
# - Comment out half the code
# - Which half has the bug?
# - Repeat until found
#
# **3. Add assertions liberally**
# ```python
# def process_temperature(temp_celsius):
#     assert -100 <= temp_celsius <= 100, f"Unrealistic temperature: {temp_celsius}"
#     # ... process ...
# ```
#
# **4. Use print() strategically**
# - Print at entry/exit of functions
# - Print loop iterations
# - Print variable types and shapes
# - Remove prints and add logging later
#
# **5. Compare with known good results**
# - Test against validated outputs
# - Use simple cases where you can calculate by hand
# - Compare with other implementations

# %% [markdown]
# ### AI and Debugging
#
# AI assistants are genuinely good at debugging support—recognizing a common error pattern and
# suggesting a fix is exactly the kind of thing they're fast at, often faster than searching
# for the error message yourself. What they're not automatically good at is knowing whether
# that fix addresses the actual problem or just makes the symptom disappear: an AI assistant's
# job is to make the error go away, and the fastest way to do that isn't always the same as
# fixing the actual cause. The debugging skill from this lecture—finding the root cause, not
# just the symptom—is exactly what lets you tell the difference.
#
# Consider a function with a classic off-by-one bug:


# %%
def get_reading_at_position(readings, position):
    """Get the reading at the given position (1-indexed)."""
    return readings[position]


try:
    print(get_reading_at_position([21.5, 22.0, 21.8], 3))
except IndexError as e:
    print(f"Crashed: {e}")

# %% [markdown]
# Asked to "fix this crash," an AI assistant might reasonably suggest catching the exception:


# %%
def get_reading_at_position_papered_over(readings, position):
    """Get the reading at the given position (1-indexed)."""
    try:
        return readings[position]
    except IndexError:
        return None


# No more crash...
print(get_reading_at_position_papered_over([21.5, 22.0, 21.8], 3))

# %% [markdown]
# ...but the 3rd reading (1-indexed) genuinely exists—it's `21.8`. The fix removed the crash
# without fixing the bug: the function now silently returns the wrong answer (`None`) for
# perfectly valid input. That's worse than the crash, which at least told you something was
# wrong. The root cause is the off-by-one indexing itself:


# %%
def get_reading_at_position_fixed(readings, position):
    """Get the reading at the given position (1-indexed)."""
    return readings[position - 1]


print(get_reading_at_position_fixed([21.5, 22.0, 21.8], 3))

# %% [markdown]
# This is exactly tip #5 from above: compare against a case you can verify by hand—the 3rd
# reading in `[21.5, 22.0, 21.8]` is obviously `21.8`. A fix that makes the error message
# disappear isn't the same as a fix that makes the code correct, whether a human or an AI
# assistant wrote it.
#
# **How prompting helps (but doesn't replace review)**: asking an AI assistant to explain *why*
# the crash happens before asking it to fix it—or explicitly requesting "a fix that addresses
# the root cause, not just the exception"—makes a papered-over fix less likely. It doesn't make
# it impossible. The verification step, checking the fix against a case you can compute by
# hand, still has to happen either way.

# %% [markdown]
# ## Summary
#
# ### Key Takeaways
#
# **Debugging:**
# 1. Use systematic approaches, not random changes
# 2. Learn to use pdb - it's more powerful than print statements
# 3. Add logging to research code from the start
# 4. Use appropriate log levels for different situations
# 5. Write tests to prevent bugs from recurring
#
# **Profiling:**
# 1. Don't optimize prematurely - profile first
# 2. Use cProfile to find slow functions
# 3. Use line_profiler for detailed line-by-line analysis
# 4. Optimize algorithms before micro-optimizations
# 5. Measure improvements to verify optimization worked
#
# **Best Practices:**
# 1. Write correct code first, optimize later
# 2. Add logging and assertions during development
# 3. Use debugger to understand code behavior
# 4. Profile before optimizing
# 5. Balance speed, correctness, and readability
#
# ### The Complete Research Software Workflow
#
# 1. **Design**: Plan your approach
# 2. **Implement**: Write clear, tested code (Lectures 1-5)
# 3. **Automate**: Set up CI/CD (Lecture 6)
# 4. **Debug**: Fix issues systematically (Lecture 7 - today!)
# 5. **Optimize**: Make it fast where needed (Lecture 7 - today!)
# 6. **Document**: Explain what and why
# 7. **Share**: Publish your research software
#
# **Remember:** Research software should be:
# - **Correct**: Produces right results
# - **Testable**: Has comprehensive tests
# - **Maintainable**: Can be understood and modified
# - **Efficient**: Fast enough for its purpose
# - **Reproducible**: Others can verify results

# %% [markdown]
# ## Debugging and Profiling in Other Languages
#
# While this lecture focused on Python, the principles apply to all programming languages.
# Here's what to look for in other common research software languages:
#
# ### R
#
# **Debugging:**
# - **browser()** - R's interactive debugger (similar to pdb)
# - **debug()** / **debugonce()** - Set breakpoints on functions
# - **traceback()** - Show call stack after errors
# - **print()** / **cat()** - Basic debugging (like Python print)
#
# **Profiling:**
# - **Rprof()** - Built-in profiler for time analysis
# - **profvis** package - Visual profiling tool
# - **microbenchmark** package - Precise timing for small code snippets
#
# **What to look for:** RStudio has excellent built-in debugging support with breakpoints and variable inspection.
#
# ### MATLAB
#
# **Debugging:**
# - **dbstop** - Set breakpoints in code
# - **dbstep** - Step through code line by line
# - **dbcont** - Continue execution
# - **dbquit** - Exit debugger
# - Built-in GUI debugger in MATLAB IDE
#
# **Profiling:**
# - **profile on/off** - Start/stop profiler
# - **profile viewer** - Visual profiling results
# - **tic/toc** - Simple timing measurements
#
# **What to look for:** MATLAB's GUI makes debugging very visual - you can
# click to set breakpoints and see variables in workspace.
#
# ### C/C++
#
# **Debugging:**
# - **gdb** - GNU Debugger (command-line, powerful)
# - **lldb** - LLVM debugger (macOS default)
# - **valgrind** - Memory debugging and leak detection
# - IDE debuggers (Visual Studio, CLion, Eclipse)
#
# **Profiling:**
# - **gprof** - GNU profiler (compile with -pg flag)
# - **perf** - Linux performance analysis tools
# - **Valgrind** with **callgrind** - Call graph profiling
# - **Intel VTune** - Advanced profiling (commercial)
#
# **What to look for:** Compiled languages need special compilation flags for
# debugging (-g) and profiling (-pg). Memory errors are common - use valgrind!
#
# ### Julia
#
# **Debugging:**
# - **Debugger.jl** - Interactive debugging package
# - **@enter** macro - Step into function
# - **@run** macro - Run with debugger
# - Similar commands to pdb: `n` (next), `s` (step), `c` (continue)
#
# **Profiling:**
# - **@time** macro - Quick timing measurement
# - **@profile** macro - Statistical profiler
# - **ProfileView.jl** - Visualize profiling results
# - **BenchmarkTools.jl** - Accurate benchmarking
#
# **What to look for:** Julia's JIT compilation means first run is slow - profile after warm-up!
#
# ### Fortran
#
# **Debugging:**
# - **gdb** - Works with Fortran (compile with -g)
# - **idb** - Intel Fortran debugger
# - **totalview** - Commercial parallel debugger
# - **print** statements - Still widely used
#
# **Profiling:**
# - **gprof** - GNU profiler (compile with -pg)
# - **Intel VTune** - For Intel compilers
# - **TAU** - Performance analysis for parallel code
# - **Scalasca** - For MPI/OpenMP programs
#
# **What to look for:** Fortran is often used for parallel computing - look for MPI/OpenMP-aware profilers.
#
# ### Rust
#
# **Debugging:**
# - **rust-gdb** / **rust-lldb** - GDB/LLDB wrappers for Rust
# - **println!** macro - Debug printing
# - **dbg!** macro - Quick debug output with values
# - IDE support (VSCode, IntelliJ)
#
# **Profiling:**
# - **cargo-flamegraph** - Generate flame graphs
# - **perf** - Linux performance tools
# - **Criterion.rs** - Benchmarking library
# - **dhat** - Heap profiling
#
# **What to look for:** Rust's ownership system catches many bugs at compile time. Focus profiling on algorithmic issues.
#
# ### Common Patterns Across Languages
#
# No matter what language you use, look for these tools:
#
# 1. **Interactive debugger** - Step through code, inspect variables
# 2. **Logging framework** - Structured output with levels
# 3. **Profiler** - Time and memory analysis
# 4. **Benchmarking tools** - Accurate performance measurement
# 5. **Memory checkers** - For compiled languages (valgrind, sanitizers)
# 6. **IDE integration** - Visual debugging and profiling
#
# **Key principle:** The concepts (systematic debugging, logging, profiling
# before optimizing) are universal - only the tools change!

# %% [markdown]
# ## Acknowledgements and References
#
# This lecture draws on established debugging and profiling practices from
# software engineering and research software development:
#
# ### Primary Sources
#
# - **Research Software Engineering with Python** by The Alan Turing Institute
#   <https://alan-turing-institute.github.io/rse-course/html/>
#   Debugging strategies and profiling approaches adapted from this course.
#
# - **Research Software Engineering with Python** by Damien Irving, Kate Hertweck,
#   Luke Johnston, Joel Ostblom, Charlotte Wickham, and Greg Wilson (2022)
#   <https://third-bit.com/py-rse/>
#   Chapter 11 "Errors and Exceptions" provided insights on debugging practices for research code.
#
# ### Python Documentation
#
# - **Python Debugger (pdb)**
#   <https://docs.python.org/3/library/pdb.html>
#   Official documentation for Python's built-in debugger.
#
# - **Python Logging**
#   <https://docs.python.org/3/library/logging.html>
#   Official documentation for Python's logging module.
#   - Logging HOWTO: <https://docs.python.org/3/howto/logging.html>
#   - Logging Cookbook: <https://docs.python.org/3/howto/logging-cookbook.html>
#
# - **Python Profilers**
#   <https://docs.python.org/3/library/profile.html>
#   Documentation for cProfile and profile modules.
#
# ### Profiling Tools
#
# - **line_profiler**
#   <https://github.com/pyutils/line_profiler>
#   Line-by-line profiling for Python code.
#
# - **memory_profiler**
#   <https://github.com/pythonprofilers/memory_profiler>
#   Memory usage profiling for Python.
#
# ### Classic References
#
# - Knuth, Donald E. (1974). "Structured Programming with go to Statements".
#   *Computing Surveys* 6 (4): 261–301.
#   Contains the famous quote: "Premature optimization is the root of all evil."
#
# - Zeller, Andreas (2009). *Why Programs Fail: A Guide to Systematic Debugging*.
#   Morgan Kaufmann. ISBN 978-0123745156.
#   Comprehensive guide to systematic debugging techniques.
#
# ### Additional Resources
#
# - **Python Debugging With Pdb**
#   <https://realpython.com/python-debugging-pdb/>
#   Practical tutorial on using pdb effectively.
#
# - **Software Carpentry**
#   Debugging and testing lessons for scientific computing.
#
# ### Notes
#
# All code examples in this lecture were developed specifically for educational purposes.
# The climate data analysis examples are simplified illustrations designed to demonstrate
# debugging and profiling concepts in a research context.

# %% [markdown]
# ### Next Steps
#
# Congratulations! You now have a comprehensive toolkit for research software engineering:
#
# - **Lectures 1-2**: Version control, collaboration, Python basics
# - **Lecture 3**: AI-assisted coding foundations
# - **Lecture 4**: Project structure and scientific libraries
# - **Lecture 5**: Testing and quality assurance
# - **Lecture 6**: Continuous integration and automation
# - **Lecture 7**: Debugging and performance optimization (today!)
#
# **In future lectures**, we'll cover:
# - Documentation and publication of research software
# - Working with data (pandas, data formats)
# - Packaging and distribution
# - Advanced topics in research software engineering
#
# **Continue practicing:**
# - Use the debugger in your daily work
# - Add logging to your research code
# - Profile before optimizing
# - Write tests for correctness
# - Share your code with confidence!
#
# **Remember:** Great research software is built through:
# - Clear code that others can understand
# - Thorough testing that builds confidence
# - Systematic debugging when issues arise
# - Strategic optimization where it matters
# - Continuous improvement and learning
#
# Happy debugging and profiling! 🐛🔍📊
