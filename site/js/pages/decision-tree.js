/* ─── Decision Tree — żywe dane z /api/decisions ─────────── */
(function() {
  'use strict';

  let refreshInterval = null;

  function renderCard(d) {
    const id = d.lp || 'D-' + d.id;
    const title = d.title || '(bez tytułu)';
    const desc = d.consequence || d.description || '(brak opisu)';
    const statusColor = d.status === 'completed' ? '#44ff88'
                      : d.status === 'active'   ? '#00d4ff'
                      : '#ffb347';
    return `
      <div class="dash-card" style="border-left:3px solid ${statusColor};position:relative;">
        <div class="dash-card-value">${id}</div>
        <div class="dash-card-title">${title}</div>
        <div class="dash-card-desc">${desc}</div>
        <div style="font-size:0.7rem;color:var(--muted);margin-top:6px;display:flex;justify-content:space-between;">
          <span>${d.decision_type || ''}</span>
          <span style="color:${statusColor}">${d.status || ''}</span>
        </div>
        ${d.created_at ? `<div style="font-size:0.65rem;color:var(--text-dim);margin-top:2px;">${d.created_at}</div>` : ''}
      </div>
    `;
  }

  registerPage('decision-tree', {
    title: 'Drzewo decyzyjne',

    render() {
      return `
        <div class="page-header">
          <h1><span data-i18n="pages.decision-tree.title">Drzewo decyzyjne</span> <span id="dt-count" style="color:var(--text-dim);font-weight:400;font-size:1rem;"></span></h1>
          <p class="page-desc" data-i18n="pages.decision-tree.desc">Decyzje NOEMY — żywe dane z bazy TaskPlan</p>
        </div>

        <div class="dash-panel">
          <div class="dash-panel-title">Drzewo decyzyjne</div>
          <div id="dt-grid" class="dash-grid" style="margin-top:8px;">
            <div style="color:var(--muted);padding:1rem;">Ładowanie...</div>
          </div>
        </div>

        <div class="dash-panel" style="margin-top:12px;">
          <div class="dash-panel-title" style="cursor:pointer;" onclick="const n=this.nextElementSibling;n.style.display=n.style.display==='none'?'block':'none';this.querySelector('.toggle-icon').textContent=n.style.display==='none'?'▶':'▼';">
            <span class="toggle-icon">▶</span> Odpowiedź JSON
          </div>
          <pre id="dt-raw" style="display:none;font-family:var(--mono);font-size:0.7rem;color:var(--text-dim);overflow:auto;max-height:200px;"></pre>
        </div>
      `;
    },

    init() {
      applyTranslations();
      fetchDecisions();
      refreshInterval = setInterval(fetchDecisions, 30000);
      return () => {
        if (refreshInterval) {
          clearInterval(refreshInterval);
          refreshInterval = null;
        }
      };
    }
  });

  function fetchDecisions() {
    fetch('/api/decisions')
      .then(r => r.json())
      .then(data => {
        if (!data || data.status !== 'ok' || !Array.isArray(data.decisions)) return;
        const decisions = data.decisions;
        const countEl = document.getElementById('dt-count');
        if (countEl) countEl.textContent = '— ' + decisions.length + ' decyzji';

        const grid = document.getElementById('dt-grid');
        if (grid) {
          if (decisions.length === 0) {
            grid.innerHTML = '<div style="color:var(--muted);padding:1rem;">Brak decyzji</div>';
          } else {
            grid.innerHTML = decisions.map(renderCard).join('');
          }
        }

        const raw = document.getElementById('dt-raw');
        if (raw) raw.textContent = JSON.stringify(data, null, 2);
      })
      .catch(() => {
        const grid = document.getElementById('dt-grid');
        if (grid) grid.innerHTML = '<div style="color:var(--error-color);padding:1rem;">Błąd ładowania danych</div>';
      });
  }

  console.log('✦ Page: Decision Tree loaded');
})();
