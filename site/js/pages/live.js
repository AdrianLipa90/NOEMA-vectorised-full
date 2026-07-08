/* ─── Live Page — prawdziwy dashboard, nie JSON string ──────── */
(function() {
  'use strict';

  const COLORS = ['#00d4ff','#8844ff','#44ff88','#ffb347','#ff4466','#ff88cc','#44ddff','#aaff44'];
  let liveInterval = null;

  registerPage('live', {
    title: 'Live',

    render() {
      return `
        <div class="page-header">
          <h1>Live Dashboard</h1>
          <p class="page-desc">Stan NOEMY w czasie rzeczywistym — wszystkie kanały powierzchniowe</p>
        </div>
        <div class="live-grid" id="live-grid">
          <!-- Primary cards -->
          <div class="dash-card" id="lc-tick">
            <div class="dash-card-title">Tick</div>
            <div class="dash-card-value c-cyan">0</div>
            <div class="dash-card-desc">Cykl ewolucji</div>
          </div>
          <div class="dash-card" id="lc-coherence">
            <div class="dash-card-title">Kuramoto R</div>
            <div class="dash-card-value c-phase">0.0000</div>
            <div class="dash-card-desc">Globalna synchronizacja (flavor[0])</div>
          </div>
          <div class="dash-card" id="lc-agent">
            <div class="dash-card-title">AGENT (M1)</div>
            <div class="dash-card-value c-purple">0.0000</div>
            <div class="dash-card-desc">Koherencja M1_Working</div>
          </div>
          <div class="dash-card" id="lc-gamma">
            <div class="dash-card-title">γ (dylatacja)</div>
            <div class="dash-card-value c-amber">0.00</div>
            <div class="dash-card-desc">Spowolnienie τ</div>
          </div>
          <div class="dash-card" id="lc-mass">
            <div class="dash-card-title">Masa</div>
            <div class="dash-card-value c-red">0.00</div>
            <div class="dash-card-desc">Semantyczna masa</div>
          </div>
          <div class="dash-card" id="lc-mood">
            <div class="dash-card-title">Nastrój</div>
            <div class="dash-card-value c-green">0.00</div>
            <div class="dash-card-desc">Stan afektywny</div>
          </div>
          <div class="dash-card" id="lc-euler">
            <div class="dash-card-title">Euler R</div>
            <div class="dash-card-value c-pink">0.0000</div>
            <div class="dash-card-desc">Berry phase closure</div>
          </div>
          <div class="dash-card" id="lc-omega">
            <div class="dash-card-title">ω̄</div>
            <div class="dash-card-value c-amber">0.00</div>
            <div class="dash-card-desc">Średnia częstotliwość</div>
          </div>
          <div class="dash-card" id="lc-tau">
            <div class="dash-card-title">τ̄</div>
            <div class="dash-card-value c-cyan">0.00</div>
            <div class="dash-card-desc">Średni czas życia</div>
          </div>
          <div class="dash-card" id="lc-sensor">
            <div class="dash-card-title">Sensor</div>
            <div class="dash-card-value c-amber">0.0000</div>
            <div class="dash-card-desc">Średnia sensor_raw</div>
          </div>
          <div class="dash-card" id="lc-unruh">
            <div class="dash-card-title">Unruh</div>
            <div class="dash-card-value c-purple">0.0000</div>
            <div class="dash-card-desc">Moc Unruha</div>
          </div>
          <div class="dash-card" id="lc-density">
            <div class="dash-card-title">ρ_sem</div>
            <div class="dash-card-value c-green">0.0000</div>
            <div class="dash-card-desc">Gęstość semantyczna</div>
          </div>

          <!-- Flavor bars -->
          <div class="dash-panel" style="grid-column:span 3;">
            <div class="dash-panel-title">Flavor Vector (6D)</div>
            <div class="flavor-bars" id="lc-flavor"></div>
          </div>

          <!-- Channel coherence (12 kanałów) -->
          <div class="dash-panel" style="grid-column:span 4;">
            <div class="dash-panel-title">Channel coherence (M0–M11)</div>
            <div class="ch-coh-grid" id="lc-channels"></div>
          </div>

          <!-- Daemons -->
          <div class="dash-panel" style="grid-column:span 2;">
            <div class="dash-panel-title">Daemons</div>
            <div id="lc-daemon-list" style="font-family:var(--mono);font-size:0.82rem;line-height:1.8;">Ładowanie...</div>
          </div>

          <!-- Surowy JSON (zwinięty) -->
          <div class="dash-panel" style="grid-column:1/-1;">
            <div class="dash-panel-title" style="cursor:pointer" onclick="const n=this.nextElementSibling;n.style.display=n.style.display==='none'?'block':'none';">Raw JSON ▶</div>
            <pre id="lc-raw" style="display:none;font-family:var(--mono);font-size:0.7rem;color:var(--text-dim);overflow:auto;max-height:300px;"></pre>
          </div>
        </div>
        <style>
          .live-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;padding:12px 0;}
          .live-grid .dash-card{grid-column:span 1;}
          @media(max-width:900px){.live-grid{grid-template-columns:repeat(3,1fr);}}
        </style>
      `;
    },

    init() {
      applyTranslations();
      pollLive();
      liveInterval = setInterval(pollLive, 2000);
      return () => { if (liveInterval) clearInterval(liveInterval); };
    }
  });

  function pollLive() {
    fetch('/api/live')
      .then(r => r.json())
      .then(updateLive)
      .catch(() => {});
    fetch('/api/modules')
      .then(r => r.json())
      .then(updateDaemonList)
      .catch(() => {});
  }

  function updateLive(data) {
    if (!data) return;
    const surfaceReady = data.surface_ready !== false;
    const offlineLabel = 'brak sygnału';

    // Karty
    setLiveCard('lc-tick', surfaceReady ? data.tick : null, surfaceReady ? (data.tick || 0).toLocaleString() : offlineLabel);
    setLiveCard('lc-coherence', surfaceReady ? data.coherence : null, surfaceReady ? (data.coherence || 0).toFixed(4) : offlineLabel);
    setLiveCard('lc-agent', surfaceReady ? data.agent_coherence : null, surfaceReady ? (data.agent_coherence || 0).toFixed(4) : offlineLabel);
    setLiveCard('lc-gamma', surfaceReady ? data.gamma : null, surfaceReady ? (data.gamma ? data.gamma.toFixed(4) : '—') : offlineLabel);
    setLiveCard('lc-mass', surfaceReady ? data.mass : null, surfaceReady ? (data.mass ? data.mass.toFixed(4) : '—') : offlineLabel);
    setLiveCard('lc-mood', surfaceReady ? data.mood : null, surfaceReady ? (data.mood ? data.mood.toFixed(4) : '—') : offlineLabel);
    setLiveCard('lc-euler', surfaceReady ? data.euler_residual : null, surfaceReady ? (data.euler_residual || 0).toFixed(4) : offlineLabel);
    setLiveCard('lc-omega', surfaceReady ? data.omega_mean : null, surfaceReady ? (data.omega_mean ? data.omega_mean.toFixed(4) : '—') : offlineLabel);
    setLiveCard('lc-tau', surfaceReady ? data.tau_mean : null, surfaceReady ? (data.tau_mean ? data.tau_mean.toFixed(4) : '—') : offlineLabel);
    setLiveCard('lc-sensor', surfaceReady ? data.sensor_mean : null, surfaceReady ? (data.sensor_mean || 0).toFixed(4) : offlineLabel);
    setLiveCard('lc-unruh', surfaceReady ? data.unruh_power : null, surfaceReady ? (data.unruh_power || 0).toFixed(4) : offlineLabel);
    setLiveCard('lc-density', surfaceReady ? data.semantic_density : null, surfaceReady ? (data.semantic_density || 0).toFixed(4) : offlineLabel);

    // Flavor
    updateLiveFlavor(data);

    // Channels
    updateLiveChannels(data);

    // Raw JSON
    const rawEl = document.getElementById('lc-raw');
    if (rawEl) rawEl.textContent = JSON.stringify(data, null, 2);
  }

  function setLiveCard(id, val, display) {
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

  function updateLiveFlavor(data) {
    const container = document.getElementById('lc-flavor');
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

  function updateLiveChannels(data) {
    const container = document.getElementById('lc-channels');
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

  function updateDaemonList(data) {
    const container = document.getElementById('lc-daemon-list');
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

  console.log('✦ Live page: loaded');
})();
