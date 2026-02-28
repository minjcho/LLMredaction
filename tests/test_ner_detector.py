"""Tests for app.detectors.ner_detector (stub)."""

from app.detectors.ner_detector import detect


def test_returns_empty_list():
    assert detect("홍길동은 서울에 살고 있습니다.") == []


def test_returns_empty_for_empty_string():
    assert detect("") == []


def test_returns_list_type():
    result = detect("some text")
    assert isinstance(result, list)
