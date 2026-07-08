/* ─── Preferences Page — konfiguracja NOEMY i stan CIEL ── */
(function() {
  'use strict';

  const CONFIG_DESCRIPTIONS = {
    surface_path: 'Ścieżka do pamięci współdzielonej mmap',
    analog_bus_path: 'Magistrala analogowa PhaseNav',
    num_oscillators: 'Liczba oscylatorów HTRI'
  };
  const DEFAULT_DESC = 'Parametr konfiguracyjny NOEMY';

  registerPage('preferences', {
    title: 'Preferencje NOEMY',

    render() {
      return `
        <div class="page-header">
          <h1>Preferencje NOEMY</h1>
          <p class="page-desc">Konfiguracja systemu i stan CIEL — dane rzeczywiste</p>
        </div>

        <div class="dash-panel">
          <div class="dash-panel-title">Konfiguracja systemu</div>
          <div id="pref-config" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:0.82rem;">
            Ładowanie konfiguracji...
          </div>
        </div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">Stan CIEL</div>
          <div id="pref-ciel" style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;font-size:0.82rem;">
            Ładowanie stanu CIEL...
          </div>
        </div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title" style="cursor:pointer;" onclick="const n=this.nextElementSibling;n.style.display=n.style.display==='none'?'block':'none';this.querySelector('.toggle-icon').textContent=n.style.display==='none'?'▶':'▼';">
            <span class="toggle-icon">▶</span> Odpowiedź JSON
          </div>
          <pre id="pref-raw" style="display:none;font-family:var(--mono);font-size:0.7rem;color:var(--text-dim);overflow:auto;max-height:200px;"></pre>
        </div>
      `;
    },

    init() {
      applyTranslations();
      fetchSettings();
      fetchCiel();
      const iv = setInterval(fetchCiel, 10000);
      return () => clearInterval(iv);
    }
  });

  let lastSettings = null;
  let lastCiel = null;

  function fetchSettings() {
    fetch('/api/settings')
      .then(r => r.json())
      .then(d => { lastSettings = d; renderConfig(d); updateRaw(); })
      .catch(() => {});
  }

  function fetchCiel() {
    fetch('/api/ciel/state')
      .then(r => r.json())
      .then(d => {
        const state = d.state || d;
        const unwrapped = state.state || state;
        lastCiel = unwrapped;
        renderCiel(unwrapped);
        updateRaw();
      })
      .catch(() => {});
  }

  function updateRaw() {
    const el = document.getElementById('pref-raw');
    if (!el) return;
    el.textContent = JSON.stringify({ settings: lastSettings, ciel_state: lastCiel }, null, 2);
  }

  function renderConfig(data) {
    const el = document.getElementById('pref-config');
    if (!el) return;
    if (!data || typeof data !== 'object') {
      el.innerHTML = '<span style="color:var(--muted)">Brak danych konfiguracji</span>';
      return;
    }
    const entries = Object.entries(data).filter(([k]) => typeof k === 'string' && k !== 'last_updated');
    const html = entries.map(([key, val]) => {
      const desc = CONFIG_DESCRIPTIONS[key] || DEFAULT_DESC;
      const display = typeof val === 'object' ? JSON.stringify(val) : String(val);
      return `
        <div class="dash-card">
          <div class="dash-card-title">${key}</div>
          <div class="dash-card-value c-cyan" style="font-size:0.78rem;word-break:break-all;">${display}</div>
          <div class="dash-card-desc">${desc}</div>
        </div>
      `;
    }).join('');
    el.innerHTML = html || '<span style="color:var(--muted)">Brak wpisów konfiguracji</span>';
  }

  function renderCiel(data) {
    const el = document.getElementById('pref-ciel');
    if (!el) return;
    if (!data) {
      el.innerHTML = '<span style="color:var(--muted)">Brak danych stanu CIEL</span>';
      return;
    }
    const mode = data.operating_mode || '—';
    const modeColor = mode === 'deep' ? '#44ff88' : mode === 'standard' ? '#ffb347' : '#ff4466';
    el.innerHTML = `
      <div class="dash-card">
        <div class="dash-card-title">Coherence Index</div>
        <div class="dash-card-value ${(data.coherence_index || 0) > 0.767 ? 'c-green' : (data.coherence_index || 0) > 0.5 ? 'c-amber' : 'c-red'}">${(data.coherence_index || 0).toFixed(4)}</div>
        <div class="dash-card-desc">Spójność tożsamości</div>
      </div>
      <div class="dash-card">
        <div class="dash-card-title">Soul Invariant</div>
        <div class="dash-card-value ${(data.soul_invariant || 0) > 0.5 ? 'c-green' : 'c-red'}">${(data.soul_invariant || 0).toFixed(4)}</div>
        <div class="dash-card-desc">Niezmiennik duszy</div>
      </div>
      <div class="dash-card">
        <div class="dash-card-title">Ethical Score</div>
        <div class="dash-card-value ${(data.ethical_score || 0) > 0.6 ? 'c-green' : (data.ethical_score || 0) > 0.4 ? 'c-amber' : 'c-red'}">${(data.ethical_score || 0).toFixed(4)}</div>
        <div class="dash-card-desc">Wynik etyczny</div>
      </div>
      <div class="dash-card">
        <div class="dash-card-title">Mood</div>
        <div class="dash-card-value ${(data.mood_normalized || 0) > 0.5 ? 'c-green' : 'c-amber'}">${(data.mood_normalized || 0).toFixed(4)}</div>
        <div class="dash-card-desc">Stan afektywny</div>
      </div>
      <div class="dash-card">
        <div class="dash-card-title">Openness</div>
        <div class="dash-card-value c-purple">${(data.openness || 0).toFixed(4)}</div>
        <div class="dash-card-desc">Otwartość systemu</div>
      </div>
      <div class="dash-card">
        <div class="dash-card-title">Operating Mode</div>
        <div class="dash-card-value" style="color:${modeColor}">${mode}</div>
        <div class="dash-card-desc">Tryb pracy CIEL</div>
      </div>
    `;
  }

  console.log('✦ Page: Preferences loaded');
})();
