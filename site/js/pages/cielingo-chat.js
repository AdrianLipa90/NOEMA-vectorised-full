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
    if (status) status.innerHTML = `
      <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${color};"></span>
      ${label}
    `;
  }

  /* ─── Add Message ────────────────────────────────────── */
  function addMessage(role, content) {
    const container = $('chat-messages');
    if (!container) return;

    const welcome = container.querySelector('div[style*="text-align:center"]');
    if (welcome) welcome.remove();

    const ts = Date.now() / 1000;
    const roleColors = {
      user: 'var(--accent)',
      assistant: 'var(--text)',
      system: '#f44336',
    };
    const roleLabels = {
      user: 'Ty',
      assistant: 'CIEL',
      system: 'System',
    };
    const bgColors = {
      user: 'var(--bg-card)',
      assistant: 'var(--bg)',
      system: 'var(--bg-card)',
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
    msgDiv.style.cssText = `
      margin-bottom:0.75rem;
      padding:0.5rem 0.75rem;
      border-radius:6px;
      background:${bgColors[role] || 'var(--bg-card)'};
      border-left: 3px solid ${roleColors[role] || 'var(--border)'};
    `;
    msgDiv.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.25rem;">
        <strong style="font-size:0.7rem;color:${roleColors[role] || 'var(--text)'}">${roleLabels[role] || role}</strong>
        <span style="font-size:0.6rem;color:var(--text-dim)">${formatTs(ts)}</span>
      </div>
      <div style="font-size:0.8rem;line-height:1.5;white-space:pre-wrap;word-break:break-word;">
        ${formattedContent}
      </div>
    `;
    container.appendChild(msgDiv);
    scrollToBottom();
  }

  /* ─── Update Frame Info ──────────────────────────────── */
  function updateFrameInfo(frame) {
    const container = $('chat-frame-info');
    if (!container || !frame) return;

    container.innerHTML = Object.entries(frame)
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

  /* ─── Update CIEL State ──────────────────────────────── */
  function updateCielState(state) {
    const container = $('chat-ciel-state');
    if (!container || !state) return;

    const rows = Object.entries(state)
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
      const resp = await fetch('/api/cielingo/thread');
      const data = await resp.json();
      if (data.ok) {
        const entries = data.data.entries || [];
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
            const content = (e.content || '').slice(0, 80);
            return `<div style="padding:3px 0;border-bottom:1px solid var(--border);">
              <span style="opacity:0.6;">${role}</span>
              <span style="font-size:0.6rem;opacity:0.4;margin-left:4px;">${ts}</span>
              <div style="font-size:0.65rem;margin-left:16px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                ${escapeHtml(content)}${(e.content || '').length > 80 ? '...' : ''}
              </div>
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
      // silent
    }
  }

  /* ─── Send Message ───────────────────────────────────── */
  async function sendMessage() {
    if (isSending) return;
    const input = $('chat-input');
    const text = input.value.trim();
    if (!text) return;

    input.value = '';
    isSending = true;

    setStatus('#f0ad4e', 'Przetwarzanie...');
    addMessage('user', text);

    try {
      const response = await fetch('/api/cielingo/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, session_id: sessionId }),
      });
      const data = await response.json();

      if (data.ok) {
        const reply = data.data.response || 'Brak odpowiedzi.';
        addMessage('assistant', reply);
        updateFrameInfo(data.data.cielingo_frame);
        updateCielState(data.data.ciel_state);
        loadThreadMemory();
        setStatus('#4caf50', 'Gotowy');
      } else {
        const err = (data.errors || ['Unknown error']).join('; ');
        addMessage('system', 'Błąd: ' + err);
        setStatus('#f44336', 'Błąd');
      }
    } catch (err) {
      addMessage('system', 'Błąd połączenia: ' + err.message);
      setStatus('#f44336', 'Offline');
    } finally {
      isSending = false;
    }
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

        <div style="display:flex;flex-direction:column;height:calc(100vh - 220px);min-height:400px;gap:0.5rem;">

          <!-- Pasek statusu -->
          <div style="display:flex;gap:0.5rem;align-items:center;flex-wrap:wrap;font-size:0.75rem;color:var(--text-dim);padding:0.25rem 0;">
            <span id="chat-status" style="display:flex;align-items:center;gap:4px;">
              <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#666;" id="chat-indicator"></span>
              Gotowy
            </span>
            <span style="opacity:0.3;">|</span>
            <span id="chat-session">Sesja: ${sessionId.slice(0, 16)}</span>
            <span style="opacity:0.3;">|</span>
            <span id="chat-metrics"></span>
            <button onclick="location.hash='#cielingo-chat';location.reload();" 
                    style="margin-left:auto;background:none;border:1px solid var(--border);color:var(--text-dim);padding:2px 8px;border-radius:4px;cursor:pointer;font-size:0.7rem;">
              ↻ Nowa rozmowa
            </button>
          </div>

          <!-- Panel z wiadomościami + panelem bocznym -->
          <div style="display:flex;flex:1;gap:0.5rem;min-height:0;">

            <!-- Główny obszar czatu -->
            <div style="flex:2;display:flex;flex-direction:column;min-width:0;">

              <!-- Messages -->
              <div id="chat-messages" 
                   style="flex:1;overflow-y:auto;background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:0.75rem;font-family:var(--mono);font-size:0.8rem;line-height:1.5;">
                <div style="text-align:center;color:var(--text-dim);padding:2rem 1rem;font-family:var(--sans);">
                  <div style="font-size:1.2rem;font-weight:600;margin-bottom:0.5rem;">CIELingo</div>
                  <div style="font-size:0.85rem;">Cognitive-Intent Engine · Lingwistyka fazowa</div>
                  <div style="margin-top:1rem;font-size:0.75rem;opacity:0.6;">
                    Wyślij wiadomość aby rozpocząć rozmowę z CIEL.
                  </div>
                </div>
              </div>

              <!-- Input area -->
              <div style="display:flex;gap:0.5rem;margin-top:0.5rem;">
                <textarea id="chat-input" 
                          style="flex:1;resize:none;padding:0.6rem;border:1px solid var(--border);border-radius:6px;background:var(--bg-card);color:var(--text);font-family:var(--mono);font-size:0.8rem;min-height:44px;max-height:120px;"
                          placeholder="Napisz wiadomość do CIEL..." 
                          rows="2"></textarea>
                <button id="chat-send-btn" 
                        style="align-self:flex-end;padding:0.6rem 1.2rem;background:var(--accent);color:white;border:none;border-radius:6px;cursor:pointer;font-weight:600;white-space:nowrap;">
                  Wyślij
                </button>
              </div>
            </div>

            <!-- Panel boczny: CIELingo frame i CIEL state -->
            <div id="chat-sidebar" 
                 style="flex:1;display:flex;flex-direction:column;gap:0.5rem;min-width:240px;max-width:360px;overflow-y:auto;">

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