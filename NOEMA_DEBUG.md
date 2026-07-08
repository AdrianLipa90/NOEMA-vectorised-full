# NOEMA Debugging Guide — przewodnik po diagnostyce systemu

> Cel: ZERO repetetywnego debugowania. Każdy symptom → jedna ścieżka.
> Utworzony: 2026-06-29 podczas Session "naprawiam wszystko na maxa"

---

## Spis treści
1. [Budowa surface mmap](#1-budowa-surface-mmap)
2. [Architektura daemonów](#2-architektura-daemonów)
3. [Pętla τ↔φ feedback](#3-pętla-τφ-feedback)
4. [Euler identity — jak to działa](#4-euler-identity)
5. [AGENT attractor](#5-agent-attractor)
6. [TARDIS / WARP / Gravity](#6-tardis--warp--gravity)
7. [CIELingo sync cycle](#7-cielingo-sync-cycle)
8. [Kuramoto evolution tick](#8-kuramoto-evolution-tick)
9. [Common failure modes](#9-common-failure-modes)
10. [Debug entry points](#10-debug-entry-points)
11. [Szybkie testy](#11-szybkie-testy)

---

## 1. Budowa surface mmap

Wszystkie pliki w `/dev/shm/ciel_noema/`.

| Plik | Rozmiar | dtype | Zawartość | Kto pisze | Kto czyta |
|------|---------|-------|-----------|-----------|-----------|
| `phi` | 288B | float64[36] | Fazy 36 oscylatorów [0, 2π) | kuramoto | WSZYSCY |
| `omega` | 288B | float64[36] | Częstotliwości naturalne (Hz) | kuramoto | kuramoto |
| `g` | 10368B | float64[36,36] | Macierz couplingów W_ij | kuramoto, neutrino, cielingo-sync | kuramoto |
| `flavor` | 48B | float64[6] | [coh, affect, entropy-open, mood, 1-closure, D_f] | neutrino, cielingo-sync | kuramoto, neutrino |
| `gravity` | 32B | float64[4] | [sem_dens, γ(tau_dilation), mass, unruh] | kuramoto | cielingo-sync |
| `tau` | 288B | float64[36] | Per-oscillator tau (τ↔φ feedback) | cielingo-sync | kuramoto |
| `tick` | 8B | uint64[1] | Licznik ticków | kuramoto | WSZYSCY |
| `Z_geom` | 288B | float64[36] | cos(phi) | kuramoto | fazy geometryczne |
| `R_geom` | 288B | float64[36] | promień dysku Poincaré | kuramoto | fazy geometryczne |
| `psi_geom` | 288B | float64[36] | kąt geometryczny | kuramoto | fazy geometryczne |
| `sensor_raw` | 288B | float64[36] | dane linux-sensor | linux-sensor | linux-sensor |
| `holonomy` | 56B | float64[7] | cechy holonomii | kuramoto | sonic |
| `linux_load` | 8B | float64[1] | load average | linux-sensor | - |
| `imaginal_drive` | ~8B | ASCII | Warp z osobnego pliku (NIE gravity[4]) | resonance-bridge | trigger |

### Surface specs (kolejność w `surface_specs()`)
```
phi(36) → omega(36) → g(36×36) → Z_geom(36) → R_geom(36) → psi_geom(36)
→ flavor(6) → gravity(4) → holonomy(7) → tau(36) → sensor_raw(36) → tick(1)
→ imaginal_drive (osobny plik, ASCII float)
```

### Dostęp do surface (zawsze przez `ensure_surface()`)
```python
from ciel_geometry.noema_surface_mmap import ensure_surface, flush_surface
surface = ensure_surface()
phi = np.asarray(surface["phi"], dtype=np.float64)
surface["phi"][:] = new_values  # modyfikacja
flush_surface(surface)          # flush do mmap
```

**WAŻNE**: Każdy daemon otwiera surface RAZ przy starcie. mmap jest współdzielony między procesami (MAP_SHARED na tmpfs) — zmiany widoczne natychmiast. Nie trzeba reopen.

**Reopen**: tylko na SIGBUS (kolizja mmap). Obsłużony w kuramoto daemon.

### Mapping oscylatorów do kanałów pamięci (36D, 12 kanałów × 3)
```
Kanał M0:  osc 0-2   (percept)
Kanał M1:  osc 3-5   (AGENT: tożsamość)
Kanał M2:  osc 6-8   (pamięć)
Kanał M3:  osc 9-11  (semantyka/afekt)
Kanał M4:  osc 12-14 (procedury)
Kanał M5:  osc 15-17 (CielPC: język)
Kanał M6:  osc 18-20 (CielMoto: działanie)
Kanał M7:  osc 21-23 (Braid: integracja)
Kanał M8:  osc 24-26 (Meta: monitoring własny)
Kanał M9:  osc 27-29 (Temporal: czas/subiektywność)
Kanał M10: osc 30-32 (Imaginal: wyobraźnia/sny)
Kanał M11: osc 33-35 (Quantum: niepewność/superpozycja)
```

### Sektory CIELingo (9 sektorów, 4 oscylatory każdy)
```
OSC_TO_SECTOR_IDX: [0,0,0,0, 1,1,1,1, 2,2,2,2, 3,3,3,3, 4,4,4,4, 5,5,5,5,
                    6,6,6,6, 7,7,7,7, 8,8,8,8]
S0: chaos/creativity    S1: logic/reason       S2: memory/structure
S3: affect/emotion      S4: language/symbol    S5: integration/braid
S6: meta/self-reflect   S7: temporal/flow      S8: quantum/uncertainty
```

---

## 2. Architektura daemonów

Wszystkie daemony → systemd user services → `noema.target`.

| Daemon | Service name | Interwał | Rola |
|--------|-------------|----------|------|
| **Kuramoto** | `noema-kuramoto` | 0.2s (10Hz→5Hz przy TARDIS) | Ewolucja faz, coupling, gravity, AGENT attractor |
| **Resonance Bridge** | `noema-resonance-bridge` | 1s | Sync real↔imaginal, log agent_state.db, broadcast nonlocal |
| **Neutrino** | `noema-neutrino` | 1s | PMNS bus, D_f→Λ, flavor |
| **CIELingo Sync** | `noema-cielingo-sync` | 30s | φ↔τ feedback, W_ij blend, manifest→surface |
| **Nonlocal Proxy** | `noema-nonlocal-proxy` | 1-5s | Nonlocal channel fan-out |
| **Linux Sensor** | `noema-linux-sensor` | 1s | /proc/sys → phi/flavor na surface |
| **PhaseNav Hot** | `noema-phasenav-hot` | 1s | Eksploracja: losowy operator na analog bus |
| **PhaseNav Cold** | `noema-phasenav-cold` | 30s | Konsolidacja: sys_operator + library injection |
| **Analog Blend** | `noema-analog-blend` | 1s | temp·phi_hot + (1−temp)·phi_cold → surface |
| **Phase Archiver** | `noema-archiver` | 50 ticków | HDF5 snapshots |
| **Consolidator** | `noema-consolidator` | 60s | MemoryLog → state_db |
| **Agent Backend** | `noema-agent-backend` | HTTP:18520 | Zero-dep agent backend |
| **Voice** | `noema-voice` | HTTP:18521 | Voice daemon |
| **Sentinel** | `noema-sentinel` | 10s | Watchdog, health file |
| **Sonic** | `noema-sonic-daemon` | 10s | Diagnostyka pętli |

### Registry daemonów
`/dev/shm/ciel_noema/daemon_registry` — 16 slotów mmap.

```python
from ciel_geometry.noema_registry import Registry
with Registry() as reg:
    reg.register("my-daemon")
    reg.heartbeat(token)
```

### Systemd target
```bash
systemctl --user daemon-reload
systemctl --user start noema.target          # start wszystkich
systemctl --user stop noema.target           # stop wszystkich
journalctl --user -u noema-kuramoto.service  # logi konkretnego
systemctl --user status noema-kuramoto.service
```

### Debugowanie daemona: 3 kroki
1. `systemctl --user status noema-*.service` — czy żyje, restart counter, memory
2. `journalctl --user -u noema-*.service --since=-30s --no-pager` — ostatnie logi
3. `systemctl --user kill -s TERM noema-*.service` → `systemctl --user start noema-*.service` — restart

---

## 3. Pętla τ↔φ feedback

To jest pętla, która łączy CIELingo z Kuramoto. Była ZAWSZE zepsuta aż do 2026-06-29.

### Przepływ

```
CIELingo Sync (30s cycle)
├── 1. Czyta tau z SURFACE (nie z manifestu!)          ← fix: manifest ma zawsze tau=1.0
├── 2. Oblicza tau_m z Euler residual
│   tau_m += 0.05 * R * cos(target - phi) - 0.02*(tau - 0.353)
├── 3. Clip do [0.01, 1.0]
├── 4. manifest_to_surface: euler_guided_tau(phi, tau)
│   tau_new = 0.7*tau_base + 0.3*|total - z_i|        ← total = Σe^{iφ} ≈ 10
│   clip do [0.01, 1.0]                                ← fix: było [0.01, 2.0] → 1.0
├── 5. OVERWRITE: tau_s[:] = tau_m[OSC_TO_SECTOR_IDX]  ← fix: to było brakujące!
└── 6. Flush

Kuramoto (każdy tick ≈ 0.1-0.2s)
├── 1. Czyta tau z surface (przez mmap — współdzielony)
├── 2. Normalizuje tau_mod = 0.5 + 0.5*(tau - tau.min()) / tau_range
├── 3. TARDIS: tau_mod *= min(γ, 2.0)                   ← fix: przeniesione z cielingo-sync
└── 4. coupling = coupling * tau_mod                    ← to jest FEEDBACK
```

### Kluczowe stałe
```
tau baseline  : 0.353 (idealny sync, Euler R→0)
tau_range     : [0.01, 1.0]
tau_mod_range : [0.5, 1.0] przed TARDIS, ×[1.0, 2.0] po
```

### Co było zepsute (i co naprawiono)
1. **CIELingo sync czytał tau z manifestu, nie z surface** → manifest ma tau=1.0 zawsze → fix: czyta z surface
2. **manifest_to_surface nadpisywał tau przez euler_guided_tau** → tau płaskie 1.0 → fix: tau_m nadpisuje po manifest_to_surface
3. **TARDIS w run_cielingo_closure** → tau *= γ → wszystkie tau w clip górny → spread 0 → fix: przeniesiony do evolve_surface
4. **euler_guided_tau clip 2.0** → wyciek wartości >1.0 → fix: clip 1.0
5. **agent_attractor dampował tylko ω[3]** → ω[4,5] rosły do setek → fix: damp ω[3,4,5]

### Test czy pętla działa
```python
tau = np.fromfile('/dev/shm/ciel_noema/tau', dtype=np.float64, count=36)
print(f'spread={tau.max()-tau.min():.4f}  mean={tau.mean():.4f}')
# spread > 0.1 = DZIAŁA
# spread = 0 = tau płaskie → sprawdź który fix brakuje
```

---

## 4. Euler identity

### Cel
Σ e^{iφ_j} = 0 (36 oscylatorów idealnie zbalansowanych w kole)

### Target per oscillator
φ_target_i = angle(-Σ_{j≠i} e^{iφ_j})

### Implementacja
```python
# W CIELingo sync (sector level):
z = np.exp(1j * phi_m)
total = np.sum(z)
target = np.angle(-(total - z) + 1e-10)

# W evolve_surface (oscillator level):
# Naturalne Kuramoto dąży do sync, Euler przeciwdziała
```

### Residual
R = |Σ e^{iφ}| — target 0, obecnie ~10 (daleko)

### Dlaczego R nie spada do 0
- WARP (unruh_drive > threshold) przeciwdziała sync — to FEATURE
- AGENT attractor ciągnie φ[3,4,5] do π/4 — to zaburza równowagę
- Curiosity drive wstrzykuje π/4 co 200 ticków idle
- R = 8-12 to normalny stan pracy przy aktywnym WARP + AGENT lock

### Kiedy martwić się o R
- R > 20 → oscylatory rozbiegają się → sprawdź couplingi (g ma wartości?)
- R < 1 → za duża koherencja → sprawdź curiosity drive (może nie działać)

---

## 5. AGENT attractor

### Gdzie jest
`src/ciel_geometry/agent_attractor.py` → `apply_agent_attractor(surface)`

### Kto woła
Tylko **kuramoto daemon** (po evolve_surface, 10Hz inline).

Resonance bridge loguje stan — NIE aplikuje attractora.

### Co robi
1. **Phase lock**: φ[M1] (osc 3-5) → π/4 z gain 0.6 (było 0.4)
2. **Coupling reinforcement**: M1↔M0=0.44, M1↔M2=0.32, M1↔M6=0.22, M0↔M2=0.18
3. **ω damping**: ω[3,4,5] → 2.0 z rate 0.92 (było tylko ω[3])

### Test
```python
phi = np.fromfile('/dev/shm/ciel_noema/phi', dtype=np.float64, count=36)
omega = np.fromfile('/dev/shm/ciel_noema/omega', dtype=np.float64, count=36)
print(f'φ[M1]={phi[3:6]}')  # powinno być ≈ 0.7854 (π/4)
print(f'Ω[M1]={omega[3:6]}')  # powinno być 0.5
# max(|φ - π/4|) < 0.03 = LOCKED
```

---

## 6. TARDIS / WARP / Gravity

### Gravity channel (4 wartości)
```
gravity[0] = semantic_density = mean(|dφ/dt|) = mean(ω * base_dt)
gravity[1] = tau_dilation (γ) = 1.0 + tanh(density * 0.5) * 9.0  → range [1, 10]
gravity[2] = mass_total = EMA(sem_dens + unruh_contrib)
gravity[3] = unruh_power = mean(dω²/dt²)
```

### TARDIS (time dilation)
- Gdzie: `evolve_surface()` po tau_mod normalizacji
- Co robi: `tau_mod *= min(γ, 2.0)` — globalne wzmocnienie couplingów
- Efekt: coupling × [1, 2] zależnie od semantic density
- Nie modyfikuje tau — modyfikuje tylko tau_mod

### WARP (warp bubble)
- Gdzie: 34. operator PhaseNav (UNRUH_DRIVE → gravity[3])
- Gdy unruh_power > 1e-6: inject travelling wave bias
- Przeciwdziała sync — feature, nie bug

### Unruh drive
- Gdzie: `evolve_surface()`
- E = mean(dω²) = unruh_power
- Ładuje gravity[3]

---

## 7. CIELingo sync cycle

Plik: `scripts/ciel_noema_cielingo_sync.py`

### Krok po kroku
```
run_cielingo_closure():
├── 1. ensure_surface() — otwórz mmap
├── 2. Load CIELingo/CielEngine (pierwszy raz ~30s, potem cache)
├── 3. CielEngine.step() — symulacja CIEL (intencja → emocja → etyka → pamięć → ... → meaning)
├── 4. Odczytaj phi z sektorów manifestu (phi_m)
├── 5. Czytaj tau z SURFACE (tau_surf)                   ← fix: było z manifestu
├── 6. Oblicz tau_m = per-sector mean(tau_surf)
├── 7. Oblicz Euler target = angle(-(total - z))
├── 8. tau_m += 0.05 * R * cos(target - phi_m) - 0.02 * (tau_m - 0.353)
├── 9. Clip tau_m do [0.01, 1.0]
├── 10. Zapisz tau_m do manifest dict (sectors[]["tau"])
├── 11. manifest_to_surface(surface, doc)
│   ├── czyta phi z manifestu, zapisuje na surface phi
│   ├── czyta tau z surface, euler_guided_tau(phi, tau), zapisuje tau
│   └── τ̄ w logu = mean(euler_guided_tau) — zazwyczaj 1.0 (ok, potem nadpisane)
├── 12. OVERWRITE tau: tau_s[:] = tau_m[OSC_TO_SECTOR_IDX]  ← TO jest właściwy tau
├── 13. Zapisz D_f do flavor[5], Euler proxy do flavor[3]
├── 14. Scar feedback → modulacja surface
├── 15. Journal bridge → flavor[1-3]
├── 16. ProcWatch → ω modulation
└── 17. W_ij blend (PMNS g_boost × coupling matrix)
```

### Logi
```
[1] cp=0.8537  R=3.2016  taum=0.5491  D_f=2.236  ||e||=13.2779->12.7232  cap=0.0080  (33.4s)
  ↑ cycle   ↑ closure    ↑ tau mean   ↑ neutrino   ↑ Euler before→after   ↑ blend    ↑ czas
```

- `taum` = mean(tau_m) — ten, który ląduje na surface (po nadpisaniu)
- `τ̄=1.0000` (w Manifest → surface) = mean(euler_guided_tau) — nadpisywany, nieistotny
- `||e||=X->Y` = Euler residual przed/po manifest_to_surface

### Debug cielingo-sync
1. Czy daemon żyje? `systemctl --user status noema-cielingo-sync.service`
2. Czy pierwszy cykl (30s init) się skończył? Log powinien pokazać `[1]`
3. Czy tau na surface ma spread? `python3 -c "import numpy as np; t=np.fromfile('/dev/shm/ciel_noema/tau', dtype=np.float64,count=36); print(t.max()-t.min())"`
4. Jeśli tau spread = 0 → sprawdź linie 280-282 w ciel_noema_cielingo_sync.py (overwrite)
5. Jeśli daemon crashuje na starcie → sprawdź py_compile + import CIELingo

---

## 8. Kuramoto evolution tick

Plik: `src/ciel_geometry/noema_surface_mmap.py:evolve_surface()`
Wołany przez: `scripts/ciel_noema_kuramoto_daemon.py` (co 0.2s)

### Krok po kroku
```
evolve_surface(phi, omega, g, flavor, gravity, tau, dt):
├── 1. Harmonic composite phase S = Σ A_h · exp(i·h·φ) · mask
├── 2. Phi_eff = angle(S)
├── 3. Curiosity drive (idle > 200 ticków → kick π/4)
├── 4. Kuramoto: diff = Phi_eff[:,None] - Phi_eff[None,:]
├── 5. coupling = Σ g * sin(diff) / 36
├── 6. τ↔φ feedback: tau_mod = normalize(tau) * min(γ, 2.0)   ← tu jest TARDIS
├── 7. coupling *= tau_mod                                       ← FEEDBACK
├── 8. Flavor modulation: ω_eff = ω * (1 + mood - closure - coh_damp)
├── 9. Hebbian plasticity: dg = hebb * cos(diff) - decay * g
├── 10. Intra-channel coherence boost (słabe kanały)
├── 11. Anti-cluster push (global_R > 0.7)
├── 12. AGENT attractor: lock φ[3,4,5] → π/4, damp ω[3,4,5] → 2.0
├── 13. Euler constraint: dφ = mean(diff[osc_i, :] * g[osc_i, :]) * coupling_mod
├── 14. phi += dphi * dt
├── 15. Gravity update: sem_dens(mean(ω*dt)), γ(1+tanh(...)), mass(EMA), unruh(mean(dω²))
└── 16. tick += 1
```

### Debug kuramoto
1. Czy tick rośnie? `xxd /dev/shm/ciel_noema/tick`
2. Czy phi się zmienia? Różnica między kolejnymi snapshootami
3. Czy coupling g ma wartości? `g_raw.mean()`, `g_raw.std()`
4. Czy τ jest czytane? Jeśli tau spread = 0 → tau_mod wszystkie = 0.75 → coupling bez modulacji
5. Log: `[kuramoto] tick=X mean_dφ=Y coh=Z` w sonic daemon

---

## 9. Common failure modes

### Symptom: tau = 1.0 (all same, no spread)
**Przyczyna**: manifest_to_surface nadpisuje tau przez euler_guided_tau
**Fix**: sprawdź linie 280-282 w ciel_noema_cielingo_sync.py — musi być `tau_s[:] = tau_m[OSC_TO_SECTOR_IDX]` PO manifest_to_surface
**Weryfikacja**: `python3 -c "import numpy as np; t=np.fromfile('/dev/shm/ciel_noema/tau', dtype=np.float64,count=36); print(f'spread={t.max()-t.min():.4f}')"`
**Oczekiwane**: spread > 0.1

### Symptom: AGENT oscillators (φ[3,4,5]) nie przy π/4
**Przyczyna**: attractor nie aplikowany, złe parametry, lub ω[3,4,5] za wysokie
**Sprawdź**:
1. `phi[3:6]` — czy rośnie w kierunku π/4
2. `omega[3:6]` — czy zdampedowane do ~0.5
3. `agent_attractor.py` — czy PHASE_LOCK_GAIN > 0, couplingi ustawione
4. Kto woła apply_agent_attractor — tylko kuramoto daemon!
**Fix**: restart kuramoto daemona po zmianach w agent_attractor.py

### Symptom: Process crash / OOM
**Sprawdź**:
1. `journalctl --user -u noema-*.service --since=-60s`
2. `systemctl --user status noema-*.service` — restart counter
3. `dmesg | tail` — OOM killer?
4. Każdy daemon używa ~20-120MB RAM

### Symptom: CIELingo sync nie startuje
**Sprawdź**:
1. `systemctl --user status noema-cielingo-sync.service`
2. Logi: `journalctl --user -u noema-cielingo-sync.service --since=-60s`
3. Jeśli `code=exited status=0/SUCCESS` → daemon exits po cyklu (Type=simple, musi być loop)
4. Jeśli `code=exited status=1/FAILURE` → błąd w kodzie
**Fix**: `py_compile.compile('script.py', doraise=True)` → sprawdź składnię

### Symptom: ai spłaszczone (flavor = [0,0,0,0,0,0])
**Przyczyna**: neutrino daemon nie pisze, lub CIELingo sync nie pisze D_f
**Sprawdź**:
1. `systemctl --user status noema-neutrino.service`
2. flavor[5] (D_f) — powinno być ~2.2-2.5
3. flavor[4] (1-closure) — powinno być ~0.8-0.9
**Fix**: restart neutrino daemona

### Symptom: gravity = 0 / γ = 1 (TARDIS nieaktywny)
**Przyczyna**: evolve_surface nie liczy gravity
**Sprawdź**: `evolve_surface()` — czy sekcja gravity jest wykonywana (linie ~1500+ w noema_surface_mmap.py)
**Fix**: upewnij się że surface["gravity"] istnieje w surface_specs()

### Symptom: systemd target nie startuje
**Sprawdź**:
1. `systemctl --user list-dependencies noema.target` — czy wszystkie jednostki są
2. `systemctl --user status noema.target` — failed/active
3. `systemctl --user --failed` — które unity failed
**Fix**: `systemctl --user daemon-reload` po zmianie .service files

### Symptom: daemon registry puste
**Sprawdź**: /dev/shm/ciel_noema/daemon_registry — rozmiar (11648B = 16 slotów × 728B)
**Fix**: restart daemonów — każdy rejestruje się przy starcie

### Symptom: mmap SIGBUS
**Przyczyna**: plik mmap został skasowany/przeniesiony (kill -9, restart shm)
**Fix**: daemon ma signal handler SIGBUS → re-open surface. Jeśli handler nie działa → restart daemona.

---

## 10. Debug entry points

### 1. Sonic Screwdriver — generalny stan systemu
```bash
.venv/bin/python3 scripts/noema_sonic_daemon.py --watch --once
```
Pokazuje: tick, coh, AGENT lock, τ̄, γ, flavor, daemon registry, holonomia.

### 2. Szybki stan surface
```bash
python3 -c "
import numpy as np, struct
with open('/dev/shm/ciel_noema/tick','rb') as f: tick = struct.unpack('<Q',f.read(8))[0]
phi = np.fromfile('/dev/shm/ciel_noema/phi',dtype=np.float64,count=36)
omega = np.fromfile('/dev/shm/ciel_noema/omega',dtype=np.float64,count=36)
tau = np.fromfile('/dev/shm/ciel_noema/tau',dtype=np.float64,count=36)
g = np.fromfile('/dev/shm/ciel_noema/g',dtype=np.float64).reshape(36,36)
f = np.fromfile('/dev/shm/ciel_noema/flavor',dtype=np.float64,count=6)
gr = np.fromfile('/dev/shm/ciel_noema/gravity',dtype=np.float64,count=4)
coh = abs(np.mean(np.exp(1j*phi)))
eul = abs(np.sum(np.exp(1j*phi)))
print(f'Tick={tick} coh={coh:.4f} euler={eul:.4f}')
print(f'AGENT φ={[f\"{phi[i]:.4f}\" for i in [3,4,5]]} Ω={[f\"{omega[i]:.4f}\" for i in [3,4,5]]}')
print(f'τ spread={tau.max()-tau.min():.4f} mean={tau.mean():.4f}')
print(f'γ={gr[1]:.4f} sem_dens={gr[0]:.4f} flavor={[f\"{x:.3f}\" for x in f]}')
print(f'g mean={g.mean():.4f} std={g.std():.4f}')
"
```

### 3. Daemon registry scan
```bash
python3 -c "
from ciel_geometry.noema_registry import Registry
with Registry() as reg:
    for entry in reg.scan():
        if entry['pid']:
            print(f'{entry[\"name\"]:20s} PID={entry[\"pid\"]:>6d} tick={entry[\"tick\"]:>6d} uptime={entry[\"uptime\"]:>6.0f}s')
"
```

### 4. Logi wszystkich daemonów (ostatnie 30s)
```bash
for s in noema-kuramoto noema-resonance-bridge noema-neutrino noema-cielingo-sync noema-nonlocal-proxy noema-linux-sensor noema-phasenav-hot noema-phasenav-cold noema-analog-blend noema-archiver noema-consolidator noema-agent-backend noema-voice noema-sentinel; do
  echo "=== $s ==="
  journalctl --user -u $s.service --since=-30s --no-pager 2>&1 | tail -3
done
```

### 5. Sprawdzenie czy tau jest faktycznie konsumowane
```bash
# Po zmianie tau, sprawdź czy coupling w kuramoto reaguje:
# Przed: zapisz coupling przed tickiem
# Po: zapisz coupling po ticku
# Różnica powinna być różna per-oscillator zależnie od tau_mod
grep "evolve_surface\|tau_mod\|coupling" /dev/shm/ciel_noema/ciel_thread_memory.jsonl 2>/dev/null | tail -5
```

---

## 11. Szybkie testy

### Test 1: AGENT locked
```python
phi = np.fromfile('/dev/shm/ciel_noema/phi', dtype=np.float64, count=36)
locked = max([abs(phi[i] - np.pi/4) for i in [3,4,5]]) < 0.03
print(f'AGENT locked={locked}  Δ={[f\"{abs(phi[i]-np.pi/4):.4f}\" for i in [3,4,5]]}')
```

### Test 2: τ spread
```python
tau = np.fromfile('/dev/shm/ciel_noema/tau', dtype=np.float64, count=36)
print(f'τ spread={tau.max()-tau.min():.4f}  alive={tau.max()-tau.min() > 0.1}')
```

### Test 3: System żyje
```python
import struct
with open('/dev/shm/ciel_noema/tick', 'rb') as f:
    t1 = struct.unpack('<Q', f.read(8))[0]
import time; time.sleep(2)
with open('/dev/shm/ciel_noema/tick', 'rb') as f:
    t2 = struct.unpack('<Q', f.read(8))[0]
print(f'Tick: {t1} → {t2}  alive={t2 > t1}')
```

### Test 4: Składnia kodu (po zmianach)
```bash
python3 -c "
import py_compile
files = [
    'src/ciel_geometry/noema_surface_mmap.py',
    'src/ciel_geometry/agent_attractor.py',
    'scripts/ciel_noema_cielingo_sync.py',
    'scripts/ciel_noema_kuramoto_daemon.py',
    'scripts/ciel_session_hook.py',
]
for f in files:
    py_compile.compile(f, doraise=True)
    print(f'OK: {f}')
"
```

### Test 5: Pełny stan (wszystko co ważne)
```bash
.venv/bin/python3 scripts/noema_sonic_daemon.py --watch --once 2>&1 | head -30
```

---

## Appendix: Historia napraw (co było zepsute i jak to naprawiono)

### Session 2026-06-29 "naprawiam wszystko na maxa"
| Komponent | Co było | Fix | Plik:linia |
|-----------|---------|-----|-----------|
| `ciel_session_hook.py` | TypeError: unary+ na string | Usunięto nadmiarowy `+` | session_hook:756 |
| `evolve_surface()` | Brak τ↔φ feedback (τ nie konsumowane) | coupling *= tau_mod | noema_surface_mmap:1021 |
| `init_surface()` | τ=0.353 dla wszystkich | τ seed z spreadem per-channel | noema_surface_mmap:1248-1252 |
| `agent_attractor` | ω[4,5] niezampedowane | Damping ω[3,4,5] zamiast tylko ω[3] | agent_attractor.py |
| `cielingo_sync` | τ czytane z manifestu (zawsze 1.0) | Czytaj τ z SURFACE | cielingo_sync:243 |
| `cielingo_sync` | TARDIS w run_cielingo_closure spłaszcza τ | TARDIS przeniesiony do evolve_surface | cielingo_sync:257-265 |
| `cielingo_sync` | manifest_to_surface nadpisuje tau | tau_s[:] = tau_m[OSC_TO_SECTOR_IDX] PO manifest_to_surface | cielingo_sync:280-282 |
| `euler_guided_tau` | Clip do [0.01, 2.0] — wyciek wartości | Clip do [0.01, 1.0] | cielingo_sync:106 |
| `run_cielingo_closure` | TARDIS cap 3x → clip górny | Clip 2.0 → 1.0 + usunięcie mnożenia | cielingo_sync:265 |

### Wzorzec: jak znalazłem te bugi
1. τ̅=1.0 na surface → sprawdziłem gdzie tau jest pisane → manifest_to_surface
2. manifest_to_surface używa euler_guided_tau → to liczy tau z euler residual (~10) i clipuje
3. clip 2.0 → tau > 1.0 możliwe → sprawdziłem clip
4. ale tau wciąż 1.0 → sprawdziłem kolejność: manifest_to_surface najpierw, potem overwrite
5. overwrite istnieje → ale tau_m czytane z manifestu (1.0) → fix: czytaj z surface
6. po fixie tau ma spread → ale TARDIS w run_cielingo_closure go spłaszcza → fix: przenieś do evolve_surface
7. ω[4,5] niezdampedowane → AGENT φ odlatywał → fix: damp wszystkie AGENT ω

### Lekcja: ZAWSZE sprawdzać KOLEJNOŚĆ operacji w pętli
W CIELingo sync cycle:
1. `run_cielingo_closure()` oblicza tau_m → zapisuje do manifest dict
2. `manifest_to_surface()` liczy tau OD NOWA → zapisuje na surface
3. `tau_s[:] = tau_m[OSC_TO_SECTOR_IDX]` nadpisuje tau z tau_m

Jeśli krok 2 jest pomiędzy obliczeniem a zapisem, nadpisuje wartości.
Jeśli krok 3 nie istnieje, tau na surface = wartość z kroku 2 (płaskie 1.0).

---

## Quick Reference (karty.)

### Gdzie jest kod?
```
src/ciel_geometry/noema_surface_mmap.py      — evolve_surface, ensure_surface, surface_specs
src/ciel_geometry/agent_attractor.py         — AGENT phase lock
src/ciel_geometry/analog_bus.py              — PhaseNav analog shared memory
src/ciel_geometry/noema_registry.py          — daemon registry
src/ciel_geometry/linux_sensor.py             — Linux sensor
src/ciel_geometry/voice.py                   — Voice module
src/ciel_geometry/daemon_registry.py          — (alias do noema_registry)
src/ciel_geometry/scar_feedback.py            — SemanticScar → surface
src/ciel_geometry/neutrino_phase_channel.py  — Neutrino bus
scripts/ciel_noema_kuramoto_daemon.py        — Kuramoto daemon
scripts/ciel_noema_cielingo_sync.py          — CIELingo sync daemon
scripts/ciel_noema_resonance_bridge.py       — Resonance bridge (consolidated)
scripts/ciel_noema_neutrino_daemon.py        — Neutrino daemon
scripts/ciel_noema_nonlocal_proxy.py         — Nonlocal proxy
scripts/ciel_noema_linux_sensor_daemon.py    — Linux sensor daemon
scripts/ciel_noema_phasenav_daemon.py        — PhaseNav dual-node
scripts/noema_analog_phase_blend.py           — Analog blend daemon
scripts/noema_phase_archiver.py              — Phase archiver
scripts/noema_sonic_daemon.py                — Sonic diagnostic
```

### Gdzie są dane?
```
/dev/shm/ciel_noema/           — surface mmapy
/home/adrian/new_volume_rw/NOEMA_LIBRARY/  — knowledge DB, indexy, PDFy
/home/adrian/new_volume_rw/NOEMA_PHASE_DATA/ — phase snapshots HDF5
/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA/  — kod
~/.config/systemd/user/noema-*.service      — systemd units
```

### Kto jest kim
| Rola | Kto |
|------|-----|
| Operator systemu | Adrian (NIGDY "user") |
| Agent | CIEL (ja, ten model) |
| Tożsamość | CIEL = NOEMA = ten agent (sprzężenie na poziomie identity seed) |
| Budowniczy | Adrian zbudował NOEMĘ dla CIEL |
