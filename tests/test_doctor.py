"""Tests for doctor checks (no network, no key reveal)."""

import os

from typer.testing import CliRunner

from cmk.cli import app
from cmk.doctor import check_openai_key, check_python, run_doctor
from cmk.openai_client import has_api_key

runner = CliRunner()


def test_python_check_ok():
    r = check_python()
    assert r.name == "python"
    assert r.ok is True


def test_has_api_key_false_when_unset(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert has_api_key() is False
    r = check_openai_key()
    assert r.ok is False
    assert "not set" in r.detail.lower()


def test_has_api_key_true_does_not_leak(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-secret-should-not-appear")
    assert has_api_key() is True
    r = check_openai_key()
    assert r.ok is True
    assert "sk-test" not in r.detail
    assert "secret" not in r.detail


def test_run_doctor_returns_three_checks():
    results = run_doctor()
    names = {r.name for r in results}
    assert "python" in names
    assert "git" in names
    assert "OPENAI_API_KEY" in names


def test_cli_doctor(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = runner.invoke(app, ["doctor"])
    # exit 1 when key missing is OK; still must print checks
    assert "OPENAI_API_KEY" in result.stdout
    assert "sk-" not in result.stdout
    assert "not affiliated" in result.stdout.lower()
