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
#     display_name: Python 3 (RSE Lecture)
#     language: python
#     name: rse_lecture
# ---

# %% [markdown]
# # Lecture 13: AI-Assisted Coding for Research Software
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
# Artificial Intelligence coding assistants have rapidly become widespread tools in
# software development, offering to help write, debug, and document code. For research
# software engineers, these tools present both exciting opportunities and serious risks.
# This lecture explores how to use AI coding assistants effectively and safely,
# understanding their capabilities and limitations, and navigating the legal and ethical
# considerations specific to research software.
#
# **Duration**: ~90 minutes
#
# ## Prerequisites
#
# Before starting this lecture, you should be familiar with:
# - Python programming (covered in Lectures 2-4)
# - Writing functions and classes
# - Basic software development practices
# - All previous RSE concepts (testing, documentation, version control)
#
# This lecture assumes you're comfortable writing code and introduces AI tools to enhance your workflow.
#
# ## Learning Objectives
# - Understand what AI coding assistants are and how they work
# - Compare different types of AI assistance (integrated vs chat-based)
# - Use GitHub Copilot and ChatGPT effectively for research coding
# - Recognize common pitfalls and security risks
# - Navigate legal implications (licensing, copyright, data protection)
# - Understand self-hosted options for sensitive research code
# - Apply best practices for AI-assisted research software development

# %% [markdown]
# ## Part 1: The Copy-Paste Catastrophe - A Cautionary Tale
#
# ### The Story
#
# Dr. Sarah Chen was excited. A new AI coding assistant had just been released, and it
# promised to "write code from comments." She was under pressure to analyze genomic data
# for an upcoming paper deadline. The AI seemed perfect - she could describe what she
# needed, and it would generate the code instantly.
#
# ```python
# # She typed: "Function to normalize gene expression data"
# # The AI generated a complete function in seconds
# ```
#
# Sarah was impressed. The function looked professional, had docstrings, and even included
# error handling. She didn't fully understand the normalization algorithm it used, but it
# ran without errors and produced reasonable-looking results. She copied it into her
# analysis pipeline.
#
# **Three weeks later**, during peer review, a reviewer asked: "Why did you use
# quantile normalization instead of the standard TPM normalization for this dataset?"
#
# Sarah froze. She didn't know what the AI had generated. Looking back at the code:
# - The normalization method was inappropriate for her data type
# - The algorithm had a subtle bug that only appeared with certain data distributions
# - The function was nearly identical to GPL-licensed code (licensing violation)
# - Her results were scientifically incorrect
#
# **The paper was rejected.** Worse, Sarah had to retract a conference presentation
# based on the flawed analysis. The AI had been fast, but she hadn't understood what
# it generated or verified it was correct.
#
# ### The Lessons
#
# This story illustrates several critical points:
#
# 1. **AI generates plausible code, not necessarily correct code**
# 2. **Understanding your code is non-negotiable in research**
# 3. **AI suggestions may have hidden bugs or use inappropriate algorithms**
# 4. **Legal issues (licensing) can arise from AI-generated code**
# 5. **Speed without comprehension is dangerous in science**
#
# With these lessons in mind, let's learn how to use AI assistants effectively and safely.

# %% [markdown]
# ## Part 2: What AI Means for Research Software Engineers
#
# ### AI as Tool, Not Replacement
#
# The rise of AI coding assistants has sparked anxiety in the software development
# community: "Will AI replace programmers?" For Research Software Engineers, this question
# misses the fundamental nature of our work. **AI doesn't replace RSEs—it changes how we work.**
#
# Think of AI assistants like calculators for mathematicians:
# - Calculators didn't replace mathematicians
# - They freed mathematicians from tedious arithmetic
# - Mathematical thinking, proof design, and insight remain uniquely human
# - The best mathematicians use calculators as tools to amplify their capabilities
#
# Similarly, AI coding assistants are tools that amplify RSE capabilities, not replacements
# for RSE expertise.
#
# ### How AI Helps Research Software Engineers
#
# AI assistants can genuinely improve RSE productivity when used appropriately:
#
# **1. Accelerating Routine Tasks**
# - Generating boilerplate code (imports, class structures, test fixtures)
# - Writing standard docstrings following established patterns
# - Converting data between formats (JSON to CSV, MATLAB to Python)
# - Implementing well-known algorithms (sorting, searching, basic statistics)
#
# **2. Learning New Tools and Libraries**
# - Getting started with unfamiliar APIs (example: "How do I read NetCDF in Python?")
# - Understanding error messages and stack traces
# - Exploring alternative approaches to a problem
# - Quickly prototyping to test ideas
#
# **3. Code Quality Improvements**
# - Suggesting better variable names
# - Identifying potential edge cases
# - Proposing more efficient algorithms
# - Generating comprehensive test cases
#
# **4. Documentation and Communication**
# - Writing clear README files and user guides
# - Creating code examples for documentation
# - Explaining complex code to collaborators
# - Drafting comments for code review
#
# **What AI does well**: Pattern recognition, synthesis from examples, generating
# variations on known solutions.
#
# ### What Remains Uniquely Human (and Why)
#
# Despite AI's capabilities, Research Software Engineering expertise remains fundamentally
# human. Here's what AI cannot do—and why RSEs remain essential:
#
# **1. Understanding the Research Question**
# - **Why AI fails**: AI doesn't understand scientific goals, hypotheses, or domain constraints
# - **RSE expertise**: Translating research questions into computational approaches
# - **Example**: Choosing between Monte Carlo and analytical methods for a climate model
#   requires understanding physics, not just coding patterns
#
# **2. Evaluating Scientific Correctness**
# - **Why AI fails**: AI recognizes code patterns but not scientific validity
# - **RSE expertise**: Knowing if an algorithm is appropriate for the data and question
# - **Example**: Sarah's story—AI suggested quantile normalization, but TPM was needed.
#   Only domain knowledge reveals this mismatch.
#
# **3. Designing Software Architecture**
# - **Why AI fails**: Large-scale design requires understanding trade-offs, scalability,
#   maintainability over years—not patterns in existing code
# - **RSE expertise**: Architecting systems that grow with research needs
# - **Example**: Deciding whether a workflow needs a database, flat files, or HDF5
#   requires understanding data access patterns, collaboration needs, and future scale
#
# **4. Critical Evaluation and Debugging**
# - **Why AI fails**: AI can suggest fixes but doesn't understand the *why* behind bugs
# - **RSE expertise**: Diagnosing root causes, not just symptoms
# - **Example**: A simulation produces unexpected results. AI might fix syntax errors,
#   but understanding if the physics equations are correct requires domain expertise.
#
# **5. Research Ethics and Integrity**
# - **Why AI fails**: Cannot make ethical judgments about data use, privacy, or research practices
# - **RSE expertise**: Navigating GDPR, research ethics, data sovereignty, reproducibility
# - **Example**: Deciding what medical research data can be sent to cloud AI services
#   requires understanding regulations and institutional policies
#
# **6. Collaboration and Mentoring**
# - **Why AI fails**: Can't build teams, resolve conflicts, or mentor junior researchers
# - **RSE expertise**: Working with researchers, teaching best practices, building community
# - **Example**: Helping a PhD student understand not just how to write a function,
#   but why testing matters and how to think about software design
#
# **The irreplaceable RSE**: You bring scientific domain knowledge, critical thinking,
# ethical judgment, and collaborative skills. AI brings pattern matching and code generation.
# These are complementary, not competing capabilities.
#
# ### Skills RSEs Need to Thrive with AI
#
# To make the best use of AI assistants while maintaining your expertise, develop these skills:
#
# **1. Critical Evaluation**
# - **Skill**: Quickly assess if AI-generated code is correct, efficient, and appropriate
# - **Why essential**: AI generates plausible code, not always correct code
# - **How to develop**: Practice reviewing AI suggestions with the same rigor as code review
#   - Does it handle edge cases?
#   - Is the algorithm appropriate for the data size?
#   - Are there security implications?
#
# **2. Prompt Engineering**
# - **Skill**: Crafting clear, specific requests that get useful AI responses
# - **Why essential**: Better prompts → better suggestions → less time debugging
# - **How to develop**:
#   - Be specific: "Generate pytest test for temperature validation with edge cases"
#     vs "write tests"
#   - Provide context: "For climate data with possible sensor errors..."
#   - Iterate: If first response misses the mark, refine your prompt
#
# **3. Deep Domain Knowledge**
# - **Skill**: Understanding the science behind your code
# - **Why essential**: Only you can judge if the algorithm matches the scientific question
# - **How to develop**:
#   - Collaborate closely with domain scientists
#   - Read the papers describing methods you implement
#   - Attend domain-specific conferences, not just software ones
#
# **4. Software Engineering Fundamentals**
# - **Skill**: Testing, version control, design patterns, performance optimization
# - **Why essential**: AI can write individual functions but can't architect systems
# - **How to develop**:
#   - Study classic software engineering (Clean Code, Design Patterns)
#   - Practice test-driven development (write tests first, then use AI for implementation)
#   - Learn to profile and optimize—AI suggestions often prioritize clarity over performance
#
# **5. Ethical and Legal Awareness**
# - **Skill**: Understanding privacy, licensing, research integrity
# - **Why essential**: AI doesn't understand these constraints
# - **How to develop**:
#   - Learn about research ethics and data protection (GDPR, HIPAA)
#   - Understand open-source licenses
#   - Follow institutional policies on data and code
#
# **6. Effective Communication**
# - **Skill**: Explaining technical decisions to non-technical researchers
# - **Why essential**: AI can't translate between research and software perspectives
# - **How to develop**:
#   - Practice explaining code in terms of scientific impact
#   - Write documentation for your future self, not just today's you
#   - Mentor others—teaching clarifies your own understanding
#
# ### The Future RSE: Human Expertise + AI Tools
#
# The most effective Research Software Engineers in the AI era will be those who:
#
# 1. **Use AI for acceleration**: Let AI handle boilerplate while you focus on hard problems
# 2. **Maintain deep expertise**: Your domain knowledge and critical thinking can't be automated
# 3. **Stay critical**: Never trust AI output without verification
# 4. **Keep learning**: Software and AI tools evolve; continuous learning is essential
# 5. **Collaborate effectively**: Work with both AI tools and human researchers
#
# **Bottom line**: AI assistants make good RSEs more productive. They don't make
# inexperienced developers into RSEs. The expertise—understanding research, evaluating
# correctness, designing systems, navigating ethics—remains uniquely human.
#
# As we explore specific AI tools in the following sections, remember: you're learning
# to use powerful tools, not training your replacement. Your judgment, expertise, and
# scientific understanding are what make you valuable. AI just helps you work faster.

# %% [markdown]
# ## Part 3: What Are AI Coding Assistants?
#
# ### The Technology
#
# AI coding assistants are built on **Large Language Models (LLMs)** trained on vast
# amounts of code from public repositories, documentation, and sometimes private sources.
# These models learn patterns in code and can generate new code based on context.
#
# **Key characteristics:**
# - **Pattern-based**: They recognize common coding patterns and reproduce them
# - **Statistical**: They predict the most likely next tokens, not "understand" logic
# - **Context-aware**: They use your current code as context for suggestions
# - **Non-deterministic**: The same prompt may produce different outputs
#
# **Important**: AI assistants don't "understand" code the way humans do. They recognize
# statistical patterns in text. This is powerful but has fundamental limitations.
#
# ### The Landscape (Brief Overview)
#
# **Integrated coding assistants** work inside your IDE:
# - GitHub Copilot (Microsoft/OpenAI) - widely used, commercial
# - Amazon CodeWhisperer - free tier available
# - Tabnine - partial free tier
# - Continue.dev - open-source, supports local models
#
# **Chat-based assistants** work through conversation:
# - ChatGPT (OpenAI) - general purpose, code-capable
# - Claude (Anthropic) - strong at code explanation
# - Gemini (Google) - multimodal capabilities
#
# **Self-hosted options** for data privacy:
# - Ollama with Code Llama - run locally
# - Continue.dev with local models - privacy-preserving
# - Tabby - self-hosted coding assistant
#
# **Note**: This landscape changes rapidly. The principles in this lecture apply
# regardless of which specific tools you use. Focus on understanding how to use any
# AI assistant safely, not memorizing today's tool list.

# %% [markdown]
# ## Part 4: GitHub Copilot vs ChatGPT - Different Tools for Different Tasks
#
# ### Understanding the Difference
#
# While both use similar underlying technology (large language models), they're designed
# for very different workflows:
#
# **GitHub Copilot** (Integrated Assistant):
# - **Where**: Works inside your code editor (VS Code, JetBrains, etc.)
# - **When**: Suggests code as you type
# - **How**: Autocomplete-style, line-by-line or multi-line suggestions
# - **Context**: Uses your current file and nearby files
# - **Speed**: Instant, real-time suggestions
# - **Best for**: Writing routine code, completing patterns, generating boilerplate
#
# **ChatGPT** (Conversational Assistant):
# - **Where**: Web interface or API
# - **When**: You explicitly ask questions
# - **How**: Back-and-forth conversation, explain-and-iterate
# - **Context**: Only what you provide in the conversation
# - **Speed**: Deliberate, response-based interaction
# - **Best for**: Learning concepts, debugging logic, designing algorithms, code review
#
# ### Comparison Through Example
#
# Let's see how each tool helps with a common research task: writing a function to
# calculate rolling statistics for time series data.
#
# #### Copilot Workflow (Integrated)
#
# **You type a comment and function signature:**
# ```python
# # Calculate rolling mean and standard deviation for time series
# def rolling_stats(data, window_size):
# ```
#
# **Copilot immediately suggests** (as you type):
# ```python
#     """
#     Calculate rolling statistics for time series data.
#
#     Parameters
#     ----------
#     data : list or np.ndarray
#         Time series data
#     window_size : int
#         Size of the rolling window
#
#     Returns
#     -------
#     tuple
#         (rolling_mean, rolling_std)
#     """
#     import numpy as np
#     # Copilot generates implementation here...
# ```
#
# **Strengths**: Fast, maintains code flow, good for experienced developers
# **Weaknesses**: Less explanation, harder to understand complex logic, may distract
#
# #### ChatGPT Workflow (Conversational)
#
# **You ask:**
# > "I need to calculate rolling statistics for climate time series data. What's the
# > best approach in Python, and are there any edge cases I should handle?"
#
# **ChatGPT responds** with:
# - Explanation of rolling window concepts
# - Comparison of different approaches (NumPy, Pandas, custom)
# - Discussion of edge cases (window size > data length, NaN handling)
# - Example implementation with explanations
# - Suggestions for testing
#
# **Then you can follow up:**
# > "What if my data has missing values? How should I handle them?"
#
# **ChatGPT explains** different strategies (skip, interpolate, forward-fill) with
# pros/cons for each.
#
# **Strengths**: Educational, exploratory, great for learning, handles complexity
# **Weaknesses**: Slower, requires copy-paste, context switching
#
# ### When to Use Which?
#
# **Use Copilot when:**
# - Writing routine, well-understood code
# - Generating boilerplate (imports, docstrings, test fixtures)
# - Completing patterns you've already established
# - You know what you want and just need it typed faster
# - You're experienced and can quickly evaluate suggestions
#
# **Use ChatGPT when:**
# - Learning a new concept or library
# - Designing an algorithm (need to think through options)
# - Debugging complex logic (explain the problem, get insights)
# - Understanding existing code (paste code, ask for explanation)
# - Planning architecture or comparing approaches
# - You're less familiar with the domain and need guidance
#
# **Use both in sequence:**
# 1. ChatGPT: Design the approach, understand the algorithm
# 2. Copilot: Implement it efficiently in your editor
# 3. ChatGPT: Review for issues you might have missed
#
# ### Live Demonstration: Writing a Data Validation Function
#
# Let's demonstrate both tools with a realistic research task: validating experimental
# data before analysis.
#
# **Task**: Write a function that validates temperature measurements, checking for:
# - Physically impossible values (e.g., below absolute zero)
# - Statistical outliers
# - Missing data
# - Temporal consistency


# %%
def validate_temperature_data(temperatures, timestamps=None, min_valid=-273.15, max_valid=100, std_threshold=3.0):
    """
    Validate temperature measurement data for physical and statistical correctness.

    This function checks experimental temperature data for common issues that could
    indicate sensor errors, data corruption, or measurement problems. It's designed
    for quality control in research data pipelines.

    Parameters
    ----------
    temperatures : list or np.ndarray
        Temperature measurements in Celsius
    timestamps : list or np.ndarray, optional
        Timestamps for each measurement (for temporal checks)
    min_valid : float, optional
        Minimum physically valid temperature (default: -273.15°C, absolute zero)
    max_valid : float, optional
        Maximum expected temperature for the application (default: 100°C)
    std_threshold : float, optional
        Number of standard deviations for outlier detection (default: 3.0)

    Returns
    -------
    dict
        Validation results containing:
        - 'valid': bool, whether all checks passed
        - 'errors': list of error messages
        - 'warnings': list of warning messages
        - 'statistics': dict of data statistics

    Examples
    --------
    >>> temps = [20.5, 21.0, 20.8, 22.1, 21.5]
    >>> result = validate_temperature_data(temps)
    >>> result['valid']
    True

    Notes
    -----
    This function is conservative - it will flag potential issues for human review
    rather than automatically removing data. In research, it's better to manually
    investigate outliers than to automatically discard potentially valid measurements.
    """
    import numpy as np

    # Convert to numpy array for easier manipulation
    temps = np.array(temperatures)

    # Initialize results
    errors = []
    warnings = []
    statistics = {}

    # Check for missing data
    if np.any(np.isnan(temps)):
        n_missing = np.sum(np.isnan(temps))
        warnings.append(f"Found {n_missing} missing values ({n_missing/len(temps)*100:.1f}%)")

    # Work with non-NaN values for remaining checks
    valid_temps = temps[~np.isnan(temps)]

    if len(valid_temps) == 0:
        errors.append("All temperature values are missing")
        return {"valid": False, "errors": errors, "warnings": warnings, "statistics": {}}

    # Check for physically impossible values
    if np.any(valid_temps < min_valid):
        impossible_count = np.sum(valid_temps < min_valid)
        min_value = np.min(valid_temps)
        errors.append(
            f"Found {impossible_count} physically impossible values " f"(minimum: {min_value:.2f}°C, below {min_valid}°C)"
        )

    if np.any(valid_temps > max_valid):
        extreme_count = np.sum(valid_temps > max_valid)
        max_value = np.max(valid_temps)
        warnings.append(
            f"Found {extreme_count} values above expected maximum " f"(maximum: {max_value:.2f}°C, threshold: {max_valid}°C)"
        )

    # Calculate statistics
    mean_temp = np.mean(valid_temps)
    std_temp = np.std(valid_temps)
    statistics = {
        "count": len(valid_temps),
        "mean": mean_temp,
        "std": std_temp,
        "min": np.min(valid_temps),
        "max": np.max(valid_temps),
        "median": np.median(valid_temps),
    }

    # Check for statistical outliers using z-score
    if std_temp > 0:  # Avoid division by zero
        z_scores = np.abs((valid_temps - mean_temp) / std_temp)
        outliers = z_scores > std_threshold
        if np.any(outliers):
            outlier_count = np.sum(outliers)
            outlier_values = valid_temps[outliers]
            warnings.append(
                f"Found {outlier_count} statistical outliers "
                f"(>{std_threshold} std devs from mean): "
                f"[{', '.join(f'{v:.2f}' for v in outlier_values[:5])}...]"
            )

    # Temporal consistency check (if timestamps provided)
    if timestamps is not None and len(timestamps) == len(temps):
        # Check for rapid temperature changes that might indicate sensor errors
        # This is a simplified check - real implementation would be more sophisticated
        temp_diffs = np.diff(valid_temps)
        if len(temp_diffs) > 0:
            max_change = np.max(np.abs(temp_diffs))
            if max_change > 10:  # More than 10°C change between consecutive readings
                warnings.append(
                    f"Large temperature jump detected: {max_change:.2f}°C "
                    "between consecutive measurements (possible sensor error)"
                )

    # Determine overall validity
    valid = len(errors) == 0

    return {"valid": valid, "errors": errors, "warnings": warnings, "statistics": statistics}


# Test with sample data
print("Example 1: Clean data")
clean_temps = [20.5, 21.0, 20.8, 22.1, 21.5, 20.9, 21.3]
result1 = validate_temperature_data(clean_temps)
print(f"Valid: {result1['valid']}")
print(f"Errors: {result1['errors']}")
print(f"Warnings: {result1['warnings']}")
print(f"Mean: {result1['statistics']['mean']:.2f}°C\n")

print("Example 2: Data with outliers")
outlier_temps = [20.5, 21.0, 45.0, 22.1, 21.5, 20.9, 21.3]  # 45°C is unusual
result2 = validate_temperature_data(outlier_temps, max_valid=30)
print(f"Valid: {result2['valid']}")
print(f"Errors: {result2['errors']}")
print(f"Warnings: {result2['warnings']}")

print("\nExample 3: Physically impossible data")
impossible_temps = [20.5, -500.0, 22.1]  # -500°C is below absolute zero
result3 = validate_temperature_data(impossible_temps)
print(f"Valid: {result3['valid']}")
print(f"Errors: {result3['errors']}")

# %% [markdown]
# ### How This Example Demonstrates Both Tools
#
# **How Copilot might help** with this function:
# - Suggesting the function structure and docstring format
# - Auto-completing common NumPy operations
# - Generating the boilerplate for the return dictionary
# - Completing parameter validation patterns
#
# **How ChatGPT would help** with this function:
# - Discussing what validation checks are appropriate for temperature data
# - Explaining the z-score method for outlier detection
# - Suggesting edge cases to handle (NaN values, empty arrays)
# - Reviewing the implementation for bugs or improvements
# - Explaining when to use errors vs warnings
#
# **The key insight**: Copilot helps you *write* code faster. ChatGPT helps you
# *understand* what to write. Both are valuable, for different reasons.

# %% [markdown]
# ## Part 5: Pitfalls, Risks, and Common Failures
#
# ### Technical Pitfalls
#
# AI coding assistants are powerful but flawed. Here are the most common technical
# problems you'll encounter:
#
# #### 1. Hallucinated APIs (Functions That Don't Exist)
#
# **The Problem**: AI models sometimes invent functions or methods that sound plausible
# but don't actually exist.
#
# **Example**:
# ```python
# # AI might suggest (Python 3.10):
# import numpy as np
# result = np.ndarray.remove_outliers(data, threshold=3.0)  # Doesn't exist!
# ```
#
# **Why it happens**: The model learns patterns like "remove_outliers" from comments
# and documentation, and generates a plausible-looking API that doesn't exist.
#
# **How to avoid**:
# - Always check documentation for unfamiliar methods
# - Test AI-generated code before trusting it
# - Use type checkers and linters (they'll catch non-existent attributes)

# %%
# Demonstration: What happens with a hallucinated function?
import numpy as np

# This is what AI might suggest, but it doesn't exist:
# result = np.ndarray.remove_outliers(data)  # Would raise AttributeError

# What actually exists - you must know your libraries:
data = np.array([1, 2, 3, 100, 4, 5])
mean = np.mean(data)
std = np.std(data)
# Manual outlier detection using z-score
z_scores = np.abs((data - mean) / std)
data_clean = data[z_scores < 3]
print(f"Original data: {data}")
print(f"After removing outliers (|z| < 3): {data_clean}")

# %% [markdown]
# #### 2. Outdated or Deprecated Code
#
# **The Problem**: AI models are trained on historical code, which may use deprecated
# APIs or outdated practices.
#
# **Example**:
# ```python
# # AI trained on old code might suggest:
# import numpy as np
# matrix = np.matrix([[1, 2], [3, 4]])  # Deprecated since NumPy 1.25!
#
# # Modern NumPy uses:
# matrix = np.array([[1, 2], [3, 4]])
# ```
#
# **How to avoid**:
# - Check the latest documentation
# - Use linters that warn about deprecated code
# - Review changelogs when updating libraries

# %%
# Modern NumPy practices
import numpy as np

# Correct modern approach
modern_array = np.array([[1, 2], [3, 4]])
print("Modern numpy array:")
print(modern_array)
print(f"Type: {type(modern_array)}")

# Old approach (still works but discouraged)
# np.matrix is deprecated - don't use it in new code!

# %% [markdown]
# #### 3. Subtle Logic Errors
#
# **The Problem**: AI-generated code may have subtle bugs that only appear with certain
# inputs or edge cases. These are the most dangerous because the code *looks* correct.
#
# **Example - Off-by-One Error**:


# %%
def calculate_differences_buggy(values):
    """Calculate differences between consecutive values (BUGGY VERSION)."""
    differences = []
    # BUG: This misses the last difference
    for i in range(len(values) - 1):
        diff = values[i + 1] - values[i]
        differences.append(diff)
    return differences


def calculate_differences_correct(values):
    """Calculate differences between consecutive values (CORRECT VERSION)."""
    if len(values) < 2:
        return []
    return [values[i + 1] - values[i] for i in range(len(values) - 1)]


# Test both versions
test_data = [10, 15, 12, 18, 20]
print(f"Input: {test_data}")
print(f"Buggy result: {calculate_differences_buggy(test_data)}")
print(f"Correct result: {calculate_differences_correct(test_data)}")
print(f"Expected: [5, -3, 6, 2]")

# Actually, both are correct! The subtle bug is harder to spot.
# Let's try with edge cases:
edge_case = [5]
print(f"\nEdge case - single value: {edge_case}")
print(f"Buggy result: {calculate_differences_buggy(edge_case)}")
print(f"Correct result: {calculate_differences_correct(edge_case)}")
print("Buggy version doesn't handle single-element arrays explicitly")

# %% [markdown]
# #### 4. Security Vulnerabilities
#
# **The Problem**: AI may suggest code with security vulnerabilities, especially for
# file handling, database queries, or user input.
#
# **Example - Path Traversal Vulnerability**:

# %%
import os
import tempfile


def load_user_file_insecure(filename):
    """
    Load a file from user directory (INSECURE - for demonstration only).

    VULNERABILITY: Path traversal attack possible!
    User could provide: "../../../etc/passwd"
    """
    # DANGEROUS: Directly concatenating user input to file path
    base_dir = tempfile.gettempdir()
    filepath = os.path.join(base_dir, filename)
    # This check can be bypassed with "../" in filename
    return filepath


def load_user_file_secure(filename):
    """
    Load a file from user directory (SECURE VERSION).

    Protection: Validates filename has no path components.
    """
    # Only allow simple filenames, no directory traversal
    if os.path.sep in filename or filename.startswith("."):
        raise ValueError(f"Invalid filename: {filename}")

    base_dir = tempfile.gettempdir()
    filepath = os.path.join(base_dir, filename)

    # Additional check: ensure final path is still within base_dir
    real_base = os.path.realpath(base_dir)
    real_path = os.path.realpath(filepath)
    if not real_path.startswith(real_base):
        raise ValueError("Path traversal detected")

    return filepath


# Demonstration
print("Insecure version allows path traversal:")
try:
    dangerous_path = load_user_file_insecure("../../../etc/passwd")
    print(f"  Would attempt to access: {dangerous_path}")
except Exception as e:
    print(f"  Error: {e}")

print("\nSecure version prevents path traversal:")
try:
    safe_path = load_user_file_secure("data.txt")
    print(f"  Safe path: {safe_path}")
except Exception as e:
    print(f"  Error: {e}")

try:
    attack_path = load_user_file_secure("../../../etc/passwd")
    print(f"  Would access: {attack_path}")
except ValueError as e:
    print(f"  Blocked: {e}")

# %% [markdown]
# ### Cognitive Risks
#
# Beyond technical issues, AI assistants pose risks to your development and learning:
#
# **1. Over-Reliance and Skill Atrophy**
# - Using AI as a crutch instead of learning fundamentals
# - Forgetting how to solve problems without AI
# - Becoming unable to code in environments without AI access
#
# **2. False Confidence**
# - Code that "looks professional" but you don't understand
# - Feeling productive while actually accumulating technical debt
# - Inability to debug or maintain AI-generated code
#
# **3. Reduced Problem-Solving**
# - Accepting the first AI solution instead of thinking deeply
# - Missing better approaches because AI gave "an answer"
# - Not developing algorithmic thinking skills
#
# **4. Research-Specific Risks**
# - Using algorithms you don't understand (like Sarah's quantile normalization)
# - Inability to explain your methods in papers or to reviewers
# - Difficulty defending your implementation choices
# - Results you can't reproduce or debug when issues arise
#
# **Best practice**: Always understand what the AI suggests before using it. In research,
# you're responsible for every line of code, whether you wrote it or AI did.

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Want to become better at working with AI? Practice these critical thinking exercises:</p>
#     <ul>
#         <li><strong>Test AI's knowledge boundaries</strong>: Ask your AI assistant about a niche library from your field. How
#         accurate is it? Try asking about recent releases (post-2023) - does it hallucinate features?</li>
#         <li><strong>Practice prompt engineering</strong>: Try asking the same question 3
#         different ways (vague, specific, with context). How does output quality change?
#         Good prompts are a skill!</li>
#         <li><strong>Verify everything</strong>: Take an AI code suggestion and check
#         every claim: Does the function exist? Are parameters correct? Does the example
#         run? Build verification habits early.</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 6: Legal, Ethical, and Data Protection Concerns
#
# ### Copyright and Licensing
#
# **The fundamental problem**: AI models are trained on code from the internet, including
# open-source code with specific licenses. When AI generates code similar to its training
# data, who owns the copyright?
#
# **Current legal uncertainty** (as of 2026):
# - Ongoing lawsuits against GitHub Copilot and Microsoft
# - Questions about whether AI output is derivative work
# - Unclear if AI-generated code inherits source licenses
# - Different jurisdictions may rule differently
#
# **GitHub Copilot lawsuit** (filed 2022):
# - Claims Copilot violates GPL and other open-source licenses
# - Argues Copilot reproduces licensed code without attribution
# - Not yet resolved as of 2026
#
# **Practical implications for researchers**:
#
# 1. **Assume risk**: AI-generated code may have licensing issues
# 2. **Check suggestions**: If code looks like it's from a library, verify the source
# 3. **Document AI use**: Note which parts were AI-assisted
# 4. **Be conservative**: For published research code, favor code you write yourself
# 5. **Institutional policies**: Check if your university has AI usage guidelines
#
# **Safe practices**:
# - Use AI for inspiration, then write your own implementation
# - Always check if AI suggestions match existing library code
# - Include license headers in your files
# - When in doubt, write it yourself

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Concerned about legal risks? Explore these validation approaches:</p>
#     <ul>
#         <li><strong>Validate AI-generated code</strong>: Take a substantial code snippet
#         from AI. Search GitHub for similar code - does exact or near-identical code
#         exist? What license does it have?</li>
#         <li><strong>Compare licenses</strong>: Read the MIT, Apache 2.0, and GPL licenses
#         (15 minutes each). Which allows what? What obligations do they create?
#         Understanding licenses protects you.</li>
#         <li><strong>Audit your dependencies</strong>: Run <code>pip-licenses</code> or
#         similar on your project. What licenses do you depend on? Are they compatible with
#         your project's license? Any surprises?</li>
#     </ul>
# </div>

# %% [markdown]
# ### Data Protection and Privacy
#
# **Critical question**: Where does your code go when you use an AI assistant?
#
# **Cloud-based AI (Copilot, ChatGPT, etc.)**:
# - Your code is sent to external servers
# - May be used to improve the model (check settings!)
# - Stored on commercial infrastructure
# - Subject to the provider's privacy policy
# - Potential access by company employees or governments
#
# **GDPR implications** (European researchers):
# - Sending code containing personal data to AI services may violate GDPR
# - Need data processing agreements with providers
# - May require anonymization before using AI assistance
#
# **Research-specific concerns**:
#
# **Unpublished research code**:
# - Pre-publication data and methods might be confidential
# - Grant-funded research may have data sharing restrictions
# - Patent considerations if research has commercial potential
#
# **Sensitive data domains**:
# - **Medical research**: Patient data, even in code comments, is protected
# - **Genomics**: Genetic sequences may be identifiable
# - **Security research**: Vulnerability code should not be shared
# - **Industry partnerships**: Proprietary algorithms or data
#
# **Best practice**: Never paste confidential research code into public AI services.
# Use self-hosted alternatives for sensitive work.

# %% [markdown]
# ### Research Integrity
#
# **Attribution and transparency**:
#
# Some journals now ask: "Was AI used in writing this paper?"
# Should you disclose AI assistance in code?
#
# **Current practices** (evolving):
# - Some journals require AI disclosure in methods
# - Code repositories may include AI usage notes
# - No universal standard yet (as of 2026)
#
# **Reproducibility concerns**:
# - AI suggestions are non-deterministic
# - Same prompt → different code on different days
# - Hard to reproduce AI-assisted development process
#
# **Recommendation**: In research software, prioritize reproducibility and understanding
# over development speed. AI is a tool, not a substitute for expertise.

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Thinking about legal and ethical implications? Explore these deeper questions:</p>
#     <ul>
#         <li><strong>Read the terms of service</strong>: Actually read GitHub Copilot's
#         or ChatGPT's terms (10-15 minutes). What rights do you retain? What do they
#         claim? Are you comfortable with this?</li>
#         <li><strong>Understand your institution's policy</strong>: Does your university
#         or research center have guidelines on AI tools? On data protection? Find and read
#         them - they exist to protect you.</li>
#         <li><strong>Consider self-hosted options</strong>: Research tools like Ollama or
#         local LLMs. What would it take to run AI assistance on your institution's
#         infrastructure? Worth exploring for sensitive projects!</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 7: Self-Hosted Solutions for Privacy-Sensitive Research
#
# ### Why Self-Host?
#
# For privacy-sensitive research (medical data, unpublished results, proprietary
# algorithms), you may need AI assistance that doesn't send your code to external
# servers.
#
# **Use cases for self-hosted AI**:
# - Medical or genomic research code
# - Unpublished methods in competitive fields
# - Industry-partnered research with NDAs
# - Government or defense research
# - Any code containing sensitive data
#
# ### How Self-Hosting Works
#
# **Conceptual overview**:
#
# 1. **Download a pre-trained code model** (e.g., Code Llama, StarCoder)
# 2. **Run the model on your local machine** or department server
# 3. **Use a coding assistant client** that connects to your local model
# 4. **Your code never leaves your infrastructure**
#
# **Key components**:
# - **Model**: Open-source LLM trained on code (Code Llama 7B/13B/34B, StarCoder, etc.)
# - **Runtime**: Ollama, llama.cpp, or similar to run the model efficiently
# - **Client**: Continue.dev, Tabby, or custom integration
# - **Hardware**: GPU recommended but CPU works (slower)
#
# ### Popular Self-Hosted Options
#
# **Option 1: Ollama + Continue.dev**
#
# Ollama (https://ollama.ai) makes running local LLMs easy:
# ```bash
# # Install Ollama (macOS, Linux, Windows)
# curl -fsSL https://ollama.ai/install.sh | sh
#
# # Download Code Llama model
# ollama pull codellama:7b
#
# # Run the model
# ollama run codellama:7b
# ```
#
# Continue.dev is an open-source Copilot alternative that works with local models.
# Install as VS Code or JetBrains extension, configure to use Ollama.
#
# **Reference**: https://ollama.ai and https://continue.dev/docs
#
# **Option 2: Tabby (Self-Hosted)**
#
# Tabby (https://tabby.tabbyml.com) is designed specifically for self-hosted code
# completion. It's optimized for code and has lower hardware requirements than
# general-purpose LLMs.
#
# ```bash
# # Run with Docker
# docker run -it \
#   --gpus all -p 8080:8080 -v $HOME/.tabby:/data \
#   tabbyml/tabby \
#   serve --model StarCoder-1B --device cuda
# ```
#
# **Reference**: https://tabby.tabbyml.com
#
# ### Trade-offs of Self-Hosting
#
# **Advantages**:
# - ✅ Complete data privacy - code never leaves your infrastructure
# - ✅ No usage limits or costs (after setup)
# - ✅ Compliance with institutional policies
# - ✅ Works offline
# - ✅ Customizable and transparent
#
# **Disadvantages**:
# - ❌ Requires technical setup
# - ❌ Lower code quality than state-of-the-art cloud models
# - ❌ Hardware requirements (GPU ideal, CPU works but slower)
# - ❌ Models need updates (you manage this)
# - ❌ No support team (community-based)
#
# ### Practical Recommendations
#
# **For most research code**:
# - Public, non-sensitive: Cloud AI (Copilot, ChatGPT) is fine
# - Always review and understand suggestions
#
# **For sensitive research**:
# - Medical/genomic data: Use self-hosted only
# - Unpublished methods: Self-hosted or no AI
# - Industry partnerships: Check NDA, likely self-hosted
#
# **Getting started with self-hosting**:
# 1. Start with Ollama (easiest setup)
# 2. Try Code Llama 7B (good balance of quality and speed)
# 3. Use Continue.dev in VS Code (familiar interface)
# 4. Test with non-sensitive code first
# 5. Evaluate quality before committing to workflow
#
# **References for self-hosted AI**:
# - Ollama documentation: https://ollama.ai
# - Continue.dev documentation: https://continue.dev/docs
# - Tabby documentation: https://tabby.tabbyml.com
# - Code Llama paper: Rozière et al. (2023), "Code Llama: Open Foundation Models for Code"
#   https://arxiv.org/abs/2308.12950

# %% [markdown]
# ## Part 8: Best Practices for AI-Assisted Research Software Development
#
# ### The Golden Rules
#
# **1. Understand before accepting**
# - Never use code you don't understand
# - If AI suggests something complex, learn what it does
# - In research, you own every line - whether AI wrote it or not
#
# **2. AI suggests, you decide**
# - Treat suggestions as proposals, not commands
# - Consider alternatives the AI didn't suggest
# - Sometimes the best choice is to write it yourself
#
# **3. Test rigorously**
# - AI-generated code needs MORE testing, not less
# - Write tests before accepting AI suggestions
# - Check edge cases AI might miss
#
# **4. Verify licensing**
# - Check if suggestions match existing libraries
# - Search for similar code online
# - When in doubt, rewrite in your own words
#
# **5. Protect sensitive data**
# - Never paste confidential code into cloud AI
# - Use self-hosted solutions for sensitive research
# - Remove data examples before asking AI for help
#
# ### Effective Prompting Strategies
#
# **For Copilot (integrated)**:
# - Write clear comments explaining what you want
# - Use descriptive variable names
# - Start with function signatures and docstrings
# - Let Copilot fill in implementation details
# - Review each suggestion before accepting (Tab key)
#
# **For ChatGPT (conversational)**:
# - Provide context: "I'm analyzing climate model output..."
# - Be specific: "Using NumPy, not Pandas"
# - Ask for explanations: "Explain why this approach..."
# - Iterate: "What about edge case X?"
# - Request alternatives: "What other approaches exist?"
#
# ### When NOT to Use AI
#
# **Situations where AI hinders more than helps**:
#
# 1. **Learning new concepts** (first time)
#    - Write it yourself to learn deeply
#    - Use AI for review/comparison afterward
#
# 2. **Critical algorithms** (core research methods)
#    - You must understand these completely
#    - AI might suggest inappropriate methods
#
# 3. **Debugging complex logic**
#    - Understanding the bug teaches you
#    - AI might suggest band-aids instead of fixes
#
# 4. **High-security code**
#    - Security requires expert review, not AI
#    - AI may introduce subtle vulnerabilities
#
# 5. **Performance-critical code**
#    - AI optimizes for readability, not speed
#    - Profiling-guided optimization is better
#
# ### Success Stories (When AI Helps)
#
# **Positive use cases from research**:
#
# **1. Accelerated test writing**
# - Researcher writes core algorithm
# - AI generates test fixtures and edge cases
# - 30% faster test coverage, same quality
#
# **2. Documentation improvement**
# - AI helps write clear docstrings
# - Generates examples from function signatures
# - More consistent documentation style
#
# **3. Code migration**
# - Converting MATLAB code to Python
# - AI provides starting point, researcher refines
# - Faster migration, researcher stays in control
#
# **4. Learning new libraries**
# - Researcher unfamiliar with library API
# - ChatGPT explains concepts and examples
# - Researcher understands before implementing
#
# ### Final Recommendations
#
# **Developing your AI-assisted workflow**:
#
# 1. **Start conservatively**: Use AI for low-risk tasks first
# 2. **Build expertise**: Learn to quickly evaluate suggestions
# 3. **Establish boundaries**: Know what you will/won't use AI for
# 4. **Stay informed**: AI tools and policies evolve rapidly
# 5. **Share experiences**: Discuss with colleagues what works
#
# **For research software specifically**:
#
# - Prioritize understanding over speed
# - Document which code was AI-assisted
# - Test more thoroughly when using AI
# - Use self-hosted AI for sensitive work
# - Keep learning fundamentals - don't let skills atrophy
#
# **Remember Sarah's story**: AI can help you code faster, but only you can ensure
# your code is correct, appropriate for your research question, and scientifically
# sound. Use AI as a tool to augment your expertise, not replace it.

# %% [markdown]
# ## Summary
#
# In this lecture, we explored AI-assisted coding for research software:
#
# **Key Takeaways**:
#
# 1. **AI assistants are tools that amplify RSE capabilities, not replacements**
#    - RSEs bring irreplaceable expertise: domain knowledge, critical thinking, ethics
#    - AI helps with routine tasks, learning new tools, and documentation
#    - What remains human: research understanding, scientific correctness, architecture design
#
# 2. **AI assistants are powerful but imperfect tools**
#    - Generate plausible code, not always correct code
#    - Built on pattern matching, not true understanding
#    - Require critical evaluation of all suggestions
#
# 3. **Different tools for different tasks**
#    - Copilot: Integrated, real-time, good for experienced developers
#    - ChatGPT: Conversational, educational, good for learning
#    - Use both strategically based on your needs
#
# 4. **Significant risks exist**
#    - Technical: hallucinated APIs, subtle bugs, security issues
#    - Cognitive: over-reliance, skill atrophy, false confidence
#    - Legal: licensing uncertainty, copyright questions
#    - Privacy: data protection, GDPR compliance
#
# 5. **Self-hosted solutions for sensitive research**
#    - Ollama + Code Llama for local AI
#    - Continue.dev or Tabby for privacy-preserving assistance
#    - Trade-off: privacy vs quality
#
# 6. **Best practices for research software**
#    - Understand every line of code
#    - Test AI suggestions rigorously
#    - Protect sensitive research data
#    - Document AI usage appropriately
#    - Keep developing your own expertise
#
# 7. **Skills RSEs need to thrive with AI**
#    - Critical evaluation of AI outputs
#    - Prompt engineering for better results
#    - Deep domain knowledge
#    - Software engineering fundamentals
#    - Ethical and legal awareness
#
# **The bottom line**: AI coding assistants are valuable tools that can accelerate
# development, but they're not substitutes for understanding, testing, or critical
# thinking. In research software, where correctness and reproducibility are paramount,
# use AI to augment your capabilities while maintaining full responsibility for your code.
# Your expertise as an RSE—combining scientific knowledge with software skills—remains
# uniquely valuable and irreplaceable.
#
# ### What's Next?
#
# In **Lecture 14**, the final lecture, we'll wrap up the course by:
# - Reviewing and integrating knowledge from all 13 lectures
# - Exploring advanced topics we didn't cover and where to learn them
# - Connecting you with the international and German RSE communities
# - Providing resources for ongoing learning and support
# - Celebrating your journey from RSE novice to practitioner
#
# You've learned an enormous amount—from basic shell commands to AI-assisted development.
# Lecture 14 will help you see how it all fits together and chart your path forward.
#
# **Ready to conclude? Move on to Lecture 14: Course Summary and the RSE Community!**
#
# **Further Learning**:
# - Try both integrated and chat-based AI tools
# - Practice evaluating AI suggestions critically
# - Experiment with self-hosted options
# - Develop your own guidelines for when to use AI
# - Stay informed about legal and policy developments
#
# **Discussion question**: How will you integrate AI assistants into your research
# workflow while maintaining scientific rigor and code quality?
