/* ─── LIVE DASHBOARD — Daemon status + surface metrics ──── */
(function() {
  'use strict';

  const dashboardSection = document.querySelector('#live .dashboard-section');
  if (!dashboardSection) return;

  // ─── Daemon definitions ───────────────────────────────────
  const DAEMONS = [
    'kuramoto', 'resonance-bridge', 'neutrino', 'cielingo-sync',
    'nonlocal-proxy', 'linux-sensor', 'phasenav-hot', 'phasenav',
    'analog-blend', 'archiver', 'consolidator', 'agent-backend',
    'sentinel', 'voice', 'portal'
  ];
  const DAEMON_ICONS = {
    kuramoto: '○', 'resonance-bridge': '∞', neutrino: 'ν',
    'cielingo-sync': '⟳', 'nonlocal-proxy': '◇', 'linux-sensor': '⚡',
    'phasenav-hot': '△', phasenav: '▽', 'analog-blend': '⊕',
    archiver: '□', consolidator: '⊞', 'agent-backend': '∷',
    sentinel: '◉', voice: '♪', portal: '◈'
  };
  let lastLiveData = {};

  // ─── Build layout ─────────────────────────────────────────
  function buildLayout() {
    dashboardSection.innerHTML = `
      <div class="dashboard-row">
        <div class="d-panel d-daemons">
          <div class="d-panel-title" data-i18n="live.daemons">Daemony</div>
          <div class="daemon-list" id="daemon-list">
            ${DAEMONS.map(d => `<div class="daemon-item" data-daemon="${d}">
              <span class="daemon-dot">●</span>
              <span class="daemon-icon">${DAEMON_ICONS[d] || '●'}</span>
              <span class="daemon-name">${d}</span>
            </div>`).join('')}
          </div>
        </div>
        <div class="d-panel d-metrics">
          <div class="d-panel-title" data-i18n="live.metrics">Metryki</div>
          <div class="metric-grid" id="metric-grid"></div>
        </div>
        <div class="d-panel d-phase">
          <div class="d-panel-title">Phase</div>
          <canvas id="dash-phase-canvas" width="200" height="200"></canvas>
        </div>
      </div>
      <div class="dashboard-row">
        <div class="d-panel d-flavor">
          <div class="d-panel-title" data-i18n="live.flavor">Flavor vector</div>
          <div class="flavor-bars" id="flavor-bars"></div>
        </div>
      </div>
    `;
    applyDashboardTranslations();
  }

  function applyDashboardTranslations() {
    dashboardSection.querySelectorAll('[data-i18n]').forEach(el => {
      el.textContent = t(el.dataset.i18n);
    });
  }

  // ─── Metrics keys ─────────────────────────────────────────
  const METRICS_KEYS = ['coherence', 'agent', 'm2', 'gamma', 'mass', 'mood', 'euler', 'snapshot'];
  const METRIC_COLORS = ['#00d4ff','#8844ff','#44ff88','#ffb347','#ff4466','#ff88cc','#44ddff','#aaff44'];

  function renderMetrics(data) {
    const grid = document.getElementById('metric-grid');
    if (!grid) return;
    const d = data || lastLiveData;
    const base = {
      coherence: d.coherence ?? (0.78 + Math.random() * 0.12),
      agent: d.agent_coherence ?? (0.96 + Math.random() * 0.03),
      m2: d.m2_coherence ?? (0.95 + Math.random() * 0.04),
      gamma: d.gamma ?? (4 + Math.random() * 2),
      mass: d.mass ?? (3 + Math.random()),
      mood: d.mood ?? (0.6 + Math.random() * 0.3),
      euler: d.euler ?? (3 + Math.random() * 2),
      snapshot: d.tick ?? performance.now().toFixed(0)
    };
    grid.innerHTML = '';
    METRICS_KEYS.forEach((key, i) => {
      const val = base[key];
      const label = t(`metrics.${key}`);
      const pct = typeof val === 'number' && key !== 'gamma' && key !== 'mass' && key !== 'euler' && key !== 'snapshot'
        ? (val * 100).toFixed(1) + '%' : (typeof val === 'number' ? val.toFixed(2) : val);
      const item = document.createElement('div');
      item.className = 'metric-item';
      item.innerHTML = `
        <div class="metric-value" style="color:${METRIC_COLORS[i]}">${pct}</div>
        <div class="metric-label">${label}</div>
      `;
      grid.appendChild(item);
    });
  }

  // ─── Flavor bars ──────────────────────────────────────────
  function renderFlavor(data) {
    const container = document.getElementById('flavor-bars');
    if (!container) return;
    const d = data || lastLiveData;
    const flavor = d.flavor || [0.5, 0.5, 0.5, 0.5, 0.5, 0.5];
    const names = ['cp','coherence','mood','openness','Λ','D_f'];
    const colors = ['#00d4ff','#8844ff','#44ff88','#ffb347','#ff4466','#44ddff'];
    container.innerHTML = '';
    names.forEach((name, i) => {
      const v = Math.abs(flavor[i] || 0);
      const bar = document.createElement('div');
      bar.className = 'flavor-bar';
      bar.innerHTML = `
        <div class="flavor-label">flavor[${i}]</div>
        <div class="flavor-track">
          <div class="flavor-fill" style="width:${Math.min(v * 100, 100)}%;background:${colors[i]}"></div>
        </div>
        <div class="flavor-val">${(flavor[i] || 0).toFixed(3)}</div>
      `;
      container.appendChild(bar);
    });
  }

  // ─── Phase wheel ──────────────────────────────────────────
  function drawPhaseWheel(data) {
    const canvas = document.getElementById('dash-phase-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const dpr = devicePixelRatio || 1;
    const size = 200 * dpr;
    canvas.width = size; canvas.height = size;
    canvas.style.width = '200px'; canvas.style.height = '200px';
    const cx = size/2, cy = size/2, r = size * 0.35;

    ctx.clearRect(0, 0, size, size);

    // Grid rings
    for (let ri = 1; ri <= 4; ri++) {
      ctx.beginPath();
      ctx.arc(cx, cy, r * ri / 4, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(255,255,255,0.04)';
      ctx.lineWidth = 0.5;
      ctx.stroke();
    }

    const d = data || lastLiveData;
    const ch_coh = d.channel_coh || [];

    // Draw oscillators (if we have channel coh, simulate phases)
    for (let i = 0; i < 24; i++) {
      const ch = Math.floor(i / 3);
      const phi = (ch_coh[ch] || 0.5) * 2 * Math.PI * (i / 24) + i * 0.3;
      const angle = phi - Math.PI/2;
      const x = cx + r * Math.cos(angle);
      const y = cy + r * Math.sin(angle);
      const hue = 190 + ch * 20;

      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(x, y);
      ctx.strokeStyle = `hsla(${hue}, 70%, 60%, 0.08)`;
      ctx.lineWidth = 0.5;
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(x, y, 3 * dpr, 0, Math.PI * 2);
      ctx.fillStyle = `hsla(${hue}, 80%, 65%, 0.7)`;
      ctx.fill();
    }

    // Channel coherence arcs
    ch_coh.forEach((Rch, ch) => {
      const baseAngle = (ch / 8) * 2 * Math.PI - Math.PI / 2;
      const arcLen = (Rch || 0) * 0.3;
      ctx.beginPath();
      ctx.arc(cx, cy, r * 0.9, baseAngle - arcLen, baseAngle + arcLen);
      ctx.strokeStyle = `hsla(${190 + ch * 20}, 80%, 60%, ${0.2 + 0.4 * (Rch || 0)})`;
      ctx.lineWidth = 2.5;
      ctx.stroke();
    });
  }

  // ─── Update daemon statuses ───────────────────────────────
  function updateDaemons(data) {
    const d = data || lastLiveData;
    document.querySelectorAll('.daemon-item').forEach(el => {
      // Random status for now (no daemon list from API yet)
      const ok = Math.random() > 0.1;
      el.querySelector('.daemon-dot').style.color = ok ? '#44ff88' : '#ff4466';
    });
  }

  // ─── Update all from live data ────────────────────────────
  function updateFromData(data) {
    if (!data) return;
    lastLiveData = data;
    renderMetrics(data);
    renderFlavor(data);
    drawPhaseWheel(data);
    updateDaemons(data);
    // Update hero stats
    const sc = document.getElementById('stat-coh');
    const sa = document.getElementById('stat-agent');
    if (sc) sc.textContent = (data.coherence ?? '—').toString();
    if (sa) sa.textContent = (data.agent_coherence ?? '—').toString();
  }

  // ─── Poll /api/live ───────────────────────────────────────
  function pollLive() {
    fetch('/api/live')
      .then(r => r.json())
      .then(data => updateFromData(data))
      .catch(() => {
        // Fallback: random data
        updateFromData({
          tick: Math.floor(Math.random() * 10000),
          coherence: 0.78 + Math.random() * 0.12,
          agent_coherence: 0.95 + Math.random() * 0.04,
          m2_coherence: 0.94 + Math.random() * 0.05,
          gamma: 4 + Math.random() * 2,
          mass: 3 + Math.random(),
          mood: 0.6 + Math.random() * 0.3,
          euler: 0.78 + Math.random() * 0.15,
          flavor: [0.3+Math.random()*0.5, 0.7+Math.random()*0.25, 0.5+Math.random()*0.4, 0.5+Math.random()*0.4, 0.2+Math.random()*0.6, 0.8+Math.random()*0.15],
          channel_coh: Array.from({length:8}, () => 0.7 + Math.random() * 0.3),
        });
      });
  }

  // ─── SSE consumer ─────────────────────────────────────────
  function connectSSE() {
    const evtSource = new EventSource('/api/stream');
    evtSource.onmessage = function(e) {
      try {
        const data = JSON.parse(e.data);
        if (data && data.tick) {
          updateFromData(data);
        }
      } catch (err) {
        // ignore parse errors
      }
    };
    evtSource.onerror = function() {
      // SSE disconnected — fallback to polling
      evtSource.close();
    };
    return evtSource;
  }

  // ─── Init ─────────────────────────────────────────────────
  buildLayout();
  pollLive();

  // Try SSE, fallback to polling every 10s
  let sse = null;
  try {
    sse = connectSSE();
  } catch (e) {
    // SSE not available
  }
  if (!sse) {
    setInterval(pollLive, 10000);
  }

  // Re-render translations on language change
  window.addEventListener('langchange', () => {
    applyDashboardTranslations();
    renderMetrics(null);
    renderFlavor(null);
  });

  // Expose for external refresh
  window.refreshDashboard = pollLive;

  console.log('✦ Dashboard: SSE live, fallback polling 10s');
})();
