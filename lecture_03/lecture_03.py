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
# # Lecture 3: Python Fundamentals and Advanced Concepts
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
#     <img src="lecture_03_qr_code.png" alt="This Lecture QR Code" width="150"/>
#     <p><strong>This Lecture</strong></p>
#   </div>
# </div>
#
# ## Overview
# This lecture deepens your Python knowledge by covering advanced function concepts,
# error handling, file I/O, and functional programming techniques. These skills are
# essential for writing robust, maintainable research software.
#
# **Duration**: ~90 minutes
#
# ## Prerequisites
#
# Before starting this lecture, you should be familiar with:
# - Python basics: variables, data types, and operators (covered in Lecture 2)
# - Basic function syntax and calling functions
# - Lists, dictionaries, and control flow (if statements, loops)
# - Git and GitHub basics for version control
#
# This lecture builds directly on the Python fundamentals introduced in Lecture 2.
#
# ## Learning Objectives
# - Master advanced function concepts and documentation
# - Handle errors gracefully with try/except blocks
# - Read and write data files
# - Use list comprehensions for elegant code
# - Create command-line scripts with argparse
# - Apply functional programming concepts

# %% [markdown]
# ## Part 1: Advanced Functions
#
# In Lecture 2, you wrote functions with simple positional parameters. Python supports several
# additional parameter types that make functions much more flexible: parameters with default
# values (so callers can omit them), keyword arguments (so callers can name them in any order),
# and variable-length argument lists. In this part, we'll explore these features and look at
# how to document functions professionally.
#
# ### Function Parameters and Arguments
#
# A function parameter can have a **default value**, making it optional when the function is
# called. If the caller doesn't supply a value, Python uses the default. This is useful when
# most calls need the same setting but some calls need to override it. The example below shows
# a function with two optional parameters: `method` (which analysis to perform) and
# `remove_outliers` (whether to clean the data first).


# %%
def analyze_data(data, method="mean", remove_outliers=False):
    """
    Analyze numerical data with different methods.

    Parameters
    ----------
    data : list
        List of numerical values
    method : str, optional
        Analysis method: 'mean', 'median', or 'mode' (default: 'mean')
    remove_outliers : bool, optional
        Whether to remove outliers before analysis (default: False)

    Returns
    -------
    float
        Calculated result

    Examples
    --------
    >>> analyze_data([1, 2, 3, 4, 5])
    3.0
    >>> analyze_data([1, 2, 3, 4, 100], remove_outliers=True)
    2.5
    """
    # Copy data to avoid modifying original
    working_data = data.copy()

    # Remove outliers if requested
    if remove_outliers:
        # Simple outlier removal: values more than 2 std devs from mean
        mean = sum(working_data) / len(working_data)
        variance = sum((x - mean) ** 2 for x in working_data) / len(working_data)
        std = variance**0.5
        working_data = [x for x in working_data if abs(x - mean) <= 2 * std]

    # Calculate based on method
    if method == "mean":
        return sum(working_data) / len(working_data)
    elif method == "median":
        sorted_data = sorted(working_data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        else:
            return sorted_data[mid]
    else:
        raise ValueError(f"Unknown method: {method}")


# Test with different parameters
data = [10, 12, 13, 11, 50, 12, 13]
print(f"Data: {data}")
print(f"Mean: {analyze_data(data, method='mean'):.2f}")
print(f"Median: {analyze_data(data, method='median'):.2f}")
print(f"Mean (outliers removed): {analyze_data(data, method='mean', remove_outliers=True):.2f}")

# %% [markdown]
# ### Default Arguments and Keyword Arguments
#
# When calling a function, Python normally matches arguments to parameters by position. However,
# you can also pass arguments **by name** (as keyword arguments), which makes the call more
# readable and lets you supply optional arguments in any order. The special `**kwargs` syntax
# captures any extra named arguments as a dictionary—useful when you want to accept arbitrary
# configuration options without listing them all explicitly.


# %%
def create_experiment(name, duration=7, temperature=25.0, samples=100, **kwargs):
    """
    Create an experiment configuration.

    Parameters
    ----------
    name : str
        Experiment name
    duration : int, optional
        Duration in days (default: 7)
    temperature : float, optional
        Temperature in Celsius (default: 25.0)
    samples : int, optional
        Number of samples (default: 100)
    **kwargs : dict
        Additional experiment parameters

    Returns
    -------
    dict
        Experiment configuration
    """
    config = {"name": name, "duration": duration, "temperature": temperature, "samples": samples}

    # Add any additional parameters
    config.update(kwargs)

    return config


# Different ways to call the function
exp1 = create_experiment("Quick Test")
exp2 = create_experiment("Long Study", duration=30, samples=500)
exp3 = create_experiment("Custom", humidity=65, location="Lab B", researcher="Dr. Smith")

print("Experiment 1:", exp1)
print("Experiment 2:", exp2)
print("Experiment 3:", exp3)

# %% [markdown]
# ### Lambda Functions
#
# Lambda functions are small, anonymous functions useful for simple operations.


# %%
# Regular function
def square(x):
    return x**2


# Equivalent lambda function
def square_lambda(x):
    return x**2


print(f"Regular function: {square(5)}")
print(f"Lambda function: {square_lambda(5)}")

# %%
# Lambda functions with sorting
experiments = [{"name": "Exp A", "score": 85}, {"name": "Exp B", "score": 92}, {"name": "Exp C", "score": 78}]

# Sort by score
sorted_by_score = sorted(experiments, key=lambda x: x["score"])
print("Sorted by score:")
for exp in sorted_by_score:
    print(f"  {exp['name']}: {exp['score']}")

# Sort by name
sorted_by_name = sorted(experiments, key=lambda x: x["name"])
print("\nSorted by name:")
for exp in sorted_by_name:
    print(f"  {exp['name']}: {exp['score']}")

# %% [markdown]
# ### Documentation Best Practices
#
# Good docstrings follow standard formats like NumPy style.


# %%
def calculate_statistics(values, precision=2):
    """
    Calculate comprehensive statistics for a dataset.

    This function computes mean, standard deviation, minimum, maximum,
    and range for a list of numerical values.

    Parameters
    ----------
    values : list of float
        Numerical data to analyze
    precision : int, optional
        Number of decimal places for rounding (default: 2)

    Returns
    -------
    dict
        Dictionary containing:
        - mean : float
            Arithmetic mean
        - std : float
            Standard deviation
        - min : float
            Minimum value
        - max : float
            Maximum value
        - range : float
            Difference between max and min

    Raises
    ------
    ValueError
        If values list is empty

    Examples
    --------
    >>> calculate_statistics([1, 2, 3, 4, 5])
    {'mean': 3.0, 'std': 1.41, 'min': 1, 'max': 5, 'range': 4}

    Notes
    -----
    Standard deviation uses the population formula (divide by n).
    For sample standard deviation, divide by (n-1).
    """
    if len(values) == 0:
        raise ValueError("Cannot calculate statistics for empty list")

    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    std = variance**0.5

    return {
        "mean": round(mean, precision),
        "std": round(std, precision),
        "min": min(values),
        "max": max(values),
        "range": max(values) - min(values),
    }


# Test the function
data = [23.5, 24.1, 23.8, 24.3, 23.9, 24.0]
stats = calculate_statistics(data)
print("Statistics:", stats)

# Access the docstring
print("\nDocstring:")
print(calculate_statistics.__doc__)

# %% [markdown]
# ## Part 2: Error Handling
#
# Errors are inevitable in programming—even experienced developers encounter them daily. The
# difference between beginner and professional code is how errors are handled. Good programs
# anticipate what can go wrong and handle errors gracefully, providing useful feedback instead
# of crashing. This is especially important in research software, where a crash during a long
# experiment can waste hours or days of computation time.
#
# ### Common Error Types
#
# Python has many built-in exception types. Understanding the most common ones helps you write
# better error handling code and debug problems faster. Each exception type represents a specific
# kind of problem.

# %%
# Examples of common errors (commented to prevent execution)

# TypeError: wrong type
# result = "10" + 5

# ValueError: invalid value
# number = int("not a number")

# KeyError: missing dictionary key
# data = {'name': 'test'}
# value = data['missing_key']

# IndexError: list index out of range
# items = [1, 2, 3]
# value = items[10]

# FileNotFoundError: file doesn't exist
# with open('nonexistent.txt', 'r') as f:
#     content = f.read()

print("Error examples shown as comments to prevent execution")

# %% [markdown]
# **Understanding these errors**:
# - **TypeError**: You tried to perform an operation on incompatible types (like adding a string to a number)
# - **ValueError**: The type is correct but the value is wrong (like converting "hello" to an integer)
# - **KeyError**: You tried to access a dictionary key that doesn't exist
# - **IndexError**: You tried to access a list element that doesn't exist
# - **FileNotFoundError**: You tried to open a file that doesn't exist
#
# **Common mistake**: Confusing ValueError and TypeError. TypeError means "wrong type entirely"
# (e.g., a string when you need a number). ValueError means "right type, wrong value" (e.g., the
# string "hello" when converting to an integer—it's a string, which is the right type for `int()`,
# but the value can't be converted).

# %% [markdown]
# ### Try-Except Blocks
#
# Use try-except to catch and handle errors. The basic pattern is: try to do something that might
# fail, and if it fails, handle the error gracefully instead of crashing. This is similar to
# "error checking" in other languages but more powerful and Pythonic.
#
# **When to use try-except**: Use it whenever you're doing something that might fail for reasons
# outside your control—reading files, network requests, parsing user input, etc. Don't use it for
# logic errors in your own code (like accessing the wrong list index)—those should be fixed, not
# caught.


# %%
def safe_divide(a, b):
    """
    Safely divide two numbers.

    Parameters
    ----------
    a : float
        Numerator
    b : float
        Denominator

    Returns
    -------
    float or None
        Result of division, or None if division by zero
    """
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print(f"Error: Cannot divide {a} by zero")
        return None


# Test the function
print(f"10 / 2 = {safe_divide(10, 2)}")
print(f"10 / 0 = {safe_divide(10, 0)}")
print(f"15 / 3 = {safe_divide(15, 3)}")

# %% [markdown]
# **Design choice**: Notice that `safe_divide` returns `None` when division by zero occurs instead
# of crashing. This allows the program to continue running. However, the caller needs to check for
# `None` before using the result. An alternative design would be to let the exception propagate up
# or raise a different exception. Choose based on how you want errors to be handled in your application.


# %%
def read_number_from_user(prompt):
    """
    Safely read a number from user input.

    Parameters
    ----------
    prompt : str
        Prompt to display to user

    Returns
    -------
    float or None
        Converted number, or None if conversion fails
    """
    # For demonstration, we'll simulate user input
    user_input = "42.5"  # In real code: input(prompt)

    try:
        number = float(user_input)
        return number
    except ValueError:
        print(f"Error: '{user_input}' is not a valid number")
        return None


# Simulated test
result = read_number_from_user("Enter a number: ")
print(f"Result: {result}")

# %% [markdown]
# ### Multiple Exception Types
#
# Real-world code often needs to handle multiple types of errors differently. Python allows you
# to specify multiple `except` blocks, each handling a specific exception type. The order matters:
# Python checks exception types from top to bottom, so put more specific exceptions before more
# general ones.
#
# **Exception hierarchy**: Python's exceptions form a hierarchy. `Exception` is a general exception
# that catches most errors. More specific exceptions like `ValueError` or `FileNotFoundError`
# inherit from it. If you catch `Exception` first, you'll never reach the more specific handlers
# below it. This is why we always put the catch-all `Exception` last.


# %%
def process_data_file(filename, column_index):
    """
    Process a data file and extract a column.

    Parameters
    ----------
    filename : str
        Path to data file
    column_index : int
        Index of column to extract

    Returns
    -------
    list
        Extracted column values
    """
    try:
        # Simulate file reading (in reality, we'd read an actual file)
        # For demo, create fake data
        data = [["Sample", "Value", "Units"], ["A", "10.5", "mg"], ["B", "12.3", "mg"], ["C", "9.8", "mg"]]

        # Extract column
        column = [row[column_index] for row in data]
        return column

    except IndexError:
        print(f"Error: Column index {column_index} is out of range")
        return []
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return []
    except PermissionError:
        print(f"Error: No permission to read '{filename}'")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


# Test with different indices
print("Column 0:", process_data_file("data.csv", 0))
print("Column 1:", process_data_file("data.csv", 1))
print("Column 5:", process_data_file("data.csv", 5))  # Out of range

# %% [markdown]
# **Best practice**: The final `except Exception as e:` catches any unexpected errors. The `as e`
# syntax gives you access to the exception object, which you can print for debugging. This catch-all
# is useful for logging unexpected problems in production code, but during development, it's often
# better to let exceptions crash your program so you notice and fix them.
#
# **Common pitfall**: Don't use bare `except:` without specifying the exception type—it will catch
# EVERYTHING, including KeyboardInterrupt (Ctrl+C), making your program hard to stop. Always specify
# the exception types you're catching, or at minimum use `except Exception:` which excludes system-
# level exceptions like KeyboardInterrupt.

# %% [markdown]
# ### Try-Except-Else-Finally
#
# Beyond the basic try-except, Python provides `else` and `finally` clauses for more sophisticated
# error handling. The `else` block runs only if no exception occurred—useful for code that should
# only run on success. The `finally` block always runs, whether an exception occurred or not—perfect
# for cleanup operations like closing files or network connections.
#
# **When to use what**:
# - Use `else` for code that should only run if everything succeeded (e.g., success logging)
# - Use `finally` for cleanup that must happen regardless (e.g., closing files, releasing locks)
# - Common pattern: `try` to open/use a resource, `finally` to close it


# %%
def analyze_file_safely(filename):
    """
    Analyze a file with comprehensive error handling.

    Parameters
    ----------
    filename : str
        Path to file

    Returns
    -------
    dict
        Analysis results
    """
    result = {"status": "unknown", "lines": 0, "words": 0}

    try:
        # Simulate file reading
        content = "This is sample content\nWith multiple lines\nFor testing"

        # Process content
        lines = content.split("\n")
        words = content.split()

        result["lines"] = len(lines)
        result["words"] = len(words)

    except FileNotFoundError:
        result["status"] = "error: file not found"
        print(f"Could not find file: {filename}")

    except Exception as e:
        result["status"] = f"error: {str(e)}"
        print(f"Error processing file: {e}")

    else:
        # Executes if try block succeeds (no exceptions)
        result["status"] = "success"
        print(f"Successfully processed {filename}")

    finally:
        # Always executes, regardless of errors or success
        print(f"Finished processing attempt for {filename}")

    return result


# Test the function
analysis = analyze_file_safely("test.txt")
print(f"Analysis result: {analysis}")

# %% [markdown]
# **Flow control**: The flow is: `try` → if error: `except` → if no error: `else` → always: `finally`.
# This allows fine-grained control: put risky operations in `try`, error handling in `except`,
# success-only operations in `else`, and cleanup in `finally`. In practice, `finally` is most
# commonly used with file I/O to ensure files are closed even if an error occurs.

# %% [markdown]
# ### Raising Exceptions
#
# You can raise your own exceptions for error conditions. This is how you enforce rules in your
# functions and provide clear error messages when something goes wrong. Raising exceptions is
# better than returning error codes or special values (like -1 or None) because:
# 1. It forces the caller to handle the error (can't accidentally ignore it)
# 2. It provides a clear error message
# 3. It automatically stops execution if not handled
#
# **When to raise exceptions**: Raise exceptions when the caller made a mistake (wrong arguments)
# or when a precondition isn't met (file doesn't exist, network is down). Use meaningful exception
# types (`ValueError` for bad values, `FileNotFoundError` for missing files) so callers can handle
# different errors differently.


# %%
def validate_temperature(temp, min_temp=-273.15, max_temp=100):
    """
    Validate a temperature reading.

    Parameters
    ----------
    temp : float
        Temperature in Celsius
    min_temp : float
        Minimum valid temperature (default: -273.15, absolute zero)
    max_temp : float
        Maximum valid temperature (default: 100)

    Returns
    -------
    bool
        True if temperature is valid

    Raises
    ------
    ValueError
        If temperature is outside valid range
    """
    if temp < min_temp:
        raise ValueError(f"Temperature {temp}°C is below absolute zero!")
    if temp > max_temp:
        raise ValueError(f"Temperature {temp}°C exceeds maximum of {max_temp}°C")
    return True


# Test with valid and invalid temperatures
try:
    validate_temperature(25)
    print("25°C is valid")

    validate_temperature(150)
    print("150°C is valid")  # Won't reach here

except ValueError as e:
    print(f"Validation error: {e}")

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Ready to master error handling? Practice makes perfect!</p>
#     <ul>
#         <li><strong>Build a robust calculator:</strong> Create a calculator function that handles division by zero, type
#         errors, and invalid operations with specific error messages for each case.</li>
#         <li><strong>Chain exception handlers:</strong> Write code with multiple except blocks to handle TypeError,
#         ValueError, and FileNotFoundError differently, showing how specific error handling improves user experience.</li>
#         <li><strong>Create custom exceptions:</strong> Design your own exception class (like TemperatureError or
#         DataValidationError) for domain-specific error handling in your research code.</li>
#     </ul>
# </div>

# %% [markdown]
# Now that you understand how to handle errors gracefully, let's apply that knowledge to a critical
# research task: reading and writing data files. Most research involves processing data from files,
# and combining file I/O with proper error handling ensures your data pipelines are robust and
# reliable.

# %% [markdown]
# ## Part 3: File Input/Output
#
# Reading and writing files is essential for research data processing. Whether you're analyzing
# experimental results, processing sensor data, or saving analysis outputs, file I/O is a core
# skill for research software engineers.

# %% [markdown]
# ### Reading Text Files
#
# Python reads files using the built-in `open()` function. The recommended pattern is the
# `with` statement, which automatically closes the file when the block ends—even if an error
# occurs. Text files are typically processed line by line: you skip comment lines or blank
# lines, then parse each data line into the type you need. The example below simulates reading
# a temperature data file by working with a multi-line string that represents the file contents.

# %%
# Writing data to demonstrate reading
sample_data = """# Sample Data File
# Temperature measurements in Celsius
23.5
24.1
23.8
24.3
23.9
24.0
"""

# In real code, you would write to a file:
# with open('temperatures.txt', 'w') as f:
#     f.write(sample_data)


# Simulate reading
def read_temperature_file(content):
    """Read temperatures from file content."""
    temperatures = []

    for line in content.split("\n"):
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith("#"):
            continue

        try:
            temp = float(line)
            temperatures.append(temp)
        except ValueError:
            print(f"Warning: Skipping invalid line: {line}")

    return temperatures


# Process the data
temps = read_temperature_file(sample_data)
print(f"Read {len(temps)} temperature values")
print(f"Temperatures: {temps}")
print(f"Average: {sum(temps) / len(temps):.2f}°C")

# %% [markdown]
# ### Writing Files
#
# Writing files follows the same `with open()` pattern as reading, but you use `'w'` (write)
# mode to create a new file or overwrite an existing one, or `'a'` (append) mode to add to an
# existing file. In the example below, we simulate writing by building the output as a list of
# strings and joining them—in real code you would pass the actual filename to `open()` instead
# of printing the result.


# %%
def save_results(filename, data, metadata=None):
    """
    Save analysis results to a file.

    Parameters
    ----------
    filename : str
        Output file path
    data : dict
        Results to save
    metadata : dict, optional
        Additional metadata to include

    Returns
    -------
    bool
        True if save successful
    """
    try:
        # In real code, open actual file
        # with open(filename, 'w') as f:

        # Simulate file writing
        output = []

        # Write metadata
        if metadata:
            output.append("# Metadata")
            for key, value in metadata.items():
                output.append(f"# {key}: {value}")
            output.append("")

        # Write results
        output.append("# Results")
        for key, value in data.items():
            output.append(f"{key}: {value}")

        content = "\n".join(output)
        print(f"Would write to {filename}:")
        print(content)

        return True

    except Exception as e:
        print(f"Error saving to {filename}: {e}")
        return False


# Test
results = {"mean": 23.93, "std": 0.24, "count": 6}
metadata = {"experiment": "Temperature Study", "date": "2024-01-15"}

save_results("results.txt", results, metadata)

# %% [markdown]
# ### Working with CSV Data
#
# CSV (Comma-Separated Values) is one of the most common file formats for research data.
# Python's built-in `csv` module handles the parsing for you. `csv.DictReader` reads each row
# as a dictionary, using the header row as keys—this is especially convenient because you can
# access columns by name (`row["Temperature"]`) instead of by index. Note that every value from
# a CSV file arrives as a string, so you need to convert numeric fields to `float` or `int`
# yourself, as shown below.

# %%
import csv
from io import StringIO

# Sample CSV data
csv_data = """Sample,Temperature,Humidity,Valid
A,23.5,65.2,True
B,24.1,64.8,True
C,23.8,66.1,True
D,25.2,63.5,False
E,23.9,65.8,True
"""


def read_csv_data(csv_content):
    """
    Read CSV data and return as list of dictionaries.

    Parameters
    ----------
    csv_content : str
        CSV content to parse

    Returns
    -------
    list of dict
        Parsed data
    """
    data = []
    csv_file = StringIO(csv_content)
    reader = csv.DictReader(csv_file)

    for row in reader:
        # Convert numeric fields
        try:
            row["Temperature"] = float(row["Temperature"])
            row["Humidity"] = float(row["Humidity"])
            row["Valid"] = row["Valid"] == "True"
        except (ValueError, KeyError) as e:
            print(f"Warning: Error processing row: {e}")
            continue

        data.append(row)

    return data


# Parse the data
measurements = read_csv_data(csv_data)
print(f"Read {len(measurements)} measurements")

# Filter valid measurements
valid_temps = [m["Temperature"] for m in measurements if m["Valid"]]
print(f"\nValid temperatures: {valid_temps}")
print(f"Average valid temperature: {sum(valid_temps) / len(valid_temps):.2f}°C")

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>File I/O is where theory meets practice—explore real data scenarios!</p>
#     <ul>
#         <li><strong>Build a data pipeline:</strong> Process a real CSV file from your research (or a public dataset),
#         validate each row, and write only the clean data to a new file with summary statistics.</li>
#         <li><strong>Handle messy data gracefully:</strong> Create a CSV reader that skips malformed rows, logs warnings
#         for questionable values, and generates a quality report showing what percentage of data was usable.</li>
#         <li><strong>Implement data versioning:</strong> Write functions that save processed data with timestamps and
#         metadata (processing date, filters applied, source file) so you can track data provenance.</li>
#     </ul>
# </div>

# %% [markdown]
# With solid foundations in functions, error handling, and file I/O, let's explore some of Python's
# elegant features that make code more concise and readable. List comprehensions are a Pythonic way
# to transform and filter data, making your research code both more expressive and often faster.

# %% [markdown]
# ## Part 4: List Comprehensions
#
# List comprehensions provide elegant, concise ways to create and transform lists. They're not just
# syntactic sugar—they're often faster than traditional loops and make your code's intent clearer.
# In research contexts, you'll use them constantly for data filtering, transformation, and processing.
#
# The basic syntax is: `[expression for item in iterable]`. You read this as "for each item in the
# iterable, compute the expression and collect the results into a list". Compare the traditional
# loop approach with the comprehension below to see how much more compact the syntax is.

# %%
# Traditional approach
squares = []
for i in range(10):
    squares.append(i**2)
print(f"Traditional: {squares}")

# List comprehension
squares_comp = [i**2 for i in range(10)]
print(f"Comprehension: {squares_comp}")

# %% [markdown]
# ### Filtering with List Comprehensions
#
# You can add an `if` clause to a list comprehension to keep only the items that satisfy a
# condition. The extended syntax is: `[expression for item in iterable if condition]`. This
# replaces the pattern of looping and conditionally appending—all in one readable line.

# %%
# Filtering with list comprehensions
temperatures = [23.5, 24.1, 26.8, 24.3, 27.1, 23.9, 25.5]

# Only temperatures above 25°C
high_temps = [t for t in temperatures if t > 25]
print(f"High temperatures: {high_temps}")

# Convert to Fahrenheit
temps_f = [t * 9 / 5 + 32 for t in temperatures]
print(f"Fahrenheit: {temps_f}")

# Combined: convert high temps to Fahrenheit
high_temps_f = [t * 9 / 5 + 32 for t in temperatures if t > 25]
print(f"High temps in Fahrenheit: {high_temps_f}")

# %% [markdown]
# ### Nested List Comprehensions
#
# You can iterate over multiple sequences in one comprehension by chaining `for` clauses. This
# is useful for working with matrices (lists of lists) or for creating all combinations of two
# sequences. Read the nested comprehension left to right: the outer `for` iterates over rows
# and the inner `for` iterates over the numbers in each row.

# %%
# Nested list comprehensions
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Flatten matrix
flattened = [num for row in matrix for num in row]
print(f"Flattened: {flattened}")

# Get diagonal
diagonal = [matrix[i][i] for i in range(len(matrix))]
print(f"Diagonal: {diagonal}")

# %% [markdown]
# ### Dictionary Comprehensions
#
# Just like list comprehensions build lists, **dictionary comprehensions** build dictionaries.
# The syntax is `{key: value for item in iterable}`. They're especially convenient when you want
# to pair up two lists into a mapping.
#
# The `zip()` function is used below to pair two lists together element by element:
# `zip(["A", "B"], [1, 2])` produces `[("A", 1), ("B", 2)]`. You can then unpack each pair
# in the comprehension using `for key, value in zip(...)`.

# %%
# Dictionary comprehensions
samples = ["A", "B", "C", "D", "E"]
temperatures = [23.5, 24.1, 23.8, 24.3, 23.9]

# Create dictionary
temp_dict = {sample: temp for sample, temp in zip(samples, temperatures)}
print(f"Temperature dictionary: {temp_dict}")

# Filter dictionary
high_temp_dict = {s: t for s, t in temp_dict.items() if t > 24.0}
print(f"High temperatures: {high_temp_dict}")

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>List comprehensions unlock functional programming—discover the elegance!</p>
#     <ul>
#         <li><strong>Refactor loops to comprehensions:</strong> Take existing code with
#         nested for-loops and multiple if statements and rewrite it as concise list/dict
#         comprehensions—see how readability improves.</li>
#         <li><strong>Chain transformations:</strong> Process data in multiple steps—first filter
#         a list of measurements using an <code>if</code> clause, then transform the remaining
#         values (e.g., convert Celsius to Fahrenheit)—and verify the result matches a
#         traditional loop approach.</li>
#         <li><strong>Combine list and dict comprehensions:</strong> Given a list of sample names
#         and a list of temperature readings, use <code>zip()</code> and a dict comprehension to
#         create a mapping from sample name to temperature, then filter the dictionary to keep
#         only samples above a threshold value.</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 5: Command-Line Scripts with argparse
#
# When you write a Python script that others will run from the command line, you need a way for
# users to pass options and file names to it. The standard library module `argparse` handles this
# for you. You declare what arguments your script accepts (positional arguments, optional flags,
# typed values), and `argparse` automatically parses `sys.argv`, validates the input, and
# generates a `--help` message. This makes your scripts behave like professional Unix tools.
#
# The typical pattern is: create a parser, add arguments with `add_argument()`, then call
# `parse_args()` to get an object whose attributes are the argument values.

# %%
import argparse


def create_parser():
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Analyze experimental data from a file.",
        epilog="Example: python analyze.py data.txt -o results.txt --threshold 25",
    )

    # Positional arguments
    parser.add_argument("input_file", help="Input data file path")

    # Optional arguments
    parser.add_argument("-o", "--output", help="Output file path (default: results.txt)", default="results.txt")

    parser.add_argument("-t", "--threshold", type=float, help="Temperature threshold in Celsius (default: 25.0)", default=25.0)

    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output")

    parser.add_argument("--method", choices=["mean", "median"], default="mean", help="Analysis method (default: mean)")

    return parser


# Simulate command-line arguments (in real script, argparse reads from sys.argv)
# Example: python script.py data.txt -o output.txt -t 24.5 -v
print("Example argument parser created")
print("\nParser help:")
parser = create_parser()
parser.print_help()

# %% [markdown]
# ### Complete Command-Line Script Example


# %%
def analyze_temperature_data(input_file, output_file="results.txt", threshold=25.0, method="mean", verbose=False):
    """
    Analyze temperature data from a file.

    Parameters
    ----------
    input_file : str
        Path to input file
    output_file : str
        Path to output file
    threshold : float
        Temperature threshold for filtering
    method : str
        Analysis method ('mean' or 'median')
    verbose : bool
        Whether to print detailed output

    Returns
    -------
    dict
        Analysis results
    """
    if verbose:
        print(f"Reading data from {input_file}")

    # Simulate reading data
    temperatures = [23.5, 24.1, 26.8, 24.3, 27.1, 23.9, 25.5]

    if verbose:
        print(f"Loaded {len(temperatures)} temperature readings")

    # Filter by threshold
    filtered = [t for t in temperatures if t >= threshold]

    if verbose:
        print(f"After filtering (>= {threshold}°C): {len(filtered)} readings")

    # Calculate statistic
    if method == "mean":
        result = sum(filtered) / len(filtered) if filtered else 0
    else:  # median
        sorted_temps = sorted(filtered)
        n = len(sorted_temps)
        if n == 0:
            result = 0
        elif n % 2 == 0:
            result = (sorted_temps[n // 2 - 1] + sorted_temps[n // 2]) / 2
        else:
            result = sorted_temps[n // 2]

    # Prepare results
    results = {
        "method": method,
        "threshold": threshold,
        "total_readings": len(temperatures),
        "filtered_readings": len(filtered),
        "result": result,
    }

    if verbose:
        print(f"Analysis complete: {method} = {result:.2f}°C")
        print(f"Saving results to {output_file}")

    return results


# Simulated script execution
results = analyze_temperature_data(
    "temperatures.txt", output_file="analysis_results.txt", threshold=24.5, method="mean", verbose=True
)

print(f"\nFinal results: {results}")

# %% [markdown]
# ## Part 6: Classes and Object-Oriented Programming
#
# Classes allow you to bundle data and functionality together. They're essential for organizing
# complex research code and are heavily used in testing frameworks like pytest (which we'll see
# in Lecture 5).
#
# ### Why Use Classes?
#
# - **Organization**: Group related data and functions together
# - **Reusability**: Create multiple instances with the same behavior
# - **Clarity**: Model real-world entities (experiments, datasets, instruments)
# - **Testing**: Organize test cases (test classes in pytest)

# %% [markdown]
# ### Basic Class Syntax


# %%
class TemperatureData:
    """Store and analyze temperature measurements."""

    def __init__(self, location, unit="celsius"):
        """
        Initialize temperature data.

        Parameters
        ----------
        location : str
            Measurement location
        unit : str, optional
            Temperature unit ('celsius' or 'fahrenheit')
        """
        self.location = location
        self.unit = unit
        self.measurements = []

    def add_measurement(self, temperature):
        """Add a temperature reading."""
        self.measurements.append(temperature)

    def get_average(self):
        """Calculate average temperature."""
        if not self.measurements:
            return None
        return sum(self.measurements) / len(self.measurements)

    def get_summary(self):
        """Return a summary string."""
        avg = self.get_average()
        if avg is None:
            return f"{self.location}: No measurements"
        return f"{self.location}: {len(self.measurements)} measurements, avg={avg:.1f}°{self.unit[0].upper()}"


# Create an instance of the class
lab_temps = TemperatureData("Lab A", unit="celsius")

# Add measurements
lab_temps.add_measurement(23.5)
lab_temps.add_measurement(24.1)
lab_temps.add_measurement(23.8)

# Use methods
print(lab_temps.get_summary())
print(f"Average: {lab_temps.get_average():.2f}°C")

# %% [markdown]
# ### Understanding `self` and `__init__`
#
# - **`__init__`**: Special method called when creating a new instance (constructor)
# - **`self`**: Refers to the instance itself (like "this" in other languages)
# - **Instance variables**: `self.location`, `self.measurements` belong to each instance
# - **Methods**: Functions defined inside a class that operate on instance data

# %% [markdown]
# ### Multiple Instances

# %%
# Create multiple independent instances
lab_a = TemperatureData("Lab A")
lab_b = TemperatureData("Lab B")
outdoor = TemperatureData("Outdoor")

# Each has its own data
lab_a.add_measurement(23.5)
lab_a.add_measurement(24.1)

lab_b.add_measurement(22.1)
lab_b.add_measurement(22.3)
lab_b.add_measurement(22.0)

outdoor.add_measurement(15.2)
outdoor.add_measurement(16.8)

# Display summaries
for location in [lab_a, lab_b, outdoor]:
    print(location.get_summary())

# %% [markdown]
# ### Classes in Testing (Preview of Lecture 5)
#
# In Lecture 5, you'll use test classes with pytest. Here's a preview of what that looks like:
#
# ```python
# class TestTemperatureConversion:
#     """Group related temperature conversion tests."""
#
#     def test_freezing_point(self):
#         """Water freezes at 0°C = 32°F."""
#         assert celsius_to_fahrenheit(0) == 32
#
#     def test_boiling_point(self):
#         """Water boils at 100°C = 212°F."""
#         assert celsius_to_fahrenheit(100) == 212
# ```
#
# Test classes organize related tests together. Each method starting with `test_` is a separate test case.

# %% [markdown]
# ### When to Use Classes vs Functions
#
# **Use classes when you need to:**
# - Store state (data) and behavior (methods) together
# - Create multiple instances of similar objects
# - Organize complex code into logical units
# - Build test suites (test classes)
#
# **Use functions when you:**
# - Have a simple operation that doesn't need state
# - Want to transform inputs to outputs
# - Need something quick and straightforward
#
# **Research example**: A function is good for calculating mean temperature. A class is better
# for representing an entire experiment with settings, data, and multiple analysis methods.

# %% [markdown]
# ## Summary
#
# In this lecture, we covered:
#
# ### Advanced Functions
# - **Parameters**: Default values, keyword arguments, *args and **kwargs
# - **Lambda functions**: Anonymous functions for simple operations
# - **Documentation**: Writing comprehensive docstrings
#
# ### Error Handling
# - **Exception types**: Common errors in Python
# - **Try-except blocks**: Catching and handling errors
# - **Error recovery**: Graceful degradation
# - **Raising exceptions**: Signaling error conditions
#
# ### File I/O
# - **Reading files**: Text files and CSV data
# - **Writing files**: Saving results and reports
# - **Error handling**: Safe file operations
#
# ### Advanced Python Techniques
# - **List comprehensions**: Concise list creation and filtering
# - **Dictionary comprehensions**: Creating dictionaries elegantly
# - **Command-line arguments**: Using argparse for CLI tools
# - **Classes and OOP**: Organizing code with classes, methods, and instances

# %% [markdown]
# ## Acknowledgements and References
#
# This lecture synthesizes best practices from established Python education resources:
#
# ### Primary Sources
#
# - **Research Software Engineering with Python** by The Alan Turing Institute
#   <https://alan-turing-institute.github.io/rse-course/html/>
#   Advanced Python concepts, error handling patterns, and object-oriented programming approaches adapted from this course.
#
# - **Research Software Engineering with Python** by Damien Irving, Kate Hertweck,
#   Luke Johnston, Joel Ostblom, Charlotte Wickham, and Greg Wilson (2022)
#   <https://third-bit.com/py-rse/>
#   Defensive programming practices, error handling strategies, and file I/O
#   patterns informed by this textbook.
#
# ### Documentation
#
# - **Python Documentation**
#   <https://docs.python.org/3/>
#   - Built-in Exceptions: <https://docs.python.org/3/library/exceptions.html>
#   - File I/O: <https://docs.python.org/3/tutorial/inputoutput.html>
#   - argparse: <https://docs.python.org/3/library/argparse.html>
#   - Classes and OOP: <https://docs.python.org/3/tutorial/classes.html>
#
# - **NumPy Docstring Style Guide**
#   <https://numpydoc.readthedocs.io/en/latest/format.html>
#   Documentation standards used in function docstrings throughout this lecture.
#
# ### Notes
#
# All code examples and exercises have been developed specifically for this course to illustrate
# key concepts in research software contexts. The pedagogical approach draws on best practices
# from the sources cited above.

# %% [markdown]
# ### Next Steps
#
# In Lecture 4, we'll learn how to structure Python projects properly and work with
# powerful libraries like NumPy and Matplotlib for scientific computing and visualization.
#
# **Ready to continue? Move on to Lecture 4: Python Project Structure and Libraries!**

# %%
