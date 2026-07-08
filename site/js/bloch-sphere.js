/* ─── Bloch Sphere 3D Engine — canvas-based, zero-dependency ── */
(function() {
  'use strict';

  // ─── 3D Vector math ─────────────────────────────────────────
  function vec3(x, y, z) { return { x, y, z }; }
  function vecAdd(a, b) { return { x: a.x + b.x, y: a.y + b.y, z: a.z + b.z }; }
  function vecSub(a, b) { return { x: a.x - b.x, y: a.y - b.y, z: a.z - b.z }; }
  function vecScale(v, s) { return { x: v.x * s, y: v.y * s, z: v.z * s }; }
  function vecDot(a, b) { return a.x * b.x + a.y * b.y + a.z * b.z; }
  function vecLen(v) { return Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z); }
  function vecNorm(v) { const l = vecLen(v); return l > 0 ? vecScale(v, 1 / l) : vec3(0, 0, 1); }
  function vecCross(a, b) { return { x: a.y * b.z - a.z * b.y, y: a.z * b.x - a.x * b.z, z: a.x * b.y - a.y * b.x }; }

  // ─── Rotation matrix from Euler angles ─────────────────────
  function rotMatrix(theta, phi, psi) {
    const c1 = Math.cos(theta), s1 = Math.sin(theta);
    const c2 = Math.cos(phi), s2 = Math.sin(phi);
    const c3 = Math.cos(psi), s3 = Math.sin(psi);
    return [
      [c2*c3, -c2*s3, s2],
      [c1*s3 + c3*s1*s2, c1*c3 - s1*s2*s3, -c2*s1],
      [s1*s3 - c1*c3*s2, c3*s1 + c1*s2*s3, c1*c2]
    ];
  }

  function applyRot(m, v) {
    return {
      x: m[0][0]*v.x + m[0][1]*v.y + m[0][2]*v.z,
      y: m[1][0]*v.x + m[1][1]*v.y + m[1][2]*v.z,
      z: m[2][0]*v.x + m[2][1]*v.y + m[2][2]*v.z,
    };
  }

  // ─── Perspective projection ─────────────────────────────────
  function project(v, cx, cy, scale, flip) {
    const perspective = 3.0;
    const d = perspective / (perspective + v.z);
    return {
      x: cx + v.x * scale * d,
      y: cy + (flip ? -v.y : v.y) * scale * d,
      z: v.z,
      d: d,
    };
  }

  // ─── Main BlochSphere class ─────────────────────────────────
  class BlochSphere {
    constructor(canvas) {
      this.canvas = canvas;
      this.ctx = canvas.getContext('2d');
      this.points = [];
      this.edges = [];
      this.vectors = [];
      this.program = [];
      this.autoRotate = true;
      this.rotX = 0.3;
      this.rotY = 0.5;
      this.rotZ = 0;
      this.showLabels = true;
      this.showGrid = true;
      this.showCouplings = true;
      this.animId = null;
      this._lastData = null;
      this._hovered = -1;
      this._dpr = devicePixelRatio || 1;

      // Channel colors
      this.chColors = [
        '#00d4ff', '#8844ff', '#44ff88', '#ffb347',
        '#ff4466', '#ff88cc', '#44ddff', '#aaff44', '#ffffff'
      ];
      this.chNames = ['M0 ID','M1 AGENT','M2 MEMORY','M3 SEM',
                      'M4 LOGIC','M5 AFFECT','M6 REL','M7 TIME','M8 META'];

      // Bind events
      canvas.addEventListener('mousemove', this._onMouseMove.bind(this));
      canvas.addEventListener('mouseleave', () => { this._hovered = -1; });
      canvas.addEventListener('click', this._onClick.bind(this));

      this._resize();
    }

    _resize() {
      const parent = this.canvas.parentElement;
      if (!parent) return;
      const rect = parent.getBoundingClientRect();
      const w = rect.width || 400;
      const h = rect.height || 400;
      this.canvas.width = w * this._dpr;
      this.canvas.height = h * this._dpr;
      this.canvas.style.width = w + 'px';
      this.canvas.style.height = h + 'px';
      this.width = w;
      this.height = h;
      this.cx = w / 2;
      this.cy = h / 2;
      this.scale = Math.min(w, h) * 0.35;
    }

    // ── Set data from API ────────────────────────────────────
    setData(data) {
      this._lastData = data;
      if (data && data.points) {
        this.points = data.points;
        this.edges = data.edges || [];
        this.vectors = data.vectors || [];
        this.program = data.program || [];
      }
    }

    // ── Animation loop ───────────────────────────────────────
    start() {
      const loop = () => {
        this._tick();
        this.draw();
        this.animId = requestAnimationFrame(loop);
      };
      loop();
    }

    stop() {
      if (this.animId) {
        cancelAnimationFrame(this.animId);
        this.animId = null;
      }
    }

    _tick() {
      if (this.autoRotate) {
        this.rotY += 0.005;
        this.rotX += 0.001;
      }
    }

    // ── Main draw ────────────────────────────────────────────
    draw() {
      const ctx = this.ctx;
      const w = this.width * this._dpr;
      const h = this.height * this._dpr;
      ctx.clearRect(0, 0, w, h);

      const cx = this.cx * this._dpr;
      const cy = this.cy * this._dpr;
      const sc = this.scale * this._dpr;

      // Background glow
      const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, sc * 2);
      grad.addColorStop(0, 'rgba(0,212,255,0.03)');
      grad.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, w, h);

      const rot = rotMatrix(this.rotX, this.rotY, this.rotZ);

      // Draw sphere
      if (this.showGrid) {
        this._drawSphere(rot, cx, cy, sc);
      }

      // Coupling lines
      if (this.showCouplings && this.points.length >= 3) {
        this._drawCouplings(rot, cx, cy, sc);
      }

      // Flow vectors: PhaseNav program execution field
      if (this.vectors.length > 0) {
        this._drawFlowVectors(rot, cx, cy, sc);
      }

      // Draw points
      if (this.points.length > 0) {
        this._drawPoints(rot, cx, cy, sc);
      }

      // Labels for channels
      if (this.showLabels) {
        this._drawLabels(rot, cx, cy, sc);
      }
    }

    _drawSphere(rot, cx, cy, sc) {
      const ctx = this.ctx;
      const steps = 16;

      // Latitude circles
      for (let i = 1; i < steps; i++) {
        const theta = (i / steps) * Math.PI;
        const r = Math.sin(theta) * sc;
        const y = Math.cos(theta) * sc;
        ctx.beginPath();
        ctx.ellipse(cx, cy - y * rot[1][1] - 0, r * Math.abs(rot[0][0]), r * 0.3, 0, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(255,255,255,0.05)';
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }

      // Longitude circles
      for (let i = 0; i < steps; i++) {
        const phi = (i / steps) * Math.PI * 2;
        ctx.beginPath();
        for (let j = 0; j <= 32; j++) {
          const t = (j / 32) * Math.PI;
          const v = { x: Math.sin(t) * Math.cos(phi), y: Math.cos(t), z: Math.sin(t) * Math.sin(phi) };
          const rv = applyRot(rot, v);
          const p = project(rv, cx, cy, sc, true);
          if (j === 0) ctx.moveTo(p.x, p.y);
          else ctx.lineTo(p.x, p.y);
        }
        ctx.strokeStyle = 'rgba(255,255,255,0.05)';
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }

      // Equator (brighter)
      ctx.beginPath();
      for (let j = 0; j <= 32; j++) {
        const t = (j / 32) * Math.PI * 2;
        const v = { x: Math.cos(t), y: 0, z: Math.sin(t) };
        const rv = applyRot(rot, v);
        const p = project(rv, cx, cy, sc, true);
        if (j === 0) ctx.moveTo(p.x, p.y);
        else ctx.lineTo(p.x, p.y);
      }
      ctx.strokeStyle = 'rgba(0,212,255,0.12)';
      ctx.lineWidth = 1;
      ctx.stroke();

      // Poles
      for (const sign of [-1, 1]) {
        const v = { x: 0, y: sign, z: 0 };
        const rv = applyRot(rot, v);
        const p = project(rv, cx, cy, sc, true);
        ctx.beginPath();
        ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255,255,255,0.3)';
        ctx.fill();
      }
    }

    _drawPoints(rot, cx, cy, sc) {
      const ctx = this.ctx;
      const projected = [];

      // Project all points
      this.points.forEach((pt, i) => {
        const v = { x: pt.x, y: pt.y, z: pt.z };
        const rv = applyRot(rot, v);
        const p = project(rv, cx, cy, sc, true);
        const ch = pt.ch || 0;
        const color = pt.color || this.chColors[ch % this.chColors.length];
        const isHover = i === this._hovered;
        projected.push({ ...p, pt, color, isHover, i });
      });

      // Sort by z (painter's algorithm)
      projected.sort((a, b) => a.z - b.z);

      projected.forEach(({ x, y, pt, color, isHover, i }) => {
        const R = pt.R || 0.5;
        const size = (4 + R * 6) * (this._dpr);
        const glow = isHover ? 12 : 2;

        // Glow
        ctx.beginPath();
        ctx.arc(x, y, size + glow, 0, Math.PI * 2);
        ctx.fillStyle = isHover ? 'rgba(0,212,255,0.2)' : 'rgba(0,212,255,0.05)';
        ctx.fill();

        // Point
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.shadowColor = color;
        ctx.shadowBlur = isHover ? 20 : 8;
        ctx.fill();
        ctx.shadowBlur = 0;

        // Label
        if (this.showLabels) {
          ctx.fillStyle = isHover ? '#fff' : 'rgba(255,255,255,0.6)';
          ctx.font = `${9 * this._dpr}px 'JetBrains Mono', monospace`;
          ctx.textAlign = 'center';
          ctx.fillText(pt.id || `φ[${pt.idx}]`, x, y - size - 6 * this._dpr);
        }
      });
    }

    _drawCouplings(rot, cx, cy, sc) {
      const ctx = this.ctx;
      if (this.edges && this.edges.length) {
        this.edges.forEach(edge => {
          const a = this.points[edge.from];
          const b = this.points[edge.to];
          if (!a || !b) return;
          const pa = project(applyRot(rot, {x:a.x, y:a.y, z:a.z}), cx, cy, sc, true);
          const pb = project(applyRot(rot, {x:b.x, y:b.y, z:b.z}), cx, cy, sc, true);
          const alpha = Math.max(0.05, Math.min(0.45, (edge.abs_weight || Math.abs(edge.weight || 0))));
          ctx.beginPath();
          ctx.moveTo(pa.x, pa.y);
          ctx.lineTo(pb.x, pb.y);
          ctx.strokeStyle = edge.weight >= 0 ? `rgba(0,212,255,${alpha})` : `rgba(255,68,102,${alpha})`;
          ctx.lineWidth = (0.5 + alpha * 2) * this._dpr;
          ctx.stroke();
        });
        return;
      }
      // Fallback: connect oscillators within same channel if backend has no edges.
      const chGroups = {};
      this.points.forEach(pt => {
        const ch = pt.ch || 0;
        if (!chGroups[ch]) chGroups[ch] = [];
        const v = { x: pt.x, y: pt.y, z: pt.z };
        const rv = applyRot(rot, v);
        const p = project(rv, cx, cy, sc, true);
        chGroups[ch].push(p);
      });

      Object.keys(chGroups).forEach(ch => {
        const pts = chGroups[ch];
        const color = this.chColors[parseInt(ch) % this.chColors.length];
        for (let i = 0; i < pts.length; i++) {
          for (let j = i + 1; j < pts.length; j++) {
            ctx.beginPath();
            ctx.moveTo(pts[i].x, pts[i].y);
            ctx.lineTo(pts[j].x, pts[j].y);
            ctx.strokeStyle = color.replace(')', ',0.15)').replace('rgb', 'rgba');
            if (!ctx.strokeStyle.includes('rgba')) ctx.strokeStyle = `rgba(255,255,255,0.08)`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      });
    }

    _drawFlowVectors(rot, cx, cy, sc) {
      const ctx = this.ctx;
      this.vectors.forEach(v => {
        const pt = this.points[v.from];
        if (!pt) return;
        const p0 = project(applyRot(rot, {x:pt.x, y:pt.y, z:pt.z}), cx, cy, sc, true);
        const p1 = project(applyRot(rot, {x:pt.x + v.x, y:pt.y + v.y, z:pt.z + v.z}), cx, cy, sc, true);
        const mag = Math.min(1, Math.abs(v.magnitude || 0));
        ctx.beginPath();
        ctx.moveTo(p0.x, p0.y);
        ctx.lineTo(p1.x, p1.y);
        ctx.strokeStyle = `rgba(255,255,255,${0.12 + mag * 0.35})`;
        ctx.lineWidth = (0.8 + mag * 1.5) * this._dpr;
        ctx.stroke();
        // arrow head
        const ang = Math.atan2(p1.y - p0.y, p1.x - p0.x);
        const ah = 5 * this._dpr;
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p1.x - Math.cos(ang - 0.45) * ah, p1.y - Math.sin(ang - 0.45) * ah);
        ctx.lineTo(p1.x - Math.cos(ang + 0.45) * ah, p1.y - Math.sin(ang + 0.45) * ah);
        ctx.closePath();
        ctx.fillStyle = `rgba(255,255,255,${0.15 + mag * 0.45})`;
        ctx.fill();
      });
    }

    _drawLabels(rot, cx, cy, sc) {
      const ctx = this.ctx;
      // Channel labels at the periphery
      this.chNames.forEach((name, ch) => {
        const angle = (ch / 8) * Math.PI * 2 - Math.PI / 2;
        const v = { x: Math.cos(angle) * 1.3, y: Math.sin(angle) * 0.3, z: Math.sin(angle) * 1.3 };
        const rv = applyRot(rot, v);
        const p = project(rv, cx, cy, sc, true);
        ctx.fillStyle = this.chColors[ch];
        ctx.font = `${9 * this._dpr}px 'JetBrains Mono', monospace`;
        ctx.textAlign = 'center';
        ctx.globalAlpha = 0.5;
        ctx.fillText(name, p.x, p.y);
        ctx.globalAlpha = 1;
      });
    }

    _onMouseMove(e) {
      const rect = this.canvas.getBoundingClientRect();
      const mx = (e.clientX - rect.left) * this._dpr;
      const my = (e.clientY - rect.top) * this._dpr;
      this._hovered = -1;
      // Would check proximity to points
    }

    _onClick(e) {
      // Placeholder for click interaction
    }

    // ── Fetch live data ──────────────────────────────────────
    fetchData() {
      fetch('/api/bloch')
        .then(r => r.json())
        .then(data => {
          this.setData(data);
        })
        .catch(() => {});
    }
  }

  // ─── Expose globally ────────────────────────────────────────
  window.BlochSphere = BlochSphere;
  console.log('✦ Bloch Sphere 3D Engine loaded');
})();
