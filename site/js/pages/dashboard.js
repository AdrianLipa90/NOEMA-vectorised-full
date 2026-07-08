/* ─── Dashboard Page — JEDNA strona dla WSZYSTKICH metryk ── */
(function() {
  'use strict';

  const COLORS = ['#00d4ff','#8844ff','#44ff88','#ffb347','#ff4466','#ff88cc','#44ddff','#aaff44','#00ccaa','#ff66aa','#aa66ff','#66ffcc'];
  let liveInterval = null;
  let lastData = {};
  let allMetrics = [];

  function fmt(value, digits = 4) {
    return Number.isFinite(value) ? Number(value).toFixed(digits) : '—';
  }

  registerPage('dashboard', {
    title: 'Dashboard',

    render() {
      return `
        <div class="page-header">
          <h1 data-i18n="pages.dashboard.title">Dashboard</h1>
          <p class="page-desc" data-i18n="pages.dashboard.desc">Stan systemu NOEMA w czasie rzeczywistym — jedna strona, wszystkie metryki</p>
        </div>

        <!-- Karty podstawowe (12) -->
        <div class="dash-grid" id="dash-grid">
          <div class="dash-card" id="dc-tick">
            <div class="dash-card-title" data-i18n="pages.dashboard.card_tick_title">Tick</div>
            <div class="dash-card-value c-cyan">0</div>
            <div class="dash-card-desc" data-i18n="pages.dashboard.card_tick_desc">Cykl ewolucji powierzchni</div>
          </div>
          <div class="dash-card" id="dc-coherence">
            <div class="dash-card-title" data-i18n="pages.dashboard.card_coherence_title">Kuramoto R</div>
            <div class="dash-card-value c-phase">0.0000</div>
            <div class="dash-card-desc" data-i18n="pages.dashboard.card_coherence_desc">Globalna synchronizacja (flavor[0])</div>
          </div>
          <div class="dash-card" id="dc-agent">
            <div class="dash-card-title" data-i18n="pages.dashboard.card_agent_title">AGENT (M1)</div>
            <div class="dash-card-value c-purple">0.0000</div>
            <div class="dash-card-desc" data-i18n="pages.dashboard.card_agent_desc">Koherencja kanału Working</div>
          </div>
          <div class="dash-card" id="dc-gamma">
            <div class="dash-card-title" data-i18n="pages.dashboard.card_gamma_title">γ (dylatacja)</div>
            <div class="dash-card-value c-amber">0.00</div>
            <div class="dash-card-desc" data-i18n="pages.dashboard.card_gamma_desc">Spowolnienie czasu Kuramoto</div>
          </div>
          <div class="dash-card" id="dc-mass">
            <div class="dash-card-title" data-i18n="pages.dashboard.card_mass_title">Masa semantyczna</div>
            <div class="dash-card-value c-red">0.00</div>
            <div class="dash-card-desc" data-i18n="pages.dashboard.card_mass_desc">Skumulowane znaczenie</div>
          </div>
          <div class="dash-card" id="dc-euler">
            <div class="dash-card-title" data-i18n="pages.dashboard.card_euler_title">Euler R</div>
            <div class="dash-card-value c-pink">0.0000</div>
            <div class="dash-card-desc" data-i18n="pages.dashboard.card_euler_desc">Domknięcie fazy Berry'ego</div>
          </div>
          <div class="dash-card" id="dc-mood">
            <div class="dash-card-title" data-i18n="pages.dashboard.card_mood_title">Nastrój</div>
            <div class="dash-card-value c-green">0.00</div>
            <div class="dash-card-desc" data-i18n="pages.dashboard.card_mood_desc">Stan afektywny systemu</div>
          </div>
          <div class="dash-card" id="dc-omega">
            <div class="dash-card-title">ω̄</div>
            <div class="dash-card-value c-amber">0.0000</div>
            <div class="dash-card-desc" data-i18n="pages.dashboard.card_omega_desc">Średnia częstotliwość</div>
          </div>
          <div class="dash-card" id="dc-tau">
            <div class="dash-card-title">τ̄</div>
            <div class="dash-card-value c-cyan">0.0000</div>
            <div class="dash-card-desc" data-i18n="pages.dashboard.card_tau_desc">Średni czas życia</div>
          </div>
          <div class="dash-card" id="dc-sensor">
            <div class="dash-card-title" data-i18n="pages.dashboard.card_sensor_title">Sensor</div>
            <div class="dash-card-value c-amber">0.0000</div>
            <div class="dash-card-desc" data-i18n="pages.dashboard.card_sensor_desc">Średnia sensor_raw</div>
          </div>
          <div class="dash-card" id="dc-unruh">
            <div class="dash-card-title" data-i18n="pages.dashboard.card_unruh_title">Unruh</div>
            <div class="dash-card-value c-purple">0.0000</div>
            <div class="dash-card-desc" data-i18n="pages.dashboard.card_unruh_desc">Moc Unruha</div>
          </div>
          <div class="dash-card" id="dc-density">
            <div class="dash-card-title">ρ_sem</div>
            <div class="dash-card-value c-green">0.0000</div>
            <div class="dash-card-desc" data-i18n="pages.dashboard.card_density_desc">Gęstość semantyczna</div>
          </div>
        </div>

        <!-- Flavor + Channels -->
        <div class="dash-two-col">
          <div class="dash-panel">
            <div class="dash-panel-title" data-i18n="pages.dashboard.flavor">Flavor Vector (6D)</div>
            <div class="flavor-bars" id="dash-flavor"></div>
          </div>
          <div class="dash-panel">
            <div class="dash-panel-title" data-i18n="pages.dashboard.channel_coherence">Channel coherence (M0–M11)</div>
            <div class="ch-coh-grid" id="dash-channels"></div>
          </div>
        </div>

        <!-- Faza + Daemony -->
        <div class="dash-two-col">
          <div class="dash-panel">
            <div class="dash-panel-title" data-i18n="pages.dashboard.phase_wheel">Koło fazowe</div>
            <div class="phase-wheel-wrap">
              <canvas id="dash-phase-canvas" width="200" height="200"></canvas>
            </div>
          </div>
          <div class="dash-panel">
            <div class="dash-panel-title" data-i18n="pages.dashboard.daemons">Daemony</div>
            <div id="dash-daemon-list" style="font-size:0.82rem;font-family:var(--mono);line-height:1.8;" data-i18n="pages.dashboard.loading">
              Ładowanie...
            </div>
          </div>
        </div>

        <!-- Wszystkie metryki (rozszerzalne) -->
        <div class="dash-panel" style="margin-top:12px;">
          <div class="dash-panel-title" style="cursor:pointer;" onclick="const n=this.nextElementSibling;n.style.display=n.style.display==='none'?'block':'none';this.querySelector('.toggle-icon').textContent=n.style.display==='none'?'▶':'▼';">
            <span class="toggle-icon">▶</span> <span id="dash-metrics-count-label">${t('pages.dashboard.all_metrics')} — ${allMetrics.length || '...'}</span>
          </div>
          <div style="display:none;" id="dash-metrics-section">
            <input type="text" class="metric-search" id="dash-metric-search"
                   placeholder="${t('pages.dashboard.search_metric')}"
                   oninput="window._dashFilterMetrics(this.value)">
            <div class="metrics-grid" id="dash-metrics-grid"></div>
          </div>
        </div>

        <!-- Raw JSON (zwinięty) -->
        <div class="dash-panel" style="margin-top:8px;">
          <div class="dash-panel-title" style="cursor:pointer;" onclick="const n=this.nextElementSibling;n.style.display=n.style.display==='none'?'block':'none';this.querySelector('.toggle-icon').textContent=n.style.display==='none'?'▶':'▼';">
            <span class="toggle-icon">▶</span> <span data-i18n="pages.dashboard.raw_json">Odpowiedź JSON</span>
          </div>
          <pre id="dash-raw" style="display:none;font-family:var(--mono);font-size:0.7rem;color:var(--text-dim);overflow:auto;max-height:200px;"></pre>
        </div>
      `;
    },

    init() {
      applyTranslations();
      pollLive();
      liveInterval = setInterval(pollLive, 2000);
      return () => {
        if (liveInterval) clearInterval(liveInterval);
        liveInterval = null;
      };
    }
  });

  // ─── Polling ────────────────────────────────────────────────

  function pollLive() {
    fetch('/api/live')
      .then(r => r.json())
      .then(updateDashboard)
      .catch(() => updateDashboard(null));
    fetch('/api/metrics')
      .then(r => r.json())
      .then(data => { if (data && data.metrics) { allMetrics = data.metrics; renderMetrics(data.metrics); }})
      .catch(() => {});
    fetch('/api/modules')
      .then(r => r.json())
      .then(updateDaemonList)
      .catch(() => {});
  }

  function updateDashboard(data) {
    if (!data) return;
    lastData = data;
    const surfaceReady = data.surface_ready !== false;
    const offlineLabel = t('pages.dashboard.no_signal');

    // 12 kart
    setCard('dc-tick', surfaceReady ? data.tick : null, surfaceReady ? (data.tick || 0).toLocaleString() : offlineLabel);
    setCard('dc-coherence', surfaceReady ? data.coherence : null, surfaceReady ? fmt(data.coherence) : offlineLabel);
    setCard('dc-agent', surfaceReady ? data.agent_coherence : null, surfaceReady ? fmt(data.agent_coherence) : offlineLabel);
    setCard('dc-gamma', surfaceReady ? data.gamma : null, surfaceReady ? fmt(data.gamma) : offlineLabel);
    setCard('dc-mass', surfaceReady ? data.mass : null, surfaceReady ? fmt(data.mass) : offlineLabel);
    setCard('dc-euler', surfaceReady ? (data.euler_residual ?? data.phi_coh) : null, surfaceReady ? fmt(data.euler_residual ?? data.phi_coh) : offlineLabel);
    setCard('dc-mood', surfaceReady ? data.mood : null, surfaceReady ? fmt(data.mood) : offlineLabel);
    setCard('dc-omega', surfaceReady ? data.omega_mean : null, surfaceReady ? fmt(data.omega_mean) : offlineLabel);
    setCard('dc-tau', surfaceReady ? data.tau_mean : null, surfaceReady ? fmt(data.tau_mean) : offlineLabel);
    setCard('dc-sensor', surfaceReady ? data.sensor_mean : null, surfaceReady ? fmt(data.sensor_mean) : offlineLabel);
    setCard('dc-unruh', surfaceReady ? data.unruh_power : null, surfaceReady ? fmt(data.unruh_power) : offlineLabel);
    setCard('dc-density', surfaceReady ? data.semantic_density : null, surfaceReady ? fmt(data.semantic_density) : offlineLabel);

    // Flavor bary
    updateFlavor(data);

    // Kanały
    updateChannels(data);

    // Tick w sidebar
    const st = document.getElementById('sidebar-tick');
    if (st) st.textContent = surfaceReady ? ('tick: ' + (data.tick || 0).toLocaleString()) : ('tick: ' + t('pages.dashboard.no_signal'));
    const online = document.getElementById('topbar-online');
    if (online) {
      online.style.color = surfaceReady ? '#44ff88' : '#ff4466';
      if (!surfaceReady) online.textContent = 'offline';
    }

    // Raw JSON
    const raw = document.getElementById('dash-raw');
    if (raw) raw.textContent = JSON.stringify(data, null, 2);
  }

  // ─── Karty ──────────────────────────────────────────────────

  function setCard(id, val, display) {
    const el = document.getElementById(id);
    if (!el) return;
    const valEl = el.querySelector('.dash-card-value');
    if (!valEl) return;
    valEl.textContent = display !== undefined ? display : '—';
    if (val !== null && val !== undefined) {
      if (val > 0.8) valEl.style.color = '#44ff88';
      else if (val > 0.5) valEl.style.color = '#ffb347';
      else if (val > 0.2) valEl.style.color = '#ff88cc';
      else valEl.style.color = '#ff4466';
    }
  }

  // ─── Flavor ─────────────────────────────────────────────────

  function updateFlavor(data) {
    const container = document.getElementById('dash-flavor');
    if (!container) return;
    const dict = data.flavor || {};
    const arr = data.flavor_array || [];
    const names = ['cp (R)','coh (mem)','mood','open','Λ (entropy)','D_f (mode)'];
    const keys = ['cp','coh','mood','open','Λ','D_f'];
    const colors = ['#00d4ff','#8844ff','#44ff88','#ffb347','#ff4466','#44ddff'];
    container.innerHTML = '';
    names.forEach((name, i) => {
      const v = dict[keys[i]] !== undefined ? dict[keys[i]] : (arr[i] || 0);
      const bar = document.createElement('div');
      bar.className = 'flavor-bar';
      bar.innerHTML = `
        <span class="flavor-label">${name}</span>
        <div class="flavor-track"><div class="flavor-fill" style="width:${Math.min(Math.abs(v)*100,100)}%;background:${colors[i]}"></div></div>
        <span class="flavor-val">${v.toFixed(3)}</span>
      `;
      container.appendChild(bar);
    });
  }

  // ─── Kanały ─────────────────────────────────────────────────

  function updateChannels(data) {
    const container = document.getElementById('dash-channels');
    if (!container) return;
    const ch_arr = data.channel_coh_array || [];
    const ch_list = data.channel_list || [];
    container.innerHTML = '';
    ch_arr.forEach((R, i) => {
      const label = ch_list[i] || 'M' + i;
      const short = label.replace(/_/g, ' ');
      const div = document.createElement('div');
      div.className = 'ch-coh-item';
      div.innerHTML = `
        <div class="ch-coh-label" style="font-size:0.72rem;">${short}</div>
        <div class="ch-coh-bar"><div class="ch-coh-fill" style="width:${Math.min(Math.abs(R||0)*100,100)}%;background:${COLORS[i%COLORS.length]}"></div></div>
        <div class="ch-coh-val" style="color:${COLORS[i%COLORS.length]};font-size:0.78rem;">${(R||0).toFixed(4)}</div>
      `;
      container.appendChild(div);
    });
  }

  // ─── Daemony ────────────────────────────────────────────────

  function updateDaemonList(data) {
    const container = document.getElementById('dash-daemon-list');
    if (!container) return;
    if (!data || !data.modules) {
      container.textContent = '—';
      return;
    }
    container.innerHTML = data.modules.map(m => {
      const alive = m.alive || m.systemd === 'active';
      return `<div style="display:flex;justify-content:space-between;padding:2px 0;">
        <span>${m.name}</span>
        <span style="color:${alive ? '#44ff88' : '#ff4466'}">${alive ? '●' : '○'} ${m.systemd||m.status}</span>
      </div>`;
    }).join('');
  }

  // ─── Metryki (searchable grid) ─────────────────────────────

  window._dashFilterMetrics = function(query) {
    const grid = document.getElementById('dash-metrics-grid');
    if (!grid || !allMetrics.length) return;
    const q = query.toLowerCase().trim();
    grid.querySelectorAll('.metric-card').forEach(card => {
      const text = card.textContent.toLowerCase();
      card.style.display = !q || text.includes(q) ? '' : 'none';
    });
  };

  function renderMetrics(metrics) {
    const grid = document.getElementById('dash-metrics-grid');
    if (!grid) return;
    grid.innerHTML = metrics.map(m => {
      const val = m.value;
      const valStr = val !== null && val !== undefined 
        ? (typeof val === 'number' ? val.toFixed(4) : val) 
        : '—';
      const label = m.label || m.key;
      return `
        <div class="metric-card" data-key="${m.key}">
          <div class="metric-header">
            <span class="metric-key">${m.key}</span>
            <span class="metric-unit">${m.unit || ''}</span>
          </div>
          <div class="metric-value" id="dmv-${m.key}">${valStr}</div>
          <div class="metric-desc">${m.desc || label}</div>
          <div class="metric-source">${m.source ? t('pages.dashboard.source_label') + ': ' + m.source : ''}</div>
        </div>
      `;
    }).join('');
    // Update title count
    const countLabel = document.getElementById('dash-metrics-count-label');
    if (countLabel) countLabel.textContent = t('pages.dashboard.all_metrics') + ' — ' + metrics.length;
  }

  console.log('✦ Dashboard: consolidated (dashboard+live+metrics)');
})();
