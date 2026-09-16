"""Build Keep-a-Changelog style release-notes prompts from commit logs."""

from __future__ import annotations

from pathlib import Path

PROMPT_TEMPLATE = """# Task: Draft Keep-a-Changelog release notes

You are helping an open-source maintainer prepare release notes.

## Constraints
- Output Markdown only.
- Follow Keep a Changelog sections: Added, Changed, Deprecated, Removed, Fixed, Security.
- Omit empty sections.
- Base every bullet on the commit list below; do not invent features.
- Prefer user-facing language over internal commit noise.
- Group related commits; drop pure chore/style noise unless it affects users.
- If a commit is ambiguous, put it under Changed with a cautious wording.

## Version / range
- From: {from_ref}
- To: {to_ref}

## Commits
```
{commits}
```

## Output format
```markdown
## [Unreleased]

### Added
- ...

### Changed
- ...

### Fixed
- ...
```
(Adjust the version heading if the maintainer named a tag in `to`.)
"""


def build_release_notes_prompt(
    commits: str,
    *,
    from_ref: str = "(file)",
    to_ref: str = "(file)",
    template_path: Path | None = None,
) -> str:
    """Render the release-notes prompt string."""
    if template_path is not None:
        template = template_path.read_text(encoding="utf-8")
    else:
        template = PROMPT_TEMPLATE
    return template.format(
        from_ref=from_ref,
        to_ref=to_ref,
        commits=commits.strip() or "(no commits in range)",
    )
