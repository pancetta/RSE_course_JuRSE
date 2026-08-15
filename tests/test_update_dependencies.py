"""Smoke tests for scripts/update_dependencies.py.

update_dependencies.py mainly orchestrates micromamba/conda-lock, which are
too slow/heavy for a smoke test suite. These tests instead cover the
pure-Python control flow (argument parsing, subprocess wrapping, and the
success/failure bookkeeping around conda-lock) by monkeypatching the actual
subprocess calls.
"""

import subprocess
import sys
from pathlib import Path

import pytest

import update_dependencies as upd

SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "update_dependencies.py"


def test_cli_help_exits_cleanly():
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()


def test_run_command_captures_output():
    result = upd.run_command([sys.executable, "-c", "print('hello')"], capture_output=True)
    assert result.returncode == 0
    assert "hello" in result.stdout


def test_run_command_raises_on_failure_by_default():
    with pytest.raises(subprocess.CalledProcessError):
        upd.run_command([sys.executable, "-c", "import sys; sys.exit(1)"])


def test_run_command_check_false_does_not_raise():
    result = upd.run_command([sys.executable, "-c", "import sys; sys.exit(1)"], check=False)
    assert result.returncode == 1


def test_create_lock_files_reports_missing_conda_lock(monkeypatch, capsys):
    def fake_run_command(cmd, *args, **kwargs):
        raise FileNotFoundError("conda-lock not found")

    monkeypatch.setattr(upd, "run_command", fake_run_command)

    assert upd.create_lock_files(platforms=["linux-64"]) is False
    assert "conda-lock is not installed" in capsys.readouterr().out


def test_create_lock_for_env_success(monkeypatch):
    calls = []

    def fake_run_command(cmd, *args, **kwargs):
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(upd, "run_command", fake_run_command)

    assert upd._create_lock_for_env("environment.yml", "environment-linux-64.lock", "linux-64") is True
    assert calls[0][:2] == ["conda-lock", "lock"]


def test_create_lock_for_env_failure(monkeypatch):
    def fake_run_command(cmd, *args, **kwargs):
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(upd, "run_command", fake_run_command)

    assert upd._create_lock_for_env("environment.yml", "environment-linux-64.lock", "linux-64") is False


def test_create_locks_for_platforms_counts_successes(monkeypatch):
    outcomes = iter([True, False, True])
    monkeypatch.setattr(upd, "_create_lock_for_env", lambda *a, **k: next(outcomes))

    count = upd._create_locks_for_platforms("environment.yml", "environment", ["linux-64", "osx-64", "win-64"])

    assert count == 2
