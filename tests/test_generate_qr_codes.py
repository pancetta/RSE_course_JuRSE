"""Smoke tests for scripts/generate_qr_codes.py."""

import sys

import pytest

import generate_qr_codes


def test_generate_qr_code_creates_a_readable_png(tmp_path):
    pytest.importorskip("qrcode")
    output_path = tmp_path / "test_qr.png"

    assert generate_qr_codes.generate_qr_code("https://example.com", output_path) is True

    assert output_path.is_file()
    assert output_path.stat().st_size > 0
    with output_path.open("rb") as f:
        assert f.read(8) == b"\x89PNG\r\n\x1a\n"  # PNG file signature


def test_generate_qr_code_missing_dependency_returns_false(monkeypatch, tmp_path, capsys):
    monkeypatch.setitem(sys.modules, "qrcode", None)

    assert generate_qr_codes.generate_qr_code("https://example.com", tmp_path / "unused.png") is False
    assert "qrcode library not found" in capsys.readouterr().out


def test_main_creates_qr_codes_for_course_and_every_lecture(tmp_path, monkeypatch):
    pytest.importorskip("qrcode")
    fake_script = tmp_path / "scripts" / "generate_qr_codes.py"
    fake_script.parent.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(generate_qr_codes, "__file__", str(fake_script))

    for i in (1, 2):
        (tmp_path / f"lecture_{i:02d}").mkdir()

    generate_qr_codes.main()

    assert (tmp_path / "course_qr_code.png").is_file()
    assert (tmp_path / "lecture_01" / "lecture_01_qr_code.png").is_file()
    assert (tmp_path / "lecture_02" / "lecture_02_qr_code.png").is_file()
