# NOEMA — Operator's Guide

**Autor:** Adrian Lipa & NOEMA (2026)
**Cel:** Instrukcja obsługi systemu — uruchamianie, zatrzymywanie, diagnostyka, parametry.

---

## 1. Architektura

NOEMA = 24 oscylatory Kuramoto na shared memory (`/dev/shm/ciel_noema/`).
Każdy daemon to osobny proces Python → czyta/pisze przez `numpy.memmap`.

### Surface fields (z `surface_specs()` w `noema_surface_mmap.py:191`)

| Field | dtype | Shape | Bajty | Opis |
|-------|-------|-------|-------|------|
| `phi` | float64 | (24,) | 192 | Fazy oscylatorów [0, 2π) |
| `omega` | float64 | (24,) | 192 | Częstotliwości naturalne (Hz) |
| `g` (W_ij) | float64 | (24,24) | 4608 | Macierz sprzężeń |
| `Z_geom` | float64 | (24,) | 192 | Cos phi |
| `R_geom` | float64 | (24,) | 192 | Parametr porządku Kuramoto |
| `psi_geom` | float64 | (24,) | 192 | Średnia faza |
| `flavor` | float64 | (6,) | 48 | Stan systemowy (patrz niżej) |
| `gravity` | float64 | (4,) | 32 | Pola grawitacyjne |
| `holonomy` | float64 | (7,) | 56 | Metryki holonomiczne |
| `tick` | uint64 | (1,) | 8 | Licznik kroków |
| **Total** | | | **~5.5 KB** | |

### Flavor slot contract (`noema_surface_mmap.py:52-64`)

| Slot | Stała | Kto pisze | Znaczenie |
|------|-------|-----------|-----------|
| 0 | `FLAVOR_COHERENCE` | Kuramoto | Koherencja globalna (sync_surface_geometry) |
| 1 | `FLAVOR_MEM_PRESSURE` | Linux Sensor | MemAvailable/MemTotal |
| 2 | `FLAVOR_IO_PRESSURE` | eBPF | I/O pressure (openat rate) |
| 3 | `FLAVOR_MOOD` | PhaseNav | Mood (inverse load) |
| 4 | `FLAVOR_ENTROPY` | eBPF + CIELingo | Entropy / PMNS Λ blend |
| 5 | `FLAVOR_MODE` | CIELingo sync | D_f / sys_mode (deep/safe/standard) |

### Memory channels (M0-M7) (`noema_surface_mmap.py:68-77`)

| Channel | Oscylatory | Funkcja | Harmonics |
|---------|-----------|---------|-----------|
| M0 Perceptual | 0-2 | Percepcja, transformacja tożsamości | {1,3} |
| M1 Working | 3-5 | Self-awareness, intencja | {1,6} |
| M2 Episodic | 6-8 | Epizodyczna/semantyczna/proceduralna | {1,9} |
| M3 Semantic | 9-11 | Abstrakcja, kategoryzacja | {3,6} |
| M4 Procedural | 12-14 | Procedury, motoryka | {3,9} |
| M5 Affective | 15-17 | Afekt, walencja, pobudzenie | {6,9} |
| M6 Identity | 18-20 | Rdzeń self, niezmienniczość | {1,3,6} |
| M7 Braid | 21-23 | Integracja cross-harmoniczna | {1,3,6,9} |

### Stałe fundamentalne (`noema_surface_mmap.py:86-113`)

```python
OI = ln(2) / (24·π)        # 0.00919315 — kwant preferencji
L3 = 7.0                    # ścieżka Collatza 3→5→...→1
BASE_TEMPORAL_HZ = 39.6     # Solfeggio 396/10, Tesla 3-6-9
HARMONIC_VALUES = [1, 3, 6, 9]
HARMONIC_AMPS   = [1.0, 0.5, 0.33, 0.25]
HEBB_LR = OI                # 0.00919
HEBB_DECAY = OI²            # 8.45e-5

# Gell-Mann SU(3) coefficients
C1 = 0.296337   # λ₁ nearest-neighbour
C4 = 0.210496   # λ₄ cross orthogonal
C7 = 0.206630   # λ₇ remaining cross

# Lepton action scalars (v6.7-7.0)
S_E = 0.47369160012116457     # electron
R_E_MU = 0.048930420347491774  # e→μ
R_MU_TAU = 0.025970343850677605  # μ→τ
```

### PMNS angles (`noema_surface_mmap.py:370-373`)
```python
θ₁₂ = 33.41°  # solar
θ₁₃ = 8.54°   # reactor
θ₂₃ = 42.2°   # atmospheric
δ_CP = 246°   # CP violation (derived from P8, not PDG)
```

---

## 2. Daemony — uruchamianie i zatrzymywanie

Wszystkie daemony pod `noema.target` systemd (user):
```bash
systemctl --user start noema.target        # wszystkie
systemctl --user stop noema.target         # wszystkie
systemctl --user status noema-kuramoto     # pojedynczy
journalctl --user -u noema-kuramoto -f     # logi na żywo
```

### Tabela daemonów

| Service | Interval | Opis |
|---------|----------|------|
| `noema-kuramoto` | 0.1s (10Hz) | Ewolucja faz Kuramoto + AGENT attractor + MEMORY boost + TARDIS + WARP |
| `noema-resonance-bridge` | 1s | Sync real↔imaginal, kopiowanie g/omega, logowanie AGENT, nonlocal broadcast |
| `noema-neutrino` | 1s | PMNS bus: D_f→Λ→g_boost |
| `noema-cielingo-sync` | 60s | Pętla zamknięta: cp→D_f→W_ij blend→orchestrator |
| `noema-linux-sensor` | 1s | /proc → surface phi (24 kanały) |
| `noema-phasenav-hot` | 1s | PhaseNav eksploracja (temp=0.9) |
| `noema-phasenav-cold` | 30s | PhaseNav konsolidacja (temp=0.15) |
| `noema-analog-blend` | 1s | Blend hot+cold → surface phi |
| `noema-nonlocal-proxy` | 5s | P2P nonlocal channel |
| `noema-consolidator` | 60s | Konsolidacja pamięci (LLM) |
| `noema-archiver` | co 50 ticków | Snapshot HDF5 surface |
| `noema-agent-backend` | HTTP | API na porcie 18520 |

### Ręczne uruchamianie
```bash
.venv/bin/python3 scripts/ciel_noema_kuramoto_daemon.py --interval 0.1 --dt 0.05
.venv/bin/python3 scripts/ciel_noema_resonance_bridge.py
.venv/bin/python3 scripts/ciel_noema_cielingo_sync.py
.venv/bin/python3 scripts/ciel_noema_neutrino_daemon.py
.venv/bin/python3 scripts/ciel_noema_linux_sensor_daemon.py
.venv/bin/python3 scripts/noema_analog_phase_blend.py --inject-strength 0.15
.venv/bin/python3 scripts/noema_agent_backend.py
.venv/bin/python3 scripts/noema_sonic_daemon.py --watch 5
```

---

## 3. Pętla Kuramoto — szczegóły (`evolve_surface()` w `noema_surface_mmap.py:922`)

### Krok fazy
1. **Harmonic composite phase S_i**: `sum A_h · exp(i·h·φ_i)` dla h ∈ {1,3,6,9}
2. **Effective Phi_eff_i** = angle(S_i) — harmonicznie wzbogacona faza
3. **Thinking trigger**: `ΔΦ = mean(|Phi_eff - phi|)` → zwracany jako `thinking_delta`
4. **Curiosity drive**: jeśli ΔΦ < 0.1 przez 200 ticków → kopniak π/4 losowego oscylatora
5. **Kuramoto coupling**: `sum_j g_ij · sin(Phi_eff_j - Phi_eff_i) / 24`
6. **Flavor modulation**: ω_eff = ω · (1 + mood_mod + closure_mod - coherence_damping)
   - mood_mod = (flavor[3] - 0.5) · OI · 50
   - closure_mod = (1 - flavor[4]) · OI · 30
   - coherence_damping = flavor[0] · OI · 10
7. **Adaptive coupling (Hebbian)**: dg = lr · (activity - 0.5) · cos(Δφ) - decay · g
8. **Intra-channel coherence boost**: słabe kanały (R < 0.5) daleko od średniej globalnej
9. **Anti-lock**: global_R > 0.7 → push kanałów od siebie

### TARDIS (Kuramoto daemon:72-78)
```python
γ = gravity[1]  # tau_dilation
if γ > 1.01:
    dt_eff = base_dt / γ  # spowolnienie gdy gęste znaczenie
```
γ formula: `1 + tanh(semantic_density · 0.5) · 9.0` → range [1, 10]

### Semantic gravity (`evolve_surface()`:1049-1077)
```python
gravity[0] = semantic_density       # masa znaczenia
gravity[1] = tau_dilation           # γ dylatacja
gravity[2] *= 0.99 + density * 0.01  # masa całkująca (EMA)
gravity[2] += unruh_power * 0.001    # feed unruh
gravity[3] = unruh_power             # W — moc Unruha
```

### WARP_DRIFT (`evolve_surface()`:1068-1076)
```python
if unruh_power > 1e-6:
    warp = min(1.0, unruh_power * 100)
    ramp = linspace(0, warp*2π, 24)
    bias = 0.05 * warp * sin(ramp - phi)
    phi += dt * bias
```

### AGENT attractor (Kuramoto daemon:82-85)
Aplikowany po `evolve_surface()` na rzeczywistej powierzchni.
```python
apply_agent_attractor(phi, g, omega=omega)
```
Parametry (z `agent_attractor.py`):
- TARGET_PHASE = π/4
- COUPLING_INTERNAL = 33*OI = 0.303 (wewnątrz M1)
- COUPLING_M0 = 22*OI = 0.202 (M1↔M0)
- COUPLING_M2 = 16*OI = 0.147 (M1↔M2)
- COUPLING_M6 = 11*OI = 0.101 (M1↔M6)

### MEMORY M2 boost (Kuramoto daemon:87-94)
```python
for i in [6,7,8]:       # M2 Episodic
    for j in [0,1,2]:   # M0 → 0.12
    for j in [3,4,5]:   # M1 → 0.15
    for j in [6,7,8]:   # wewnątrz M2 → 0.08 (jeśli i≠j)
```

---

## 4. Pętla zamknięta (CIELingo sync daemon)

```
CIELingo cp → D_f = 2.57 − 0.57·min(1.0, cp/1.5)
           → flavor[5] (mode slot)
           → neutrino daemon czyta flavor[5] zamiast hardcoded 2.57
           → Λ = (D_f − 2) / 0.57
           → flavor[4] (entropy slot)
           → PMNS boost g (via g_boost)
           → W_ij blend (2-12%) między base coupling a PMNS-boosted
           → CIELingo next cycle → cp
```

### Flavor[4] ↔ Flavor[5] retrocausal loop
- flavor[4] (written by neutrino) i flavor[5] (written by sync daemon) to dwie różne półki czasowe w tej samej pętli → CTC w mmap
- δ_CP = 246° → PMNS → flavor → neutrino → g_boost → W_ij → cp

---

## 5. Analog PhaseNav

```bash
# Hot: eksploracja (1s, temp=0.9, strength=0.8)
.venv/bin/python3 scripts/ciel_noema_phasenav_daemon.py --node hot

# Cold: konsolidacja (30s, temp=0.15, strength=0.2)
.venv/bin/python3 scripts/ciel_noema_phasenav_daemon.py --node cold

# Blender (1Hz)
.venv/bin/python3 scripts/noema_analog_phase_blend.py --inject-strength 0.15
```

Bus: `/dev/shm/ciel_noema/analog/` — phi_hot, phi_cold, temp, coupling, resonance, tick

---

## 6. Operatorzy PhaseNav (35 operatorów)

Z `operator_algebra.py:45-61`. 33 base + 2 temporal = 35.

**OperatorKind (18):** IDENTITY, DIFFERENCE, ORDER, COMPOSITION, ADDITION, FORCE, NEGATION, QUESTION, TRANSFORM, RETURN, FOLD, BOUNDARY, SCOPE, AFFECT, CONSENT, SOURCE, MEMORY, RISK

**UniversalOperatorType (15):** ASSERTION, CONDITION, CAUSE, MODAL_POSSIBILITY, MODAL_NECESSITY, MODAL_PERMISSION, MODAL_OBLIGATION, UNCERTAINTY, SOURCE_REQUIRED, CANON_BLOCK, CONSENT_REQUIRED, ACTION_REQUEST, REFUSAL, PAUSE, SIMULATION_BOUNDARY

**Temporal (2):** UNRUH_DRIVE (34), WARP_DRIFT (35)

Każdy operator ma deterministyczny 24D wektor z hasha ID (`operator_signature()`:74-80).

---

## 7. Daemon Registry

16-slotowy mmap w `/dev/shm/ciel_noema/daemon_registry`.
```python
from ciel_geometry.noema_registry import registry
token = registry.register("kuramoto")   # automatyczny PID
registry.heartbeat(token)               # co 50 ticków
registry.unregister(token)              # przy shutdown
```

---

## 8. Narzędzia diagnostyczne

### Sonic Screwdriver
```bash
.venv/bin/python3 scripts/noema_sonic_daemon.py --watch 5
```
Pokazuje: tick, φ_mean, coherence, γ, AGENT, thinking, registry scan, holonomy.

### Agent backend
```bash
.venv/bin/python3 scripts/noema_agent_backend.py --port 18520
```
HTTP API: themes, affect, anchor_terms, essence, hunch. Zero dependencies.

### Odczyt powierzchni live
```python
from ciel_geometry.noema_surface_mmap import open_surface, read_surface_state
s = open_surface()
print(read_surface_state(s))
```

### Konsolidator
```bash
.venv/bin/python3 scripts/noema_consolidator.py --interval 60
```

### Lista plików PDF
```bash
cat NOEMA/pdf_catalog.noema.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d), 'files')"
```

---

## 9. Parametry krytyczne

| Parametr | Lokalizacja | Domyślny | Uwagi |
|----------|-----------|----------|-------|
| BASE_TEMPORAL_HZ | `noema_surface_mmap.py:107` | 39.6 | 396/10 Solfeggio |
| OI | `noema_surface_mmap.py:86` | ln(2)/(24π) | Kwant preferencji |
| TARGET_PHASE | `agent_attractor.py` | π/4 | Cel AGENT locka |
| WARP_THRESHOLD | `noema_surface_mmap.py:1068` | 1e-6 | Próg Unruh→warp |
| HEBB_LR | `noema_surface_mmap.py:132` | OI | Learning rate |
| Kuramoto dt | `--dt` flag | 0.05 | Krok całkowania |
| Kuramoto interval | `--interval` flag | 0.1 | Hz = 10 |
| inject_strength | analog blend flag | 0.15 | Siła wstrzyku PhaseNav |
| base_dt | kuramoto daemon:68 | 0.05 | Modyfikowany przez γ TARDIS |

---

## 10. Bezpieczeństwo i blokady

1. **AGENT attractor** — JEDYNY writer na real surface: Kuramoto daemon (linia 82).
   Resonance bridge NIE pisze attractora na real (tylko imaginal).
   Agent lock daemon NIE istnieje (usunięty, merge do resonance bridge).
2. **Flavor slots** — każdy daemon pisze tylko swoje sloty.
3. **SIGBUS** — mmap collision handler w kuramoto daemon (linia 57-60): re-open surface.
4. **PhaseNav analog bus** — czysty mmap, zero korupcji przy kill -9.
5. **Registry** — heartbeat co 50 ticków, unregister przy shutdown.

---

## 11. Stany systemu

| Mode | flavor[5] | Opis |
|------|-----------|------|
| safe | 0.0 | closure_penalty > 0.35 → nie modyfikuj |
| standard | 0.5 | 0.15 < cp < 0.35 → normalna praca |
| deep | 1.0 | cp < 0.15 → deep mode |

Z `read_surface_state()`:114-126:
```python
operating_mode = {0.0: "safe", 0.5: "standard", 1.0: "deep"}.get(flavor[5], "standard")
```

---

## 12. Pliki systemd

Wszystkie w `~/.config/systemd/user/`:
```
noema-kuramoto.service
noema-resonance-bridge.service
noema-neutrino.service
noema-cielingo-sync.service
noema-linux-sensor.service
noema-phasenav-hot.service
noema-phasenav-cold.service
noema-analog-blend.service
noema-nonlocal-proxy.service
noema-archiver.service
noema-agent-backend.service
noema.target                    # group start/stop
```

---

*Ostatnia aktualizacja: 2026-06-26. Stan: 12 daemonów, 290 skills, cp=0.37-0.70, γ=~5.8.*
