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
# # Lecture 5: Testing Research Software
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
#     <img src="lecture_05_qr_code.png" alt="This Lecture QR Code" width="150"/>
#     <p><strong>This Lecture</strong></p>
#   </div>
# </div>
#
# ## Overview
# This lecture introduces software testing practices essential for reliable research software.
# We'll follow a cautionary tale of a research project that produced incorrect results due to
# untested code, then learn how to prevent such disasters through systematic testing.
#
# **Duration**: ~90 minutes
#
# ## Prerequisites
#
# Before starting this lecture, you should be familiar with:
# - Writing Python functions and classes (covered in Lectures 2-4)
# - Python project structure and modules
# - Basic use of the command line for running Python scripts
# - NumPy arrays and basic scientific computing (covered in Lecture 4)
# - AI-assisted coding basics, including reviewing AI suggestions like a diff (covered in
#   Lecture 3)
#
# This lecture builds on your Python programming skills and introduces testing methodologies.
#
# ## Learning Objectives
# - Understand why testing is critical for research software
# - Write unit tests using pytest
# - Organize related tests using pytest test classes
# - Use assertions for defensive programming
# - Measure test coverage
# - Apply test-driven development (TDD) principles
# - Build confidence in research results through comprehensive testing
# - Critically evaluate whether an AI-generated test actually verifies correct behavior

# %% [markdown]
# ## Part 1: A Cautionary Tale - The Temperature Conversion Disaster
#
# ### The Story
#
# In 2020, a climate research team published a groundbreaking paper suggesting unexpected warming
# patterns in the Arctic. The paper received significant media attention and influenced policy
# discussions. Six months later, another team tried to reproduce the results and discovered a
# critical bug: **the temperature conversion function had a subtle error**.
#
# The original team had to retract their paper. Years of work were lost. Careers were damaged.
# Policy decisions made based on the flawed data had to be reversed. All because of a simple,
# untested function.
#
# ### The Flawed Code
#
# Let's look at the type of code that caused this disaster:


# %%
def celsius_to_fahrenheit(celsius):
    """Convert temperature from Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    """Convert temperature from Fahrenheit to Celsius."""
    # BUG: This should be (fahrenheit - 32) * 5 / 9
    return (fahrenheit - 32) * 9 / 5  # Wrong formula!


def calculate_temperature_anomaly(temperatures_f, baseline_f):
    """
    Calculate temperature anomaly relative to baseline.

    Parameters
    ----------
    temperatures_f : list
        List of temperatures in Fahrenheit
    baseline_f : float
        Baseline temperature in Fahrenheit

    Returns
    -------
    list
        Temperature anomalies in Celsius
    """
    anomalies = []
    for temp in temperatures_f:
        # Convert to Celsius
        temp_c = fahrenheit_to_celsius(temp)
        baseline_c = fahrenheit_to_celsius(baseline_f)
        # Calculate anomaly
        anomaly = temp_c - baseline_c
        anomalies.append(anomaly)
    return anomalies


# Let's use this function with real-looking data
observed_temps = [32.5, 33.0, 34.2, 35.1, 33.8]
baseline_temp = 32.0

anomalies = calculate_temperature_anomaly(observed_temps, baseline_temp)
print(f"Temperature anomalies: {anomalies}")
print(f"Average anomaly: {sum(anomalies) / len(anomalies):.2f}°C")

# %% [markdown]
# ### What Went Wrong?
#
# The bug in `fahrenheit_to_celsius` multiplies by 9/5 instead of 5/9. This error:
#
# 1. **Wasn't immediately obvious** - the function still returns numbers
# 2. **Wasn't caught during development** - no tests were written
# 3. **Wasn't caught during review** - reviewers didn't verify the formula
# 4. **Produced plausible-looking results** - the values seemed reasonable at first glance
# 5. **Compounded through the analysis** - every calculation using this function was wrong
#
# This is exactly the kind of error that **testing prevents**. Let's see how.

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>The best way to learn testing is to catch real bugs—let's hunt!</p>
#     <ul>
#         <li><strong>Write tests that catch the disaster:</strong> Before looking at the
#         solution, write comprehensive tests for the buggy fahrenheit_to_celsius
#         function—see if you can create a test suite that would have caught the bug before
#         publication.</li>
#         <li><strong>Test your own research code:</strong> Pick a critical function from
#         your current project and write 3-5 tests for it—edge cases, typical inputs, and
#         error conditions. You might discover bugs you didn't know existed!</li>
#         <li><strong>Practice test-first thinking:</strong> Choose a new small feature you
#         need and write the tests BEFORE implementing it—experience how tests clarify
#         requirements and guide design.</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 2: Introduction to Testing
#
# ### Why Test Research Software?
#
# Research software is often perceived as "write once, run once" code that doesn't need testing.
# This is a dangerous misconception. In reality, research code is modified constantly, used with
# different datasets, and often reused in future projects. Without tests, every change is a potential
# source of bugs that can silently corrupt your results.
#
# **Research is iterative**: You'll run and modify your code many times as you refine your analysis
# - **Data changes**: New data might expose edge cases your code doesn't handle
# - **Collaborators need confidence**: Others must trust your results to build on them
# - **You might be wrong**: Even experts make mistakes (as our story shows)—tests catch them
# - **Future you needs help**: You'll forget the implementation details in 6 months; tests document behavior
# - **Journals increasingly require it**: Many publishers now expect code and tests to be available
#
# **Testing mindset**: Think of tests as "documentation that runs." They show how your code is
# supposed to work and prove that it does. Good tests make refactoring safe—you can improve your
# code's implementation without breaking its behavior.
#
# ### Real-World Research Software Failures
#
# Our story is fictional, but based on real incidents:
#
# 1. **Geoffrey Chang (2006)**: Retracted 5 papers from *Science* due to a data column flip
# 2. **Reinhart-Rogoff (2010)**: Excel error affected global economic policy
# 3. **Mars Climate Orbiter (1999)**: $327M loss due to unit conversion error
# 4. **Ariane 5 (1996)**: $370M rocket destroyed by integer overflow
#
# ### Types of Testing
#
# Testing comes in different forms, each serving a specific purpose:
#
# - **Unit tests**: Test individual functions in isolation—does this one function work correctly?
# - **Integration tests**: Test how components work together—do these functions interact properly?
# - **Regression tests**: Ensure bugs don't come back—once fixed, stay fixed
# - **Acceptance tests**: Verify the software meets requirements—does it solve the right problem?
#
# Today we focus on **unit tests**—the foundation of testing. Unit tests are small, fast, and test
# one specific piece of functionality. They're the most common type of test and the easiest to write.
#
# **Testing pyramid**: Most projects should have many unit tests (fast, easy to write), fewer
# integration tests (slower, test interactions), and a few acceptance tests (slowest, test whole
# system). Start with unit tests—they give you the most value for the least effort.
#
# <img src="figures/testing_pyramid.svg" alt="Testing pyramid: many fast unit tests at the base, fewer integration tests, and few slow acceptance tests at the top" width="600"/>
#
# *The pyramid shape is the point: the cheaper and faster a test is to write and run, the
# more of them you should have. Regression tests aren't a separate layer—they apply at
# every level, re-checking that a fixed bug stays fixed.*

# %% [markdown]
# ## Part 3: Writing Your First Test
#
# ### Manual Testing (What NOT to Do)
#
# Before learning proper testing, let's see what manual testing looks like:

# %%
# Manual testing - fragile and non-repeatable
print("Testing celsius_to_fahrenheit...")
result = celsius_to_fahrenheit(0)
if result == 32:
    print("✓ Freezing point test passed")
else:
    print(f"✗ Freezing point test FAILED: expected 32, got {result}")

result = celsius_to_fahrenheit(100)
if result == 212:
    print("✓ Boiling point test passed")
else:
    print(f"✗ Boiling point test FAILED: expected 212, got {result}")

# %% [markdown]
# ### Problems with Manual Testing
#
# 1. **Not automated**: You must run it manually every time—easy to forget or skip
# 2. **Not organized**: Tests scattered throughout code—hard to maintain
# 3. **Not comprehensive**: Easy to forget edge cases—what about negative numbers? zero? infinity?
# 4. **Not persistent**: Tests lost when cells are re-run—no record of what was tested
# 5. **No clear pass/fail**: Must interpret output yourself—did all tests pass?
#
# **Why this matters**: Manual testing is how bugs slip through. You test the happy path (normal
# inputs) but forget edge cases. You test once but don't re-test after changes. You test locally
# but not on different systems. Automated testing solves all these problems.
#
# %% [markdown]
# ### Using pytest - The Right Way
#
# `pytest` is Python's most popular testing framework. It makes testing easy and automatic. Unlike
# manual testing, pytest discovers and runs all your tests automatically, provides clear pass/fail
# output, and integrates with CI/CD systems.
#
# **Why pytest over alternatives?**:
# - **Simple**: Just write functions starting with `test_` and use `assert`
# - **Powerful**: Advanced features like fixtures and parametrization when you need them
# - **Fast**: Runs tests in parallel and caches results
# - **Popular**: Huge ecosystem of plugins and community support
#
# **Best practice**: Keep test files separate from source code. Put them in a `tests/` directory with
# names like `test_module.py`. This keeps your source code clean and makes tests easy to find.

# %%
# First, let's write tests in a format pytest can discover
# In practice, these would be in a separate file: test_temperature.py


def test_celsius_to_fahrenheit_freezing():
    """Test conversion at water freezing point."""
    assert celsius_to_fahrenheit(0) == 32


def test_celsius_to_fahrenheit_boiling():
    """Test conversion at water boiling point."""
    assert celsius_to_fahrenheit(100) == 212


def test_celsius_to_fahrenheit_negative():
    """Test conversion with negative temperature."""
    assert celsius_to_fahrenheit(-40) == -40  # -40°C = -40°F


# Run the tests
print("Running manual test execution:")
try:
    test_celsius_to_fahrenheit_freezing()
    print("✓ Freezing point test passed")
except AssertionError as e:
    print(f"✗ Freezing point test FAILED: {e}")

try:
    test_celsius_to_fahrenheit_boiling()
    print("✓ Boiling point test passed")
except AssertionError as e:
    print(f"✗ Boiling point test FAILED: {e}")

try:
    test_celsius_to_fahrenheit_negative()
    print("✓ Negative temperature test passed")
except AssertionError as e:
    print(f"✗ Negative temperature test FAILED: {e}")

# %% [markdown]
# ### Understanding Assertions
#
# An **assertion** is a statement that must be true. If it's false, Python raises an `AssertionError`.
#
# ```python
# assert condition, "Optional error message"
# ```
#
# **Good assertions are:**
# - Clear: Easy to understand what's being tested
# - Specific: Test one thing at a time
# - Meaningful: Include helpful error messages
#
# **Common assertion patterns:**


# %%
def test_assertion_patterns():
    """Demonstrate common assertion patterns."""

    # Equality
    assert celsius_to_fahrenheit(0) == 32

    # Approximate equality (for floating point)
    result = celsius_to_fahrenheit(37)
    expected = 98.6
    assert abs(result - expected) < 0.01, f"Expected {expected}, got {result}"

    # Type checking
    result = celsius_to_fahrenheit(0)
    assert isinstance(result, (int, float)), f"Expected numeric type, got {type(result)}"

    # Range checking
    result = celsius_to_fahrenheit(20)
    assert 60 < result < 80, f"Room temperature should be 60-80°F, got {result}"

    print("All assertion patterns demonstrated successfully!")


test_assertion_patterns()

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Coverage is your safety net—aim for comprehensive test suites!</p>
#     <ul>
#         <li><strong>Measure your test coverage:</strong> Run pytest with --cov on your research code and aim for >80%
#         coverage—identify untested code paths and write tests for them.</li>
#         <li><strong>Find the gaps:</strong> Use coverage reports to discover edge cases
#         you missed—what happens with empty inputs, negative numbers, None values, or
#         extremely large datasets?</li>
#         <li><strong>Test the error paths:</strong> Many codebases test only the "happy path"—write tests that intentionally
#         trigger errors, validate error messages, and ensure cleanup happens even when things fail.</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 4: Testing the Buggy Code
#
# Now let's write tests for our flawed `fahrenheit_to_celsius` function.
# **These tests will FAIL** - which is exactly what we want! They'll catch the bug.


# %%
def test_fahrenheit_to_celsius_freezing():
    """Test conversion at water freezing point."""
    result = fahrenheit_to_celsius(32)
    expected = 0
    assert abs(result - expected) < 0.01, f"32°F should be 0°C, got {result}°C"


def test_fahrenheit_to_celsius_boiling():
    """Test conversion at water boiling point."""
    result = fahrenheit_to_celsius(212)
    expected = 100
    assert abs(result - expected) < 0.01, f"212°F should be 100°C, got {result}°C"


def test_fahrenheit_to_celsius_negative():
    """Test conversion with negative temperature."""
    result = fahrenheit_to_celsius(-40)
    expected = -40
    assert abs(result - expected) < 0.01, f"-40°F should be -40°C, got {result}°C"


# Run the tests and see them FAIL (revealing the bug!)
print("Testing the BUGGY fahrenheit_to_celsius function:\n")

tests = [
    ("Freezing point", test_fahrenheit_to_celsius_freezing),
    ("Boiling point", test_fahrenheit_to_celsius_boiling),
    ("Negative temp", test_fahrenheit_to_celsius_negative),
]

for name, test_func in tests:
    try:
        test_func()
        print(f"✓ {name} test passed")
    except AssertionError as e:
        print(f"✗ {name} test FAILED: {e}")

# %% [markdown]
# ### The Bug is Exposed!
#
# The tests fail because our `fahrenheit_to_celsius` function is wrong. This is **good**!
# The tests are doing their job: **catching bugs before they cause problems**.
#
# Now let's fix the bug:


# %%
def fahrenheit_to_celsius_fixed(fahrenheit):
    """Convert temperature from Fahrenheit to Celsius (CORRECTED)."""
    return (fahrenheit - 32) * 5 / 9  # Correct formula!


# Update our test functions to use the fixed version
def test_fahrenheit_to_celsius_fixed_freezing():
    """Test conversion at water freezing point."""
    result = fahrenheit_to_celsius_fixed(32)
    expected = 0
    assert abs(result - expected) < 0.01, f"32°F should be 0°C, got {result}°C"


def test_fahrenheit_to_celsius_fixed_boiling():
    """Test conversion at water boiling point."""
    result = fahrenheit_to_celsius_fixed(212)
    expected = 100
    assert abs(result - expected) < 0.01, f"212°F should be 100°C, got {result}°C"


def test_fahrenheit_to_celsius_fixed_negative():
    """Test conversion with negative temperature."""
    result = fahrenheit_to_celsius_fixed(-40)
    expected = -40
    assert abs(result - expected) < 0.01, f"-40°F should be -40°C, got {result}°C"


# Run the tests on the FIXED function
print("Testing the FIXED fahrenheit_to_celsius function:\n")

tests_fixed = [
    ("Freezing point", test_fahrenheit_to_celsius_fixed_freezing),
    ("Boiling point", test_fahrenheit_to_celsius_fixed_boiling),
    ("Negative temp", test_fahrenheit_to_celsius_fixed_negative),
]

for name, test_func in tests_fixed:
    try:
        test_func()
        print(f"✓ {name} test passed")
    except AssertionError as e:
        print(f"✗ {name} test FAILED: {e}")

# %% [markdown]
# ## Part 5: Organizing Tests with pytest
#
# ### Test File Structure
#
# In real projects, tests live in separate files following a specific structure:
#
# ```
# my_project/
# ├── src/
# │   └── temperature.py       # Main code
# ├── tests/
# │   ├── __init__.py
# │   └── test_temperature.py  # Tests
# └── README.md
# ```
#
# **Naming conventions:**
# - Test files: `test_*.py` or `*_test.py`
# - Test functions: `test_*()`
# - Test classes: `Test*`
#
# pytest automatically discovers tests following these patterns.

# %% [markdown]
# ### Organizing Tests with Classes
#
# So far, every test has been a standalone function. Once a test file grows, it helps to group
# related tests together—pytest supports this with test classes. You already know the syntax
# from Lecture 2 (`class`, `__init__`, `self`); pytest test classes use the same mechanics, just
# with methods named `test_*` instead of a meaningful `__init__`.
#
# **Why group tests into a class?**
# - **Organization**: all tests for `celsius_to_fahrenheit` live in one place, separate from tests
#   for `fahrenheit_to_celsius`
# - **Discovery**: pytest finds classes named `Test*` automatically, just like it finds functions
#   named `test_*`
# - **Shared setup**: a class can define `setup_method()`, which runs before every test in
#   it—useful when several tests need the same starting data (more on this with fixtures, later)


# %%
class TestCelsiusToFahrenheit:
    """Group all tests related to celsius_to_fahrenheit together."""

    def test_freezing_point(self):
        """Water freezes at 0°C = 32°F."""
        assert celsius_to_fahrenheit(0) == 32

    def test_boiling_point(self):
        """Water boils at 100°C = 212°F."""
        assert celsius_to_fahrenheit(100) == 212

    def test_negative_temperature(self):
        """Test with negative temperature."""
        assert celsius_to_fahrenheit(-40) == -40


# Run the class-based tests manually, the same way we ran the function-based tests above
print("Running TestCelsiusToFahrenheit:")
test_instance = TestCelsiusToFahrenheit()
for method_name in ["test_freezing_point", "test_boiling_point", "test_negative_temperature"]:
    try:
        getattr(test_instance, method_name)()
        print(f"✓ {method_name} passed")
    except AssertionError as e:
        print(f"✗ {method_name} FAILED: {e}")

# %% [markdown]
# **Note**: pytest instantiates the test class and calls each `test_*` method for you
# automatically—the manual loop above just shows what pytest does behind the scenes, the same way
# we manually ran function-based tests earlier in this lecture.

# %% [markdown]
# ### Creating a Test File
#
# Let's create a proper test file for our temperature module. Notice that the
# `TestCelsiusToFahrenheit` class below follows exactly the pattern you just ran above:

# %%
# This represents the content of: tests/test_temperature.py

test_file_content = '''"""
Tests for temperature conversion functions.

This module contains unit tests for temperature conversion
between Celsius and Fahrenheit scales.
"""

def celsius_to_fahrenheit(celsius):
    """Convert temperature from Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    """Convert temperature from Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5 / 9


class TestCelsiusToFahrenheit:
    """Tests for celsius_to_fahrenheit function."""
    
    def test_freezing_point(self):
        """Water freezes at 0°C = 32°F."""
        assert celsius_to_fahrenheit(0) == 32
    
    def test_boiling_point(self):
        """Water boils at 100°C = 212°F."""
        assert celsius_to_fahrenheit(100) == 212
    
    def test_body_temperature(self):
        """Normal body temperature: 37°C ≈ 98.6°F."""
        result = celsius_to_fahrenheit(37)
        assert abs(result - 98.6) < 0.1
    
    def test_absolute_zero(self):
        """Absolute zero: -273.15°C = -459.67°F."""
        result = celsius_to_fahrenheit(-273.15)
        assert abs(result - (-459.67)) < 0.1
    
    def test_negative_temperature(self):
        """Test with negative temperature."""
        assert celsius_to_fahrenheit(-40) == -40


class TestFahrenheitToCelsius:
    """Tests for fahrenheit_to_celsius function."""
    
    def test_freezing_point(self):
        """Water freezes at 32°F = 0°C."""
        assert fahrenheit_to_celsius(32) == 0
    
    def test_boiling_point(self):
        """Water boils at 212°F = 100°C."""
        assert fahrenheit_to_celsius(212) == 100
    
    def test_body_temperature(self):
        """Normal body temperature: 98.6°F ≈ 37°C."""
        result = fahrenheit_to_celsius(98.6)
        assert abs(result - 37) < 0.1
    
    def test_negative_temperature(self):
        """Test with negative temperature."""
        assert fahrenheit_to_celsius(-40) == -40
    
    def test_roundtrip_conversion(self):
        """Converting C->F->C should give original value."""
        original = 25
        fahrenheit = celsius_to_fahrenheit(original)
        back_to_celsius = fahrenheit_to_celsius(fahrenheit)
        assert abs(back_to_celsius - original) < 0.01
'''

print("Example test file created:")
print("=" * 60)
print(test_file_content)

# %% [markdown]
# ### Running Tests with pytest
#
# To run tests with pytest, use the command line:
#
# ```bash
# # Run all tests
# pytest
#
# # Run tests in a specific file
# pytest tests/test_temperature.py
#
# # Run tests matching a pattern
# pytest -k "freezing"
#
# # Run with verbose output
# pytest -v
#
# # Run and show print statements
# pytest -s
#
# # Run and stop at first failure
# pytest -x
# ```
#
# **Pytest output shows:**
# - Number of tests run
# - Which tests passed/failed
# - Detailed failure information
# - Execution time

# %% [markdown]
# ## Part 6: Test-Driven Development (TDD)
#
# ### The TDD Cycle: Red-Green-Refactor
#
# Test-Driven Development follows a simple cycle:
#
# 1. **Red**: Write a test that fails (because feature doesn't exist yet)
# 2. **Green**: Write minimal code to make the test pass
# 3. **Refactor**: Improve the code while keeping tests passing
# 4. **Repeat**: Add next test
#
# ### TDD Example: Temperature Statistics
#
# Let's use TDD to build a function that calculates temperature statistics:

# %%
# STEP 1 (RED): Write the test FIRST (it will fail)


def test_temperature_statistics_mean():
    """Test mean temperature calculation."""
    temps = [0, 10, 20, 30, 40]
    stats = temperature_statistics(temps)
    assert abs(stats["mean"] - 20) < 0.01


# STEP 2 (GREEN): Write minimal code to pass the test


def temperature_statistics(temperatures):
    """Calculate statistics for a list of temperatures."""
    return {"mean": sum(temperatures) / len(temperatures)}


# Verify the test passes
try:
    test_temperature_statistics_mean()
    print("✓ Mean temperature test passed")
except (AssertionError, NameError) as e:
    print(f"✗ Mean temperature test failed: {e}")

# %% [markdown]
# ### Adding More Features with TDD

# %%
# STEP 1 (RED): Add test for standard deviation


def test_temperature_statistics_std():
    """Test standard deviation calculation."""
    temps = [0, 10, 20, 30, 40]
    stats = temperature_statistics_extended(temps)
    # Expected std ≈ 14.14
    assert abs(stats["std"] - 14.14) < 0.1


# STEP 2 (GREEN): Extend function to calculate std


def temperature_statistics_extended(temperatures):
    """Calculate statistics for a list of temperatures."""
    n = len(temperatures)
    mean = sum(temperatures) / n
    variance = sum((t - mean) ** 2 for t in temperatures) / n
    std = variance**0.5

    return {"mean": mean, "std": std}


# Verify tests pass
try:
    # Update to use extended version
    temps = [0, 10, 20, 30, 40]
    stats = temperature_statistics_extended(temps)
    assert abs(stats["mean"] - 20) < 0.01
    print("✓ Mean temperature test passed")
except (AssertionError, NameError) as e:
    print(f"✗ Mean temperature test failed: {e}")

try:
    test_temperature_statistics_std()
    print("✓ Std temperature test passed")
except (AssertionError, NameError) as e:
    print(f"✗ Std temperature test failed: {e}")

# %% [markdown]
# ### Benefits of TDD
#
# Test-Driven Development might feel backward at first (write tests before code?!), but it has
# profound benefits:
#
# 1. **Clear requirements**: Tests define what the code should do before you write it—no ambiguity
# 2. **Confidence**: You know your code works because you've tested every feature as you built it
# 3. **Documentation**: Tests show how to use the code—they're executable examples
# 4. **Design**: Writing tests first leads to better code design—testable code is usually good code
# 5. **Regression prevention**: Tests catch bugs when changing code—refactor fearlessly
#
# **When to use TDD**: TDD is especially valuable for algorithmic code, data processing, or any logic-
# heavy code where correctness is critical. For exploratory research, you might start without TDD
# and add tests as your code stabilizes. The key is to eventually have tests, even if you don't
# write them first.
#
# **Common misconception**: TDD doesn't mean "write ALL tests first, then ALL code." It means work
# in small cycles: one test, just enough code to pass it, repeat. Each cycle takes minutes, not days.

# %% [markdown]
# ## Part 7: Test Coverage
#
# ### What is Test Coverage?
#
# **Test coverage** measures which lines of code are executed during testing. It's a metric that
# tells you how much of your code is actually being tested. Think of it as a quality check for your
# test suite.
#
# - **100% coverage**: Every line is tested—but this doesn't mean bug-free!
# - **<100% coverage**: Some code is untested—potential bugs hiding there
#
# **Important caveat**: High coverage doesn't guarantee correctness. You can have 100% coverage
# with terrible tests that don't assert anything meaningful. Coverage tells you what's tested, not
# whether it's tested well. It's a necessary but not sufficient condition for quality.
#
# **Coverage targets**: Aim for 80-90% coverage for research software. 100% is often not worth the
# effort—some code (like logging or error messages) is hard to test meaningfully. Focus on testing
# your core scientific logic comprehensively.
#
# ### Measuring Coverage with pytest-cov
#
# Use `pytest-cov` to measure coverage. This plugin integrates with pytest to track which lines
# run during tests and generates reports showing untested code.
#
# ```bash
# # Run tests with coverage report
# pytest --cov=src tests/
#
# # Generate HTML coverage report (easier to read, highlights untested lines)
# pytest --cov=src --cov-report=html tests/
#
# # Set minimum coverage threshold (fails if below 80%)
# pytest --cov=src --cov-fail-under=80 tests/
# ```
#
# **Reading coverage reports**: The HTML report shows your code with green (tested) and red (untested)
# highlighting. Look for red sections—those are your blind spots. Prioritize testing branches (if/else),
# loops, and error handling paths.
#
# **Coverage in CI/CD**: Add coverage checks to your CI pipeline with `--cov-fail-under`. This ensures
# coverage doesn't drop over time. Many projects display a coverage badge in their README showing
# their coverage percentage—it's a quality signal to users.
#
# ### Coverage Example


# %%
# Function with multiple paths
def classify_temperature(celsius):
    """
    Classify temperature into categories.

    Parameters
    ----------
    celsius : float
        Temperature in Celsius

    Returns
    -------
    str
        Temperature classification
    """
    if celsius < -40:
        return "extremely cold"
    elif celsius < 0:
        return "freezing"
    elif celsius < 15:
        return "cold"
    elif celsius < 25:
        return "comfortable"
    elif celsius < 35:
        return "warm"
    else:
        return "hot"


# Incomplete tests (poor coverage)
def test_classify_temperature_comfortable():
    """Test comfortable temperature."""
    assert classify_temperature(20) == "comfortable"


def test_classify_temperature_hot():
    """Test hot temperature."""
    assert classify_temperature(40) == "hot"


# These tests only cover 2 of 6 code paths!
# Coverage would show: ~33% coverage

print("Testing temperature classification:")
try:
    test_classify_temperature_comfortable()
    print("✓ Comfortable temperature test passed")
except AssertionError as e:
    print(f"✗ Test failed: {e}")

try:
    test_classify_temperature_hot()
    print("✓ Hot temperature test passed")
except AssertionError as e:
    print(f"✗ Test failed: {e}")

print("\n⚠ Warning: Only 2 of 6 code paths tested (poor coverage)!")

# %% [markdown]
# ### Comprehensive Tests (Good Coverage)


# %%
def test_classify_temperature_comprehensive():
    """Comprehensive tests for all temperature classifications."""

    # Test all branches
    assert classify_temperature(-50) == "extremely cold"
    assert classify_temperature(-20) == "freezing"
    assert classify_temperature(5) == "cold"
    assert classify_temperature(20) == "comfortable"
    assert classify_temperature(30) == "warm"
    assert classify_temperature(40) == "hot"

    # Test boundary conditions
    assert classify_temperature(-40) == "freezing"  # Exact boundary
    assert classify_temperature(0) == "cold"  # Exact boundary
    assert classify_temperature(15) == "comfortable"  # Exact boundary

    print("✓ All temperature classifications tested (100% coverage)")


test_classify_temperature_comprehensive()

# %% [markdown]
# ### Coverage Reports
#
# A typical coverage report looks like:
#
# ```
# Name                      Stmts   Miss  Cover
# ---------------------------------------------
# src/temperature.py           45      0   100%
# src/statistics.py            32      5    84%
# src/plotting.py              28     14    50%
# ---------------------------------------------
# TOTAL                       105     19    82%
# ```
#
# **What to aim for:**
# - **Critical functions**: 100% coverage
# - **Overall project**: 80%+ coverage
# - **Don't obsess**: 100% isn't always necessary
# - **Focus on logic**: Trivial getters/setters less important

# %% [markdown]
# ### AI and Test Writing
#
# AI assistants are genuinely good at test writing—given a function, they'll turn it into a
# structured `test_*` function in seconds, faster than typing the boilerplate by hand. What
# they're not automatically good at is choosing an assertion that actually verifies the
# behavior you care about. The question from Lecture 3 applies here just as much as to
# production code: **a test you don't understand is a test you can't trust.**
#
# The specific risk for tests is subtle: a test can *pass* while checking almost nothing. That
# looks fine on a coverage report (the code ran, so it counts as "covered"), but a passing test
# that doesn't actually verify the right answer gives you false confidence—arguably worse than
# no test at all, since it looks like safety without providing it.


# %%
def broken_converter(celsius):
    """Convert Celsius to Fahrenheit (deliberately broken for this demo)."""
    return 98.6  # Always returns the same wrong value, regardless of input!


# A weak, AI-generated-style test: checks that something came back, not that it's correct
def test_weak(convert):
    result = convert(0)
    assert result is not None
    return "PASSED"


# A meaningful test: checks against a known, hand-calculated value
def test_meaningful(convert):
    result = convert(0)
    assert result == 32, f"Expected 32, got {result}"
    return "PASSED"


print(f"Weak test against broken_converter: {test_weak(broken_converter)}")
try:
    print(f"Meaningful test against broken_converter: {test_meaningful(broken_converter)}")
except AssertionError as e:
    print(f"Meaningful test against broken_converter: FAILED - {e}")

# %% [markdown]
# The weak test passes against a function that's obviously wrong—`assert result is not None`
# is true for almost anything, including `98.6` every single time. The meaningful test catches
# the bug immediately, because it checks against a value we can verify by hand (0°C is exactly
# 32°F). When you review an AI-generated test, ask the same question you'd ask of AI-generated
# production code: **if this code were completely wrong, would the test actually fail?** If you
# can't answer yes, it isn't testing what you think it's testing.
#
# **How prompting helps (but doesn't replace review)**: asking specifically for what the test
# should verify—"check that this returns exactly 32 for 0°C and exactly 212 for 100°C"—is far
# more likely to produce a meaningful assertion than "write a test for this function." That's
# the specificity habit from Lecture 3. It shifts the odds; it doesn't guarantee the result. You
# still have to read the test before you trust it.

# %% [markdown]
# ## Part 8: Defensive Programming with Assertions
#
# ### Using Assertions in Production Code
#
# Assertions aren't just for tests - use them in your code to catch bugs early!


# %%
def calculate_temperature_change(initial, final):
    """
    Calculate temperature change.

    Parameters
    ----------
    initial : float
        Initial temperature in Celsius
    final : float
        Final temperature in Celsius

    Returns
    -------
    float
        Temperature change
    """
    # Defensive programming: check inputs
    assert isinstance(initial, (int, float)), f"Initial temperature must be numeric, got {type(initial)}"
    assert isinstance(final, (int, float)), f"Final temperature must be numeric, got {type(final)}"
    assert initial >= -273.15, f"Initial temperature {initial}°C below absolute zero!"
    assert final >= -273.15, f"Final temperature {final}°C below absolute zero!"

    change = final - initial

    # Postcondition: verify reasonable result
    assert abs(change) < 500, f"Temperature change {change}°C seems unrealistic!"

    return change


# Test with valid inputs
print("Valid input:")
result = calculate_temperature_change(20, 25)
print(f"Temperature change: {result}°C")

# Test with invalid input
print("\nInvalid input (below absolute zero):")
try:
    result = calculate_temperature_change(-300, 20)
except AssertionError as e:
    print(f"✓ Assertion caught invalid input: {e}")

# %% [markdown]
# ### Preconditions, Postconditions, and Invariants
#
# **Preconditions**: What must be true before function runs
# ```python
# assert temperature >= -273.15, "Temperature below absolute zero"
# assert len(data) > 0, "Data list cannot be empty"
# ```
#
# **Postconditions**: What must be true after function runs
# ```python
# assert result >= 0, "Result must be non-negative"
# assert len(output) == len(input), "Output size must match input"
# ```
#
# **Invariants**: What must remain true during execution
# ```python
# for item in data:
#     assert item is not None, "Data contains None values"
# ```

# %% [markdown]
# ## Part 9: Complete Example - From Bug to Full Coverage
#
# ### The Complete Fixed Temperature Module


# %%
def celsius_to_fahrenheit_final(celsius):
    """
    Convert temperature from Celsius to Fahrenheit.

    Parameters
    ----------
    celsius : float
        Temperature in Celsius

    Returns
    -------
    float
        Temperature in Fahrenheit
    """
    assert celsius >= -273.15, f"Temperature {celsius}°C below absolute zero"
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius_final(fahrenheit):
    """
    Convert temperature from Fahrenheit to Celsius.

    Parameters
    ----------
    fahrenheit : float
        Temperature in Fahrenheit

    Returns
    -------
    float
        Temperature in Celsius
    """
    assert fahrenheit >= -459.67, f"Temperature {fahrenheit}°F below absolute zero"
    return (fahrenheit - 32) * 5 / 9


def calculate_temperature_anomaly_final(temperatures_f, baseline_f):
    """
    Calculate temperature anomaly relative to baseline.

    Parameters
    ----------
    temperatures_f : list
        List of temperatures in Fahrenheit
    baseline_f : float
        Baseline temperature in Fahrenheit

    Returns
    -------
    list
        Temperature anomalies in Celsius
    """
    assert isinstance(temperatures_f, list), "temperatures_f must be a list"
    assert len(temperatures_f) > 0, "temperatures_f cannot be empty"
    assert isinstance(baseline_f, (int, float)), "baseline_f must be numeric"

    baseline_c = fahrenheit_to_celsius_final(baseline_f)

    anomalies = []
    for temp in temperatures_f:
        assert isinstance(temp, (int, float)), f"Temperature {temp} is not numeric"
        temp_c = fahrenheit_to_celsius_final(temp)
        anomaly = temp_c - baseline_c
        anomalies.append(anomaly)

    return anomalies


# %% [markdown]
# ### Comprehensive Test Suite


# %%
def test_celsius_to_fahrenheit_final_suite():
    """Comprehensive test suite for celsius_to_fahrenheit."""
    # Test standard conversions
    assert celsius_to_fahrenheit_final(0) == 32
    assert celsius_to_fahrenheit_final(100) == 212
    assert celsius_to_fahrenheit_final(-40) == -40

    # Test edge cases
    assert abs(celsius_to_fahrenheit_final(-273.15) - (-459.67)) < 0.1
    assert celsius_to_fahrenheit_final(37) - 98.6 < 0.1

    # Test assertions catch invalid input
    try:
        celsius_to_fahrenheit_final(-300)
        assert False, "Should have raised AssertionError"
    except AssertionError:
        pass  # Expected

    print("✓ All celsius_to_fahrenheit tests passed")


def test_fahrenheit_to_celsius_final_suite():
    """Comprehensive test suite for fahrenheit_to_celsius."""
    # Test standard conversions
    assert fahrenheit_to_celsius_final(32) == 0
    assert fahrenheit_to_celsius_final(212) == 100
    assert fahrenheit_to_celsius_final(-40) == -40

    # Test roundtrip conversion
    for temp in [-40, 0, 25, 37, 100]:
        f = celsius_to_fahrenheit_final(temp)
        c = fahrenheit_to_celsius_final(f)
        assert abs(c - temp) < 0.01

    print("✓ All fahrenheit_to_celsius tests passed")


def test_calculate_temperature_anomaly_final_suite():
    """Comprehensive test suite for calculate_temperature_anomaly."""
    # Test basic calculation
    temps = [32, 33, 34, 35]
    baseline = 32
    anomalies = calculate_temperature_anomaly_final(temps, baseline)
    assert len(anomalies) == len(temps)
    assert abs(anomalies[0]) < 0.01  # First temp = baseline, anomaly ≈ 0

    # Test with known values
    temps = [68, 77]  # 20°C and 25°C
    baseline = 68  # 20°C
    anomalies = calculate_temperature_anomaly_final(temps, baseline)
    assert abs(anomalies[0]) < 0.01  # Should be 0
    assert abs(anomalies[1] - 5) < 0.01  # Should be 5°C

    print("✓ All temperature anomaly tests passed")


# Run all tests
test_celsius_to_fahrenheit_final_suite()
test_fahrenheit_to_celsius_final_suite()
test_calculate_temperature_anomaly_final_suite()

print("\n🎉 All tests passed! Code is fully tested and bug-free!")

# %% [markdown]
# ## Summary: What We Learned
#
# ### The Journey
#
# 1. **Started with disaster**: Untested code with a critical bug
# 2. **Learned about testing**: Why it matters, especially in research
# 3. **Wrote our first tests**: Using pytest and assertions
# 4. **Found and fixed bugs**: Tests revealed the formula error
# 5. **Applied TDD**: Write tests first, then implementation
# 6. **Measured coverage**: Ensured all code paths tested
# 7. **Added defensive programming**: Assertions in production code
# 8. **Built comprehensive suite**: Full test coverage of corrected code
#
# ### Key Takeaways
#
# ✅ **Always test research software** - your career may depend on it
# ✅ **Write tests early** - before bugs cause problems
# ✅ **Use pytest** - it makes testing easy and automatic
# ✅ **Aim for high coverage** - test all code paths
# ✅ **Use assertions** - catch bugs at the source
# ✅ **TDD works** - write tests first for better design
# ✅ **Tests are documentation** - they show how code should work
#
# ### Testing Best Practices for Research
#
# 1. **Test scientific correctness**: Verify formulas and algorithms
# 2. **Test edge cases**: Boundary conditions, empty inputs, extreme values
# 3. **Test with known results**: Use published data or hand-calculated examples
# 4. **Keep tests simple**: One assertion per test when possible
# 5. **Run tests often**: Before committing, after changes, in CI
# 6. **Don't skip testing**: Even "simple" functions can have bugs
#
# ### Testing in Other Programming Languages
#
# While this lecture focused on Python and pytest, **every modern programming language has
# testing frameworks**. Here's what to look for in other languages you might use for research:
#
# **C/C++**
# - **Popular frameworks**: Google Test (gtest), Catch2, CppUnit, Boost.Test
# - **What to look for**: Unit testing with assertions, test fixtures, mocking
# - **Example**: `ASSERT_EQ(celsius_to_fahrenheit(0), 32);`
# - **Note**: More manual setup than Python, but same concepts apply
#
# **Java**
# - **Popular frameworks**: JUnit (most common), TestNG, AssertJ
# - **What to look for**: Annotations like `@Test`, assertions, test runners
# - **Example**: `@Test public void testCelsiusToFahrenheit() { assertEquals(32, celsiusToFahrenheit(0)); }`
# - **Note**: Integrated into most Java IDEs
#
# **Julia**
# - **Built-in testing**: `Test` standard library (no external install needed)
# - **What to look for**: `@test` macro, `@testset` for grouping
# - **Example**: `@test celsius_to_fahrenheit(0) ≈ 32`
# - **Note**: Very Pythonic feel, easy to get started
#
# **R**
# - **Popular frameworks**: testthat (most popular), RUnit, tinytest
# - **What to look for**: `test_that()` function, expectations like `expect_equal()`
# - **Example**: `test_that("conversion works", { expect_equal(celsius_to_fahrenheit(0), 32) })`
# - **Note**: Well integrated with RStudio and package development
#
# **JavaScript/TypeScript**
# - **Popular frameworks**: Jest, Mocha, Jasmine, Vitest
# - **What to look for**: `describe()` and `it()` blocks, assertions with `expect()`
# - **Example**: `expect(celsiusToFahrenheit(0)).toBe(32);`
# - **Note**: Essential for web-based research tools
#
# **Fortran**
# - **Popular frameworks**: pFUnit, FRUIT, Funit
# - **What to look for**: Test suites, assertions, fixtures
# - **Example**: `@assertEqual(32.0, celsius_to_fahrenheit(0.0))`
# - **Note**: Yes, even Fortran has modern testing frameworks!
#
# **MATLAB**
# - **Built-in testing**: Unit Testing Framework (no toolbox required in modern versions)
# - **What to look for**: `matlab.unittest.TestCase`, `verifyEqual()`
# - **Example**: `testCase.verifyEqual(celsiusToFahrenheit(0), 32)`
# - **Note**: Integrated with MATLAB IDE
#
# **Rust**
# - **Built-in testing**: Part of the language itself
# - **What to look for**: `#[test]` attribute, `assert_eq!()` macro
# - **Example**: `#[test] fn test_conversion() { assert_eq!(celsius_to_fahrenheit(0.0), 32.0); }`
# - **Note**: Testing is a first-class citizen in Rust
#
# **Common Patterns Across All Languages**
#
# No matter what language you use, look for these features:
#
# 1. **Assertion functions**: Check expected vs. actual values
# 2. **Test organization**: Group related tests together
# 3. **Test discovery**: Automatic finding and running of tests
# 4. **Setup/teardown**: Code that runs before/after tests
# 5. **Mocking**: Replace real objects with test doubles
# 6. **Coverage tools**: Measure which code is tested
# 7. **CI integration**: Run tests automatically in pipelines
#
# **Key Takeaway**: The language changes, but **the principles remain the same**:
# - Write tests for your code
# - Test edge cases and scientific correctness
# - Run tests frequently
# - Automate testing in CI
#
# Don't let an unfamiliar language stop you from testing. Every language has tools—find them, learn them, use them!

# %% [markdown]
# ## Acknowledgements and References
#
# This lecture draws on established testing practices and real-world lessons from research software:
#
# ### Primary Sources
#
# - **Research Software Engineering with Python** by The Alan Turing Institute
#   <https://alan-turing-institute.github.io/rse-course/html/>
#   Testing philosophy, pytest examples, and test-driven development approaches adapted from this course.
#
# - **Research Software Engineering with Python** by Damien Irving, Kate Hertweck,
#   Luke Johnston, Joel Ostblom, Charlotte Wickham, and Greg Wilson (2022)
#   <https://third-bit.com/py-rse/>
#   Chapter on "Testing Software" provided foundational concepts for defensive
#   programming and test organization.
#
# ### Testing Framework Documentation
#
# - **pytest Documentation**
#   <https://docs.pytest.org/>
#   Official pytest framework documentation for test writing, fixtures, and coverage.
#   - Getting Started: <https://docs.pytest.org/en/stable/getting-started.html>
#   - Fixtures: <https://docs.pytest.org/en/stable/fixture.html>
#   - Parametrize: <https://docs.pytest.org/en/stable/parametrize.html>
#
# - **pytest-cov Plugin**
#   <https://pytest-cov.readthedocs.io/>
#   For test coverage measurement and reporting.
#
# ### Inspirational Sources
#
# The "cautionary tale" in this lecture is inspired by real research software failures documented in:
# - Merali, Z. (2010). "Computational science: Error, why scientific programming does not compute". Nature 467, 775-777.
# - Soergel, D.A. (2015). "Rampant software errors may undermine scientific results". F1000Research.
#
# Notable real incidents that motivated our approach:
# - Geoffrey Chang protein structure retractions (2006)
# - Reinhart-Rogoff Excel error in economics (2013)
# - Mars Climate Orbiter loss due to unit conversion (1999)
#
# ### Additional References
#
# - **Software Carpentry: Testing**
#   Testing principles and practices for scientific computing.
#
# - **Python Documentation: unittest**
#   <https://docs.python.org/3/library/unittest.html>
#   Python's built-in testing framework (alternative to pytest).
#
# ### Notes
#
# While inspired by real research software failures, the specific "temperature conversion disaster" story
# is a composite fictional narrative created for pedagogical purposes. All code examples and tests
# were developed specifically for this lecture to illustrate testing concepts in research contexts.

# %% [markdown]
# ### Next Steps
#
# In **Lecture 6**, we'll learn how to:
# - Automate testing with Continuous Integration (CI)
# - Use GitHub Actions to run tests automatically
# - Set up testing workflows in GitLab
# - Build reproducible analysis pipelines
# - Ensure every code change is tested before merging
#
# ### Remember the Cautionary Tale
#
# The climate research team's disaster could have been prevented with:
# - A single test comparing to known conversion values
# - 5 minutes writing tests vs. 6 months dealing with retraction
# - Test coverage showing untested functions
# - Peer review of both code AND tests
#
# **Don't let your research become a cautionary tale - test your code!**
