"""Environment health checks for maintainers (never prints secret values)."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass

from cmk.openai_client import has_api_key


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    detail: str


def check_git() -> CheckResult:
    path = shutil.which("git")
    if not path:
        return CheckResult("git", False, "not found on PATH")
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        return CheckResult("git", False, f"failed to run: {exc}")
    version = (result.stdout or result.stderr or "").strip()
    return CheckResult("git", result.returncode == 0, version or path)


def check_openai_key() -> CheckResult:
    if has_api_key():
        return CheckResult(
            "OPENAI_API_KEY",
            True,
            "set (value not shown)",
        )
    return CheckResult(
        "OPENAI_API_KEY",
        False,
        "not set — export OPENAI_API_KEY or use --dry-run",
    )


def check_python() -> CheckResult:
    import sys

    ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    ok = sys.version_info >= (3, 10)
    return CheckResult("python", ok, f"{ver} (need >= 3.10)")


def run_doctor() -> list[CheckResult]:
    return [check_python(), check_git(), check_openai_key()]
