"""Tests for release-notes dry-run path (no network)."""

from pathlib import Path

from typer.testing import CliRunner

from cmk.cli import app
from cmk.release_notes import build_release_notes_prompt

runner = CliRunner()


SAMPLE_LOG = """abc1234 Add CLI doctor command
Implements env checks for git and API key.
---
def5678 Fix empty commits handling
---
"""


def test_build_prompt_contains_commits():
    prompt = build_release_notes_prompt(
        SAMPLE_LOG, from_ref="v0.1.0", to_ref="HEAD"
    )
    assert "Keep-a-Changelog" in prompt or "Keep a Changelog" in prompt
    assert "Add CLI doctor command" in prompt
    assert "v0.1.0" in prompt
    assert "HEAD" in prompt


def test_cli_dry_run_with_commits_file(tmp_path: Path):
    commits = tmp_path / "log.txt"
    commits.write_text(SAMPLE_LOG, encoding="utf-8")
    out = tmp_path / "prompt.md"
    result = runner.invoke(
        app,
        [
            "release-notes",
            "--commits-file",
            str(commits),
            "--dry-run",
            "--out",
            str(out),
        ],
    )
    assert result.exit_code == 0, result.stdout + result.stderr
    text = out.read_text(encoding="utf-8")
    assert "Add CLI doctor command" in text
    assert "do not invent" in text.lower() or "Do not invent" in text


def test_cli_dry_run_stdout(tmp_path: Path):
    commits = tmp_path / "log.txt"
    commits.write_text(SAMPLE_LOG, encoding="utf-8")
    result = runner.invoke(
        app,
        ["release-notes", "--commits-file", str(commits), "--dry-run"],
    )
    assert result.exit_code == 0
    assert "Added" in result.stdout or "Keep" in result.stdout


def test_cli_missing_args_fails():
    result = runner.invoke(app, ["release-notes", "--dry-run"])
    assert result.exit_code != 0


def test_cli_empty_commits_file_fails(tmp_path: Path):
    empty = tmp_path / "empty.txt"
    empty.write_text("", encoding="utf-8")
    result = runner.invoke(
        app,
        ["release-notes", "--commits-file", str(empty), "--dry-run"],
    )
    assert result.exit_code != 0
