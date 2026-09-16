"""Thin OpenAI API wrapper. Secrets only via environment variables."""

from __future__ import annotations

import os
from typing import Any


def has_api_key() -> bool:
    """True when OPENAI_API_KEY is set and non-empty (value never returned)."""
    key = os.environ.get("OPENAI_API_KEY", "")
    return bool(key.strip())


def default_model() -> str:
    return os.environ.get("CMK_OPENAI_MODEL", "gpt-4o-mini")


def draft_with_openai(prompt: str, *, model: str | None = None) -> str:
    """Call Chat Completions and return assistant text.

    Requires OPENAI_API_KEY in the environment. Does not log or echo the key.
    """
    if not has_api_key():
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Export it or use --dry-run to print the prompt only."
        )
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "openai package is not installed; pip install 'codex-maintainer-kit'"
        ) from exc

    client = OpenAI()  # reads OPENAI_API_KEY from env
    chosen = model or default_model()
    response: Any = client.chat.completions.create(
        model=chosen,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an experienced open-source maintainer. "
                    "Write clear, accurate Keep-a-Changelog style release notes. "
                    "Do not invent commits or features that are not in the prompt."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    choice = response.choices[0].message.content
    if not choice:
        raise RuntimeError("OpenAI API returned empty content")
    return choice.strip()
