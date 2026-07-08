/* ─── HERO CANVAS — HTRI Oscillators ──────────────────────── */
(function() {
  const canvas = document.getElementById('hero-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let W, H, centerX, centerY, radius;
  const N = 24;
  const phases = new Float64Array(N);
  const freqs = new Float64Array(N);
  const coupling = 0.02;
  let hue = 190;

  function resize() {
    const rect = canvas.parentElement.getBoundingClientRect();
    W = canvas.width = rect.width * devicePixelRatio;
    H = canvas.height = rect.height * devicePixelRatio;
    canvas.style.width = rect.width + 'px';
    canvas.style.height = rect.height + 'px';
    centerX = W / 2;
    centerY = H / 2;
    radius = Math.min(W, H) * 0.32;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
  }

  function init() {
    for (let i = 0; i < N; i++) {
      phases[i] = Math.random() * 2 * Math.PI;
      freqs[i] = 0.5 + Math.random() * 1.5;
    }
  }

  function step() {
    const dphi = new Float64Array(N);
    const sumSin = new Float64Array(N);
    const sumCos = new Float64Array(N);

    // Kuramoto coupling
    for (let i = 0; i < N; i++) {
      let ssin = 0, scos = 0;
      for (let j = 0; j < N; j++) {
        if (i === j) continue;
        const diff = phases[j] - phases[i];
        ssin += Math.sin(diff);
        scos += Math.cos(diff);
      }
      // 3-6-9 harmonic contribution
      const eff = phases[i];
      const harm = Math.sin(eff) + 0.5 * Math.sin(3*eff) + 0.33 * Math.sin(6*eff) + 0.25 * Math.sin(9*eff);
      dphi[i] = freqs[i] + coupling * ssin + 0.01 * harm;
    }

    for (let i = 0; i < N; i++) {
      phases[i] += dphi[i] * 0.03;
    }
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);

    // Background glow
    const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius * 1.4);
    gradient.addColorStop(0, 'rgba(0, 212, 255, 0.04)');
    gradient.addColorStop(0.5, 'rgba(136, 68, 255, 0.02)');
    gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, W, H);

    // Connecting lines (between close oscillators)
    for (let i = 0; i < N; i++) {
      const angle_i = phases[i];
      const xi = centerX + radius * Math.cos(angle_i);
      const yi = centerY + radius * Math.sin(angle_i);
      for (let j = i + 1; j < N; j++) {
        const angle_j = phases[j];
        const xj = centerX + radius * Math.cos(angle_j);
        const yj = centerY + radius * Math.sin(angle_j);
        const dist = Math.hypot(xj - xi, yj - yi);
        if (dist < radius * 0.7) {
          const alpha = 0.08 * (1 - dist / (radius * 0.7));
          ctx.beginPath();
          ctx.moveTo(xi, yi);
          ctx.lineTo(xj, yj);
          ctx.strokeStyle = `rgba(0, 212, 255, ${alpha})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }

    // Draw oscillators
    const orderParam = computeOrder();

    for (let i = 0; i < N; i++) {
      const angle = phases[i];
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);

      // Memory channel color (M0-M7)
      const ch = Math.floor(i / 3);
      const chHue = (ch / 8) * 260 + 180;
      const sat = 80 + 20 * Math.sin(phases[i] * 2);
      const lit = 50 + 20 * Math.cos(phases[i]);

      // Glow
      const glow = ctx.createRadialGradient(x, y, 0, x, y, 20 * devicePixelRatio);
      glow.addColorStop(0, `hsla(${chHue}, ${sat}%, ${lit}%, 0.3)`);
      glow.addColorStop(1, `hsla(${chHue}, ${sat}%, ${lit}%, 0)`);
      ctx.fillStyle = glow;
      ctx.beginPath();
      ctx.arc(x, y, 20 * devicePixelRatio, 0, Math.PI * 2);
      ctx.fill();

      // Dot
      ctx.beginPath();
      ctx.arc(x, y, 3 * devicePixelRatio, 0, Math.PI * 2);
      ctx.fillStyle = `hsla(${chHue}, ${sat}%, ${lit}%, 0.9)`;
      ctx.fill();

      // Phase tick
      const tickLen = 6 * devicePixelRatio;
      ctx.beginPath();
      ctx.moveTo(x + tickLen * Math.cos(angle), y + tickLen * Math.sin(angle));
      ctx.lineTo(x - tickLen * Math.cos(angle), y - tickLen * Math.sin(angle));
      ctx.strokeStyle = `hsla(${chHue}, ${sat}%, ${lit}%, 0.4)`;
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    // Center order parameter
    const R = orderParam.R;
    const psi = orderParam.psi;
    const cx = centerX + radius * 0.2 * Math.cos(psi);
    const cy = centerY + radius * 0.2 * Math.sin(psi);

    ctx.beginPath();
    ctx.arc(centerX, centerY, 4 * devicePixelRatio, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(255, 255, 255, ${0.3 * R})`;
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(cx, cy);
    ctx.strokeStyle = `rgba(0, 212, 255, ${0.5 * R})`;
    ctx.lineWidth = 2;
    ctx.stroke();

    // R value
    ctx.fillStyle = `rgba(0, 212, 255, ${0.4 + 0.3 * R})`;
    ctx.font = `${14 * devicePixelRatio}px "JetBrains Mono", monospace`;
    ctx.textAlign = 'center';
    ctx.fillText(`R = ${R.toFixed(3)}`, centerX, centerY + radius * 1.25);
  }

  function computeOrder() {
    let sumRe = 0, sumIm = 0;
    for (let i = 0; i < N; i++) {
      sumRe += Math.cos(phases[i]);
      sumIm += Math.sin(phases[i]);
    }
    const R = Math.sqrt(sumRe * sumRe + sumIm * sumIm) / N;
    const psi = Math.atan2(sumIm, sumRe);
    return { R, psi };
  }

  let animId = null;
  function loop() {
    step();
    draw();
    animId = requestAnimationFrame(loop);
  }

  window.addEventListener('resize', resize);
  resize();
  init();
  loop();
})();
