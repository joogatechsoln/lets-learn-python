/* Optional three.js backend for the live preview.
 * It exposes the same small API as mini3d.js (box, cyl, cone, sphere, plane, group, cable, label, mover, tick ...),
 * so every scene in scenes.js works unchanged. It is only used when static/vendor/three.min.js is a real three.js
 * build (r128 or newer with a global THREE). If anything goes wrong, app.js falls back to the built-in engine. */
(function (global) {
  "use strict";
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const len = (a) => Math.hypot(a[0], a[1], a[2]);
  const norm = (a) => { const l = len(a) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };
  const rgb = (hex) => { if (Array.isArray(hex)) return hex; const h = hex.replace("#", ""); return [parseInt(h.slice(0, 2), 16) / 255, parseInt(h.slice(2, 4), 16) / 255, parseInt(h.slice(4, 6), 16) / 255]; };

  class Node {
    constructor(geom, o) {
      this.geom = geom; this.pos = o.pos || [0, 0, 0]; this.rot = o.rot || [0, 0, 0]; this.scale = o.scale || [1, 1, 1];
      this.color = rgb(o.color || "#cccccc"); this.emis = o.emis || 0; this.alpha = o.alpha == null ? 1 : o.alpha; this.ghost = !!o.ghost;
      this.grid = o.grid || 0; this.visible = true; this.children = []; this.parent = null; this.custom = null; this.obj = null;
    }
    add(n) { n.parent = this; this.children.push(n); return n; }
    set(o) { Object.assign(this, o.color ? { ...o, color: rgb(o.color) } : o); return this; }
  }

  function create(canvas, labelLayer, onFail) {
    const T = global.THREE;
    if (!T || !T.WebGLRenderer) return null;
    let renderer;
    try { renderer = new T.WebGLRenderer({ canvas, antialias: true, alpha: true }); } catch (e) { console.warn("three.js could not start:", e); return null; }
    renderer.setClearColor(0x000000, 0);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    try { renderer.shadowMap.enabled = true; renderer.shadowMap.type = T.PCFSoftShadowMap; } catch (e) { /* shadows are optional */ }
    const scene = new T.Scene(), camera = new T.PerspectiveCamera(46, 1, 0.3, 200);
    scene.add(new T.HemisphereLight(0xffffff, 0x3a4660, 0.95));
    const sun = new T.DirectionalLight(0xffffff, 0.85); sun.position.set(14, 24, 12);
    try { sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); const sc = sun.shadow.camera; sc.left = -32; sc.right = 32; sc.top = 32; sc.bottom = -32; sc.near = 1; sc.far = 80; sun.shadow.bias = -0.0005; } catch (e) { /* optional */ }
    scene.add(sun);
    scene.fog = new T.Fog(0x101a2f, 26, 72);

    const E = { engine: "three.js", canvas, cam: { yaw: 0.6, pitch: 0.55, dist: 26, target: [0, 1, 0] }, home: null, ticks: [], labels: [], autoRotate: true, lastTouch: 0, fog: [0.06, 0.1, 0.18], time: 0, running: true };
    E.root = new Node(null, {}); E.fx = E.root.add(new Node(null, {})); E.stat = E.root.add(new Node(null, {}));
    const GEO = { box: new T.BoxGeometry(1, 1, 1), cyl: new T.CylinderGeometry(1, 1, 1, 24), cone: new T.ConeGeometry(1, 1, 24), sphere: new T.SphereGeometry(1, 24, 16), plane: new T.PlaneGeometry(1, 1).rotateX(-Math.PI / 2) };
    const tmp = new T.Vector3();

    function sync(n, parentObj) {
      if (!n.obj) {
        n.obj = n.geom ? new T.Mesh(GEO[n.geom], new T.MeshStandardMaterial({ roughness: 0.75, metalness: 0.05 })) : new T.Group();
        n.obj.userData.node = n; n.obj.rotation.order = "YXZ";
        if (n.geom) { n.obj.castShadow = n.geom !== "plane"; n.obj.receiveShadow = true; }
        if (n.grid && n.geom === "plane") {
          const size = Math.max(n.scale[0], n.scale[2]), gh = new T.GridHelper(size, Math.max(1, Math.round(size / n.grid)), 0x7a97c9, 0x7a97c9);
          gh.scale.set(1 / n.scale[0], 1, 1 / n.scale[2]); gh.position.y = 0.01; gh.material.transparent = true; gh.material.opacity = 0.22; n.obj.add(gh);
        }
      }
      const o = n.obj;
      if (o.parent !== parentObj) parentObj.add(o);
      o.visible = n.visible !== false;
      if (n.custom) { o.matrixAutoUpdate = false; o.matrix.fromArray(n.custom); o.matrixWorldNeedsUpdate = true; }
      else { o.matrixAutoUpdate = true; o.position.set(n.pos[0], n.pos[1], n.pos[2]); o.rotation.set(n.rot[0], n.rot[1], n.rot[2]); o.scale.set(n.scale[0], n.scale[1], n.scale[2]); }
      if (n.geom) {
        const m = o.material, key = n.color.join() + "|" + n.emis + "|" + n.alpha + "|" + n.ghost;
        if (n._key !== key) {
          n._key = key;
          if (n.obj.castShadow !== undefined) n.obj.castShadow = !n.ghost && n.alpha >= 1 && n.geom !== "plane";
          if (n.ghost) { m.color.setRGB(0.42, 0.7, 1); m.emissive.setRGB(0.42, 0.7, 1); m.emissiveIntensity = 0.35; m.transparent = true; m.opacity = 0.22; m.depthWrite = false; }
          else { m.color.setRGB(n.color[0], n.color[1], n.color[2]); m.emissive.setRGB(n.color[0], n.color[1], n.color[2]); m.emissiveIntensity = n.emis; m.transparent = n.alpha < 1; m.opacity = n.alpha; m.depthWrite = n.alpha >= 1; }
          m.needsUpdate = true;
        }
      }
      const keep = new Set(n.children);
      for (let i = o.children.length - 1; i >= 0; i--) { const c = o.children[i], cn = c.userData && c.userData.node; if (cn && !keep.has(cn)) o.remove(c); }
      n.children.forEach((c) => sync(c, o));
    }

    E.resize = () => {
      const w = canvas.clientWidth, h = canvas.clientHeight;
      if (w && h && (canvas._w !== w || canvas._h !== h)) { canvas._w = w; canvas._h = h; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); }
    };
    let last = performance.now();
    function frame(now) {
      requestAnimationFrame(frame);
      if (!E.running || document.hidden || !canvas.clientWidth) return;
      try {
        const dt = Math.min((now - last) / 1000, 0.1); last = now; E.time += dt; E.resize();
        if (E.autoRotate && now - E.lastTouch > 3500) E.cam.yaw += dt * 0.07;
        E.ticks = E.ticks.filter((t) => !t.fn(E.time, dt));
        const c = E.cam, cp = Math.cos(c.pitch);
        camera.position.set(c.target[0] + c.dist * cp * Math.sin(c.yaw), c.target[1] + c.dist * Math.sin(c.pitch), c.target[2] + c.dist * cp * Math.cos(c.yaw));
        camera.lookAt(c.target[0], c.target[1], c.target[2]);
        scene.fog.color.setRGB(E.fog[0], E.fog[1], E.fog[2]);
        sync(E.root, scene);
        renderer.render(scene, camera);
        scene.updateMatrixWorld(true);
        const W = canvas.clientWidth, H = canvas.clientHeight;
        for (const L of E.labels) {
          if (L.target.obj) L.target.obj.getWorldPosition(tmp); else tmp.set(L.target[0], L.target[1], L.target[2]);
          tmp.y += L.dy; tmp.project(camera);
          if (tmp.z > 1 || tmp.z < -1 || L.target.visible === false) { L.el.style.display = "none"; continue; }
          L.el.style.display = ""; L.el.style.transform = `translate(-50%,-100%) translate(${(tmp.x * 0.5 + 0.5) * W}px,${(-tmp.y * 0.5 + 0.5) * H}px)`;
        }
      } catch (e) { E.running = false; console.error("three.js engine failed:", e); if (onFail) onFail(e); }
    }
    requestAnimationFrame(frame);

    const make = (geom, o) => { const n = new Node(geom, o); (o.parent || E.stat).add(n); return n; };
    E.box = (w, h, d, color, o = {}) => make("box", { ...o, color, scale: [w, h, d] });
    E.cyl = (r, h, color, o = {}) => make("cyl", { ...o, color, scale: [r, h, r] });
    E.cone = (r, h, color, o = {}) => make("cone", { ...o, color, scale: [r, h, r] });
    E.sphere = (r, color, o = {}) => make("sphere", { ...o, color, scale: [r, r, r] });
    E.plane = (w, d, color, o = {}) => make("plane", { ...o, color, scale: [w, 1, d] });
    E.group = (o = {}) => { const n = new Node(null, o); (o.parent || E.stat).add(n); return n; };
    E.cable = (a, b, color, r = 0.05, o = {}) => {
      const n = make("cyl", { ...o, color, scale: [r, 1, r] });
      n.setEnds = (p, q) => {
        const d = sub(q, p), L = len(d) || 0.001, y = norm(d), h = Math.abs(y[1]) > 0.98 ? [1, 0, 0] : [0, 1, 0], x = norm(cross(h, y)), z = cross(y, x);
        n.custom = [x[0] * r, x[1] * r, x[2] * r, 0, y[0] * L, y[1] * L, y[2] * L, 0, z[0] * r, z[1] * r, z[2] * r, 0, (p[0] + q[0]) / 2, (p[1] + q[1]) / 2, (p[2] + q[2]) / 2, 1];
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
    E.reset = () => { Object.assign(E.cam, E.home || { yaw: 0.6, pitch: 0.55, dist: 26 }); E.cam.target = [...(E.home || { target: [0, 1, 0] }).target]; };
    E.setHome = (h) => { E.home = { ...h, target: [...h.target] }; E.reset(); };

    E.pickAt = (cx, cy) => {
      const rc = canvas.getBoundingClientRect(), W = rc.width, H = rc.height, mx = cx - rc.left, my = cy - rc.top, p = new T.Vector3();
      let best = null, bestScore = 1e9; const stack = [E.root];
      while (stack.length) {
        const n = stack.pop(); n.children.forEach((c) => stack.push(c));
        if (!n.info || n.visible === false || !n.obj) continue;
        n.obj.getWorldPosition(p);
        const dist = Math.hypot(p.x - camera.position.x, p.y - camera.position.y, p.z - camera.position.z); p.project(camera);
        if (p.z > 1) continue;
        const rad = Math.max(n.scale[0], n.scale[1], n.scale[2]) * 0.55, pr = Math.max(16, (rad / (dist * 0.4245)) * (H / 2));
        const d = Math.hypot((p.x * 0.5 + 0.5) * W - mx, (-p.y * 0.5 + 0.5) * H - my);
        if (d < pr && d - pr < bestScore) { best = n; bestScore = d - pr; }
      }
      if (best) { const old = best.emis; best.emis = 1; E.after(700, () => { best.emis = old; }); if (E.onPick) E.onPick(best); }
    };
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
  global.Three3D = { create };
})(window);
