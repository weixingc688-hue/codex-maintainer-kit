# Push blocked — add weixingc688-hue to `gh` (do not remove 笑笑)

## Status
- Local repo ready at `/workspace/codex-maintainer-kit` (git init, commit `e670f1b` on `main`).
- Remote: `https://github.com/weixingc688-hue/codex-maintainer-kit.git` (has Initial commit `f6b8057`).
- Active `gh` account: **kilborntomaselli316-code** (笑笑) — pull-only on that repo; **do not log them out permanently**.
- Push needs account **weixingc688-hue** added as a second GitHub login.

## Device login (in progress on this box)
A `gh auth login --hostname github.com --git-protocol https --web` is waiting for you.

1. Open: **https://github.com/login/device**
2. Enter one-time code: **5E3A-1D3A**
3. Sign in as **weixingc688-hue** (not kilborntomaselli316-code) and authorize `gh`.
4. When the terminal shows success, tell the parent agent to continue: switch active account to weixingc688-hue, fetch/merge remote README history (`pull --allow-unrelated-histories` or fetch+merge), then `git push -u origin main`.

## If the code expired
Re-run on the box (adds a second account; does not remove 笑笑):

```bash
gh auth login --hostname github.com --git-protocol https --web
```

Then complete the new device URL/code as weixingc688-hue.

## After auth (parent/agent checklist)
```bash
gh auth status
gh auth switch --user weixingc688-hue   # if needed
cd /workspace/codex-maintainer-kit
git fetch origin
git pull origin main --allow-unrelated-histories --no-edit
# resolve any README/LICENSE conflicts if prompted, prefer keeping both project content + remote license/readme as appropriate
git push -u origin main
```

Do **not** install GitHub Apps or connect Cursor/Grok.
