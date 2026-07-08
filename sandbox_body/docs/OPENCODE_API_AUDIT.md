# Opencode API Audit — local findings

## Artefakty lokalne
- Binary: `/home/adrian/.opencode/bin/opencode`
- Config: `/home/adrian/.config/opencode/opencode.jsonc`
- SDK: `/home/adrian/.config/opencode/node_modules/@opencode-ai/sdk`
- Plugin API: `/home/adrian/.config/opencode/node_modules/@opencode-ai/plugin`

## Fakty potwierdzone
- `opencode serve` = headless HTTP server
- `createOpencodeServer()` z SDK startuje proces `opencode serve --hostname --port`
- `createOpencodeClient()` dodaje header/query `directory`
- TUI ma osobne endpointy `/tui/*`
- istnieje kolejka control `/tui/control/next` i `/tui/control/response`
- zdarzenia globalne i sesyjne są streamowane przez SSE

## Najważniejsze endpointy
- `POST /session` — create session
- `GET /session` — list sessions
- `POST /session/{id}/message` — prompt do sesji
- `GET /session/{id}/messages` — historia + parts
- `GET /event` — SSE event stream
- `POST /tui/append-prompt`
- `POST /tui/submit-prompt`
- `POST /tui/execute-command`
- `GET /tui/control/next`
- `POST /tui/control/response`

## Wniosek
Nowe ciało **nie musi patchować** TUI binarki. Wystarczy użyć istniejącego server mode i zbudować własny klient/renderer.

## Potwierdzenie praktyczne
- sandboxowy loop utworzył sesję `PHASENAV Body Sandbox`
- `POST /session/{id}/message` działa z `parts: [{type:"text", text:"..."}]`
- `GET /session/{id}/message?limit=N` zwraca parts z `reasoning`, `text`, `step-start`, `step-finish`
- runtime można izolować przez `XDG_CONFIG_HOME` + `XDG_STATE_HOME`
