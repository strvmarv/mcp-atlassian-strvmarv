"""Tests for the pagination clamp utility."""

import pytest

from mcp_atlassian.utils.pagination import (
    DEFAULT_MAX_PAGINATION_LIMIT,
    clamp_limit,
)


def test_clamp_limit_caps_to_default(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("ATLASSIAN_MAX_PAGINATION_LIMIT", raising=False)
    assert clamp_limit(500) == DEFAULT_MAX_PAGINATION_LIMIT


def test_clamp_limit_passes_through_under_cap(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("ATLASSIAN_MAX_PAGINATION_LIMIT", raising=False)
    assert clamp_limit(50) == 50


def test_clamp_limit_respects_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("ATLASSIAN_MAX_PAGINATION_LIMIT", "25")
    assert clamp_limit(500) == 25
    assert clamp_limit(10) == 10


def test_clamp_limit_disabled_when_cap_le_zero(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("ATLASSIAN_MAX_PAGINATION_LIMIT", "0")
    assert clamp_limit(9999) == 9999


def test_clamp_limit_invalid_env_falls_back(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("ATLASSIAN_MAX_PAGINATION_LIMIT", "not-a-number")
    assert clamp_limit(500) == DEFAULT_MAX_PAGINATION_LIMIT


def test_clamp_limit_passes_through_non_positive():
    # Caller's own validation handles 0/negative; we don't fight it.
    assert clamp_limit(0) == 0
    assert clamp_limit(-5) == -5
