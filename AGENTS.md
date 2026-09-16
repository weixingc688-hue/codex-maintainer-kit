# AGENTS.md — for Codex / coding agents maintaining this repo

This file teaches automated coding agents (including OpenAI Codex) how to work
in **codex-maintainer-kit**. Humans should also skim it before large changes.

**Not affiliated with OpenAI.** Treat model output as untrusted until reviewed.

## Product intent

`cmk` helps open-source maintainers with:

1. Release-note prompt/draft generation from git history
2. PR review checklists tuned for Codex-assisted reviews
3. Environment doctor checks (git + API key presence)

Do **not** turn this into an unrelated domain tool (e.g. education/geography demos).
Keep the focus on maintainer hygiene: release, review, docs, CI.

## Layout

```
src/cmk/          # library + Typer CLI
tests/            # pytest; dry-run paths must not hit the network
docs/             # human workflows
prompts/          # reusable Codex prompts
.github/workflows # CI
```

## Commands agents should run

```bash
pip install -e ".[dev]"
pytest
cmk doctor
cmk release-notes --commits-file tests/fixtures/sample_commits.txt --dry-run
cmk pr-checklist --lang en
```

If fixtures are missing, create a temporary commits file instead of inventing git history.

## Coding rules

- Python 3.10+; public CLI via Typer entry point `cmk`
- Never hard-code API keys; read `OPENAI_API_KEY` from the environment only
- Doctor and logs must never echo secret values
- Network calls only when the user opts out of `--dry-run`
- Keep dependencies minimal: `typer`, `openai`, `rich` (+ pytest for dev)
- Prefer small, tested functions over large rewrites
- Update README / CHANGELOG-facing docs when CLI flags change
- MIT license; do not paste incompatible licensed code

## How maintainers should use Codex with this CLI

1. Ask Codex to implement a change; require tests for dry-run paths
2. Run `cmk pr-checklist` (or open `prompts/pr-review.md`) while reviewing the PR
3. Before a tag, run `cmk release-notes --from <tag> --to HEAD --dry-run` and paste into Codex if needed
4. Only call the live API when the prompt looks correct

## Out of scope

- Acting as an official OpenAI product or SDK wrapper beyond thin Chat Completions usage
- Storing user credentials on disk
- Scraping private repos or bypassing access controls
