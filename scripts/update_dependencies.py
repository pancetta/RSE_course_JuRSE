#!/usr/bin/env python3
"""
Conda dependency update and testing script.

This script helps maintain conda environments by:
1. Testing updated dependencies
2. Creating lock files for reproducibility
3. Identifying incompatible package versions
4. Generating pinning recommendations when tests fail

Usage:
    python update_dependencies.py [--test-only] [--create-locks]
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
import tempfile
import shutil


def run_command(cmd, shell=False, check=True, capture_output=False):
    """Run a shell command and return the result."""
    print(f"Running: {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
    result = subprocess.run(cmd, shell=shell, check=check, capture_output=capture_output, text=True)
    return result


def test_environment(env_file, name="test-env"):
    """
    Test an environment by creating it and running the CI test suite.

    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    print(f"\n{'='*60}")
    print(f"Testing environment from: {env_file}")
    print(f"{'='*60}\n")

    try:
        # Create test environment
        print("Creating test environment...")
        run_command(["micromamba", "create", "-n", name, "-f", env_file, "-y"])

        # Run formatting check
        print("\n=== Running black formatting check ===")
        run_command(f"micromamba run -n {name} black --check .", shell=True)

        # Run ruff linting
        print("\n=== Running ruff linting ===")
        run_command(f"micromamba run -n {name} ruff check .", shell=True)

        # Check Python syntax
        print("\n=== Checking Python syntax ===")
        run_command(f"micromamba run -n {name} python -m py_compile scripts/convert_to_notebooks.py", shell=True)

        lecture_files = Path(".").glob("lecture_*/lecture_*.py")
        for lecture_file in lecture_files:
            print(f"Checking syntax: {lecture_file}")
            run_command(f"micromamba run -n {name} python -m py_compile {lecture_file}", shell=True)

        # Convert lectures
        print("\n=== Converting lectures to notebooks ===")
        run_command(f"micromamba run -n {name} python scripts/convert_to_notebooks.py", shell=True)

        # Execute notebooks
        print("\n=== Executing notebooks ===")
        lecture_files = Path(".").glob("lecture_*/lecture_*.py")
        for lecture_file in lecture_files:
            notebook_file = lecture_file.with_suffix(".ipynb")
            print(f"Executing: {notebook_file}")
            run_command(
                f"micromamba run -n {name} jupyter nbconvert --to notebook --execute --inplace {notebook_file}", shell=True
            )

        print("\n✅ All tests passed!")
        return True, None

    except subprocess.CalledProcessError as e:
        error_msg = f"Test failed: {e}"
        print(f"\n❌ {error_msg}")
        return False, error_msg

    finally:
        # Clean up test environment
        print(f"\nCleaning up test environment '{name}'...")
        try:
            run_command(["micromamba", "env", "remove", "-n", name, "-y"], check=False)
        except Exception:
            pass

        # Clean up generated notebooks
        print("Cleaning up generated notebooks...")
        for notebook in Path(".").glob("lecture_*/*.ipynb"):
            notebook.unlink()


def _create_lock_for_env(env_file, lock_file, platform):
    """Helper function to create a single lock file."""
    try:
        run_command(["conda-lock", "lock", "--file", env_file, "--platform", platform, "--lockfile", lock_file])
        print(f"  ✅ Created {lock_file}")
        return True
    except subprocess.CalledProcessError:
        print(f"  ❌ Failed to create {lock_file}")
        return False


def _create_locks_for_platforms(env_file, prefix, platforms):
    """Create lock files for an environment across multiple platforms."""
    count = 0
    for platform in platforms:
        lock_file = f"{prefix}-{platform}.lock"
        if _create_lock_for_env(env_file, lock_file, platform):
            count += 1
    return count


def create_lock_files(platforms=None):
    """
    Create conda-lock files for all environments.

    Args:
        platforms: List of platforms to create locks for.
                  Defaults to ['linux-64', 'osx-64', 'osx-arm64', 'win-64']
    """
    if platforms is None:
        platforms = ["linux-64", "osx-64", "osx-arm64", "win-64"]

    print(f"\n{'='*60}")
    print("Creating conda-lock files for reproducibility")
    print(f"Platforms: {', '.join(platforms)}")
    print(f"{'='*60}\n")

    # Check if conda-lock is available
    try:
        run_command(["conda-lock", "--version"], capture_output=True)
    except FileNotFoundError:
        print("ERROR: conda-lock is not installed")
        print("Install it with: micromamba install -c conda-forge conda-lock")
        return False

    lock_count = 0

    # Create lock for unified environment
    print("Creating lock files for environment...")
    lock_count += _create_locks_for_platforms("environment.yml", "environment", platforms)

    print(f"\n✅ Created {lock_count} lock files")
    return True


def main():
    parser = argparse.ArgumentParser(description="Test and update conda dependencies for RSE lectures")
    parser.add_argument("--test-only", action="store_true", help="Only test current environment, don't create lock files")
    parser.add_argument("--create-locks", action="store_true", help="Create conda-lock files for all platforms")
    parser.add_argument(
        "--platforms",
        nargs="+",
        default=["linux-64", "osx-64", "osx-arm64", "win-64"],
        help="Platforms to create lock files for",
    )

    args = parser.parse_args()

    # Change to repository root (parent of scripts directory)
    repo_root = Path(__file__).parent.parent
    os.chdir(repo_root)

    print("=" * 60)
    print("Conda Dependency Update and Testing")
    print("=" * 60)

    # Test the current environment
    success, error = test_environment("environment.yml", "test-rse-env")

    if not success:
        print("\n" + "=" * 60)
        print("❌ DEPENDENCY UPDATE FAILED")
        print("=" * 60)
        print("\nThe current dependency versions have compatibility issues.")
        print("This may indicate that a recent package update broke compatibility.")
        print("\nRecommended actions:")
        print("1. Check the error message above to identify the problematic package")
        print("2. Pin the previous working version in environment.yml")
        print("3. Open an issue with the package maintainer if it's a bug")
        print("\nExample pinning:")
        print("  - matplotlib==3.8.0  # Pin to specific version")
        print("  - numpy>=1.21.0,<2.0.0  # Exclude breaking version")
        sys.exit(1)

    # If tests passed and lock files requested, create them
    if args.create_locks or not args.test_only:
        if not create_lock_files(args.platforms):
            sys.exit(1)

    print("\n" + "=" * 60)
    print("✅ SUCCESS")
    print("=" * 60)
    print("\nAll tests passed with current dependencies!")
    if args.create_locks or not args.test_only:
        print("Lock files have been created for reproducibility.")
        print("\nNext steps:")
        print("1. Commit the lock files to the repository")
        print("2. Update the CI workflow to use lock files")
        print("3. Document the lock file usage in README.md")


if __name__ == "__main__":
    main()
