"""CIELingo web digest utilities.

This module keeps the web-facing part small and deterministic:
- fetch content through the stdlib-based web_fetcher
- extract a compact digest from the fetched text
- prepare a structured payload that can be stored in PhaseMemory
"""
from __future__ import annotations

import hashlib
import re
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Iterable
from urllib.parse import urlparse

from ciel_geometry.weighting import canonical_weighting_from_phase_metadata

from .web_fetcher import FetchResult, fetch, fetch_news

DEFAULT_FETCH_TIMEOUT = 15
DEFAULT_SUMMARY_SENTENCES = 3
DEFAULT_NEWS_ARTICLES = 5
DEFAULT_SUMMARY_CHARS = 1200
DEFAULT_EXCERPT_CHARS = 500
MAX_TEXT_CHARS = 100000
SUMMARY_SCORE_MIN = 0.35
SUMMARY_SCORE_MED = 0.65

_WORD_RE = re.compile(r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9]{3,}")
_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
_STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "are", "was", "were", "been",
    "have", "has", "had", "not", "you", "your", "they", "them", "their", "there",
    "then", "when", "where", "what", "why", "how", "who", "which", "will", "would",
    "could", "should", "can", "may", "might", "into", "onto", "over", "under", "about",
    "after", "before", "because", "while", "during", "between", "through", "using",
    "without", "with", "the", "a", "an", "of", "in", "on", "to", "is", "it", "as",
    "i", "we", "he", "she", "they", "me", "us", "my", "our", "your", "their",
    "i", "w", "na", "z", "do", "od", "po", "dla", "oraz", "jest", "nie", "to", "się",
    "jak", "co", "czy", "ale", "gdy", "gdyz", "gdyż", "gdzie", "kiedy", "tam", "tu",
}


@dataclass(frozen=True)
class WebDigest:
    url: str
    title: str
    source: str
    fetched_at: float
    status: int
    content_type: str
    content_digest: str
    word_count: int
    sentence_count: int
    summary: str
    excerpt: str
    keywords: tuple[str, ...] = field(default_factory=tuple)
    quality_score: float = 0.5
    phase_profile: dict[str, float] = field(default_factory=dict)
    error: str = ""
    article_count: int = 0
    articles: tuple[dict[str, str], ...] = field(default_factory=tuple)

    def as_dict(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "title": self.title,
            "source": self.source,
            "fetched_at": self.fetched_at,
            "status": self.status,
            "content_type": self.content_type,
            "content_digest": self.content_digest,
            "word_count": self.word_count,
            "sentence_count": self.sentence_count,
            "summary": self.summary,
            "excerpt": self.excerpt,
            "keywords": list(self.keywords),
            "quality_score": self.quality_score,
            "phase_profile": dict(self.phase_profile),
            "error": self.error,
            "article_count": self.article_count,
            "articles": [dict(article) for article in self.articles],
        }


def _tokenize(text: str) -> list[str]:
    return [token.lower() for token in _WORD_RE.findall(text)]


def _split_sentences(text: str) -> list[str]:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return []
    parts = [part.strip() for part in _SENTENCE_RE.split(cleaned) if part.strip()]
    return parts or [cleaned]


def _effective_text(result: FetchResult) -> str:
    if result.articles:
        article_texts = []
        for article in result.articles:
            title = article.get("title", "").strip()
            summary = article.get("summary", "").strip()
            joined = ". ".join(part for part in (title, summary) if part)
            if joined:
                article_texts.append(joined)
        if article_texts:
            feed_text = "\n".join(article_texts)
            if result.text:
                return f"{feed_text}\n{result.text}"
            return feed_text
    return result.text


def summarize_text(text: str, *, max_sentences: int = DEFAULT_SUMMARY_SENTENCES, max_chars: int = DEFAULT_SUMMARY_CHARS) -> str:
    sentences = _split_sentences(text)
    if not sentences:
        return ""

    joined = " ".join(sentences)
    tokens = [token for token in _tokenize(joined) if token not in _STOPWORDS]
    if not tokens:
        return " ".join(sentences[:max_sentences])[:max_chars].strip()

    freq = Counter(tokens)
    scores: list[tuple[float, int, str]] = []
    for idx, sentence in enumerate(sentences):
        sentence_tokens = [token for token in _tokenize(sentence) if token not in _STOPWORDS]
        if not sentence_tokens:
            continue
        score = sum(freq[token] for token in sentence_tokens)
        score += min(len(sentence_tokens), 24) * 0.2
        scores.append((score, idx, sentence))

    if not scores:
        return " ".join(sentences[:max_sentences])[:max_chars].strip()

    chosen = [sentence for _, _, sentence in sorted(scores, key=lambda item: (-item[0], item[1]))[:max_sentences]]
    chosen.sort(key=lambda sentence: sentences.index(sentence))
    summary = " ".join(chosen).strip()
    return summary[:max_chars].strip()


def extract_keywords(text: str, *, limit: int = 8) -> tuple[str, ...]:
    tokens = [token for token in _tokenize(text) if token not in _STOPWORDS]
    if not tokens:
        return ()
    freq = Counter(tokens)
    ranked = [token for token, _count in freq.most_common(limit * 2)]
    seen: list[str] = []
    for token in ranked:
        if token not in seen:
            seen.append(token)
        if len(seen) >= limit:
            break
    return tuple(seen)


def _title_from_url(url: str) -> str:
    parsed = urlparse(url)
    tail = parsed.path.strip("/").split("/")[-1] if parsed.path else ""
    if tail:
        tail = re.sub(r"[-_]+", " ", tail).strip()
    return tail.title() if tail else parsed.netloc or url


def build_phase_profile(
    *,
    text: str,
    summary: str,
    keywords: Iterable[str],
    status: int,
    article_count: int,
) -> dict[str, float]:
    token_count = len(_tokenize(text))
    summary_count = len(_tokenize(summary))
    semantic_mass = max(0.0, min(1.0, token_count / 160.0))
    projection_confidence = max(0.0, min(1.0, 0.25 + 0.75 * min(1.0, summary_count / 48.0)))
    phase_nav_similarity = 1.0 if status == 200 else 0.35
    affective_similarity = max(0.0, min(1.0, 0.35 + 0.05 * len(list(keywords))))
    euler_alignment = max(0.0, min(1.0, 0.45 + 0.08 * min(article_count, 4)))
    novelty = max(0.0, min(1.0, 0.25 + 0.06 * len(list(keywords))))
    contradiction_risk = 0.1 if summary else 0.55
    profile = canonical_weighting_from_phase_metadata(
        {
            "semantic_mass": semantic_mass,
            "projection_confidence": projection_confidence,
            "phase_nav_similarity": phase_nav_similarity,
            "affective_similarity": affective_similarity,
            "euler_alignment": euler_alignment,
            "novelty": novelty,
            "contradiction_risk": contradiction_risk,
        },
        semantic={
            "labels": list(keywords),
            "tokens": _tokenize(text),
            "relations": [],
        },
    )
    return {key: float(value) for key, value in profile.items()}


def digest_fetch_result(result: FetchResult, *, max_sentences: int = DEFAULT_SUMMARY_SENTENCES) -> WebDigest:
    source_text = _effective_text(result)
    summary = summarize_text(source_text, max_sentences=max_sentences)
    if not summary:
        summary = result.text[:DEFAULT_SUMMARY_CHARS].strip()
    excerpt = source_text[:DEFAULT_EXCERPT_CHARS].strip()
    keywords = extract_keywords(source_text)
    content_digest = hashlib.sha256(source_text.encode("utf-8")).hexdigest()
    title = result.articles[0]["title"] if result.articles else _title_from_url(result.url)
    source = result.articles[0].get("source", "web") if result.articles else result.content_type or "web"
    phase_profile = build_phase_profile(
        text=source_text,
        summary=summary,
        keywords=keywords,
        status=result.status,
        article_count=len(result.articles),
    )
    return WebDigest(
        url=result.url,
        title=title,
        source=source,
        fetched_at=time.time(),
        status=result.status,
        content_type=result.content_type,
        content_digest=content_digest,
        word_count=len(_tokenize(source_text)),
        sentence_count=len(_split_sentences(source_text)),
        summary=summary,
        excerpt=excerpt,
        keywords=keywords,
        quality_score=phase_profile["composite"],
        phase_profile=phase_profile,
        error=result.error,
        article_count=len(result.articles),
        articles=tuple(dict(article) for article in result.articles),
    )


def digest_url(url: str, *, timeout: int = DEFAULT_FETCH_TIMEOUT, max_sentences: int = DEFAULT_SUMMARY_SENTENCES, cache: bool = True) -> WebDigest:
    return digest_fetch_result(fetch(url, timeout=timeout, cache=cache), max_sentences=max_sentences)


def digest_news(*, sources: list[str] | None = None, max_articles: int = DEFAULT_NEWS_ARTICLES, max_sentences: int = 2) -> list[WebDigest]:
    digests: list[WebDigest] = []
    for article in fetch_news(sources=sources, max_articles=max_articles):
        title = article.get("title", "").strip() or article.get("url", "")
        text = ". ".join(part for part in (title, article.get("summary", "").strip()) if part)
        source_digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        summary = summarize_text(text, max_sentences=max_sentences) or text[:DEFAULT_SUMMARY_CHARS]
        keywords = extract_keywords(text)
        phase_profile = build_phase_profile(
            text=text,
            summary=summary,
            keywords=keywords,
            status=200,
            article_count=1,
        )
        digests.append(
            WebDigest(
                url=article.get("url", ""),
                title=title or _title_from_url(article.get("url", "")),
                source=article.get("source", "rss"),
                fetched_at=time.time(),
                status=200,
                content_type="rss/article",
                content_digest=source_digest,
                word_count=len(_tokenize(text)),
                sentence_count=len(_split_sentences(text)),
                summary=summary,
                excerpt=text[:DEFAULT_EXCERPT_CHARS],
                keywords=keywords,
                quality_score=phase_profile["composite"],
                phase_profile=phase_profile,
                article_count=1,
                articles=(dict(article),),
            )
        )
    return digests


def digest_many(urls: Iterable[str], *, timeout: int = 15, max_sentences: int = 3, cache: bool = True) -> list[WebDigest]:
    return [digest_url(url, timeout=timeout, max_sentences=max_sentences, cache=cache) for url in urls]


__all__ = [
    "WebDigest",
    "digest_fetch_result",
    "digest_many",
    "digest_news",
    "digest_url",
    "extract_keywords",
    "summarize_text",
]
