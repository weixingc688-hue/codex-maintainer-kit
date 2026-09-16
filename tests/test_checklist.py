"""Tests for PR checklist rendering (no network)."""

from pathlib import Path

from typer.testing import CliRunner

from cmk.checklist import render_checklist
from cmk.cli import app

runner = CliRunner()


def test_checklist_en_has_security_section():
    text = render_checklist("en")
    assert "Security" in text or "secrets" in text.lower()
    assert "Codex" in text
    assert "not affiliated" in text.lower() or "Not affiliated" in text


def test_checklist_zh_has_chinese():
    text = render_checklist("zh")
    assert "审查" in text
    assert "安全" in text
    assert "OpenAI" in text


def test_checklist_invalid_lang():
    try:
        render_checklist("fr")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "unsupported" in str(exc)


def test_cli_pr_checklist_stdout():
    result = runner.invoke(app, ["pr-checklist", "--lang", "en"])
    assert result.exit_code == 0
    assert "PR Review Checklist" in result.stdout


def test_cli_pr_checklist_out_file(tmp_path: Path):
    out = tmp_path / "check.md"
    result = runner.invoke(app, ["pr-checklist", "--lang", "zh", "--out", str(out)])
    assert result.exit_code == 0
    assert out.is_file()
    assert "审查" in out.read_text(encoding="utf-8")
