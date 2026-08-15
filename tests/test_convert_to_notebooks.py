"""Smoke tests for scripts/convert_to_notebooks.py.

These run the real functions against a throwaway fake "repo" under tmp_path
(by monkeypatching the module's __file__, which convert_to_notebooks.py uses
to locate the repo root) so nothing is ever written into the real repository.
"""

import shutil

import pytest

import convert_to_notebooks
from conftest import MINIMAL_JUPYTEXT_PY

requires_jupytext_cli = pytest.mark.skipif(shutil.which("jupytext") is None, reason="jupytext CLI not on PATH")


def make_fake_repo(tmp_path, monkeypatch, n_lectures=1):
    """Point convert_to_notebooks at tmp_path and populate it with fake lectures."""
    fake_script = tmp_path / "scripts" / "convert_to_notebooks.py"
    fake_script.parent.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(convert_to_notebooks, "__file__", str(fake_script))

    for i in range(1, n_lectures + 1):
        lecture_dir = tmp_path / f"lecture_{i:02d}"
        lecture_dir.mkdir()
        (lecture_dir / f"lecture_{i:02d}.py").write_text(MINIMAL_JUPYTEXT_PY)

    return tmp_path


def test_generate_qr_codes_creates_course_and_lecture_codes(tmp_path, monkeypatch):
    pytest.importorskip("qrcode")
    make_fake_repo(tmp_path, monkeypatch, n_lectures=2)

    assert convert_to_notebooks.generate_qr_codes() is True

    assert (tmp_path / "course_qr_code.png").is_file()
    assert (tmp_path / "lecture_01" / "lecture_01_qr_code.png").is_file()
    assert (tmp_path / "lecture_02" / "lecture_02_qr_code.png").is_file()


def test_generate_qr_codes_does_not_overwrite_existing_files(tmp_path, monkeypatch):
    pytest.importorskip("qrcode")
    make_fake_repo(tmp_path, monkeypatch, n_lectures=1)
    qr_path = tmp_path / "course_qr_code.png"
    qr_path.write_bytes(b"not a real qr code")

    convert_to_notebooks.generate_qr_codes()

    assert qr_path.read_bytes() == b"not a real qr code"


def test_generate_qr_codes_missing_dependency_returns_false(monkeypatch, tmp_path, capsys):
    make_fake_repo(tmp_path, monkeypatch, n_lectures=1)
    monkeypatch.setitem(__import__("sys").modules, "qrcode", None)

    assert convert_to_notebooks.generate_qr_codes() is False
    assert "qrcode library not found" in capsys.readouterr().out


@requires_jupytext_cli
def test_convert_lecture_creates_notebook(tmp_path):
    lecture_dir = tmp_path / "lecture_01"
    lecture_dir.mkdir()
    py_file = lecture_dir / "lecture_01.py"
    py_file.write_text(MINIMAL_JUPYTEXT_PY)

    assert convert_to_notebooks.convert_lecture(py_file) is True
    assert (lecture_dir / "lecture_01.ipynb").is_file()


@requires_jupytext_cli
def test_convert_lecture_returns_false_for_missing_file(tmp_path):
    missing = tmp_path / "does_not_exist.py"
    assert convert_to_notebooks.convert_lecture(missing) is False


@requires_jupytext_cli
def test_main_converts_all_lectures_and_generates_qr_codes(tmp_path, monkeypatch, capsys):
    pytest.importorskip("qrcode")
    make_fake_repo(tmp_path, monkeypatch, n_lectures=2)

    convert_to_notebooks.main()

    for i in (1, 2):
        lecture_dir = tmp_path / f"lecture_{i:02d}"
        assert (lecture_dir / f"lecture_{i:02d}.ipynb").is_file()
    assert (tmp_path / "course_qr_code.png").is_file()

    out = capsys.readouterr().out
    assert "Successfully converted: 2" in out
    assert "Failed: 0" in out


def test_main_handles_no_lecture_directories(tmp_path, monkeypatch, capsys):
    fake_script = tmp_path / "scripts" / "convert_to_notebooks.py"
    fake_script.parent.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(convert_to_notebooks, "__file__", str(fake_script))

    convert_to_notebooks.main()

    assert "No lecture directories found" in capsys.readouterr().out
