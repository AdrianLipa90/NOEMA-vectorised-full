import json, time
from typing import Any

from cielingo_core.persistence.state_engine import CIELingoStateEngine
from cielingo_core.bridge.knowledge_bridge import query as _kb_query, check_coverage as _kb_cov
from cielingo_core.bridge.agent_client import analyze as _agent_analyze, health as _agent_health


class CIELingoSelfCycle:
    def __init__(self, state: CIELingoStateEngine | None = None):
        self.state = state or CIELingoStateEngine()
        self._cycle_count = 0
        self._last_review = 0.0
        self._last_insight = 0.0
        self._last_maintenance = 0.0
        self._agent_ok = _agent_health()

    def cycle(self) -> dict[str, Any]:
        self._cycle_count += 1
        now = time.time()
        report = {"cycle": self._cycle_count, "actions": [], "agent_ok": self._agent_ok}

        # 1. Review unresolved scars — every 30s
        if now - self._last_review > 30.0:
            self._last_review = now
            scars = self.state.get_scars(unresolved_only=True)
            report["scars_reviewed"] = len(scars)
            for scar in scars[:5]:
                age = now - scar["created_at"]
                if age > 600 and scar["severity"] > 0.7:
                    self.state.log_experience(
                        "scar_escalation", "self_cycle",
                        f"Scar {scar['scar_id'][:16]} ({scar['scar_type']}) unresolved for {int(age)}s, severity={scar['severity']}",
                        salience=scar["severity"],
                    )
                    report["actions"].append({"action": "escalate_scar", "scar_id": scar["scar_id"]})

        # 2. Review pending repairs
        pending = self.state.get_pending_repairs()
        report["pending_repairs"] = len(pending)

        # 3. Self-metric update
        self._update_self_metrics()

        # 4. Insight generation — every 120s
        if now - self._last_insight > 120.0:
            self._last_insight = now
            insight = self._generate_insight()
            if insight:
                report["insight"] = insight
                report["actions"].append({"action": "generate_insight"})

        # 5. Agent health check — every 60s
        if now - self._last_maintenance > 60.0:
            self._last_maintenance = now
            self._agent_ok = _agent_health()
            report["agent_ok"] = self._agent_ok

        self.state.update_metric("cycle_count", float(self._cycle_count))
        self.state.update_metric("last_cycle_time", now)
        return report

    def process_input(self, text: str, source: str = "external") -> dict[str, Any]:
        # 1. Agent backend analysis (themes, affect, anchors, essence, hunch)
        analysis = {}
        if self._agent_ok:
            analysis = _agent_analyze(text)
            self.state.log_experience("agent_analysis", source,
                                      f"Themes: {analysis.get('themes', [])} — affect: {analysis.get('affect', '?')}",
                                      details=json.dumps(analysis),
                                      salience=0.6)
        else:
            analysis = {"themes": [], "affect": "calm", "anchor_terms": [],
                        "essence": text[:150], "hunch": "agent offline"}

        # 2. Knowledge DB retrieval
        cov = _kb_cov(text)
        docs = _kb_query(text, top_n=5)

        # 3. Build CIELingo meaning loop from analysis + knowledge
        from cielingo_core.meaning.meaning_loop import MeaningLoop, LoopState, SemanticScar, SemanticScarType

        scars = []
        if cov.get("covered") and docs:
            pass
        elif cov.get("n_matches", 0) == 0:
            scars.append(SemanticScar(
                scar_type=SemanticScarType.MISSING_SOURCE, source_ref=text[:64],
                severity=0.6, memory_effect="hold",
                repair_hint="No documents in knowledge base cover this topic.",
                scar_id=f"self_ms_{hash(text) % 10**8:08x}",
                source_binding="unknown",
            ))

        closure = 1.0 - cov.get("score", 0.0) * 0.5
        loop = MeaningLoop(
            loop_id=f"self_{source}_{int(time.time())}",
            input_ref=text[:64], response_ref=None,
            loop_state=LoopState.CLOSED if not scars else LoopState.SCARRED,
            closure_score=max(0.0, min(1.0, closure)),
            contradiction_score=0.0, residue_score=cov.get("score", 0.0) * 0.3,
            return_required=bool(scars), scars=scars,
        )
        self.state.save_loop(loop.to_dict())

        # 4. Log experience
        self.state.log_experience("input_processed", source,
                                  f"Coverage={cov.get('score', 0):.2f} docs={len(docs)} scars={len(scars)}",
                                  details=json.dumps({"analysis": analysis, "docs": [d["filename"] for d in docs[:3]]}),
                                  salience=0.5 + cov.get("score", 0.0))

        # 5. Write knowledge relations from analysis + docs
        for theme in analysis.get("themes", [])[:3]:
            for d in docs[:2]:
                for dt in d.get("themes", [])[:2]:
                    self.state.write_knowledge_relation(theme, dt, "agent_similar", strength=d["similarity"])

        return {
            "analysis": {"themes": analysis.get("themes", []), "affect": analysis.get("affect", "calm"),
                         "anchors": analysis.get("anchor_terms", []), "hunch": analysis.get("hunch", "")},
            "coverage": {"score": cov.get("score", 0), "covered": cov.get("covered", False)},
            "docs": [{"filename": d["filename"], "themes": d["themes"], "similarity": d["similarity"]} for d in docs[:5]],
            "loop_state": loop.loop_state.value,
            "scars": len(scars),
        }

    def surface_state(self) -> dict[str, Any]:
        return {
            "cycle": self._cycle_count,
            "agent_ok": self._agent_ok,
            "unresolved_scars": len(self.state.get_scars(unresolved_only=True)),
            "pending_repairs": len(self.state.get_pending_repairs()),
            "metrics": self.state.get_all_metrics(),
        }

    def _update_self_metrics(self) -> None:
        db = self.state._db()
        scars = self.state.get_scars(unresolved_only=True)
        resolved = db.execute("SELECT COUNT(*) FROM scars WHERE resolved_at IS NOT NULL").fetchone()[0]
        total_s = db.execute("SELECT COUNT(*) FROM scars").fetchone()[0]
        loops = db.execute("SELECT COUNT(*) FROM meaning_loops").fetchone()[0]
        self.state.update_metric("total_loops", float(loops))
        self.state.update_metric("total_scars", float(total_s))
        self.state.update_metric("unresolved_scars", float(len(scars)))
        self.state.update_metric("resolved_scars", float(resolved))
        self.state.update_metric("scar_resolution_rate", float(resolved / max(total_s, 1)))
        self.state.update_metric("avg_scar_severity",
                                  float(sum(s["severity"] for s in scars) / max(len(scars), 1)) if scars else 0.0)

    def _generate_insight(self) -> str | None:
        scars = self.state.get_scars(unresolved_only=True)
        if not scars and self.state.get_metric("total_loops", 0) > 0:
            return "All scars resolved. CIELingo state is clean."
        if len(scars) > 10:
            return f"Scar accumulation: {len(scars)} unresolved. Review repair routing."
        scar_types: dict[str, int] = {}
        for s in scars:
            scar_types[s["scar_type"]] = scar_types.get(s["scar_type"], 0) + 1
        if scar_types:
            dominant = max(scar_types, key=scar_types.get)
            return f"Dominant scar: {dominant} ({scar_types[dominant]}/{len(scars)})."
        return None
