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
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Lecture 2: Advanced Git, GitHub, GitLab, and Python Concepts for RSE
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
#     <img src="lecture_02_qr_code.png" alt="This Lecture QR Code" width="150"/>
#     <p><strong>This Lecture</strong></p>
#   </div>
# </div>
#
# ## Overview
# This lecture builds on Git fundamentals from Lecture 1 and introduces collaboration with GitHub
# and GitLab. It then reviews the Python concepts—error handling, the `with` statement,
# comprehensions, and classes—that you'll need to follow the rest of this course, whether you're
# writing code yourself or reading code a teammate or an AI assistant generated for you.
#
# **Duration**: ~90 minutes
#
# ## Prerequisites
#
# Before starting this lecture, you should be familiar with:
# - Basic command-line operations (covered in Lecture 1)
# - Git fundamentals: `git init`, `git add`, `git commit`, `git status`, `git log`
# - Basic understanding of version control concepts
# - **Basic Python skills**: you should be comfortable *reading* Python code and have written at
#   least a little of it yourself. This course does not teach Python from scratch—see Lecture 1
#   for the full list of course prerequisites if you're unsure whether that's you.
#
# If you haven't completed Lecture 1, please review it first as we build directly on those concepts.
#
# ## Learning Objectives
# - Master Git branching and merging workflows
# - Understand .gitignore patterns and file management
# - Collaborate effectively using GitHub and GitLab
# - Understand differences between GitHub and GitLab workflows
# - Read and write Python error handling, comprehensions, and simple classes confidently
# - Recognize the `with` statement / context-manager pattern wherever it appears

# %% [markdown]
# ## Part 1: Advanced Git Concepts
#
# ### Git Branching
#
# Branches allow you to work on different features or experiments without affecting the main codebase.
#
# #### Why Use Branches?
#
# - **Isolation**: Work on new features without breaking the main code
# - **Collaboration**: Multiple people can work simultaneously
# - **Experimentation**: Try new ideas safely
# - **Organization**: Separate development, testing, and production code
#
# #### Basic Branch Commands
#
# ```bash
# # Create a new branch
# git branch feature-analysis
#
# # List all branches (* marks current branch)
# git branch
#
# # Switch to a branch
# git checkout feature-analysis
#
# # Create and switch in one command
# git checkout -b new-feature
#
# # Modern alternative (Git 2.23+)
# git switch feature-analysis
# git switch -c new-feature
# ```

# %% [markdown]
# ### Branching Workflow Example
#
# Let's walk through a typical workflow. This is the pattern you'll use countless times when
# developing software: create a branch for your work, make your changes, and then merge them back.
# Working on a branch keeps your main code stable while you experiment or develop new features.
#
# ```bash
# # Start on main branch
# git checkout main
#
# # Create a new feature branch
# git checkout -b add-statistics
#
# # Make changes to your code
# # ... edit files ...
#
# # Stage and commit changes
# git add analysis.py
# git commit -m "Add mean and median calculations"
#
# # More changes
# # ... edit files ...
# git add analysis.py
# git commit -m "Add standard deviation calculation"
#
# # View your branch history
# git log --oneline --graph
# ```
#
# **Pro tip**: Use descriptive branch names like `fix-data-loading-bug` or `add-visualization-feature`
# rather than generic names like `test` or `new-branch`. This makes it easier to remember what each
# branch is for, especially when you're working on multiple features simultaneously.

# %% [markdown]
# ### Merging Branches
#
# Once your feature is complete and tested, merge it back into the main branch. Git provides
# different types of merges depending on the situation. Understanding these helps you maintain
# a clean, readable Git history.
#
# #### Fast-Forward Merge
#
# When main hasn't changed since you branched, Git can do a "fast-forward" merge. This simply
# moves the main branch pointer forward to include your commits—no merge commit is created.
# It's the simplest and cleanest type of merge.
#
# ```bash
# # Switch to main
# git checkout main
#
# # Merge feature branch
# git merge add-statistics
#
# # Delete the feature branch (optional, but keeps things tidy)
# git branch -d add-statistics
# ```
#
# #### Three-Way Merge
#
# When both branches have new commits (for example, if someone else pushed changes to main while
# you were working on your feature), Git creates a special "merge commit" that combines the changes.
# This preserves the full history of both branches.
#
# ```bash
# # Git creates a merge commit
# git checkout main
# git merge add-statistics
#
# # Git will open an editor for merge commit message
# # Save and close to complete the merge
# ```
#
# **When does this happen?** This is common in collaborative projects. While you're working on your
# feature branch, your colleague merges their changes into main. When you go to merge, Git needs to
# reconcile both sets of changes.

# %% [markdown]
# ### Handling Merge Conflicts
#
# Conflicts occur when the same lines are changed in both branches. This is actually quite common
# and nothing to be afraid of! Git is smart enough to merge most changes automatically, but when
# two people edit the exact same lines, Git needs you to decide which version to keep (or how to
# combine them).
#
# ```bash
# # When a conflict occurs
# git merge feature-branch
# # Auto-merging file.py
# # CONFLICT (content): Merge conflict in file.py
# # Automatic merge failed; fix conflicts and then commit the result.
#
# # Check which files have conflicts
# git status
#
# # Open conflicted files - you'll see markers like:
# # <<<<<<< HEAD
# # Your changes
# # =======
# # Their changes
# # >>>>>>> feature-branch
#
# # Edit files to resolve conflicts
# # Remove conflict markers
# # Keep the code you want
#
# # Stage resolved files
# git add file.py
#
# # Complete the merge
# git commit -m "Merge feature-branch, resolved conflicts"
# ```
#
# **How to resolve conflicts**: Open the file and look for the `<<<<<<<`, `=======`, and `>>>>>>>`
# markers. The section between `<<<<<<< HEAD` and `=======` is your current branch's version. The
# section between `=======` and `>>>>>>> feature-branch` is the incoming branch's version. Delete
# the markers and edit the code to include the changes you want to keep. Sometimes you'll keep one
# version, sometimes the other, and sometimes you'll combine both. After editing, save the file,
# stage it with `git add`, and complete the merge with `git commit`.
#
# **Common mistake**: Forgetting to remove the conflict markers (`<<<<<<<`, etc.) from your code.
# If you leave them in, your code won't run! Always check that the final version is valid code
# before committing.

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Master Git branching and conflict resolution:</p>
#     <ul>
#         <li><strong>Create an intentional conflict:</strong> Make two branches that modify the same
#         line in different ways, then practice resolving the conflict manually</li>
#         <li><strong>Experiment with merge strategies:</strong> Try both fast-forward and three-way
#         merges. Use <code>git log --graph</code> to visualize the differences in history</li>
#         <li><strong>Practice the feature branch workflow:</strong> Create a branch for a small
#         feature, make several commits, then merge it back to main with a descriptive commit
#         message</li>
#     </ul>
# </div>

# %% [markdown]
# ### The .gitignore File
#
# Not all files should be tracked by Git. Some files are generated automatically (like compiled code),
# some are too large (like data files), and some contain sensitive information (like API keys). The
# `.gitignore` file tells Git which files to ignore completely.
#
# Use `.gitignore` to exclude:
# - **Build artifacts and compiled code**: These are regenerated from source code
# - **Dependencies**: Like `node_modules/` or `venv/` – these can be recreated from requirements files
# - **Temporary files**: Cache files, log files, etc.
# - **Sensitive data**: Passwords, API keys, tokens – NEVER commit these!
# - **Large data files**: Git isn't designed for large binary files; use Git LFS or store separately
#
# **Why this matters**: Including generated files in Git creates unnecessary noise in your history
# and can cause merge conflicts when different machines generate slightly different versions. Worse,
# accidentally committing API keys or passwords can be a serious security breach.
#
# #### Common .gitignore Patterns
#
# ```gitignore
# # Python
# __pycache__/
# *.pyc
# *.pyo
# *.pyd
# .Python
# venv/
# env/
# *.egg-info/
# dist/
# build/
#
# # Jupyter
# .ipynb_checkpoints/
# *.ipynb_checkpoints
#
# # Data files (be careful with research data!)
# *.csv
# *.dat
# data/*.txt
#
# # OS files
# .DS_Store
# Thumbs.db
#
# # IDE
# .vscode/
# .idea/
# *.swp
#
# # Specific files
# secrets.txt
# config_local.py
# ```
#
# Create a `.gitignore` file in your repository root and Git will automatically ignore matching files.

# %% [markdown]
# ### Best Practices for Branching
#
# 1. **Keep branches focused**: One feature or fix per branch
# 2. **Use descriptive names**: `fix-data-loading` not `temp` or `test`
# 3. **Merge or delete completed branches**: Don't let them pile up
# 4. **Pull before you push**: Get latest changes from remote
# 5. **Commit often on branches**: Makes it easier to track progress

# %% [markdown]
# Now that you understand Git branching and merging workflows, let's explore how GitHub and GitLab
# extend Git with powerful collaboration features. These platforms transform Git from a personal
# version control tool into a collaborative research environment where teams can work together
# effectively.

# %% [markdown]
# ## Part 2: GitHub Collaboration
#
# ### GitHub Workflow Basics
#
# GitHub extends Git with collaboration features:
#
# #### Forking a Repository
#
# - Click "Fork" on GitHub to create your own copy
# - Clone your fork locally
# - Make changes on a branch
# - Push to your fork
# - Create a Pull Request to propose changes
#
# #### Pull Requests (PRs)
#
# A Pull Request is a request to merge your changes into another repository:
#
# 1. **Create**: After pushing a branch to GitHub, click "New Pull Request"
# 2. **Describe**: Explain what changes you made and why
# 3. **Review**: Others can comment on your code
# 4. **Update**: Push new commits to address feedback
# 5. **Merge**: Maintainer merges when ready
#
# #### Working with Remotes (this is not a GitHub feature!)
#
# ```bash
# # View remote repositories
# git remote -v
#
# # Add a remote (e.g., upstream original)
# git remote add upstream https://github.com/original/repo.git
#
# # Fetch changes from remote
# git fetch origin
# git fetch upstream
#
# # Pull changes (fetch + merge)
# git pull origin main
#
# # Push your changes
# git push origin my-branch
# ```

# %% [markdown]
# ### GitHub Best Practices
#
# 1. **Write clear PR descriptions**: Explain the problem and solution
# 2. **Keep PRs focused**: Small, reviewable changes
# 3. **Respond to reviews**: Address feedback promptly
# 4. **Use Issues**: Track bugs and feature requests
# 5. **Document in README**: Help others understand your project

# %% [markdown]
# ## Part 2b: GitLab Collaboration
#
# Don't want to use GitHub, fear not: GitLab is another popular platform for Git repository hosting and collaboration.
# While similar to GitHub, GitLab has some unique features and terminology.
#
# ### GitLab vs GitHub: Key Differences
#
# - **Merge Requests** (GitLab) vs **Pull Requests** (GitHub)
# - GitLab can be self-hosted or used on GitLab.com
# - Integrated CI/CD pipelines built into GitLab vs GitHub Actions
# - Different interface and feature set
#
# ### Forking in GitLab
#
# Forking in GitLab works similarly to GitHub:
#
# 1. **Navigate** to the project you want to fork
# 2. **Click "Fork"** in the upper-right corner
# 3. **Choose namespace**: Select where to create your fork (personal namespace or group)
# 4. **Configure fork options**:
#    - Edit project name and slug (URL)
#    - Choose which branches to include (all branches or only default)
#    - Set visibility level (public, internal, or private)
# 5. **Create fork**: GitLab creates your personal copy
#
# #### Keeping Your Fork Updated (will work similarly for all git remote repos)
#
# ```bash
# # Add the upstream repository
# git remote add upstream https://gitlab.com/original-owner/project.git
#
# # View your remotes
# git remote -v
# # origin    https://gitlab.com/your-username/project.git (fetch)
# # origin    https://gitlab.com/your-username/project.git (push)
# # upstream  https://gitlab.com/original-owner/project.git (fetch)
# # upstream  https://gitlab.com/original-owner/project.git (push)
#
# # Fetch changes from upstream
# git fetch upstream
#
# # Merge upstream changes into your main branch
# git checkout main
# git merge upstream/main
#
# # Push updates to your fork
# git push origin main
# ```
#
# GitLab also provides a UI button to update your fork directly from the web interface.

# %% [markdown]
# ### Merge Requests in GitLab
#
# Merge Requests (MRs) are GitLab's equivalent to GitHub's Pull Requests.
#
# #### Creating a Merge Request
#
# ```bash
# # Create a new branch in your fork
# git checkout -b feature-improvement
#
# # Make your changes
# # ... edit files ...
#
# # Commit and push to your fork
# git add .
# git commit -m "Add feature improvement"
# git push origin feature-improvement
# ```
#
# Then on GitLab:
#
# 1. **Navigate** to your fork on GitLab
# 2. **Click "Create merge request"** (appears after pushing a branch)
# 3. **Configure the merge request**:
#    - Choose source branch (your feature branch)
#    - Choose target branch (usually `main` in upstream)
#    - Select target project (upstream repository)
# 4. **Write description**: Explain your changes
#    - Use merge request templates if available
#    - Reference related issues with `#issue-number`
#    - Use closing patterns like `Closes #123` to auto-close issues
# 5. **Assign reviewers and assignees**
# 6. **Create merge request**
#
# #### Merge Request Features
#
# GitLab Merge Requests include:
#
# - **Inline code reviews**: Comment on specific lines
# - **Threaded discussions**: Track conversations
# - **Approval rules**: Require approvals before merging (Premium/Ultimate)
# - **CI/CD pipelines**: Automatic testing
# - **Auto-merge**: Merge automatically when conditions are met
# - **Draft status**: Mark MRs as work-in-progress
#
# #### Working with Remotes in GitLab
#
# ```bash
# # Clone your fork
# git clone https://gitlab.com/your-username/project.git
# cd project
#
# # Add upstream remote
# git remote add upstream https://gitlab.com/original-owner/project.git
#
# # Create a feature branch
# git checkout -b fix-bug
#
# # Make changes and commit
# # ... edit files ...
# git add .
# git commit -m "Fix critical bug"
#
# # Before pushing, sync with upstream
# git fetch upstream
# git rebase upstream/main
#
# # Push to your fork
# git push origin fix-bug
#
# # Create merge request on GitLab
# ```

# %% [markdown]
# ### GitLab Best Practices
#
# 1. **Use descriptive MR titles**: Summarize the change clearly
# 2. **Link to issues**: Connect MRs to related issues for context
# 3. **Keep MRs focused**: One feature or fix per merge request
# 4. **Use draft MRs**: Mark work-in-progress with "Draft:" prefix
# 5. **Respond to feedback**: Address reviewer comments promptly
# 6. **Use CI/CD**: Ensure pipelines pass before merging
# 7. **Squash commits**: Keep history clean (when appropriate)
# 8. **Update documentation**: Include docs in your changes

# %% [markdown]
# ### Comparison: GitHub vs GitLab Workflows
#
# | Feature | GitHub | GitLab |
# |---------|--------|--------|
# | Contribution model | Pull Request | Merge Request |
# | Fork update | Manual or sync fork button | Manual or update fork button |
# | Review process | Code review, comments | Code review, threaded discussions |
# | CI/CD | GitHub Actions | GitLab CI/CD (built-in) |
# | Project hosting | GitHub.com only | GitLab.com or self-hosted |
# | Issue tracking | GitHub Issues | GitLab Issues |
# | Draft/WIP | Draft Pull Request | Draft Merge Request |
#
# Both platforms support similar workflows - the choice often depends on:
# - Your organization's preference
# - Self-hosting requirements
# - Specific features needed
# - Existing infrastructure

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Experience collaborative workflows firsthand:</p>
#     <ul>
#         <li><strong>Create a practice PR/MR:</strong> Fork a small open-source project (or use a
#         personal test repo), make a meaningful improvement, and submit a pull request or merge
#         request</li>
#         <li><strong>Review someone else's code:</strong> Find an open PR in a project you're
#         interested in, read through the changes, and try to understand what they do and why</li>
#         <li><strong>Explore CI/CD in action:</strong> Look at the GitHub Actions or GitLab CI logs of
#         a real project to see how automated tests and checks work</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 3: Python Concepts You Need to Know
#
# This course assumes you can already read Python and have written at least a little of it
# before—it does not teach Python from scratch. What follows is a fast tour of the handful of
# Python patterns that show up repeatedly in the rest of this course: error handling, the `with`
# statement, comprehensions, and classes. The goal isn't to make you fluent in writing all of
# these from a blank page—it's so that when you see them later, whether you wrote them, a
# teammate did, or an AI assistant generated them, you can read them confidently and judge
# whether they're doing the right thing.
#
# ### Why Python for Research?
#
# - **Easy to learn**: Clear, readable syntax that resembles English
# - **Powerful libraries**: NumPy for numerical computing, pandas for data analysis, matplotlib for
#   visualization, scikit-learn for machine learning, and thousands more
# - **Interactive**: Jupyter notebooks let you explore data and test ideas interactively
# - **Community**: Large, helpful community with extensive documentation and Stack Overflow answers
# - **Cross-platform**: Write once, run anywhere—Windows, macOS, or Linux
# - **Research-ready**: Used across all scientific domains from genomics to astronomy to economics
#
# ### Why *Not* Python for Research?
#
# - **Performance limitations**: Slower than compiled languages like C or Fortran for compute-intensive tasks without optimization
# - **Dependency management headaches**: Version conflicts and environment issues can be frustrating to resolve
# - **Memory usage**: Large datasets can quickly consume RAM, especially without careful optimization, no full control over memory
# - **Global Interpreter Lock (GIL)**: Limits true multi-threaded CPU-bound parallelism
# - **Dynamic typing pitfalls**: Type-related bugs may only appear at runtime
# - **Scaling challenges**: May require additional frameworks (e.g., distributed computing tools) for very large-scale workloads
#
#
# **Fun fact**: Python is named after Monty Python's Flying Circus, not the snake! The language was
# designed to be fun to use, and you'll often see Monty Python references in Python documentation.

# %% [markdown]
# ### Reading and Handling Errors
#
# Errors are inevitable in programming—even experienced developers encounter them daily. The
# difference between beginner and professional code is how errors are handled. Good programs
# anticipate what can go wrong and handle errors gracefully, providing useful feedback instead
# of crashing. This is especially important in research software, where a crash during a long
# experiment can waste hours or days of computation time. It also matters when reading
# AI-generated code: an assistant will happily hand you a function with no error handling at
# all, and it's your job to notice and decide whether that's acceptable.
#
# Python has many built-in exception types. Understanding the most common ones helps you read
# error-handling code and debug problems faster.

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
# ### Try-Except Blocks
#
# Use try-except to catch and handle errors. The basic pattern is: try to do something that might
# fail, and if it fails, handle the error gracefully instead of crashing.
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
# or raise a different exception—choose based on how you want errors to be handled in your
# application.
#
# ### Raising Exceptions
#
# You can raise your own exceptions for error conditions. This is how you enforce rules in your
# functions and provide clear error messages when something goes wrong. Raising exceptions is
# better than returning error codes or special values (like -1 or None) because it forces the
# caller to handle the error, provides a clear message, and stops execution if not handled.
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
# **Common pitfall**: Don't use bare `except:` without specifying the exception type—it will catch
# EVERYTHING, including KeyboardInterrupt (Ctrl+C), making your program hard to stop. Always specify
# the exception types you're catching, or at minimum use `except Exception:`. When you see an AI
# assistant hand you a bare `except:`, that's worth pushing back on.

# %% [markdown]
# ### The `with` Statement and File Handling
#
# Python reads and writes files using the built-in `open()` function. The recommended pattern is
# the `with` statement, which automatically closes the file when the block ends—even if an error
# occurs inside it. `open()` is Python's most common example of a **context manager**: an object
# that defines setup and teardown behavior around a `with` block. You'll meet the same idiom
# again in Lecture 11 when working with HDF5 files (`with h5py.File(...) as f:`)—same pattern,
# different resource being managed.

# %%
from io import StringIO

# StringIO behaves like a file object, so it supports the same `with` pattern as
# open()—useful here so this cell doesn't touch your filesystem. Try removing the
# `with` and calling buffer.read() afterwards: it raises ValueError, because the
# `with` block already closed the buffer for you.
with StringIO("23.5\n24.1\n23.8\n") as buffer:
    for line in buffer:
        print(f"Read: {line.strip()}")

# %% [markdown]
# That's the mechanics of `with`. Real research data is rarely this clean, though—here's a more
# complete example that also skips comment lines and blank lines, and handles values that don't
# parse as numbers.

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
# **Why this matters beyond files**: any resource that needs cleanup—a file, a database
# connection, a network socket, a temporary test environment—tends to show up behind a `with`
# statement in Python. Recognizing the pattern (`with <get a resource> as <name>:`) matters more
# than memorizing file-specific syntax.

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Practice reading and handling errors:</p>
#     <ul>
#         <li><strong>Trigger real errors:</strong> Uncomment one of the examples above (e.g.
#         <code>int("not a number")</code>) and run it to see the actual traceback Python
#         produces—then wrap it in a <code>try</code>/<code>except</code> that handles it
#         gracefully.</li>
#         <li><strong>Add validation:</strong> Extend <code>validate_temperature</code> with a check
#         for a new precondition (e.g. temperature must be a number, not a string) and raise an
#         appropriate exception.</li>
#         <li><strong>Read someone else's <code>with</code> block:</strong> Find any Python code
#         online (or ask an AI assistant to generate one) that uses <code>with open(...) as f:</code>,
#         and explain in your own words what happens if an error occurs partway through the
#         block.</li>
#     </ul>
# </div>

# %% [markdown]
# ### List and Dictionary Comprehensions
#
# List comprehensions provide elegant, concise ways to create and transform lists. They're not just
# syntactic sugar—they're often faster than traditional loops and make your code's intent clearer.
# In research contexts, you'll see them constantly for data filtering, transformation, and
# processing, including in code an AI assistant generates for you.
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
sample_temperatures = [23.5, 24.1, 23.8, 24.3, 23.9]

# Create dictionary
temp_dict = {sample: temp for sample, temp in zip(samples, sample_temperatures)}
print(f"Temperature dictionary: {temp_dict}")

# Filter dictionary
high_temp_dict = {s: t for s, t in temp_dict.items() if t > 24.0}
print(f"High temperatures: {high_temp_dict}")

# %% [markdown]
# ### Classes and Object-Oriented Programming
#
# Classes allow you to bundle data and functionality together. They're essential for organizing
# complex research code and are heavily used in testing frameworks like pytest, which is where
# you'll put this to direct use in Lecture 5.
#
# **Why use classes?**
# - **Organization**: Group related data and functions together
# - **Reusability**: Create multiple instances with the same behavior
# - **Clarity**: Model real-world entities (experiments, datasets, instruments)
# - **Testing**: Organize test cases (test classes in pytest)


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
# **Understanding `self` and `__init__`**:
# - **`__init__`**: Special method called when creating a new instance (constructor)
# - **`self`**: Refers to the instance itself (like "this" in other languages)
# - **Instance variables**: `self.location`, `self.measurements` belong to each instance
# - **Methods**: Functions defined inside a class that operate on instance data

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
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Practice reading comprehensions and classes:</p>
#     <ul>
#         <li><strong>Refactor a loop:</strong> Take a traditional for-loop with an <code>if</code>
#         check and rewrite it as a list comprehension—compare readability.</li>
#         <li><strong>Extend <code>TemperatureData</code>:</strong> Add a method
#         <code>get_range()</code> that returns the minimum and maximum recorded temperature.</li>
#         <li><strong>Read AI-generated code:</strong> Ask an AI assistant to write a small class for
#         a research object you care about (an experiment, a sample, a dataset), and identify the
#         <code>__init__</code>, instance variables, and methods before running it.</li>
#     </ul>
# </div>

# %% [markdown]
# ## Summary
#
# In this lecture, we covered:
#
# ### Advanced Git
# - **Branching**: Creating isolated development environments
# - **Merging**: Combining branches and resolving conflicts
# - **.gitignore**: Managing which files Git tracks
# - **Best practices**: Workflow tips for effective version control
#
# ### GitHub Collaboration
# - **Forking and Pull Requests**: Contributing to projects on GitHub
# - **Remote repositories**: Working with GitHub
# - **Collaboration best practices**: Effective teamwork on GitHub
#
# ### GitLab Collaboration
# - **Forking in GitLab**: Creating personal copies of projects
# - **Merge Requests**: GitLab's contribution workflow
# - **Remote management**: Syncing with upstream repositories
# - **Platform comparison**: Understanding GitHub vs GitLab differences
#
# ### Python Concepts for RSE
# - **Error handling**: Reading and writing `try`/`except`/`raise`, recognizing common exception types
# - **Context managers**: The `with` statement pattern for managing resources like files
# - **Comprehensions**: List and dictionary comprehensions for concise data transformations
# - **Classes**: Basic object-oriented syntax—`__init__`, `self`, instance methods—used throughout
#   the rest of the course, especially in testing (Lecture 5)

# %% [markdown]
# ## Acknowledgements and References
#
# This lecture builds upon concepts from multiple authoritative sources:
#
# ### Primary Sources
#
# - **Research Software Engineering with Python** by The Alan Turing Institute
#   <https://alan-turing-institute.github.io/rse-course/html/>
#   Git branching workflows, collaboration patterns, and Python concepts content adapted from this course.
#
# - **Research Software Engineering with Python** by Damien Irving, Kate Hertweck,
#   Luke Johnston, Joel Ostblom, Charlotte Wickham, and Greg Wilson (2022)
#   <https://third-bit.com/py-rse/>
#   Python fundamentals and best practices informed by this comprehensive
#   textbook.
#
# ### Platform Documentation
#
# - **GitHub Documentation**
#   <https://docs.github.com/>
#   - Pull Requests: <https://docs.github.com/en/pull-requests>
#   - Forking Workflow: <https://docs.github.com/en/get-started/quickstart/fork-a-repo>
#   - Branch Protection:
#     <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches>
#   - GitHub Flow: <https://docs.github.com/en/get-started/quickstart/github-flow>
#
# - **GitLab Documentation**
#   <https://docs.gitlab.com/>
#   - Merge Requests: <https://docs.gitlab.com/ee/user/project/merge_requests/>
#   - GitLab Flow: <https://docs.gitlab.com/ee/topics/gitlab_flow.html>
#   - Forking Workflow: <https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html>
#
# ### Additional Resources
#
# - **Pro Git Book** by Scott Chacon and Ben Straub
#   <https://git-scm.com/book/en/v2>
#   Advanced Git concepts including branching, merging, and conflict resolution.
#
# - **Software Carpentry: Version Control with Git**
#   <https://swcarpentry.github.io/git-novice/>
#   Collaborative Git workflows and best practices.
#
# - **Python Documentation**
#   <https://docs.python.org/3/>
#   Official Python language reference for syntax and built-in types.
#
# ### Notes
#
# The lecture structure, examples, and exercises have been developed specifically for this course,
# drawing on best practices from the sources above. Platform-specific content (GitHub/GitLab)
# references official documentation to ensure accuracy.

# %% [markdown]
# ### Next Steps
#
# With Git, GitHub/GitLab, and the core Python patterns behind us, Lecture 3 turns to a topic
# that shapes how you'll write code for the rest of this course and beyond: AI-assisted and
# agentic coding tools. We'll look at what these tools actually do, where they go wrong, and how
# the fundamentals from this course help you use them responsibly.
#
# **Ready to continue? Move on to Lecture 3!**
