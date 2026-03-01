# Quick Start Guide - Automated Dependency Management

This is a quick reference for using the automated conda dependency management system.

## TL;DR

**The system is now active and requires no immediate action.**

- ✅ Automated testing runs every Monday at 9:00 UTC
- ✅ PRs are created automatically when updates are available and pass tests
- ✅ No PR means either no updates or tests failed (check workflow logs)
- ✅ Current working versions are always maintained

## For Repository Users

### Install with Exact Versions (Once Lock Files Exist)

```bash
# Linux
micromamba create -n rse_lecture --file environment-linux-64.lock

# macOS (Intel)
micromamba create -n rse_lecture --file environment-osx-64.lock

# macOS (Apple Silicon)
micromamba create -n rse_lecture --file environment-osx-arm64.lock

# Windows
micromamba create -n rse_lecture --file environment-win-64.lock
```

### Install with Latest Compatible Versions (Current Method)

```bash
# Continue using the current method
make install
micromamba activate rse_lecture
```

## For Maintainers

### Weekly Routine (5 minutes)

1. **Check for automated PRs**
   - Go to: https://github.com/pancetta/RSE_course_JuRSE/pulls
   - Look for: "chore: Update conda dependencies"

2. **If PR exists:**
   - ✅ Review changes (see what packages were updated)
   - ✅ CI should already be passing (workflow only creates PR if tests pass)
   - ✅ Merge the PR
   - Done!

3. **If NO PR exists:**
   - Either no updates available, OR
   - Tests failed with new versions
   - Check workflow logs: Actions → Conda Dependency Update
   - If failed, see "Handling Failures" below

### Handling Failures

When tests fail with updated dependencies:

1. **Identify the problem package** from workflow logs

2. **Pin the version** in `environment.yml`:
   ```yaml
   dependencies:
     - problematic-package>=1.0.0,<2.0.0  # Exclude breaking v2.0
   ```

3. **Test locally:**
   ```bash
   make test-deps
   ```

4. **Commit and push** the pinned version

5. **Next week** the workflow will test with the pin

### Manual Testing

Test anytime without waiting for the weekly run:

```bash
# Test current dependencies
make test-deps

# Test and create lock files
make update-deps

# Just create lock files
make create-locks
```

### Manual Workflow Trigger

Don't want to wait until Monday?

1. Go to: Actions → Conda Dependency Update
2. Click "Run workflow"
3. Select branch and click "Run workflow"

## For Contributors

### Before Committing

Always test your changes:

```bash
# Test that everything still works
make test-deps
```

### Adding New Dependencies

1. **Add to `environment.yml`:**

2. **Test:**
   ```bash
   make test-deps
   ```

3. **Commit** (lock files will be updated automatically)

## Common Commands

| Task | Command |
|------|---------|
| Test dependencies | `make test-deps` |
| Create lock files | `make create-locks` |
| Update & test | `make update-deps` |
| Install from lock | `micromamba create -n rse --file environment-linux-64.lock` |
| View help | `make help` |
| Manual trigger | GitHub Actions → Conda Dependency Update → Run workflow |

## Troubleshooting

### No PR after Monday

**Possible reasons:**
- No updates available ✅ (good!)
- Tests failed ❌ (check logs)

**Action:**
Check workflow logs to see which

### Tests pass locally but fail in workflow

**Try:**
- Check you're testing same environment (use `environment.yml`)
- Check platform differences (workflow runs on Linux)

### Can't create lock files locally

**Need:**
```bash
micromamba install -c conda-forge conda-lock
```

## Documentation

| Document | Purpose |
|----------|---------|
| **SOLUTION_SUMMARY.md** | Complete overview of the solution |
| **DEPENDENCY_MANAGEMENT.md** | Detailed system guide |
| **TESTING_DEPENDENCIES.md** | Testing instructions |
| **README.md** | Updated with usage info |
| **.github/workflows/README.md** | Workflow documentation |

## System Status

Check system health:

1. **Latest workflow run:**
   - Actions → Conda Dependency Update → Latest run

2. **Recent PRs:**
   - Pull Requests → Filter by label: `dependencies`

3. **Lock file age:**
   ```bash
   ls -lh *-*.lock lecture_*/*-*.lock
   ```

## When to Check

- ✅ **Monday afternoons** - Check for automated PRs
- ✅ **After adding dependencies** - Test locally
- ✅ **Before releasing** - Ensure lock files are current

## When to Act

- ✅ **PR appears** - Review and merge
- ⚠️ **Tests fail** - Pin problematic versions
- ℹ️ **No PR** - No action needed (unless tests failed)

## Quick Decisions

**Should I merge the automated PR?**
- CI passing? → Yes, merge it
- CI failing? → Investigate first

**Should I pin a version?**
- New version breaks tests? → Yes, pin it
- New version works? → No, use automatic updates

**Should I update lock files?**
- Changed environment files? → Yes, run `make create-locks`
- Just using the repo? → No, automated system handles it

## Help

Stuck? Check:
1. This file for quick answers
2. SOLUTION_SUMMARY.md for overview
3. DEPENDENCY_MANAGEMENT.md for details
4. TESTING_DEPENDENCIES.md for testing help
5. GitHub Issues for support

---

**Remember:** The system is designed to be low-maintenance. Most weeks, you'll just merge a PR or do nothing!
