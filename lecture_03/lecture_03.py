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
# # Lecture 3: AI-Assisted Coding Foundations
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
# This lecture is a foundations-only introduction to AI-assisted coding: what these tools
# actually do, what they're genuinely good at, how to prompt them effectively, the one habit
# that keeps you safe while using them, and the most common ways they go wrong. It won't make
# you an expert, and that's on purpose—later lectures pick this
# back up in context, once you have more RSE fundamentals to apply. Lecture 5 asks whether AI
# can write your tests for you, Lecture 7 uses AI to help track down a bug, Lecture 10 covers
# reviewing AI-assisted pull requests, and Lecture 14 covers the legal, ethical, and
# data-protection questions properly. Think of this lecture as establishing shared vocabulary
# and one non-negotiable habit before we put it into practice for the rest of the course.
#
# **Duration**: ~90 minutes
#
# ## Prerequisites
#
# Before starting this lecture, you should be familiar with:
# - Git fundamentals, including reading a diff (Lectures 1-2)
# - The Python concepts covered in Lecture 2—you'll mostly be *reading* code in this lecture,
#   not writing it from scratch
#
# No prior experience with any specific AI coding tool is assumed or required.
#
# ## Learning Objectives
# - Distinguish autocomplete-style, chat-style, and agentic AI coding tools by what they do to
#   your review burden, not by brand name
# - Identify the kinds of RSE tasks where AI assistants genuinely save time
# - Write specific, well-scoped prompts that make an AI assistant's assumptions visible
#   instead of silent
# - Apply the core habit: treat every AI suggestion as a diff you must review before committing
# - Recognize the most common ways AI-generated code goes wrong
# - Know where the deeper AI topics (testing, debugging, review, legal/ethics) come up later in
#   the course, so you know what to expect and what's still to come

# %% [markdown]
# ## Part 1: The Copy-Paste Catastrophe - A Cautionary Tale
#
# ### The Story
#
# Dr. Sarah Chen was under pressure to analyze genomic data for an upcoming paper deadline
# when a new AI coding assistant promised to "write code from comments." She described what
# she needed, and it generated a complete function in seconds—professional-looking, with
# docstrings and error handling. It ran without errors and produced reasonable-looking
# results, so she copied it into her analysis pipeline without fully understanding the
# normalization algorithm it used.
#
# **Three weeks later**, during peer review, a reviewer asked why she'd used quantile
# normalization instead of the standard method for her data type. Sarah froze—she didn't
# know what the AI had actually generated. Looking back at the code, the normalization method
# was inappropriate for her data, the algorithm had a subtle bug that only appeared with
# certain data distributions, and the results were scientifically incorrect.
#
# **The paper was rejected**, and Sarah had to retract a conference presentation built on the
# flawed analysis. The AI had been fast, but she hadn't understood what it generated or
# verified it was correct.
#
# ### The Lessons
#
# - **AI generates plausible code, not necessarily correct code**
# - **Understanding your code is non-negotiable in research**—"it ran without errors" is not
#   the same as "it's right"
# - **AI suggestions can have hidden bugs or use inappropriate algorithms** for your specific
#   data or question
# - **Speed without comprehension is dangerous in science**
#
# With these lessons in mind, let's build a foundation for using AI assistants effectively and
# safely.

# %% [markdown]
# ## Part 2: What AI Coding Tools Actually Do
#
# ### Three Categories, Not Brands
#
# It's tempting to learn AI-assisted coding as "how to use tool X." Don't—specific products
# rise and fall constantly, but the way they change your workflow falls into three durable
# categories, based on how much you see before you commit to it:
#
# - **Autocomplete-style**: suggests code as you type, usually a line or a few lines at a
#   time. You review each suggestion almost as closely as you'd review your own typing.
# - **Chat-style**: you ask a question or describe a task, and it drafts a snippet or an
#   explanation in a conversation. You review a self-contained block before using it.
# - **Agentic**: you describe a goal, and it plans and carries out multiple steps on its
#   own—editing several files, running commands, sometimes opening a pull request. You review
#   a diff you didn't watch get written, possibly touching code you haven't looked at yet.
#
# Notice the pattern: as tools move from autocomplete toward agentic, you see less of the
# process and more of the result. Your review habits need to adjust accordingly—which is
# exactly what Part 5 is about.
#
# <img src="figures/ai_tool_spectrum.svg" alt="Spectrum of AI coding tools from autocomplete-style through chat-style to agentic, with review effort increasing as autonomy increases" width="700"/>
#
# *The three categories sit on a spectrum, not in separate boxes: as tools move from
# autocomplete toward agentic, you see less of the process and the review effort you owe
# on the result goes up accordingly.*
#
# ### How These Tools Actually Work
#
# AI coding assistants are built on **Large Language Models (LLMs)** trained on huge amounts
# of code and text. A few properties matter for how you use them:
#
# - **Pattern-based**: they recognize and reproduce common coding patterns, not the logic
#   behind them
# - **Statistical**: they predict a plausible continuation, not a verified-correct one
# - **Context-aware**: they use the code and conversation you've provided as context
# - **Non-deterministic**: the same prompt can produce different output on different runs
#
# **The key implication**: these tools don't "understand" your code the way you do. They're
# very good at producing something that *looks* like a correct answer to your question—which
# is exactly what made Sarah's bug so easy to miss.
#
# **A practical consequence of "context-aware"**: an assistant only "sees" what's in its
# context window—your open files, the recent conversation, sometimes a repo index. It doesn't
# automatically know your project's conventions, your team's error-handling style, or a
# decision made in a meeting last week. An assistant that hasn't seen those things will
# confidently generate code that ignores them—not because it's malfunctioning, but because it
# was never given the context to do otherwise. Giving relevant context (open the right files,
# state the convention explicitly) is one of the most effective ways to improve suggestions.

# %% [markdown]
# <div style="background-color: #e3f2fd; border-left: 5px solid #1976d2; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #0d47a1; margin-top: 0;">🔧 Tools Landscape (snapshot, not an endorsement)</h4>
#     <p>Examples only—this list moves fast, and the categories above are what actually matters.
#     Check what's current before class.</p>
#     <ul>
#         <li><strong>Autocomplete-style</strong>: e.g. GitHub Copilot, Amazon Q Developer, Tabnine</li>
#         <li><strong>Chat-style</strong>: e.g. ChatGPT, Claude, Gemini</li>
#         <li><strong>Agentic</strong>: e.g. Claude Code, Cursor's agent mode, GitHub Copilot's
#         agent/coding-agent mode</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 3: What AI Is Actually Good At
#
# It would be easy for a lecture like this to turn into a parade of cautionary tales—we've
# already had one, and there are more ahead. Before that happens, it's worth being direct
# about the other half of the picture: used well, these tools genuinely save real time on
# real tasks. That's not a caveat before a warning—it's true on its own terms.
#
# **Accelerating boilerplate and repetitive code**: turning a handful of known values into
# test cases, generating a standard class scaffold, writing the docstring for the tenth
# similar function today—AI is very good at mechanical pattern completion. This is exactly
# the kind of task where typing it out by hand adds no value.


# %%
def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32


# Give an AI assistant five known conversions and ask for test cases—turning a short list
# of known values into code like this is exactly the kind of repetitive pattern completion
# these tools handle well:
known_conversions = [
    (0, 32),
    (100, 212),
    (-40, -40),
    (37, 98.6),
    (20, 68),
]

for celsius, expected in known_conversions:
    actual = celsius_to_fahrenheit(celsius)
    status = "PASS" if abs(actual - expected) < 0.1 else "FAIL"
    print(f"{status}: celsius_to_fahrenheit({celsius}) = {actual} (expected {expected})")

# %% [markdown]
# **Getting oriented fast**: pointed at an unfamiliar library, an unfamiliar error message, or
# a codebase you didn't write, an AI assistant is often faster than a documentation search for
# a first orientation—"what does this function do," "why am I getting this error," "what's the
# idiomatic way to do this in this library." You'll still confirm what comes back, but as a
# starting point for exploration, it's hard to beat.
#
# **Drafting a first pass**: a rough first version of a test suite, a README section, an
# explanation of what a piece of code does—having something concrete to react to and edit is
# often faster than starting from a blank page, even when you end up changing most of it.
#
# **Exploring alternatives**: "what's another way to do this," "is there a simpler
# approach"—AI is a reasonable brainstorming partner for surfacing options you might not have
# considered, precisely because it's drawing on a huge range of code it's seen before.
#
# None of this requires blind trust in the output. It just means the honest starting point
# for this course isn't "AI is dangerous, be careful." It's "AI is a genuinely useful tool for
# a specific set of tasks—here's how to get the most out of it, and here's what to watch for
# along the way."

# %% [markdown]
# ## Part 4: Getting Good Results - Effective Prompting
#
# Before we get to reviewing what comes out of an AI assistant, it's worth spending a moment
# on what goes in. A vague request forces the model to guess at the details you didn't
# specify—and it will guess, confidently, without telling you it did. This is exactly what
# happened to Sarah in Part 1: her prompt, "Function to normalize gene expression data,"
# never named a normalization method, so the AI picked one silently. A more specific prompt
# wouldn't have guaranteed success, but it would have forced that choice into the open where
# she could catch it.
#
# ### What Makes a Prompt Well-Specified
#
# - **State the task precisely**: not just what the function does, but what its inputs,
#   outputs, and edge cases should be
# - **Name the edge cases you care about**: empty input, too little data, unusual or invalid
#   values—if you don't mention them, don't expect the result to handle them
# - **Provide context**: point to relevant existing code, conventions, or constraints ("match
#   the docstring style used elsewhere in this file")
# - **Iterate rather than restart**: if the first response misses something, say specifically
#   what's wrong and ask again—that's usually faster than starting over
#
# Let's see the difference a specific prompt makes, using the outlier-filtering idea from
# Lecture 2 as an example.

# %%
# A vague prompt: "Write a function to remove outliers from temperature readings"
# This is a plausible response—reasonable, but silent about a decision the AI had
# to make on your behalf: what happens when there isn't enough data to say
# anything statistical?


def remove_outliers_vague(readings):
    """Remove outliers from temperature readings."""
    mean = sum(readings) / len(readings)
    std = (sum((x - mean) ** 2 for x in readings) / len(readings)) ** 0.5
    return [x for x in readings if abs(x - mean) <= 2 * std]


# Looks fine on a normal sample...
print(remove_outliers_vague([21.0, 22.5, 21.8, 22.3, 21.6, 45.0, 22.1]))

# %% [markdown]
# That works. But the prompt never said what should happen with very little data—so neither
# did the AI. Let's check:

# %%
too_few_readings = []
try:
    print(remove_outliers_vague(too_few_readings))
except ZeroDivisionError as e:
    print(f"Crashed: {e}")

# %% [markdown]
# A crash: `ZeroDivisionError`, because `mean` divides by `len(readings)`, which is zero.
# Nothing about the vague prompt asked for this case to be handled, so it wasn't. Now compare
# a prompt that names the edge case explicitly:
#
# *"Write a function that removes temperature readings more than 2 standard deviations from
# the mean. If there are fewer than 3 readings, there isn't enough data to compute a
# meaningful standard deviation—return the readings unchanged instead."*


# %%
def remove_outliers_specified(readings):
    """
    Remove readings more than 2 standard deviations from the mean.

    With fewer than 3 readings, standard deviation isn't meaningful, so the
    readings are returned unchanged.
    """
    if len(readings) < 3:
        return readings
    mean = sum(readings) / len(readings)
    std = (sum((x - mean) ** 2 for x in readings) / len(readings)) ** 0.5
    return [x for x in readings if abs(x - mean) <= 2 * std]


print(f"Empty input: {remove_outliers_specified(too_few_readings)}")
print(f"Two readings: {remove_outliers_specified([21.0, 35.0])}")
print(f"Normal sample: {remove_outliers_specified([21.0, 22.5, 21.8, 22.3, 21.6, 45.0, 22.1])}")

# %% [markdown]
# No crash, and the edge case is handled the way we actually decided it should be—because we
# decided it, in the prompt, instead of leaving it to chance. Specificity doesn't guarantee a
# correct result (you still need to review it, per Part 5), but it turns silent guesses into
# visible decisions you can check.

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Practice turning vague requests into specific ones:</p>
#     <ul>
#         <li><strong>Rewrite Sarah's prompt:</strong> Go back to Part 1. Rewrite "Function to
#         normalize gene expression data" as a well-specified prompt that names a normalization
#         method and states why—would a more specific prompt have caught the problem before it
#         reached her pipeline?</li>
#         <li><strong>Find one more edge case:</strong> <code>remove_outliers_specified</code>
#         still doesn't say what should happen if every reading is identical (standard deviation
#         of zero). Decide what the "right" behavior is, then write the prompt that would
#         specify it.</li>
#         <li><strong>Audit your own prompts:</strong> Next time you ask an AI assistant for
#         code, write the prompt, then list every decision it will have to make that you didn't
#         specify. Which of those decisions actually mattered?</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 5: The Core Habit - Review Every Suggestion Like a Diff
#
# You already know how to review a diff—Lecture 2 covered reading `git diff` output and
# reviewing pull requests. Apply exactly that skill here: **an AI suggestion is a diff someone
# else wrote, and you are the reviewer, whether or not you asked to be.** Before it becomes
# your code, it needs the same scrutiny you'd give a teammate's PR.
#
# The single most useful technique is simple: **verify the suggestion against a case you can
# check by hand.** Let's see why that matters with a concrete example.

# %%
# Suppose you asked an AI assistant: "write a function that averages a list of numbers,
# ignoring any missing values represented as None"


def average_ignoring_missing(values):
    """Calculate the average of a list, ignoring missing values (None)."""
    total = sum(v for v in values if v is not None)
    return total / len(values)


# It runs without error and returns a plausible-looking number...
sample = [10, 20, None, 40]
print(f"Average: {average_ignoring_missing(sample)}")

# %% [markdown]
# That ran without crashing and printed a normal-looking number—easy to accept at a glance.
# Now let's review it the way we'd review a diff: check it against a case we can compute by
# hand.

# %%
# Reviewing like a diff: verify against a case you can check by hand.
# Only three values are present (10, 20, 40), so the average should be their mean.
expected = (10 + 20 + 40) / 3
actual = average_ignoring_missing(sample)

print(f"Expected (by hand): {expected:.2f}")
print(f"Function returned:  {actual:.2f}")
print(f"Match: {abs(expected - actual) < 0.01}")

# %% [markdown]
# They don't match. The docstring says "ignoring missing values," but the divisor
# (`len(values)`) still counts the `None` entries—only the numerator excludes them. The AI
# produced code that *looks like* a typical averaging function, not code that correctly
# implements *this specific request*. That's the pattern-matching-not-understanding property
# from Part 2, showing up as a bug you'd only catch by checking the arithmetic yourself.
#
# The fix is a one-line change once you've spotted the problem:


# %%
def average_ignoring_missing_fixed(values):
    """Calculate the average of a list, ignoring missing values (None)."""
    present = [v for v in values if v is not None]
    if not present:
        return None
    return sum(present) / len(present)


fixed_result = average_ignoring_missing_fixed(sample)
print(f"Fixed average: {fixed_result:.2f}")
print(f"Matches hand calculation: {abs(fixed_result - expected) < 0.01}")

# %% [markdown]
# Notice the fixed version also handles a case the original silently didn't: a list that's
# entirely `None`. The original would raise a `ZeroDivisionError`; this one returns `None`
# instead—the kind of edge case a careful review catches, exactly like the error-handling
# habits from Lecture 2.
#
# ### Review Scales With What You Can't See
#
# The example above was a single function—easy to check by hand in a minute. Now imagine an
# agentic tool made a similar change across five files: renamed a parameter, updated three
# call sites, and adjusted a test to match. The same kind of bug (silently counting the wrong
# things) could hide in any one of those files, and checking all of them by hand takes real
# time.
#
# This is exactly why the three categories from Part 2 matter in practice, not just in theory:
# the more a tool does in one step, the more deliberately you need to budget review time for
# it. A one-line autocomplete suggestion might get a five-second glance; a multi-file agentic
# change deserves the same scrutiny you'd give a colleague's pull request—because that's
# exactly what it is.

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Practice reviewing AI suggestions like diffs:</p>
#     <ul>
#         <li><strong>Find another edge case:</strong> Does <code>average_ignoring_missing_fixed</code>
#         handle a list with no arguments, or a list of all <code>None</code>s, sensibly? Try it and
#         decide whether returning <code>None</code> is really the right behavior for your use case.</li>
#         <li><strong>Verify a real suggestion:</strong> Ask an AI assistant (or find AI-generated
#         code online) for a function that solves a problem you already understand well. Before
#         trusting it, check its output against a case you can compute by hand—the same technique
#         used above.</li>
#         <li><strong>Practice on your own recent work:</strong> Pick a diff from your own project
#         (AI-assisted or not) and apply the same "verify against a known case" habit to it.</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 6: Common Pitfalls
#
# ### Hallucinated APIs and Plausible-Looking Bugs
#
# AI assistants sometimes invent functions, parameters, or methods that don't actually
# exist—confidently, with no indication of uncertainty. For example, asked for "the pandas
# function that removes duplicate rows, keeping the row with the highest value in a column,"
# an assistant might produce:
#
# ```python
# # Looks plausible, but pandas' `keep` parameter only accepts
# # "first", "last", or False—there is no "max" option:
# df.drop_duplicates(subset="id", keep="max")
# ```
#
# This fails immediately with an error, which is actually the easy case—you notice right
# away. The harder case is code that runs and produces a *wrong but plausible* answer, the
# way `average_ignoring_missing` did above. Both failure modes come from the same root cause:
# the model is generating something that *resembles* a correct answer, not verifying that it
# *is* one.
#
# ### Outdated or Insecure Patterns
#
# AI assistants are trained on a snapshot of public code, which includes plenty of code that
# was never a good idea and code that's since been deprecated. Two patterns worth watching
# for:
#
# - **Deprecated APIs**: a suggestion might use a function signature or library version that's
#   since changed—it may already emit a warning, or silently behave differently, on the
#   version you actually have installed
# - **Insecure patterns**: string-concatenated database queries, hardcoded credentials in
#   example code, or overly permissive file permissions can appear in suggestions simply
#   because they appeared often enough in training data, not because they're recommended
#   practice
#
# Neither of these is exotic—they're exactly the kind of thing a normal code review catches,
# which is precisely why the diff-review habit from Part 5 covers them too. AI-generated code
# doesn't get a pass on scrutiny just because a human didn't type it.
#
# ### Automation Bias: The Cognitive Risk
#
# The technical pitfalls above are only half the problem—the other half is human. The more
# fluent and confident AI output looks, the easier it is to under-review it. This is called
# **automation bias**: trusting a system's output more than the evidence warrants, simply
# because it came from the system.
#
# **Why it's a particular risk for research software**:
# - Confident-looking code with docstrings and error handling *reads* as trustworthy, whether
#   or not it is
# - Under deadline pressure (like Sarah in Part 1), the temptation to skip verification grows
# - The more code an agentic tool writes at once, the more there is to under-review in one
#   pass
#
# **The mitigation is the same habit from Part 5**: verify against a case you can check by
# hand, every time, regardless of how confident the output looks. Confidence in the output is
# not evidence of correctness.

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Spot the pitfalls before they cost you:</p>
#     <ul>
#         <li><strong>Hunt for a hallucination:</strong> Ask an AI assistant a question about a
#         library function you already know well, and see whether it invents a parameter or
#         method that doesn't exist. Check the real documentation to confirm.</li>
#         <li><strong>Design a review checklist:</strong> Write three questions you'll ask yourself
#         before accepting any AI-generated function into your own code (e.g., "what case can I
#         verify by hand?", "what happens on empty input?").</li>
#         <li><strong>Reflect on the three categories:</strong> Of autocomplete-style, chat-style,
#         and agentic tools from Part 2, which would you trust least without careful review, and
#         why? What would change your answer?</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 7: Where AI Shows Up for the Rest of This Course
#
# This lecture deliberately stayed narrow: a shared vocabulary and one habit, not a complete
# guide. The rest of the course picks this back up once you have more to apply it with:
#
# - **Lecture 5 (Testing)**: can AI write your tests for you? What changes, and what doesn't.
# - **Lecture 7 (Debugging)**: using AI to help explain a traceback or suggest a fix—and how
#   your debugging skill tells you whether it actually found the cause.
# - **Lecture 10 (Code Review)**: reviewing AI-assisted and agent-authored pull requests, where
#   the diff-review habit from this lecture gets applied at full scale.
# - **Lecture 14 (RSE Community)**: the legal, ethical, and data-protection questions—licensing,
#   privacy, and when self-hosted tools matter for sensitive research data—get the dedicated
#   treatment they deserve, once you've seen how these tools behave in practice.
#
# You don't need to memorize all of this now. Just remember the core habit from Part 5: treat
# every AI suggestion as a diff you must review before committing.

# %% [markdown]
# ## Summary
#
# In this lecture, we covered:
#
# - **A cautionary tale**: AI generates plausible code, not necessarily correct code—and "it
#   ran without errors" is not the same as "it's right"
# - **Three categories, not brands**: autocomplete-style, chat-style, and agentic tools differ
#   in how much of the process you see before you review the result
# - **What AI is good at**: accelerating boilerplate, getting oriented fast, drafting a first
#   pass, exploring alternatives—genuine time savings on real tasks, not just a lead-in to a
#   warning
# - **Effective prompting**: specific prompts that name edge cases and constraints turn silent
#   assumptions into visible decisions you can check
# - **The core habit**: treat every AI suggestion as a diff you must review before
#   committing—and verify it against a case you can check by hand
# - **Common pitfalls**: hallucinated APIs, plausible-but-wrong logic, and automation bias
# - **What's next**: AI-assisted workflows return in context throughout the rest of the
#   course—testing, debugging, review, and the legal/ethical questions each get their own
#   dedicated treatment later

# %% [markdown]
# ## Acknowledgements and References
#
# This lecture builds upon concepts from multiple sources:
#
# ### Primary Sources
#
# - **Research Software Engineering with Python** by The Alan Turing Institute
#   <https://alan-turing-institute.github.io/rse-course/html/>
#   General framing on critically evaluating tools in a research software context, adapted for
#   AI-assisted coding.
#
# ### Tool and Technology References
#
# - **GitHub Copilot Documentation** <https://docs.github.com/en/copilot>
#   Referenced as an example of an autocomplete-style and agentic assistant.
#
# - **ChatGPT** by OpenAI <https://chat.openai.com>
#   Referenced as an example of a chat-style assistant.
#
# - Rozière, B. et al. (2023). *Code Llama: Open Foundation Models for Code*. arXiv:2308.12950
#   <https://arxiv.org/abs/2308.12950>
#   Background on how code-focused large language models are trained, informing the
#   "How These Tools Actually Work" section.
#
# ### Notes
#
# The lecture structure, cautionary tale, and exercises have been developed specifically for
# this course. Tool examples are illustrative and deliberately kept out of the main narrative,
# since this landscape changes faster than any other topic in the course—see the "Tools
# Landscape" box in Part 2 for current examples, and expect to check for newer options before
# each time this lecture is taught.

# %% [markdown]
# ### Next Steps
#
# Bringing it together: these tools can genuinely speed up real work—boilerplate, orientation,
# first drafts, exploring alternatives. What deserves your attention is the specific ways they
# go wrong: confident-looking mistakes, hallucinated APIs, edge cases silently skipped. And the
# way to use them responsibly is the habit this lecture keeps returning to: review every
# suggestion like a diff, checked against a case you can verify by hand. Within that, there's
# real room to enjoy the speed—go have fun with these tools, and stay safe while you do.
#
# Lecture 4 puts that discipline to work on something concrete—organizing research code into
# professional Python projects and working with NumPy and Matplotlib—the kind of code you'll be
# writing, reviewing, and sometimes AI-assisting, from here on.
#
# **Ready to continue? Move on to Lecture 4: Python Project Structure and Scientific
# Libraries!**
