# Automated Conda Dependency Management Solution

## Summary

This solution provides automated dependency testing and updating for conda environments while ensuring the repository always contains executable versions of the lectures.

## What Was Added

### 1. GitHub Actions Workflow
**File:** `.github/workflows/conda-dependency-update.yml`

An automated workflow that:
- Runs weekly (every Monday at 9:00 UTC)
- Can be manually triggered via GitHub Actions UI
- Tests all dependencies with updated versions
- Creates conda-lock files for reproducibility
- Automatically creates a PR if tests pass
- Does NOT create a PR if tests fail (maintains current working versions)

### 2. Python Testing Script
**File:** `update_dependencies.py`

A comprehensive script that:
- Tests environments against full CI suite
- Creates conda-lock files for all platforms (linux-64, osx-64, osx-arm64, win-64)
- Provides detailed diagnostic output
- Can be run locally for development

### 3. Makefile Targets
**Added to:** `Makefile`

New convenience targets:
- `make test-deps` - Test current dependencies without creating lock files
- `make update-deps` - Test dependencies and create lock files
- `make create-locks` - Just create lock files (no testing)

### 4. Documentation

**DEPENDENCY_MANAGEMENT.md**
- Complete guide to the dependency system
- How the automated workflow works
- How to handle failing updates
- How to pin problematic versions
- Lock file management

**TESTING_DEPENDENCIES.md**
- Detailed testing instructions
- How to test locally
- How to test the GitHub Actions workflow
- How to simulate and handle failures
- Debugging tips

**.github/workflows/README.md**
- Overview of all workflows
- Customization options
- Monitoring and debugging

**README.md updates**
- Added section on automated dependency updates
- Links to detailed guides
- Usage examples

### 5. Optional Files

**ci-with-locks.yml.example**
- Example of how to modify CI to use lock files
- Provides even more reproducibility
- Can be adopted when lock files are established

## How It Works

### Weekly Automated Process

1. **Every Monday at 9:00 UTC**, the workflow runs automatically
2. **Creates lock files** with latest compatible package versions
3. **Tests the environment** by:
   - Running flake8 linting
   - Checking Python syntax
   - Converting lectures to notebooks
   - Executing all notebooks
4. **If all tests pass**:
   - Commits lock files
   - Creates a PR with title "chore: Update conda dependencies"
   - Adds labels: "dependencies", "automated"
   - Assigns to repository owner
5. **If tests fail**:
   - No PR is created
   - Workflow logs show what failed
   - Current working versions are maintained

### Manual Process

Developers and maintainers can also:

```bash
# Test current dependencies
make test-deps

# Test and create lock files
make update-deps

# Manual workflow trigger via GitHub UI
# Go to Actions → Conda Dependency Update → Run workflow
```

## Handling Dependency Failures

When a new package version breaks compatibility:

### What Happens
1. Weekly workflow runs
2. Tests fail with the new version
3. No PR is created
4. Repository maintains current working versions

### What To Do
1. **Check the workflow logs** to identify the problematic package
2. **Pin the version** in `environment.yml`:
   ```yaml
   # environment.yml
   dependencies:
     - matplotlib>=3.5.0,<3.9.0  # Exclude breaking version
     # or
     - numpy==1.24.3  # Pin to specific working version
   ```
3. **Add a comment** explaining why the pin is needed
4. **Test locally**: `make test-deps`
5. **Commit the pinned version**
6. **Next weekly run** will test with the pinned version
7. **Optional**: Open an issue with the package maintainer

### Example Pinning

```yaml
name: rse_lecture
channels:
  - conda-forge
dependencies:
  - python>=3.7
  - jupytext>=1.14.0
  - jupyter>=1.0.0
  - notebook>=6.5.0
  - numpy>=1.21.0,<2.0.0  # Pinned: v2.0 has breaking changes
  - jupyter-book>=2.0.0
  - matplotlib>=3.5.0,<3.9.0  # Pinned: v3.9+ breaks with our code
```

## Lock Files for Reproducibility

### What are Lock Files?

Lock files contain exact versions of all packages and their dependencies:
- Exact version numbers
- Build strings
- Package hashes
- Platform information

This ensures bit-for-bit reproducible environments.

### Using Lock Files

```bash
# Install from lock file (exact versions)
micromamba create -n rse_lecture --file environment-linux-64.lock

# Platform-specific files
# - environment-linux-64.lock
# - environment-osx-64.lock
# - environment-osx-arm64.lock
# - environment-win-64.lock
```

### When Lock Files are Created

Lock files are created/updated when:
1. Weekly automated workflow runs and tests pass
2. Manual run: `make create-locks` or `make update-deps`
3. After pinning a problematic version

## Benefits of This Solution

1. **Automated Updates**: No manual dependency management needed
2. **Always Executable**: Repository always has tested, working versions
3. **Fail-Safe**: Broken updates don't get merged
4. **Reproducible**: Lock files ensure exact environment recreation
5. **Cross-Platform**: Supports Linux, macOS (Intel & ARM), Windows
6. **Transparent**: PRs show exactly what changed
7. **Simple**: Works with existing conda workflows, no migration to pip
8. **Educational**: Clear documentation and examples

## Simple Solution

Yes, this is a simple solution that:
- ✅ Requires minimal maintenance (just review PRs)
- ✅ Uses conda/micromamba (not pip)
- ✅ Automatically tests dependencies
- ✅ Handles failures gracefully
- ✅ Maintains working versions
- ✅ Provides reproducibility
- ✅ Integrates with existing CI

## Quick Start

1. **Wait for the first automated run** (next Monday at 9:00 UTC)
2. **Review the PR** when it appears (if tests pass)
3. **Merge the PR** to update lock files
4. **If no PR appears**, check workflow logs for failures
5. **Pin problematic versions** as needed

## Testing Before First Run

You can test manually before the first automated run:

```bash
# 1. Install conda-lock
micromamba install -c conda-forge conda-lock

# 2. Test current dependencies
make test-deps

# 3. Create lock files
make create-locks

# 4. Commit lock files
git add *-*.lock lecture_*/*-*.lock
git commit -m "chore: add initial conda lock files"
git push
```

## Files Added to Repository

```
.github/workflows/
  ├── conda-dependency-update.yml  (Automated workflow)
  ├── ci-with-locks.yml.example    (Optional enhanced CI)
  └── README.md                     (Workflows documentation)

update_dependencies.py               (Testing script)
DEPENDENCY_MANAGEMENT.md             (Complete guide)
TESTING_DEPENDENCIES.md              (Testing instructions)
Makefile                             (Updated with new targets)
README.md                            (Updated with new section)
```

## What You Need to Do

### Immediately
- Nothing! The system is ready to go

### Weekly (when PRs appear)
- Review the automated PR
- Check what packages were updated
- Merge if everything looks good

### When Tests Fail (no PR created)
- Check workflow logs
- Pin problematic versions
- Commit the pins

## Support

For detailed information:
- **DEPENDENCY_MANAGEMENT.md** - Complete dependency guide
- **TESTING_DEPENDENCIES.md** - Testing and debugging
- **.github/workflows/README.md** - Workflow details
- **README.md** - Updated with usage examples

## Customization

### Change Schedule

Edit `.github/workflows/conda-dependency-update.yml`:

```yaml
on:
  schedule:
    - cron: '0 9 * * 1'  # Change this line
```

### Add More Platforms

Edit the platforms list in `update_dependencies.py` or the workflow.

### Modify Tests

The workflow runs the same tests as CI. To change tests, modify both CI and dependency update workflow.

## Conclusion

This solution ensures your repository always contains executable versions of the lectures by:
1. Automatically testing dependency updates
2. Creating reproducible lock files
3. Only merging updates that pass all tests
4. Maintaining current versions when updates fail
5. Providing clear documentation and tools

All while staying with conda/micromamba (no pip migration required).
