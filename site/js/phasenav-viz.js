/* ─── PHASENAV EXPLORER — Operator visualization ──────────── */
(function() {
  'use strict';

  // Module-level state
  let _initialized = false;
  let _canvas, _ctx, _infoName, _infoCoh, _infoDesc;
  let _W, _H, _cx, _cy, _rad;

  function _resize() {
    if (!_canvas) return;
    const dpr = devicePixelRatio || 1;
    const parent = _canvas.parentElement;
    if (!parent) return;
    const rect = parent.getBoundingClientRect();
    if (!rect.width || !rect.height) return;
    _W = _canvas.width = rect.width * dpr;
    _H = _canvas.height = rect.height * dpr;
    _canvas.style.width = rect.width + 'px';
    _canvas.style.height = rect.height + 'px';
    _cx = _W / 2;
    _cy = _H / 2;
    _rad = Math.min(_W, _H) * 0.35;
  }

  function generateOperatorVec(idx) {
    const vec = new Float64Array(24);
    const base = idx / 15;
    for (let i = 0; i < 24; i++) {
      const ch = Math.floor(i / 3);
      const osc = i % 3;
      vec[i] = base * Math.PI * 2 + (ch * 0.4) + (osc * 0.2) +
               Math.sin(idx * 0.5 + i * 0.3) * 0.3 +
               (idx === 0 && (i >= 3 && i <= 5) ? 0.78 : 0) +
               (idx === 1 && (i >= 6 && i <= 8) ? 0.5 : 0);
    }
    for (let i = 0; i < 24; i++) {
      vec[i] = ((vec[i] % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
    }
    return vec;
  }

  function _draw(vec, op) {
    if (!_ctx) return;
    const ctx = _ctx;
    ctx.clearRect(0, 0, _W, _H);

    // Grid
    for (let r = _rad * 0.25; r <= _rad; r += _rad * 0.25) {
      ctx.beginPath();
      ctx.arc(_cx, _cy, r, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(255,255,255,0.05)';
      ctx.lineWidth = 0.5;
      ctx.stroke();
    }

    // Channel axes
    for (let ch = 0; ch < 8; ch++) {
      const angle = (ch / 8) * 2 * Math.PI - Math.PI / 2;
      ctx.beginPath();
      ctx.moveTo(_cx, _cy);
      ctx.lineTo(_cx + _rad * Math.cos(angle), _cy + _rad * Math.sin(angle));
      ctx.strokeStyle = 'rgba(255,255,255,0.03)';
      ctx.lineWidth = 0.5;
      ctx.stroke();
    }

    // Oscillators
    for (let i = 0; i < 24; i++) {
      const angle = vec[i] - Math.PI / 2;
      const dist = _rad * (0.3 + 0.5 * (i / 24));
      const x = _cx + dist * Math.cos(angle);
      const y = _cy + dist * Math.sin(angle);
      const ch = Math.floor(i / 3);
      const hue = 190 + ch * 20;

      ctx.beginPath();
      ctx.moveTo(_cx, _cy);
      ctx.lineTo(x, y);
      ctx.strokeStyle = `hsla(${hue}, 70%, 60%, 0.15)`;
      ctx.lineWidth = 0.5;
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(x, y, 3 * (devicePixelRatio || 1), 0, Math.PI * 2);
      ctx.fillStyle = `hsla(${hue}, 80%, 65%, 0.8)`;
      ctx.fill();
    }

    // Channel coherence arcs
    for (let ch = 0; ch < 8; ch++) {
      let sr = 0, si = 0;
      for (let o = 0; o < 3; o++) {
        const i = ch * 3 + o;
        sr += Math.cos(vec[i]);
        si += Math.sin(vec[i]);
      }
      const Rch = Math.sqrt(sr*sr + si*si) / 3;
      const baseAngle = (ch / 8) * 2 * Math.PI - Math.PI / 2;
      const arcLen = Rch * 0.3;
      ctx.beginPath();
      ctx.arc(_cx, _cy, _rad * 0.85, baseAngle - arcLen, baseAngle + arcLen);
      ctx.strokeStyle = `hsla(${190 + ch * 20}, 80%, 60%, ${0.2 + 0.4 * Rch})`;
      ctx.lineWidth = 3;
      ctx.stroke();
    }

    // Operator name
    ctx.fillStyle = 'rgba(255,255,255,0.15)';
    ctx.font = `${Math.round(32 * (devicePixelRatio || 1))}px "Inter", sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    if (op && op.id) ctx.fillText(op.id, _cx, _cy);
  }

  function selectOperator(idx) {
    if (!_canvas) { _init(); if (!_canvas) return; }
    const ops = t('operators');
    if (typeof ops === 'string') {
      const fallbacks = [
        { id: 'AGENT', desc: 'Operator tożsamości AGENT' },
        { id: 'MEMORY', desc: 'Operator pamięci M2' },
        { id: 'TRANSFORM', desc: 'Operator transformacji' },
      ];
      const op = fallbacks[idx] || fallbacks[0];
      const vec = generateOperatorVec(idx);
      _draw(vec, op);
      if (_infoName) _infoName.textContent = op.id;
      if (_infoCoh) _infoCoh.textContent = 'koherencja: —';
      if (_infoDesc) _infoDesc.textContent = op.desc;
      return;
    }
    const op = ops[idx] || ops[0];
    const vec = generateOperatorVec(idx);
    _draw(vec, op);

    if (_infoName) _infoName.textContent = op.id;
    let sr = 0, si = 0;
    for (let i = 0; i < 24; i++) {
      sr += Math.cos(vec[i]);
      si += Math.sin(vec[i]);
    }
    const R = Math.sqrt(sr*sr + si*si) / 24;
    if (_infoCoh) _infoCoh.textContent = `${t('phasenav.coherence')}: ${R.toFixed(4)}`;
    if (_infoDesc) _infoDesc.textContent = op.desc;
  }

  function _init() {
    _canvas = document.getElementById('phasenav-canvas');
    if (!_canvas) { _initialized = false; return; }
    _ctx = _canvas.getContext('2d');
    _infoName = document.querySelector('.info-name');
    _infoCoh = document.querySelector('.info-coherence');
    _infoDesc = document.querySelector('.info-desc');
    _resize();
    window.addEventListener('resize', _resize);
    _initialized = true;
  }

  // ─── Public API ──────────────────────────────────────────
  window.selectOperator = selectOperator;
  window.initPhaseNav = function() {
    _init();
    if (_initialized) {
      setTimeout(() => {
        const active = document.querySelector('.operator-btn.active');
        if (active) selectOperator(parseInt(active.dataset.idx) || 0);
        else selectOperator(0);
      }, 100);
    }
  };
  window.addEventListener('langchange', () => {
    if (!_initialized) return;
    const active = document.querySelector('.operator-btn.active');
    const idx = active ? parseInt(active.dataset.idx) || 0 : 0;
    selectOperator(idx);
  });

  // Auto-init on page load
  _init();
})();
