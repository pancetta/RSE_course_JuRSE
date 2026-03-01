# GitHub Actions Workflows

This directory contains the continuous integration and deployment workflows for the RSE Lectures repository.

## Active Workflows

### ci.yml
**CI - Lecture Scripts**

Runs on every push and pull request to main/master branches.

**Purpose:**
- Ensure code quality and functionality
- Verify lectures work across platforms

**What it does:**
1. Sets up micromamba environment
2. Lints code with flake8
3. Checks Python syntax
4. Converts lectures to notebooks
5. Executes all notebooks to verify they run

**Platforms tested:**
- Ubuntu (latest)
- macOS (latest and 26)
- Windows (latest)

**Trigger:** Push or PR to main/master

---

### deploy.yml
**Deploy Jupyter Book**

Deploys the lecture website to GitHub Pages.

**What it does:**
1. Waits for CI workflow to complete successfully
2. Converts lectures to notebooks
3. Executes notebooks to generate plots
4. Builds static HTML with Jupyter Book
5. Deploys to GitHub Pages

**Trigger:** 
- Automatically after CI workflow completes successfully on main branch
- Manual workflow dispatch

**Dependencies:**
- Only runs after "CI - Lecture Scripts" workflow completes successfully
- This ensures deployment only happens when all tests pass

---

### conda-dependency-update.yml
**Conda Dependency Update**

Automated dependency testing and update system.

**Purpose:**
- Keep dependencies up-to-date
- Ensure compatibility of new versions
- Maintain reproducible environments

**What it does:**
1. Creates conda-lock files with latest compatible versions
2. Tests the updated environment against all CI checks
3. Commits lock files if tests pass
4. Creates a PR with the updates

**Trigger:**
- Weekly on Mondays at 9:00 UTC
- Manual workflow dispatch

**Behavior:**
- ✅ Tests pass → PR created with updates
- ❌ Tests fail → No PR, maintainers need to pin problematic versions
- ℹ️ No updates → No PR, no action needed

For more details, see [dependency management documentation](../../docs/)

---

### link-checker.yml
**Link Checker**

Automated link validation for documentation and lecture materials.

**Purpose:**
- Monitor broken or stale links
- Provide informational reports about link health
- Maintain high-quality documentation over time

**What it does:**
1. Scans all markdown files (README, docs, etc.)
2. Scans all lecture Python files (lecture_*.py)
3. Validates each link (with retries for robustness)
4. Saves detailed report as artifact
5. Reports results without failing the build (informational only)

**Trigger:**
- Weekly on Mondays at 10:00 UTC (after dependency updates)
- Manual workflow dispatch

**Configuration:**
- Settings in `.lycherc.toml` at repository root
- Excludes example/placeholder URLs (localhost, github.com/user/*, etc.)
- Excludes flaky sites that block bots or have intermittent issues
- 30-second timeout per request (increased for slow sites)
- 3 retries with 5-second wait time between retries
- Custom user agent to avoid being blocked
- Accepts status codes including redirects and rate limiting (429)

**Typical results:**
- ~340 total links checked
- ~12 seconds execution time (instant with cache)
- Detailed report available as workflow artifact (30-day retention)

**Why informational only?**
Many sites have intermittent issues (rate limiting, temporary downtime, bot blocking) that
cause false positives. Running as informational allows monitoring without breaking CI/CD.

**Customization:**
To exclude additional URLs, edit `.lycherc.toml` and add patterns to the `exclude` array.

---

## Optional/Example Workflows

### ci-with-locks.yml.example
**CI with Lock Files (Optional)**

Example of how to modify CI to use conda lock files for more reproducible builds.

**To use:**
1. Generate lock files: `make create-locks`
2. Commit lock files
3. Replace `ci.yml` with this workflow

**Benefits:**
- Exact reproducibility of builds
- Faster environment creation
- Protection against breaking updates

**Trade-offs:**
- Lock files must be kept up-to-date
- Larger repository size
- Manual updates required more often

---

## Workflow Permissions

All workflows use minimal required permissions:

- **ci.yml**: `contents: read` - Read repository contents
- **deploy.yml**: `contents: read`, `pages: write`, `id-token: write` - Deploy to Pages
- **conda-dependency-update.yml**: `contents: write`, `pull-requests: write` - Create PRs
- **link-checker.yml**: `contents: read` - Read repository contents for link checking

## Customization

### Changing Update Schedule

Edit `conda-dependency-update.yml`:

```yaml
on:
  schedule:
    - cron: '0 9 * * 1'  # Monday at 9:00 UTC
```

Change to your preferred schedule using [cron syntax](https://crontab.guru/).

### Adding More Platforms

To test on additional platforms, edit the matrix in `ci.yml`:

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, macos-26, windows-latest]
    # Add more platforms here
```

### Modifying Test Steps

All workflows follow the same test pattern. To add or modify tests:

1. Edit the relevant workflow file
2. Add steps after the environment setup
3. Use `shell: bash -el {0}` for conda environment access
4. Ensure tests are cross-platform compatible

## Monitoring

### Check Workflow Status

1. Go to the "Actions" tab in the repository
2. Select a workflow from the left sidebar
3. View recent runs and their status

### Email Notifications

GitHub sends notifications for workflow failures if:
- You have email notifications enabled
- The workflow is triggered by your actions
- The workflow fails

### Dependency Update PRs

Automated PRs from the dependency update workflow:
- Title: "chore: Update conda dependencies"
- Labels: "dependencies", "automated"
- Assignee: Repository owner
- Description includes what was tested

## Debugging Workflows

### View Logs

1. Go to Actions → Select workflow → Select run
2. Click on the job name
3. Expand steps to see detailed logs

### Re-run Failed Workflows

1. Go to the failed workflow run
2. Click "Re-run all jobs" or "Re-run failed jobs"

### Test Locally

Most workflow steps can be tested locally:

```bash
# Install dependencies
make install

# Run lint
flake8 . --count --statistics

# Test conversion
python scripts/convert_to_notebooks.py

# Test execution
for notebook in lecture_*/*.ipynb; do
  jupyter nbconvert --to notebook --execute --inplace "$notebook"
done
```

## Best Practices

1. **Always test locally** before pushing
2. **Keep workflows simple** and focused
3. **Use caching** to speed up builds (already enabled for micromamba)
4. **Minimize workflow runs** to save GitHub Actions minutes
5. **Review automated PRs** promptly

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Micromamba Setup Action](https://github.com/mamba-org/setup-micromamba)
- [Conda Lock](https://github.com/conda/conda-lock)
- [Create Pull Request Action](https://github.com/peter-evans/create-pull-request)
