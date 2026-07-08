from __future__ import annotations

import cielingo.__main__ as cli
from cielingo.web_fetcher import FetchResult
from cielingo.web_digest import digest_fetch_result, summarize_text


class _FakeInference:
    def __init__(self) -> None:
        self.calls: list[tuple[str, int]] = []

    def answer(self, question: str, k: int = 5):
        self.calls.append((question, k))
        return {
            "answer": "CIELingo answer",
            "operator": "MEMORY",
            "decision": {"confidence": "high"},
            "sources": [{"text": "memory source", "sim": 0.91}],
        }


def test_cmd_ask_prints_one_shot_answer(monkeypatch, capsys) -> None:
    fake = _FakeInference()
    monkeypatch.setattr(cli, "_load_inference", lambda: fake)

    cli._cmd_ask(["--k", "3", "jak działa pamięć?"])

    captured = capsys.readouterr().out
    assert "CIELingo answer" in captured
    assert "operator: MEMORY" in captured
    assert "memory source" in captured
    assert fake.calls == [("jak działa pamięć?", 3)]


def test_cmd_chat_delegates_to_run_cli(monkeypatch) -> None:
    calls: list[bool] = []

    def fake_run_cli() -> None:
        calls.append(True)

    monkeypatch.setattr("ciel_geometry.cielingo_inference.run_cli", fake_run_cli)

    cli._cmd_chat()

    assert calls == [True]


def test_main_dispatches_ask(monkeypatch, capsys) -> None:
    fake = _FakeInference()
    monkeypatch.setattr(cli, "_load_inference", lambda: fake)
    monkeypatch.setattr(cli.sys, "argv", ["cielingo", "ask", "co to jest lingo?"])

    cli.main()

    captured = capsys.readouterr().out
    assert "CIELingo answer" in captured


def test_cmd_digest_prints_digest(monkeypatch, capsys) -> None:
    class FakeInference:
        def digest_web(self, url: str, **kwargs):
            return {
                "title": "Example",
                "url": url,
                "summary": "short digest",
                "keywords": ["example", "digest"],
                "error": "",
            }

    monkeypatch.setattr(cli, "_load_inference", lambda: FakeInference())

    cli._cmd_digest(["https://example.com/article"])

    captured = capsys.readouterr().out
    assert "Example" in captured
    assert "short digest" in captured


def test_cmd_learn_stores_web_content(monkeypatch, capsys) -> None:
    calls: list[str] = []

    class FakeInference:
        def __init__(self) -> None:
            self.memory = type("M", (), {"size": 0})()

        def learn_web(self, url: str, **kwargs):
            calls.append(url)
            return {
                "digest": {"title": "Example", "url": url, "summary": "short digest", "keywords": []},
                "learned": {"index": 7},
            }

    monkeypatch.setattr(cli, "_load_inference", lambda: FakeInference())

    cli._cmd_learn(["https://example.com/article"])

    captured = capsys.readouterr().out
    assert "stored index: 7" in captured
    assert calls == ["https://example.com/article"]


def test_digest_text_summary_prefers_relevant_sentence() -> None:
    text = (
        "Noise sentence about weather. "
        "The protocol stores a digest in memory and learns from web content. "
        "Another irrelevant sentence."
    )

    summary = summarize_text(text, max_sentences=1)

    assert "digest in memory" in summary


def test_digest_fetch_result_uses_article_titles() -> None:
    result = FetchResult(
        url="https://example.com/feed",
        status=200,
        text="",
        content_type="application/rss+xml",
        elapsed=0.1,
        error="",
        articles=[{"title": "Breaking News", "url": "https://example.com/x", "summary": "Something happened", "source": "rss"}],
    )

    digest = digest_fetch_result(result)

    assert digest.title == "Breaking News"
    assert digest.summary
    assert "breaking" in " ".join(digest.keywords)
    assert 0.0 <= digest.quality_score <= 1.0
    assert "composite" in digest.phase_profile
