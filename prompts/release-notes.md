# Prompt: Release notes from git log

Copy this into Codex / ChatGPT, or use `cmk release-notes --dry-run` which embeds the same structure.

```
# Task: Draft Keep-a-Changelog release notes

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
- From: {{FROM_REF}}
- To: {{TO_REF}}

## Commits
```
{{GIT_LOG}}
```

## Output format
Use a Keep a Changelog heading and only non-empty sections.
```

Replace `{{FROM_REF}}`, `{{TO_REF}}`, and `{{GIT_LOG}}` with real values, or run:

```bash
cmk release-notes --from v0.1.0 --to HEAD --dry-run
```
