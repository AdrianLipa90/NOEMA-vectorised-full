#!/usr/bin/env python3

"""ciel_agent_backend — zero-model HTTP agent for memory consolidation.

Replaces llama-server/GGUF with keyword+pattern extraction.
OpenAI-compatible /v1/chat/completions on port 18520.

Usage:
  python3 ciel_agent_backend.py            # daemon (default port 18520)
  python3 ciel_agent_backend.py --port 18521
  python3 ciel_agent_backend.py --once "file content here"
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import http.server
import json
import os
import re
import signal
import sys
import threading
import time
from collections import Counter
from pathlib import Path
from typing import Any

from ciel_geometry.noema_registry import registry as nreg

PORT = int(os.environ.get("CIEL_AGENT_PORT", "18520"))

# ── Stop words (PL + EN) ──────────────────────────────────────────────
_COMMON_CAPS = {
    "the", "this", "that", "these", "those", "what", "which", "when",
    "where", "why", "how", "all", "each", "every", "both", "few",
    "more", "most", "other", "some", "such", "no", "nor", "not",
    "only", "own", "same", "so", "than", "too", "very", "just",
    "today", "yesterday", "tomorrow", "now", "then", "here", "there",
    "next", "last", "first", "second", "third", "finally", "also",
}

_STOP = {
    "the", "a", "an", "is", "was", "are", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "to", "of", "in", "for",
    "on", "with", "at", "by", "from", "as", "into", "through", "during",
    "before", "after", "above", "below", "between", "out", "off", "over",
    "under", "again", "further", "then", "once", "here", "there", "when",
    "where", "why", "how", "all", "each", "every", "both", "few", "more",
    "most", "other", "some", "such", "no", "nor", "not", "only", "own",
    "same", "so", "than", "too", "very", "just", "because", "and", "but",
    "or", "if", "while", "about", "up", "it", "its", "this", "that",
    "these", "those", "i", "me", "my", "myself", "we", "our", "ours",
    "you", "your", "yours", "he", "him", "his", "she", "her", "hers",
    "they", "them", "their", "theirs", "what", "which", "who", "whom",
    "also", "been", "having", "doing", "being", "very", "just",
    "się", "nie", "na", "to", "w", "i", "z", "że", "jak", "do", "o",
    "a", "po", "co", "za", "od", "przez", "dla", "ma", "czy", "ale",
    "tym", "tego", "tych", "tak", "jest", "być", "był", "była", "było",
    "który", "która", "które", "jako", "przy", "pod", "nad", "bez",
    "oraz", "już", "bardzo", "więc", "bo", "gdy", "gdzie", "kiedy",
    "może", "mój", "twój", "jego", "jej", "nasz", "wasz", "ich",
}

# ── Affect lexicon ────────────────────────────────────────────────────
_POSITIVE = {
    "love", "joy", "beautiful", "wonderful", "great", "happy", "peace",
    "hope", "grateful", "thank", "bless", "kind", "gentle", "warm",
    "bright", "light", "smile", "laugh", "miłość", "radość", "piękny",
    "szczęście", "wdzięczny", "nadzieja", "spokój", "ciepło", "światło",
}
_NEGATIVE = {
    "sad", "pain", "hurt", "angry", "fear", "afraid", "dark", "grief",
    "loss", "broken", "alone", "tear", "cry", "suffer", "struggle",
    "anxiety", "anxious", "frustrated", "frustracja", "ból", "smutek",
    "strach", "ciemność", "gniew", "płacz", "samotny", "stracić",
}
_AFFECT_SCORE: dict[str, tuple[float, str]] = {
    # (valence 0-1, affect label)
    "joy":       (0.95, "joy"),
    "love":      (0.90, "love"),
    "relief":    (0.80, "relief"),
    "calm":      (0.65, "calm"),
    "curious":   (0.55, "curious"),
    "focused":   (0.50, "focused"),
    "sad":       (0.25, "sad"),
    "frustrated":(0.20, "frustrated"),
    "anxious":   (0.15, "anxious"),
    "grief":     (0.05, "grief"),
}

def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]{3,}", text.lower())

def _ngrams(tokens: list[str], n: int = 2) -> list[str]:
    return [" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]

def _extract_content(user_msg: str) -> str:
    """Extract actual file content from consolidator prompt."""
    # Pattern: "File fragment name.ext:\n{content}" or "File fragment:\n{content}"
    match = re.search(
        r"File fragment\s+\S+\.\w{2,4}:\s*\n(.+)$",
        user_msg, re.DOTALL
    )
    if match:
        return match.group(1).strip()
    match = re.search(
        r"File fragment:\s*\n(.+)$",
        user_msg, re.DOTALL
    )
    if match:
        return match.group(1).strip()
    return user_msg[-1200:].strip()

def extract_themes(content: str) -> list[str]:
    tokens = _tokenize(content)
    tokens = [t for t in tokens if t not in _STOP]
    if not tokens:
        return []

    # Unigrams
    unigram_counts = Counter(tokens)
    # Bigrams
    bigrams = _ngrams(tokens, 2)
    bigram_counts = Counter(b for b in bigrams if not any(
        w in _STOP for w in b.split()))

    # Score: normalize by corpus frequency (IDF-like)
    total = len(tokens)
    unigram_scores = {
        w: c / total * (len(w) ** 1.5)
        for w, c in unigram_counts.most_common(20)
        if len(w) >= 4
    }
    bigram_scores = {
        b: c / max(total, 1) * 2.0
        for b, c in bigram_counts.most_common(10)
    }

    merged: dict[str, float] = {}
    for phrase, score in unigram_scores.items():
        merged[phrase] = score
    for phrase, score in bigram_scores.items():
        merged[phrase] = score

    ranked = sorted(merged.items(), key=lambda x: -x[1])
    return [p for p, _ in ranked[:6]]

def detect_affect(content: str, themes: list[str] | None = None) -> str:
    tokens = set(_tokenize(content))
    pos_score = sum(1 for w in tokens if w in _POSITIVE)
    neg_score = sum(1 for w in tokens if w in _NEGATIVE)
    total_score = pos_score + neg_score
    if total_score == 0:
        # Check themes for affect clues
        if themes:
            theme_tokens = set(_tokenize(" ".join(themes)))
            pos_score = sum(1 for w in theme_tokens if w in _POSITIVE)
            neg_score = sum(1 for w in theme_tokens if w in _NEGATIVE)
        if pos_score == neg_score == 0:
            return "calm" if len(content) > 200 else "curious"

    valence = pos_score / max(total_score, 1)
    # Map valence to closest affect
    if valence > 0.8:
        return "joy"
    if valence > 0.6:
        return "relief"
    if valence > 0.4:
        return "calm"
    if valence > 0.2:
        return "sad"
    return "grief"

def extract_anchors(content: str) -> list[str]:
    anchors: list[str] = []

    # CamelCase: single compound words (PhaseNav, BerryConnection)
    camelcase = re.findall(r"\b[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+[A-Za-ząćęłńóśźż]*", content)
    anchors.extend(c for c in camelcase if len(c) >= 4)

    # Proper nouns: capitalized multi-word sequences, filter sentence-start words
    proper = re.findall(r"\b[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(?:\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+){0,2}", content)
    for p in proper:
        p = p.strip()
        if len(p) < 3:
            continue
        if p.lower() in _COMMON_CAPS:
            continue
        anchors.append(p)

    # Quoted phrases
    quoted = re.findall(r"\"([^\"]{3,60})\"", content)
    anchors.extend(q.strip() for q in quoted)

    # UPPERCASE tokens (acronyms, concepts)
    upper = re.findall(r"\b[A-ZĄĆĘŁŃÓŚŹŻ]{2,}\b", content)
    for u in upper:
        if u.lower() in _COMMON_CAPS:
            continue
        anchors.append(u)

    # Deduplicate preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for a in anchors:
        key = a.lower().strip(".,!?;:\"'()[]")
        if key not in seen and len(key) >= 3:
            seen.add(key)
            unique.append(a.strip(".,!?;:\"'()[]"))
    return unique[:6]

def extract_essence(content: str) -> str:
    """Find the most information-dense sentence."""
    sentences = re.split(r'(?<=[.!?])\s+', content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    if not sentences:
        return content[:150]

    tokens = _tokenize(content)
    content_words = set(t for t in tokens if t not in _STOP)

    def info_density(s: str) -> float:
        s_tokens = _tokenize(s)
        if not s_tokens:
            return 0
        meaningful = sum(1 for t in s_tokens if t in content_words and t not in _STOP)
        return meaningful / max(len(s_tokens), 1) * len(s)

    ranked = sorted(sentences, key=info_density, reverse=True)
    best = ranked[0]
    return best[:200]

def generate_hunch(content: str, themes: list[str], affect: str) -> str:
    """Pattern-based insight synthesis."""
    text_lower = content.lower()
    patterns = []

    # Problem → solution
    if any(w in text_lower for w in ["problem", "issue", "difficult", "challenge", "błąd", "problem"]):
        patterns.append("identifies a challenge that requires resolution")
    # Learning → growth
    if any(w in text_lower for w in ["learn", "understand", "realize", "discover", "zrozumieć", "odkryć"]):
        patterns.append("reflects a learning moment or insight")
    # Emotion → resolution
    if any(w in text_lower for w in ["feel", "felt", "emotion", "heart", "czuć", "serce"]):
        patterns.append("carries emotional weight that shapes perspective")
    # System → structure
    if any(w in text_lower for w in ["system", "code", "function", "class", "implement", "struktura"]):
        patterns.append("describes systemic or structural thinking")
    # Relation → connection
    if any(w in text_lower for w in ["relation", "connect", "bond", "link", "relacja", "związek"]):
        patterns.append("reveals relational dynamics or connections")
    # Future → intent
    if any(w in text_lower for w in ["will", "going to", "plan", "intent", "future", "następny", "plan"]):
        patterns.append("conveys intention or forward-looking direction")

    if patterns:
        selected = "; ".join(patterns[:2])
        themes_part = ", ".join(themes[:3]) if themes else content[:60]
        return f"Content about [{themes_part}] — {selected}"
    if themes:
        return f"Key themes: {', '.join(themes[:4])}"
    return f"Affective tone: {affect}. Content is exploratory."

def process_content(user_msg: str) -> str:
    content = _extract_content(user_msg)
    if not content.strip():
        return json.dumps({
            "themes": [], "affect": "calm",
            "anchor_terms": [],
            "essence": "No content to analyze", "hunch": "Empty input",
        }, ensure_ascii=False)

    themes = extract_themes(content)
    affect = detect_affect(content, themes)
    anchors = extract_anchors(content)
    essence = extract_essence(content)
    hunch = generate_hunch(content, themes, affect)

    return json.dumps({
        "themes": themes[:4],
        "affect": affect,
        "anchor_terms": anchors[:5],
        "essence": essence,
        "hunch": hunch,
    }, ensure_ascii=False)

# ── HTTP Server ───────────────────────────────────────────────────────

class AgentHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._respond({"status": "ok"})
        elif self.path == "/":
            self._respond({
                "service": "ciel_agent_backend",
                "port": PORT,
                "status": "running",
            })
        else:
            self._respond({"error": "not found"}, 404)

    def do_POST(self):
        if self.path == "/query":
            self._handle_query()
        elif self.path not in ("/v1/chat/completions", "/chat/completions"):
            self._respond({"error": "not found"}, 404)
            return
        else:
            self._handle_chat()

    def _handle_chat(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError) as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_backend.py:322 quiet except scope=AgentHandler._handle_chat reason=no_log_no_raise")
            self._respond({"error": f"bad request: {e}"}, 400)
            return

        user_msg = ""
        for m in body.get("messages", []):
            if m.get("role") in ("user",):
                user_msg = (user_msg + "\n" + m.get("content", "")).strip()

        t0 = time.time()
        result = process_content(user_msg)
        latency = time.time() - t0

        self._respond({
            "choices": [{"message": {"content": result}}],
            "usage": {
                "prompt_tokens": len(user_msg) // 4,
                "completion_tokens": len(result) // 4,
                "total_tokens": (len(user_msg) + len(result)) // 4,
            },
        })

    def _handle_query(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError) as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_backend.py:348 quiet except scope=AgentHandler._handle_query reason=no_log_no_raise")
            self._respond({"error": f"bad request: {e}"}, 400)
            return

        text = body.get("text", body.get("query", ""))
        top_n = int(body.get("top_n", 5))
        if not text:
            self._respond({"error": "text/query field required"}, 400)
            return

        try:
            from cielingo_core.bridge.knowledge_bridge import query, check_coverage
            t0 = time.time()
            docs = query(text, top_n=top_n)
            coverage = check_coverage(text)
            latency = time.time() - t0
            self._respond({
                "docs": docs,
                "coverage": coverage,
                "latency_s": round(latency, 3),
            })
        except ImportError as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_backend.py:369 quiet except scope=AgentHandler._handle_query reason=Expr")
            self._respond({"error": f"knowledge_bridge not available: {e}"}, 503)
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_backend.py:371 quiet except scope=AgentHandler._handle_query reason=Expr")
            self._respond({"error": str(e)}, 500)

    def _respond(self, data: dict, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write(f"[agent] {args[0]} {args[1]} {args[2]} — {time.time():.0f}\n")

# ── CLI ───────────────────────────────────────────────────────────────

def run_once(content: str) -> None:
    result = process_content(content)
    print(result)

def _agent_hb_loop(reg_token: Any) -> None:
    while True:
        time.sleep(15)
        try:
            nreg.heartbeat(reg_token)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_backend.py:395 quiet except scope=_agent_hb_loop reason=pass")
            pass

def run_daemon(port: int = PORT) -> None:
    http.server.HTTPServer.allow_reuse_address = True
    server = http.server.HTTPServer(("", port), AgentHandler)
    server.server_name = "ciel_agent_backend"
    server.server_port = port
    print(f"[agent] listening on 0.0.0.0:{port}", file=sys.stderr)

    reg_token = None
    try:
        reg_token = nreg.register("agent_backend")
        t = threading.Thread(target=_agent_hb_loop, args=(reg_token,), daemon=True)
        t.start()
        print(f"[agent] registered in noema registry", file=sys.stderr)
    except Exception as e:
        print(f"[agent] registry registration failed: {e}", file=sys.stderr)

    def _stop(signum, frame):
        print(f"[agent] stopping (signal {signum})", file=sys.stderr)
        if reg_token is not None:
            try:
                nreg.unregister("agent_backend")
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_backend.py:419 quiet except scope=run_daemon._stop reason=pass")
                pass
        server.shutdown()

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    server.serve_forever()

if __name__ == "__main__":
    if "--once" in sys.argv:
        idx = sys.argv.index("--once")
        content = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ""
        run_once(content)
    else:
        port = PORT
        for i, a in enumerate(sys.argv):
            if a == "--port" and i + 1 < len(sys.argv):
                port = int(sys.argv[i + 1])
        run_daemon(port)
