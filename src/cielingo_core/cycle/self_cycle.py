import json, time
from typing import Any

from cielingo_core.persistence.state_engine import CIELingoStateEngine
from cielingo_core.bridge.knowledge_bridge import query as _kb_query, check_coverage as _kb_cov
from cielingo_core.bridge.agent_client import analyze as _agent_analyze, health as _agent_health
from cielingo_core.bridge.phasenav_learning_bridge import PhaseNavLearningBridge
from cielingo_core.consolidation.consolidator import consolidate_experiences


class CIELingoSelfCycle:
    def __init__(self, state: CIELingoStateEngine | None = None):
        self.state = state or CIELingoStateEngine()
        self._cycle_count = 0
        self._last_review = 0.0
        self._last_insight = 0.0
        self._last_maintenance = 0.0
        self._last_phasenav_scan = 0.0
        self._last_repair_apply = 0.0
        self._last_consolidation = 0.0
        self._agent_ok = _agent_health()
        self._pn_bridge = PhaseNavLearningBridge(state=self.state)

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

        # 3. PhaseNav scar scan — every 60s (szukaj ścieżek naprawczych przez PhaseNav)
        if now - self._last_phasenav_scan > 60.0:
            self._last_phasenav_scan = now
            pn_result = self._pn_bridge.scan_scars_via_phasenav()
            if pn_result.get("scanned") and pn_result.get("n_repair_paths", 0) > 0:
                report["phasenav_repair_paths"] = pn_result["n_repair_paths"]
                report["actions"].append({"action": "phasenav_scar_scan", "paths": pn_result["n_repair_paths"]})

        # 4. Self-metric update
        self._update_self_metrics()

        # 5. Insight generation — every 120s (wzbogacone o PhaseNav)
        if now - self._last_insight > 120.0:
            self._last_insight = now
            insight = self._generate_insight()
            if insight:
                report["insight"] = insight
                report["actions"].append({"action": "generate_insight"})

        # 6. Agent health check — every 60s
        if now - self._last_maintenance > 60.0:
            self._last_maintenance = now
            self._agent_ok = _agent_health()
            report["agent_ok"] = self._agent_ok

        # 7. Apply repairs — every 90s
        if now - self._last_repair_apply > 90.0:
            self._last_repair_apply = now
            apply_result = self._apply_repairs()
            if apply_result.get("applied", 0) > 0:
                report["repairs_applied"] = apply_result
                report["actions"].append({"action": "apply_repairs", **apply_result})

        # 8. Consolidate experiences — every 300s
        if now - self._last_consolidation > 300.0:
            self._last_consolidation = now
            cons_result = consolidate_experiences(self.state,
                                                  max_age_hours=48.0,
                                                  decay_factor=0.15,
                                                  min_salience=0.2)
            if cons_result.get("n_decayed_experiences", 0) > 0 or cons_result.get("n_decayed_weights", 0) > 0:
                report["consolidation"] = cons_result
                report["actions"].append({"action": "consolidate", **cons_result})

        self.state.update_metric("cycle_count", float(self._cycle_count))
        self.state.update_metric("last_cycle_time", now)
        return report

    def _apply_repairs(self) -> dict:
        pending = self.state.get_pending_repairs()
        if not pending:
            return {"applied": 0, "reason": "no_pending"}
        applied = 0
        skipped = 0
        for repair in pending[:5]:
            scar_id = repair.get("scar_id", "")
            loop_id = repair.get("loop_id", "")
            confidence = repair.get("confidence", 0.0)
            if confidence < 0.6:
                skipped += 1
                continue
            resolution = repair.get("route_kind", "auto_resolved")
            self.state.resolve_scar(scar_id, resolution,
                                    f"auto-applied via self_cycle: {repair.get('description', '')[:128]}")
            self.state.resolve_repair(repair["repair_id"], "applied",
                                      f"scar {scar_id[:16]} → {resolution}")
            if loop_id:
                self.state.update_loop_state(loop_id, "closed", closure_score=0.85)
            self.state.log_experience("repair_applied", "self_cycle",
                                      f"Applied repair: {resolution} for scar {scar_id[:16]}",
                                      f"loop={loop_id} confidence={confidence:.2f}",
                                      salience=confidence)
            applied += 1
        return {"applied": applied, "skipped": skipped, "total_pending": len(pending)}

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

        # 2b. PhaseNav enrichment — dodaj operator signature do analizy
        pn_learned = self._pn_bridge.enrich_and_learn(text, source=source)
        if pn_learned.get("enriched"):
            self.state.log_experience(
                "phasenav_enrichment", source,
                f"PhaseNav enriched: op={pn_learned['operator_id']} "
                f"fp={pn_learned.get('harmonic_fingerprint', '?')} mass={pn_learned['semantic_mass']:.4f}",
                salience=pn_learned["semantic_mass"],
            )

        # 3. Build CIELingo meaning loop from analysis + knowledge
        from cielingo_core.meaning.meaning_loop import MeaningLoop, LoopState, SemanticScar, SemanticScarType
        from cielingo_core.meaning.repair_routing import route_repairs_for_meaning_loop
        from cielingo_core.global_layer.meaning_signal_bridge import build_global_meaning_signal

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

        closure = max(0.0, min(1.0, 1.0 - cov.get("score", 0.0) * 0.5))
        loop = MeaningLoop(
            loop_id=f"self_{source}_{int(time.time())}",
            input_ref=text[:64], response_ref=None,
            loop_state=LoopState.CLOSED if not scars else LoopState.SCARRED,
            closure_score=closure,
            contradiction_score=0.0, residue_score=cov.get("score", 0.0) * 0.3,
            return_required=bool(scars), scars=scars,
            noema_writeback_allowed=closure >= 0.85 and not scars,
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

        result = {
            "analysis": {"themes": analysis.get("themes", []), "affect": analysis.get("affect", "calm"),
                         "anchors": analysis.get("anchor_terms", []), "hunch": analysis.get("hunch", "")},
            "coverage": {"score": cov.get("score", 0), "covered": cov.get("covered", False)},
            "docs": [{"filename": d["filename"], "themes": d["themes"], "similarity": d["similarity"]} for d in docs[:5]],
            "loop_state": loop.loop_state.value,
            "scars": len(scars),
        }
        if pn_learned.get("enriched"):
            result["phasenav"] = {
                "operator_id": pn_learned["operator_id"],
                "harmonic_fingerprint": pn_learned.get("harmonic_fingerprint", "?"),
                "semantic_mass": pn_learned["semantic_mass"],
            }
        return result

    def surface_state(self) -> dict[str, Any]:
        return {
            "cycle": self._cycle_count,
            "agent_ok": self._agent_ok,
            "unresolved_scars": len(self.state.get_scars(unresolved_only=True)),
            "pending_repairs": len(self.state.get_pending_repairs()),
            "metrics": self.state.get_all_metrics(),
            "learning": self._learning_metrics(),
        }

    def _learning_metrics(self) -> dict:
        db = self.state._db()
        total_exp = db.execute("SELECT COUNT(*) FROM experience_log").fetchone()[0]
        cons_exp = db.execute("SELECT COUNT(*) FROM experience_log WHERE consolidated=1").fetchone()[0]
        total_repairs = db.execute("SELECT COUNT(*) FROM repair_candidates").fetchone()[0]
        applied_repairs = db.execute(
            "SELECT COUNT(*) FROM repair_candidates WHERE status='applied'").fetchone()[0]
        return {
            "total_experiences": total_exp,
            "consolidated_experiences": cons_exp,
            "consolidation_rate": round(cons_exp / max(total_exp, 1), 3),
            "total_repair_candidates": total_repairs,
            "applied_repairs": applied_repairs,
            "repair_application_rate": round(applied_repairs / max(total_repairs, 1), 3),
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

        # Learning effectiveness: how many resolved scars stayed resolved
        recent_cutoff = time.time() - 86400
        reverted = db.execute(
            "SELECT COUNT(*) FROM scars WHERE resolved_at IS NOT NULL AND resolved_at > ?",
            (recent_cutoff,),
        ).fetchone()[0]
        self.state.update_metric("learning_effectiveness_24h",
                                  float(reverted / max(resolved, 1)))

        # Model update count
        update_count = self.state.get_metric("model_update_count", 0)
        self.state.update_metric("model_update_count", float(update_count))

    def _generate_insight(self) -> str | None:
        scars = self.state.get_scars(unresolved_only=True)
        loops = self.state.get_metric("total_loops", 0)

        # PhaseNav status
        pn_count = self._pn_bridge.count()
        pn_concepts = pn_count.get("concepts", 0)
        pn_edges = pn_count.get("edges", 0)

        if not scars and loops > 0:
            if pn_concepts > 0:
                return f"All scars resolved. PhaseNav active: {pn_concepts} concepts, {pn_edges} edges."
            return "All scars resolved. CIELingo state is clean."
        if len(scars) > 10:
            return f"Scar accumulation: {len(scars)} unresolved. PhaseNav scan recommended."
        scar_types: dict[str, int] = {}
        for s in scars:
            scar_types[s["scar_type"]] = scar_types.get(s["scar_type"], 0) + 1
        if scar_types:
            dominant = max(scar_types, key=scar_types.get)
            pn_hint = f" PhaseNav: {pn_concepts} concepts." if pn_concepts > 0 else ""
            return f"Dominant scar: {dominant} ({scar_types[dominant]}/{len(scars)}).{pn_hint}"
        return None
