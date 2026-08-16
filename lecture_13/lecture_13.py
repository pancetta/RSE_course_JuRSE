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
# # Lecture 13: Software Architecture and Design for Research Software
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
#     <img src="lecture_13_qr_code.png" alt="This Lecture QR Code" width="150"/>
#     <p><strong>This Lecture</strong></p>
#   </div>
# </div>
#
# ## Overview
# This lecture is about the code-level design decisions that determine whether research software
# stays maintainable as it grows — how you shape functions and modules, not the large-scale
# architecture of distributed systems (that stays out of scope for this course, as ever). We'll
# follow a single running example through four connected stages: the design principles that keep
# code maintainable in the first place, the code smells that signal when those principles have
# been violated, the decision framework for what to do once problems have accumulated into
# technical debt, and the architectural code review habit that catches all of the above before it
# ships. Treated separately, these would be four topics. Followed through one story, they're one
# practice: designing, recognizing, fixing, and reviewing for maintainability.
#
# **Duration**: ~90 minutes
#
# ## Prerequisites
#
# Before starting this lecture, you should be familiar with:
# - Python functions, classes, and modules (Lectures 2 and 4)
# - Writing and running tests with pytest, and what makes code "testable" (Lecture 5)
# - Reading a git diff and participating in pull request review (Lecture 10)
# - AI-assisted coding basics, including reviewing AI suggestions like a diff (covered in
#   Lecture 3)
#
# This lecture assumes you're comfortable writing Python functions and have written or reviewed
# at least one pull request.
#
# ## Learning Objectives
# - Apply DRY, Single Responsibility, and Separation of Concerns to keep research code
#   maintainable as it grows
# - Recognize common code smells — god functions, duplicated code, magic numbers, tight
#   coupling, global state — and explain why they make code hard to test
# - Decide when to refactor versus rewrite using a practical, risk-based framework
# - Refactor incrementally, using tests to keep each step safe
# - Review a pull request for architectural quality, not just correctness, and give
#   constructive design feedback
# - Recognize when the same design problem is recurring across multiple pull requests

# %% [markdown]
# ## Part 1: A Cautionary Tale - The PR That Worked Perfectly
#
# ### The Story
#
# Meet StationWatch: a weather-station network analysis pipeline maintained by a five-person
# research group. It started, like most research software does, as a single script one PhD
# student wrote to answer one question — are two given stations far enough apart to be treated
# as independent in a spatial-correlation model? The script loaded a CSV of station coordinates,
# looped over every pair, and printed the ones within range.
#
# Over the next two years, the script grew. Other lab members added new analyses, and each
# addition reused the pattern that already existed: reach directly into the raw station
# dictionaries wherever a field was needed, and write a new function around whatever shape of
# data that function happened to touch. It worked. Every pull request passed review, because
# every pull request produced correct numbers on the test data. Nobody was writing bad code on
# purpose — they were doing what people do under a deadline: making the smallest change that
# made the current task work.
#
# Then came the PR that broke things — except it didn't look like it should have. A new postdoc
# needed to add a second instrument type to the network: soil-moisture sensors, which report
# readings in a different structure than the weather stations. The PR "worked perfectly": CI was
# green, the reviewer approved it, and it merged. Three months later, when the team tried to add
# a *third* instrument type, they discovered that soil-moisture support had been bolted on by
# copy-pasting the station-analysis function and hand-editing the parts that differed. Now there
# were two nearly-identical, 80-line functions, each reaching directly into a different
# dictionary shape, and neither could be tested without constructing a full, realistic dataset by
# hand. Adding the third instrument type meant untangling both functions first — an estimated
# three weeks of work for a feature that should have taken three days.
#
# ### What Went Wrong?
#
# Nothing in the offending PR was *incorrect*. Every review before it checked correctness and
# style, and every check passed. What nobody was checking was **whether the code's structure
# would survive the next change** — whether functions were reusable, whether pieces could be
# tested independently, whether the design would bend or break when requirements shifted. That's
# what this lecture is about: the code-level design habits that keep the *next* PR cheap, and the
# review habits that catch the drift before it costs three weeks instead of three days.
#
# We'll follow StationWatch through the rest of this lecture — starting with the principles that
# would have prevented the mess, then the smells that would have flagged it in progress, then the
# decision about what to do once it's already there, and finally the review practice that stops
# it from happening again.

# %% [markdown]
# ## Part 2: Design Principles for Maintainable Code
#
# Good software design starts with three principles that make code maintainable, reusable, and
# easy to understand — and that would have kept StationWatch out of trouble in Part 1. These
# principles come from decades of software engineering experience and apply especially well to
# research software, where code often lives for years and is modified by multiple people
# (including future you!).
#
# #### Principle 1: DRY - Don't Repeat Yourself
#
# **The problem**: Copy-pasting code creates maintenance nightmares. When you find a bug or need to
# change behavior, you must remember to update all copies. Miss one, and you have inconsistent
# behavior that's hard to track down.
#
# **The solution**: Write code once, reuse it everywhere. If you find yourself copying and pasting,
# extract that code into a function or class. This is where a good project structure is helpful!
#
# **Bad example - Repetitive code:** this is the shape StationWatch's readings started in—one
# near-identical analysis function per sensor type, before anyone noticed the pattern.


# %%
# DON'T DO THIS: Repeated calculation logic
def analyze_temperature_data(temps):
    """Analyze temperature dataset."""
    mean = sum(temps) / len(temps)
    variance = sum((x - mean) ** 2 for x in temps) / len(temps)
    std_dev = variance**0.5
    return {"mean": mean, "std": std_dev}


def analyze_pressure_data(pressures):
    """Analyze pressure dataset."""
    mean = sum(pressures) / len(pressures)
    variance = sum((x - mean) ** 2 for x in pressures) / len(pressures)
    std_dev = variance**0.5
    return {"mean": mean, "std": std_dev}


def analyze_humidity_data(humidity):
    """Analyze humidity dataset."""
    mean = sum(humidity) / len(humidity)
    variance = sum((x - mean) ** 2 for x in humidity) / len(humidity)
    std_dev = variance**0.5
    return {"mean": mean, "std": std_dev}


# Same calculation logic repeated three times! ❌

# %% [markdown]
# **Good example - DRY principle applied:**


# %%
# DO THIS: Extract common logic
def calculate_statistics(data):
    """Calculate mean and standard deviation for any dataset."""
    if not data:
        raise ValueError("Cannot calculate statistics for empty dataset")

    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std_dev = variance**0.5
    return {"mean": mean, "std": std_dev}


# Now reuse it for any type of data
temp_stats = calculate_statistics([15.2, 16.8, 14.5, 17.3])
pressure_stats = calculate_statistics([1013, 1015, 1012, 1014])
humidity_stats = calculate_statistics([65, 68, 72, 70])

print(f"Temperature: {temp_stats}")
print(f"Pressure: {pressure_stats}")
print(f"Humidity: {humidity_stats}")

# One function, reused three times! ✓
# Bug fixes or improvements only need to be made in ONE place.

# %% [markdown]
# **Why DRY matters in research**:
# - **Fix bugs once**: When you find a calculation error, fix it in one place
# - **Update algorithms easily**: Improve your method without hunting for all copies
# - **Consistency**: The same input always produces the same output
# - **Testing**: Test the logic once instead of testing every copy
#
# **Warning**: Don't take DRY to extremes. If code *looks* similar but has different *purposes*,
# it's okay to keep it separate. DRY applies to logic and behavior, not just appearance.
#
# #### Principle 2: Single Responsibility Principle (SRP)
#
# **The idea**: Each function or module should do **one thing** and do it well. If you can't explain
# what a function does in one simple sentence, it's probably doing too much.
#
# **The benefit**: When each component has one job, it's easier to:
# - Understand what the code does
# - Find where bugs are
# - Test each piece independently
# - Reuse code in different contexts
# - Modify behavior without breaking unrelated functionality
#
# **Bad example - Too many responsibilities:** this is close to what StationWatch's original
# single-question script grew into, one "just add it here" commit at a time.


# %%
# DON'T DO THIS: Function doing too many things
def process_climate_data_badly(filename):
    """Process climate data... but what does it actually do?"""
    # Responsibility 1: Read file
    with open(filename) as f:
        lines = f.readlines()

    # Responsibility 2: Parse data
    temps = []
    for line in lines[1:]:  # Skip header
        parts = line.split(",")
        temps.append(float(parts[2]))

    # Responsibility 3: Calculate statistics
    mean_temp = sum(temps) / len(temps)

    # Responsibility 4: Format output
    output = f"Average temperature: {mean_temp:.1f}°C"

    # Responsibility 5: Write result
    with open("results.txt", "w") as f:
        f.write(output)

    # Responsibility 6: Generate plot
    # (imagine plotting code here)

    return mean_temp


# This function does EVERYTHING. Hard to test, hard to reuse, hard to modify. ❌

# %% [markdown]
# **Good example - Single Responsibility:**

# %%
# DO THIS: Separate concerns into focused functions


def read_csv_file(filename):
    """Read lines from a CSV file."""
    with open(filename) as f:
        return f.readlines()


def parse_temperature_column(lines, column_index=2):
    """Extract temperature values from CSV lines."""
    temps = []
    for line in lines[1:]:  # Skip header
        parts = line.split(",")
        temps.append(float(parts[column_index]))
    return temps


def calculate_mean(values):
    """Calculate arithmetic mean of values."""
    return sum(values) / len(values)


def format_temperature_result(mean_temp):
    """Format temperature result as a string."""
    return f"Average temperature: {mean_temp:.1f}°C"


def write_text_file(filename, content):
    """Write content to a text file."""
    with open(filename, "w") as f:
        f.write(content)


# Now compose them for the full workflow:
# lines = read_csv_file('climate_data.csv')
# temps = parse_temperature_column(lines)
# mean_temp = calculate_mean(temps)
# result_text = format_temperature_result(mean_temp)
# write_text_file('results.txt', result_text)

print("Each function has ONE clear job! ✓")

# %% [markdown]
# **Benefits of this approach**:
# - Each function is easy to test independently
# - Functions are reusable in different contexts (e.g., `calculate_mean` works for any data)
# - Easy to swap implementations (e.g., use pandas instead of manual parsing)
# - Clear what each function does just from its name
# - Bugs are easier to locate (if parsing fails, check `parse_temperature_column`)
#
# #### Principle 3: Separation of Concerns
#
# **The idea**: Different aspects of your program should be in different places. Don't mix data
# loading with analysis logic, don't mix visualization with calculations, don't mix business logic
# with file I/O.
#
# **Why it matters**: Research projects often evolve from a single analysis script to a complex
# pipeline. If concerns are separated from the start, you can easily:
# - Switch data sources (file → database → API)
# - Change output format (console → file → web)
# - Reuse analysis logic in different projects
# - Test each layer independently
#
# **Project structure enforces separation:**
#
# ```
# src/
# ├── data_loading.py      # Concern: Getting data into memory
# ├── preprocessing.py     # Concern: Cleaning and transforming data
# ├── analysis.py          # Concern: Scientific calculations
# ├── visualization.py     # Concern: Creating plots
# └── export.py            # Concern: Saving results
# ```
#
# **Example in practice:** exactly the separation StationWatch was missing—if data access,
# validation, and analysis had been kept apart, adding soil-moisture sensors would have meant
# writing one new loader function, not copy-pasting the whole pipeline.

# %%
# GOOD: Clear separation of concerns


# Concern 1: Data access (could switch from files to database)
def load_experiment_data(source):
    """Load data from source (file, database, API)."""
    # In real code, handle different source types
    return [15.2, 16.8, 14.5, 17.3, 15.9]


# Concern 2: Data validation (ensures quality)
def validate_temperature_data(temps):
    """Check that temperature data is physically reasonable."""
    return [t for t in temps if -100 < t < 100]


# Concern 3: Analysis (pure calculation, no I/O)
def compute_anomaly(temps, baseline):
    """Calculate temperature anomalies from baseline."""
    return [t - baseline for t in temps]


# Concern 4: Presentation (formatting for output)
def format_anomaly_report(anomalies):
    """Create human-readable report of anomalies."""
    return f"Anomalies: {[f'{a:.1f}' for a in anomalies]}"


# Workflow: compose the concerns
data = load_experiment_data("experiment.csv")
valid_data = validate_temperature_data(data)
anomalies = compute_anomaly(valid_data, baseline=16.0)
report = format_anomaly_report(anomalies)
print(report)

# Each layer can be tested and modified independently! ✓

# %% [markdown]
# **Real research example**: Imagine you wrote a paper analyzing temperature data from CSV files.
# Later, you get a grant to analyze 10 years of satellite data from a NASA non-CSV database. If your analysis
# logic is mixed with CSV parsing, you'll have to rewrite everything. If concerns are separated, you
# just write a new `load_experiment_data()` function and reuse all the analysis code!
#
# #### Key Takeaways: Applying Design Principles
#
# These principles work together:
#
# 1. **DRY** prevents code duplication → easier maintenance
# 2. **Single Responsibility** keeps functions focused → easier testing and reuse
# 3. **Separation of Concerns** organizes code by purpose → easier evolution
#
# **Research software benefits**:
# - **Reproduce results reliably**: Well-designed code has fewer bugs
# - **Collaborate effectively**: Team members understand clear, focused code
# - **Publish with confidence**: Reviewers can verify well-structured code
# - **Reuse in future projects**: Good design makes code portable
# - **Evolve as requirements change**: Separated concerns adapt easily
#
# **Start simple**: You don't need perfect design on day one. But as your research code grows beyond
# a few hundred lines, applying these principles will save you countless hours of debugging and
# refactoring. Start as early as possible with a good file/folder structure AND basic software engineering practices. Future you will thank present you!
#
#
# **Further reading** on design principles:
# - Robert C. Martin, *Clean Code: A Handbook of Agile Software Craftsmanship* (2008)
# - Martin Fowler, *Refactoring: Improving the Design of Existing Code* (2018)
# - John Ousterhout, *A Philosophy of Software Design* (2018)

# %% [markdown]
# ## Part 3: Code Smells - Warning Signs of Design Problems
#
# Part 2 told you what good design looks like. **Code smells** tell you when it's missing. The
# term was coined by Kent Beck and popularized by Martin Fowler in his book *Refactoring*. A code
# smell isn't a bug — the code might work perfectly, exactly like the StationWatch PR in Part 1 —
# but it indicates that the code will be hard to maintain, test, or understand.
#
# **Why this matters for testing**: Code that smells bad is often hard or impossible to test. If
# you find yourself struggling to write tests, the problem might not be with your testing
# approach — it might be that your code has design problems (Lecture 5 covers the testing
# techniques that would surface this). Learning to recognize code smells helps you write more
# testable, maintainable code from the start.
#
# **The connection**: Well-designed code is testable code. If your code is hard to test, it's
# probably poorly designed. Code smells are your early warning system.
#
# #### Common Code Smells in Research Software
#
# Let's examine the most common smells in research code, with examples:
#
# **1. God Function (or "Long Function")**
#
# A function that does everything—hundreds of lines, multiple responsibilities, impossible to
# understand or test. It's what StationWatch's SRP violation in Part 2 becomes if nobody ever
# splits it back up.


# %%
# CODE SMELL: God Function ❌
def analyze_experiment(data_file, config_file, output_dir):
    """Analyze experimental data... but what does this really do?"""
    # Read configuration (50 lines)
    # Load data from file (40 lines)
    # Clean and validate data (60 lines)
    # Apply multiple transformations (80 lines)
    # Calculate statistics (50 lines)
    # Generate plots (70 lines)
    # Save results (40 lines)
    # Email notification (30 lines)
    # Total: 420 lines in ONE function!

    # How do you test this? Where do bugs hide?
    # Can you reuse any part of this?
    # Can you understand what it does 6 months from now?
    pass  # Imagine 420 lines here...


# %% [markdown]
# **Why it smells**:
# - Hard to test (must set up files, configs, email server...)
# - Hard to debug (bug could be anywhere in 420 lines)
# - Hard to reuse (all or nothing)
# - Hard to understand (what's the main logic vs details?)
#
# **The fix**: Break into smaller, focused functions (like we saw in Part 2's Single
# Responsibility Principle).
#
# **2. Duplicated Code**
#
# Copy-pasted code that appears in multiple places. We saw this in Part 2 with the DRY principle
# — and it's exactly what happened to StationWatch's soil-moisture PR in Part 1.


# %%
# CODE SMELL: Duplicated code ❌
def analyze_temperature_2019(temps):
    total = 0
    for t in temps:
        total += t
    mean = total / len(temps)

    squared_diffs = 0
    for t in temps:
        squared_diffs += (t - mean) ** 2
    variance = squared_diffs / len(temps)
    return {"mean": mean, "variance": variance}


def analyze_temperature_2020(temps):
    total = 0
    for t in temps:
        total += t
    mean = total / len(temps)

    squared_diffs = 0
    for t in temps:
        squared_diffs += (t - mean) ** 2
    variance = squared_diffs / len(temps)
    return {"mean": mean, "variance": variance}


# Same logic, copied and pasted! Bug in one = bug in both (probably)

# %% [markdown]
# **Why it smells**:
# - Bug fixes must be applied multiple times
# - Easy to miss one copy when updating
# - More code to test and maintain
#
# **The fix**: Extract common logic into a shared function (DRY principle).
#
# **3. Magic Numbers and Unclear Names**
#
# Numbers or strings that appear without explanation, or variables named `x`, `tmp`, `data2`.
# Keep an eye out—Part 4's StationWatch case study hides an unexplained `0.5` of exactly this
# kind in a real distance calculation.


# %%
# CODE SMELL: Magic numbers and unclear names ❌
def process(x, y):
    """Process... what? How?"""
    if x > 273.15:  # What is 273.15?
        z = x * 1.8 + 32  # What is this calculating?
        if z > 200:  # Why 200?
            return z * 0.5  # Why multiply by 0.5?
    return y


# What does this function do? Impossible to tell without detective work!

# BETTER: Self-documenting code ✓
ABSOLUTE_ZERO_KELVIN = 273.15
EXTREME_TEMP_FAHRENHEIT = 200
ADJUSTMENT_FACTOR = 0.5


def convert_temperature_with_bounds(temp_kelvin, fallback_value):
    """Convert Kelvin to Fahrenheit with bounds checking."""
    if temp_kelvin > ABSOLUTE_ZERO_KELVIN:
        temp_fahrenheit = temp_kelvin * 1.8 + 32

        if temp_fahrenheit > EXTREME_TEMP_FAHRENHEIT:
            return temp_fahrenheit * ADJUSTMENT_FACTOR

    return fallback_value


# Now it's clear what the function does and why!

# %% [markdown]
# **Why it smells**:
# - Hard to understand intent
# - Easy to misuse or misunderstand
# - Harder to modify (what was 273.15 again?)
#
# **The fix**: Use named constants and descriptive variable names.
#
# **4. Tight Coupling (or "Feature Envy")**
#
# Functions that reach deep into other objects or modules, creating dependencies that make testing
# difficult. This is precisely the shape of the StationWatch problem from Part 1: both
# instrument-type functions reached directly into a specific dictionary structure.


# %%
# CODE SMELL: Tight coupling ❌
class ExperimentData:
    def __init__(self):
        self.temps = [15.2, 16.8, 14.5]
        self.pressures = [1013, 1015, 1012]


def analyze_data_badly(experiment):
    """This function knows too much about ExperimentData's internals."""
    # Directly accessing internal data structures
    mean_temp = sum(experiment.temps) / len(experiment.temps)
    mean_pressure = sum(experiment.pressures) / len(experiment.pressures)

    # What if ExperimentData changes how it stores data?
    # This function breaks! Testing requires creating full ExperimentData objects.
    return mean_temp, mean_pressure


# BETTER: Loose coupling ✓
# Part 2 already gave us a generic calculate_mean(values) - reuse it instead of writing a
# new function that reaches into ExperimentData's internals.
print(calculate_mean([15.2, 16.8, 14.5]))
print(calculate_mean([1013, 1015, 1012]))

# ExperimentData can change internals without breaking this function.

# %% [markdown]
# **Why it smells**:
# - Hard to test (need to create complex objects)
# - Fragile (breaks when other code changes)
# - Hard to reuse (tied to specific data structures)
#
# **The fix**: Depend on abstractions, not implementations. Accept simple parameters.
#
# **5. Global State and Hidden Dependencies**
#
# Functions that read or modify global variables, making behavior unpredictable and testing
# difficult. If StationWatch had computed anomalies against one hardcoded global baseline,
# supporting a second region with a different baseline climate would have meant hunting through
# the whole codebase for every place that baseline was assumed.

# %%
# CODE SMELL: Global state ❌
BASELINE_TEMPERATURE = 15.0  # Global variable


def calculate_anomaly_bad(temp):
    """Uses global state - hard to test and reason about."""
    return temp - BASELINE_TEMPERATURE


# What happens when multiple analyses need different baselines?
# How do you test this with different baselines?
# Whoever changes BASELINE_TEMPERATURE affects all code!


# BETTER: Explicit dependencies ✓
def calculate_anomaly_good(temp, baseline):
    """Baseline is explicit parameter - easy to test and reuse."""
    return temp - baseline


# Test with any baseline you want!
assert calculate_anomaly_good(20, 15) == 5
assert calculate_anomaly_good(20, 18) == 2

# %% [markdown]
# **Why it smells**:
# - Unpredictable behavior (depends on hidden state)
# - Hard to test (must set up global state)
# - Causes action-at-a-distance bugs (changing one place breaks another)
#
# **The fix**: Make dependencies explicit through parameters.
#
# #### Code Smell Quick Reference
#
# | Smell | Red Flag | Impact on Testing | Fix |
# |-------|----------|------------------|-----|
# | **God Function** | Function > 50 lines, multiple tasks | Setup complex, many tests needed | Split into focused functions |
# | **Duplicated Code** | Copy-pasted logic | Must test same logic multiple times | Extract to shared function (DRY) |
# | **Magic Numbers** | Unexplained constants like `273.15` | Tests unclear without context | Named constants |
# | **Tight Coupling** | Function accesses deep internals | Requires complex object setup | Accept simple parameters |
# | **Global State** | Reads/writes global variables | Tests interfere with each other | Explicit parameters |
# | **Poor Naming** | Variables like `x`, `tmp`, `data2` | Hard to write meaningful test names | Descriptive names |
#
# #### Spotting Code Smells in Practice
#
# Let's put this into practice on a small function from a StationWatch-style pipeline — one that
# converts sensor readings from Fahrenheit to Celsius before combining them with the rest of the
# network's data. Can you spot the smells?


# %%
# Can you spot the code smells?
def fahrenheit_to_celsius_smelly(fahrenheit):
    """Convert temperature from Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 9 / 5  # Bug: should be 5/9


def calculate_temperature_anomaly_smelly(temperatures_f, baseline_f):
    """Calculate temperature anomaly relative to baseline."""
    anomalies = []
    for temp in temperatures_f:
        temp_c = fahrenheit_to_celsius_smelly(temp)
        baseline_c = fahrenheit_to_celsius_smelly(baseline_f)  # SMELL: Duplicated calculation!
        anomaly = temp_c - baseline_c
        anomalies.append(anomaly)
    return anomalies


# %% [markdown]
# **Smells identified**:
#
# 1. **Duplicated calculation**: `fahrenheit_to_celsius(baseline_f)` is called in every loop
#    iteration, but the result never changes! This is wasteful and obscures intent.
#
# 2. **Magic number**: The `32` and fractions aren't explained. A comment would help, or better
#    yet, named constants like `FAHRENHEIT_OFFSET = 32`.
#
# 3. **Not obvious that conversion is wrong**: Without tests, the formula error went unnoticed.
#    The function "smells okay" at first glance but has a subtle bug.
#
# **Better version**:

# %%
# Cleaned up - smells removed ✓
FAHRENHEIT_OFFSET = 32
FAHRENHEIT_TO_CELSIUS_RATIO = 5 / 9


def fahrenheit_to_celsius_clean(fahrenheit):
    """Convert temperature from Fahrenheit to Celsius using standard formula."""
    return (fahrenheit - FAHRENHEIT_OFFSET) * FAHRENHEIT_TO_CELSIUS_RATIO


def calculate_temperature_anomaly_clean(temperatures_f, baseline_f):
    """Calculate temperature anomalies relative to baseline, all in Celsius."""
    # Calculate baseline once, not in loop!
    baseline_c = fahrenheit_to_celsius_clean(baseline_f)

    anomalies = []
    for temp_f in temperatures_f:
        temp_c = fahrenheit_to_celsius_clean(temp_f)
        anomaly = temp_c - baseline_c
        anomalies.append(anomaly)

    return anomalies


# Now the code is clearer and more testable!

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Refactoring smelly code is incredibly satisfying—transform bad into beautiful!</p>
#     <ul>
#         <li><strong>Refactor the code smells:</strong> Take the example functions above
#         and refactor them to eliminate all code smells—extract functions, remove
#         duplication, add clear names, and compare before/after readability.</li>
#         <li><strong>Audit your own code:</strong> Review your current research code for the
#         5 common smells—make a list of issues found, prioritize by impact, and refactor
#         the worst offenders first.</li>
#         <li><strong>Practice continuous refactoring:</strong> Next time you write new code, pause every 30 minutes to
#         refactor—experience how incremental cleanup prevents technical debt from accumulating.</li>
#     </ul>
# </div>

# %% [markdown]
# #### The Testing Connection: Smelly Code is Hard to Test
#
# Here's the key insight: **If your code is hard to test, it probably has design problems.**
#
# **Signs that code smells are making testing hard**:
# - "I need to create 5 objects just to test this one function"
#   → Probably tight coupling
# - "I can't test this without reading/writing files"
#   → Probably mixing I/O with logic (separation of concerns)
# - "My test breaks when I change unrelated code"
#   → Probably global state or tight coupling
# - "I need to mock 10 different things to test this"
#   → Probably god function doing too much
# - "I don't know what to name this test"
#   → Probably unclear what the function does (poor naming)
#
# **Good news**: Testable code is well-designed code. When you write tests, you naturally improve
# your design because:
# - You need simple interfaces (avoid coupling)
# - You need predictable behavior (avoid global state)
# - You need focused functionality (avoid god functions)
# - You need clear contracts (good naming and documentation)
#
# **Further reading on code smells**:
# - Martin Fowler, *Refactoring: Improving the Design of Existing Code* (2018) - The definitive guide
# - Robert C. Martin, *Clean Code* (2008) - Chapters 3, 6, 10 on functions, objects, and classes
# - Steve McConnell, *Code Complete* (2004) - Chapter 7 on defensive programming

# %% [markdown]
# ## Part 4: Technical Debt and Refactoring Decisions
#
# Sooner or later, code smells accumulate into something bigger: **technical debt**. Remember
# StationWatch from Part 1 — two nearly-identical, tightly-coupled analysis functions that took
# three weeks to untangle instead of three days? That's technical debt in its most common
# research-software form. When Lecture 7's profiling tools reveal that code is slow, it's
# frequently technical debt you're seeing — inefficient algorithms and duplicated work
# accumulated the same way. This section asks the question that follows: **when should you
# refactor code, and when should you rewrite it?**
#
# #### What is Technical Debt?
#
# **Technical debt** is a metaphor coined by Ward Cunningham. It's the cost of choosing a quick
# solution now that will require more work later. Like financial debt, it accumulates "interest" -
# the longer you wait to address it, the harder and more expensive it becomes.
#
# **Examples in research code:**
# - Copy-pasting code instead of creating functions (violates DRY)
# - Hardcoding values instead of using configuration
# - Skipping tests "just this once"
# - Writing unclear code because "I'll clean it up later"
# - Using inefficient algorithms because "it works for now"
#
# **Why debt accumulates**: Research projects evolve. What started as a 100-line script for one
# experiment becomes a 10,000-line analysis pipeline used by your whole lab. The quick hacks you
# made in week 1 now slow down everyone in year 2.
#
# **Profiling reveals debt**: When profiling shows that your code is slow, it's often because of
# technical debt—inefficient algorithms, duplicated work, poor data structures. The question is:
# fix the debt (refactor) or start over (rewrite)?
#
# #### Refactor or Rewrite? A Decision Framework
#
# **Refactoring**: Improving code structure without changing behavior. Small, incremental changes.
#
# **Rewriting**: Throwing away code and starting fresh. Big, risky changes.
#
# **When to REFACTOR** (most cases):
#
# ✅ Code works but is hard to understand or maintain
# ✅ You have tests that verify correctness
# ✅ Problems are localized to specific functions/modules
# ✅ You want to preserve git history and attribution
# ✅ Team is actively using the code
# ✅ Changes can be made incrementally
#
# **When to REWRITE** (rare):
#
# ⚠️ Fundamental architectural problems throughout
# ⚠️ Technology stack is obsolete (Python 2 → Python 3)
# ⚠️ Requirements changed completely
# ⚠️ Code is a prototype, never meant for production
# ⚠️ No tests exist and code is too complex to test
# ⚠️ Rewrite would be faster than fixing
#
# **Default choice: REFACTOR**. Rewrites are risky, often fail, and lose accumulated knowledge.
#
# #### Decision Matrix: Size × Risk × Time
#
# | Code Size | Test Coverage | Risk | Recommendation |
# |-----------|---------------|------|----------------|
# | < 100 lines | None | Low | Rewrite OK if you want |
# | < 1000 lines | Good tests | Low | Refactor incrementally |
# | > 1000 lines | Good tests | Medium | Definitely refactor |
# | > 1000 lines | No tests | High | Write tests first, then refactor |
# | > 10000 lines | Any | Very High | Never rewrite everything at once |
#
# **The "Strangler Fig" pattern**: For large rewrites, create new code alongside old code,
# gradually replacing pieces until nothing of the old remains. Named after the fig tree that
# grows around and eventually replaces its host tree.
#
# #### Profiling-Driven Refactoring: A Case Study
#
# Let's make this concrete with a different piece of the StationWatch pipeline, further down the
# line: profiling revealed a bottleneck in the code that finds nearby station pairs.


# %%
# BEFORE: Slow code with technical debt
def analyze_all_stations_slow(stations):
    """Analyze all station pairs - SLOW due to O(n²) algorithm."""
    results = []
    n = len(stations)

    # Technical debt #1: Nested loop (quadratic complexity)
    for i in range(n):
        for j in range(i + 1, n):
            # Technical debt #2: Duplicated distance calculation
            dx = stations[i]["lon"] - stations[j]["lon"]
            dy = stations[i]["lat"] - stations[j]["lat"]
            distance = (dx**2 + dy**2) ** 0.5

            # Technical debt #3: Magic number (what is 0.5?)
            if distance < 0.5:
                results.append((i, j))

    return results


# Decision: Refactor or rewrite?
# - Size: ~15 lines - small
# - Tests: Have tests from earlier
# - Problem: Algorithm complexity, magic numbers
# - Decision: REFACTOR (incremental improvements)

# %% [markdown]
# **Refactoring approach - Step by step:**

# %%
# Step 1: Extract magic number (immediate improvement)
MAX_DISTANCE_DEGREES = 0.5  # Stations within ~50km


def analyze_all_stations_v2(stations):
    """Version 2: Extracted constant."""
    results = []
    n = len(stations)

    for i in range(n):
        for j in range(i + 1, n):
            dx = stations[i]["lon"] - stations[j]["lon"]
            dy = stations[i]["lat"] - stations[j]["lat"]
            distance = (dx**2 + dy**2) ** 0.5

            if distance < MAX_DISTANCE_DEGREES:
                results.append((i, j))

    return results


# Test: Still works? ✓

# %% [markdown]
# Step 2: Extract distance calculation (apply DRY):


# %%
def calculate_distance(station_a, station_b):
    """Calculate approximate distance between two stations."""
    dx = station_a["lon"] - station_b["lon"]
    dy = station_a["lat"] - station_b["lat"]
    return (dx**2 + dy**2) ** 0.5


def analyze_all_stations_v3(stations):
    """Version 3: Extracted distance calculation."""
    results = []
    n = len(stations)

    for i in range(n):
        for j in range(i + 1, n):
            distance = calculate_distance(stations[i], stations[j])

            if distance < MAX_DISTANCE_DEGREES:
                results.append((i, j))

    return results


# Test: Still works? ✓
# Bonus: Can now test calculate_distance() separately!

# %% [markdown]
# Step 3: Improve algorithm (the real performance fix):


# %%
def analyze_nearby_stations_only(stations):
    """Version 4: Smarter algorithm - only check nearby stations."""
    results = []

    # Sort by longitude for spatial indexing
    sorted_stations = sorted(enumerate(stations), key=lambda x: x[1]["lon"])

    for idx, (i, station_i) in enumerate(sorted_stations):
        # Only check stations within MAX_DISTANCE in longitude
        for j, station_j in sorted_stations[idx + 1 :]:
            if abs(station_i["lon"] - station_j["lon"]) > MAX_DISTANCE_DEGREES:
                break  # No need to check further

            distance = calculate_distance(station_i, station_j)
            if distance < MAX_DISTANCE_DEGREES:
                results.append((i, j))

    return results


# Test: Still works? ✓
# Performance: Much faster! (early termination)

# %% [markdown]
# **What we accomplished through refactoring:**
#
# 1. ✅ **Improved clarity** (named constant instead of magic number)
# 2. ✅ **Improved testability** (extracted distance function)
# 3. ✅ **Improved performance** (better algorithm)
# 4. ✅ **Preserved correctness** (tests passed at each step)
# 5. ✅ **Kept git history** (incremental commits show evolution)
#
# **Why refactoring worked here:**
# - Small, focused changes
# - Tests verified each step
# - Each version was an improvement
# - Never broke working code
#
# **Compare to rewriting**: If we'd thrown away the code and started over, we might have:
# - Introduced new bugs
# - Lost edge case handling
# - Broken dependent code
# - Wasted time reimplementing working parts
#
# #### Incremental Refactoring Strategy
#
# **The boy scout rule**: "Leave code cleaner than you found it."
#
# When you touch code (for any reason), make it slightly better:
#
# 1. **Adding a feature?** → Clean up surrounding code first
# 2. **Fixing a bug?** → Refactor to prevent similar bugs
# 3. **Profiling reveals slowness?** → Extract the slow part, optimize it
# 4. **Code review feedback?** → Apply the lesson throughout the codebase
#
# **Small refactorings compound**: Five minutes of cleanup per day = cleaner codebase in weeks.
#
# **Safe refactoring practices:**
# - Always have tests before refactoring
# - Make one change at a time
# - Run tests after each change
# - Commit working changes frequently
# - Use version control (easy to revert if needed)
# - Don't change behavior and refactor simultaneously
#
# #### When Technical Debt is Acceptable
#
# **Controversial opinion**: Some technical debt is okay, even good!
#
# **Accept debt when:**
# - Prototyping to test research ideas
# - Rapid iteration is more important than quality
# - Code will be thrown away after the experiment
# - You're learning and will rewrite with knowledge gained
# - Deadline is critical (conference submission!)
#
# **But**: Make it intentional. Write a comment: `# TODO: This is hacky, clean up later`
#
# **Pay debt before:**
# - Publishing the code
# - Sharing with collaborators
# - Using in production analysis
# - Building upon it for future work
#
# **Research reality**: Your "quick prototype" often becomes the production code your entire
# paper depends on. Plan accordingly!
#
# #### Key Takeaways: Refactoring Mindset
#
# 1. **Technical debt is inevitable** - research code evolves, requirements change
# 2. **Default to refactoring** - rewrites are risky and often fail
# 3. **Profiling guides refactoring** - focus on actual bottlenecks, not guesses
# 4. **Small steps, tested** - incremental changes with tests are safe
# 5. **Don't rewrite working code** - unless you have a really good reason
# 6. **Tests enable refactoring** - you can't refactor safely without tests
#
# **Connections:**
# - **Part 2 of this lecture**: Good design principles prevent technical debt from accumulating
#   in the first place
# - **Lecture 5**: Tests make refactoring safe
# - **Lecture 7**: Profiling reveals where to refactor for performance
#
# **Further reading**:
# - Martin Fowler, *Refactoring: Improving the Design of Existing Code* (2018)
# - Michael Feathers, *Working Effectively with Legacy Code* (2004)
# - Joel Spolsky, "Things You Should Never Do, Part I" (on why rewrites fail)

# %% [markdown]
# ## Part 5: Reviewing Pull Requests for Architecture
#
# Beyond checking for correctness and style, effective code reviews also evaluate **software
# architecture and design quality**. This is especially important in research software, where
# code often evolves from a quick prototype to a critical analysis pipeline used by many people.
#
# Reviewing architecture helps prevent technical debt and ensures code remains maintainable as
# projects grow. Let's learn how to review code for design quality, not just bugs.
#
# ### Why Architectural Review Matters
#
# You know why: it's the StationWatch PR from Part 1. **A five-minute architectural review during
# that PR would have caught the design issue that cost three weeks later.** Architectural problems
# compound—a poorly designed function becomes a poorly designed module, then a poorly designed
# system—so catching them in review is far cheaper than refactoring later.
#
# **What architectural review catches, beyond correctness and style**: code smells (Part 3),
# violations of the design principles from Part 2, technical debt (Part 4), missing abstractions,
# and inconsistent patterns across the codebase.
#
# ### Architectural Review Checklist
#
# When reviewing a PR, ask these design-focused questions:
#
# #### 1. Design Principles (Part 2)
#
# **DRY - Don't Repeat Yourself**
# ```python
# # ❌ Code smell in PR:
# def analyze_temp_2019(data):
#     mean = sum(data) / len(data)
#     variance = sum((x - mean)**2 for x in data) / len(data)
#     return mean, variance
#
# def analyze_temp_2020(data):
#     mean = sum(data) / len(data)
#     variance = sum((x - mean)**2 for x in data) / len(data)
#     return mean, variance
#
# # Review comment:
# # "These functions duplicate the statistics calculation. Could we extract
# #  a shared calculate_statistics(data) function and call it from both?"
# ```
#
# **Single Responsibility and Separation of Concerns get the same treatment in review** — watch
# for one function whose name would need "and" to describe honestly, or calculation logic mixed
# with file I/O:
#
# | Violation | Review Comment Example |
# |-----------|------------------------|
# | **SRP**: one 300-line function loads, cleans, analyzes, plots, *and* emails results | "Could we split this into `load_data`, `clean_data`, `analyze_data`, and `save_results`? That would make each piece testable and reusable on its own." |
# | **Separation of Concerns**: `calculate_correlation(file1, file2)` opens the files itself | "Could this take `data1, data2` instead of filenames? Pure calculation is testable without creating files, and reusable with data from a database or API." |
#
# #### 2. Code Smells (Part 3)
#
# **Watch for these red flags in PRs:**
#
# | Smell | What to Look For | Review Comment Example |
# |-------|------------------|------------------------|
# | **God Function** | Function > 50 lines, multiple tasks | "Could we split this into smaller functions?" |
# | **Magic Numbers** | Unexplained constants like `273.15` | "Consider extracting this as KELVIN_OFFSET" |
# | **Tight Coupling** | Function depends on internals of other classes | "Accept simple parameters instead of whole object" |
# | **Global State** | Uses/modifies global variables | "Pass this as a parameter for testability" |
# | **Poor Naming** | Variables like `tmp`, `x2`, `calc` | "More descriptive names would help readability" |
# | **Duplication** | Same logic in multiple places | "Extract shared logic to avoid duplication" |
#
# #### 3. API Design and Consistency
#
# **Check for consistent patterns across the codebase:**
#
# ```python
# # ❌ Inconsistent API in PR:
# # Existing code:
# def load_temperature_data(filename, units='celsius'):
#     """Load data with configurable units."""
#     pass
#
# # New code in PR:
# def load_pressure_data(filename):
#     """Load pressure data in pascals only."""
#     pass
#
# # Review comment:
# # "For consistency with load_temperature_data(), should we add a units
# #  parameter here too? Future users might need different pressure units
# #  (Pa, hPa, bar, etc.). API consistency makes the library easier to learn."
# ```
#
# The flip side is worth praising, not just flagging: when a PR *does* unify an interface — say,
# one `load_scientific_data(filename, data_type, units=None)` instead of a loader per instrument
# type — say so. A good abstraction deserves the same specific feedback as a missing one.
#
# #### 4. Testability
#
# **Hard-to-test code is often poorly designed code (the Testing Connection from Part 3):**
#
# ```python
# # ❌ Hard to test (no tests in PR):
# def analyze_experiment():
#     data = load_from_database(DB_CONNECTION_STRING)  # Global!
#     results = complex_analysis(data)
#     save_to_file('results.csv', results)
#     return results
#
# # Review comment:
# # "This function is hard to test because it depends on a database and
# #  writes to files. Could we refactor to:
# #
# #  def analyze_experiment(data):
# #      return complex_analysis(data)
# #
# #  Then the caller handles I/O, and we can easily test the analysis
# #  logic with simple test data. This follows separation of concerns."
# ```
#
# #### 5. Future Maintainability
#
# **Think about code evolution:**
#
# ```python
# # Review question:
# # "If we need to support a new instrument type in 6 months, would this
# #  design make that easy or would we need major refactoring?"
#
# # Review question:
# # "If we need to parallelize this computation, is the design amenable
# #  to that? (No global state, pure functions, etc.)"
#
# # Review question:
# # "When we publish this code, will external users find the API clear
# #  and intuitive?"
# ```
#
# ### When to Suggest Refactoring in Review
#
# ✅ **Do suggest it** when a design issue blocks testability, violates a project standard, or is
# localized and low-risk to fix while the PR is already touching that code.
#
# ⚠️ **Don't insist on it** when the change is purely aesthetic, would expand the PR's scope,
# touches temporary/experimental code, or would overwhelm a new contributor.
#
# **Balance is key**: Focus on architectural issues that matter, not perfection.
#
# ### How to Give Architectural Feedback Constructively
#
# **Bad review comment** (sounds like criticism):
# ```
# This design is wrong. You should use the strategy pattern here.
# ```
#
# **Good review comment** (collaborative and educational):
# ```
# This function is doing a lot! I wonder if we could simplify by extracting
# the file I/O from the calculation logic? That would make it easier to test
# and reuse. What do you think?
#
# For reference, see Part 2's section on Separation of Concerns above. Happy
# to discuss alternatives if you have thoughts on this!
# ```
#
# **Components of good architectural feedback:**
#
# 1. **Explain the problem and suggest a solution**: "This makes testing hard because... could we
#    extract this into..."
# 2. **Ask, don't demand, and offer to discuss**: "What do you think? Happy to chat if you want to
#    explore options."
# 3. **Provide references**: "See Part 3 on code smells"
#
# ### Balancing Nitpicking vs. Structural Issues
#
# **Not all review comments are equally important. Prioritize:**
#
# - **🔴 Critical (must fix before merge)**: correctness bugs, security vulnerabilities, major
#   architectural flaws (god functions, tight coupling), missing tests for critical functionality
# - **🟡 Important (should fix, but negotiable)**: inconsistencies with project patterns, code
#   smells that hinder maintenance, missing documentation
# - **🟢 Nice-to-have (optional suggestions)**: style preferences, naming improvements,
#   refactoring opportunities beyond the PR's scope
#
# **Mark the priority explicitly** — a `[Critical]`, `[Important]`, or `[Nit]` tag at the start of
# a comment tells the author what blocks the merge and what's a suggestion for later.
#
# ### Spotting Architectural Smells Across PRs
#
# **Watch for patterns across multiple PRs:**
#
# - **All PRs adding similar code** → Missing abstraction
# - **Many PRs touching same file** → God file/class
# - **PRs constantly fixing bugs in same area** → Design issue
# - **PRs blocked on merge conflicts** → Tight coupling
# - **Hard to review large PRs** → Functions doing too much
#
# **Team-level action:**
# ```
# "I've noticed 3 recent PRs all duplicate the same statistics calculation.
#  Should we refactor to extract a shared stats module? This would prevent
#  future duplication and make testing centralized."
# ```
#
# ### Code Review: A Learning Opportunity
#
# Reviews teach design skills in both directions: reviewers see how others solve similar
# problems and practice articulating design principles, while authors get feedback on their
# design choices and learn team standards through iteration. Many researchers haven't had formal
# software engineering training — code review is how a team collectively learns good design. Be
# patient, be educational, and remember: everyone is still learning this.
#
# ### Key Takeaways: Architectural Code Review
#
# 1. **Look beyond correctness** - review for maintainability and design quality, and think
#    about whether the design will adapt well to future change
# 2. **Apply the principles from Parts 2-3** - DRY, SRP, code smells
# 3. **Balance perfectionism and pragmatism** - not every issue needs fixing now; prioritize
#    critical vs. important vs. nice-to-have
# 4. **Be constructive and educational** - reviews are learning opportunities in both directions
# 5. **Catch patterns early** - watch for the same design problem recurring across PRs
#
# **Connections:**
# - **Part 2**: Apply design principles in review
# - **Part 3**: Spot code smells in PRs
# - **Part 4**: Suggest refactoring when technical debt has accumulated
#
# **Remember**: The goal is not perfect code—it's code that works correctly, is maintainable,
# and enables the team to do great science together!
#
# **Further reading**:
# - Karl E. Wiegers, *Peer Reviews in Software: A Practical Guide* (2002)
# - Jeff Atwood, "Code Reviews: Just Do It" (blog post)
# - Thoughtbot's "Code Review Guide" (freely available online)

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Interested in architectural thinking? Explore these design-focused activities:</p>
#     <ul>
#         <li><strong>Map your project's architecture</strong>: Draw a diagram of how
#         your main code modules relate. Where does data flow? Which parts depend on
#         others? Seeing structure helps you review it.</li>
#         <li><strong>Review for future change</strong>: Look at a PR and ask: "If
#         requirements changed, which parts would need to be rewritten?" Good architecture
#         makes change easy - is this flexible or brittle?</li>
#         <li><strong>Spot coupling in the wild</strong>: Find a large function in your
#         codebase that does multiple things. How would you split it? What would make it
#         more testable and maintainable?</li>
#     </ul>
# </div>

# %% [markdown]
# ## Summary
#
# ### Following StationWatch Through This Lecture
#
# Across this lecture, one project illustrated the whole arc:
#
# 1. **The PR that worked perfectly** (Part 1) — correct code, tightly coupled design, no review
#    caught it
# 2. **The principles that would have prevented it** (Part 2) — DRY, Single Responsibility,
#    Separation of Concerns
# 3. **The smells that would have flagged it** (Part 3) — god functions, duplication, magic
#    numbers, tight coupling, global state
# 4. **The decision once it's already there** (Part 4) — refactor incrementally, guided by tests
#    and profiling, rather than rewriting from scratch
# 5. **The review practice that stops it recurring** (Part 5) — a design-focused checklist,
#    applied for five minutes on every PR
#
# ### Key Takeaways
#
# ✅ Good design principles (DRY, SRP, Separation of Concerns) are cheap when applied early and
# expensive to retrofit later
#
# ✅ Code smells are not bugs — code can smell bad and still produce correct output — but they
# predict where the next bug or the next expensive rewrite will come from
#
# ✅ Hard-to-test code is usually a symptom of a design problem, not a testing problem
#
# ✅ Default to refactoring, not rewriting; small tested steps beat a risky rewrite almost every
# time
#
# ✅ Some technical debt is a reasonable trade-off — taken on intentionally, and paid off before
# the code is shared or published
#
# ✅ Architectural review is a five-minute habit added to your existing review process, not a
# separate one
#
# ### A Note on Scope
#
# This lecture stayed at the level of functions, modules, and pull requests — the code-level
# design decisions research software engineers make every week. Large-scale system architecture
# (microservices, distributed systems, formal methods) is out of scope for this course. But the
# habits covered here — naming the responsibility of a function, keeping I/O separate from
# computation, reviewing structure alongside correctness — are the same habits that scale up to
# those bigger questions, if and when your research software grows into that territory.

# %% [markdown]
# ## Acknowledgements and References
#
# This lecture consolidates and builds on established software design literature:
#
# ### Primary Sources
#
# - **Research Software Engineering with Python** by The Alan Turing Institute
#   <https://alan-turing-institute.github.io/rse-course/html/>
#   General framing on code quality and maintainability in a research context.
#
# ### Classic References on Design and Refactoring
#
# - Martin Fowler, *Refactoring: Improving the Design of Existing Code* (2018)
#   The definitive reference for code smells and refactoring technique, cited throughout Parts 3
#   and 4.
#
# - Robert C. Martin, *Clean Code: A Handbook of Agile Software Craftsmanship* (2008)
#   Informs the design-principles discussion in Part 2 and the code-smell catalogue in Part 3.
#
# - John Ousterhout, *A Philosophy of Software Design* (2018)
#   Informs Part 2's discussion of Separation of Concerns.
#
# - Steve McConnell, *Code Complete* (2004), Chapter 7
#   Informs Part 3's discussion of defensive, self-documenting code.
#
# - Michael Feathers, *Working Effectively with Legacy Code* (2004)
#   Informs Part 4's refactor-vs-rewrite framework.
#
# - Joel Spolsky, "Things You Should Never Do, Part I" (blog post)
#   Informs Part 4's caution against full rewrites.
#
# - Ward Cunningham's technical debt metaphor, as popularized in the software engineering
#   literature. Informs Part 4.
#
# - Kent Beck's coinage of "code smell," as popularized by Martin Fowler. Informs Part 3.
#
# - Karl E. Wiegers, *Peer Reviews in Software: A Practical Guide* (2002)
#   Informs Part 5's review practices.
#
# - Jeff Atwood, "Code Reviews: Just Do It" (blog post)
#   Informs Part 5.
#
# - Thoughtbot's "Code Review Guide" (freely available online)
#   Informs Part 5.
#
# ### Notes
#
# This lecture consolidates content that, in an earlier structure of the course, was distributed
# across separate lectures on project structure, testing, debugging, and collaboration into a
# single, dedicated treatment, connected by a running example developed for this course. The
# StationWatch scenario and its code examples are illustrative and were developed specifically
# for this course.

# %% [markdown]
# ### Next Steps
#
# Design and architecture aren't a one-time lesson — they're a habit you apply on every PR from
# here on, alongside the testing, debugging, and collaboration practices from Lectures 5, 7, and
# 10. Lecture 14 closes out the course with a summary of everything you've learned and a look at
# the RSE community and career paths ahead.
#
# **Ready to continue? Move on to Lecture 14: Course Summary and the RSE Community!**
