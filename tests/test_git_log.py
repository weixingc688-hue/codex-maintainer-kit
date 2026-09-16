"""Unit tests for commit collection helpers."""

from pathlib import Path

import pytest

from cmk.git_log import collect_commits, load_commits_file


def test_load_commits_file(tmp_path: Path):
    p = tmp_path / "c.txt"
    p.write_text("aaa Fix bug\n", encoding="utf-8")
    assert "Fix bug" in load_commits_file(p)


def test_load_missing_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_commits_file(tmp_path / "nope.txt")


def test_collect_requires_args():
    with pytest.raises(ValueError):
        collect_commits(from_ref=None, to_ref=None, commits_file=None)
