/* mini3d: a small, dependency-free WebGL scene engine for the live project preview.
 * Boxes, cylinders, cones, spheres, planes, cables, animated movers, HTML labels, orbit camera.
 * Scenes talk to it through the small API at the bottom (E.box, E.cyl, E.label, E.mover ...). */
(function (global) {
  "use strict";
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  const len = (a) => Math.hypot(a[0], a[1], a[2]);
  const norm = (a) => { const l = len(a) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };
  const ident = () => new Float32Array([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]);
  function mul(a, b) {
    const o = new Float32Array(16);
    for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++) {
      let s = 0;
      for (let k = 0; k < 4; k++) s += a[k * 4 + r] * b[c * 4 + k];
      o[c * 4 + r] = s;
    }
    return o;
  }
  function persp(fov, asp, n, f) {
    const t = 1 / Math.tan(fov / 2), o = new Float32Array(16);
    o[0] = t / asp; o[5] = t; o[10] = (f + n) / (n - f); o[11] = -1; o[14] = (2 * f * n) / (n - f);
    return o;
  }
  function look(e, t, up) {
    const z = norm(sub(e, t)), x = norm(cross(up, z)), y = cross(z, x);
    return new Float32Array([x[0], y[0], z[0], 0, x[1], y[1], z[1], 0, x[2], y[2], z[2], 0, -dot(x, e), -dot(y, e), -dot(z, e), 1]);
  }
  function rotM(ax, a) {
    const c = Math.cos(a), s = Math.sin(a), m = ident();
    if (ax === 0) { m[5] = c; m[6] = s; m[9] = -s; m[10] = c; }
    else if (ax === 1) { m[0] = c; m[2] = -s; m[8] = s; m[10] = c; }
    else { m[0] = c; m[1] = s; m[4] = -s; m[5] = c; }
    return m;
  }
  function compose(p, r, s) {
    let m = ident();
    if (r[1]) m = mul(m, rotM(1, r[1]));
    if (r[0]) m = mul(m, rotM(0, r[0]));
    if (r[2]) m = mul(m, rotM(2, r[2]));
    for (let c = 0; c < 3; c++) for (let k = 0; k < 3; k++) m[c * 4 + k] *= s[c];
    m[12] = p[0]; m[13] = p[1]; m[14] = p[2];
    return m;
  }
  function rgb(hex) {
    if (Array.isArray(hex)) return hex;
    const h = hex.replace("#", "");
    return [parseInt(h.slice(0, 2), 16) / 255, parseInt(h.slice(2, 4), 16) / 255, parseInt(h.slice(4, 6), 16) / 255];
  }

  // ---- geometry (interleaved position + normal) ---------------------------------------
  function build(verts, idx) { return { v: new Float32Array(verts), i: new Uint16Array(idx) }; }
  function boxGeom() {
    const F = [[[0, 0, 1], [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]], [[0, 0, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1], [1, 1, -1]],
      [[1, 0, 0], [1, -1, 1], [1, -1, -1], [1, 1, -1], [1, 1, 1]], [[-1, 0, 0], [-1, -1, -1], [-1, -1, 1], [-1, 1, 1], [-1, 1, -1]],
      [[0, 1, 0], [-1, 1, 1], [1, 1, 1], [1, 1, -1], [-1, 1, -1]], [[0, -1, 0], [-1, -1, -1], [1, -1, -1], [1, -1, 1], [-1, -1, 1]]];
    const v = [], i = [];
    F.forEach((f, k) => { for (let j = 1; j < 5; j++) v.push(f[j][0] / 2, f[j][1] / 2, f[j][2] / 2, ...f[0]); i.push(k * 4, k * 4 + 1, k * 4 + 2, k * 4, k * 4 + 2, k * 4 + 3); });
    return build(v, i);
  }
  function cylGeom(N, topR) {
    const v = [], i = [];
    for (let k = 0; k <= N; k++) {
      const a = (k / N) * Math.PI * 2, c = Math.cos(a), s = Math.sin(a);
      v.push(c, -0.5, s, c, 0, s, topR * c, 0.5, topR * s, c, 0, s);
    }
    for (let k = 0; k < N; k++) { const b = k * 2; i.push(b, b + 1, b + 3, b, b + 3, b + 2); }
    let base = v.length / 6;
    for (const y of [0.5, -0.5]) {
      const r = y > 0 ? topR : 1;
      v.push(0, y, 0, 0, y > 0 ? 1 : -1, 0);
      for (let k = 0; k <= N; k++) { const a = (k / N) * Math.PI * 2; v.push(r * Math.cos(a), y, r * Math.sin(a), 0, y > 0 ? 1 : -1, 0); }
      for (let k = 0; k < N; k++) i.push(base, base + 1 + k + (y > 0 ? 1 : 0), base + 1 + k + (y > 0 ? 0 : 1));
      base = v.length / 6;
    }
    return build(v, i);
  }
  function sphereGeom(LA, LO) {
    const v = [], i = [];
    for (let a = 0; a <= LA; a++) for (let b = 0; b <= LO; b++) {
      const th = (a / LA) * Math.PI, ph = (b / LO) * Math.PI * 2;
      const x = Math.sin(th) * Math.cos(ph), y = Math.cos(th), z = Math.sin(th) * Math.sin(ph);
      v.push(x, y, z, x, y, z);
    }
    for (let a = 0; a < LA; a++) for (let b = 0; b < LO; b++) { const p = a * (LO + 1) + b, q = p + LO + 1; i.push(p, q, p + 1, q, q + 1, p + 1); }
    return build(v, i);
  }
  function planeGeom() { return build([-0.5, 0, -0.5, 0, 1, 0, 0.5, 0, -0.5, 0, 1, 0, 0.5, 0, 0.5, 0, 1, 0, -0.5, 0, 0.5, 0, 1, 0], [0, 2, 1, 0, 3, 2]); }

  const VS = `attribute vec3 aPos; attribute vec3 aNor; uniform mat4 uVP; uniform mat4 uM; varying vec3 vN; varying vec3 vW;
    void main(){ vec4 w = uM * vec4(aPos, 1.0); vW = w.xyz; vN = (uM * vec4(aNor, 0.0)).xyz; gl_Position = uVP * w; }`;
  const FS = `precision mediump float; varying vec3 vN; varying vec3 vW;
    uniform vec3 uColor; uniform vec3 uLight; uniform vec3 uCam; uniform vec3 uFog; uniform float uEmis; uniform float uAlpha; uniform float uGhost; uniform float uGrid;
    void main(){
      vec3 n = normalize(vN); vec3 vd = normalize(uCam - vW);
      float d = max(dot(n, normalize(uLight)), 0.0); float hemi = 0.5 + 0.5 * n.y;
      vec3 col = uColor * (0.30 + 0.42 * hemi + 0.58 * d) + uColor * uEmis;
      float rim = pow(1.0 - max(dot(n, vd), 0.0), 3.0);
      col += vec3(rim * 0.12);
      float a = uAlpha;
      if (uGhost > 0.5) { vec3 holo = vec3(0.42, 0.70, 1.0); float r2 = pow(1.0 - abs(dot(n, vd)), 2.0); col = mix(holo * 0.5, holo, r2) + r2 * 0.35; a = 0.16 + r2 * 0.4; }
      if (uGrid > 0.0) { vec2 f = fract(vW.xz / uGrid); float ln = max(step(0.965, f.x), step(0.965, f.y)); col = mix(col, col * 1.9 + 0.05, ln * 0.55); }
      float fog = clamp((length(uCam - vW) - 24.0) / 46.0, 0.0, 0.7);
      gl_FragColor = vec4(mix(col, uFog, fog), a);
    }`;

  class Node {
    constructor(E, geom, o) {
      this.E = E; this.geom = geom; this.pos = o.pos || [0, 0, 0]; this.rot = o.rot || [0, 0, 0]; this.scale = o.scale || [1, 1, 1];
      this.color = rgb(o.color || "#cccccc"); this.emis = o.emis || 0; this.alpha = o.alpha == null ? 1 : o.alpha; this.ghost = !!o.ghost;
      this.grid = o.grid || 0; this.visible = true; this.children = []; this.parent = null; this.custom = null; this.world = ident();
    }
    add(n) { n.parent = this; this.children.push(n); return n; }
    set(o) { Object.assign(this, o.color ? { ...o, color: rgb(o.color) } : o); return this; }
  }

  function create(canvas, labelLayer) {
    const gl = canvas.getContext("webgl", { antialias: true, alpha: true, premultipliedAlpha: false }) || canvas.getContext("experimental-webgl");
    if (!gl) return null;
    const E = { canvas, gl, root: new Node(null, null, {}), cam: { yaw: 0.6, pitch: 0.55, dist: 26, target: [0, 1, 0] }, home: null, ticks: [], labels: [],
      autoRotate: true, lastTouch: 0, fog: [0.06, 0.1, 0.18], light: [0.5, 1, 0.6], time: 0, running: true };
    E.root.E = E; E.fx = E.root.add(new Node(E, null, {})); E.stat = E.root.add(new Node(E, null, {}));
    const prog = gl.createProgram();
    for (const [t, src] of [[gl.VERTEX_SHADER, VS], [gl.FRAGMENT_SHADER, FS]]) {
      const s = gl.createShader(t); gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { console.error(gl.getShaderInfoLog(s)); return null; }
      gl.attachShader(prog, s);
    }
    gl.bindAttribLocation(prog, 0, "aPos"); gl.bindAttribLocation(prog, 1, "aNor"); gl.linkProgram(prog); gl.useProgram(prog);
    const U = {};
    ["uVP", "uM", "uColor", "uLight", "uCam", "uFog", "uEmis", "uAlpha", "uGhost", "uGrid"].forEach((n) => (U[n] = gl.getUniformLocation(prog, n)));
    const mk = (g) => { const vb = gl.createBuffer(), ib = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vb); gl.bufferData(gl.ARRAY_BUFFER, g.v, gl.STATIC_DRAW);
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ib); gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, g.i, gl.STATIC_DRAW); return { vb, ib, n: g.i.length }; };
    const G = { box: mk(boxGeom()), cyl: mk(cylGeom(24, 1)), cone: mk(cylGeom(24, 0.001)), sphere: mk(sphereGeom(12, 18)), plane: mk(planeGeom()) };
    gl.enable(gl.DEPTH_TEST); gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); gl.clearColor(0, 0, 0, 0);

    const eye = () => { const c = E.cam, cp = Math.cos(c.pitch); return [c.target[0] + c.dist * cp * Math.sin(c.yaw), c.target[1] + c.dist * Math.sin(c.pitch), c.target[2] + c.dist * cp * Math.cos(c.yaw)]; };
    function walk(n, parentW, out) {
      n.world = n.custom ? mul(parentW, n.custom) : mul(parentW, compose(n.pos, n.rot, n.scale));
      if (!n.visible) return;
      if (n.geom) out.push(n);
      for (const c of n.children) walk(c, n.world, out);
    }
    function draw(n) {
      const g = G[n.geom];
      gl.bindBuffer(gl.ARRAY_BUFFER, g.vb); gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, g.ib);
      gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 24, 0);
      gl.enableVertexAttribArray(1); gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 24, 12);
      gl.uniformMatrix4fv(U.uM, false, n.world); gl.uniform3fv(U.uColor, n.color); gl.uniform1f(U.uEmis, n.emis);
      gl.uniform1f(U.uAlpha, n.alpha); gl.uniform1f(U.uGhost, n.ghost ? 1 : 0); gl.uniform1f(U.uGrid, n.grid);
      gl.drawElements(gl.TRIANGLES, g.n, gl.UNSIGNED_SHORT, 0);
    }
    E.resize = () => {
      const r = Math.min(window.devicePixelRatio || 1, 2), w = canvas.clientWidth, h = canvas.clientHeight;
      if (w && h && (canvas.width !== Math.round(w * r) || canvas.height !== Math.round(h * r))) { canvas.width = Math.round(w * r); canvas.height = Math.round(h * r); }
    };
    let last = performance.now();
    function frame(now) {
      requestAnimationFrame(frame);
      if (!E.running || document.hidden || !canvas.clientWidth) return;
      const dt = Math.min((now - last) / 1000, 0.1); last = now; E.time += dt; E.resize();
      if (E.autoRotate && now - E.lastTouch > 3500) E.cam.yaw += dt * 0.07;
      E.ticks = E.ticks.filter((t) => !t.fn(E.time, dt));
      gl.viewport(0, 0, canvas.width, canvas.height); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      const e = eye(), vp = mul(persp(0.8, canvas.width / canvas.height, 0.3, 200), look(e, E.cam.target, [0, 1, 0]));
      E.lastVP = vp; E.lastEye = e;
      gl.uniformMatrix4fv(U.uVP, false, vp); gl.uniform3fv(U.uLight, E.light); gl.uniform3fv(U.uCam, e); gl.uniform3fv(U.uFog, E.fog);
      const list = []; walk(E.root, ident(), list);
      const op = list.filter((n) => n.alpha >= 1 && !n.ghost), tr = list.filter((n) => n.alpha < 1 || n.ghost);
      gl.depthMask(true); op.forEach(draw);
      tr.sort((a, b) => Math.hypot(b.world[12] - e[0], b.world[13] - e[1], b.world[14] - e[2]) - Math.hypot(a.world[12] - e[0], a.world[13] - e[1], a.world[14] - e[2]));
      gl.depthMask(false); tr.forEach(draw); gl.depthMask(true);
      const W = canvas.clientWidth, H = canvas.clientHeight;
      for (const L of E.labels) {
        const p = L.target.world ? [L.target.world[12], L.target.world[13], L.target.world[14]] : L.target;
        const x = p[0], y = p[1] + L.dy, z = p[2];
        const cx = vp[0] * x + vp[4] * y + vp[8] * z + vp[12], cy = vp[1] * x + vp[5] * y + vp[9] * z + vp[13], cw = vp[3] * x + vp[7] * y + vp[11] * z + vp[15];
        if (cw <= 0.1 || (L.target.visible === false)) { L.el.style.display = "none"; continue; }
        L.el.style.display = ""; L.el.style.transform = `translate(-50%,-100%) translate(${((cx / cw) * 0.5 + 0.5) * W}px,${(-(cy / cw) * 0.5 + 0.5) * H}px)`;
      }
    }
    requestAnimationFrame(frame);

    // ---- scene-building API ------------------------------------------------------------
    const make = (geom, o) => { const n = new Node(E, geom, o); (o.parent || E.stat).add(n); return n; };
    E.box = (w, h, d, color, o = {}) => make("box", { ...o, color, scale: [w, h, d] });
    E.cyl = (r, h, color, o = {}) => make("cyl", { ...o, color, scale: [r, h, r] });
    E.cone = (r, h, color, o = {}) => make("cone", { ...o, color, scale: [r, h, r] });
    E.sphere = (r, color, o = {}) => make("sphere", { ...o, color, scale: [r, r, r] });
    E.plane = (w, d, color, o = {}) => make("plane", { ...o, color, scale: [w, 1, d] });
    E.group = (o = {}) => { const n = new Node(E, null, o); (o.parent || E.stat).add(n); return n; };
    E.cable = (a, b, color, r = 0.05, o = {}) => {
      const n = make("cyl", { ...o, color, scale: [r, 1, r] });
      n.setEnds = (p, q) => {
        const d = sub(q, p), L = len(d) || 0.001, y = norm(d), h = Math.abs(y[1]) > 0.98 ? [1, 0, 0] : [0, 1, 0], x = norm(cross(h, y)), z = cross(y, x);
        n.custom = new Float32Array([x[0] * r, x[1] * r, x[2] * r, 0, y[0] * L, y[1] * L, y[2] * L, 0, z[0] * r, z[1] * r, z[2] * r, 0, (p[0] + q[0]) / 2, (p[1] + q[1]) / 2, (p[2] + q[2]) / 2, 1]);
      };
      n.setEnds(a, b); return n;
    };
    E.label = (target, html, o = {}) => {
      const el = document.createElement("div"); el.className = "lbl " + (o.cls || ""); el.innerHTML = html; labelLayer.appendChild(el);
      const L = { target, el, dy: o.dy == null ? 1 : o.dy, owner: o.owner || null, set: (h) => { el.innerHTML = h; } };
      E.labels.push(L); return L;
    };
    E.tick = (fn, owner) => { E.ticks.push({ fn, owner: owner || null }); };
    E.after = (ms, fn, owner) => { let t = 0; E.tick((_, dt) => { t += dt * 1000; if (t >= ms) { fn(); return true; } return false; }, owner); };
    E.remove = (n) => { if (n.parent) n.parent.children = n.parent.children.filter((c) => c !== n); E.labels = E.labels.filter((L) => { if (L.target === n) { L.el.remove(); return false; } return true; }); };
    E.clear = (group) => {
      group.children = [];
      E.ticks = E.ticks.filter((t) => t.owner !== group);
      E.labels = E.labels.filter((L) => { if (L.owner === group) { L.el.remove(); return false; } return true; });
    };
    // Move a node along a polyline at `speed` units per second. loop: repeat. delay: seconds before it starts.
    E.mover = (node, pts, speed, o = {}) => {
      const cum = [0]; for (let i = 1; i < pts.length; i++) cum.push(cum[i - 1] + Math.hypot(...sub(pts[i], pts[i - 1])));
      const total = cum[cum.length - 1] || 1; let s = -(o.delay || 0) * speed; node.visible = false;
      E.tick((_, dt) => {
        s += speed * dt;
        if (s < 0) return false;
        if (s >= total) { if (o.loop) s -= total; else { E.remove(node); if (o.onDone) o.onDone(); return true; } }
        node.visible = true; let k = 1; while (k < cum.length - 1 && cum[k] < s) k++;
        const u = (s - cum[k - 1]) / ((cum[k] - cum[k - 1]) || 1); node.pos = [0, 1, 2].map((i) => pts[k - 1][i] + (pts[k][i] - pts[k - 1][i]) * u);
        return false;
      }, o.owner);
    };
    E.reset = () => { Object.assign(E.cam, E.home || { yaw: 0.6, pitch: 0.55, dist: 26, target: [0, 1, 0] }); E.cam.target = [...(E.home || { target: [0, 1, 0] }).target]; };
    E.setHome = (h) => { E.home = { ...h, target: [...h.target] }; E.reset(); };

    // Click to inspect: the tagged node (one with an .info object) nearest to the click on screen
    E.pickAt = (cx, cy) => {
      const rc = canvas.getBoundingClientRect(), W = rc.width, H = rc.height, mx = cx - rc.left, my = cy - rc.top, vp = E.lastVP, eye0 = E.lastEye;
      if (!vp) return;
      let best = null, bestScore = 1e9; const stack = [E.root];
      while (stack.length) {
        const n = stack.pop(); n.children.forEach((c) => stack.push(c));
        if (!n.info || n.visible === false) continue;
        const x = n.world[12], y = n.world[13], z = n.world[14], cw = vp[3] * x + vp[7] * y + vp[11] * z + vp[15];
        if (cw <= 0.1) continue;
        const sx = ((vp[0] * x + vp[4] * y + vp[8] * z + vp[12]) / cw * 0.5 + 0.5) * W, sy = (-(vp[1] * x + vp[5] * y + vp[9] * z + vp[13]) / cw * 0.5 + 0.5) * H;
        const rad = Math.max(n.scale[0], n.scale[1], n.scale[2]) * 0.55, dist = Math.hypot(eye0[0] - x, eye0[1] - y, eye0[2] - z);
        const pr = Math.max(16, (rad / (dist * 0.4228)) * (H / 2)), d = Math.hypot(sx - mx, sy - my);
        if (d < pr && d - pr < bestScore) { best = n; bestScore = d - pr; }
      }
      if (best) { const old = best.emis; best.emis = 1; E.after(700, () => { best.emis = old; }); if (E.onPick) E.onPick(best); }
    };

    // ---- orbit controls -----------------------------------------------------------------
    let drag = null, downAt = null;
    canvas.style.touchAction = "none";
    canvas.addEventListener("pointerdown", (e) => { drag = { x: e.clientX, y: e.clientY }; downAt = { x: e.clientX, y: e.clientY }; E.lastTouch = performance.now(); canvas.setPointerCapture(e.pointerId); });
    canvas.addEventListener("pointermove", (e) => {
      if (!drag) return;
      E.cam.yaw -= (e.clientX - drag.x) * 0.008; E.cam.pitch = Math.max(0.12, Math.min(1.35, E.cam.pitch + (e.clientY - drag.y) * 0.006));
      drag = { x: e.clientX, y: e.clientY }; E.lastTouch = performance.now();
    });
    canvas.addEventListener("pointerup", (e) => { drag = null; if (downAt && Math.hypot(e.clientX - downAt.x, e.clientY - downAt.y) < 5) E.pickAt(e.clientX, e.clientY); downAt = null; });
    canvas.addEventListener("wheel", (e) => { e.preventDefault(); E.cam.dist = Math.max(8, Math.min(60, E.cam.dist * Math.exp(e.deltaY * 0.001))); E.lastTouch = performance.now(); }, { passive: false });
    canvas.addEventListener("dblclick", () => E.reset());
    return E;
  }
  global.Mini3D = { create };
})(window);
