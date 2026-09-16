"""Collect commit messages between refs or from an exported file."""

from __future__ import annotations

import subprocess
from pathlib import Path


class GitError(RuntimeError):
    """Raised when git is unavailable or the working tree is not a repo."""


def is_git_repo(cwd: Path | None = None) -> bool:
    """Return True if cwd (or process cwd) is inside a git work tree."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise GitError("git executable not found on PATH") from exc
    return result.returncode == 0 and result.stdout.strip() == "true"


def git_log_between(
    from_ref: str,
    to_ref: str,
    *,
    cwd: Path | None = None,
) -> str:
    """Return `git log` output between two refs (exclusive..inclusive style).

    Uses ``from_ref..to_ref`` which is the usual release-notes range.
    """
    if not is_git_repo(cwd):
        raise GitError(
            "not a git repository; pass --commits-file with a pre-exported log"
        )
    result = subprocess.run(
        [
            "git",
            "log",
            f"{from_ref}..{to_ref}",
            "--pretty=format:%h %s%n%b---",
            "--no-merges",
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        err = (result.stderr or result.stdout or "unknown git error").strip()
        raise GitError(f"git log failed: {err}")
    return result.stdout.strip()


def load_commits_file(path: Path) -> str:
    """Load a pre-exported commit log from disk."""
    if not path.is_file():
        raise FileNotFoundError(f"commits file not found: {path}")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"commits file is empty: {path}")
    return text


def collect_commits(
    *,
    from_ref: str | None,
    to_ref: str | None,
    commits_file: Path | None,
    cwd: Path | None = None,
) -> str:
    """Resolve commit text from either git range or --commits-file."""
    if commits_file is not None:
        return load_commits_file(commits_file)
    if not from_ref or not to_ref:
        raise ValueError("provide --from/--to or --commits-file")
    return git_log_between(from_ref, to_ref, cwd=cwd)
