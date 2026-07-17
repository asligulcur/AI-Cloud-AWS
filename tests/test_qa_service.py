import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src" / "app"))

from qa_service import answer_question  # noqa: E402


def test_empty_question_raises():
    with pytest.raises(ValueError):
        answer_question("")


def test_whitespace_only_question_raises():
    with pytest.raises(ValueError):
        answer_question("   ")


def test_stub_mode_returns_stub_answer():
    os.environ["STUB_MODE"] = "1"
    try:
        result = answer_question("What is AWS?")
        assert result["source"] == "stub"
        assert result["answer"]
    finally:
        del os.environ["STUB_MODE"]


def test_falls_back_to_stub_without_bedrock_access(monkeypatch):
    monkeypatch.delenv("STUB_MODE", raising=False)
    result = answer_question("What is AWS?")
    assert result["source"] in ("stub", "bedrock")
    assert result["answer"]
