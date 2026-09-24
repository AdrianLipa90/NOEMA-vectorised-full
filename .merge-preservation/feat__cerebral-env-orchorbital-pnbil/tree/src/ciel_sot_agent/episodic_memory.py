from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence
import hashlib
import json
import re


PROVENANCE_CLASSES = {
    "source",
    "user_statement",
    "assistant_inference",
    "hypothesis",
    "correction",
    "memory_retrieval",
}


@dataclass(frozen=True)
class TemporalAnchor:
    kind: str
    value: str | None
    precision: str
    resolved: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Episode:
    episode_id: str
    content: str
    topic: str | None
    provenance_class: str
    temporal_anchor: TemporalAnchor
    confidence: float
    admission_verdict: str
    memory_layer: str
    source_ref: str | None
    supersedes: List[str]
    sequence: int

    def to_dict(self) -> Dict[str, Any]:
        row = asdict(self)
        row["temporal_anchor"] = self.temporal_anchor.to_dict()
        return row


@dataclass(frozen=True)
class ContradictionEdge:
    left_episode_id: str
    right_episode_id: str
    relation: str
    reason: str
    confidence: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _tokens(text: str) -> List[str]:
    return re.findall(r"[\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ-]+", text, flags=re.UNICODE)


def _normalize_topic(topic: str | None) -> str | None:
    if topic is None:
        return None
    value = topic.strip()
    return value or None


def resolve_temporal_anchor(text: str, *, now: datetime | None = None, language: str = "pl") -> TemporalAnchor:
    base = now or datetime.now(timezone.utc)
    if base.tzinfo is None:
        base = base.replace(tzinfo=timezone.utc)
    low = text.lower()

    iso = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", text)
    if iso:
        return TemporalAnchor("absolute_date", iso.group(1), "day", True)

    if language == "pl":
        mapping = {
            "dzisiaj": 0,
            "dziś": 0,
            "wczoraj": -1,
            "przedwczoraj": -2,
            "jutro": 1,
            "pojutrze": 2,
        }
        vague_past = ("wcześniej", "wczesniej", "poprzednio", "ostatnio")
        present = ("teraz", "obecnie", "aktualnie")
    else:
        mapping = {"today": 0, "yesterday": -1, "tomorrow": 1}
        vague_past = ("earlier", "previously", "recently")
        present = ("now", "currently")

    for marker, delta in mapping.items():
        if marker in low:
            value = (base + timedelta(days=delta)).date().isoformat()
            return TemporalAnchor("relative_date", value, "day", True)
    if any(marker in low for marker in present):
        return TemporalAnchor("present", base.isoformat(), "instant", True)
    if any(marker in low for marker in vague_past):
        return TemporalAnchor("relative_past", None, "unknown", False)
    return TemporalAnchor("unspecified", None, "unknown", False)


def classify_provenance(
    text: str,
    *,
    role: str,
    explicit_class: str | None = None,
    correction_requested: bool = False,
) -> str:
    if explicit_class in PROVENANCE_CLASSES:
        return explicit_class
    low = text.strip().lower()
    if correction_requested:
        return "correction"
    if role == "user":
        if low.startswith(("hipoteza:", "chyba ", "może ", "moze ", "prawdopodobnie ")):
            return "hypothesis"
        return "user_statement"
    if role == "assistant":
        if low.startswith(("hipoteza:", "chyba ", "prawdopodobnie ", "i infer", "inference:")):
            return "hypothesis"
        return "assistant_inference"
    if role == "source":
        return "source"
    return "memory_retrieval"


def admission_policy(provenance_class: str, confidence: float) -> tuple[str, str]:
    conf = max(0.0, min(1.0, float(confidence)))
    if provenance_class == "source":
        return ("accept", "semantic") if conf >= 0.75 else ("candidate", "episodic")
    if provenance_class == "correction":
        return ("accept", "episodic") if conf >= 0.70 else ("candidate", "episodic")
    if provenance_class == "user_statement":
        return ("accept", "episodic") if conf >= 0.55 else ("candidate", "episodic")
    if provenance_class in {"hypothesis", "assistant_inference"}:
        return ("candidate", "episodic") if conf >= 0.35 else ("reject", "none")
    if provenance_class == "memory_retrieval":
        return ("accept", "working") if conf >= 0.50 else ("candidate", "working")
    return "reject", "none"


def make_episode(
    content: str,
    *,
    topic: str | None,
    role: str,
    confidence: float,
    sequence: int,
    language: str = "pl",
    now: datetime | None = None,
    explicit_class: str | None = None,
    correction_requested: bool = False,
    source_ref: str | None = None,
    supersedes: Sequence[str] | None = None,
) -> Episode:
    provenance = classify_provenance(
        content,
        role=role,
        explicit_class=explicit_class,
        correction_requested=correction_requested,
    )
    verdict, layer = admission_policy(provenance, confidence)
    anchor = resolve_temporal_anchor(content, now=now, language=language)
    seed = json.dumps(
        {
            "content": content,
            "topic": _normalize_topic(topic),
            "provenance": provenance,
            "sequence": int(sequence),
            "source_ref": source_ref,
        },
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    episode_id = "ep_" + hashlib.sha256(seed).hexdigest()[:20]
    return Episode(
        episode_id=episode_id,
        content=content.strip(),
        topic=_normalize_topic(topic),
        provenance_class=provenance,
        temporal_anchor=anchor,
        confidence=max(0.0, min(1.0, float(confidence))),
        admission_verdict=verdict,
        memory_layer=layer,
        source_ref=source_ref,
        supersedes=list(supersedes or []),
        sequence=int(sequence),
    )


def append_episode(journal_path: str | Path, episode: Episode) -> None:
    path = Path(journal_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(episode.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")


def load_episodes(journal_path: str | Path) -> List[Episode]:
    path = Path(journal_path)
    if not path.exists():
        return []
    out: List[Episode] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        anchor_row = row.get("temporal_anchor", {})
        row["temporal_anchor"] = TemporalAnchor(**anchor_row)
        out.append(Episode(**row))
    return out


def _claim_signature(text: str, topic: str | None) -> tuple[set[str], bool]:
    low = text.lower()
    neg = bool(re.search(r"\b(nie|nigdy|brak|never|not|no)\b", low))
    stop = {
        "pamiętam", "pamietam", "powiedział", "powiedzial", "twierdzi", "that", "remember",
        "wczoraj", "dzisiaj", "dziś", "teraz", "yesterday", "today", "now",
    }
    sig = {tok.lower()[:7] for tok in _tokens(text) if len(tok) >= 4 and tok.lower() not in stop}
    if topic:
        sig.add(topic.lower()[:7])
    return sig, neg


def build_contradiction_lattice(episodes: Sequence[Episode]) -> List[ContradictionEdge]:
    edges: List[ContradictionEdge] = []
    accepted = [ep for ep in episodes if ep.admission_verdict != "reject"]
    for i, left in enumerate(accepted):
        for right in accepted[i + 1 :]:
            if left.topic and right.topic and left.topic.lower() != right.topic.lower():
                continue
            lsig, lneg = _claim_signature(left.content, left.topic)
            rsig, rneg = _claim_signature(right.content, right.topic)
            overlap = len(lsig & rsig)
            if overlap < 2 or lneg == rneg:
                continue
            if right.provenance_class == "correction" or left.episode_id in right.supersedes:
                relation = "supersedes"
                reason = "later_correction_overrides_conflicting_claim"
            else:
                relation = "conflicts_with"
                reason = "opposed_polarity_on_shared_signature"
            conf = min(left.confidence, right.confidence)
            edges.append(
                ContradictionEdge(
                    left_episode_id=left.episode_id,
                    right_episode_id=right.episode_id,
                    relation=relation,
                    reason=reason,
                    confidence=conf,
                )
            )
    return edges



def episodes_from_rows(rows: Sequence[Mapping[str, Any]]) -> List[Episode]:
    out: List[Episode] = []
    for row in rows:
        if not isinstance(row, Mapping):
            continue
        content = str(row.get("content") or row.get("text") or "").strip()
        if not content:
            continue
        anchor_row = row.get("temporal_anchor") if isinstance(row.get("temporal_anchor"), Mapping) else None
        if anchor_row:
            anchor = TemporalAnchor(
                kind=str(anchor_row.get("kind", "unspecified")),
                value=str(anchor_row.get("value")) if anchor_row.get("value") is not None else None,
                precision=str(anchor_row.get("precision", "unknown")),
                resolved=bool(anchor_row.get("resolved", False)),
            )
        else:
            anchor = resolve_temporal_anchor(content, language=str(row.get("language", "pl")))
        provenance = str(row.get("provenance_class", "memory_retrieval"))
        if provenance not in PROVENANCE_CLASSES:
            provenance = "memory_retrieval"
        confidence = max(0.0, min(1.0, float(row.get("confidence", 0.5) or 0.5)))
        verdict = str(row.get("admission_verdict", ""))
        layer = str(row.get("memory_layer", ""))
        if not verdict or not layer:
            verdict, layer = admission_policy(provenance, confidence)
        seed = json.dumps({
            "content": content,
            "topic": row.get("topic"),
            "sequence": int(row.get("sequence", len(out))),
            "provenance": provenance,
        }, ensure_ascii=False, sort_keys=True).encode("utf-8")
        episode_id = str(row.get("episode_id") or ("ep_" + hashlib.sha256(seed).hexdigest()[:20]))
        out.append(Episode(
            episode_id=episode_id,
            content=content,
            topic=_normalize_topic(str(row.get("topic"))) if row.get("topic") is not None else None,
            provenance_class=provenance,
            temporal_anchor=anchor,
            confidence=confidence,
            admission_verdict=verdict,
            memory_layer=layer,
            source_ref=str(row.get("source_ref")) if row.get("source_ref") is not None else None,
            supersedes=[str(x) for x in row.get("supersedes", [])] if isinstance(row.get("supersedes", []), list) else [],
            sequence=int(row.get("sequence", len(out))),
        ))
    return out

def select_episodic_memory(
    query: str,
    episodes: Sequence[Episode],
    *,
    topic: str | None = None,
) -> Episode | None:
    qtokens = {tok.lower()[:6] for tok in _tokens(query) if len(tok) >= 4}
    best: tuple[float, Episode] | None = None
    for ep in episodes:
        if ep.admission_verdict == "reject":
            continue
        etokens = {tok.lower()[:6] for tok in _tokens(ep.content) if len(tok) >= 4}
        lexical = len(qtokens & etokens)
        topic_bonus = 2.0 if topic and ep.topic and topic.lower() == ep.topic.lower() else 0.0
        provenance_bonus = {
            "source": 0.8,
            "correction": 0.7,
            "user_statement": 0.4,
            "memory_retrieval": 0.3,
            "hypothesis": 0.1,
            "assistant_inference": 0.0,
        }.get(ep.provenance_class, 0.0)
        score = lexical + topic_bonus + provenance_bonus + ep.confidence
        if score <= 0:
            continue
        if best is None or score > best[0] or (score == best[0] and ep.sequence > best[1].sequence):
            best = (score, ep)
    return best[1] if best else None
