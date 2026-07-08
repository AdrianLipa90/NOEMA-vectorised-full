(function() {
  'use strict';

  const OPS = [
    { id: 'NEGATION',           desc: 'Negacja — odwrócenie fazy o π',                               shift: Math.PI,          harmonic: '1,3' },
    { id: 'QUESTION',           desc: 'Pytanie — otwarcie fazy, delikatne wychylenie',               shift: Math.PI / 8,      harmonic: '3,6' },
    { id: 'ASSERTION',          desc: 'Asercja — brak przesunięcia, stan bazowy',                    shift: 0,                harmonic: '1' },
    { id: 'CONDITION',          desc: 'Warunek — przesunięcie warunkowe π/6',                        shift: Math.PI / 6,      harmonic: '3' },
    { id: 'CAUSE',              desc: 'Przyczyna — przesunięcie przyczynowe π/4',                    shift: Math.PI / 4,      harmonic: '3,9' },
    { id: 'MODAL_POSSIBILITY',  desc: 'Możliwość — lekka faza modalna π/10',                         shift: Math.PI / 10,     harmonic: '6' },
    { id: 'MODAL_NECESSITY',    desc: 'Konieczność — silne przesunięcie modalne π/3',                shift: Math.PI / 3,      harmonic: '9' },
    { id: 'MODAL_PERMISSION',   desc: 'Pozwolenie — subtelna faza zgody π/12',                       shift: Math.PI / 12,     harmonic: '1,3' },
    { id: 'MODAL_OBLIGATION',   desc: 'Obowiązek — wymuszenie fazy π/2.5',                           shift: Math.PI / 2.5,    harmonic: '6,9' },
    { id: 'UNCERTAINTY',        desc: 'Niepewność — fluktuacja fazy π/5',                            shift: Math.PI / 5,      harmonic: '3,6,9' },
    { id: 'SOURCE_REQUIRED',    desc: 'Źródło wymagane — powrót do źródła -π/4',                    shift: -Math.PI / 4,     harmonic: '1' },
    { id: 'CANON_BLOCK',        desc: 'Blokada kanonu — zablokowanie fazy 2π/3',                     shift: 2 * Math.PI / 3,  harmonic: '1,6,9' },
    { id: 'CONSENT_REQUIRED',   desc: 'Zgoda wymagana — przesunięcie konsensu π/7',                 shift: Math.PI / 7,      harmonic: '3,6' },
    { id: 'ACTION_REQUEST',     desc: 'Żądanie akcji — aktywna faza π/2',                            shift: Math.PI / 2,      harmonic: '3,9' },
    { id: 'REFUSAL',            desc: 'Odmowa — negatywne przesunięcie -π/3',                        shift: -Math.PI / 3,     harmonic: '1,9' },
    { id: 'PAUSE',              desc: 'Pauza — zatrzymanie fazy, niemierzalne przesunięcie',          shift: 0.001,            harmonic: '1,3,6,9' },
    { id: 'SIMULATION_BOUNDARY',desc: 'Granica symulacji — przesunięcie brzegowe 3π/4',              shift: 3 * Math.PI / 4,  harmonic: '6,9' },
  ];

  let liveInterval = null;
  let graphicsInterval = null;
  let liveData = { phi_mean: 0, omega_mean: 0, tau_mean: 0, coherence: 0, gamma: 0, mass: 0 };
  let graphicsData = null;
  let graphicsScene = 'surface';

  registerPage('phasenav', {
    title: 'PhaseNav',

    render() {
      return `
        <div class="page-header">
          <h1>PhaseNav — stan przestrzeni fazowej</h1>
          <p class="page-desc">Operator algebra PhaseNav z danymi live z powierzchni fazowej NOEMY</p>
        </div>

        <div class="dash-panel">
          <div class="dash-panel-title">Stan fazowy <span style="color:var(--text-dim);font-weight:400;font-size:0.75rem;">(live z /api/live — odświeżanie co 5s)</span></div>
          <div class="pn-live-grid">
            <div class="dash-card" id="pn-phi">
              <div class="dash-card-title">φ̄ (faza średnia)</div>
              <div class="dash-card-value">—</div>
              <div class="dash-card-desc">Średnia faza oscylatorów 36D [rad]</div>
            </div>
            <div class="dash-card" id="pn-omega">
              <div class="dash-card-title">ω̄ (częstotliwość)</div>
              <div class="dash-card-value">—</div>
              <div class="dash-card-desc">Średnia częstotliwość naturalna [Hz]</div>
            </div>
            <div class="dash-card" id="pn-tau">
              <div class="dash-card-title">τ̄ (czas życia)</div>
              <div class="dash-card-value">—</div>
              <div class="dash-card-desc">Średni czas życia pamięci [s]</div>
            </div>
            <div class="dash-card" id="pn-coherence">
              <div class="dash-card-title">R (koherencja)</div>
              <div class="dash-card-value">—</div>
              <div class="dash-card-desc">Globalny parametr porządku Kuramoto</div>
            </div>
            <div class="dash-card" id="pn-gamma">
              <div class="dash-card-title">γ (dylatacja)</div>
              <div class="dash-card-value">—</div>
              <div class="dash-card-desc">Dylatacja czasu — spowolnienie τ</div>
            </div>
            <div class="dash-card" id="pn-mass">
              <div class="dash-card-title">Masa semantyczna</div>
              <div class="dash-card-value">—</div>
              <div class="dash-card-desc">Gęstość masy semantycznej</div>
            </div>
          </div>
        </div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">Operator — efekt na φ̄ live</div>
          <div id="pn-current-phase" style="text-align:center;padding:16px 0 8px;">
            <span style="font-size:2.4rem;font-weight:800;font-family:var(--mono);color:var(--phase);" id="pn-phase-badge">—</span>
            <span style="display:block;color:var(--text-dim);font-size:0.82rem;margin-top:4px;">
              Aktualna φ̄ — poniżej każdy operator przesuwa fazę o swój stały kąt
            </span>
          </div>
        </div>

        <div class="pn-ops-grid" id="pn-ops-grid" style="margin-top:1rem;"></div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">PhaseNav graphics composer <span style="color:var(--text-dim);font-weight:400;font-size:0.75rem;">(Bloch / memory / relational / operator)</span></div>
          <div style="display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 12px;" id="pn-graphics-tabs">
            <button class="pn-graphics-btn active" data-scene="surface">Surface</button>
            <button class="pn-graphics-btn" data-scene="relations">Relacje</button>
            <button class="pn-graphics-btn" data-scene="memory">Pamięć</button>
            <button class="pn-graphics-btn" data-scene="operators">Operatory</button>
          </div>
          <div id="pn-graphics-summary" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;margin-bottom:12px;"></div>
          <div id="pn-graphics-view" class="pn-graphics-view"></div>
        </div>

        <style>
          .pn-live-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;}
          @media(max-width:900px){.pn-live-grid{grid-template-columns:repeat(3,1fr);}}
          .pn-ops-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin-top:1rem;}
          .pn-op-card{cursor:default;}
          .pn-op-card .op-effect{font-size:0.92rem;font-weight:600;font-family:var(--mono);margin:6px 0;}
          .pn-op-card .op-harmonic{font-size:0.72rem;color:var(--text-dim);font-family:var(--mono);}
          .pn-graphics-btn{border:1px solid rgba(68,221,255,0.2);background:rgba(255,255,255,0.02);color:var(--text);border-radius:999px;padding:6px 12px;font-size:0.78rem;cursor:pointer;font-family:var(--mono);}
          .pn-graphics-btn.active{background:rgba(68,221,255,0.12);border-color:rgba(68,221,255,0.38);color:#d7fbff;}
          .pn-graphics-view{min-height:360px;border:1px solid var(--border);border-radius:16px;overflow:hidden;background:linear-gradient(180deg, rgba(5,10,16,0.9), rgba(2,4,8,0.96));}
          .pn-graphics-view svg{display:block;width:100%;height:auto;}
          .pn-graphics-metric{padding:10px 12px;border:1px solid var(--border);border-radius:12px;background:rgba(255,255,255,0.02);}
          .pn-graphics-metric .label{font-size:0.68rem;text-transform:uppercase;letter-spacing:0.08em;color:var(--text-dim);font-family:var(--mono);}
          .pn-graphics-metric .value{font-size:0.92rem;font-family:var(--mono);color:#d8f8ff;margin-top:4px;}
        </style>
      `;
    },

    init() {
      renderOperators();
      bindGraphicsTabs();
      pollPhaseNav();
      pollGraphics();
      liveInterval = setInterval(pollPhaseNav, 5000);
      graphicsInterval = setInterval(pollGraphics, 8000);
      return () => {
        if (liveInterval) clearInterval(liveInterval);
        if (graphicsInterval) clearInterval(graphicsInterval);
      };
    }
  });

  function renderOperators() {
    const grid = document.getElementById('pn-ops-grid');
    if (!grid) return;
    grid.innerHTML = OPS.map((op, i) => `
      <div class="dash-card pn-op-card" id="op-${i}">
        <div class="dash-card-title">${op.id}</div>
        <div class="op-effect" id="op-eff-${i}">φ<sub>eff</sub> = —</div>
        <div class="dash-card-desc">${op.desc}</div>
        <div class="op-harmonic">Harmonic: {${op.harmonic}} · shift: ${op.shift.toFixed(4)} rad</div>
      </div>
    `).join('');
  }

  function pollPhaseNav() {
    fetch('/api/live')
      .then(r => r.json())
      .then(updateLive)
      .catch(() => {});
  }

  function pollGraphics() {
    fetch(`/api/phasenav/graphics?scene=${encodeURIComponent(graphicsScene)}&q=NOEMA`)
      .then(r => r.json())
      .then(updateGraphics)
      .catch(() => {});
  }

  function updateLive(data) {
    if (!data) return;
    Object.assign(liveData, {
      phi_mean: data.phi_mean || 0,
      omega_mean: data.omega_mean || 0,
      tau_mean: data.tau_mean || 0,
      coherence: data.coherence || 0,
      gamma: data.gamma || 0,
      mass: data.mass || 0,
    });

    setCard('pn-phi', liveData.phi_mean.toFixed(6), liveData.phi_mean);
    setCard('pn-omega', liveData.omega_mean.toFixed(4), liveData.omega_mean);
    setCard('pn-tau', liveData.tau_mean.toFixed(4), liveData.tau_mean);
    setCard('pn-coherence', liveData.coherence.toFixed(4), liveData.coherence);
    setCard('pn-gamma', liveData.gamma.toFixed(4), liveData.gamma);
    setCard('pn-mass', liveData.mass.toFixed(4), liveData.mass);

    const badge = document.getElementById('pn-phase-badge');
    if (badge) badge.textContent = `φ = ${liveData.phi_mean.toFixed(6)} rad`;

    const twoPI = 2 * Math.PI;
    OPS.forEach((op, i) => {
      const eff = ((liveData.phi_mean + op.shift) % twoPI + twoPI) % twoPI;
      const el = document.getElementById(`op-eff-${i}`);
      if (el) el.textContent = `φeff = ${eff.toFixed(6)} rad`;
    });
  }

  function setCard(id, display, val) {
    const el = document.getElementById(id);
    if (!el) return;
    const valEl = el.querySelector('.dash-card-value');
    if (!valEl) return;
    valEl.textContent = display;
    if (val != null) {
      if (val > 0.8) valEl.style.color = '#44ff88';
      else if (val > 0.5) valEl.style.color = '#ffb347';
      else if (val > 0.2) valEl.style.color = '#ff88cc';
      else valEl.style.color = '#ff4466';
    }
  }

  function bindGraphicsTabs() {
    const tabs = document.getElementById('pn-graphics-tabs');
    if (!tabs) return;
    tabs.addEventListener('click', (ev) => {
      const target = ev.target;
      if (!(target instanceof HTMLElement)) return;
      const scene = target.getAttribute('data-scene');
      if (!scene) return;
      graphicsScene = scene;
      tabs.querySelectorAll('.pn-graphics-btn').forEach(btn => btn.classList.remove('active'));
      target.classList.add('active');
      renderGraphicsScene();
      pollGraphics();
    });
  }

  function updateGraphics(data) {
    if (!data || data.status !== 'ok') return;
    graphicsData = data;
    renderGraphicsScene();
  }

  function renderGraphicsScene() {
    const view = document.getElementById('pn-graphics-view');
    const summary = document.getElementById('pn-graphics-summary');
    if (!view || !summary) return;
    const scenes = graphicsData && graphicsData.scenes ? graphicsData.scenes : {};
    const scene = scenes[graphicsScene] || scenes.surface || null;
    if (!scene) {
      view.innerHTML = '<div style="padding:16px;color:var(--text-dim);">Brak danych grafiki</div>';
      summary.innerHTML = '';
      return;
    }
    const metrics = scene.summary || {};
    summary.innerHTML = [
      ['Scene', scene.title || graphicsScene],
      ['Nodes', metrics.node_count ?? 0],
      ['Edges', metrics.edge_count ?? 0],
      ['Projection', scene.projection || '—'],
      ['Hash', scene.scene_hash ? String(scene.scene_hash).slice(0, 12) : '—'],
    ].map(([label, value]) => `
      <div class="pn-graphics-metric">
        <div class="label">${label}</div>
        <div class="value">${value}</div>
      </div>
    `).join('');
    view.innerHTML = scene.svg || '<div style="padding:16px;color:var(--text-dim);">Brak SVG</div>';
  }

  console.log('✦ PhaseNav page: loaded (17 UniversalOperatorType)');
})();
