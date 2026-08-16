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
# # Lecture 10: Collaboration and Code Review in Research Software
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
#     <img src="lecture_10_qr_code.png" alt="This Lecture QR Code" width="150"/>
#     <p><strong>This Lecture</strong></p>
#   </div>
# </div>
#
# ## Overview
# This lecture explores how to work effectively in research software teams, from code
# reviews and pull requests to onboarding new collaborators. Research is increasingly
# collaborative, and your software needs to support multiple contributors while
# maintaining quality and reproducibility. We'll examine practical workflows for team
# collaboration, effective code review practices, and how to build a welcoming
# community around your research software.
#
# **Duration**: ~90 minutes
#
# ## Prerequisites
#
# Before starting this lecture, you should be familiar with:
# - Git branching and merging (covered in Lecture 2)
# - GitHub/GitLab basics including pull/merge requests
# - Writing and testing Python code (covered in Lectures 2-5)
# - Code review concepts from earlier lectures
# - AI-assisted coding basics, including reviewing AI suggestions like a diff (covered in
#   Lecture 3)
#
# This lecture builds on your Git knowledge and introduces systematic collaboration practices.
#
# ## Learning Objectives
# - Understand why collaboration requires deliberate processes and practices
# - Master the pull request workflow for collaborative development
# - Conduct effective and constructive code reviews
# - Handle merge conflicts and coordinate with team members
# - Onboard new contributors to research projects
# - Apply collaboration practices across different version control platforms
# - Navigate team dynamics and communication challenges
# - Adapt collaboration practices for different programming languages
# - Review AI-assisted and agentic pull requests with the same rigor as any other PR, and
#   apply a clear attribution norm for AI-authored contributions

# %% [markdown]
# ## Part 1: Why Collaboration Is Hard - A Research Lab Story
#
# ### The Single-Developer Comfort Zone
#
# Dr. James Park had been developing his climate simulation software for three years.
# He knew every line of code, every quirk, every optimization. His workflow was simple:
# - Write code directly on the `main` branch
# - Commit when features work
# - No code reviews (who would review?)
# - Documentation? "I know how it works"
#
# The code worked perfectly - for him.
#
# ### The Growth Phase: Adding Collaborators
#
# James's research gained attention. His lab hired:
# - **Lisa**: Postdoc expert in data analysis
# - **Raj**: PhD student working on new algorithms
# - **Maya**: Research software engineer improving performance
#
# **Week 1** - Excitement:
# ```bash
# # Everyone clones the repository
# git clone https://github.com/jpark/climate-sim.git
# # Everyone starts coding...
# ```
#
# **Week 2** - Chaos:
# - Lisa pushed code that broke Raj's simulations
# - Raj's commit overwrote Maya's performance improvements
# - Maya couldn't understand James's variable names (`tmp_x2`, `calc_v3_FINAL`)
# - James spent 15 hours fixing merge conflicts
# - Nobody knew which version of the code produced which results
#
# **Week 3** - Crisis:
# - A critical bug in the main branch delayed everyone's research
# - Nobody could identify who introduced it (no code reviews)
# - The team wasted a week tracking it down
# - Tensions rose: "Why didn't you test before pushing?"
#
# ### The Transformation
#
# The lab brought in a research software engineering consultant who introduced:
# - **Branch-based workflow**: Feature branches instead of working on `main`
# - **Pull requests**: All changes reviewed before merging
# - **Code review checklist**: Consistent quality standards
# - **Communication protocols**: Clear expectations and feedback
# - **Documentation requirements**: Every PR needs updated docs
#
# **Three months later:**
# - 5 contributors working smoothly
# - Zero conflicts on main branch
# - Bugs caught in review before merging
# - New contributors onboarded in days, not weeks
# - Improved code quality across the board
# - Published results with clear attribution
#
# **The lesson**: Good collaboration requires **process**, not just **Git**.

# %% [markdown]
# ## Part 2: The Pull Request Workflow
#
# ### Understanding Pull Requests
#
# A **Pull Request (PR)** (GitHub) or **Merge Request (MR)** (GitLab) is a formal
# request to merge your changes into another branch. It's not just about code - it's
# about **communication** and **collaboration**.
#
# **What a PR provides:**
# - ✅ Place for discussion about changes
# - ✅ Code review before merging
# - ✅ Automated testing (CI/CD)
# - ✅ Documentation of why changes were made
# - ✅ Clear attribution of contributions
# - ✅ Opportunity to catch problems early
#
# ### The Standard Git Workflow for Teams
#
# **Step 1: Sync with main branch**
# ```bash
# # Start with updated main
# git checkout main
# git pull origin main
# ```
#
# **Step 2: Create a feature branch**
# ```bash
# # Use descriptive names
# git checkout -b fix/temperature-calculation
# # NOT: git checkout -b mybranch
# # NOT: git checkout -b temp
# ```
#
# **Branch naming conventions:**
# - `feature/add-wind-speed-model` - New functionality
# - `fix/correct-precipitation-units` - Bug fixes
# - `docs/update-api-reference` - Documentation
# - `refactor/simplify-data-loading` - Code improvements
# - `test/add-climate-validation` - Test additions
#
# **Step 3: Make your changes**
# ```bash
# # Edit files, test locally
# python simulate_climate.py
# pytest tests/
#
# # Commit with clear messages
# git add src/temperature.py tests/test_temperature.py
# git commit -m "Fix temperature calculation for polar regions
#
# - Correct formula for temperatures below -50°C
# - Add test cases for Arctic/Antarctic conditions
# - Resolves issue #42"
# ```
#
# **Step 4: Push your branch**
# ```bash
# git push origin fix/temperature-calculation
# ```
#
# **Step 5: Open a pull request**
# - Go to GitHub/GitLab repository
# - Click "New Pull Request" / "New Merge Request"
# - Select: `main` ← `fix/temperature-calculation`
# - Fill in the PR template (see next section)
# - Request reviewers
# - Submit
#
# **Step 6: Address review comments**
# ```bash
# # Make requested changes
# git add src/temperature.py
# git commit -m "Address review: Add bounds checking"
# git push origin fix/temperature-calculation
# # PR updates automatically!
# ```
#
# **Step 7: Merge after approval**
# - Reviewer approves
# - CI tests pass ✅
# - Merge the PR (squash, rebase, or merge commit - team decision)
# - Delete the feature branch
#
# ### Platform Comparison: GitHub vs GitLab
#
# **GitHub Pull Requests:**
# - Called "Pull Requests" (PRs)
# - Located: Repository → Pull requests tab
# - Can assign reviewers, labels, milestones
# - Draft PRs available for work-in-progress
# - Can require approval before merging
# - Supports automated review requests
#
# **GitLab Merge Requests:**
# - Called "Merge Requests" (MRs)
# - Located: Repository → Merge requests
# - Similar review and approval workflow
# - Additional features: Approval rules, merge trains
# - Can mark MRs as "Work in Progress" (WIP)
# - Supports multiple approval rules per repository
#
# **Both platforms support:**
# - Inline code comments
# - Discussion threads
# - CI/CD integration
# - Protected branch rules
# - Auto-merge when conditions met

# %% [markdown]
# ## Part 3: Writing Effective Pull Requests
#
# ### The Anatomy of a Good PR
#
# A pull request is **documentation** of your changes. Make it easy for reviewers
# to understand what you did and why.
#
# **Bad PR description:**
# ```
# Title: Fix bug
#
# Description: Fixed the thing
# ```
#
# **Good PR description:**
# ```
# Title: Fix temperature calculation for polar regions
#
# ## Problem
# Temperature calculations were producing incorrect values for regions with
# temperatures below -50°C. The current formula doesn't account for the
# non-linear behavior of air at extreme cold.
#
# ## Solution
# - Updated temperature calculation formula in src/temperature.py
# - Added special handling for temperatures < -50°C
# - Implemented the Clausius-Clapeyron relation for polar conditions
#
# ## Testing
# - Added unit tests for Arctic and Antarctic test cases
# - Validated against NSIDC observational data
# - All existing tests still pass
#
# ## References
# - Fixes #42
# - Related to climate model validation project
# - Based on formula from Smith et al. (2023), J. Climate
#
# ## Checklist
# - [x] Tests added and passing
# - [x] Documentation updated
# - [x] CHANGELOG.md updated
# - [x] Code follows project style guide
# ```
#
# ### PR Template
#
# Create `.github/pull_request_template.md` (GitHub) or
# `.gitlab/merge_request_templates/Default.md` (GitLab):
#
# ```markdown
# ## Description
# <!-- Briefly describe what this PR does and why -->
#
# ## Type of Change
# - [ ] Bug fix (non-breaking change fixing an issue)
# - [ ] New feature (non-breaking change adding functionality)
# - [ ] Breaking change (fix or feature causing existing functionality to change)
# - [ ] Documentation update
#
# ## Testing
# <!-- Describe the tests you ran and how to reproduce them -->
# - [ ] All existing tests pass
# - [ ] New tests added for new functionality
# - [ ] Tested on multiple platforms/environments
#
# ## Checklist
# - [ ] Code follows project style guidelines
# - [ ] Self-review completed
# - [ ] Comments added for complex code
# - [ ] Documentation updated (if applicable)
# - [ ] No new warnings generated
# - [ ] Dependent changes merged and published
#
# ## References
# <!-- Link to related issues, papers, or discussions -->
# Fixes #
# ```

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Want to build your team's review culture? Here's how to start:</p>
#     <ul>
#         <li><strong>Create your team's standards</strong>: Gather your research group and
#         draft a simple review checklist. What matters most to your projects? Start with
#         5-7 items.</li>
#         <li><strong>Customize the PR template</strong>: Copy the template above into your
#         repository's <code>.github/pull_request_template.md</code>. Adapt it to your
#         team's needs - remove what doesn't fit, add what's missing.</li>
#         <li><strong>Practice with old PRs</strong>: Go back to a merged PR from your
#         project. Review it using your new checklist. What would you have caught? What
#         questions would you ask?</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 4: Code Review - The Art of Constructive Feedback
#
# ### Why Code Review Matters
#
# Code review is **not** about finding faults - it's about:
# - ✅ **Catching bugs** before they reach production
# - ✅ **Sharing knowledge** across the team
# - ✅ **Maintaining consistency** in code style and practices
# - ✅ **Improving design** through discussion
# - ✅ **Onboarding** new contributors
# - ✅ **Building quality culture** in the team
#
# Research shows code review catches 60% of defects that would slip through testing.
#
# ### What to Look for in Code Review
#
# **1. Correctness**
# - Does the code do what it claims?
# - Are algorithms implemented correctly?
# - Are edge cases handled?
# - Are units and dimensions correct? (Critical in scientific code!)
#
# ```python
# # ❌ Problematic
# def calculate_energy(mass):
#     return mass * 3e8 ** 2  # Should this be (3e8)**2?
#
# # ✅ Better
# def calculate_energy_joules(mass_kg):
#     """Calculate energy using E=mc^2.
#
#     Parameters
#     ----------
#     mass_kg : float
#         Mass in kilograms
#
#     Returns
#     -------
#     float
#         Energy in joules
#     """
#     SPEED_OF_LIGHT_M_PER_S = 299792458  # m/s
#     return mass_kg * SPEED_OF_LIGHT_M_PER_S ** 2
# ```
#
# **2. Testing**
# - Are there tests for new functionality?
# - Do tests cover edge cases?
# - Are test names descriptive?
#
# ```python
# # ❌ Weak test
# def test_calc():
#     assert calculate_energy(1) > 0
#
# # ✅ Strong test
# def test_calculate_energy_for_one_kg():
#     """Test E=mc^2 for 1 kg mass."""
#     mass_kg = 1.0
#     expected_joules = 8.987551787e16  # 1 kg * c^2
#     actual_joules = calculate_energy_joules(mass_kg)
#     assert abs(actual_joules - expected_joules) < 1e10  # Within 0.01%
# ```
#
# **3. Documentation**
# - Are functions documented?
# - Is complex logic explained?
# - Are assumptions stated?
# - Are units specified?
#
# **4. Code Style and Readability**
# - Consistent with project conventions?
# - Variable names descriptive?
# - Functions small and focused?
# - No unnecessary complexity?
#
# **5. Performance (when relevant)**
# - Are there obvious inefficiencies?
# - Is the approach scalable?
# - Are there better algorithms available?
#
# **6. Security (when relevant)**
# - Are user inputs validated?
# - Are file paths sanitized?
# - Are credentials handled safely?
#
# ### How to Give Constructive Feedback
#
# **❌ Destructive comments:**
# ```
# "This code is terrible"
# "Did you even test this?"
# "You obviously don't understand Python"
# "Why would you do it this way?"
# ```
#
# **✅ Constructive comments:**
# ```
# "This implementation might have issues with negative inputs.
#  Could we add input validation?"
#
# "I think we could simplify this by using numpy.clip() here.
#  What do you think?"
#
# "Great approach! One suggestion: adding a docstring would help
#  future contributors understand the algorithm."
#
# "I'm not sure I understand the logic here. Could you add a
#  comment explaining why we multiply by 2?"
# ```
#
# ### The "Yes, and..." Technique
#
# Instead of "No, but..." use "Yes, and...":
#
# **❌ "No, but..."**
# ```
# "No, this won't work for large datasets."
# ```
#
# **✅ "Yes, and..."**
# ```
# "This works well for small datasets! For scaling to larger data,
#  we might want to consider using Dask for parallel processing.
#  What do you think about implementing that as a follow-up PR?"
# ```
#
# ### Praise Good Work
#
# Don't just point out problems - acknowledge good work:
#
# ```
# "Excellent test coverage! The edge cases you covered will prevent
#  bugs down the line."
#
# "I really like how you documented the assumptions. This makes the
#  code much easier to understand."
#
# "Smart optimization! Using vectorization here is much cleaner than
#  the loop we had before."
# ```

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Ready to practice constructive code review? Try these approaches:</p>
#     <ul>
#         <li><strong>Review a colleague's code</strong>: Ask a lab mate if you can review
#         one of their recent PRs or scripts. Focus on being helpful, not critical. Did
#         they appreciate your feedback?</li>
#         <li><strong>Get your code reviewed</strong>: Share a small piece of your code and
#         explicitly ask for feedback on readability and design. What did you learn? What
#         surprised you?</li>
#         <li><strong>Practice "Yes, and..."</strong>: Next time you see code you'd do
#         differently, start your comment with "This works, and we could also..." Notice
#         how the tone changes!</li>
#     </ul>
# </div>

# %% [markdown]
# ### Reviewing AI-Assisted and Agentic Pull Requests
#
# Agentic tools are genuinely good at producing a complete, consistent first draft across
# several files at once—applying the same fix pattern everywhere it's needed, or scaffolding a
# multi-file feature—faster than typing it out by hand. What they're not automatically good at
# is knowing when that draft is actually ready for someone else to build on. Everything above
# about giving and receiving feedback still applies whether a human or an AI assistant wrote
# the code under review—the review process doesn't get a "trust me, an AI wrote it" exemption,
# and it doesn't get an extra-suspicious one either. What does change is scale: an agentic tool
# can open a PR touching several files in one step, the way Lecture 3 discussed. A five-line
# diff gets a five-line review; a fifty-line, five-file diff needs the same scrutiny you'd give
# a colleague's PR of that size, not the glance you'd give a one-line autocomplete suggestion.
#
# ### A Note on Attribution
#
# If an AI assistant wrote or substantially contributed to a commit, say so—many teams use a
# trailer in the commit message (for example, `Co-Authored-By: <tool name>`) to record it,
# similar to how you'd credit a human collaborator. This isn't about assigning blame; it's about
# provenance. A future maintainer (including you, in six months) benefits from knowing which
# parts of the history came from an assistant, the same way version control already tracks who
# wrote what and when.
#
# ### Practice: Reviewing an Agentic PR
#
# Suppose an agentic tool was asked to "add a moving average function to smooth a temperature
# time series" and opened this PR:


# %%
def moving_average(readings, window):
    """Compute the moving average of readings using the given window size."""
    result = []
    for i in range(len(readings)):
        window_readings = readings[max(0, i - window) : i]
        result.append(sum(window_readings) / window)
    return result


# %% [markdown]
# Applying the review habits from this lecture and Lecture 3—read it like a diff, and verify
# against a case you can check by hand—let's see what it does with a short series:

# %%
readings = [10, 20, 30, 40, 50]
print([round(v, 2) for v in moving_average(readings, window=3)])

# %% [markdown]
# Only the last two entries are correct 3-point averages: `[10, 20, 30]` → `20.0` and
# `[20, 30, 40]` → `30.0`, once the window is actually full. The first three are wrong in a way
# that's easy to miss: at `i=0` there are no prior readings at all, yet the function still
# divides by `window` (3), silently producing `0.0`. At `i=1`, only one reading is available
# (`[10]`), but it's still divided by 3, giving `3.33` instead of `10`. At `i=2`, two readings
# are available (`[10, 20]`), divided by 3 again, giving `10.0` instead of `15.0`. The bug is
# real, but it's invisible unless you check a case where the window isn't full yet—exactly the
# kind of boundary a quick skim misses and a hand-calculated check catches.
#
# **How prompting helps (but doesn't replace review)**: a prompt that names the edge case up
# front—"add a moving_average function; for indices before the window is fully populated,
# average over whatever data is actually available"—is much less likely to produce this exact
# bug. But "less likely" isn't "guaranteed," and a well-specified prompt for this function might
# still miss a different edge case neither of us thought to name. The review habit is what
# catches whichever one shows up.

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Practice reviewing AI-assisted contributions:</p>
#     <ul>
#         <li><strong>Write the review comment:</strong> Using the constructive feedback
#         techniques from this lecture, write the PR comment you'd leave on
#         <code>moving_average</code>—identify the bug and suggest what the function should do
#         at the boundaries.</li>
#         <li><strong>Fix it and re-verify:</strong> Rewrite <code>moving_average</code> so it
#         either skips indices without a full window or averages over however many readings are
#         actually available—then check it against the same hand-calculated case.</li>
#         <li><strong>Decide your team's attribution norm:</strong> Would you want AI-assisted
#         commits marked in your own project's history? Write one sentence for a
#         CONTRIBUTING.md explaining the policy and why.</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 5: Handling Review Feedback
#
# ### Receiving Feedback Professionally
#
# **Remember:**
# - Reviewers are critiquing **code**, not **you**
# - Everyone's goal is better software
# - Even experienced developers get feedback
# - Questions are opportunities to improve documentation
#
# **Good responses to feedback:**
#
# ```
# "Great catch! I'll add input validation."
#
# "Good point about edge cases. I've added tests for empty arrays."
#
# "I hadn't considered that scenario. Let me update the implementation."
#
# "You're right that the docstring was unclear. I've rewritten it."
#
# "Interesting suggestion! I chose approach A because of memory
#  constraints, but let me document that decision in a comment."
# ```
#
# ### When to Push Back (Politely)
#
# It's okay to disagree if you have good reasons:
#
# ```
# "I considered using approach B, but it performs poorly with our
#  typical dataset sizes (see benchmark results attached). I think
#  approach A is better for our use case, but I'm open to discussion."
#
# "The additional abstraction you suggested would be valuable if we
#  had multiple implementations. Since this is our only use case,
#  I think the simpler approach is more maintainable. What do you think?"
# ```
#
# ### Resolving Disagreements
#
# If you and reviewers disagree:
#
# **1. Understand their perspective**
# - Ask clarifying questions
# - Consider their expertise
# - Look for the underlying concern
#
# **2. Provide context**
# - Explain your reasoning
# - Share relevant benchmarks/data
# - Reference documentation or papers
#
# **3. Seek consensus**
# - Propose compromises
# - Invite third opinions
# - Focus on project goals, not personal preference
#
# **4. Document the decision**
# - Add comments explaining why you chose this approach
# - Update documentation if needed
# - Record decision in PR discussion for future reference

# %% [markdown]
# ## Part 6: Merge Conflicts and How to Handle Them
#
# ### Understanding Merge Conflicts
#
# A **merge conflict** occurs when Git can't automatically merge changes because
# multiple people edited the same lines of code differently.
#
# **Scenario:**
# ```python
# # Original code in main branch
# def calculate_temperature(kelvin):
#     return kelvin - 273.15
# ```
#
# **Your branch:**
# ```python
# def calculate_temperature(kelvin):
#     """Convert Kelvin to Celsius."""
#     return kelvin - 273.15
# ```
#
# **Colleague's branch (merged first):**
# ```python
# def calculate_temperature_celsius(kelvin):
#     return kelvin - 273.15
# ```
#
# When you try to merge, Git doesn't know which change to keep.
#
# ### Resolving Conflicts - Step by Step
#
# **Step 1: Update your branch**
# ```bash
# # On your feature branch
# git checkout fix/temperature-calculation
# git fetch origin
# git merge origin/main
# # Conflict detected!
# ```
#
# **Step 2: Identify conflicting files**
# ```bash
# git status
# # Shows:
# # both modified:   src/temperature.py
# ```
#
# **Step 3: Open the file and examine conflict markers**
# ```python
# <<<<<<< HEAD (your changes)
# def calculate_temperature(kelvin):
#     """Convert Kelvin to Celsius."""
#     return kelvin - 273.15
# =======
# def calculate_temperature_celsius(kelvin):
#     return kelvin - 273.15
# >>>>>>> origin/main (their changes)
# ```
#
# **Step 4: Resolve the conflict**
#
# You need to decide how to combine the changes. Options:
# - Keep your version only
# - Keep their version only
# - Combine both changes
# - Write something entirely new
#
# ```python
# # Resolution: Keep rename and add docstring
# def calculate_temperature_celsius(kelvin):
#     """Convert temperature from Kelvin to Celsius.
#
#     Parameters
#     ----------
#     kelvin : float
#         Temperature in Kelvin
#
#     Returns
#     -------
#     float
#         Temperature in Celsius
#     """
#     return kelvin - 273.15
# ```
#
# **Step 5: Mark as resolved and commit**
# ```bash
# git add src/temperature.py
# git commit -m "Merge main and resolve temperature function conflict
#
# - Kept function rename from main branch
# - Added docstring from feature branch"
# git push origin fix/temperature-calculation
# ```
#
# ### Preventing Conflicts
#
# **Best practices:**
# - ✅ **Keep PRs small** - easier to review and merge
# - ✅ **Sync frequently** - merge main into your branch regularly
# - ✅ **Communicate** - let team know what you're working on
# - ✅ **Modular code** - different people work on different modules
# - ✅ **Fast reviews** - don't let PRs sit for weeks
#
# ### GitLab Merge Strategies
#
# Both GitHub and GitLab offer different merge strategies:
#
# **1. Merge Commit** (default)
# - Creates explicit merge commit
# - Preserves full history
# - Can make history complex
#
# **2. Squash and Merge**
# - Combines all commits into one
# - Clean linear history
# - Loses intermediate commit history
#
# **3. Rebase and Merge**
# - Replays commits on top of main
# - Linear history without merge commits
# - Rewrites commit history (use with care)
#
# **Team decision**: Choose one strategy and document it in CONTRIBUTING.md

# %% [markdown]
# ## Part 7: Onboarding New Team Members
#
# ### The First Day Experience
#
# **Bad onboarding:**
# ```
# "Here's the repository. Good luck!"
# ```
# Result: Confused contributor, wasted time, frustration
#
# **Good onboarding:**
# - Welcome message with clear first steps
# - Documentation for setting up development environment
# - "Good first issue" labels on suitable tasks
# - Designated mentor for questions
# - Checklist of onboarding tasks
#
# ### Creating a CONTRIBUTING.md
#
# Every project should have clear contribution guidelines:
#
# ```markdown
# # Contributing to Climate Simulation Project
#
# Thank you for contributing! We value your input.
#
# ## Getting Started
#
# 1. Fork the repository
# 2. Clone your fork: `git clone https://github.com/yourusername/climate-sim.git`
# 3. Set up development environment: `make install-dev`
# 4. Run tests to verify setup: `pytest tests/`
#
# ## Development Workflow
#
# 1. Create a feature branch: `git checkout -b feature/your-feature-name`
# 2. Make your changes
# 3. Run tests: `pytest tests/`
# 4. Run linter: `flake8 src/`
# 5. Commit with descriptive message
# 6. Push and create a Pull Request
#
# ## Code Style
#
# - Follow PEP 8 for Python code
# - Use type hints for function signatures
# - Add docstrings (NumPy style) for all public functions
# - Keep functions under 50 lines when possible
# - Write descriptive variable names (no single letters except i, j, k in loops)
#
# ## Testing Requirements
#
# - All new features must include tests
# - Maintain >90% code coverage
# - Tests must be fast (<1 second each)
# - Use descriptive test names: `test_<what>_<condition>_<expected>`
#
# ## Pull Request Process
#
# 1. Fill in the PR template completely
# 2. Request review from at least one team member
# 3. Address all review comments
# 4. Ensure CI tests pass
# 5. Squash commits before merging (if requested)
#
# ## Code Review Guidelines
#
# - Reviews should be completed within 2 business days
# - Be constructive and respectful
# - Focus on code, not the person
# - Ask questions rather than make demands
# - Acknowledge good work
#
# ## Getting Help
#
# - Questions about code: Open a GitHub Discussion
# - Bug reports: Open an Issue with the bug template
# - Security issues: Email security@example.org
# - General chat: Join our Slack channel
#
# ## Good First Issues
#
# Look for issues labeled `good-first-issue` - these are specifically
# selected for new contributors and include extra guidance.
# ```
#
# ### Mentoring New Contributors
#
# **For new contributors, be extra supportive:**
#
# ```
# "Welcome! Thanks for your first contribution to the project.
#
#  I see you're working on [feature]. Here are a few tips:
#  - Our test files are in tests/
#  - We use pytest for testing
#  - Check out other test files for examples
#
#  Don't hesitate to ask questions - we're here to help!"
# ```
#
# **When reviewing first PRs:**
# - Be encouraging
# - Explain the "why" behind suggestions
# - Point to examples in the codebase
# - Acknowledge effort
# - Offer to pair program for complex changes

# %% [markdown]
# ## Part 8: Communication and Team Dynamics
#
# ### Choosing the Right Communication Channel
#
# Different channels for different purposes:
#
# **GitHub/GitLab Issues:**
# - Bug reports
# - Feature requests
# - Task tracking
# - Public, searchable, permanent
#
# **Pull/Merge Request comments:**
# - Code-specific discussions
# - Implementation questions
# - Review feedback
# - Tied to specific changes
#
# **GitHub Discussions / GitLab Wikis:**
# - General questions
# - Design discussions
# - Community announcements
# - Less formal than issues
#
# **Slack/Discord/Mattermost:**
# - Quick questions
# - Real-time collaboration
# - Team coordination
# - Not searchable long-term (free tiers)
#
# **Email:**
# - Formal communications
# - External collaborators
# - Confidential matters
# - Long-form discussions
#
# **Video calls:**
# - Complex discussions
# - Pair programming
# - Team meetings
# - Onboarding sessions
#
# **Rule of thumb:**
# - Decisions should be documented in GitHub/GitLab
# - Chat is for quick coordination
# - If a chat discussion leads to a decision, document it in an issue
#
# ### Asynchronous Collaboration
#
# Research teams are often distributed across time zones. Write for async:
#
# **❌ Synchronous-dependent:**
# ```
# "Can we discuss this?"
# (6 hours later)
# "Never mind, I figured it out"
# ```
#
# **✅ Async-friendly:**
# ```
# "I'm considering two approaches for the data preprocessing:
#
#  Approach A: Pandas with chunked reading
#  - Pros: Familiar to team, easy to debug
#  - Cons: Memory intensive for large files
#
#  Approach B: Dask for out-of-core processing
#  - Pros: Scales to large datasets
#  - Cons: More complex, adds dependency
#
#  I'm leaning toward A for now since our datasets are <1GB.
#  Thoughts? I'll implement A tomorrow unless concerns are raised."
# ```
#
# ### Handling Disagreements Professionally
#
# Disagreements are normal and healthy - if handled well:
#
# **1. Assume good intentions**
# - Everyone wants the project to succeed
# - People have different backgrounds and perspectives
# - Misunderstandings happen in text communication
#
# **2. Focus on technical merits**
# - Discuss trade-offs objectively
# - Use benchmarks and data when possible
# - Separate personal preference from technical requirements
#
# **3. Escalate when needed**
# - If consensus can't be reached, involve team lead
# - Document both perspectives
# - Accept decisions gracefully
#
# **4. Learn from conflict**
# - Update guidelines to prevent future disagreements
# - Clarify decision-making processes
# - Improve documentation

# %% [markdown]
# ## Part 9: Collaboration Beyond Python
#
# ### Language-Specific Collaboration Practices
#
# The principles of collaboration are universal, but tools differ by ecosystem.
#
# ### R Projects
#
# **Version Control:**
# - Git workflow identical to Python
# - Pull requests work the same way
#
# **Code Review Focus:**
# ```r
# # ❌ Hard to review
# res <- dat %>% filter(x > 0) %>% group_by(grp) %>%
#        summarize(m = mean(val)) %>% arrange(desc(m))
#
# # ✅ Easier to review (one operation per line)
# res <- dat %>%
#   filter(x > 0) %>%
#   group_by(grp) %>%
#   summarize(mean_value = mean(val)) %>%
#   arrange(desc(mean_value))
# ```
#
# **R-Specific Tools:**
# - `lintr` for code style checking (like flake8 for Python)
# - `testthat` for testing (like pytest)
# - `devtools::check()` for package validation
# - `pkgdown` for documentation websites
#
# **GitLab CI for R:**
# ```yaml
# test:
#   image: rocker/tidyverse:latest
#   script:
#     - R -e "devtools::install_deps()"
#     - R -e "devtools::test()"
#     - R -e "devtools::check()"
# ```
#
# ### C/C++ Projects
#
# **Build System Considerations:**
# - PRs must include build system updates (CMakeLists.txt, Makefile)
# - Cross-platform builds often differ
# - Review must verify compilation on multiple platforms
#
# **Code Review Focus:**
# ```cpp
# // ❌ Potential issues
# char* buffer = new char[size];  // No delete? Memory leak!
# int* data = (int*)malloc(n * sizeof(int));  // Mixed C/C++?
#
# // ✅ Modern C++ practices
# std::vector<char> buffer(size);  // Automatic memory management
# std::unique_ptr<int[]> data(new int[n]);  // Smart pointer
# ```
#
# **Tools:**
# - `clang-format` for automatic code formatting
# - `clang-tidy` for static analysis
# - `cppcheck` for additional checks
# - `valgrind` for memory leak detection
#
# **GitHub Actions for C++:**
# ```yaml
# name: C++ CI
# on: [push, pull_request]
# jobs:
#   build:
#     strategy:
#       matrix:
#         os: [ubuntu-latest, macos-latest, windows-latest]
#         compiler: [gcc, clang]
#     runs-on: ${{ matrix.os }}
#     steps:
#       - uses: actions/checkout@v4
#       - name: Build
#         run: |
#           cmake -B build
#           cmake --build build
#       - name: Test
#         run: ctest --test-dir build
# ```
#
# ### Julia Projects
#
# **Package System:**
# - Dependencies in `Project.toml` (like requirements.txt)
# - Manifest.toml locks exact versions (like conda locks)
#
# **Code Review:**
# ```julia
# # ❌ Type instability (performance issue)
# function compute(x)
#     if x > 0
#         return x  # Float
#     else
#         return 0  # Int - type instability!
#     end
# end
#
# # ✅ Type stable
# function compute(x::Float64)::Float64
#     if x > 0
#         return x
#     else
#         return 0.0
#     end
# end
# ```
#
# **Tools:**
# - `Pkg.test()` runs package tests
# - `JuliaFormatter.jl` for code formatting
# - `Documenter.jl` for documentation
#
# ### Fortran Projects
#
# **Modern Fortran Best Practices:**
# ```fortran
# ! ❌ Old style (hard to review)
#       SUBROUTINE CALC(X,Y,N,RES)
#       IMPLICIT NONE
#       INTEGER N
#       REAL X(N),Y(N),RES
#
# ! ✅ Modern style (clearer intent)
# subroutine calculate_result(input_x, input_y, result)
#     real, dimension(:), intent(in) :: input_x, input_y
#     real, intent(out) :: result
#
#     ! Clear variable roles with intent
# ```
#
# **Tools:**
# - `fprettify` for code formatting
# - `ford` for documentation generation
# - `fpm` (Fortran Package Manager) for modern project structure
#
# ### MATLAB Projects
#
# **Version Control Challenges:**
# - Binary `.mat` files don't diff well
# - Consider exporting to HDF5 or text for version control
#
# **Code Review:**
# ```matlab
# % ❌ Magic numbers
# y = x * 9.81;
#
# % ✅ Named constants
# GRAVITY_M_PER_S2 = 9.81;
# y = x * GRAVITY_M_PER_S2;
# ```
#
# **Tools:**
# - MATLAB's built-in code analyzer (orange squiggles)
# - `checkcode()` function for programmatic checking
# - MATLAB Unit Test framework

# %% [markdown]
# ## Part 10: Advanced Collaboration Practices
#
# ### Protected Branches
#
# **Configure repository settings to require:**
# - Pull request reviews before merging
# - Passing CI tests
# - Up-to-date branches
# - Signed commits (for security-critical projects)
#
# **GitHub:**
# Settings → Branches → Branch protection rules
#
# **GitLab:**
# Settings → Repository → Protected branches
#
# **Typical rules:**
# - Require 1-2 approving reviews
# - Require status checks to pass
# - Require branches to be up to date before merging
# - No force pushes to main
# - No deletions of main branch
#
# ### Code Owners (CODEOWNERS)
#
# Automatically request reviews from relevant experts:
#
# **`.github/CODEOWNERS` (GitHub) or `.gitlab/CODEOWNERS` (GitLab):**
# ```
# # Climate physics algorithms
# /src/physics/           @climate-team @physics-lead
#
# # Data processing pipeline
# /src/data/              @data-team
#
# # Documentation
# *.md                    @docs-team
# /docs/                  @docs-team
#
# # CI/CD configuration
# /.github/workflows/     @devops-team
# .gitlab-ci.yml          @devops-team
# ```
#
# When someone opens a PR touching these files, the specified teams/users are
# automatically requested as reviewers.
#
# ### Draft Pull Requests
#
# Use draft PRs for early feedback:
#
# **GitHub:**
# - Create PR and select "Create draft pull request"
# - Mark as "Ready for review" when done
#
# **GitLab:**
# - Prefix title with `Draft:` or `WIP:` (Work in Progress)
# - Remove prefix when ready
#
# **Use cases:**
# - Get early feedback on approach
# - Show progress on complex features
# - Trigger CI without requesting formal review
# - Collaborate on design before implementation complete
#
# ### Pair Programming for Complex Changes
#
# Some changes benefit from real-time collaboration:
#
# **Tools:**
# - **VS Code Live Share**: Real-time collaborative editing
# - **Tuple/Pop**: Pair programming with high-quality screen sharing
# - **Zoom/Google Meet**: Screen sharing for simpler collaboration
#
# **When to pair program:**
# - Onboarding new team members
# - Debugging complex issues
# - Designing critical algorithms
# - Learning new technologies
# - Resolving difficult merge conflicts
#
# **Protocol:**
# - One person "drives" (types)
# - Other person "navigates" (thinks strategically)
# - Switch roles every 20-30 minutes
# - Both stay engaged

# %% [markdown]
# ## Part 11: Real-World Example - Collaborative Bug Fix
#
# Let's walk through a complete example of collaborative development.
#
# ### Scenario: Bug in Climate Model
#
# **Issue #127**: "Temperature model produces NaN for coastal regions"
#
# **Step 1: Lisa reproduces the bug**
# ```python
# # Create test file: tests/test_coastal_temperature.py
# import pytest
# import numpy as np
# from climate_model import calculate_temperature
#
# def test_coastal_temperature_should_not_be_nan():
#     """Coastal regions should produce valid temperature values."""
#     # Coordinates for coastal grid cell
#     lat = 37.8
#     lon = -122.4  # San Francisco Bay
#     land_fraction = 0.5  # 50% land, 50% water
#
#     temp = calculate_temperature(lat, lon, land_fraction)
#
#     assert not np.isnan(temp), "Temperature should not be NaN for coastal cells"
#     assert -50 < temp < 50, "Temperature should be physically reasonable"
# ```
#
# **Step 2: Lisa creates a feature branch**
# ```bash
# git checkout main
# git pull origin main
# git checkout -b fix/coastal-nan-temperature
# ```
#
# **Step 3: Lisa commits the failing test**
# ```bash
# git add tests/test_coastal_temperature.py
# git commit -m "Add test for coastal temperature NaN bug (currently fails)
#
# Documents the bug with a reproducible test case.
# Test will pass once bug is fixed.
#
# Relates to #127"
# git push origin fix/coastal-nan-temperature
# ```
#
# **Step 4: Lisa opens a draft PR**
# ```
# Title: [WIP] Fix coastal temperature NaN bug
#
# ## Problem
# Temperature calculation produces NaN for coastal grid cells where
# land_fraction is between 0 and 1.
#
# ## Current Progress
# - [x] Reproduced bug with test case
# - [ ] Identified root cause
# - [ ] Implemented fix
# - [ ] All tests passing
#
# Relates to #127
# ```
#
# **Step 5: Lisa investigates and finds the bug**
# ```python
# # In src/temperature.py - BEFORE fix
# def calculate_temperature(lat, lon, land_fraction):
#     land_temp = calculate_land_temperature(lat, lon)
#     ocean_temp = calculate_ocean_temperature(lat, lon)
#
#     # BUG: Division by zero when land_fraction is exactly 0.5!
#     weight = (land_fraction - 0.5) / (land_fraction - 0.5)  # Always 1 or NaN!
#
#     return land_temp * weight + ocean_temp * (1 - weight)
# ```
#
# **Step 6: Lisa fixes the bug**
# ```python
# # In src/temperature.py - AFTER fix
# def calculate_temperature(lat, lon, land_fraction):
#     """Calculate temperature for a grid cell.
#
#     For coastal cells (0 < land_fraction < 1), interpolates between
#     land and ocean temperatures based on land fraction.
#
#     Parameters
#     ----------
#     lat : float
#         Latitude in degrees
#     lon : float
#         Longitude in degrees
#     land_fraction : float
#         Fraction of grid cell that is land (0 = all ocean, 1 = all land)
#
#     Returns
#     -------
#     float
#         Temperature in Celsius
#     """
#     land_temp = calculate_land_temperature(lat, lon)
#     ocean_temp = calculate_ocean_temperature(lat, lon)
#
#     # Linear interpolation between land and ocean temperatures
#     return land_temp * land_fraction + ocean_temp * (1 - land_fraction)
# ```
#
# **Step 7: Lisa verifies the fix**
# ```bash
# pytest tests/test_coastal_temperature.py  # Passes!
# pytest tests/  # All tests pass
# ```
#
# **Step 8: Lisa updates the PR**
# ```bash
# git add src/temperature.py
# git commit -m "Fix coastal temperature NaN bug
#
# Root cause: Incorrect interpolation formula was dividing by zero
# for land_fraction = 0.5.
#
# Solution: Use simple linear interpolation between land and ocean
# temperatures based on land_fraction.
#
# The new formula is:
# - temp = land_temp * land_fraction + ocean_temp * (1 - land_fraction)
#
# This correctly handles all values of land_fraction from 0 to 1.
#
# Fixes #127"
# git push origin fix/coastal-nan-temperature
# ```
#
# **Step 9: Lisa marks PR as ready and requests review**
# - Remove [WIP] from title
# - Request review from @james (climate physics expert)
# - Request review from @maya (code quality expert)
#
# **Step 10: James reviews (domain expert)**
# ```
# Comment on the interpolation line:
# "Great fix! The linear interpolation is physically reasonable for
#  coastal cells. One suggestion: for very small land fractions (<0.01),
#  we might want to just use ocean temperature to avoid numerical issues.
#  But that can be a follow-up optimization - this fix is solid."
#
# ✅ Approved
# ```
#
# **Step 11: Maya reviews (code quality expert)**
# ```
# Comment on docstring:
# "Excellent documentation! The formula is now clear.
#
#  Minor suggestion: Could you add a test for the edge cases
#  (land_fraction = 0 and land_fraction = 1) to ensure we didn't
#  break the all-land and all-ocean cases?"
#
# 🔄 Request changes
# ```
#
# **Step 12: Lisa addresses feedback**
# ```python
# # Add to tests/test_coastal_temperature.py
# def test_temperature_all_land():
#     """All-land cells should use only land temperature."""
#     temp_land_only = calculate_temperature(lat=40.0, lon=-100.0,
#                                            land_fraction=1.0)
#     expected = calculate_land_temperature(40.0, -100.0)
#     assert temp_land_only == expected
#
# def test_temperature_all_ocean():
#     """All-ocean cells should use only ocean temperature."""
#     temp_ocean_only = calculate_temperature(lat=30.0, lon=-60.0,
#                                             land_fraction=0.0)
#     expected = calculate_ocean_temperature(30.0, -60.0)
#     assert temp_ocean_only == expected
# ```
#
# ```bash
# git add tests/test_coastal_temperature.py
# git commit -m "Add edge case tests for all-land and all-ocean cells
#
# Address review feedback from @maya"
# git push origin fix/coastal-nan-temperature
# ```
#
# **Step 13: Maya re-reviews**
# ```
# "Perfect! The edge case tests are valuable.
#  ✅ Approved"
# ```
#
# **Step 14: Merge!**
# - Both reviewers approved ✅
# - All CI tests pass ✅
# - Branch is up-to-date ✅
# - Click "Squash and merge"
# - Delete branch `fix/coastal-nan-temperature`
#
# **Step 15: Close the issue**
# GitHub automatically closes #127 because commit message said "Fixes #127"
#
# ### Lessons from This Example
#
# - ✅ Test first documented the bug
# - ✅ Draft PR enabled early feedback
# - ✅ Clear commit messages explained reasoning
# - ✅ Documentation improved code clarity
# - ✅ Reviews caught missing edge cases
# - ✅ Constructive feedback improved quality
# - ✅ Everyone's expertise contributed
# - ✅ Final code better than any one person would have written alone

# %% [markdown]
# ## Part 12: Summary - Building Collaborative Research Software
#
# ### Key Takeaways
#
# **1. Collaboration requires process**
# - Git alone isn't enough
# - Pull requests provide structure
# - Code review catches bugs and shares knowledge
# - Clear guidelines prevent conflicts
#
# **2. Communication matters**
# - Write clear PR descriptions
# - Give constructive feedback
# - Assume good intentions
# - Document decisions
#
# **3. Make contributing easy**
# - Write CONTRIBUTING.md
# - Label "good first issues"
# - Provide PR templates
# - Welcome new contributors warmly
#
# **4. Tools support people**
# - Protected branches enforce process
# - CODEOWNERS route reviews
# - CI automates quality checks
# - But people make collaboration work
#
# **5. Adapt to your team**
# - Different projects need different workflows
# - Start simple, add process as needed
# - Document your decisions
# - Review and improve regularly
#
# ### The Collaboration Maturity Model
#
# **Level 1: Solo developer**
# - Direct commits to main
# - No reviews
# - Works until team grows
#
# **Level 2: Basic collaboration**
# - Feature branches
# - Pull requests
# - Informal reviews
# - Good for small teams (2-3 people)
#
# **Level 3: Structured process**
# - Required reviews
# - CI/CD integration
# - Contribution guidelines
# - Good for growing teams (4-10 people)
#
# **Level 4: Scaled collaboration**
# - CODEOWNERS
# - Multiple approval rules
# - Automated quality checks
# - Release management process
# - Necessary for large teams (10+ people)
#
# **Start where you are, grow as needed.**
#
# ### Final Thoughts
#
# Good collaboration is about:
# - **Respect** for collaborators' time and expertise
# - **Clarity** in communication and expectations
# - **Quality** in code and reviews
# - **Growth** of both code and people
#
# Research software is better when developed collaboratively. The code becomes
# more robust, the science more reproducible, and the research community stronger.
#
# Your future self - and your future collaborators - will thank you for building
# good collaboration practices from the start.

# %% [markdown]
# ### What's Next?
#
# In **Lecture 11**, we'll shift focus to managing research data effectively. You'll learn:
# - FAIR principles for research data (Findable, Accessible, Interoperable, Reusable)
# - Choosing appropriate file formats for different types of scientific data
# - Working with specialized formats like HDF5 and NetCDF
# - Using databases for structured research data
# - Ensuring data integrity and validation
#
# Good collaboration practices you've learned here will help you work with shared datasets
# and maintain data quality across your team.
#
# **Ready to continue? Move on to Lecture 11: Working with Research Data!**

# %% [markdown]
# ## References and Further Reading
#
# ### Collaboration and Code Review
#
# - **The Turing Way - Guide to Collaboration**
#   <https://the-turing-way.netlify.app/collaboration/collaboration.html>
#   Comprehensive handbook on collaborative research practices.
#
# - **Best Practices for Code Review**
#   <https://google.github.io/eng-practices/review/>
#   Google's engineering practices for code review.
#
# - **Thoughtbot Code Review Guide**
#   <https://github.com/thoughtbot/guides/tree/main/code-review>
#   Practical guide to giving and receiving code review feedback.
#
# ### Version Control Workflows
#
# - **GitHub Flow**
#   <https://docs.github.com/en/get-started/quickstart/github-flow>
#   Simple workflow for teams using GitHub.
#
# - **GitLab Flow**
#   <https://docs.gitlab.com/ee/topics/gitlab_flow.html>
#   GitLab's recommended workflow combining feature branches and environments.
#
# - **Atlassian Git Workflows**
#   <https://www.atlassian.com/git/tutorials/comparing-workflows>
#   Comparison of different Git workflow strategies.
#
# ### Pull Request Best Practices
#
# - **GitHub Pull Request Documentation**
#   <https://docs.github.com/en/pull-requests>
#   Official GitHub documentation for pull requests.
#
# - **GitLab Merge Request Documentation**
#   <https://docs.gitlab.com/ee/user/project/merge_requests/>
#   Official GitLab documentation for merge requests.
#
# ### Onboarding and Contribution
#
# - **Open Source Guides - How to Contribute**
#   <https://opensource.guide/how-to-contribute/>
#   GitHub's guide to contributing to open source projects.
#
# - **Contributing.md Template**
#   <https://github.com/nayafia/contributing-template>
#   Template for creating contribution guidelines.
#
# ### Communication and Team Dynamics
#
# - **The Art of Giving and Receiving Code Reviews Gracefully**
#   <https://www.alexandra-hill.com/2018/06/25/the-art-of-giving-and-receiving-code-reviews/>
#   Blog post on constructive code review practices.
#
# - **How to Make Your Code Reviewer Fall in Love with You**
#   <https://mtlynch.io/code-review-love/>
#   Practical tips for submitting reviewable pull requests.
#
# ### Language-Specific Resources
#
# **R:**
# - **R Packages Book - Git and GitHub**
#   <https://r-pkgs.org/software-development-practices.html>
#   Hadley Wickham's guide to collaboration in R packages.
#
# **C/C++:**
# - **clang-format**
#   <https://clang.llvm.org/docs/ClangFormat.html>
#   Automatic code formatting for C/C++.
#
# - **Modern CMake for Modular Design**
#   <https://cliutils.gitlab.io/modern-cmake/>
#   Best practices for C++ project structure and collaboration.
#
# **Julia:**
# - **Julia Community Standards**
#   <https://julialang.org/community/standards/>
#   Code of conduct and collaboration guidelines for Julia community.
#
# **Fortran:**
# - **Fortran Package Manager (fpm)**
#   <https://fpm.fortran-lang.org/>
#   Modern package manager improving Fortran collaboration.
#
# ### Protected Branches and Repository Settings
#
# - **GitHub Branch Protection Rules**
#   <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches>
#   Documentation on configuring branch protection.
#
# - **GitLab Protected Branches**
#   <https://docs.gitlab.com/ee/user/project/protected_branches.html>
#   GitLab's branch protection features.
#
# - **CODEOWNERS**
#   <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners>
#   Automatic review requests based on file ownership.
#
# ### Research Software Collaboration
#
# - **The Turing Way**
#   <https://the-turing-way.netlify.app/>
#   Handbook for reproducible research, including collaboration practices.
#
# - **Software Carpentry - Git for Teams**
#   <https://swcarpentry.github.io/git-novice/>
#   Introductory material on version control for collaborative research.
#
# - **FAIR Principles for Research Software**
#   <https://doi.org/10.15497/RDA00068>
#   Findable, Accessible, Interoperable, and Reusable research software.
#
# ### Notes
#
# The example of "Dr. James Park" and his climate simulation team is a fictional
# composite created for pedagogical purposes. The scenario illustrates common
# patterns in research software development but does not represent any specific
# individuals or projects.
