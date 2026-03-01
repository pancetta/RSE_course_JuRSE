# Dependency Management Guide

This guide explains how the automated dependency management system works and how to handle dependency updates.

## Overview

The repository uses conda for dependency management with an automated update system that:
- Tests dependency updates weekly
- Creates lock files for reproducibility
- Automatically proposes updates via Pull Requests
- Maintains working versions when updates break compatibility

## System Components

### 1. Conda Environment Files

- `environment.yml` - Environment with all dependencies for all lectures

### 2. Conda Lock Files

Lock files ensure reproducible environments across different platforms:
- `environment-{platform}.lock` - Locked environment

Supported platforms: `linux-64`, `osx-64`, `osx-arm64`, `win-64`

### 3. Automated Workflow

**`.github/workflows/conda-dependency-update.yml`**
- Runs every Monday at 9:00 UTC
- Can be triggered manually via GitHub Actions UI
- Tests all dependencies with lecture materials
- Creates lock files if tests pass
- Opens PR with updates

### 4. Update Script

**`update_dependencies.py`**
- Python script for local testing
- Tests environments against CI checks
- Creates lock files for all platforms
- Provides diagnostic output

## Using the System

### For Users

Install from lock files for exact reproducibility:

```bash
# Linux
micromamba create -n rse_lecture --file environment-linux-64.lock

# macOS Intel
micromamba create -n rse_lecture --file environment-osx-64.lock

# macOS Apple Silicon
micromamba create -n rse_lecture --file environment-osx-arm64.lock

# Windows
micromamba create -n rse_lecture --file environment-win-64.lock
```

### For Developers

Test your changes before committing:

```bash
# Test current dependencies
make test-deps

# Test and create lock files
make update-deps
```

### For Maintainers

#### Handling Automated Update PRs

When the automated workflow creates a PR:

1. **Review the changes**: Check which packages were updated in the lock files
2. **Verify CI passes**: The PR will only be created if tests passed
3. **Merge the PR**: If everything looks good, merge it
4. **Lock files are updated**: Users can now install the tested versions

#### Handling Failed Updates

If the weekly workflow fails (no PR created):

1. **Check workflow logs** in GitHub Actions to identify the failing package
2. **Reproduce locally**:
   ```bash
   make test-deps
   ```
3. **Investigate the failure**:
   - Is it a known bug in the new version?
   - Is there a breaking change?
   - Is it an incompatibility between packages?

4. **Pin the problematic version**:
   
   Edit `environment.yml`:
   ```yaml
   dependencies:
     # Pin to exclude breaking version
     - matplotlib>=3.5.0,<3.9.0
     
     # Or pin to specific working version
     - numpy==1.24.3
   ```

5. **Test the pinned version**:
   ```bash
   make test-deps
   ```

6. **Commit and push** the pinned version

7. **Document the issue**:
   - Add a comment in the environment file explaining why
   - Open an issue with the package maintainer if it's a bug

8. **Next weekly run** will test with the pinned version

#### Adding New Dependencies

When adding a new dependency to a lecture:

1. **Add to `environment.yml`**

2. **Test locally**:
   ```bash
   make test-deps
   ```

3. **Create lock files**:
   ```bash
   make create-locks
   ```

4. **Commit both** environment file and lock files

5. **The automated workflow** will keep testing the new dependency weekly

## Lock File Management

### When to Update Lock Files

Lock files should be updated when:
- Dependencies in environment files change
- The automated workflow finds compatible updates
- A manual dependency update is needed

### How Lock Files are Created

The `update_dependencies.py` script uses `conda-lock` to:
1. Resolve all dependencies for each environment
2. Create platform-specific lock files
3. Include exact version pins and build numbers

### Lock File Format

Lock files are YAML files containing:
- Exact package versions
- Build strings
- Package hashes
- Channel information
- Platform metadata

This ensures bit-for-bit reproducible environments.

## Troubleshooting

### "Lock file creation failed"

**Cause**: conda-lock couldn't resolve dependencies for a platform

**Solution**:
1. Check if all packages are available on conda-forge for that platform
2. Consider removing platform-specific lock file if the platform isn't supported
3. Check for conflicting version constraints

### "Tests fail with lock files but pass without"

**Cause**: Lock files may be outdated

**Solution**:
```bash
# Delete old lock files
rm -f *-*.lock lecture_*/*-*.lock

# Recreate them
make create-locks
```

### "Automated workflow doesn't create PR"

**Possible causes**:
1. Tests failed with updated dependencies
2. No dependency updates available
3. Workflow permissions issue

**Solution**:
1. Check workflow logs in GitHub Actions
2. Run `make test-deps` locally to reproduce
3. Fix failing tests or pin problematic versions

## Best Practices

1. **Always test before committing** environment changes
2. **Include lock files** in commits when updating dependencies
3. **Document pinned versions** with comments explaining why
4. **Review automated PRs promptly** to keep dependencies current
5. **Use lock files in CI** for reproducible tests
6. **Keep lock files for all platforms** to ensure cross-platform compatibility

## Manual Workflow

If you need to update dependencies manually (outside the automated workflow):

```bash
# 1. Update environment.yml as needed
vim environment.yml

# 2. Test the changes
make test-deps

# 3. If tests pass, create lock files
make create-locks

# 4. Commit everything
git add environment.yml *-*.lock
git commit -m "chore: update dependencies"
git push

# 5. Create a PR or merge to main
```

## Resources

- [Conda Lock Documentation](https://github.com/conda/conda-lock)
- [Conda Environment Files](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
- [GitHub Actions Workflows](https://docs.github.com/en/actions/using-workflows)
