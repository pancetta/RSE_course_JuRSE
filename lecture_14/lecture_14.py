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
# # Lecture 14: Course Summary and the RSE Community
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
#     <img src="lecture_14_qr_code.png" alt="This Lecture QR Code" width="150"/>
#     <p><strong>This Lecture</strong></p>
#   </div>
# </div>
#
# ## Overview
# This final half-lecture wraps up our Research Software Engineering journey by reviewing
# what we've learned, exploring important topics we didn't cover, and connecting you with
# the broader RSE community. This session provides perspective on how the course content
# fits together and how you can continue growing as a research software engineer.
#
# **Duration**: 45-60 minutes (half-lecture)
#
# **Note**: This lecture will be augmented later with information about the course exam,
# further educational offers, and a Q&A session.
#
# ## Prerequisites
#
# Before starting this lecture, you should have:
# - Completed Lectures 1-13
# - Hands-on experience with the RSE tools and practices covered
# - A basic understanding of all major topics: version control, Python, testing, CI/CD,
#   documentation, containers, collaboration, data management, workflows, software architecture
#   and design, and AI tools
#
# This final lecture synthesizes everything you've learned into a cohesive whole.
#
# ## Learning Objectives
# - Review and integrate knowledge from all 13 lectures
# - Understand advanced topics beyond this course and how to learn them
# - Connect with the international and German RSE communities
# - Know where to find ongoing support and resources
# - Feel confident continuing your RSE journey
# - Know what to check before using AI tools with sensitive research data, and understand how
#   AI reshapes—rather than replaces—the RSE role

# %% [markdown]
# ## Part 1: Course Summary - What We've Learned
#
# ### The Complete Journey (Lectures 1-13)
#
# Over the past 13 lectures, we've covered a comprehensive path from basic tools to
# professional research software engineering practices. Let's review what we've learned
# and how it all fits together.
#
# #### Lectures 1-2: Foundations
#
# **Lecture 1: Introduction to RSE, Shell Basics, and Git Fundamentals**
# - What RSE is and why it matters for modern research
# - Essential shell commands for navigating and managing files
# - Git basics: commits, repositories, version control workflow
# - **Key takeaway**: Version control is the foundation of professional software development
#
# **Lecture 2: Advanced Git, GitHub & GitLab Collaboration, and Python Concepts for RSE**
# - Branching, merging, and collaborative workflows
# - GitHub and GitLab platforms for code sharing
# - Python concepts for RSE: error handling, context managers, comprehensions, classes
# - **Key takeaway**: Collaboration requires both technical tools and communication
#
# #### Lectures 3-4: From AI Assistance to Project Structure
#
# **Lecture 3: AI-Assisted Coding Foundations**
# - Three categories of AI tools: autocomplete-style, chat-style, agentic
# - The core habit: review every AI suggestion like a diff, verified against a case you can check by hand
# - Common pitfalls: hallucinated APIs, outdated/insecure patterns, automation bias
# - **Key takeaway**: AI generates plausible code, not necessarily correct code—verify before you trust it
#
# **Lecture 4: Python Project Structure and Scientific Libraries**
# - Project organization and package structure
# - Design principles: DRY, Single Responsibility, Separation of Concerns
# - NumPy for numerical computing
# - Matplotlib for visualization
# - **Key takeaway**: Good structure early prevents technical debt later
#
# #### Lectures 5-7: Code Quality and Maintenance
#
# **Lecture 5: Testing Research Software**
# - Why testing matters in research
# - pytest framework and test organization
# - Code coverage and test-driven development
# - Code smells: recognizing design problems
# - **Key takeaway**: Tests are not overhead—they're how you know your code works
#
# **Lecture 6: Automation and Continuous Integration**
# - Automating repetitive tasks
# - GitHub Actions and GitLab CI/CD
# - Automated testing and quality checks
# - **Key takeaway**: Automate what computers do well, focus your time on what requires human judgment
#
# **Lecture 7: Debugging and Profiling**
# - Systematic debugging with pdb
# - Performance profiling and optimization
# - Technical debt and refactoring decisions
# - **Key takeaway**: Debugging is a skill—systematic approaches beat random changes
#
# #### Lectures 8-10: Professional Practices
#
# **Lecture 8: Documenting and Publishing Research Software**
# - Writing effective documentation
# - Docstrings, README files, and user guides
# - Publishing to PyPI and Zenodo
# - **Key takeaway**: Undocumented software has no users (including future you)
#
# **Lecture 9: Containerization and Reproducibility**
# - Docker, Podman, and Apptainer containers
# - Reproducible computational environments
# - Sharing research software reliably
# - **Key takeaway**: "It works on my machine" is not acceptable in research
#
# **Lecture 10: Collaboration and Code Review**
# - Effective code review practices
# - Reviewing for architecture and design
# - Communication in distributed teams
# - **Key takeaway**: Code review improves both code quality and team knowledge
#
# #### Lectures 11-13: Advanced Topics
#
# **Lecture 11: Working with Research Data**
# - File formats: HDF5, NetCDF, CSV
# - Database basics and SQL
# - Pandas for data manipulation
# - **Key takeaway**: Choose data formats based on access patterns and longevity
#
# **Lecture 12: Scientific Workflows and Automation**
# - Make, Snakemake, and Nextflow
# - Workflow design patterns
# - Scaling computational research
# - **Key takeaway**: Workflows make research reproducible and scalable
#
# **Lecture 13: Software Architecture and Design for Research Software**
# - DRY, Single Responsibility, and Separation of Concerns
# - Code smells: god functions, duplication, magic numbers, tight coupling, global state
# - Refactoring versus rewriting, and how to refactor safely
# - Architectural code review
# - **Key takeaway**: Good design habits keep code cheap to change as it grows
#
# ### How It All Fits Together
#
# These lectures aren't isolated topics—they form an integrated approach to research
# software engineering:
#
# **The Foundation Stack**:
# 1. **Version Control (Lecture 1-2)**: Track changes, collaborate safely
# 2. **Python Skills (Lecture 2-4)**: Write clear, maintainable code
# 3. **Testing (Lecture 5)**: Ensure correctness
# 4. **CI/CD (Lecture 6)**: Automate verification
#
# **The Quality Stack**:
# 1. **Debugging (Lecture 7)**: Fix problems systematically
# 2. **Documentation (Lecture 8)**: Make code understandable
# 3. **Code Review (Lecture 10)**: Learn from others, improve together
# 4. **Architecture and Design (Lecture 13)**: Keep code maintainable as it grows
#
# **The Research Stack**:
# 1. **Data Management (Lecture 11)**: Handle research data properly
# 2. **Workflows (Lecture 12)**: Automate analysis pipelines
# 3. **Reproducibility (Lecture 9)**: Enable others to verify your work
#
# ### Skills You've Gained
#
# By completing this course, you can now:
#
# ✅ **Manage code professionally** with Git and GitHub
# ✅ **Write maintainable Python** following best practices
# ✅ **Test your code** systematically with pytest
# ✅ **Automate workflows** with CI/CD and workflow tools
# ✅ **Debug and profile** code effectively
# ✅ **Document** software for yourself and others
# ✅ **Containerize** applications for reproducibility
# ✅ **Collaborate** through code review and version control
# ✅ **Handle research data** with appropriate formats and tools
# ✅ **Use AI assistants** responsibly and effectively
#
# These skills are valuable in:
# - Academic research (thesis work, publications)
# - Research software engineering positions
# - Data science and computational research
# - Industry positions requiring scientific computing
# - Open source scientific software projects

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Ready to solidify what you've learned? Reflect on your RSE journey:</p>
#     <ul>
#         <li><strong>Inventory your new skills</strong>: Pick three lectures that changed
#         how you work. What specific practices have you adopted? Which ones will you
#         implement next week?</li>
#         <li><strong>Review your old code</strong>: Look at a project from before this
#         course. What would you do differently now? What quick wins could you apply
#         (tests, documentation, Git workflow)?</li>
#         <li><strong>Make a learning plan</strong>: From the course topics, which do you
#         want to master? Pick one to dive deep into this month - focused practice beats
#         broad exposure.</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 2: Important Topics We Didn't Cover
#
# ### Why We Can't Cover Everything
#
# Research software engineering is a vast field that intersects with computer science,
# software engineering, and domain-specific research. A comprehensive course would take
# years, not weeks. We've focused on **foundational skills that apply broadly** rather
# than specialized topics that serve narrower audiences.
#
# The topics below are important, but they either:
# - Require the foundations we've built (you're now ready to learn them)
# - Are specific to certain research domains
# - Are rapidly evolving (better learned when you need them)
# - Are too advanced for an introductory course
#
# ### Advanced Software Engineering
#
# **Topics**:
# - Object-oriented programming (classes, inheritance, polymorphism)
# - Design patterns (factory, observer, strategy, etc.)
# - Software architecture (microservices, event-driven, layered)
# - Type systems and static typing (mypy, type hints)
# - Functional programming patterns
#
# **Why we didn't cover them**:
# - You need strong Python fundamentals first (which you now have)
# - Design patterns make more sense with real project experience
# - Many research scripts don't require complex architecture
# - These topics are better learned in context of a specific project
#
# **How to learn more**:
# - *Clean Code* by Robert C. Martin
# - *Design Patterns: Elements of Reusable Object-Oriented Software* by Gang of Four
# - *Fluent Python* by Luciano Ramalho (excellent for advanced Python)
# - *Refactoring: Improving the Design of Existing Code* by Martin Fowler
# - Real Python: https://realpython.com (excellent tutorials on advanced Python)
#
# ### High-Performance Computing (HPC)
#
# **Topics**:
# - Parallel programming (OpenMP, MPI)
# - GPU computing (CUDA, OpenCL, ROCm)
# - Job scheduling systems (SLURM, PBS, LSF)
# - HPC cluster architecture
# - Performance optimization for HPC
#
# **Why we didn't cover them**:
# - HPC is a specialized domain (not all RSEs work on HPC)
# - Requires significant computational resources
# - Often domain-specific (computational chemistry vs. climate modeling)
# - Better taught by HPC centers with hands-on cluster access
#
# **How to learn more**:
# - *Parallel Programming in Science and Engineering* by Demmel et al.
# - LLNL HPC Tutorials: https://hpc.llnl.gov/documentation/tutorials
# - ARCHER2 Training: https://www.archer2.ac.uk/training/
# - Your institution's HPC center (usually offers training)
# - Jülich Supercomputing Centre courses: https://www.fz-juelich.de/en/ias/jsc/education
#
# ### Web Development for Research
#
# **Topics**:
# - Web frameworks (Flask, Django, FastAPI)
# - JavaScript and frontend development
# - RESTful APIs
# - Database design and ORM
# - Web deployment and hosting
#
# **Why we didn't cover them**:
# - Not all research software needs a web interface
# - Web development is a deep specialization
# - Rapidly evolving technologies
# - Many research projects use existing platforms rather than custom web apps
#
# **How to learn more**:
# - *Flask Web Development* by Miguel Grinberg
# - *Two Scoops of Django* by Audrey and Daniel Roy Greenfeld
# - MDN Web Docs: https://developer.mozilla.org/
# - FastAPI documentation: https://fastapi.tiangolo.com/
# - freeCodeCamp: https://www.freecodecamp.org/
#
# ### Machine Learning and Data Science
#
# **Topics**:
# - Scikit-learn for classical machine learning
# - TensorFlow and PyTorch for deep learning
# - Statistical modeling and inference
# - Data cleaning and preprocessing at scale
# - MLOps and model deployment
#
# **Why we didn't cover them**:
# - ML is its own field with dedicated courses
# - Requires statistics and linear algebra background
# - Libraries change rapidly
# - Not all research involves ML/AI
#
# **How to learn more**:
# - *Python Data Science Handbook* by Jake VanderPlas (excellent, free online)
# - *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* by Aurélien Géron
# - Fast.ai courses: https://www.fast.ai/
# - Kaggle Learn: https://www.kaggle.com/learn
# - Coursera Machine Learning Specialization by Andrew Ng
#
# ### Cloud Computing
#
# **Topics**:
# - Cloud platforms (AWS, Google Cloud, Azure)
# - Infrastructure as Code (Terraform, CloudFormation)
# - Kubernetes and container orchestration
# - Serverless computing
# - Cloud cost management
#
# **Why we didn't cover them**:
# - Cloud platforms are commercial products (not always accessible to students)
# - Each platform has its own learning curve
# - Many researchers work on local clusters or university infrastructure
# - Costs can accumulate quickly during learning
#
# **How to learn more**:
# - AWS Free Tier: https://aws.amazon.com/free/
# - Google Cloud Skills Boost: https://www.cloudskillsboost.google/
# - Microsoft Learn for Azure: https://learn.microsoft.com/azure/
# - *Cloud Native DevOps with Kubernetes* by Arundel and Domingus
# - Cloud provider documentation (AWS, GCP, Azure all have excellent tutorials)
#
# ### Specialized Programming Languages
#
# **Topics**:
# - C/C++ for performance-critical code
# - Fortran for legacy scientific codes
# - Julia for scientific computing
# - R for statistical analysis
# - Rust for systems programming
#
# **Why we didn't cover them**:
# - Python is the most accessible language for beginners
# - Learning programming concepts matters more than syntax
# - Most RSE work uses Python or requires interfacing with Python
# - Specialized languages are better learned when needed for a specific project
#
# **How to learn more**:
# - *The C Programming Language* by Kernighan and Ritchie (classic)
# - Learn C++: https://www.learncpp.com/
# - Julia Documentation: https://docs.julialang.org/
# - *The R Book* by Michael Crawley
# - *The Rust Programming Language* (free online book)
#
# ### Software Security
#
# **Topics**:
# - Vulnerability scanning and dependency auditing
# - Secure coding practices
# - Authentication and authorization
# - Encryption and data protection
# - Security in CI/CD pipelines
#
# **Why we didn't cover them**:
# - Security is a deep specialization
# - Many security concepts require web/network knowledge
# - Security threats evolve rapidly
# - Basic security (not committing secrets) was covered in version control
#
# **How to learn more**:
# - OWASP (Open Web Application Security Project): https://owasp.org/
# - *Security Engineering* by Ross Anderson (free online)
# - GitHub Security Features: https://docs.github.com/en/code-security
# - Bandit (Python security linter): https://bandit.readthedocs.io/
# - Snyk Learn: https://learn.snyk.io/
#
# ### Advanced Git and Version Control
#
# **Topics**:
# - Git internals (objects, refs, index)
# - Advanced rebasing and history rewriting
# - Git hooks and automation
# - Monorepo management
# - Alternative version control systems (Mercurial, Perforce)
#
# **Why we didn't cover them**:
# - Basic Git covers 95% of daily work
# - Advanced topics can be confusing without solid Git fundamentals
# - History rewriting is dangerous if misused
# - Better learned when you encounter specific needs
#
# **How to learn more**:
# - *Pro Git* by Scott Chacon and Ben Straub (free online)
# - Git documentation: https://git-scm.com/doc
# - GitHub Git Guides: https://github.com/git-guides
# - Advanced Git tutorials on Atlassian: https://www.atlassian.com/git/tutorials/advanced-overview
#
# ### Domain-Specific Tools
#
# **Examples**:
# - Bioinformatics: BioPython, sequence alignment tools
# - Computational chemistry: OpenMM, RDKit, PyMOL
# - Climate science: xarray, Climate Data Operators (CDO)
# - Astronomy: Astropy, FITS file handling
# - Social sciences: NetworkX, graph analysis tools
#
# **Why we didn't cover them**:
# - Each research domain has unique software ecosystems
# - Tool landscape changes based on field
# - Better learned in domain-specific courses
# - Foundations from this course apply to learning any domain tools
#
# **How to learn more**:
# - Field-specific software carpentry workshops
# - Domain communities (e.g., Bioconductor, Astropy project)
# - Conference tutorials in your field
# - Lab colleagues and domain experts
#
# ### The Good News
#
# **You now have the foundations to learn any of these topics**. This course gave you:
# - How to read documentation and learn new libraries
# - Version control to safely experiment
# - Testing skills to verify your implementations
# - Debugging techniques when things go wrong
# - How to ask good questions and find help
#
# The specific technologies will change, but the practices and principles we've covered
# remain relevant. You're equipped to continue learning independently.

# %% [markdown]
# ## Part 3: The RSE Community - You're Not Alone
#
# ### The International RSE Movement
#
# Research Software Engineering is more than a skillset—it's a growing international
# community dedicated to improving how research software is developed and maintained.
#
# **Society of Research Software Engineering (Society-RSE)**
# - **Website**: https://society-rse.org/
# - **What it is**: International umbrella organization for RSE associations worldwide
# - **Why it matters**: Connects national RSE groups, promotes RSE as a career path
# - **What they offer**:
#   - Annual international RSE conferences (RSECon)
#   - Best practices and policy advocacy
#   - Career resources and job boards
#   - Connection to national RSE groups
#
# **National RSE Associations**
# - UK RSE: https://society-rse.org/community/rse-groups/
# - US-RSE: https://us-rse.org/
# - Nordic RSE: https://nordic-rse.org/
# - RSE-AUNZ (Australia and New Zealand): https://rse-aunz.github.io/
# - And many more growing internationally
#
# ### The German RSE Community
#
# Germany has a particularly active and well-organized RSE community with resources
# specifically relevant to German research institutions.
#
# **de-RSE: Society for Research Software (German RSE Association)**
# - **Website**: https://de-rse.org/en/
# - **German site**: https://de-rse.org/de/
# - **What it is**: German national association for research software and RSEs
# - **What they offer**:
#   - Annual deRSE conference (in Germany, alternating locations)
#   - Local chapters and regional meetups
#   - Mailing lists and communication channels
#   - Policy work with German research organizations
#   - Position papers and best practice guidelines
# - **How to get involved**:
#   - Join the mailing list
#   - Attend the annual conference (highly recommended!)
#   - Participate in local chapter meetings
#   - Contribute to community discussions
#
# ### Helmholtz Association RSE Resources
#
# The Helmholtz Association has invested significantly in RSE infrastructure and training.
#
# **Helmholtz Platform for Research Software Engineering (HiRSE)**
# - **Website**: https://www.helmholtz-hirse.de/
# - **What it is**: Helmholtz-wide initiative to support RSE practices
# - **What they offer**:
#   - Incubator program for RSE projects
#   - Community building across Helmholtz centers
#   - Software engineering expertise and consulting
#   - Collaboration platforms and tools
#
# **HiRSE Seminar Series**
# - **Website**: https://www.helmholtz-hirse.de/series.html
# - **What it is**: Regular online seminars on RSE topics
# - **Topics covered**:
#   - Best practices in research software development
#   - Emerging tools and technologies
#   - Case studies from Helmholtz centers
#   - Career development for RSEs
# - **How to participate**:
#   - Check the website for upcoming seminars
#   - Seminars are typically recorded and available online
#   - Open to anyone interested (not just Helmholtz employees)
#
# ### Forschungszentrum Jülich RSE Team
#
# Jülich Supercomputing Centre has a dedicated RSE team supporting research software
# across the center.
#
# **Jülich RSE Team**
# - **Website**: https://www.fz-juelich.de/en/rse
# - **What they offer**:
#   - Software engineering consulting for research projects
#   - Training courses and workshops
#   - Best practices guidance
#   - Code review and quality assessment
#   - HPC expertise combined with software engineering
# - **Services**:
#   - Project consultations
#   - Software architecture design
#   - Performance optimization
#   - CI/CD setup and automation
# - **How to connect**:
#   - Visit the website for contact information
#   - Attend Jülich training events
#   - Reach out for project support
#
# ### Communication Channels
#
# The RSE community is active and welcoming. Here's how to connect:
#
# **Matrix Chat (National RSE Chat for Germany)**
# - **What it is**: Decentralized, open-source chat platform
# - **German RSE channel**: Check de-rse.org for current Matrix server and channels
# - **Why Matrix**:
#   - Open source and privacy-respecting
#   - No commercial tracking
#   - Federation allows institutional control
#   - Growing adoption in research communities
# - **How to join**:
#   - Create Matrix account (element.io is a popular client)
#   - Join German RSE channels (links on de-rse.org)
#   - Introduce yourself and ask questions
#
# **Mailing Lists**
# - **de-RSE mailing list**: Subscribe via https://de-rse.org/en/join.html
# - **Society-RSE announcements**: Available through society-rse.org
# - **Helmholtz RSE list**: Check with your Helmholtz center
#
# **Social Media and Forums**
# - **Mastodon**: Many RSEs are on Mastodon (decentralized Twitter alternative)
# - **LinkedIn**: Search for "Research Software Engineering" groups
# - **GitHub Discussions**: Many RSE projects use GitHub for community discussions
#
# **Conferences and Events**
# - **deRSE Conference**: Annual German RSE conference (check de-rse.org)
# - **RSECon**: International RSE conference (check society-rse.org)
# - **Local Meetups**: Check de-rse.org for regional chapters
# - **Helmholtz seminars**: Regular online seminars (helmholtz-hirse.de)
#
# ### Getting Help and Staying Current
#
# **For technical questions**:
# - Stack Overflow: https://stackoverflow.com/ (tag your questions appropriately)
# - GitHub Discussions for specific projects
# - RSE Slack/Matrix channels (domain-specific help)
# - Your institution's RSE team or help desk
#
# **For career development**:
# - Society-RSE job board
# - National RSE association career resources
# - Helmholtz career development programs
# - Conference networking
#
# **For staying current**:
# - Subscribe to relevant mailing lists
# - Follow RSE organizations on social media
# - Attend conferences and seminars
# - Join paper reading groups or coding clubs
# - Contribute to open source projects
#
# **For learning new skills**:
# - Software Carpentry workshops: https://software-carpentry.org/
# - The Carpentries (includes Data Carpentry, Library Carpentry): https://carpentries.org/
# - Your institution's training programs
# - Online courses and tutorials (references from Part 2)

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Curious about what's next in your RSE journey? Explore these growth paths:</p>
#     <ul>
#         <li><strong>Pick one advanced topic</strong>: From Part 2, choose something that
#         excites you (HPC, web dev, ML, etc.). Spend 30 minutes exploring - read an
#         article, watch a tutorial. Is this your next learning goal?</li>
#         <li><strong>Attend an RSE event</strong>: Find the next de-RSE meetup, HiRSE seminar, or local coding club. Mark your
#         calendar now - community connections matter more than you think!</li>
#         <li><strong>Map your learning path</strong>: Where do you want to be in 6 months? 1 year? What skills would get you
#         there? Write down 3-5 concrete learning goals and share them with a friend for accountability.</li>
#     </ul>
# </div>

# %% [markdown]
# ### Contributing to the Community
#
# As you grow in your RSE journey, consider giving back:
#
# - **Share your experience**: Give talks at local meetups
# - **Mentor others**: Help newcomers learn RSE practices
# - **Write tutorials**: Document what you've learned
# - **Contribute to open source**: Find projects aligned with your research
# - **Review code**: Help improve others' work
# - **Organize events**: Start a local coding club or study group
# - **Advocate for RSE**: Promote good practices in your research group
#
# The RSE community thrives on mutual support and knowledge sharing. Your contributions,
# no matter how small, make a difference.

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Ready to give back and grow the RSE community? Start contributing today:</p>
#     <ul>
#         <li><strong>Teach someone something</strong>: Find a colleague struggling with
#         Git, testing, or Python. Spend 30 minutes helping them. Teaching solidifies your
#         own understanding and builds community!</li>
#         <li><strong>Contribute to open source</strong>: Find a scientific package you use.
#         Check their issues for "good first issue" or "documentation" labels. Even fixing
#         a typo helps - and you'll learn their workflow!</li>
#         <li><strong>Document your journey</strong>: Write a blog post, create a tutorial,
#         or give a talk about what you learned in this course. Future you (and others!)
#         will appreciate it. Share your knowledge!</li>
#     </ul>
# </div>

# %% [markdown]
# ### Using AI Responsibly: Legal, Ethical, and Data Protection Considerations
#
# Lecture 3 introduced the technical habits for working with AI coding assistants safely.
# Before you rely on them in a real research project, there are a few institutional and legal
# considerations worth knowing about too—not a complete legal briefing, but things to check
# before they become a problem.
#
# **Licensing and copyright**: Lecture 3 focused on whether AI-generated code is *correct*.
# There's a separate question: is it *yours to use*? AI models are trained on large amounts of
# existing code, some of it under licenses (like GPL) that impose obligations on anything
# derived from it, and AI-generated code can closely resemble licensed code without any visible
# indication that it does. There's no simple test to check this yourself, but treating
# AI-generated code the way you'd treat code copied from a random web page—unknown provenance
# until proven otherwise—is a reasonable default.
#
# **Data protection and privacy**: Whatever you paste into a chat-based AI assistant may leave
# your institution's control, depending on the tool and how it's configured. Before pasting
# unpublished results, patient data, proprietary data, or anything covered by a data-sharing
# agreement into a cloud-based tool, check your institution's policy—many research institutions
# now have explicit rules about this, precisely because "just ask the AI" is an easy habit to
# fall into without thinking about where the data goes.
#
# **When self-hosted tools matter**: For genuinely sensitive data, self-hosted or local AI
# models—running entirely on infrastructure you or your institution control—avoid sending data
# to a third party at all. They typically lag behind the largest cloud-based models in
# capability, which is a real trade-off, but for some research data that's the right trade-off
# to make. It's worth knowing the option exists before you need it.
#
# **The practical takeaway**: none of this requires becoming a lawyer. It requires knowing
# these questions exist, checking your institution's policy before you're mid-deadline and
# tempted to skip that step, and applying the same "verify before you trust it" habit from
# Lecture 3 to claims about what a tool does or doesn't do with your data.

# %% [markdown]
# ## Part 4: Next Steps and Closing Thoughts
#
# ### What Comes Next for This Course
#
# **Future additions to this lecture**:
#
# This lecture will be augmented with additional content:
# - **Exam Information**: Details about course assessment and requirements
# - **Further Educational Offers**: Advanced courses and continuing education
# - **Extended Q&A Session**: Time for your questions and discussion
# - **Feedback and Course Evaluation**: Your input to improve the course
#
# Watch for announcements about these additions.
#
# ### Continuing Your RSE Journey
#
# **In the next week**:
# - Review lecture materials and fill in gaps
# - Pick one new skill from Part 2 that interests you
# - Join at least one RSE communication channel (Matrix, mailing list, etc.)
# - Identify a research project where you can apply these skills
#
# **In the next month**:
# - Apply testing practices to your current research code
# - Set up CI/CD for a project
# - Attend an RSE meetup or seminar
# - Contribute to documentation for a project you use
#
# **In the next year**:
# - Attend an RSE conference (deRSE or RSECon)
# - Mentor someone learning RSE skills
# - Contribute to an open source scientific software project
# - Consider RSE as a career path (if it interests you)
#
# ### Career Paths for RSEs
#
# Research Software Engineering skills open many doors:
#
# **Academic Research**:
# - PhD work with strong computational component
# - Postdoctoral research in computational fields
# - Research scientist positions
# - Group leader in computational research
#
# **RSE Career Track**:
# - RSE positions at universities and research centers
# - HPC centers (computational science and engineering)
# - Core facilities and shared infrastructure
# - Scientific software development teams
#
# **Industry Transitions**:
# - Data science and analytics
# - Software engineering at tech companies
# - Scientific computing in industry (pharma, finance, aerospace)
# - Developer relations and technical writing
#
# **Education and Training**:
# - Teaching computational methods
# - Developing training materials
# - Software Carpentry instruction
# - Technical workshop facilitation
#
# RSE skills are increasingly valued—many institutions are creating dedicated RSE
# positions recognizing that good software is essential to modern research.
#
# ### AI and the Future of the RSE Role
#
# It's worth asking directly: if AI can write code, what's left for an RSE to do? The honest
# answer has been consistent in every lecture that touched AI: AI changes *how* you work, not
# *whether* the work needs you.
#
# What AI is good at is generating code that matches patterns it has seen before. What it can't
# do is know whether a normalization method matches your specific dataset (Lecture 3), whether a
# test actually verifies the behavior you care about (Lecture 5), whether a fix addresses the
# root cause or just silences the symptom (Lecture 7), whether a docstring matches what the code
# actually does at the boundaries (Lecture 8), or whether a design decision will hold up as a
# research codebase grows. Those all require domain knowledge, critical judgment, and the
# verification habits this course has spent 14 lectures building—exactly what AI doesn't have.
#
# **What this means for your career**: RSE skills aren't becoming less valuable because AI can
# write code faster. They're becoming more valuable, because the bottleneck shifts from "can
# someone write this code" to "can someone tell whether the code is right"—and that's a skill
# only you bring. The RSE who knows how to review, test, and verify is more useful with AI tools
# available, not less.
#
# ### Final Thoughts
#
# **You've learned a lot**. From command-line basics to AI-assisted development,
# from writing your first Python function to setting up CI/CD pipelines. These skills
# will serve you throughout your research career.
#
# **You're part of a community**. RSE isn't practiced in isolation. Connect with the
# de-RSE community, attend events, ask questions, and share what you learn.
#
# **Software is research**. The code you write, the tools you build, the workflows you
# create—these are research outputs as valuable as papers. Treat them professionally.
#
# **Keep learning**. Technology changes, but the principles remain. Stay curious, try
# new tools, and always ask "is there a better way?"
#
# **Be patient with yourself**. Becoming proficient at RSE takes time and practice. You
# will make mistakes, write bad code, and break things. That's part of learning.
#
# **Share your knowledge**. When you've learned something, help others learn it too.
# The RSE community grows stronger when we support each other.
#
# ### Acknowledgments
#
# This course builds on the work of many people and organizations:
# - The Alan Turing Institute's RSE course
# - The Carpentries workshops and materials
# - Society of Research Software Engineering
# - de-RSE community
# - Helmholtz HiRSE platform
# - Forschungszentrum Jülich RSE team
# - Countless open source contributors
#
# Thank you for your participation in this course. May your code be bug-free, your tests
# comprehensive, and your research impactful.
#
# **Good luck on your research software engineering journey!**

# %% [markdown]
# ## Additional Resources
#
# ### Quick Reference Links
#
# **RSE Communities**:
# - Society of Research Software Engineering: https://society-rse.org/
# - de-RSE (German RSE): https://de-rse.org/en/
# - Helmholtz HiRSE: https://www.helmholtz-hirse.de/
# - HiRSE Seminar Series: https://www.helmholtz-hirse.de/series.html
# - Jülich RSE Team: https://www.fz-juelich.de/en/rse
#
# **Learning Resources**:
# - Software Carpentry: https://software-carpentry.org/
# - The Carpentries: https://carpentries.org/
# - Real Python: https://realpython.com/
# - Research Software Engineering with Python: https://third-bit.com/py-rse/
# - The Turing Way: https://the-turing-way.netlify.app/
#
# **Documentation and References**:
# - Python Documentation: https://docs.python.org/3/
# - Git Documentation: https://git-scm.com/doc
# - pytest Documentation: https://docs.pytest.org/
# - NumPy Documentation: https://numpy.org/doc/
#
# ### Course Materials
#
# All lecture materials are available at:
# - **Repository**: https://github.com/pancetta/RSE_course_JuRSE
# - **License**: MIT License (free to use and adapt)
# - **Contributions**: Welcome via pull requests
#
# ### Feedback
#
# Your feedback helps improve this course for future students. Please share:
# - What worked well
# - What could be improved
# - Topics you wish were covered
# - Suggestions for examples or exercises
#
# ---
#
# **Thank you and happy coding!** 🚀
