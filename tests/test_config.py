from pathlib import Path

from app import config


def test_resolve_writable_runtime_path_uses_tmp_on_vercel(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    resolved = config.resolve_writable_runtime_path("", "generated")
    assert resolved == Path("/tmp/generated")


def test_resolve_writable_runtime_path_keeps_absolute_path(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    resolved = config.resolve_writable_runtime_path("/tmp/custom-output", "generated")
    assert resolved == Path("/tmp/custom-output")
