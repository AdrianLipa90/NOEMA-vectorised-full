/* ─── Metrics Page ──────────────────────────────────────────── */
(function() {
  'use strict';

  let metricsData = [];
  let liveInterval = null;

  registerPage('metrics', {
    title: 'Metryki',

    render() {
      return `
        <div class="page-header">
          <h1 data-i18n="pages.metrics.title">Metryki systemowe</h1>
          <p class="page-desc" data-i18n="pages.metrics.desc">Wszystkie metryki NOEMY z opisami i wartościami live</p>
        </div>
        <input type="text" class="metric-search" id="metric-search" 
               placeholder="🔍 Szukaj metryki..." data-i18n="pages.metrics.search" 
               oninput="window.filterMetrics(this.value)">
        <div class="metrics-grid" id="metrics-grid">
          <div class="page-loading"><div class="loading-spinner"></div><span>Ładowanie metryk...</span></div>
        </div>
      `;
    },

    init() {
      applyTranslations();
      loadMetrics();
      liveInterval = setInterval(refreshValues, 5000);
      return () => {
        if (liveInterval) clearInterval(liveInterval);
        liveInterval = null;
      };
    }
  });

  // Expose filter globally
  window.filterMetrics = function(query) {
    const grid = document.getElementById('metrics-grid');
    if (!grid || !metricsData.length) return;
    const q = query.toLowerCase().trim();
    grid.querySelectorAll('.metric-card').forEach(card => {
      const text = card.textContent.toLowerCase();
      card.style.display = !q || text.includes(q) ? '' : 'none';
    });
  };

  function loadMetrics() {
    fetch('/api/metrics')
      .then(r => r.json())
      .then(data => {
        if (data && data.metrics) {
          metricsData = data.metrics;
          renderMetrics(data.metrics);
        } else {
          document.getElementById('metrics-grid').innerHTML = '<div class="page-loading">Brak danych</div>';
        }
      })
      .catch(() => {
        document.getElementById('metrics-grid').innerHTML = '<div class="page-loading">Nie można załadować metryk</div>';
      });
  }

  function renderMetrics(metrics) {
    const grid = document.getElementById('metrics-grid');
    if (!grid) return;
    grid.innerHTML = metrics.map(m => {
      const lang = window.LANG || 'pl';
      const label = lang === 'pl' ? (m.label_pl || m.label) : m.label;
      const val = m.value;
      const valStr = val !== null && val !== undefined 
        ? (typeof val === 'number' ? val.toFixed(4) : val) 
        : '—';
      return `
        <div class="metric-card" data-key="${m.key}">
          <div class="metric-header">
            <span class="metric-key">${m.key}</span>
            <span class="metric-unit">${m.unit}</span>
          </div>
          <div class="metric-value" id="mv-${m.key}">${valStr}</div>
          <div class="metric-desc">${m.desc}</div>
          <div class="metric-source">źródło: ${m.source}</div>
        </div>
      `;
    }).join('');
  }

  function refreshValues() {
    fetch('/api/metrics')
      .then(r => r.json())
      .then(data => {
        if (data && data.metrics) {
          data.metrics.forEach(m => {
            const el = document.getElementById(`mv-${m.key}`);
            if (el) {
              const val = m.value;
              el.textContent = val !== null && val !== undefined 
                ? (typeof val === 'number' ? val.toFixed(4) : val) 
                : '—';
            }
          });
        }
      })
      .catch(() => {});
  }

  console.log('✦ Page: Metrics loaded');
})();
