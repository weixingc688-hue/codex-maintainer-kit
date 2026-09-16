# codex-maintainer-kit (`cmk`)

面向使用 **OpenAI Codex / ChatGPT Codex / OpenAI API** 的开源维护者的实用 MIT 工具包。

> **声明：本项目为社区开源工具，与 OpenAI 无隶属、无背书、无赞助关系（Not affiliated with OpenAI）。**

帮助维护者把「发版说明」和「PR 审查」做得更干净：从 `git log` 生成 Keep-a-Changelog 风格提示词（可选调用 API 起草），输出适配 Codex 辅助审查的清单，并用 `doctor` 检查本地环境。

---

## English (short)

**codex-maintainer-kit** is an unofficial MIT CLI for OSS maintainers who use Codex / the OpenAI API. It drafts Keep-a-Changelog prompts from git history, emits PR review checklists, and runs env checks — secrets only via `OPENAI_API_KEY`. Not affiliated with OpenAI.

```bash
pip install -e ".[dev]"
cmk doctor
cmk release-notes --from v0.1.0 --to HEAD --dry-run
cmk pr-checklist --lang en
```

---

## 功能

| 命令 | 作用 |
|------|------|
| `cmk release-notes` | 根据 refs 之间的 `git log`（或 `--commits-file`）生成发布说明提示词；默认可 `--dry-run`；去掉 dry-run 且配置了 `OPENAI_API_KEY` 时调用 OpenAI 起草 |
| `cmk pr-checklist` | 输出维护者 PR 审查清单（`zh` / `en`），覆盖安全、测试、文档、破坏性变更与 AI 生成代码卫生 |
| `cmk doctor` | 检查 Python / git / `OPENAI_API_KEY` 是否存在（**不打印密钥内容**） |

## 安装

```bash
cd /path/to/codex-maintainer-kit
pip install -e ".[dev]"
pytest
```

需要 Python 3.10+。密钥仅通过环境变量提供：

```bash
export OPENAI_API_KEY=sk-...   # 可选；dry-run 不需要
```

## 快速演示（dry-run，无网络）

```bash
# 在 git 仓库内
cmk release-notes --from HEAD~5 --to HEAD --dry-run

# 或不在 git 仓库时，使用预先导出的提交日志
printf 'abc0001 Add doctor command\n---\n' > /tmp/commits.txt
cmk release-notes --commits-file /tmp/commits.txt --dry-run --out /tmp/rn-prompt.md

cmk pr-checklist --lang zh --out /tmp/pr-checklist.zh.md
cmk doctor
```

## 文档与提示词

- [docs/codex-workflow.md](docs/codex-workflow.md) — 维护者 + Codex 协作流程
- [prompts/](prompts/) — `release-notes.md` / `pr-review.md` / `issue-triage.md`
- [AGENTS.md](AGENTS.md) — 给 Codex / 编码代理的仓库维护说明
- [CONTRIBUTING.md](CONTRIBUTING.md)

## 设计原则

- **建设性**：服务真实维护者的发版与审查卫生，而非演示玩具
- **可离线迭代**：`--dry-run` 只打印提示词，方便先改 prompt 再花 API 额度
- **密钥安全**：只读环境变量；`doctor` 与日志不回显密钥
- **诚实**：明确标注非官方、与 OpenAI 无关

## 许可证

[MIT](LICENSE)
