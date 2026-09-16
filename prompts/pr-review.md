# Prompt: Codex-assisted PR review

Paste the PR diff (or summary) after this block. Prefer `cmk pr-checklist` for the checklist itself.

```
You are reviewing a pull request for an MIT-licensed open-source project.
Use the maintainer checklist below. Be specific: cite files/hunks.
Do not approve blindly; flag security, missing tests, and breaking changes.
Distinguish "must fix" vs "nice to have".

## Checklist focus
1. Scope matches description
2. Tests cover new behavior
3. No secrets in the diff
4. Docs/CHANGELOG updated if user-facing
5. AI-generated code reviewed for hallucinated APIs

## PR materials
(paste title, description, and diff or `gh pr diff` output here)
```

Generate a local checklist file:

```bash
cmk pr-checklist --lang en --out /tmp/pr-checklist.md
cmk pr-checklist --lang zh --out /tmp/pr-checklist.zh.md
```
