/* ─── Engineering Page — runtime, build and ops surface ───── */
(function() {
  'use strict';

  let engineeringTimer = null;

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function unwrap(payload) {
    if (!payload) return null;
    if (payload.ok === true && Object.prototype.hasOwnProperty.call(payload, 'data')) {
      return payload.data;
    }
    return payload;
  }

  registerPage('engineering', {
    title: 'Inżynieria',

    render() {
      return `
        <div class="page-header">
          <h1 data-i18n="nav.engineering">Inżynieria</h1>
          <p class="page-desc">Warstwa operacyjna NOEMY: daemon registry, TaskPlan DB, skills i systemowe zależności</p>
        </div>

        <div class="dash-two-col">
          <div class="dash-panel">
            <div class="dash-panel-title">Daemony i moduły</div>
            <div id="eng-modules" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;"></div>
          </div>
          <div class="dash-panel">
            <div class="dash-panel-title">Build surface</div>
            <div id="eng-build" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;"></div>
          </div>
        </div>

        <div class="dash-panel" style="margin-top:1rem;">
          <div class="dash-panel-title">TaskPlan / Skills</div>
          <div id="eng-plan" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;"></div>
        </div>
      `;
    },

    init() {
      applyTranslations();
      refreshEngineering();
      engineeringTimer = setInterval(refreshEngineering, 12000);
      return () => {
        if (engineeringTimer) clearInterval(engineeringTimer);
        engineeringTimer = null;
      };
    }
  });

  function refreshEngineering() {
    Promise.all([
      fetch('/api/modules').then(r => r.json()).then(unwrap).catch(() => null),
      fetch('/api/status/summary').then(r => r.json()).then(unwrap).catch(() => null),
      fetch('/api/tasks/queue').then(r => r.json()).then(unwrap).catch(() => null),
      fetch('/api/skills/stats').then(r => r.json()).then(unwrap).catch(() => null),
      fetch('/api/portal/manifest').then(r => r.json()).then(unwrap).catch(() => null),
    ]).then(([modules, summary, tasks, skills, manifestEnvelope]) => {
      const manifest = manifestEnvelope || {};
      const modEl = document.getElementById('eng-modules');
      const buildEl = document.getElementById('eng-build');
      const planEl = document.getElementById('eng-plan');

      const modList = modules && modules.modules ? modules.modules : [];
      if (modEl) {
        modEl.innerHTML = modList.length ? modList.map(m => {
          const alive = m.alive || m.systemd === 'active';
          return `
            <div class="dash-card">
              <div class="dash-card-title">${escapeHtml(m.name || '—')}</div>
              <div class="dash-card-value ${alive ? 'c-green' : 'c-red'}">${alive ? 'active' : 'offline'}</div>
              <div class="dash-card-desc">PID ${escapeHtml(String(m.pid || '—'))} · ${escapeHtml(String(m.systemd || m.status || '—'))}</div>
            </div>
          `;
        }).join('') : '<div class="dash-card"><div class="dash-card-desc">Brak modułów</div></div>';
      }

      if (buildEl) {
        const portal = summary && summary.portal ? summary.portal : {};
        const surface = summary && summary.surface ? summary.surface : {};
        const pages = manifest && manifest.pages ? manifest.pages.length : '—';
        buildEl.innerHTML = [
          ['Hub', portal.port || '18888', 'serwer i router'],
          ['Surface', surface.tick !== undefined ? surface.tick : '—', 'stan live'],
          ['Strony', pages, 'SPA routes'],
          ['Endpointy', manifest && manifest.endpoints ? manifest.endpoints.length : '—', 'kontrakty API'],
        ].map(([label, value, desc]) => `
          <div class="dash-card">
            <div class="dash-card-title">${escapeHtml(label)}</div>
            <div class="dash-card-value c-purple">${escapeHtml(String(value))}</div>
            <div class="dash-card-desc">${escapeHtml(desc)}</div>
          </div>
        `).join('');
      }

      if (planEl) {
        const queue = tasks && tasks.tasks ? tasks.tasks : (tasks && tasks.queue ? tasks.queue : []);
        const skillCount = skills && skills.count !== undefined ? skills.count : (skills && skills.skills ? skills.skills.length : '—');
        planEl.innerHTML = [
          ['Tasks queued', queue.length || 0, 'TaskPlan queue'],
          ['Skills', skillCount, 'skill registry'],
          ['Plans', tasks && tasks.plans ? tasks.plans.length : '—', 'roadmap entries'],
          ['Lessons', tasks && tasks.lessons ? tasks.lessons.length : '—', 'operational memory'],
        ].map(([label, value, desc]) => `
          <div class="dash-card">
            <div class="dash-card-title">${escapeHtml(label)}</div>
            <div class="dash-card-value c-cyan">${escapeHtml(String(value))}</div>
            <div class="dash-card-desc">${escapeHtml(desc)}</div>
          </div>
        `).join('');
      }
    });
  }
})();
