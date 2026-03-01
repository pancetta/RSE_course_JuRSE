# Testing the Dependency Update System

This document provides instructions for testing the automated dependency update system.

## Prerequisites

Install conda-lock:
```bash
micromamba install -c conda-forge conda-lock
# or
conda install -c conda-forge conda-lock
# or
pip install conda-lock
```

## Local Testing

### 1. Test Current Dependencies

Test that the current environment files work correctly:

```bash
make test-deps
```

This will:
- Create a temporary test environment
- Run all CI checks (lint, syntax, conversion, execution)
- Report success or failure
- Clean up the test environment

**Expected output:**
```
============================================================
Testing environment from: environment.yml
============================================================

Creating test environment...
...
=== Running flake8 lint checks ===
...
=== Checking Python syntax ===
...
=== Converting lectures to notebooks ===
...
=== Executing notebooks ===
...
✅ All tests passed!
```

### 2. Create Lock Files

Generate lock files for all supported platforms:

```bash
make create-locks
```

This creates:
- `environment-linux-64.lock` - Environment for Linux
- Same for `osx-64`, `osx-arm64`, `win-64`

**Note:** Lock file creation requires conda-lock to be installed.

### 3. Test and Create Lock Files (Full Update)

Run both testing and lock file creation:

```bash
make update-deps
```

This is what the automated workflow does weekly.

## Testing the GitHub Actions Workflow

### Manual Trigger

1. Go to your GitHub repository
2. Click on "Actions" tab
3. Select "Conda Dependency Update" workflow
4. Click "Run workflow" button
5. Select the branch and click "Run workflow"

The workflow will:
- Set up micromamba
- Create lock files for all platforms
- Test the environment with all CI checks
- Commit lock files if tests pass
- Create a PR with the updates

### Test on Different Platforms

The workflow only runs on `ubuntu-latest` by default for lock file creation. To test on other platforms, you can modify the workflow temporarily:

```yaml
jobs:
  test-dependencies:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
```

## Verifying Lock Files

After creating lock files, verify they work:

```bash
# Create environment from lock file
micromamba create -n test-from-lock --file environment-linux-64.lock

# Activate and test
micromamba activate test-from-lock
python scripts/convert_to_notebooks.py
# ... run other tests ...

# Clean up
micromamba deactivate
micromamba env remove -n test-from-lock
```

## Testing Failure Scenarios

### Simulating a Breaking Dependency Update

To test how the system handles breaking changes:

1. **Edit environment.yml** to include a known incompatible version:
   ```yaml
   dependencies:
     - numpy>=2.0.0  # Might break with older code
   ```

2. **Run the test**:
   ```bash
   make test-deps
   ```

3. **Expected behavior**:
   - Tests should fail
   - Script should report the failure
   - No lock files should be created
   - Exit code should be non-zero

4. **Fix the issue** by pinning the working version:
   ```yaml
   dependencies:
     - numpy>=1.21.0,<2.0.0  # Exclude breaking version
   ```

5. **Re-test**:
   ```bash
   make test-deps
   ```

6. **Now tests should pass**

## Continuous Integration Testing

The automated workflow runs weekly. To verify it's working:

### Check Recent Workflow Runs

1. Go to Actions → Conda Dependency Update
2. Check the status of recent runs
3. View logs to see what was tested

### Check for Automated PRs

If dependency updates are available and tests pass:
1. A PR will be automatically created
2. Title: "chore: Update conda dependencies"
3. Labels: "dependencies", "automated"
4. The PR description will show what was tested

### If No PR is Created

Possible reasons:
1. **No updates available** - Dependencies are already at latest compatible versions
2. **Tests failed** - New versions broke compatibility
3. **Workflow error** - Check the workflow logs

## Common Issues and Solutions

### "conda-lock: command not found"

Install conda-lock:
```bash
micromamba install -c conda-forge conda-lock
```

### "micromamba: command not found"

The testing script requires micromamba. Install from:
https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html

Or use conda/mamba instead by modifying the script to use `conda` command.

### Lock file creation fails for a platform

This usually means packages aren't available for that platform. Options:
1. Remove the platform from the list
2. Use platform-specific environment files
3. Check if all dependencies support the platform

### Tests pass locally but fail in CI

Possible causes:
1. Platform differences (test locally on Linux for CI)
2. Different micromamba/conda versions
3. Cache issues in CI

## Development Workflow

When working on the dependency system:

1. **Make changes** to workflow or script
2. **Test locally** with `make test-deps`
3. **Commit and push** to a feature branch
4. **Manually trigger** the workflow on your branch
5. **Verify** it works as expected
6. **Merge** to main

## Expected Behavior Summary

| Scenario | Test Result | Lock Files Created | PR Created |
|----------|-------------|-------------------|------------|
| No updates, all pass | ✅ Pass | ❌ No | ❌ No |
| Updates available, tests pass | ✅ Pass | ✅ Yes | ✅ Yes |
| Updates available, tests fail | ❌ Fail | ❌ No | ❌ No |
| Lock files exist, no updates | ✅ Pass | ❌ No | ❌ No |

## Debugging Tips

### View detailed test output

```bash
# Run script directly with verbose output
python update_dependencies.py --test-only 2>&1 | tee test-output.log
```

### Check lock file contents

```bash
# View lock file to see exact versions
cat environment-linux-64.lock | grep "name:"
```

### Test specific lecture

```bash
# Create environment and test a specific lecture
micromamba create -n lecture-test --file environment-linux-64.lock
micromamba activate lecture-test
python scripts/convert_to_notebooks.py
jupyter nbconvert --to notebook --execute lecture_04/lecture_04.ipynb
```

## Next Steps

After successful testing:
1. Let the automated workflow run weekly
2. Review and merge PRs when they appear
3. Monitor for any failures
4. Pin versions when necessary
5. Keep lock files in sync with environment files
