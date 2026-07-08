/* ─── Memory Page — CIEL memory system M0–M11 + CIELingo wątki ── */
(function() {
  'use strict';

  const CHANNELS = [
    { id: 'M0_Perceptual',      label: 'M0_Perceptual',      desc: 'Percepcja — wrażenia zmysłowe i strumień surowych danych' },
    { id: 'M1_Working',         label: 'M1_Working',         desc: 'Pamięć robocza — aktywna manipulacja i AGENT' },
    { id: 'M2_Episodic',        label: 'M2_Episodic',        desc: 'Epizodyczna — zdarzenia i osobiste doświadczenia' },
    { id: 'M3_Semantic',        label: 'M3_Semantic',        desc: 'Semantyczna — wiedza ogólna i znaczenia' },
    { id: 'M4_Procedural',      label: 'M4_Procedural',      desc: 'Proceduralna — umiejętności i nawyki' },
    { id: 'M5_AffectiveEthical',label: 'M5_AffectiveEthical',desc: 'Afektywno-etyczna — emocje i wartości moralne' },
    { id: 'M6_Identity',        label: 'M6_Identity',        desc: 'Tożsamość — samoświadomość i jaźń' },
    { id: 'M7_Braid_Invariant', label: 'M7_Braid_Invariant', desc: 'Braid_Invariant — niezmienniki splotów i topologia' },
    { id: 'M8_Meta',            label: 'M8_Meta',            desc: 'Meta — metapamięć i monitoring poznawczy' },
    { id: 'M9_Temporal',        label: 'M9_Temporal',        desc: 'Temporalna — czas subiektywny i następstwo zdarzeń' },
    { id: 'M10_Imaginal',       label: 'M10_Imaginal',       desc: 'Imaginalna — wyobraźnia i symulacje mentalne' },
    { id: 'M11_Quantum',        label: 'M11_Quantum',        desc: 'Kwantowa — superpozycja stanów i splątanie' },
  ];

  const COLORS = ['#00d4ff','#8844ff','#44ff88','#ffb347','#ff4466','#ff88cc','#44ddff','#aaff44','#00ccaa','#ff66aa','#aa66ff','#66ffcc'];
  let liveInterval = null;
  let threadInterval = null;

  registerPage('memory', {
    title: 'Pamięć CIEL',

    render() {
      return `
        <div class="page-header">
          <h1>Pamięć CIEL — kanały M0–M11</h1>
          <p class="page-desc">Koherencja kanałów pamięci i wątki CIELingo w czasie rzeczywistym</p>
        </div>

        <div class="dash-panel">
          <div class="dash-panel-title">Koherencja kanałów M0–M11</div>
          <div class="dash-grid" id="memory-ch-grid">
            ${CHANNELS.map((ch, i) => `
              <div class="dash-card memory-card" id="mem-${ch.id}">
                <div class="dash-card-title">${ch.label}</div>
                <div class="dash-card-value" style="color:${COLORS[i]}">—</div>
                <div class="dash-card-desc">${ch.desc}</div>
              </div>
            `).join('')}
          </div>
        </div>

        <div class="dash-panel" style="margin-top:16px;">
          <div class="dash-panel-title">Wątki CIELingo</div>
          <div id="memory-thread-list" style="font-family:var(--mono);font-size:0.82rem;line-height:1.6;">
            Ładowanie...
          </div>
        </div>

        <div class="dash-panel" style="margin-top:8px;">
          <div class="dash-panel-title" style="cursor:pointer;" onclick="const n=this.nextElementSibling;n.style.display=n.style.display==='none'?'block':'none';this.querySelector('.toggle-icon').textContent=n.style.display==='none'?'▶':'▼';">
            <span class="toggle-icon">▶</span> Odpowiedź JSON
          </div>
          <pre id="memory-raw" style="display:none;font-family:var(--mono);font-size:0.7rem;color:var(--text-dim);overflow:auto;max-height:200px;"></pre>
        </div>
      `;
    },

    init() {
      applyTranslations();
      pollLive();
      pollThread();
      liveInterval = setInterval(pollLive, 5000);
      threadInterval = setInterval(pollThread, 5000);
      return () => {
        if (liveInterval) clearInterval(liveInterval);
        if (threadInterval) clearInterval(threadInterval);
        liveInterval = null;
        threadInterval = null;
      };
    }
  });

  function pollLive() {
    fetch('/api/live')
      .then(r => r.json())
      .then(updateChannels)
      .catch(() => {});
  }

  function pollThread() {
    fetch('/api/cielingo/thread')
      .then(r => r.json())
      .then(updateThread)
      .catch(() => {});
  }

  function updateChannels(data) {
    if (!data) return;
    const ch = data.channel_coh || {};
    CHANNELS.forEach(chInfo => {
      const val = ch[chInfo.id];
      const el = document.getElementById('mem-' + chInfo.id);
      if (!el) return;
      const valEl = el.querySelector('.dash-card-value');
      if (!valEl) return;
      if (val !== undefined && val !== null) {
        valEl.textContent = val.toFixed(4);
        if (val > 0.8) valEl.style.color = '#44ff88';
        else if (val > 0.5) valEl.style.color = '#ffb347';
        else if (val > 0.2) valEl.style.color = '#ff88cc';
        else valEl.style.color = '#ff4466';
      } else {
        valEl.textContent = '—';
        valEl.style.color = COLORS[CHANNELS.indexOf(chInfo) % COLORS.length];
      }
    });

    const raw = document.getElementById('memory-raw');
    if (raw) raw.textContent = JSON.stringify(data, null, 2);
  }

  function updateThread(data) {
    const container = document.getElementById('memory-thread-list');
    if (!container) return;

    if (!data || (Array.isArray(data) && data.length === 0)) {
      container.innerHTML = '<span style="color:var(--text-dim)">Brak wpisów w wątku.</span>';
      return;
    }

    const entries = Array.isArray(data) ? data : (data.entries || data.messages || data.thread || []);
    if (!entries.length) {
      container.innerHTML = '<span style="color:var(--text-dim)">Brak wpisów w wątku.</span>';
      return;
    }

    container.innerHTML = entries.map(entry => {
      const ts = entry.timestamp || entry.created_at || '';
      const role = entry.role || 'system';
      const content = entry.content || entry.text || entry.message || JSON.stringify(entry);
      const roleColor = role === 'user' ? '#44ddff' : role === 'assistant' ? '#44ff88' : '#888';
      return `
        <div style="padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.06);">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="color:${roleColor};font-weight:bold;">[${role}]</span>
            <span style="color:var(--text-dim);font-size:0.7rem;">${ts}</span>
          </div>
          <div style="margin-top:2px;color:var(--text);white-space:pre-wrap;word-break:break-word;">${escHtml(content)}</div>
        </div>
      `;
    }).join('');
  }

  function escHtml(s) {
    if (!s) return '';
    const d = document.createElement('div');
    d.textContent = typeof s === 'string' ? s.slice(0, 2000) : String(s).slice(0, 2000);
    return d.innerHTML;
  }

  console.log('✦ Memory page loaded (M0–M11 + CIELingo thread)');
})();
