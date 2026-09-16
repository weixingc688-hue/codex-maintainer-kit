# Codex workflow for maintainers

This guide shows how to use **codex-maintainer-kit** (`cmk`) together with
ChatGPT Codex / the OpenAI API during day-to-day maintenance.

> **Disclaimer:** This project is community-maintained and **not affiliated with,
> endorsed by, or sponsored by OpenAI**.

## Prerequisites

1. Python 3.10+
2. `git` on PATH
3. Optional: `OPENAI_API_KEY` in the environment (never commit it)

```bash
pip install -e ".[dev]"
cmk doctor
```

`cmk doctor` reports whether `git` and `OPENAI_API_KEY` are available. It never
prints the key value.

## Release notes

### Dry-run (recommended first)

Print the prompt without calling the API:

```bash
cmk release-notes --from v0.1.0 --to HEAD --dry-run
cmk release-notes --from v0.1.0 --to HEAD --dry-run --out /tmp/rn-prompt.md
```

Paste the prompt into Codex, or review/edit it before spending API credits.

### Live draft (uses OpenAI API)

```bash
export OPENAI_API_KEY=sk-...   # your secret; not stored by cmk
cmk release-notes --from v0.1.0 --to HEAD --out CHANGELOG.draft.md
```

Override model with `--model` or `CMK_OPENAI_MODEL` (default `gpt-4o-mini`).

### Outside a git clone

Export a log elsewhere, then:

```bash
git log v0.1.0..HEAD --pretty=format:'%h %s%n%b---' --no-merges > /tmp/commits.txt
cmk release-notes --commits-file /tmp/commits.txt --dry-run
```

## PR review hygiene

```bash
cmk pr-checklist --lang en --out pr-checklist.md
cmk pr-checklist --lang zh
```

Attach the checklist to your review notes, or feed it to Codex with `gh pr diff`.
See also [`prompts/pr-review.md`](../prompts/pr-review.md).

## Issue triage

Use [`prompts/issue-triage.md`](../prompts/issue-triage.md) with the issue body
in Codex. Keep human judgment on labels and closes.

## Security habits

- Secrets only via environment variables (`OPENAI_API_KEY`)
- Prefer `--dry-run` when iterating on prompts
- Never paste production keys into chat logs you cannot control
- Review all model output before merging or tagging a release

## Suggested maintainer loop

1. `cmk doctor`
2. Implement / review with Codex using `AGENTS.md` and `prompts/`
3. `cmk pr-checklist` during review
4. `cmk release-notes --dry-run` → edit → optional live API draft → tag
