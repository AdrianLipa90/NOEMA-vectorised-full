"""Experience consolidation — decay, aggregate, prune.

Reads from CIELingoStateEngine, never writes NOEMA/canon.
Only marks experience_log rows as consolidated and prunes old scars.
"""

from __future__ import annotations

import json
import time
from typing import Any

from cielingo_core.persistence.state_engine import CIELingoStateEngine


def consolidate_experiences(
    state: CIELingoStateEngine | None = None,
    max_age_hours: float = 48.0,
    decay_factor: float = 0.15,
    min_salience: float = 0.2,
) -> dict[str, Any]:
    state = state or CIELingoStateEngine()
    now = time.time()
    cutoff = now - max_age_hours * 3600

    db = state._db()

    # 1. Mark old, low-salience experiences as consolidated
    old_low = db.execute(
        "SELECT id, salience, summary FROM experience_log "
        "WHERE consolidated=0 AND timestamp<? AND salience<?",
        (cutoff, min_salience),
    ).fetchall()
    n_decayed = 0
    for row in old_low:
        db.execute("UPDATE experience_log SET consolidated=1 WHERE id=?", (row["id"],))
        n_decayed += 1

    # 2. Summarize recent high-salience experiences by event_type
    recent_high = db.execute(
        "SELECT event_type, COUNT(*) as count, AVG(salience) as avg_sal, "
        "MAX(timestamp) as last_ts FROM experience_log "
        "WHERE consolidated=0 AND salience>=? GROUP BY event_type",
        (min_salience,),
    ).fetchall()

    # 3. Decay operator weights if no recent activity
    metrics = state.get_all_metrics()
    n_decayed_weights = 0
    for key, value in metrics.items():
        if key.startswith("op_weight_") and value > 0.1:
            last_updated = db.execute(
                "SELECT updated_at FROM self_metrics WHERE metric=?", (key,)
            ).fetchone()
            if last_updated and (now - last_updated["updated_at"]) > max_age_hours * 3600:
                new_val = max(0.1, value - decay_factor)
                state.update_metric(key, new_val)
                n_decayed_weights += 1

    # 4. Update consolidation metrics
    state.update_metric("n_consolidated_experiences",
                        float(state.get_metric("n_consolidated_experiences", 0) + n_decayed))
    state.update_metric("last_consolidation_time", now)

    db.commit()

    return {
        "n_decayed_experiences": n_decayed,
        "n_decayed_weights": n_decayed_weights,
        "event_type_summary": [
            {"event_type": r["event_type"], "count": r["count"],
             "avg_salience": round(r["avg_sal"], 3), "last": r["last_ts"]}
            for r in recent_high
        ],
    }


__all__ = ["consolidate_experiences"]
