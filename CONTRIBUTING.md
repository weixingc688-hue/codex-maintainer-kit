# Contributing

Thanks for helping improve **codex-maintainer-kit**. This project is MIT-licensed
and **not affiliated with OpenAI**.

## Setup

```bash
pip install -e ".[dev]"
pytest
cmk doctor
```

## Guidelines

1. Keep the product focused on maintainer hygiene (release notes, PR checklists, doctor).
2. Add or update pytest coverage for dry-run / offline paths — tests must not require network or a real API key.
3. Never commit secrets. Use `OPENAI_API_KEY` from the environment only.
4. Match existing code style; prefer small PRs with a clear description.
5. Update README / `docs/codex-workflow.md` / `AGENTS.md` when CLI behavior changes.
6. By contributing, you agree your changes are licensed under the MIT License.

## PR checklist

```bash
cmk pr-checklist --lang en
```

## Release notes

```bash
cmk release-notes --from <previous-tag> --to HEAD --dry-run
```
