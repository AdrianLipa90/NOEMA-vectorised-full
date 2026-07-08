# FOR-LOOP AUDIT — BATCH 4

---

## 1. `scripts/ciel_agent_backend.py` (383 lines)

- **Line 92**: `for i in range(len(tokens) - n + 1)` — **DICT-BUILD/STRUCTURED**. Builds n-gram list. Per request. Trivial size (~tokens). Cannot vectorize.
- **Line 124**: `for b in bigrams if not any(...)` — **DICT-BUILD/STRUCTURED**. Filters bigrams against stopwords. Per request.
- **Line 140-141**: `for phrase, score in unigram_scores.items()` — **DICT-BUILD/STRUCTURED**. Merges scored dict. Per request.
- **Line 142-143**: `for phrase, score in bigram_scores.items()` — **DICT-BUILD/STRUCTURED**. Same pattern.
- **Line 185-191**: `for p in proper` — **DICT-BUILD/STRUCTURED**. Filters proper noun regex matches. Per request.
- **Line 199-202**: `for u in upper` — **DICT-BUILD/STRUCTURED**. Filters UPPERCASE tokens.
- **Line 207-211**: `for a in anchors` — **DICT-BUILD/STRUCTURED**. Deduplicates anchor list. Per request.
- **Line 322-324**: `for m in body.get("messages", [])` — **DICT-BUILD/STRUCTURED**. Iterates messages in POST body (1-10 iters). Per request.
- **Line 380-382**: `for i, a in enumerate(sys.argv)` — **INIT-ONLY**. Parses CLI args once at startup.

**No VECTORIZABLE loops found.**

---

## 2. `scripts/ciel_memory_consolidator.py` (1124 lines)

- **Line 105-109**: `for conn in psutil.net_connections(kind="tcp")` — **I/O-BOUND**. Iterates system network connections. Per status/assessment call.
- **Line 160-161**: `for line in prompt_lines` — **DICT-BUILD/STRUCTURED**. Prints permission prompt. Per fallback check.
- **Line 242-252**: `for column, decl in {...}.items()` — **INIT-ONLY**. DB migration at startup.
- **Line 278-280**: `for src in SCAN_SOURCES` — **I/O-BOUND**. Filesystem stat per source. Per cycle.
- **Line 283-285**: `for f in d.rglob("*")` — **I/O-BOUND**. Recursive filesystem scan. Per cycle.
- **Line 288-315**: `for f in candidates` — **I/O-BOUND**. Filesystem stat + INSERT/UPDATE per candidate. Per cycle. Could be batched with executemany but bottleneck is IO.
- **Line 378-381**: `for d in ... conn.execute(...)` — **I/O-BOUND** (DB). Per status request.
- **Line 382-385**: `for ... in conn.execute(...)` — **I/O-BOUND** (DB).
- **Line 533-534**: `for w in filtered` — **DICT-BUILD/STRUCTURED**. Word frequency counting in `_extract_keywords`. Typically ~100s of words. Could use `collections.Counter(filtered)` instead but trivial.
- **Line 561**: `for l in text.splitlines()` — **DICT-BUILD/STRUCTURED**. Reads last 8 lines of JSONL file. Per file read.
- **Line 662-664**: `for issue in json.loads(...)` — **DICT-BUILD/STRUCTURED**. Per audit row.
- **Line 681-707**: `for row in rows` — **I/O-BOUND** (DB UPDATE per row). Per audit cycle (up to 100 rows).
- **Line 730-746**: `for row in rows` — **I/O-BOUND** (DB). Per failure reason audit.
- **Line 764-766**: `for reason, count in audit.get("counts", {}).items()` — **DICT-BUILD/STRUCTURED**. Per report.
- **Line 1000-1002**: `for row in pending` — **I/O-BOUND** (file processing via LLM per row). Per cycle (batch=5).
- **Line 1054-1056**: `for _ in range(interval)` — **I/O-BOUND** (sleep loop). Per daemon cycle.

**No VECTORIZABLE loops found.**

---

## 3. `scripts/ciel_subconscious.py` (393 lines)

- **Line 152-155**: `for r in results` — **DICT-BUILD/STRUCTURED**. Builds context links from M3 retrieval. Per inference call (top_k=4).
- **Line 281**: `for line in text_clean.strip().splitlines()` — **DICT-BUILD/STRUCTURED**. Parses LLM output lines. Per inference. Text processing, cannot vectorize.
- **Line 286-295**: `for alias, dest in _KEY_ALIASES.items()` — **DICT-BUILD/STRUCTURED**. 3 iterations over small alias dict. Per inference.
- **Line 304-308**: `for w in stripped` — **DICT-BUILD/STRUCTURED**. Checks for emotion words in freeform fallback. Per inference.
- **Line 313-314**: `for w in stripped` (in comprehension) — **DICT-BUILD/STRUCTURED**. Filters content words.
- **Line 322-326**: `for s in ...` — **DICT-BUILD/STRUCTURED**. Finds first short sentence for impulse fallback.
- **Line 174-175**: `for l in lines` (in `_parse`) — technically line 174 is NOT a for loop.

**No VECTORIZABLE loops found.**

---

## 4. `scripts/cielingo_100_loop.py` (205 lines)

- **Line 145-165**: `for i, prompt in enumerate(PROMPTS)` — **NOT-RUNTIME**. Main benchmark loop. Runs once and exits. 134 iterations. Each iteration calls `sem_encode()` which is the actual work.
- **Line 178-180**: `for r in results` — **NOT-RUNTIME**. Builds brain distribution summary. Runs once at end.

**All NOT-RUNTIME (one-shot benchmark).**

---

## 5. `scripts/ciel_graph_extractor.py` (347 lines)

- **Line 106-110**: `for key in sorted(KNOWN_ENTITIES.keys(), ...)` — **DICT-BUILD/STRUCTURED**. Entity extraction. Per article. ~60 known entities.
- **Line 128**: `for sent in sentences` — **DICT-BUILD/STRUCTURED**. Per sentence in article.
- **Line 137-139**: `for rel_type, keywords in RELATION_PATTERNS` — **DICT-BUILD/STRUCTURED**. 8 patterns checked per sentence.
- **Line 143-146**: `for i, src in enumerate(sent_entities); for tgt in sent_entities[i+1:]` — **DICT-BUILD/STRUCTURED**. Pairwise entity relations per sentence. N small.
- **Line 167-175**: `for line in content.splitlines()` — **I/O-BOUND** / DICT-BUILD. Reads existing subject file.
- **Line 179-183**: `for r in relations` — **DICT-BUILD/STRUCTURED**. Deduplication.
- **Line 217-218**: `for e in all_entities` — **DICT-BUILD/STRUCTURED**. Dedup.
- **Line 222-223**: `for r in all_relations` — **DICT-BUILD/STRUCTURED**. Edge counting.
- **Line 284-299**: `for art in articles` — **I/O-BOUND** (network: RSS fetch + article text fetch). Per --live run.
- **Line 303-304**: `for e in all_entities` — **DICT-BUILD/STRUCTURED**.
- **Line 307-309**: `for r in all_relations` — **DICT-BUILD/STRUCTURED**.
- **Line 311-312**: `for name, entity in entity_map.items()` — **I/O-BOUND** (file write per entity).

**No VECTORIZABLE loops found.**

---

## 6. `scripts/ciel_code_learner.py` (233 lines)

- **Line 61-81**: `for node in ast.walk(tree)` — **DICT-BUILD/STRUCTURED**. AST walking. Per file. Number of nodes varies.
- **Line 98-135**: `for frag in frags` — **I/O-BOUND** (DB INSERT per fragment). Per file.
- **Line 121-132**: `for _attempt in range(5)` — **I/O-BOUND** (DB retry loop). Per fragment.
- **Line 137-143**: `for _attempt in range(5)` — **I/O-BOUND** (DB retry). Per file.
- **Line 176-188**: `for pyfile in sorted(directory.rglob("*.py"))` — **I/O-BOUND** (filesystem). Watch mode (3s poll).
- **Line 223-227**: `for p in paths` — **I/O-BOUND** (file processing + DB). Per run.

**No VECTORIZABLE loops found.**

---

## 7. `scripts/ciel_hw_monitor.py` (393 lines)

- **Line 65-69**: `for line in lines; parts = line.split()` — **DICT-BUILD/STRUCTURED**. Parses `/proc/meminfo` fallback. Per snapshot.
- **Line 116-131**: `for p in psutil.process_iter(...)` — **I/O-BOUND**. Iterates over all system processes. Per snapshot.
- **Line 253-255**: `for p in procs` — **DICT-BUILD/STRUCTURED**. Display formatting. Per snapshot.

**No VECTORIZABLE loops found.**

---

## 8. `scripts/ciel_proxy.py` (554 lines)

- **Line 143-146**: `for search_path in GGUF_SEARCH_PATHS` — **I/O-BOUND** (filesystem glob). INIT-ONLY (startup).
- **Line 167-169**: `for i, m in enumerate(models[:8])` — **INIT-ONLY** (logging found models).
- **Line 172-175**: `for m in models` — **INIT-ONLY** (auto-select tiny model).
- **Line 178**: `for m in models` in `safe = [...]` — **INIT-ONLY** (list comprehension).
- **Line 266-268**: `for msg in messages` — **DICT-BUILD/STRUCTURED**. Formats messages for LLM. Per request.
- **Line 271-273**: `for block in content` — **DICT-BUILD/STRUCTURED**. Concatenates text blocks. Per request.
- **Line 347-356**: `for chunk in stream` — **I/O-BOUND** (LLM stream iteration). Per streaming request.
- **Line 420-425**: `async for chunk in stream_llama(...)` — **I/O-BOUND** (SSE streaming).
- **Line 427-428**: `async for chunk in resp.aiter_bytes()` — **I/O-BOUND** (HTTP streaming).

**No VECTORIZABLE loops found.**

---

## 9. `scripts/ciel_per_message.py` (88 lines)

- **Line 41**: `sum(complex(math.cos(p), math.sin(p)) for p in phi)` — **VECTORIZABLE**. Generator expression over 24 phi values, calling `math.cos`/`math.sin` individually. Runs once per message (could be thousands of calls across a session). **Suggestion**: `R = abs(np.mean(np.exp(1j * np.array(phi))))` — single vectorized numpy call.
- **Line 40**: `r = abs(sum(complex(...) for p in phi)) / n` — same as above, this is the full line.

**One VECTORIZABLE generator expression (line 40).**

---

## 10. `scripts/ciel_message_step.py` (729 lines)

- **Line 52-58**: `for _, path in candidates` — **I/O-BOUND** (pickle file reading). Per load.
- **Line 75-81**: `for path in (STATE_FILE, STATE_PERSIST)` — **I/O-BOUND** (pickle file writing). Per save. 2 iterations.
- **Line 274**: `for key, candidate in m3_top` — **DICT-BUILD/STRUCTURED**. Per periodic consolidation (every 5 cycles). max 3 iters.
- **Line 277-279**: `for key, candidate in m3_top` — same.
- **Line 287-294**: `for key, candidate in m5_top` — same. max 2 iters.
- **Line 333-335**: `for k, _ in m3_top` — list comprehension. DICT-BUILD.
- **Line 457-458**: `for k in ("affect", "concept", "impulse")` — **DICT-BUILD/STRUCTURED**. 3 iters. Strips brackets from sub output.
- **Line 489-492**: `for name, ev in result.eba_results.items()` — **DICT-BUILD/STRUCTURED**. List comprehension filtering coherent loops.
- **Line 689-691**: `for block in message` — **DICT-BUILD/STRUCTURED**. Extracts text from content blocks. Per message.

**No VECTORIZABLE loops found.**

---

## 11. `scripts/ciel_system_report.py` (556 lines)

- **Line 66-70**: `for t in tensions` — **DICT-BUILD/STRUCTURED**. Deduplicates tension pairs.
- **Line 108-113**: `for line in lines[-n:]` — **I/O-BOUND** / DICT-BUILD. Reads sub log.
- **Line 159-161**: `for v in values[-width:]` — **DICT-BUILD/STRUCTURED**. Sparkline generation. max 30 iters.
- **Line 253-256**: `for pair, val in tensions` — **DICT-BUILD/STRUCTURED**. HTML row generation.
- **Line 267-279**: `for entry in sub[:8]` — **DICT-BUILD/STRUCTURED**. HTML sub feed rendering.
- **Line 285-296**: `for f in files` — **DICT-BUILD/STRUCTURED**. HTML file rows.

**All NOT-RUNTIME (one-shot report generator).**

---

## 12. `scripts/ciel_benchmark.py` (178 lines)

- **Line 87-120**: `for i, prompt in enumerate(PROMPTS)` — **NOT-RUNTIME**. 3 prompts, one-shot benchmark.
- **Line 143-148**: `for b in benchmarks` — **NOT-RUNTIME**. Summary display.

**All NOT-RUNTIME.**

---

## 13. `scripts/couple_assistant.py` (97 lines)

- **No `for` loops in this file.**

---

## 14. `scripts/converse.py` (137 lines)

- **No explicit `for` loops.** List comprehension on line 25 (`parts = [...]`) is DICT-BUILD/STRUCTURED — builds summary string parts. Per interactive conversation turn. Trivial.

---

## 15. `scripts/dream_whisper.py` (154 lines)

- **Line 61-62**: `for key, item in getattr(orch.m3, ...).items()` — **NOT-RUNTIME** (one-shot). Iterates M3 memory items.
- **Line 63-64**: `for key, item in getattr(orch.m5, ...).items()` — **NOT-RUNTIME**. Same for M5.
- **Line 72-73**: `for key, conf, layer in candidates` — **NOT-RUNTIME**. Picks new candidate.
- **Line 76-78**: `for key, conf, layer in candidates` — **NOT-RUNTIME**. Fallback.
- **Line 101-103**: `for existing in insights` — **NOT-RUNTIME**. Deduplication.

**All NOT-RUNTIME (one-shot).**

---

## 16. `scripts/ebpf_noema_daemon.py` (69 lines)

- **No `for` loops in this file.** Main loop is `while running:`.

---

## 17. `scripts/htri_bench.py` (162 lines)

- **Line 60-80**: `for i, prompt in enumerate(PROMPTS[:N_ROUNDS])` — **NOT-RUNTIME**. 5 prompts, one-shot benchmark.

**All NOT-RUNTIME.**

---

## 18. `scripts/htri_mini.py` (101 lines)

- **Line 50-61**: `for step in range(N_STEPS)` — **NOT-RUNTIME**. 5000-step simulation. Body calls `network.step()` which is internally vectorized via numpy. This is a time-stepping loop, not a per-element loop. ALREADY VECTORIZED internally.
- **Line 66**: `ohm = np.unwrap(np.angle(np.exp(1j * network.phases)))` — vectorized, no loop.

**NOT-RUNTIME (one-shot simulation). Already vectorized internally.**

---

## 19. `scripts/kuramoto_sym.py` (476 lines)

- **Line 105-127**: `for i in range(steps)` — **NOT-RUNTIME**. Main time-stepping loop (default 10000 steps). **Body is ALREADY VECTORIZED** using numpy (line 107: `np.mean(np.exp(1j * phases))`, line 113: full vector ops). Cannot eliminate outer time loop.
- **Line 129-130**: `cos_matrix = 1 - np.cos(...)` — vectorized numpy. No loop.
- **Line 161-162**: `for d in EXPERIMENT_SUBDIRS` — **INIT-ONLY**.
- **Line 219-226**: `for` in `with open` — **NOT-RUNTIME** (logging).
- **Line 229-238**: same.
- **Line 365-374**: `for k in kappas` — **NOT-RUNTIME** (sweep, up to 21 points).
- **Line 393-412**: matplotlib plot code — **NOT-RUNTIME**.

**NOT-RUNTIME. Core loop already vectorized.**

---

## 20. `scripts/optimize_wij.py` (280 lines)

- **Line 71-76**: `for src, targets in base_couplings.items(); for dst in targets` — **INIT-ONLY**. Extracts coupling pairs once.
- **Line 82-84**: `for val, (src, dst) in zip(x, pairs)` — **INIT-ONLY**. Converts flat vector to coupling dict.
- **Line 92-93**: `for _ in range(n_steps)` — **INIT-ONLY** (runs inside scipy objective). Calls `orbital_step()` which is internally vectorized. warm_steps=3.
- **Line 236-239**: `for (src, dst), x_new, x_old in zip(...)` — **NOT-RUNTIME** (result display).
- **Line 246-251**: `for src in all_names; for dst in all_names` — **NOT-RUNTIME** (matrix display).

**INIT-ONLY (optimizer setup) + NOT-RUNTIME (display).**

---

## SUMMARY

| File | Total loops | VECTORIZABLE | I/O-BOUND | INIT-ONLY | DICT-BUILD | NOT-RUNTIME |
|------|-------------|-------------|-----------|-----------|------------|-------------|
| 1. ciel_agent_backend.py | 9 | 0 | 0 | 1 | 8 | 0 |
| 2. ciel_memory_consolidator.py | 17 | 0 | 12 | 1 | 4 | 0 |
| 3. ciel_subconscious.py | 7 | 0 | 0 | 0 | 7 | 0 |
| 4. cielingo_100_loop.py | 2 | 0 | 0 | 0 | 0 | 2 |
| 5. ciel_graph_extractor.py | 14 | 0 | 4 | 0 | 10 | 0 |
| 6. ciel_code_learner.py | 6 | 0 | 6 | 0 | 0 | 0 |
| 7. ciel_hw_monitor.py | 3 | 0 | 1 | 0 | 2 | 0 |
| 8. ciel_proxy.py | 9 | 0 | 5 | 4 | 0 | 0 |
| 9. ciel_per_message.py | 1 | **1** | 0 | 0 | 0 | 0 |
| 10. ciel_message_step.py | 9 | 0 | 2 | 0 | 7 | 0 |
| 11. ciel_system_report.py | 6 | 0 | 0 | 0 | 0 | 6 |
| 12. ciel_benchmark.py | 2 | 0 | 0 | 0 | 0 | 2 |
| 13. couple_assistant.py | 0 | 0 | 0 | 0 | 0 | 0 |
| 14. converse.py | 0 | 0 | 0 | 0 | 0 | 0 |
| 15. dream_whisper.py | 5 | 0 | 0 | 0 | 0 | 5 |
| 16. ebpf_noema_daemon.py | 0 | 0 | 0 | 0 | 0 | 0 |
| 17. htri_bench.py | 1 | 0 | 0 | 0 | 0 | 1 |
| 18. htri_mini.py | 1 | 0 | 0 | 0 | 0 | 1 |
| 19. kuramoto_sym.py | 6 | 0 | 0 | 1 | 0 | 5 |
| 20. optimize_wij.py | 5 | 0 | 0 | 3 | 0 | 2 |
| **TOTAL** | **93** | **1** | **30** | **10** | **38** | **24** |

### Only VECTORIZABLE candidate found:

**`scripts/ciel_per_message.py:40`** — generator expression `sum(complex(math.cos(p), math.sin(p)) for p in phi)` over 24 phi values. Calls `math.cos`/`math.sin` individually. **Suggestion**: replace with `R = abs(np.mean(np.exp(1j * np.array(phi))))` which is a single vectorized numpy call. This runs per message invocation (potentially thousands of times per session). Impact: small (24 iters), but the current approach creates Python overhead for each of 24 oscillators.
