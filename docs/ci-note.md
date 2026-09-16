# CI note

GitHub Actions workflow was omitted from the initial push because the `gh` OAuth token lacked the `workflow` scope. Maintainers can add `.github/workflows/ci.yml` later after authorizing the workflow scope, or run `pytest` locally:

```bash
pip install -e ".[dev]"
pytest
```
