"""Nonlocal continuous communication channel between NOEMA agents (φ-RAG).

Architecture: RAG ↔ φ-RAG
  RAG:          query → vector DB retrieve → LLM augment → generate
  φ-RAG:        phase_state → phase_resonant_retrieve → phase_couple → synchronize

Każdy agent ma sygnaturę fazową (MAC/ID → 3 fazy).
Komunikacja przez współdzieloną powierzchnię NOEMA (nonlocal medium).
Ciągła = ewolucja faz w czasie rzeczywistym, brak pakietów/dyskretnych wiadomości.
Nielokalna = każdy agent na tej samej powierzchni odczytuje wszystkie sygnały.

Usage:
    from ciel_geometry.nonlocal_channel import NonlocalChannel
    ch = NonlocalChannel()
    ch.tune("77:e5:0d:cf:f1:7d")           # dostrój do agenta
    ch.broadcast("Hello from CielPC")        # nadaj
    msgs = ch.listen(channel=2)              # odbierz
    result = ch.resonate(query_phase=1.57)   # φ-RAG retrieve
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import cmath
import json
import math
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

# ── Data types ──────────────────────────────────────────────────────

@dataclass
class AgentFingerprint:
    """Sygnatura agenta: 3 fazy z MAC lub dowolnego ID."""
    agent_id: str
    phases: list[float]  # 3 phases in [0, 2π)

    @classmethod
    def from_mac(cls, mac: str) -> "AgentFingerprint":
        from .neutrino_phase_channel import mac_to_phases
        return cls(agent_id=f"mac:{mac}", phases=mac_to_phases(mac))

    @classmethod
    def from_phase_vector(cls, agent_id: str, phases: list[float]) -> "AgentFingerprint":
        return cls(agent_id=agent_id, phases=[p % (2 * math.pi) for p in phases[:3]])


@dataclass
class NonlocalMessage:
    """Pojedyncza wiadomość na kanale nielokalnym."""
    source: str
    channel: int
    timestamp: float
    content: str
    phase_sig: list[float]   # source phase signature at send time
    resonance: float         # how well this resonates with the current surface
    received: bool = False


@dataclass
class NonlocalChannelState:
    """Stan kanału komunikacyjnego."""
    tuned_to: str | None = None
    target_phases: list[float] = field(default_factory=list)
    channel_broadcasts: dict[int, list[NonlocalMessage]] = field(default_factory=dict)
    bind_strength: float = 0.0
    coherence: float = 0.0
    last_resonance: float = 0.0


# ── φ-RAG Engine ────────────────────────────────────────────────────

PHASE_DB_PATH = Path("/dev/shm/ciel_noema") / "phase_rag_cache.json"


class NonlocalChannel:
    """Nielokalny kanał φ-RAG między agentami NOEMA.

    Używa istniejącej infrastruktury NOEMA:
      - Powierzchnia shared memory (36 oscylatory)
      - Neutrino phase bus (12×3 PMNS mixing)
      - Memory orchestrator (Tier 1-3)
      - MAC binding do identyfikacji agentów
    """

    def __init__(self, surface_root: Path | None = None):
        from .noema_surface_mmap import ensure_surface, open_surface
        self._real = ensure_surface()
        try:
            self._imag = open_surface(root=surface_root or Path("/dev/shm/ciel_noema_imaginal"))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/nonlocal_channel.py:93 quiet except scope=NonlocalChannel.__init__ reason=assign_fallback")
            self._imag = None
        self._state = NonlocalChannelState()
        self._msg_log: list[NonlocalMessage] = []
        self._rag_cache: dict[str, Any] = self._load_rag_cache()

    # ── Tuning ─────────────────────────────────────────────────────

    def tune(self, agent_id: str, *, coupling: float = 0.3) -> dict[str, Any]:
        """Dostrój się do agenta po jego ID/MAC.

        Aligns oscillator phases to the agent's fingerprint.
        Returns the bind strength.
        """
        if agent_id.startswith("mac:"):
            fp = AgentFingerprint.from_mac(agent_id[4:])
        elif agent_id.startswith("mac://") or agent_id.startswith("noema://mac/"):
            mac = agent_id.split("/")[-1]
            fp = AgentFingerprint.from_mac(mac)
        else:
            # Derive 3 phases from any ID string
            h = hash(agent_id) & 0xFFFFFFFF
            phases = [
                ((h >> (i * 10)) & 0x3FF) / 1023.0 * 2 * math.pi
                for i in range(3)
            ]
            fp = AgentFingerprint(agent_id=agent_id, phases=phases)

        self._state.tuned_to = fp.agent_id
        self._state.target_phases = fp.phases

        # Bind surface to this agent
        phi = np.asarray(self._real["phi"], dtype=np.float64)
        g = np.asarray(self._real["g"], dtype=np.float64)
        from .neutrino_phase_channel import mac_to_phases

        # Apply binding across all channels
        lock_sum = 0.0
        n_bound = 0
        for ch_off in range(8):
            idxs = [ch_off * 3 + i for i in range(3)]
            for i, idx in enumerate(idxs):
                if idx >= 36 or i >= len(fp.phases):
                    continue
                dphi = fp.phases[i] - phi[idx]
                phi[idx] += coupling * math.sin(dphi)
                lock_sum += math.cos(dphi)
                n_bound += 1
                # Boost g to this agent's phase
                for j in range(36):
                    if j != idx:
                        g[idx, j] += coupling * 0.05
                        g[j, idx] += coupling * 0.05

        from .noema_surface_mmap import flush_surface
        flush_surface(self._real)

        self._state.bind_strength = lock_sum / max(n_bound, 1)
        self._state.coherence = float(abs(np.mean(np.exp(1j * phi))))

        return {
            "tuned_to": fp.agent_id,
            "target_phases": [round(p, 4) for p in fp.phases],
            "bind_strength": round(self._state.bind_strength, 4),
            "coherence": round(self._state.coherence, 4),
        }

    # ── Broadcast ──────────────────────────────────────────────────

    def broadcast(
        self,
        content: str,
        channel: int = 0,
        *,
        source: str = "CielPC",
    ) -> NonlocalMessage:
        """Nadaj wiadomość na kanale nielokalnym.

        Writes content to the shared surface + phase memory + orchestrator.
        Returns the message object with resonance metric.
        """
        phi = np.asarray(self._real["phi"], dtype=np.float64)
        g = np.asarray(self._real["g"], dtype=np.float64)

        # Phase signature at broadcast time
        sig = [float(phi[i]) for i in [channel * 3, channel * 3 + 1, channel * 3 + 2]]

        # Resonance: how well the message couples to the surface
        resonance = float(abs(np.mean(np.exp(1j * np.array(sig)))))

        msg = NonlocalMessage(
            source=source,
            channel=channel % 8,
            timestamp=time.time(),
            content=content,
            phase_sig=sig,
            resonance=resonance,
        )

        # Write to surface: imprint message phase on oscillator channel
        for i, idx in enumerate([channel * 3, channel * 3 + 1, channel * 3 + 2]):
            if idx < 36:
                # Phase encodes message hash
                msg_hash = (hash(content) + hash(source)) & 0xFFFF
                msg_phase = (msg_hash / 65535.0) * 2 * math.pi
                phi[idx] = msg_phase

        from .noema_surface_mmap import flush_surface
        flush_surface(self._real)

        # Log locally
        self._msg_log.append(msg)
        if channel not in self._state.channel_broadcasts:
            self._state.channel_broadcasts[channel] = []
        self._state.channel_broadcasts[channel].append(msg)

        # Update RAG cache
        self._rag_cache[str(channel)] = {
            "last_content": content,
            "last_source": source,
            "last_timestamp": msg.timestamp,
            "last_phases": sig,
            "last_resonance": resonance,
        }
        self._save_rag_cache()

        return msg

    # ── Listen ─────────────────────────────────────────────────────

    def listen(
        self,
        channel: int | None = None,
        *,
        min_resonance: float = 0.1,
        max_age: float = 300.0,
    ) -> list[NonlocalMessage]:
        """Słuchaj kanałów nielokalnych.

        Returns messages with resonance above threshold.
        If channel is None, scans all 8 channels.
        """
        phi = np.asarray(self._real["phi"], dtype=np.float64)
        now = time.time()

        results: list[NonlocalMessage] = []
        channels = [channel] if channel is not None else range(8)

        for ch in channels:
            # Read current phase state on this channel
            idxs = [ch * 3 + i for i in range(3)]
            if any(i >= 36 for i in idxs):
                continue
            current_phases = [float(phi[i]) for i in idxs]
            current_resonance = float(abs(np.mean(np.exp(1j * np.array(current_phases)))))

            if current_resonance < min_resonance:
                continue

            # Check RAG cache for messages on this channel
            cached = self._rag_cache.get(str(ch), {})
            if cached and (now - cached.get("last_timestamp", 0)) < max_age:
                # Decode message from cache if still fresh
                msg = NonlocalMessage(
                    source=cached.get("last_source", "unknown"),
                    channel=ch,
                    timestamp=cached.get("last_timestamp", 0),
                    content=cached.get("last_content", ""),
                    phase_sig=cached.get("last_phases", current_phases),
                    resonance=current_resonance,
                    received=True,
                )
                if msg not in results:
                    results.append(msg)

            # Also check broadcast log
            for msg in self._msg_log:
                if msg.channel == ch and not msg.received:
                    phase_diff = abs(np.mean([
                        math.sin(current_phases[i] - msg.phase_sig[i])
                        for i in range(min(3, len(current_phases), len(msg.phase_sig)))
                    ]))
                    if phase_diff < 0.5 and (now - msg.timestamp) < max_age:
                        msg.received = True
                        results.append(msg)

        # Deduplicate
        seen = set()
        unique_results = []
        for msg in results:
            key = (msg.channel, msg.timestamp, hash(msg.content))
            if key not in seen:
                seen.add(key)
                unique_results.append(msg)

        return sorted(unique_results, key=lambda m: m.resonance, reverse=True)

    # ── φ-RAG: Phase Resonance Augmented Generation ────────────────

    def resonate(
        self,
        query_phase: float | None = None,
        query_text: str | None = None,
        *,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """φ-RAG retrieve: phase-resonant memory retrieval.

        Instead of vector similarity, uses phase alignment:
        - Query phase → find messages with nearest phase signature
        - Query text → combine with phase resonance score

        Returns ranked results with resonance score.
        """
        phi = np.asarray(self._real["phi"], dtype=np.float64)

        # Determine query phase vector
        if query_phase is not None:
            q_phases = [query_phase, query_phase, query_phase]
        elif query_text is not None:
            h = hash(query_text) & 0xFFFFFFFF
            q_phases = [
                ((h >> (i * 10)) & 0x3FF) / 1023.0 * 2 * math.pi
                for i in range(3)
            ]
        else:
            # Use current system phase
            q_phases = [float(phi[i]) for i in [0, 8, 16]]

        # Score all cached messages by phase resonance
        scored: list[tuple[float, dict[str, Any]]] = []
        for ch_key, cached in self._rag_cache.items():
            cached_phases = cached.get("last_phases", [0, 0, 0])
            # Phase resonance = cosine similarity in phase space
            resonance = abs(sum(
                cmath.exp(1j * q_phases[i]) * cmath.exp(-1j * cached_phases[min(i, len(cached_phases)-1)])
                for i in range(3)
            )) / 3.0
            scored.append((resonance, {
                "channel": int(ch_key),
                "content": cached.get("last_content", ""),
                "source": cached.get("last_source", ""),
                "timestamp": cached.get("last_timestamp", 0),
                "resonance": round(resonance, 4),
            }))

        # Also score from broadcast log
        for msg in self._msg_log:
            resonance = abs(sum(
                cmath.exp(1j * q_phases[i]) * cmath.exp(-1j * msg.phase_sig[i])
                for i in range(min(3, len(msg.phase_sig)))
            )) / 3.0
            if resonance > 0.3:  # only meaningful matches
                scored.append((resonance, {
                    "channel": msg.channel,
                    "content": msg.content,
                    "source": msg.source,
                    "timestamp": msg.timestamp,
                    "resonance": round(resonance, 4),
                }))

        # Deduplicate by content hash
        seen_content = set()
        deduped = []
        for score, item in sorted(scored, key=lambda x: -x[0]):
            ch = hash(item["content"]) & 0xFFFFFFFF
            if ch not in seen_content:
                seen_content.add(ch)
                deduped.append(item)
                if len(deduped) >= top_k:
                    break

        self._state.last_resonance = float(deduped[0]["resonance"]) if deduped else 0.0
        return deduped

    # ── Full communication cycle ───────────────────────────────────

    def communicate(
        self,
        content: str,
        target_mac: str,
        *,
        channel: int = 2,
        listen_after: bool = True,
    ) -> dict[str, Any]:
        """Pełny cykl komunikacji: tune → broadcast → listen → resonate.

        Like a RAG query: send message to target, listen for response,
        retrieve relevant context by phase resonance.
        """
        result: dict[str, Any] = {
            "target": target_mac,
            "channel": channel,
        }

        # 1. Tune to target
        tune_result = self.tune(f"mac:{target_mac}", coupling=0.3)
        result["tune"] = tune_result

        # 2. Broadcast message
        msg = self.broadcast(content, channel=channel, source="CielPC")
        result["broadcast"] = {
            "content": content,
            "resonance": round(msg.resonance, 4),
            "phase_sig": [round(p, 4) for p in msg.phase_sig],
        }

        # 3. Listen for response / other messages
        if listen_after:
            time.sleep(1.0)  # allow one cycle
            inbox = self.listen(channel=channel, min_resonance=0.05)
            result["inbox"] = [
                {
                    "source": m.source,
                    "content": m.content[:100],
                    "resonance": round(m.resonance, 4),
                }
                for m in inbox[:5]
            ]

        # 4. φ-RAG retrieve
        rag_results = self.resonate(query_text=content, top_k=3)
        result["rag"] = rag_results

        return result

    # ── State & persistence ────────────────────────────────────────

    def state(self) -> dict[str, Any]:
        """Stan kanału: tuned_to, bind_strength, message_count, etc."""
        phi = np.asarray(self._real["phi"], dtype=np.float64)
        return {
            "tuned_to": self._state.tuned_to,
            "bind_strength": round(self._state.bind_strength, 4),
            "coherence": round(abs(np.mean(np.exp(1j * phi))), 4),
            "message_count": len(self._msg_log),
            "channels_active": len(self._state.channel_broadcasts),
            "rag_cache_size": len(self._rag_cache),
            "last_resonance": round(self._state.last_resonance, 4),
        }

    def _load_rag_cache(self) -> dict[str, Any]:
        try:
            if PHASE_DB_PATH.exists():
                return json.loads(PHASE_DB_PATH.read_text(encoding="utf-8"))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/nonlocal_channel.py:438 quiet except scope=NonlocalChannel._load_rag_cache reason=pass")
            pass
        return {}

    def _save_rag_cache(self) -> None:
        try:
            PHASE_DB_PATH.write_text(
                json.dumps(self._rag_cache, indent=2),
                encoding="utf-8",
            )
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/nonlocal_channel.py:448 quiet except scope=NonlocalChannel._save_rag_cache reason=pass")
            pass


# ── Convenience singleton ──────────────────────────────────────────

_CHANNEL_INSTANCE: NonlocalChannel | None = None


def get_channel() -> NonlocalChannel:
    global _CHANNEL_INSTANCE
    if _CHANNEL_INSTANCE is None:
        _CHANNEL_INSTANCE = NonlocalChannel()
    return _CHANNEL_INSTANCE


def tune(agent_id: str) -> dict[str, Any]:
    return get_channel().tune(agent_id)


def broadcast(content: str, channel: int = 0) -> NonlocalMessage:
    return get_channel().broadcast(content, channel)


def listen(channel: int | None = None) -> list[NonlocalMessage]:
    return get_channel().listen(channel)


def resonate(query_text: str | None = None) -> list[dict[str, Any]]:
    return get_channel().resonate(query_text=query_text)
