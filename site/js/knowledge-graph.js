/* ─── KNOWLEDGE GRAPH — 3D force-directed graph ──────────── */
(function() {
  'use strict';

  const container = document.getElementById('graph-container');
  if (!container) return;

  const W = container.clientWidth || 800;
  const H = container.clientHeight || 600;

  // ─── Categories ──────────────────────────────────────────
  const CAT_NAMES = ['PhaseNav','CIELingo','Daemon','Physics','Memory','System','Linguistics','Mathematics'];
  const CAT_COLORS = ['#00d4ff','#8844ff','#44ff88','#ffb347','#ff4466','#ff88cc','#44ddff','#aaff44'];

  // ─── Nodes ────────────────────────────────────────────────
  const SEED = 42;
  function seededRandom(s) {
    return function() {
      s = (s * 16807 + 0) % 2147483647;
      return (s - 1) / 2147483646;
    };
  }
  const rng = seededRandom(SEED);

  const nodes = [];
  const catCount = [8, 6, 14, 4, 5, 7, 5, 5];
  const catPrefix = ['PH','CI','DM','PHY','MEM','SYS','LNG','MTH'];
  const nodeNames = {
    PhaseNav: ['AGENT','MEMORY','EMOTION','TRANSFORM','BRAID','SCOPE','CONDITION','NEGATION'],
    CIELingo: ['MeaningLoop','SemanticScar','ImmuneSignal','KnowledgeBridge','Engine','RepairRouting'],
    Daemon: ['Kuramoto','ResonanceBridge','Neutrino','CIELingoSync','Nonlocal','LinuxSensor',
             'PhaseNavHot','PhaseNavCold','AnalogBlend','Archiver','Consolidator','Backend','Sentinel','Voice'],
    Physics: ['Metatime','PMNS','UnruhDrive','WarpDrift'],
    Memory: ['TieredMemory','HolonomicMemory','WPM','PhaseMemory','StateDB'],
    System: ['SurfaceMMap','DaemonRegistry','LinuxCards','SystemdTarget','Config','Orchestrator','AgentAttractor'],
    Linguistics: ['CaseGauge','DynamicDeixis','TAME','Valency','ScopeQuantifier'],
    Mathematics: ['LieAlgebra','BerryConnection','EulerIdentity','Collatz','PoincareDisk']
  };

  CAT_NAMES.forEach((cat, ci) => {
    const names = nodeNames[cat] || [];
    for (let i = 0; i < catCount[ci] && i < names.length; i++) {
      nodes.push({
        id: `${catPrefix[ci]}-${i}`,
        label: names[i],
        cat: cat,
        color: CAT_COLORS[ci],
        x: (rng() - 0.5) * 400,
        y: (rng() - 0.5) * 300,
        z: (rng() - 0.5) * 200,
        vx: 0, vy: 0, vz: 0
      });
    }
  });

  // ─── Edges ────────────────────────────────────────────────
  const edges = [];
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      if (nodes[i].cat === nodes[j].cat) {
        // same category: weak connection
        edges.push({ src: i, dst: j, strength: 0.1 + rng() * 0.2 });
      } else if (rng() < 0.04) {
        // cross-category
        edges.push({ src: i, dst: j, strength: 0.3 + rng() * 0.4 });
      }
    }
  }

  // ─── Force simulation (manual) ────────────────────────────
  function simulate() {
    const repel = 8000;
    const attract = 0.001;
    const damping = 0.85;
    const center = 0.001;

    for (let i = 0; i < nodes.length; i++) {
      const n = nodes[i];
      let fx = 0, fy = 0, fz = 0;

      // Center pull
      fx -= n.x * center;
      fy -= n.y * center;
      fz -= n.z * center;

      for (let j = i + 1; j < nodes.length; j++) {
        const m = nodes[j];
        const dx = n.x - m.x, dy = n.y - m.y, dz = n.z - m.z;
        const distSq = dx*dx + dy*dy + dz*dz + 1;
        const rep = repel / distSq;
        fx += dx / Math.sqrt(distSq) * rep;
        fy += dy / Math.sqrt(distSq) * rep;
        fz += dz / Math.sqrt(distSq) * rep;
      }

      // Edge attraction
      for (const e of edges) {
        if (e.src === i || e.dst === i) {
          const other = nodes[e.src === i ? e.dst : e.src];
          const dx = other.x - n.x, dy = other.y - n.y, dz = other.z - n.z;
          const dist = Math.sqrt(dx*dx + dy*dy + dz*dz + 1);
          const force = e.strength * attract * dist;
          fx += dx * force;
          fy += dy * force;
          fz += dz * force;
        }
      }

      n.vx = (n.vx + fx) * damping;
      n.vy = (n.vy + fy) * damping;
      n.vz = (n.vz + fz) * damping;
      n.x += n.vx;
      n.y += n.vy;
      n.z += n.vz;

      // Bounds
      const lim = 500;
      if (Math.abs(n.x) > lim) { n.x = Math.sign(n.x) * lim; n.vx *= -0.5; }
      if (Math.abs(n.y) > lim) { n.y = Math.sign(n.y) * lim; n.vy *= -0.5; }
      if (Math.abs(n.z) > lim) { n.z = Math.sign(n.z) * lim; n.vz *= -0.5; }
    }
  }

  // ─── Render ───────────────────────────────────────────────
  const canvas = document.getElementById('graph-canvas');
  if (!canvas) return;
  canvas.width = W; canvas.height = H;
  const ctx = canvas.getContext('2d');

  let angleX = 0.3, angleY = 0.5;
  let mouseDown = false, lastMX = 0, lastMY = 0;

  canvas.addEventListener('mousedown', e => { mouseDown = true; lastMX = e.clientX; lastMY = e.clientY; });
  window.addEventListener('mouseup', () => mouseDown = false);
  canvas.addEventListener('mousemove', e => {
    if (!mouseDown) return;
    const dx = e.clientX - lastMX;
    const dy = e.clientY - lastMY;
    angleY += dx * 0.01;
    angleX += dy * 0.01;
    angleX = Math.max(-1.2, Math.min(1.2, angleX));
    lastMX = e.clientX; lastMY = e.clientY;
  });

  // Touch support
  canvas.addEventListener('touchstart', e => {
    if (e.touches.length === 1) {
      mouseDown = true;
      lastMX = e.touches[0].clientX;
      lastMY = e.touches[0].clientY;
    }
  });
  canvas.addEventListener('touchend', () => mouseDown = false);
  canvas.addEventListener('touchmove', e => {
    if (!mouseDown || e.touches.length !== 1) return;
    const dx = e.touches[0].clientX - lastMX;
    const dy = e.touches[0].clientY - lastMY;
    angleY += dx * 0.01;
    angleX += dy * 0.01;
    angleX = Math.max(-1.2, Math.min(1.2, angleX));
    lastMX = e.touches[0].clientX;
    lastMY = e.touches[0].clientY;
  });

  function project(x, y, z) {
    // Rotate X
    let y1 = y * Math.cos(angleX) - z * Math.sin(angleX);
    let z1 = y * Math.sin(angleX) + z * Math.cos(angleX);
    y = y1; z = z1;
    // Rotate Y
    let x1 = x * Math.cos(angleY) + z * Math.sin(angleY);
    z1 = -x * Math.sin(angleY) + z * Math.cos(angleY);
    x = x1; z = z1;
    const scale = 600 / (800 + z);
    return { sx: W/2 + x * scale, sy: H/2 + y * scale, depth: z };
  }

  function render() {
    ctx.clearRect(0, 0, W, H);

    // Sort by depth
    const projected = nodes.map(n => ({ ...n, ...project(n.x, n.y, n.z) }));
    projected.sort((a, b) => a.depth - b.depth);

    // Edges
    for (const e of edges) {
      const a = projected[e.src];
      const b = projected[e.dst];
      ctx.beginPath();
      ctx.moveTo(a.sx, a.sy);
      ctx.lineTo(b.sx, b.sy);
      ctx.strokeStyle = `rgba(255,255,255,${0.04 + e.strength * 0.06})`;
      ctx.lineWidth = 0.5;
      ctx.stroke();
    }

    // Hover
    let hovered = null;
    const mx = lastMX - canvas.getBoundingClientRect().left;
    const my = lastMY - canvas.getBoundingClientRect().top;

    // Nodes
    for (const n of projected) {
      const rad = Math.max(3, 6 - n.depth * 0.003);
      const r2 = rad * 2;
      const alpha = Math.max(0.3, 1 - Math.abs(n.depth) * 0.001);

      ctx.beginPath();
      ctx.arc(n.sx, n.sy, r2, 0, Math.PI * 2);
      ctx.fillStyle = n.color + Math.round(alpha * 200).toString(16).padStart(2,'0');
      ctx.fill();

      // Check hover
      if (Math.abs(n.sx - mx) < 8 && Math.abs(n.sy - my) < 8) {
        hovered = n;
      }
    }

    // Labels (only for hovered or shallow)
    for (const n of projected) {
      if (n === hovered || Math.abs(n.depth) < 50) {
        const label = n.label;
        ctx.fillStyle = n === hovered ? '#ffffff' : 'rgba(255,255,255,0.5)';
        ctx.font = n === hovered ? 'bold 11px "Inter",sans-serif' : '10px "Inter",sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(label, n.sx, n.sy + 14);
      }
    }

    // Tooltip on hover
    if (hovered) {
      const catLabel = t('graph.categories.' + hovered.cat);
      container.setAttribute('title', `${hovered.label} (${catLabel})`);
    } else {
      container.removeAttribute('title');
    }

    simulate();
    requestAnimationFrame(render);
  }

  render();

  // Resize handler
  function resizeCanvas() {
    const rect = container.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;
  }
  window.addEventListener('resize', resizeCanvas);
})();
