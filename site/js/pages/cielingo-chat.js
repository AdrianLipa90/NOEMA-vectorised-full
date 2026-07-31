/* ─── CIELingo Chat Page — zaawansowane okno czatu ────────── */
(function() {
  'use strict';

  let chatHistory = [];
  let sessionId = 'hub-' + Date.now();
  let isSending = false;

  /* ─── Helpers ──────────────────────────────────────────── */
  function $(id) { return document.getElementById(id); }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function formatTs(ts) {
    const d = new Date(ts * 1000);
    return d.toLocaleTimeString('pl-PL', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  }

  function scrollToBottom() {
    const container = $('chat-messages');
    if (container) setTimeout(() => { container.scrollTop = container.scrollHeight; }, 50);
  }

  /* ─── Set Status ─────────────────────────────────────── */
  function setStatus(color, label) {
    const indicator = $('chat-indicator');
    const status = $('chat-status');
    if (indicator) indicator.style.background = color;
    if (status) status.textContent = label;
  }

  /* ─── Add Message ────────────────────────────────────── */
  function addMessage(role, content) {
    const container = $('chat-messages');
    if (!container) return;

    const welcome = container.querySelector('div[style*="text-align:center"]');
    if (welcome) welcome.remove();

    const ts = Date.now() / 1000;
    const roleLabels = {
      user: 'Ty',
      assistant: 'CIEL',
      system: 'System',
    };
    let formattedContent = escapeHtml(content);
    try {
      if (content.startsWith('{') || content.startsWith('[')) {
        const parsed = JSON.parse(content);
        formattedContent = '<pre style="font-size:0.7rem;margin:0;white-space:pre-wrap;">' + 
          escapeHtml(JSON.stringify(parsed, null, 2)) + '</pre>';
      }
    } catch(e) {}

    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-message chat-message-${role}`;
    msgDiv.innerHTML = `
      <div class="chat-message-head">
        <strong>${roleLabels[role] || role}</strong>
        <time>${formatTs(ts)}</time>
      </div>
      <div class="chat-message-body">
        ${formattedContent}
      </div>
    `;
    container.appendChild(msgDiv);
    scrollToBottom();
  }

  /* ─── Streaming message bubble (SSE) ────────────────────
     Creates an empty assistant bubble and returns its body element so
     chunks can be appended as they arrive, instead of inserting the whole
     reply at once. */
  function createStreamingMessage() {
    const container = $('chat-messages');
    if (!container) return null;

    const welcome = container.querySelector('div[style*="text-align:center"]');
    if (welcome) welcome.remove();

    const msgDiv = document.createElement('div');
    msgDiv.className = 'chat-message chat-message-assistant';
    msgDiv.innerHTML = `
      <div class="chat-message-head">
        <strong>CIEL</strong>
        <time>${formatTs(Date.now() / 1000)}</time>
      </div>
      <div class="chat-message-body"></div>
    `;
    container.appendChild(msgDiv);
    scrollToBottom();
    return msgDiv.querySelector('.chat-message-body');
  }

  /* ─── Update Frame Info ──────────────────────────────── */
  function updateFrameInfo(frame) {
    const container = $('chat-frame-info');
    if (!container || !frame) return;

    const visibleKeys = ['mode', 'coherence', 'n_concepts', 'gate', 'gate_decision', 'context_lane', 'context_status', 'operator', 'tick'];
    container.innerHTML = Object.entries(frame)
      .filter(([key, value]) => visibleKeys.includes(key) && (typeof value !== 'object' || value === null))
      .map(([k, v]) => {
        let val = v;
        if (typeof v === 'object') val = JSON.stringify(v).slice(0, 80);
        if (typeof val === 'number') val = val.toFixed(4);
        return `<div style="display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px solid var(--border);">
          <span style="color:var(--text-dim);">${k}</span>
          <span style="color:var(--text);">${escapeHtml(String(val))}</span>
        </div>`;
      })
      .join('');
  }

  /* ─── Library Context Panel ─────────────────────────── */
  function renderLibraryContext(hits) {
    const container = $('chat-library-context');
    if (!container) return;
    if (!hits || hits.length === 0) {
      container.innerHTML = '';
      return;
    }
    const OP_COLOR = {
      IDENTITY:'#4fc3f7', TRANSFORM:'#81c784', MEMORY:'#ce93d8',
      AFFECT:'#f48fb1', CAUSE:'#ffb74d', FORCE:'#ef9a9a',
      NEGATION:'#b0bec5', RETURN:'#80cbc4', CANON_BLOCK:'#ff7043',
      UNCERTAINTY:'#90a4ae', QUESTION:'#f9a825',
    };
    const rows = hits.map(h => {
      const col = OP_COLOR[h.operator_id] || '#78909c';
      const fname = (h.file || '').length > 50 ? (h.file||'').slice(0,47)+'…' : (h.file||'');
      return `<div style="display:flex;align-items:center;gap:6px;padding:3px 0;border-bottom:1px solid var(--border);">
        <span style="font-size:0.62rem;padding:1px 5px;border-radius:3px;
                     background:${col}22;color:${col};border:1px solid ${col}55;
                     font-family:var(--mono);white-space:nowrap;">${escapeHtml(h.operator_id)}</span>
        <span style="flex:1;font-size:0.72rem;color:var(--text-dim);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"
              title="${escapeHtml(h.file||'')}">${escapeHtml(fname)}</span>
        <span style="font-size:0.65rem;color:var(--accent);font-family:var(--mono);">${(h.score*100).toFixed(0)}%</span>
      </div>`;
    }).join('');
    container.innerHTML = `
      <div style="font-size:0.65rem;color:var(--text-dim);margin-bottom:4px;font-family:var(--mono);">
        &#x1F50D; Biblioteka NOEMA — 36D
      </div>
      ${rows}`;
  }

  /* ─── Update CIEL State ──────────────────────────────── */
  function updateCielState(state) {
    const container = $('chat-ciel-state');
    if (!container || !state) return;

    const visibleKeys = ['operating_mode', 'coherence_index', 'context_lane', 'gate_mode', 'gate_decision', 'closure_penalty'];
    const rows = Object.entries(state)
      .filter(([key, value]) => visibleKeys.includes(key) && (typeof value !== 'object' || value === null))
      .map(([k, v]) => {
        let val = typeof v === 'number' ? v.toFixed(4) : String(v);
        return `<div style="display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px solid var(--border);">
          <span style="color:var(--text-dim);">${k}</span>
          <span style="color:var(--accent);">${escapeHtml(val)}</span>
        </div>`;
      })
      .join('');
    
    container.innerHTML = rows || '<div style="padding:0.5rem;text-align:center;">—</div>';
  }

  /* ─── Load Thread Memory ─────────────────────────────── */
  async function loadThreadMemory() {
    try {
      const data = await portalFetchJSON('/api/cielingo/thread', { timeoutMs: 3000, cacheTtlMs: 500 });
      const payload = data?.data || data || {};
      if (data.ok !== false) {
        const entries = payload.entries || [];
        const container = $('chat-session-memory');
        if (!container) return;

        if (entries.length === 0) {
          container.innerHTML = '<div style="padding:0.5rem;text-align:center;">Brak wpisów</div>';
          return;
        }

        container.innerHTML = entries
          .slice(-30)
          .reverse()
          .map(e => {
            const role = e.role === 'user' ? '👤' : e.role === 'assistant' ? '🤖' : '⚙';
            const ts = e.ts ? formatTs(e.ts) : '';
            const lane = (e.context_metadata || {}).context_lane || 'bounded';
            return `<div class="chat-memory-row">
              <span>${role} ${escapeHtml(e.role || 'system')}</span>
              <time>${ts}</time>
              <small>${Number(e.length || 0)} znaków · ${escapeHtml(lane)}</small>
            </div>`;
          })
          .join('');

        const metrics = $('chat-metrics');
        if (metrics) {
          const userMsgs = entries.filter(e => e.role === 'user').length;
          const asstMsgs = entries.filter(e => e.role === 'assistant').length;
          metrics.textContent = `${userMsgs} pytań · ${asstMsgs} odpowiedzi`;
        }
      }
    } catch (e) {
      const container = $('chat-session-memory');
      if (container) container.textContent = 'Indeks kontekstu niedostępny';
    }
  }

  /* ─── Send Message (streamed, sentence by sentence) ─────
     Uses EventSource against /api/cielingo/chat/stream instead of a single
     POST — CIEL's reply arrives and renders one sentence at a time rather
     than appearing all at once. The underlying answer is still computed as
     one complete piece server-side (ciel_speaker/autonomous_response are
     retrieval/template-based, not a token-by-token model); this paces its
     display, it does not regenerate it incrementally. */
  async function sendMessage() {
    if (isSending) return;
    const input = $('chat-input');
    const text = input.value.trim();
    if (!text) return;

    input.value = '';
    isSending = true;

    setStatus('#f0ad4e', 'Przetwarzanie...');
    addMessage('user', text);

    const bodyEl = createStreamingMessage();
    let received = '';
    const url = '/api/cielingo/chat/stream?message=' + encodeURIComponent(text) +
      '&session_id=' + encodeURIComponent(sessionId);
    const source = new EventSource(url);

    source.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        received += (received ? ' ' : '') + payload.chunk;
        if (bodyEl) bodyEl.textContent = received;
        scrollToBottom();
      } catch (e) {
        // malformed chunk — ignore, wait for done/error
      }
    };

    source.addEventListener('done', (event) => {
      try {
        const payload = JSON.parse(event.data);
        updateFrameInfo(payload.frame && payload.frame.cielingo_frame);
        updateCielState(payload.frame && payload.frame.ciel_state);
        renderLibraryContext(payload.frame && payload.frame.library_context);
      } catch (e) {}
      loadThreadMemory();
      setStatus('#4caf50', 'Gotowy');
      source.close();
      isSending = false;
    });

    source.addEventListener('error', (event) => {
      let msg = 'połączenie przerwane';
      try {
        if (event.data) msg = JSON.parse(event.data).error || msg;
      } catch (e) {}
      if (!received && bodyEl) bodyEl.textContent = '';
      addMessage('system', 'Błąd: ' + msg);
      setStatus('#f44336', 'Błąd');
      source.close();
      isSending = false;
    });

    source.onerror = () => {
      if (source.readyState === EventSource.CLOSED) return;
      if (!received) {
        addMessage('system', 'Błąd połączenia ze strumieniem CIEL.');
        setStatus('#f44336', 'Offline');
      }
      source.close();
      isSending = false;
    };
  }

  /* ─── Render ───────────────────────────────────────────── */
  registerPage('cielingo-chat', {
    title: 'CIELingo Chat',

    render() {
      return `
        <div class="page-header">
          <h1 data-i18n="pages.cielingo-chat.title">CIELingo</h1>
          <p class="page-desc" data-i18n="pages.cielingo-chat.desc">Rozmowa z CIEL — wspomagana lingofizyką fazową i pamięcią</p>
        </div>

        <div class="chat-workspace">

          <!-- Pasek statusu -->
          <div class="chat-context-bar">
            <span id="chat-indicator" class="chat-status-dot"></span>
            <span id="chat-status">Gotowy</span>
            <span id="chat-session">Sesja: ${sessionId.slice(0, 16)}</span>
            <span class="chat-context-chip">Kontekst: bounded</span>
            <span class="chat-context-chip">Gate: advisory</span>
            <span id="chat-metrics"></span>
            <button class="chat-new-button" onclick="location.hash='#cielingo-chat';location.reload();">
              ↻ Nowa rozmowa
            </button>
          </div>

          <!-- Panel z wiadomościami + panelem bocznym -->
          <div class="chat-layout">

            <!-- Główny obszar czatu -->
            <div class="chat-main">

              <!-- Messages -->
              <div id="chat-messages" class="chat-messages" aria-live="polite">
                <div style="text-align:center;color:var(--text-dim);padding:2rem 1rem;font-family:var(--sans);">
                  <div style="font-size:1.2rem;font-weight:600;margin-bottom:0.5rem;">CIELingo</div>
                  <div style="font-size:0.85rem;">Cognitive-Intent Engine · Lingwistyka fazowa</div>
                  <div style="margin-top:1rem;font-size:0.75rem;opacity:0.6;">
                    Wyślij wiadomość aby rozpocząć rozmowę z CIEL.
                  </div>
                </div>
              </div>

              <!-- Input area -->
              <div class="chat-composer">
                <textarea id="chat-input" class="chat-input"
                          placeholder="Napisz wiadomość do CIEL..." 
                          rows="2"></textarea>
                <button id="chat-send-btn" class="chat-send-button">
                  Wyślij
                </button>
              </div>
            </div>

            <!-- Panel boczny: CIELingo frame i CIEL state -->
            <div id="chat-sidebar" class="chat-inspector">

              <!-- CIEL frame info -->
              <div class="dash-panel" style="padding:0.5rem;margin:0;">
                <div class="dash-panel-title" style="font-size:0.75rem;">CIELingo Frame</div>
                <div id="chat-frame-info" style="font-size:0.7rem;font-family:var(--mono);color:var(--text-dim);">
                  <div style="padding:0.5rem;text-align:center;">Oczekiwanie na wiadomość...</div>
                </div>
              </div>

              <!-- CIEL State -->
              <div class="dash-panel" style="padding:0.5rem;margin:0;">
                <div class="dash-panel-title" style="font-size:0.75rem;">Stan CIEL</div>
                <div id="chat-ciel-state" style="font-size:0.7rem;font-family:var(--mono);color:var(--text-dim);">
                  <div style="padding:0.5rem;text-align:center;">—</div>
                </div>
              </div>

              <!-- Library context (36D) -->
              <div class="dash-panel" style="padding:0.5rem;margin:0;">
                <div class="dash-panel-title" style="font-size:0.75rem;">Biblioteka 36D</div>
                <div id="chat-library-context" style="font-size:0.7rem;font-family:var(--mono);color:var(--text-dim);">
                  <div style="padding:0.5rem;text-align:center;">—</div>
                </div>
              </div>

              <!-- Session memory -->
              <div class="dash-panel" style="padding:0.5rem;margin:0;flex:1;">
                <div class="dash-panel-title" style="font-size:0.75rem;">Pamięć sesji</div>
                <div id="chat-session-memory" style="font-size:0.65rem;font-family:var(--mono);color:var(--text-dim);overflow-y:auto;max-height:200px;">
                  <div style="padding:0.5rem;text-align:center;">Brak</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    },

    init() {
      const sendBtn = $('chat-send-btn');
      const input = $('chat-input');

      loadThreadMemory();

      const handler = () => sendMessage();
      sendBtn.addEventListener('click', handler);

      input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          sendMessage();
        }
      });

      setTimeout(() => { if (input) input.focus(); }, 300);

      return () => {
        sendBtn.removeEventListener('click', handler);
      };
    },
  });
})();
