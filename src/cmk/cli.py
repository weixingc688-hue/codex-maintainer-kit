"""Typer CLI entrypoint for `cmk`."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from cmk import __version__
from cmk.checklist import render_checklist
from cmk.doctor import run_doctor
from cmk.git_log import GitError, collect_commits
from cmk.openai_client import draft_with_openai
from cmk.release_notes import build_release_notes_prompt

app = typer.Typer(
    name="cmk",
    help=(
        "codex-maintainer-kit — practical helpers for OSS maintainers "
        "using Codex / OpenAI API. Not affiliated with OpenAI."
    ),
    no_args_is_help=True,
    add_completion=False,
)
console = Console()
err_console = Console(stderr=True)


def _write_out(text: str, out: Optional[Path]) -> None:
    if out is None:
        console.print(text, markup=False)
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
    console.print(f"[green]Wrote[/green] {out}")


@app.callback()
def main() -> None:
    """codex-maintainer-kit CLI."""


@app.command("version")
def version_cmd() -> None:
    """Print package version."""
    console.print(__version__)


@app.command("doctor")
def doctor_cmd() -> None:
    """Print environment checks (git, Python, OPENAI_API_KEY presence)."""
    results = run_doctor()
    all_ok = True
    lines = ["codex-maintainer-kit doctor", f"version: {__version__}", ""]
    for r in results:
        mark = "OK" if r.ok else "MISS"
        if not r.ok:
            all_ok = False
        lines.append(f"[{mark}] {r.name}: {r.detail}")
    lines.append("")
    lines.append(
        "Note: this toolkit is unofficial and not affiliated with OpenAI."
    )
    console.print("\n".join(lines))
    raise typer.Exit(code=0 if all_ok else 1)


@app.command("pr-checklist")
def pr_checklist_cmd(
    lang: str = typer.Option(
        "en",
        "--lang",
        "-l",
        help="Checklist language: zh or en",
    ),
    out: Optional[Path] = typer.Option(
        None,
        "--out",
        "-o",
        help="Write Markdown to this file instead of stdout",
    ),
) -> None:
    """Emit a maintainer PR review checklist for Codex-assisted reviews."""
    try:
        text = render_checklist(lang)
    except ValueError as exc:
        err_console.print(f"[red]error:[/red] {exc}")
        raise typer.Exit(code=2) from exc
    _write_out(text, out)


@app.command("release-notes")
def release_notes_cmd(
    from_ref: Optional[str] = typer.Option(
        None,
        "--from",
        help="Git ref for range start (exclusive), e.g. v0.1.0",
    ),
    to_ref: Optional[str] = typer.Option(
        None,
        "--to",
        help="Git ref for range end (inclusive), e.g. HEAD",
    ),
    commits_file: Optional[Path] = typer.Option(
        None,
        "--commits-file",
        help="Pre-exported git log file (use when not inside a git repo)",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Print the prompt only; do not call OpenAI",
    ),
    out: Optional[Path] = typer.Option(
        None,
        "--out",
        "-o",
        help="Write result to this file instead of stdout",
    ),
    model: Optional[str] = typer.Option(
        None,
        "--model",
        help="OpenAI model override (default: CMK_OPENAI_MODEL or gpt-4o-mini)",
    ),
) -> None:
    """Draft Keep-a-Changelog notes from git log (or --commits-file).

    With --dry-run, prints the prompt only (no network).
    Without --dry-run, requires OPENAI_API_KEY and calls the OpenAI API.
    """
    try:
        commits = collect_commits(
            from_ref=from_ref,
            to_ref=to_ref,
            commits_file=commits_file,
        )
    except (GitError, FileNotFoundError, ValueError) as exc:
        err_console.print(f"[red]error:[/red] {exc}")
        raise typer.Exit(code=2) from exc

    prompt = build_release_notes_prompt(
        commits,
        from_ref=from_ref or "(commits-file)",
        to_ref=to_ref or "(commits-file)",
    )

    if dry_run:
        _write_out(prompt, out)
        return

    try:
        draft = draft_with_openai(prompt, model=model)
    except RuntimeError as exc:
        err_console.print(f"[red]error:[/red] {exc}")
        raise typer.Exit(code=2) from exc
    except Exception as exc:  # noqa: BLE001 — surface API errors cleanly
        err_console.print(f"[red]OpenAI API error:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    _write_out(draft, out)


@app.command("about")
def about_cmd() -> None:
    """Short product blurb."""
    console.print(
        Panel.fit(
            "[bold]codex-maintainer-kit[/bold] v"
            + __version__
            + "\nPractical release + PR hygiene for maintainers.\n"
            "[dim]Unofficial · MIT · Not affiliated with OpenAI[/dim]",
            title="cmk",
        )
    )


if __name__ == "__main__":
    app()
