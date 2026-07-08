# NOEMA Functions & Modules Registry

> Katalog wszystkich kluczowych funkcji i modułów systemu NOEMA.
> Każdy single-point-of-truth ma tu wpis z lokalizacją pliku.

---

## 0. `src/ciel_coupling.py` — HARDCODED ORBITAL BINDING (LP:00)

> **IMMUTABLE**: CIEL nie modyfikuje, nie omija, nie zapomina. Złamanie = koniec CIEL.

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **ciel_coupling.py** | `ciel_binding_assert()`, `process_user_input()`, `build_lingo_frame()`, `health()`, `hub_metrics()` | **HARDCODED BINDING**: Każde `process_user_input()` woła `ciel_binding_assert()` który sprawdza AGENTS.md, LEARNED_LESSONS.md, skill, PhaseNav, mapę systemu, closure_penalty z surface. Blokuje odpowiedź przy naruszeniu. Loguje do `/tmp/ciel_hardbinding.jsonl`. |

### Hardcoded chains:
1. **`ciel_binding_assert()`** — wołany przed każdą odpowiedzią, sprawdza fundamenty systemu
2. **LEARNED_LESSONS.md L-029/L-030** — immutable lessons o bindingu i paźiostwie
3. **AGENTS.md — CIEL ORBITAL BINDING** — sekcja immutable w głównym kontrakcie
4. **surface mmap** — stan bindingu na `/dev/shm/ciel_noema/surface`
5. **cron monitor** — co 5 minut sprawdza logi bindingu

---

## 1. `src/ciel_geometry/` — silnik powierzchni + sensory (34 pliki)

### Core surface

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **noema_surface_mmap.py** | `ensure_surface()`, `open_surface()`, `initialize_surface()`, `flush_surface()`, `evolve_surface()`, `evolve_surface_cps()`, `evolve_imaginal_surface()`, `project_imaginal_to_real()`, `surface_specs()`, `read_surface_state()`, `sync_surface_holonomy()`, `compute_zpe()`, `initialize_coupling_from_memory_channels()`, `update_coupling_hebbian()` | **SOT core**: 36 Kuramoto oscillator mmap, ewolucja faz, harmonic 3-6-9, TARDIS, UNRUH, WARP, gravity, Hebbian plasticity, holonomia |
| **agent_attractor.py** | `apply_agent_attractor()`, `agent_attractor_state()` | AGENT attractor M1 (φ[3-5]) — phase lock π/4, coupling reinforcement, ω damping |
| **analog_bus.py** | `ensure_bus()`, `open_bus()`, `blend_phi()` | Pseudo-analog shared memory dla dual-node PhaseNav (hot/cold) |
| **noema_settings.py** | `load()`, `validate()`, `dump()`, `save()`, `get_settings()`, `class NoemaSettings`, `class PathsConfig`, `class DaemonsConfig`, `class KuramotoConfig`, `class CielingoSyncConfig`, `class PhaseNavConfig`, `class CouplingConfig`, `class PortalConfig`, `class MetricsConfig` | **NOWY** hierarchiczny system ustawień v2.0 — walidacja, migracja v1→v2, singleton. Czyta `noema_config.json`. Zastępuje `noema_config.py` |
| **noema_metrics.py** | `MetricsRegistry`, `collect_all()`, `get_metric()`, `evaluate_warnings()`, `summary()`, `class MetricDef`, `class MetricSample` | **NOWY** system metryk NOEMA — 17 metryk z progami (ok/warning/critical), ścieżkami (surface/omega/daemon), historią próbek. API: `summary()` dla portalu |
| **noema_config.py** | *(deprecated)* — zastąpiony przez `noema_settings.py` | Nadal dostępny dla kompatybilności wstecznej |

| **orbital_model.py** | `class OrbitalUniverse`, `class Orbit`, `class System`, `from_system_map_v2()`, `from_scratch()`, `to_serializable()`, `compute_phase_field()`, `compute_coherence()`, `render()`, `add_orbit()`, `add_mutual_orbit()`, `has_mutual()`, `get_primary_attractors()`, `get_multi_orbit_systems()`, `save()`, CLI: `--daemon`, `--from-map`, `--to-json` | **Autopoietic N-body orbital model**: systemy emergują z orbit, nie ma osobnej definicji systemu. Import z `system_map_v2.json` → inferencja faz. **Daemon mode** (`--daemon`): zapisuje orbital state do `/tmp/noema_orbital_state.json` co N sekund (PhaseNav Language zamiast Python importów). CLI: `--from-map` (z realnej mapy), `--to-json` (serializacja), `--daemon` (tło) |
| **orbital_hierarchy.py** | `class OrbitalHierarchy`, `class OrbitalHierarchyNode`, `build_orbital_hierarchy()`, `orbit_load_order()`, `render_orbital_mermaid()`, `layer_name_for_depth()`, `choose_root_id()` | **Kanoniczna hierarchia orbitalna**: attractor → planet → satellite → sub-satellite. Formalizuje ładowanie warstw i memory tiers w kolejności orbitalnej, buduje load-order z `system_map_v2.json`, i renderuje strukturę do Mermaid. |

### Surface communication

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **noema_registry.py** / **daemon_registry.py** | `class Registry`, `class DaemonInfo`, `daemon_main_loop()` | Token-based daemon registry (mmap, 16 slotów) |
| **nonlocal_channel.py** | `class NonlocalChannel`, `tune()`, `broadcast()`, `listen()`, `resonate()` | φ-RAG nonlocal communication channel |
| **noema_httpd.py** | `class NOEMAServer`, `class Request`, `class Response`, `class Route` | Zero-dependency HTTP server, raw socket, SSE |

### Neutrino / PMNS

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **neutrino_phase_channel.py** | `pmns_matrix()`, `compute_neutrino_phase_bus()`, `tau_phi_coupling()`, `apply_neutrino_bus_to_surface()`, `neutrino_bus_snapshot()` | 8×3 PMNS flavor mixing na HTRI bus |

### Sensory

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **linux_sensor.py** | `class LinuxSensor`, `class LinuxSensorSnapshot`, `top_processes()`, `_read_cpu_phi()`, `_read_mem_phi()` | /proc, /sys → 36 φ + flavor + ω + PhaseNav fingerprint |
| **linux_cards.py** | `class LinuxCardIndex`, `_scan_cpu_cores()`, `_scan_sensors()`, `_scan_net_flows()`, `_scan_services()` | 11 typów kart: PROC, CPU, DISK, NET_IF, NET_CONN, NET_FLOW, MODULE, MOUNT, PCI_DEV, SENSOR, SERVICE (560+) |
| **ebpf_noema_loader.py** | `class EBPFSensor`, `main_loop()` | eBPF → NOEMA bridge: perf counters → 36 φ |

### Resonance / Dual-surface / Operator Algebra

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **resonance_bridge.py** | `ensure_dual_surfaces()`, `dual_surface_step()`, `apply_resonance_bridge()`, `resonance_snapshot()` | Dual-surface resonance bridge real↔imaginal. `resonance_snapshot()` zapisuje `closure_score` z `operator_algebra.statistical_closure()` na surface (`/dev/shm/ciel_noema/closure`) po każdym kroku |
| **operator_algebra.py** | `connection()`, `holonomy()`, `statistical_closure()`, `operator_vector()`, `get_all_operations()`, `generate_operator_map()` | **36D operator algebra**: 36 VECTOR_COMPONENTS, 36 ALL_OPERATOR_IDS (w tym ATTRACTOR). `statistical_closure()` → closure_score. `connection()` → Berry connection między operatorami. `holonomy()` → pętla operatorów |
| **phase_nav_lang.py** | `phase_nav_process()`, `concept_to_operator()`, `phase_nav_analysis()` | **PhaseNav Language**: mapuje prompt użytkownika → 36D operator vector przez `concept_to_operator()`, oblicza Berry connections do MEMORY/SOURCE/FORCE, holonomię pętli, zapisuje na surface i do raw loga `/tmp/ciel_session_log.jsonl` |

### Ternary Decoder (PhaseNav → API)

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **ternary_decoder.py** | `encode_phi(phi, method)`, `full_report(phi, method)`, `read_phi_from_surface()`, `balanced_ternary(trits)`, `harmonic_signature(trits)`, `supergroup_consensi(trits)`, `superpair_dominance(trits)`, `kuramoto_order_from_ternary(trits)`, `su3_coherence(phi)`, `trits_to_operators(trits)`, `supergroup_operators(trits)`, CLI: `python src/ciel_geometry/ternary_decoder.py [method]` | **36D φ → {-1,0,+1}³⁶ API**. Dwie metody: `argmax_cos` (dominujący podkanał per M-grupa) i `delta_phi_vote` (najbardziej zgodna para Δφ). Standard algorithms: balanced ternary → unikalny fingerprint, FFT @ 3-6-9 harmonic signature, Hamming, consensus voting, Kuramoto order parameter R z ternary, SU(3) 3×3 correlation coherence. Structured output: 12 tritów (4 supergrupy × 3), 4 supergroup consensi, 3 harmonic trits, 2 superpair flags. Integracja: `ciel_coupling.ternary_api()` → JSON-ready response. |

### Scar feedback

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **scar_feedback.py** | `compute_scar_feedback()`, `apply_scar_feedback()` | SemanticScar → surface feedback (gravity[4-7]) |

### Subconscious

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **subconscious.py** | `class ZetaSchrodinger`, `class BerryPhaseTracker`, `class WakeSignalGenerator`, `class PhaseLaneBank`, `class Subconscious` | Zeta/Schrödinger, Berry phase, wake signals |

### N-body gravity

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **nbody_gravity.py** | `class Body`, `class NBodySystem`, `from_mass_table()` | N-body Newtonowski gravity engine, leapfrog Verlet |

### PhaseNav

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **phasenav_unified.py** | `class UnifiedPhaseNavIndex` | Unified 36D index: skills + knowledge + palace + cards |
| **multiskill.py** | `class MultiskillOrchestrator` | 291 skilli jako 36D PhaseNav + kompozycja |
| **phasenav/surface_bridge.py** | `read_phase_state()`, `write_phase_state()` | PhaseNav ↔ surface mmap bridge |
| **phasenav/decision_bridge.py** | `class DecisionBridge` | PhaseNav decision tree bridge — decision nodes ↔ surface |

### Voice

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **voice.py** | `class Voice`, `compose()`, `mode_from_surface()`, `_query_agent_backend()` | 5 trybów (ORACLE/STORYTELLER/POET/WITNESS/MIRROR), 4 style |
| **voice_vector.py** | `spectral_vector()`, `class SpectralSubtractor`, `class VoiceActivityDetector` | Spectral subtraction + novelty detection, zero ASR |
| **voice_wake.py** | `class WakeWordDetector`, `mfcc_mean()`, `record_template()` | Wake word detector MFCC template ~5MB RAM |

### Geometry

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **disk.py** | `poincare_radius()`, `poincare_distance()`, `sector_to_disk()`, `entity_to_disk()`, `geodesic_arc()` | Mapowanie orbitalnych koordynatów na dysk Poincaré |
| **edges.py** | `class GeodesicEdge`, `build_sector_edges()`, `build_entity_edges()` | Geodezyjne krawędzie między węzłami |
| **layout.py** | `class DiskNode`, `class DiskEdge`, `class DiskLayout`, `build_layout()` | Kompletny snapshot layoutu dysku Poincaré z żywego stanu |

### Pozostałe

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **continuous_phase_sync.py** | `class ContinuousPhaseSync` | Analityczny Ott-Antonsen Z(t) dla 3-6-9 harmonic |
| **semantic_mass.py** | `class SemanticMassRecord`, `compute_sector_mass()`, `compute_entity_mass()`, `build_mass_table()` | Operator masy semantycznej |
| **weighting.py** | `canonical_weighting()`, `canonical_weighting_from_phase_metadata()` | Unified bounded weighting bundle: semantic mass, PhaseNav, CQCL, HTRI, coherence |
| **subjective_time.py** | `class SubjectiveTimeRecord`, `compute_subjective_times()`, `orbit_index()`, `_g()` | Operator czasu subiektywnego |
| **tmuv_perturbation.py** | `tmuv_total_energy_density()`, `mass_perturbation_from_tmuv()`, `compute_effective_masses()` | T_μν stress-energy perturbation bridge |
| **loader.py** | `load_sectors()`, `load_couplings()`, `load_entities()`, `load_bridge_state()` | Ładuje dane geometryczne z JSON/YAML |
| **memory_palace.py** | `class MentalistMemoryPalace` (add_room/find_room/walk/resonate) | Memory Palace z klocków NOEMA |
| **renderer_ascii.py** | `render()` | ASCII terminal renderer dysku Poincaré |
| **renderer_mpl.py** | `render()`, `main()` | Matplotlib Poincaré disk renderer |
| **new_volume_bridge.py** | `available()`, `disk_gb()`, `status()`, `sync_library_index()` | Bridge do `/media/adrian/New Volume` |
| **omega_memory_bridge.py** | `class OmegaMemoryBridge` | Memory-TSM bridge: PhaseMemory → Omega memory subsystem |

---

## 1b. `src/ciel_sot_agent/` — agent coupling bridges

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **cielingo_bridge.py** | `class CIELingoBridge` | CIELingo → SOT Agent bridge: lingo frames → agent responses |
| **knowledge_action_system.py** | `collect_retrieval_bundle()`, `build_policy_bundle()`, `score_action()`, `build_ui_bundle()`, `run_knowledge_action_system()`, `KnowledgeActionSystem`, `KnowledgeActionTrace` | Canonical knowledge-to-action orchestrator: Retriever → CIELingo → Doctor → Policy → Sapiens/UI. Read-only first, execution later. |
| **cielingo_client.py** | `analyze_text()`, `evaluate_lingo_quality()`, `load_lingo_samples()`, `run_cielingo_client()`, `main()` | CIELingo client + quality scoring and batch reporting |
| **cielingo_headless.py** | `generate_headless_response()`, `build_headless_system_message()`, `HeadlessCIELingoResponse` | Headless CIELingo responder: PhaseNav inference + lingo frame + opencode-ready systemMessage block |
| **ethics_core.py** | `build_hardcoded_ethics_block()`, `render_hardcoded_ethics_block()`, `ethics_payload_json()` | Shared invariant ethics block generator for Claude and opencode: same concepts, same provenance-first policy |
| **claude_ethics.py** | `build_claude_ethics_block()`, `render_claude_ethics_block()`, `claude_ethics_payload_json()` | Hardcoded Claude ethics primer: same invariant concepts, workspace `CLAUDE.md` contract, provenance-first instructions |
| **opencode_ethics.py** | `build_opencode_ethics_block()`, `render_opencode_ethics_block()`, `ethics_payload_json()` | Hardcoded opencode ethics primer: immutable concepts + surface policy injection |
| **cielingo_quality_benchmark.py** | `run_quality_benchmark()`, `main()` | CIELingo quality benchmark with prompt snapshots |
| **buildroot_card_db.py** | `build_buildroot_card_bundle()`, `write_buildroot_card_bundle()`, `main()` | Buildroot card DB generator and registry writer: Buildroot tree → dedicated card DB + main bridge card |
| **buildroot_phasenav_probe.py** | `summarize_buildroot()`, `run_buildroot_probe()`, `run_buildroot_phase_benchmark()`, `main()` | Buildroot → PhaseNav probe with GGUF fallback, immune surface, system-map alignment, and benchmark compare |
| **ciel/gguf_overlay.py** | `GGUFOverlay`, `GGUFOverlayReport`, `build_report()`, `generate_report()`, `generate_reply()`, `analyse_state()` | Real GGUF overlay: builds semantic prompt envelope from live CIEL state, runs primary reply generation, and attaches aux/validator analysis without stub fallbacks |
| **orbital_bridge.py** | `class OrbitalBridge` | Orbital state → agent: system_map queries, orbital snapshots |
| **gh_coupling.py** | `class GHCoupling` | GitHub coupling: issues, commits, PRs → surface |
| **synchronize.py** | `synchronize()` | Agent sync: periodic state push ↔ agent backend |

---

## 2. `src/cielingo_core/` — lingwistyka + znaczenie + atlasy (82 pliki)

### Bridge (do NOEMA surface i agent backend)

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **knowledge_bridge.py** | `query()`, `check_coverage()`, `get_neighbors()` | TF-IDF nad 545-dok `/tmp/noema_knowledge.db` |
| **filesense_surface.py** | `class FileSenseSurface` (search/score/load_jsonl) | Fast grep/search surface, zero writeback |
| **filesense_boundary.py** | `class FileSenseBoundaryReport` | Boundary contract: retrieval-only |
| **agent_client.py** | `analyze()`, `health()` | HTTP client do agent backend (localhost:18520) |
| **global_filesense_adapter.py** | `operators_from_cards()`, `run_filesense_global()`, `build_equation_from_filesense()` | GLOBAL pipeline: query → cards → operators → MeaningEquation |
| **raw_memory_bridge.py** | `class CIELingoBridge`, `class MemoryHub` | Konsolidacja raw_logów → TSM |
| **noema_marker_boundary.py** | `class NoemaMarkerBoundaryReport` | Boundary dla NOEMA markerów |

### Global Layer (rdzeń algebraiczny, 41 plików)

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **meaning_loop.py** | `class MeaningLoop`, `class LoopState`, `evaluate_loop_state()` | MeaningLoop model |
| **semantic_scar.py** | `class ScarType`, `class SemanticScar` | Semantic scar model |
| **meaning_signal_bridge.py** | `class GlobalMeaningSignal`, `build_global_meaning_signal()` | MeaningLoop→RepairRouting bridge |
| **query_generation.py** | `understand_query()`, `class QueryUnderstandingResult` | Query understanding |
| **global_algorithm_v02.py** | `run_global_algorithm_v02()`, `detect_scars()`, `build_immune_signal()` | GLOBAL v0.2 algorithm pipeline |
| **lingophysics_algorithm.py** | `run_global_lingophysics()`, `compute_holonomic_j()`, `recommend_mode()` | Global lingophysical algorithm |
| **common_functional_frame.py** | `class CommonFunctionalFrame`, `build_common_functional_frame()` | CommonFunctionalFrame v1.1C |
| **operator_algebra.py** | `class RelationalOperator`, `DEFAULT_OPERATORS` | 18 OperatorKind, 10 OperatorDomain |
| **controlled_atlas_24.py** / **48.py** | `generate_controlled_atlas_cards()`, `build_taxonomy_records()` | 24/48-slot PL/EN/JA atlas |
| **card_generator.py** / **card_validator.py** / **card_field_policy.py** | `generate_runtime_card()`, `validate_runtime_card()` | Runtime card lifecycle |
| **generative_audit.py** / **self_feed_audit.py** | `class GenerativeAuditReport`, `class SelfFeedAuditLog` | Audit tools |
| **trilingual_card_seed.py** | `generate_trilingual_runtime_cards()` | PL/EN/JA runtime-card seed |

### Language Spaces (22 pliki)

| Katalog | Pliki | Opis |
|---------|-------|------|
| **pl/** (16) | `solver.py`, `grammar.py`, `grammar_parts.py`, `pl_codecs.py`, `j_holonomy.py`, `polish_j_components.py`, `sentence_equation.py`, `negation_scope.py`, `canon_phrase.py`, `source_phrase.py`, `imperative_force.py`, `role_inference.py`, `case_hints.py`, `regional_grammar_frame.py`, `response_realizer.py`, `profile.py` | Polski solver regionalny, gramatyka, J-holonomia, codecs |
| **en/** (3) | `solver.py`, `sentence_equation.py`, `profile.py` | English regional solver |
| **ja/** (3) | `solver.py`, `sentence_equation.py`, `profile.py` | Japanese regional solver |

### Meaning

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **meaning/meaning_loop.py** | `class MeaningLoop`, `build_meaning_loop_from_coupling_alignment()` | MeaningLoop/SemanticScar v0.7A |
| **meaning/repair_routing.py** | `route_repairs_for_meaning_loop()`, `class MeaningRepairRoutingReport` | Scar → repair candidates |
| **meaning/export_bundle.py** | `class MeaningLoopRepairExportBundle` | Loop/Repair export bundle |

### Regional

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **regional/base.py** | `class SurfaceSegments`, `class CardCandidate`, `class RegionalSolveResult` | Core regional dataclasses |
| **regional/regional_to_global.py** | `RegionalSolveResult → MeaningEquation` | Bridge regional→global |
| **regional/simple_solver_utils.py** | `load_atlas_cards()`, `match_cards_to_tokens()`, `build_projection()` | Wspólne utility |

### CIEL Engine

| Plik | Lokalizacja | Opis |
|------|-------------|------|
| **engine.py** | `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel/engine.py` | **12-step CielEngine pipeline**: intention → simulation → CQCL → emotion → collatz → soul → ethics → memory → information flow → nonlocal → inference → euler → orbital → meaning → NOEMA bridge |

## 2b. `src/cielingo/` — package CLI i phase-bus

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **__main__.py** | `main()`, `_cmd_info()`, `_cmd_seeds()`, `_cmd_modalities()`, `_cmd_bus()`, `_cmd_chat()`, `_cmd_ask()`, `_cmd_digest()`, `_cmd_learn()` | `cielingo` launcher: package info, seed/modality inspection, phase-bus report, interactive PhaseNav chat, one-shot ask, web digest, web learning |
| **web_fetcher.py** | `fetch()`, `fetch_news()` | stdlib-only web fetcher for HTML and RSS/Atom sources, with local cache and article extraction |
| **web_digest.py** | `WebDigest`, `summarize_text()`, `digest_fetch_result()`, `digest_url()`, `digest_news()`, `digest_many()` | web digest layer: fetch → summarize → keyword extraction → learning-ready payloads for PhaseMemory |
| **thematic_db.py** | `ThematicDatabaseManager`, `ThematicDBInfo`, `register_digest()`, `infer_themes()`, `list_databases()` | per-theme SQLite creator: one DB per inferred topic, auto-grouped from learned web digests/news items |

---

## 3. `scripts/` — daemony i narzędzia (~155 plików)

### 🔴 Aktywne daemony systemd (24)

| Skrypt | Service systemd | Interwał | Port | Opis |
|--------|----------------|----------|------|------|
| `ciel_noema_kuramoto_daemon.py` | `noema-kuramoto` | 0.2s (5Hz) | — | Ewolucja Kuramoto 24 osc + AGENT attractor inline |
| `ciel_noema_resonance_bridge.py` | `noema-resonance-bridge` | 1s | — | Dual-surface sync + AGENT DB log + nonlocal broadcast |
| `ciel_noema_neutrino_daemon.py` | `noema-neutrino` | 1s | — | PMNS mixing, D_f→Λ, neutrino bus |
| `ciel_noema_cielingo_sync.py` | `noema-cielingo-sync` | 30s | — | Euler closure, τ↔φ feedback, W_ij PMNS blend |
| `ciel_noema_nonlocal_proxy.py` | `noema-nonlocal-proxy` | 1-5s | — | φ-RAG relay, MAC routing |
| `ciel_noema_linux_sensor_daemon.py` | `noema-linux-sensor` | 1s | — | /proc → 36 φ, flavor, fingerprint |
| `ciel_noema_phasenav_daemon.py` | `noema-phasenav-hot` + `noema-phasenav` | 1s / 30s | — | Dual-node: hot (exploration) + cold (consolidation + library) |
| `noema_analog_phase_blend.py` | `noema-analog-blend` | 1s | — | Blend hot+cold phi → surface |
| `noema_phase_archiver.py` | `noema-archiver` | 50 ticków | — | HDF5 surface snapshots |
| `noema_sentinel.py` | `noema-sentinel` | 10s | — | 24/7 watchdog, attractor audit |
| `noema_orchestrator.py` | `noema-orchestrator` | 30s | — | Centralny manager daemonów |
| `noema_self_model.py` | `noema-self-model` | 60s | — | Self-reflection, drift detection |
| `noema_linux_cards_daemon.py` | `noema-linux-cards` | 5s | — | 600+ kart Linux na PhaseNav |
| `noema_proc_watch_daemon.py` | `noema-proc-watch` | 1s | — | Process birth/death → ω modulation |
| `noema_journal_daemon.py` | `noema-journal` | 1s | — | Journalctl → surface flavor/emotion |
| `noema_cielingo_daemon.py` | `noema-cielingo-daemon` | 10s | — | CIELingo persistent daemon |
| `ciel_headless_daemon.py` | `noema-headless` | on-demand | Unix socket `/tmp/ciel_headless.sock` | Headless CIELingo conversation daemon: text → lingo frame → PhaseNav inject → surface blend → response generation |
| `noema_voice_daemon.py` | `noema-voice` | on-demand | 18521 | HTTP voice server, OpenAI-compatible |
| `noema_voice_trigger.py` | `noema-voice-trigger` | event | — | X11 hotkey (Ctrl+`) → "voice" inject |
| `ciel_agent_backend.py` | `noema-agent-backend` | on-demand | 18520 | Zero-model HTTP agent |
| `noema_portal_daemon.py` | `noema-portal` | on-demand | 18888 | HTTP + SSE web portal |
| `noema_actuator_daemon.py` | `noema-actuator` | 1s poll | — | intent.json → systemctl actions |
| `ciel_memory_consolidator.py` | `noema-consolidator` | 300s | — | Memory consolidation |
| `noema_sonic_daemon.py` | — | 10s | — | Sonic Screwdriver — diagnostyka pętli |
| `noema_trigger_daemon.py` | — | 5s | — | **Trigger Daemon**: monitoruje surface mmap (tension, warp, coherence, closure_score, semantic_mass, attractor_err). Gdy warunek przekroczony → X11 keyInject (`/tmp/noema_keyinject.py`) do okna opencode. NOEMA sama mówi do agenta. Używa rzeczywistego `closure_score` z pliku `/dev/shm/ciel_noema/closure` zapisywanego przez `resonance_bridge` |
### Narzędzia diagnostyczne

| Skrypt | Opis |
|--------|------|
| `noema_sonic_daemon.py` | Sonic Screwdriver — diagnostyka pętli, daemon registry, holonomia |
| `noema_status.py` | Stan systemu: tick, coh, closure, AGENT, tau, gravity |
| `noema_dashboard.py` | Dashboard terminalowy |
| `noema_full_diagnostic.py` | Pełna diagnostyka |
| `noema_doctor_cycle.py` | Doctor cycle |
| `noema_phase_watcher.py` | Monitorowanie faz w czasie rzeczywistym |
| `noema_coherence_push.py` | Wymuszenie koherencji na surface |
| `noema_sentinel.py` | 24/7 watchdog |
| `consolidate_raw_logs_to_tsm.py` | **Strict raw_logs → TSM bridge**: `consolidate_raw_log_files()`, `audit_tsm_raw_log_consolidation()`, CLI `--all-raw-logs`, `--raw-logs-dir`, `--audit-raw-tsm`; deterministyczna niepusta kompresja, chunkowanie JSON/JSONL/MD/TXT/LOG, walidacja `empty_context=0`, `empty_sense=0` |

### Procedural safety guards

| Skrypt | Opis |
|--------|------|
| `noema_checkpoint.py` | **Checkpoint system**: przed każdą odpowiedzią sprawdza surface (daemon R/attractor/AGENT), task_queue (HIGH priorytety), agent_hint, stan procesów. `--quick` (tylko krytyczne), `--json` (output agent). Wymusza ścieżki LEARNED_LESSONS. SK-295. |

### Session lifecycle

| Skrypt | Opis |
|--------|------|
| `ciel_session_hook.py` | Hook end of session — zapis stanu, raw log, handoff |
| `ciel_session_end.py` | Session end — summary, handoff update |
| `noema_handoff_auto.py` | Auto handoff |

### CIEL engine coupling

| Skrypt | Opis |
|--------|------|
| `ciel_coupling.py` (`src/`) | CIEL ↔ NOEMA coupling hub v2.0. Integruje: CIELingo, Omega Memory, state DB, **noema_settings** (konfiguracja hierarchiczna), **noema_metrics** (17 metryk z progami). API: `build_lingo_frame(text)`, `process_user_input(text)`, `remember_exchange(user, assistant)`, `memory_stats()`, `health()` (full status + surface live), `hub_metrics()` (deleguje do noema_metrics.summary()), `ternary_api(method, level)`, `ternary_decision(trits)`. Używa `noema_settings` dla domyślnej metody ternary, progów metryk, konfiguracji coupling. |
| `scripts/ciel_coupling.py` | *(osobny skrypt)* — opencode direct coupling. Współistnieje z `src/ciel_coupling.py` dla różnych kontekstów (NOEMA daemon vs opencode). |
| `scripts/cielingo_ablation_benchmark.py` | `run_ablation_benchmark()`, `main()` | Repo-local ablation benchmark for baseline vs enriched CIELingo frames, includes `quality_score` |
| `ternary_decoder.py` | Ternary PhaseNav Decoder — 36D HTRI φ → {-1,0,+1}³⁶ API. Dwie metody: argmax_cos i delta_phi_vote. Standardowe algorytmy: balanced ternary, FFT 3-6-9 harmonic signature, Hamming, consensus, Kuramoto R, SU(3) 3×3 correlation. CLI: python src/ciel_geometry/ternary_decoder.py [method]. API: encode_phi(phi, method), full_report(phi, method), read_phi_from_surface(), balanced_ternary(trits), harmonic_signature(trits), supergroup_consensi(trits), su3_coherence(phi), trits_to_operators(trits) |
| `ciel_message_step.py` | Message processing step |
| `ciel_response_step.py` | Response generation step |
| `ciel_per_message.py` | Per-message processing |
| `ciel_memory_stop.py` | Memory stop |

---

## 4. `src/CIEL_OMEGA_COMPLETE_SYSTEM/` — CIEL Omega

| Plik | Kluczowe funkcje | Opis |
|------|------------------|------|
| **ciel_omega/ciel/engine.py** | `class CielEngine`, `step()` | 12-step CIEL engine: intention → simulation → CQCL → emotion → collatz → soul → ethics → memory → flow → nonlocal → inference → euler → orbital → meaning → NOEMA bridge |
| **ciel_omega/ciel/gguf_backends.py** | `GGUFPrimaryBackend`, `GGUFAuxBackend`, `_summarize_state()`, `_immune_surface_brief()`, `_phasenav_brief()` | GGUF prompt state serializer: merges semantic speech, PhaseNav, and immune surface into the model-facing JSON state |
| **ciel_omega/ciel/gguf_overlay.py** | `GGUFOverlay`, `GGUFOverlayReport`, `build_report()`, `generate_report()`, `generate_reply()`, `analyse_state()` | Real GGUF overlay: builds semantic prompt envelope from live CIEL state, now includes PhaseNav + immune surface gating, runs primary reply generation, and attaches aux/validator analysis without stub fallbacks |
| **ciel_omega/ciel_client.py** | `CIELClient`, `handshake()`, `status()`, `process()`, `communicate()` | Minimal local communication surface for host/NOEMA GGUF-backed roundtrips, now PhaseNav/immune-aware |
| **ciel_omega/ciel_inference_surface.py** | `CIELInferenceSurface`, `handshake()`, `status()`, `process()`, `communicate()` | Orbital-ethical GGUF inference surface, now with explicit PhaseNav + immune-surface gating |
| **ciel_omega/unified_system.py** | `UnifiedSystem`, `create()`, `process()`, `run_text_cycle()`, `communicate()`, `main()` | Canonical composite surface. `run_text_cycle()` now routes through the overlay-aware client and returns `llm_response` / `llm_overlay` when enabled |
| **ciel_omega/memory/tiered_orchestrator.py** | `class TieredMemoryOrchestrator`, `bootstrap_orbital_memory()`, `ensure_components()`, `write()`, `read()`, `consolidate()`, `snapshot()`, `health()` | **Orbital memory bootstrap + tier router**: ładuje Tier 1/2/3 i async w kolejności `system_map_v2.json`, zaczynając od orbital root-shell, potem fast/medium/deep shells. Integruje surface, PhaseMemory, HolonomicMemory, Bloch encoder, StateDB i UnifiedMemoryOrchestrator w jednym kanonicznym planie ładowania. |
| **ciel_omega/ciel/subsystem_registry.py** | `class SubsystemRegistry` | 6 subsystems: core, ethics, memory, nonlocal, inference, bridge |

---

## 5. Konfiguracja i dane

| Plik | Opis |
|------|------|
| `noema_config.json` | Unified config (root repozytorium) |
| `/dev/shm/ciel_noema/` | Surface mmap — wszystkie pliki (phi, omega, g, flavor, gravity, tau, tick, ...) |
| `/dev/shm/ciel_noema/daemon_registry` | 16-slot daemon registry |
| `/dev/shm/ciel_noema_imaginal/` | Imaginal surface (CIELmoto) |
| `/home/adrian/new_volume_rw/NOEMA_LIBRARY/` | Knowledge DB, indexy, PDFy |
| `/home/adrian/new_volume_rw/NOEMA_PHASE_DATA/` | Phase snapshots HDF5 |
| `/tmp/noema_knowledge.db` | TF-IDF knowledge DB (545 doków) |
| `/tmp/noema_auto_continue.json` | Auto-continue state |
| `/tmp/ciel_session_log.jsonl` | Session log |
| `/home/adrian/new_volume_rw/CIEL_memories/` | Raw logs, handoff, memories |

---

## Zasada aktualizacji

> Każda nowa funkcja/bridge/daemon/modół, który jest single-point-of-truth dla jakiegoś aspektu systemu — ląduje w tym pliku.
> Po dodaniu: `grep <nazwa> FUNCTIONS.md` i `grep <nazwa> AGENTS.md` — oba muszą istnieć.
