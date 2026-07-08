/* ─── Projects Page — realne projekty i zadania NOEMY ─────────── */
(function() {
  'use strict';

  let refreshInterval = null;

  registerPage('projects', {
    title: 'Projekty NOEMY',

    render() {
      return `
        <div class="page-header">
          <h1 data-i18n="pages.projects.title">Projekty NOEMY</h1>
          <p class="page-desc" data-i18n="pages.projects.desc">Rzeczywiste systemy i zadania — dane live z API</p>
        </div>

        <div class="dash-panel">
          <div class="dash-panel-title">Systemy — <span id="pj-sys-count">0</span></div>
          <div id="pj-systems-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;margin-top:8px;">
            Ładowanie systemów...
          </div>
        </div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">Zadania — <span id="pj-task-count">0</span></div>
          <div id="pj-tasks-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;margin-top:8px;">
            Ładowanie zadań...
          </div>
        </div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title" style="cursor:pointer;" onclick="const n=this.nextElementSibling;n.style.display=n.style.display==='none'?'block':'none';this.querySelector('.toggle-icon').textContent=n.style.display==='none'?'▶':'▼';">
            <span class="toggle-icon">▶</span> Odpowiedź JSON
          </div>
          <pre id="pj-raw" style="display:none;font-family:var(--mono);font-size:0.7rem;color:var(--text-dim);overflow:auto;max-height:200px;"></pre>
        </div>
      `;
    },

    init() {
      fetchSystems();
      fetchTasks();
      refreshInterval = setInterval(fetchTasks, 15000);
      return () => {
        if (refreshInterval) clearInterval(refreshInterval);
        refreshInterval = null;
      };
    }
  });

  function fetchSystems() {
    fetch('/api/cards')
      .then(r => r.json())
      .then(data => {
        const systems = (data && data.systems) || [];
        const cnt = document.getElementById('pj-sys-count');
        if (cnt) cnt.textContent = systems.length;
        renderSystems(systems);
        updateRaw(data);
      })
      .catch(() => {
        const el = document.getElementById('pj-systems-grid');
        if (el) el.innerHTML = '<div class="dash-card" style="color:var(--muted);">Nie można załadować systemów — API niedostępne</div>';
      });
  }

  function fetchTasks() {
    fetch('/api/tasks')
      .then(r => r.json())
      .then(data => {
        const tasks = (data && data.tasks) || [];
        const cnt = document.getElementById('pj-task-count');
        if (cnt) cnt.textContent = tasks.length;
        renderTasks(tasks);
      })
      .catch(() => {});
  }

  function renderSystems(systems) {
    const el = document.getElementById('pj-systems-grid');
    if (!el) return;
    if (!systems || !systems.length) {
      el.innerHTML = '<div class="dash-card" style="color:var(--muted);">Brak systemów</div>';
      return;
    }

    const typeColors = {
      core: '#00d4ff', module: '#8844ff', data: '#44ff88',
      bridge: '#ffb347', service: '#ff4466', system: '#44ddff',
      other: '#888888'
    };

    el.innerHTML = systems.map(s => {
      const t = s.type || 'other';
      const color = typeColors[t] || typeColors.other;
      return `
        <div class="dash-card" style="display:flex;flex-direction:column;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
            <div class="dash-card-title" style="margin-bottom:0;color:${color};">${s.name}</div>
            <span style="font-size:0.65rem;padding:2px 6px;border-radius:3px;background:${color}22;color:${color};border:1px solid ${color}44;text-transform:uppercase;font-family:var(--mono);">${t}</span>
          </div>
          <div class="dash-card-desc" style="flex:1;">${s.description || '—'}</div>
        </div>
      `;
    }).join('');
  }

  function renderTasks(tasks) {
    const el = document.getElementById('pj-tasks-grid');
    if (!el) return;
    if (!tasks || !tasks.length) {
      el.innerHTML = '<div class="dash-card" style="color:var(--muted);">Brak zadań</div>';
      return;
    }

    const statusColors = {
      pending: '#ffb347',
      in_progress: '#00d4ff',
      completed: '#44ff88',
      cancelled: '#888888'
    };

    el.innerHTML = tasks.map(t => {
      const st = t.status || 'pending';
      const sc = statusColors[st] || statusColors.pending;
      const prio = t.priority || '—';
      const cat = t.category || '—';
      return `
        <div class="dash-card" style="display:flex;flex-direction:column;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
            <div class="dash-card-title" style="margin-bottom:0;font-size:0.85rem;">${t.title}</div>
            <span style="font-size:0.65rem;padding:2px 6px;border-radius:3px;background:${sc}22;color:${sc};border:1px solid ${sc}44;text-transform:uppercase;font-family:var(--mono);">${st}</span>
          </div>
          <div style="display:flex;gap:8px;margin-bottom:4px;">
            <span class="dash-card-value" style="font-size:0.7rem;color:var(--muted);">priorytet: ${prio}</span>
            <span class="dash-card-value" style="font-size:0.7rem;color:var(--muted);">kategoria: ${cat}</span>
          </div>
          <div class="dash-card-desc" style="flex:1;">${t.description || '—'}</div>
        </div>
      `;
    }).join('');
  }

  function updateRaw(data) {
    const el = document.getElementById('pj-raw');
    if (!el) return;
    el.textContent = JSON.stringify(data, null, 2);
  }

  console.log('✦ Page: Projects loaded');
})();
