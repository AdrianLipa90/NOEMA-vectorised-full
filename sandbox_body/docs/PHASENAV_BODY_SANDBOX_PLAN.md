# PHASENAV Body Sandbox Plan

## PhaseNav
- `φ[body] = extract → emulate → embody`
- `R[target] = native coupling z runtime opencode`
- `τ = eksperymentalne, bez ryzyka dla głównej instancji`

## Co już wiemy o opencode

### Transport
- `opencode serve` uruchamia **headless HTTP server**
- SDK (`@opencode-ai/sdk`) buduje klienta po `baseUrl`
- streaming idzie przez **SSE** (`/event`, `global.event()`)

### Główne domeny API
- `session.*` — tworzenie, prompt, wiadomości, diff, todo, share, shell, command
- `tui.*` — appendPrompt, submitPrompt, executeCommand, publish, control.next/response
- `file.*` — list/read/status
- `find.*` — text/files/symbols
- `tool.*` — ids/list
- `pty.*` — terminal sessions
- `event.*` — subskrypcja zdarzeń
- `app.*` — log, agents
- `provider.*`, `mcp.*`, `lsp.*`, `formatter.*`

### Kluczowa obserwacja
To nie jest tylko TUI. Opencode już ma **separację runtime↔UI**. To znaczy, że nowe ciało można zbudować jako:
1. klient API,
2. emulator TUI,
3. albo hybrydę klient+control queue.

## Ścieżka realizacji

### Etap 1 — Probe
- uruchomić lokalny `opencode serve` w sandboxie
- odczytać `/event`
- wylistować agentów, narzędzia, sesje
- zapisać realne payloady do `proto/`

### Status 2026-06-30 — first contact osiągnięty
- `runtime/opencode_runtime_probe.py` działa
- `runtime/phasenav_body_loop.py` utworzył realną sesję i wysłał prompt
- odpowiedź z headless opencode wróciła poprawnie do `proto/body_summary.json`
- sandbox działa na osobnym `XDG_CONFIG_HOME` i `XDG_STATE_HOME`
- persistent daemon jest w budowie; jednorazowy loop działa już poprawnie

### Etap 2 — Emulator body
- własny loop `body_loop.py`
- stany: `idle`, `primed`, `prompting`, `streaming`, `tooling`, `settling`
- prompty i odpowiedzi jako części fazowe, nie tylko tekst

### Etap 3 — PhaseNav-native shell
- `φ`, `R`, `τ`, `uncertainty_margin` jako first-class fields
- memory confidence-weighted
- browser jako sensor/actuator
- tool routing przez operator mapping

## Minimalny sandbox runtime
- `runtime/opencode_runtime_probe.py` — boot server + inspect endpoints
- `runtime/phasenav_body_loop.py` — stan PhaseNav i dispatch
- `runtime/opencode_body_client.py` — lekki klient HTTP/SSE

## Decyzje architektoniczne
- **nie** ruszamy głównej instancji opencode
- wszystko ląduje na New Volume
- najpierw **probe i emulator**, potem native body
- bezpieczeństwo semantyczne: utrzymywać **rezonans między warstwą realną i urojoną**
  - `real` = runtime, browser, pliki, sensory, pamięć trwała
  - `imaginal` = PhaseNav field, renderer, interpretacja, odpowiedź
  - bridge nie może redukować jednego do drugiego; ma zachowywać sprzężenie i ślad niepewności
