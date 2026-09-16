"""Maintainer PR review checklists tuned for Codex-assisted reviews."""

from __future__ import annotations

CHECKLIST_EN = """# PR Review Checklist (Codex-assisted)

> Use with ChatGPT Codex / OpenAI API. This project is **not affiliated with OpenAI**.
> Paste this checklist into your review notes or feed it to Codex with the PR diff.

## Scope & intent
- [ ] PR description states problem, approach, and user-visible impact
- [ ] Linked issue / discussion exists (or rationale for no issue)
- [ ] Diff stays within stated scope (no drive-by refactors)

## Correctness
- [ ] Happy path and edge cases covered in description or tests
- [ ] Error handling is explicit; no silent swallows
- [ ] Public APIs / CLIs remain backward compatible, or breaking changes are called out

## Tests
- [ ] New/changed behavior has automated tests
- [ ] Tests fail without the change (not tautologies)
- [ ] CI is green on this branch

## Security & secrets
- [ ] No secrets, tokens, or private keys in the diff
- [ ] User input / file paths / shell args are validated or escaped
- [ ] Dependency bumps reviewed for known advisories
- [ ] Network / filesystem side effects are intentional and documented

## Docs & UX
- [ ] README / CHANGELOG / help text updated when behavior changes
- [ ] Examples still run
- [ ] Breaking changes noted for release notes

## Codex hygiene (when AI helped write the PR)
- [ ] AI-generated code was reviewed line-by-line by a human
- [ ] No hallucinated APIs, imports, or config keys
- [ ] Licenses of pasted snippets are compatible (MIT-friendly)

## Maintainer decision
- [ ] Approve / request changes / ask for follow-up issue
- [ ] Labels and milestone set
"""

CHECKLIST_ZH = """# PR 审查清单（适配 Codex 辅助审查）

> 配合 ChatGPT Codex / OpenAI API 使用。本项目**与 OpenAI 无任何隶属关系**。
> 可将本清单粘贴到审查意见，或连同 PR diff 交给 Codex。

## 范围与意图
- [ ] PR 描述写清问题、方案与用户可见影响
- [ ] 已关联 issue / 讨论（或说明为何无需 issue）
- [ ] Diff 不超出声明范围（无顺手大重构）

## 正确性
- [ ] 描述或测试覆盖主路径与边界情况
- [ ] 错误处理明确，无静默吞异常
- [ ] 公共 API / CLI 保持兼容，或已标明破坏性变更

## 测试
- [ ] 新增/变更行为有自动化测试
- [ ] 去掉改动后测试会失败（非同义反复）
- [ ] 本分支 CI 通过

## 安全与密钥
- [ ] Diff 中无密钥、token、私钥
- [ ] 用户输入 / 路径 / shell 参数已校验或转义
- [ ] 依赖升级已粗查已知漏洞
- [ ] 网络 / 文件系统副作用是有意且有文档的

## 文档与体验
- [ ] 行为变更时已更新 README / CHANGELOG / 帮助文案
- [ ] 示例仍可运行
- [ ] 破坏性变更已记入发布说明草稿

## Codex 卫生（AI 参与编写时）
- [ ] 人类已逐行审过 AI 生成代码
- [ ] 无幻觉 API、import 或配置项
- [ ] 粘贴片段许可证与 MIT 兼容

## 维护者结论
- [ ] 批准 / 要求修改 / 开 follow-up issue
- [ ] 已打标签与里程碑
"""


def render_checklist(lang: str = "en") -> str:
    """Return checklist Markdown for ``zh`` or ``en``."""
    key = (lang or "en").lower()
    if key in ("zh", "zh-cn", "cn", "chinese"):
        return CHECKLIST_ZH.strip() + "\n"
    if key in ("en", "english"):
        return CHECKLIST_EN.strip() + "\n"
    raise ValueError(f"unsupported lang: {lang!r}; use 'zh' or 'en'")
