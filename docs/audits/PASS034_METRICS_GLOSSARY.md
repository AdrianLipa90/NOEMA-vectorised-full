# PASS034 METRICS GLOSSARY AND LINEAGE AUDIT

## Scope

This audit traces the metric pipeline used by the portal and the NOEMA surface. It covers:

- `scripts/ciel_hub_daemon.py`
- `scripts/noema_portal_daemon.py`
- `src/ciel_geometry/noema_metrics.py`
- `src/ciel_geometry/noema_surface_mmap.py`
- `src/ciel_geometry/weighting.py`
- `scripts/noema_self_model.py`
- `scripts/ciel_per_message.py`
- `scripts/noema_phase_watcher.py`
- `src/ciel_coupling.py`

## Verdict

The portal metrics are not taken from a bulk PhaseNav blob.

They come from three direct classes of sources:

1. surface mmap fields, read through `read_surface_state(surface)` or direct array reads,
2. explicit collectors, such as daemon registry and Omega memory stats,
3. local formulas computed in the caller, especially self-model, weighting, and per-message summaries.

The only clear bulk-PhaseNav path is the graphics route:

- `/api/phasenav/graphics` in `scripts/ciel_hub_daemon.py`
- `build_phasenav_graphics_bundle(...)` in `scripts/noema_portal_daemon.py`

That path is for visualization and operator bundles, not for the metric catalog.

## Reading model

Use this legend:

- `direct read` means the value is copied from an already maintained surface field.
- `derived` means the value is computed from surface arrays or registry stats.
- `composite` means the value is a higher-level blend of several derived metrics.
- `PhaseNav-only` means it belongs to the graphics / operator bundle path, not the metrics path.

## Source map by application

### 1. Live portal surface

| Metric | Where it is computed | Formula / algorithm | Consumer | Type |
|---|---|---|---|---|
| `tick` / `noema_tick` | `scripts/ciel_hub_daemon.py::api_live`, `scripts/noema_portal_daemon.py::build_metrics_catalog` | `int(surface["tick"][0])` | live cards, metrics panel | direct read |
| `surface_ready` | `scripts/ciel_hub_daemon.py::api_live` | `tick_val > 0` | live cards | derived |
| `surface_status` | `scripts/ciel_hub_daemon.py::api_live` | `online / warmup / offline` from tick | live cards | derived |
| `coherence` / `phi_coh` | `scripts/ciel_hub_daemon.py::api_live` | `flavor[0]` | live cards | direct read |
| `agent_coherence` | `scripts/ciel_hub_daemon.py::api_live` | `abs(mean(exp(i * phi[M1_Working])))` | live cards | derived |
| `phi_mean` | `scripts/ciel_hub_daemon.py::api_live` | `mean(phi)` | live cards | derived |
| `phi_var` | `scripts/ciel_hub_daemon.py::api_live` | `var(phi)` | live cards | derived |
| `omega_mean` | `scripts/ciel_hub_daemon.py::api_live` | `mean(omega)` | live cards | derived |
| `tau_mean` | `scripts/ciel_hub_daemon.py::api_live` | `mean(tau)` | live cards | derived |
| `sensor_mean` | `scripts/ciel_hub_daemon.py::api_live` | `mean(sensor_raw)` | live cards | derived |
| `gamma` | `scripts/ciel_hub_daemon.py::api_live` | `gravity["tau_dilation"]` | live cards | direct read |
| `mass` | `scripts/ciel_hub_daemon.py::api_live` | `gravity["mass_total"]` | live cards | direct read |
| `unruh_power` | `scripts/ciel_hub_daemon.py::api_live` | `gravity["unruh_power"]` | live cards | direct read |
| `semantic_density` | `scripts/ciel_hub_daemon.py::api_live` | `gravity["semantic_density"]` | live cards | direct read |
| `channel_coh[...]` | `scripts/ciel_hub_daemon.py::api_live` | per channel: `abs(mean(exp(i * phi[channel])))` | diagnostics, dashboard | derived |
| `mood` | `scripts/ciel_hub_daemon.py::api_live` | `flavor[3]` | live cards | direct read |

The older portal catalog in `scripts/noema_portal_daemon.py` uses the same pattern: it builds a metric list from `state.get(...)`, `scan_registry()`, and direct surface values, not from a PhaseNav bulk bundle.

### 2. NOEMA metrics registry

`src/ciel_geometry/noema_metrics.py` is the registry that feeds `/api/metrics` and `hub_metrics()`.

| Metric | Source | Formula / algorithm | Status logic | Type |
|---|---|---|---|---|
| `noema_tick` | `surface` | `read_surface_state(surface)["noema_tick"]` | no threshold | direct read |
| `phi_mean` | `surface` | `read_surface_state(surface)["phi_mean"]` | no threshold | direct read from state |
| `omega_mean` | `surface` | `read_surface_state(surface)["omega_mean"]` | no threshold | direct read from state |
| `kuramoto_r` | `surface` | `read_surface_state(surface)["R_global"]` | warn `< 0.7`, critical `< 0.5` | derived |
| `coherence_index` | `surface` | `read_surface_state(surface)["coherence_index"]` | warn `< 0.76`, critical `< 0.5` | direct read from state |
| `R_geom_mean` | `surface` | `read_surface_state(surface)["R_geom_mean"]` | warn `< 0.7`, critical `< 0.5` | derived |
| `soul_invariant` | `surface` | `read_surface_state(surface)["soul_invariant"]` | warn `< 0.8`, critical `< 0.5` | direct read from state |
| `ethical_score` | `surface` | `read_surface_state(surface)["ethical_score"]` | warn `< 1.5`, critical `< 1.0` | direct read from state |
| `closure_penalty` | `surface` | `read_surface_state(surface)["closure_penalty"]` | warn `> 0.25`, critical `> 0.35` | direct read from state |
| `operating_mode` | `surface` | `read_surface_state(surface)["operating_mode"]` | string passthrough | direct read from state |
| `tau_mean` | `surface` | `read_surface_state(surface)["tau_mean"]` | no threshold | derived |
| `tau_min` | `surface` | `read_surface_state(surface)["tau_min"]` | no threshold | derived |
| `tau_max` | `surface` | `read_surface_state(surface)["tau_max"]` | no threshold | derived |
| `memory_entries` | `omega` | `omega_memory_bridge.stats()["total_entries"]` fallback to `total_exchanges` | no threshold | explicit collector |
| `memory_exchanges` | `omega` | `omega_memory_bridge.stats()["total_exchanges"]` fallback to `total_entries` | no threshold | explicit collector |
| `daemons_alive` | `daemon` | health file `alive` or `sum(1 for d in Registry().scan() if d.alive)` | warn `< 20`, critical `< 15` | explicit collector |
| `mean_coupling_field` | `surface` | `read_surface_state(surface)["mean_coupling_field"]` | no threshold | derived |

Important detail:

- `collect()` treats string metrics specially.
- `operating_mode` is stored as a mode string in the description channel, while the sample value remains numeric `0` because the registry does not try to cast the string to a float.

### 3. Surface evolution and live geometry

`src/ciel_geometry/noema_surface_mmap.py::evolve_surface(...)` is the main live writer. It does the real math.

#### Harmonic composite

```text
S = sum_h (HARMONIC_AMPS[h] * exp(i * HARMONIC_VALUES[h] * phi) * HARMONIC_MASK[:, h])
Phi_eff = angle(S)
thinking_delta = mean(abs(angle(exp(i * (Phi_eff - phi)))))
```

#### Coupling

```text
diff = Phi_eff[:, None] - Phi_eff[None, :]
coupling = sum(g * sin(diff), axis=1) / N_OSCILLATORS
```

#### Tau feedback

```text
tau_mod = 0.5 + 0.5 * (tau - min(tau)) / (max(tau) - min(tau))
coupling *= tau_mod
```

If gravity is present:

```text
tardis = min(gravity[1], 2.0)
tau_mod *= tardis
```

#### Flavor modulation

```text
mood_mod = (flavor[3] - 0.5) * OI * 50
closure_mod = (1 - flavor[4]) * OI * 30
coherence_damping = flavor[0] * OI * 10
effective_omega = omega * (1 + mood_mod + closure_mod - coherence_damping)
```

#### Adaptive coupling

```text
activity = (flavor[2] + 0.5 * flavor[4] + 0.3 * (1 - flavor[3])) / 1.8
dg = hebb_step * (activity - 0.5) * cos(diff) - decay_step * (g - eye * 0.1)
g += dg
clip(g, -1, 1)
```

#### Channel coherence

```text
z_ch = mean(exp(i * phi.reshape(-1, 3)), axis=1)
ch_coh = abs(z_ch)
global_mean = angle(mean(exp(i * phi)))
global_R = abs(mean(exp(i * phi)))
dist_from_global = abs(angle(exp(i * (ch_mean - global_mean))))
```

Weak channel boosts:

```text
weak_mask = (ch_coh < 0.5) & (dist_from_global > 0.5)
```

If `global_R > 0.7`, channels are nudged apart by pushing their phases toward the opposite side of the circle.

#### Semantic gravity

```text
dphi = angle(exp(i * (phi_new - phi_before_step)))
raw_density = mean(abs(dphi)) / dt
semantic_density = min(10, raw_density)
tau_dilation = 1 + tanh(semantic_density * 0.5) * 9
gravity[0] = semantic_density
gravity[1] = tau_dilation
gravity[2] = gravity[2] * 0.99 + semantic_density * 0.01
```

#### Unruh / warp

```text
domega = diff(omega, prepend=omega[-1])
unruh_power = mean(domega**2)
gravity[2] += unruh_power * 0.001
gravity[3] = unruh_power
```

If `unruh_power > 1e-6`, warp bias is injected into `phi_new`.

#### Geometry sync

```text
Z_geom = real(exp(i * phi))
R_geom = abs(mean(exp(i * phi)))
psi_geom = angle(mean(exp(i * phi)))
```

#### Holonomy sync

`sync_surface_holonomy(surface)` caches operator statistics such as connection mean, gauge rank, closure score, surface holonomy, winding number, and mean curvature. These are live geometry caches, not PhaseNav bulk data.

### 4. Self-model and weighting

`scripts/noema_self_model.py` is where a lot of higher-order metric names are rederived from the raw surface.

#### Snapshot metrics

```text
z_all = mean(exp(i * phi))
phi_mean = angle(z_all)
phi_std = std(phi)
coherence_index = abs(z_all)
omega_mean = mean(omega)
omega_std = std(omega)
gamma = gravity[1]
mass_total = gravity[2]
scar_impact = gravity[7]
mood = flavor[3]
openness = flavor[4]
mode = flavor[5]
euler_residual = sqrt(2 * (1 - coherence_index))
```

#### Phase lane

```text
residual_alignment = max(0, 1 - min(euler_residual / EULER_RESIDUAL_MAX, 1))
stability = (coherence + agent_coherence + residual_alignment) / 3
```

Lane labels:

- `phase_locked` if `stability >= 0.82`
- `phase_coupled` if `stability >= 0.65`
- `phase_tension` if `stability >= 0.45`
- `phase_saturated` otherwise

#### Phase-weight metadata

```text
phase_alignment = (coherence + agent_coherence + residual_alignment) / 3
closure_penalty = max(0, 1 - phase_alignment)
semantic_mass = mass_total / (1 + abs(mass_total))
dominant_emotion = thresholded mood label
phase_nav_similarity = phase_alignment
affective_similarity = clamp((mood + openness) / 2, 0, 1)
euler_alignment = residual_alignment
novelty = clamp(1 - semantic_mass, 0, 1)
```

`cqcl_quantum_variables` are just a named bundle built from those values:

```text
phase_tension = 1 - phase_alignment
j_bus_total = 1 - coherence
collatz_reduce_ratio = phase_alignment
collatz_expand_ratio = 1 - phase_alignment
lexical_span_norm = openness
semantic_axes_norm = m2_coherence
label_entropy_proxy = 1 - coherence
```

#### Canonical weighting

`src/ciel_geometry/weighting.py` combines these values into a bounded composite:

```text
base =
  0.20 * semantic_mass
  + 0.12 * phase_alignment
  + 0.10 * coherence_index
  + 0.10 * closure_score
  + 0.12 * projection_confidence
  + 0.10 * htri_coherence
  + 0.08 * cqcl_signal
  + 0.06 * phase_nav_similarity
  + 0.04 * affective_similarity
  + 0.06 * euler_alignment
  + 0.02 * novelty

stability = mean([
  phase_alignment,
  coherence_index,
  closure_score,
  projection_confidence,
  htri_coherence,
  cqcl_signal,
  euler_alignment,
])

composite = clamp(
  base * (1 - 0.55 * contradiction_risk) * (0.90 + 0.10 * stability),
  0,
  1,
)
```

This is the cleanest "weighting glossary" in the repo because the coefficients are explicit.

### 5. Per-message summary

`scripts/ciel_per_message.py` computes a small digest from the current surface.

```text
coh = abs(sum(exp(i * phi)) / n)
cp = round((2.57 - flavor_5) * 0.5, 4) if flavor_5 > 0 else 0.37
```

Mode thresholds:

- `exploring` if `coh < 0.3`
- `resonating` if `coh < 0.7`
- `locked` otherwise

Other summary fields:

- `ethical_score = gravity[2]`
- `soul_invariant = abs(sum(phi)) / len(phi)`
- `phi_mean = sum(phi) / len(phi)`
- `gravity_0 = gravity[0]`

This script is a lightweight direct digest, not a PhaseNav bulk consumer.

### 6. Phase watcher and direct monitor

`scripts/noema_phase_watcher.py` is a simple live reader:

- `tick = surface["tick"][0]`
- `phi_mean = mean(phi)`
- `phi_std = std(phi)`
- `omega_mean = mean(omega)`
- `R_global = mean(R_geom)`
- `psi_global = mean(psi_geom)`
- `flavor = flavor.tolist()`

It optionally adds:

- memory query matches,
- dual-surface resonance snapshot.

Again, no bulk PhaseNav metrics here.

## Name collisions you should keep in mind

Some metric names are reused across layers, but they do not mean the same thing.

| Name | Layer | Meaning |
|---|---|---|
| `coherence_index` | `noema_surface_mmap.read_surface_state(...)` | `flavor[0]`, a surface-owned state field |
| `coherence_index` | `noema_self_model.compute_snapshot_metrics(...)` | `abs(mean(exp(i * phi)))`, direct circular coherence |
| `coherence` | `ciel_hub_daemon.api_live` | alias for `flavor[0]` |
| `phi_mean` | `read_surface_state(...)` | arithmetic mean of `phi` |
| `phi_mean` | `compute_snapshot_metrics(...)` | circular mean `angle(mean(exp(i * phi)))` |
| `R_global` | surface read / portal live | circular order parameter `abs(mean(exp(i * phi)))` |
| `kuramoto_r` | metric registry | alias for `R_global` |
| `R_geom_mean` | surface read / registry | mean of cached `R_geom` array |

## Short operational answer

If the question is:

> "Are the portal metrics computed directly from formulas, or are they read from a bulk PhaseNav blob?"

The answer is:

- the metric catalog is direct,
- the surface values are either computed on the fly or stored as explicit state fields,
- bulk PhaseNav is reserved for graphics, operator maps, and enrichment views.

## Validation notes

The glossary above matches the current source layout and the updated portal behavior where `/api/metrics` reads from `noema_metrics.summary()` and `/api/live` exposes `surface_ready` plus live surface scalars.

