/* ─── Bloch Sphere Page — ALL NOEMA Attributes ────────────── */
(function() {
  'use strict';

  let sphere = null;
  let fetchInterval = null;

  registerPage('bloch', {
    title: 'Sfera Blocha',

    render() {
      return `
        <div class="page-header">
          <h1 data-i18n="pages.bloch.title">Sfera Blocha 36D</h1>
          <p class="page-desc" id="bloch-status-line">REAL · PhaseNav vector program · wszystkie atrybuty NOEMA</p>
        </div>
        <div class="bloch-layout">
          <!-- Lewa kolumna: sfera 3D -->
          <div class="bloch-left">
            <div class="bloch-canvas-wrap">
              <canvas id="bloch-canvas"></canvas>
            </div>
            <div class="bloch-controls">
              <button id="bloch-toggle-rotate">⟳ Auto-rotate</button>
              <button id="bloch-toggle-labels">A Etykiety</button>
              <button id="bloch-reset-view">⌖ Reset view</button>
            </div>
            <div class="bloch-legend" id="bloch-legend"></div>
          </div>

          <!-- Prawa kolumna: ALL atrybuty -->
          <div class="bloch-right">
            <!-- Status bar -->
            <div class="bloch-attr-bar">
              <span class="ba-item"><span class="ba-label">Tick</span><span class="ba-value" id="ba-tick">—</span></span>
              <span class="ba-item"><span class="ba-label">Operator</span><span class="ba-value" id="ba-op">—</span></span>
              <span class="ba-item"><span class="ba-label">Flow RMS</span><span class="ba-value" id="ba-flow">—</span></span>
              <span class="ba-item"><span class="ba-label">Linux Load</span><span class="ba-value" id="ba-load">—</span></span>
            </div>

            <!-- COHERENCE -->
            <div class="ba-section">
              <div class="ba-section-title">COHERENCE</div>
              <div class="ba-section-body">
                <div class="ba-row"><span>R global</span><span class="ba-val c-phase" id="ba-rglobal">—</span></div>
                <div class="ba-row"><span>CIEL coherence</span><span class="ba-val" id="ba-cielcoh">—</span></div>
                <div class="ba-row"><span>Flavor[0]</span><span class="ba-val" id="ba-flavcoh">—</span></div>
              </div>
            </div>

            <!-- FLAVOR (6 slotów) -->
            <div class="ba-section">
              <div class="ba-section-title">FLAVOR [0..5]</div>
              <div class="ba-section-body" id="ba-flavor"></div>
            </div>

            <!-- GRAVITY (4) -->
            <div class="ba-section">
              <div class="ba-section-title">GRAVITY</div>
              <div class="ba-section-body" id="ba-gravity"></div>
            </div>

            <!-- HOLONOMY (7) -->
            <div class="ba-section">
              <div class="ba-section-title">HOLONOMY</div>
              <div class="ba-section-body" id="ba-holonomy"></div>
            </div>

            <!-- ANALOG BUS -->
            <div class="ba-section">
              <div class="ba-section-title">ANALOG BUS</div>
              <div class="ba-section-body">
                <div class="ba-row"><span>Temp</span><span class="ba-val" id="ba-temp">—</span></div>
                <div class="ba-row"><span>Resonance</span><span class="ba-val" id="ba-res">—</span></div>
                <div class="ba-row"><span>Hot φ mean</span><span class="ba-val" id="ba-hphi">—</span></div>
                <div class="ba-row"><span>Cold φ mean</span><span class="ba-val" id="ba-cphi">—</span></div>
                <div class="ba-row"><span>Writing φ mean</span><span class="ba-val" id="ba-wphi">—</span></div>
              </div>
            </div>

            <!-- CIEL STATE -->
            <div class="ba-section">
              <div class="ba-section-title">CIEL STATE</div>
              <div class="ba-section-body" id="ba-ciel"></div>
            </div>

            <!-- AGENT HINT -->
            <div class="ba-section">
              <div class="ba-section-title">AGENT HINT</div>
              <div class="ba-section-body" id="ba-agent"></div>
            </div>
          </div>
        </div>
      `;
    },

    init() {
      applyTranslations();

      const canvas = document.getElementById('bloch-canvas');
      if (!canvas) return;

      // Build legend
      const chColors = ['#00d4ff','#8844ff','#44ff88','#ffb347','#ff4466','#ff88cc','#44ddff','#aaff44','#ffffff'];
      const chNames = ['M0 ID','M1 AGENT','M2 MEMORY','M3 SEM',
                       'M4 LOGIC','M5 AFFECT','M6 REL','M7 TIME','M8 META'];
      const legend = document.getElementById('bloch-legend');
      if (legend) {
        legend.innerHTML = chNames.map((n, i) => `
          <span class="bloch-legend-item">
            <span class="bloch-legend-dot" style="background:${chColors[i]}"></span>
            ${n}
          </span>
        `).join('');
      }

      // Initialize sphere
      sphere = new window.BlochSphere(canvas);

      setTimeout(() => {
        sphere._resize();
        sphere.fetchData();
        sphere.start();
      }, 100);

      // Fetch data every 3s
      fetchInterval = setInterval(() => {
        if (sphere) sphere.fetchData();
      }, 3000);

      // Controls
      const toggleRotate = document.getElementById('bloch-toggle-rotate');
      if (toggleRotate) {
        toggleRotate.onclick = () => {
          if (sphere) {
            sphere.autoRotate = !sphere.autoRotate;
            document.getElementById('bloch-rotate').textContent = sphere.autoRotate ? 'ON' : 'OFF';
          }
        };
      }
      const toggleLabels = document.getElementById('bloch-toggle-labels');
      if (toggleLabels) {
        toggleLabels.onclick = () => {
          if (sphere) { sphere.showLabels = !sphere.showLabels; }
        };
      }
      const resetView = document.getElementById('bloch-reset-view');
      if (resetView) {
        resetView.onclick = () => {
          if (sphere) { sphere.rotX = 0.3; sphere.rotY = 0.5; sphere.rotZ = 0; }
        };
      }

      // ─── Update ALL attributes from live data ───
      const updateAttrs = () => {
        const d = sphere ? sphere._lastData : null;
        if (!d) return;

        // Status bar
        setText('ba-tick', d.tick != null ? d.tick.toLocaleString() : '—');
        setText('ba-op', d.operator || '—');
        setText('ba-flow', d.flow_rms != null ? d.flow_rms.toFixed(4) : '—');
        setText('ba-load', d.linux_load != null ? d.linux_load.toFixed(2) : '—');

        // Coherence
        const coh = d.coherence || {};
        setText('ba-rglobal', coh.r_global != null ? coh.r_global.toFixed(4) : '—');
        setText('ba-cielcoh', coh.ciel_coherence_index != null ? coh.ciel_coherence_index.toFixed(4) : '—');
        setText('ba-flavcoh', coh.flavor_coherence != null ? coh.flavor_coherence.toFixed(4) : '—');

        // Flavor (6 bars)
        const flv = d.flavor || {};
        const flavorEl = document.getElementById('ba-flavor');
        if (flavorEl && flv.raw_vector) {
          const fnames = ['Coherence','Mem Pressure','IO Pressure','Mood','Entropy','Mode'];
          flavorEl.innerHTML = flv.raw_vector.map((v, i) => `
            <div class="ba-bar-row">
              <span class="ba-bar-label">${fnames[i]||'f'+i}</span>
              <div class="ba-bar-track">
                <div class="ba-bar-fill" style="width:${Math.min(100, Math.abs(v)*100)}%; background:hsl(${180+v*120},70%,50%)"></div>
              </div>
              <span class="ba-bar-val">${(typeof v==='number')?v.toFixed(3):v}</span>
            </div>
          `).join('');
        }

        // Gravity (4)
        const grv = d.gravity || {};
        const gravEl = document.getElementById('ba-gravity');
        if (gravEl && grv.raw_vector) {
          const gnames = ['Semantic Density','Tau Dilation','Mass Total','Unruh Power'];
          gravEl.innerHTML = grv.raw_vector.map((v, i) => `
            <div class="ba-row"><span>${gnames[i]||'g'+i}</span><span class="ba-val">${(typeof v==='number')?v.toFixed(4):v}</span></div>
          `).join('');
        }

        // Holonomy (7)
        const hol = d.holonomy || {};
        const holEl = document.getElementById('ba-holonomy');
        if (holEl && hol.raw_vector) {
          const hnames = ['Mean Conn','Gauge Rank','Closure Score','Surface Gamma','Max Conn','Winding','Curvature'];
          holEl.innerHTML = hol.raw_vector.map((v, i) => `
            <div class="ba-row"><span>${hnames[i]||'h'+i}</span><span class="ba-val">${(typeof v==='number')?v.toFixed(4):v}</span></div>
          `).join('');
        }

        // Analog bus
        const ab = d.analog_bus || {};
        setText('ba-temp', ab.temp != null ? ab.temp.toFixed(3) : '—');
        setText('ba-res', ab.resonance != null ? ab.resonance.toFixed(4) : '—');
        if (ab.phi_hot) {
          const hmean = ab.phi_hot.reduce((a,b)=>a+b,0)/ab.phi_hot.length;
          setText('ba-hphi', hmean.toFixed(4));
        }
        if (ab.phi_cold) {
          const cmean = ab.phi_cold.reduce((a,b)=>a+b,0)/ab.phi_cold.length;
          setText('ba-cphi', cmean.toFixed(4));
        }
        if (ab.writing_phi) {
          const wmean = ab.writing_phi.reduce((a,b)=>a+b,0)/ab.writing_phi.length;
          setText('ba-wphi', wmean.toFixed(4));
        }

        // CIEL state
        const cs = d.ciel_state || {};
        const cielEl = document.getElementById('ba-ciel');
        if (cielEl) {
          cielEl.innerHTML = Object.entries(cs).map(([k,v]) => `
            <div class="ba-row"><span>${k}</span><span class="ba-val">${typeof v==='number'?v.toFixed(3):v}</span></div>
          `).join('');
        }

        // Agent hint
        const ah = d.agent_hint || {};
        const agentEl = document.getElementById('ba-agent');
        if (agentEl) {
          const ahDetails = ah.details || {};
          agentEl.innerHTML = `
            <div class="ba-row"><span>action</span><span class="ba-val">${ah.action || '—'}</span></div>
            <div class="ba-row"><span>ts</span><span class="ba-val">${ah.ts || '—'}</span></div>
            <div class="ba-row"><span>pid</span><span class="ba-val">${ah.pid || '—'}</span></div>
            <div class="ba-row"><span>response</span><span class="ba-val ba-small">${ahDetails.response_preview || '—'}</span></div>
          `;
        }
      };

      const updateTimer = setInterval(updateAttrs, 2000);

      // Cleanup
      return () => {
        if (sphere) sphere.stop();
        if (fetchInterval) clearInterval(fetchInterval);
        clearInterval(updateTimer);
        sphere = null;
      };
    }
  });

  function setText(id, val) {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  }

  console.log('✦ Page: Bloch (ALL attributes) loaded');
})();
