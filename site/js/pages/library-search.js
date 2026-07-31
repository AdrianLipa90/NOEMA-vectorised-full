/* ─── Library Search Page — wyszukiwarka biblioteki NOEMA 36D ── */
(function () {
  'use strict';

  const OPERATORS = [
    'ACTION_REQUEST','AFFECT','ADDITION','ASSERTION','ATTRACTOR',
    'BOUNDARY','CANON_BLOCK','CAUSE','COMPOSITION','CONDITION',
    'CONSENT','CONSENT_REQUIRED','DIFFERENCE','FOLD','FORCE',
    'IDENTITY','MEMORY','MODAL_NECESSITY','MODAL_OBLIGATION',
    'MODAL_PERMISSION','MODAL_POSSIBILITY','NEGATION','ORDER',
    'PAUSE','QUESTION','REFUSAL','RETURN','RISK','SCOPE',
    'SIMULATION_BOUNDARY','SOURCE','SOURCE_REQUIRED','TRANSFORM',
    'UNCERTAINTY','UNRUH_DRIVE','WARP_DRIFT',
  ];

  let _stats = null;
  let _lastQuery = '';
  let _searching = false;

  /* ── helpers ── */
  function $id(id) { return document.getElementById(id); }

  function escHtml(s) {
    return String(s)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function operatorColor(op) {
    const map = {
      IDENTITY:'#4fc3f7', TRANSFORM:'#81c784', MEMORY:'#ce93d8',
      AFFECT:'#f48fb1',   CAUSE:'#ffb74d',     FORCE:'#ef9a9a',
      NEGATION:'#b0bec5', RETURN:'#80cbc4',     DIFFERENCE:'#fff176',
      COMPOSITION:'#a5d6a7', CANON_BLOCK:'#ff7043', CONSENT:'#4db6ac',
      UNCERTAINTY:'#90a4ae', QUESTION:'#f9a825', ASSERTION:'#ce93d8',
    };
    return map[op] || '#78909c';
  }

  /* ── render ── */
  registerPage('library-search', {
    title: 'Wyszukiwarka biblioteki',

    render() {
      const opOptions = OPERATORS.map(op =>
        `<option value="${op}">${op}</option>`
      ).join('');

      return `
        <div class="page-header">
          <h1>&#x1F50D; Biblioteka NOEMA</h1>
          <p class="page-desc">Wyszukiwarka 1293 dokumentów przez PhaseNav 36D</p>
        </div>

        <!-- Stats bar -->
        <div class="dash-panel" style="padding:0.75rem 1rem;margin-bottom:1rem;">
          <div style="display:flex;gap:2rem;flex-wrap:wrap;font-size:0.78rem;font-family:var(--mono);">
            <span>Dokumenty: <strong id="ls-stat-docs" class="c-cyan">…</strong></span>
            <span>Indeks: <strong id="ls-stat-dim" class="c-accent">36D</strong></span>
            <span>Top operator: <strong id="ls-stat-top" class="c-text">…</strong></span>
          </div>
        </div>

        <!-- Search form -->
        <div class="dash-panel" style="padding:1rem;margin-bottom:1rem;">
          <div style="display:flex;gap:0.5rem;flex-wrap:wrap;align-items:flex-end;">
            <div style="flex:1;min-width:200px;">
              <label style="font-size:0.72rem;color:var(--text-dim);display:block;margin-bottom:4px;">Zapytanie</label>
              <input id="ls-input" type="text" class="chat-input"
                style="width:100%;padding:0.5rem 0.75rem;font-size:0.9rem;"
                placeholder="np. świadomość tożsamość, CIEL NOEMA, fizyka kwantowa…" />
            </div>
            <div style="min-width:120px;">
              <label style="font-size:0.72rem;color:var(--text-dim);display:block;margin-bottom:4px;">Operator (opcja)</label>
              <select id="ls-op-filter" style="width:100%;padding:0.45rem 0.5rem;background:var(--bg2);color:var(--text);border:1px solid var(--border);border-radius:4px;font-size:0.8rem;">
                <option value="">— wszystkie —</option>
                ${opOptions}
              </select>
            </div>
            <div style="min-width:70px;">
              <label style="font-size:0.72rem;color:var(--text-dim);display:block;margin-bottom:4px;">Top-K</label>
              <input id="ls-topk" type="number" min="1" max="50" value="10"
                style="width:100%;padding:0.45rem 0.5rem;background:var(--bg2);color:var(--text);border:1px solid var(--border);border-radius:4px;font-size:0.85rem;text-align:center;" />
            </div>
            <button id="ls-btn" class="chat-send-button" style="height:36px;padding:0 1.2rem;">
              Szukaj
            </button>
          </div>
        </div>

        <!-- Results -->
        <div id="ls-results" style="min-height:200px;">
          <div style="padding:2rem;text-align:center;color:var(--text-dim);font-size:0.85rem;">
            Wpisz zapytanie i naciśnij <em>Szukaj</em> lub Enter.
          </div>
        </div>

        <!-- Operator distribution chart -->
        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">Rozkład operatorów w bibliotece</div>
          <div id="ls-op-chart" style="margin-top:0.5rem;font-size:0.72rem;font-family:var(--mono);">
            <div style="text-align:center;color:var(--text-dim);">Ładowanie…</div>
          </div>
        </div>
      `;
    },

    init() {
      const input  = $id('ls-input');
      const btn    = $id('ls-btn');
      const topkEl = $id('ls-topk');
      const opEl   = $id('ls-op-filter');

      /* load stats */
      fetch('/api/library/stats')
        .then(r => r.json())
        .then(d => {
          _stats = d;
          if ($id('ls-stat-docs')) $id('ls-stat-docs').textContent = d.n_documents ?? '?';
          const topOp = Object.entries(d.operator_distribution || {})
            .sort((a, b) => b[1] - a[1])[0];
          if (topOp && $id('ls-stat-top'))
            $id('ls-stat-top').textContent = `${topOp[0]} (${topOp[1]})`;
          renderOpChart(d.operator_distribution || {});
        })
        .catch(() => {});

      const doSearch = () => {
        const q = input.value.trim();
        if (!q || _searching) return;
        doSearchRequest(q, parseInt(topkEl.value) || 10, opEl.value);
      };

      btn.addEventListener('click', doSearch);
      input.addEventListener('keydown', e => {
        if (e.key === 'Enter') doSearch();
      });
    },
  });

  /* ── search request ── */
  function doSearchRequest(q, topK, operator) {
    if (_searching) return;
    _searching = true;
    _lastQuery = q;

    const container = $id('ls-results');
    if (!container) { _searching = false; return; }

    container.innerHTML = `
      <div style="padding:2rem;text-align:center;color:var(--text-dim);">
        <div class="loading-spinner" style="display:inline-block;margin-right:8px;"></div>
        Szukam…
      </div>`;

    const body = { q, top_k: topK };
    if (operator) body.operator = operator;

    fetch('/api/library/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
      .then(r => r.json())
      .then(data => {
        _searching = false;
        renderResults(container, data);
      })
      .catch(err => {
        _searching = false;
        if (container) container.innerHTML =
          `<div style="padding:1rem;color:var(--c-red);">Błąd: ${escHtml(String(err))}</div>`;
      });
  }

  /* ── render results ── */
  function renderResults(container, data) {
    if (!data.ok) {
      container.innerHTML =
        `<div class="dash-panel" style="padding:1rem;color:var(--c-red);">
           Błąd: ${escHtml(data.error || 'nieznany')}
         </div>`;
      return;
    }

    const results = data.results || [];
    if (results.length === 0) {
      container.innerHTML =
        `<div class="dash-panel" style="padding:1.5rem;text-align:center;color:var(--text-dim);">
           Brak wyników dla: <em>${escHtml(data.query)}</em>
         </div>`;
      return;
    }

    const rows = results.map(r => {
      const col = operatorColor(r.operator_id);
      const score = (r.score * 100).toFixed(1);
      const fname = r.file.length > 60 ? r.file.slice(0, 57) + '…' : r.file;
      const coll  = r.collection || '—';
      const author = r.author && r.author !== 'unknown' ? r.author : '';

      return `
        <div style="display:flex;align-items:flex-start;gap:0.75rem;padding:0.6rem 0.75rem;
                    border-bottom:1px solid var(--border);transition:background 0.15s;"
             onmouseenter="this.style.background='var(--bg2)'"
             onmouseleave="this.style.background=''">

          <!-- rank -->
          <div style="min-width:28px;text-align:center;font-size:0.7rem;
                      color:var(--text-dim);padding-top:3px;">${r.rank}</div>

          <!-- score bar -->
          <div style="min-width:52px;text-align:right;">
            <div style="font-size:0.85rem;font-weight:600;color:var(--accent);">${score}%</div>
            <div style="height:3px;background:var(--border);border-radius:2px;margin-top:3px;">
              <div style="height:3px;width:${score}%;background:${col};border-radius:2px;"></div>
            </div>
          </div>

          <!-- operator badge -->
          <div style="min-width:130px;">
            <span style="display:inline-block;padding:2px 6px;border-radius:3px;
                         font-size:0.65rem;font-family:var(--mono);
                         background:${col}22;color:${col};border:1px solid ${col}55;">
              ${escHtml(r.operator_id)}
            </span>
          </div>

          <!-- file info -->
          <div style="flex:1;min-width:0;">
            <div style="font-size:0.82rem;color:var(--text);word-break:break-all;"
                 title="${escHtml(r.file)}">${escHtml(fname)}</div>
            <div style="font-size:0.7rem;color:var(--text-dim);margin-top:2px;">
              ${escHtml(coll)}${author ? ' · ' + escHtml(author) : ''}
            </div>
          </div>

        </div>`;
    }).join('');

    container.innerHTML = `
      <div class="dash-panel" style="padding:0;">
        <div style="padding:0.5rem 0.75rem;border-bottom:1px solid var(--border);
                    font-size:0.72rem;color:var(--text-dim);display:flex;justify-content:space-between;">
          <span>Wyniki dla: <strong style="color:var(--text);">${escHtml(data.query)}</strong></span>
          <span>${data.n} wyników</span>
        </div>
        ${rows}
      </div>`;
  }

  /* ── operator distribution chart ── */
  function renderOpChart(dist) {
    const el = $id('ls-op-chart');
    if (!el) return;
    const entries = Object.entries(dist).sort((a, b) => b[1] - a[1]);
    const maxVal  = entries[0]?.[1] || 1;
    el.innerHTML = entries.map(([op, n]) => {
      const pct = (n / maxVal * 100).toFixed(0);
      const col = operatorColor(op);
      return `
        <div style="display:flex;align-items:center;gap:6px;margin:3px 0;cursor:pointer;"
             onclick="document.getElementById('ls-op-filter').value='${op}'">
          <div style="min-width:130px;color:var(--text-dim);text-align:right;font-size:0.7rem;">${op}</div>
          <div style="flex:1;height:10px;background:var(--border);border-radius:2px;">
            <div style="width:${pct}%;height:10px;background:${col};border-radius:2px;"></div>
          </div>
          <div style="min-width:24px;color:var(--text-dim);">${n}</div>
        </div>`;
    }).join('');
  }

})();
