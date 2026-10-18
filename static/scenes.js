/* Industry scenes for the live preview. Each scene has:
 *   setup(E)           builds the fixed environment once
 *   render(E, W, d)    rebuilds the parts that depend on the learner's program (W = world state, d = dynamic group)
 *   onOutput(E, W, s)  plays a short animation when the program prints a new line
 *   actions            buttons shown above the scene
 * Solid objects are things the learner's code has created; translucent blue "ghost" objects are the blueprint still to build. */
(function (global) {
  "use strict";
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const fmt = (n) => (typeof n === "number" && !Number.isInteger(n) ? +n.toFixed(2) : n);
  const PAL = ["#f2b01e", "#e46a5a", "#59b6ff", "#7ed6a0"];
  const kit = (E, d) => ({
    B: (w, h, dp, c, x, y, z, o = {}) => E.box(w, h, dp, c, { parent: d, pos: [x, y, z], ...o }),
    C: (r, h, c, x, y, z, o = {}) => E.cyl(r, h, c, { parent: d, pos: [x, y, z], ...o }),
    S: (r, c, x, y, z, o = {}) => E.sphere(r, c, { parent: d, pos: [x, y, z], ...o }),
    K: (r, h, c, x, y, z, o = {}) => E.cone(r, h, c, { parent: d, pos: [x, y, z], ...o }),
    L: (t, html, cls, dy) => E.label(t, html, { owner: d, cls, dy }),
    A: (fn) => E.tick(fn, d),
  });
  const fx = (E, shape, color, pts, speed, opt = {}) => {   // one-shot effect object that travels a path
    const n = shape === "box" ? E.box(0.4, 0.4, 0.4, color, { parent: E.fx, emis: 0.7 }) : E.sphere(opt.r || 0.22, color, { parent: E.fx, emis: 0.8 });
    E.mover(n, pts, speed, { onDone: opt.onDone });
    return n;
  };
  const bubble = (E, at, html, cls, ms) => {
    const L = E.label(at, html, { owner: E.fx, cls: cls || "ok", dy: 1 });
    E.after(ms || 2600, () => { L.el.remove(); E.labels = E.labels.filter((x) => x !== L); }, E.fx);
  };
  const sign = (E, K, W, x, y, z, w, color) => {
    const b = K.B(w, 1.3, 0.25, color || "#0e1a2e", x, y, z, { emis: 0.12, ghost: !W.banner });
    K.L(b, W.banner ? esc(W.banner) : "<i>waiting for print()...</i>", "sign" + (W.banner ? " on" : ""), 0.2);
    b.info = { title: "Banner sign", rows: [["It shows", W.banner || "nothing yet"]], code: 'print("Welcome to ...")', note: "Whatever your program prints that starts with Welcome appears here." };
  };
  const probe = (E, K, W, x, z, label) => {
    const s = W.sensor, live = !!s, col = !live ? "#6fb3ff" : s.alert ? "#ff6b5e" : "#2fb67c";
    K.C(0.07, 1.6, "#9aa8bf", x, 0.8, z, { ghost: !live });
    const ball = K.S(0.28, col, x, 1.8, z, { emis: live ? 0.8 : 0, ghost: !live });
    ball.info = live ? { title: s.name, rows: [["Reading", fmt(s.reading) + " " + (s.unit || "")], ["Alert", s.alert ? "yes" : "none"]], code: "print(reading)", note: "Set from the sensor_name and reading variables in your code." }
      : { title: "Probe (not built yet)", rows: [["Status", "blueprint"]], code: 'sensor_name = "..."\nreading = 0.0', note: "Chapter 2 builds this." };
    if (live) { const ring = K.S(0.5, col, x, 1.8, z, { alpha: 0.22 }); K.A((t) => { const k = 1 + 0.35 * Math.sin(t * 3); ring.scale = [0.5 * k, 0.5 * k, 0.5 * k]; return false; }); }
    K.L(ball, live ? `${esc(s.name)}<br><b>${fmt(s.reading)} ${esc(s.unit || "")}</b>` : esc(label || "probe: not built yet"), live ? "info" : "ghost", 0.5);
  };
  const flag = (th, W, r) => (W.hasLevel && r.qty !== undefined ? (r.qty <= W.level ? "le" : "gt") : null);
  const tx = (W, key, dflt) => (W.th.world_text && W.th.world_text[key]) || dflt;
  const fill = (E, bg) => { E.fog = bg; };
  // What the Inspector shows when you click a thing in the 3D world, including the Python behind it
  const rinfo = (W, r) => {
    const v = W.th.v, dq = W.vars[v.qtys], isMap = dq && typeof dq === "object" && !Array.isArray(dq), rows = [["Name", r.name]];
    if (r.qty !== undefined) rows.push([W.th.qty_unit || "Quantity", fmt(r.qty)]);
    if (r.rate !== undefined) rows.push(["Rate", W.th.rp + fmt(r.rate) + W.th.rs]);
    if (r.qty !== undefined && r.rate !== undefined) rows.push([W.th.total_label || "Value", W.th.tp + fmt(+(r.qty * r.rate).toFixed(4)) + W.th.ts]);
    const f = flag(W.th, W, r);
    if (f) rows.push(["Rule", (f === "le" ? "at or below " : "above ") + W.level]);
    const read = isMap ? `${v.qtys}["${r.name}"]` : v.qty;
    return r.real ? { title: r.name, rows, code: `print(${read})   # ${fmt(r.qty)}`, note: "Built by your code." }
      : { title: r.name + " (blueprint)", rows, code: `${v.qtys}["${r.name}"] = ${r.qty}`, note: "Not built yet. Your code creates it." };
  };
  const shelfUnit = (E, K, W, i, x, z, o) => {            // retail and pharmacy shelf with stacked items
    const r = W.records[i], ghost = !r.real, f = flag(W.th, W, r), col = o.itemColor(i);
    K.B(0.14, 3.8, 1.3, o.frame, x - 2.4, 1.9, z, { ghost }); K.B(0.14, 3.8, 1.3, o.frame, x + 2.4, 1.9, z, { ghost });
    for (let b = 0; b < 3; b++) { const bd = K.B(4.9, 0.14, 1.3, o.board, x, 0.9 + b * 1.15, z, { ghost }); if (b === 0) bd.info = rinfo(W, r); }
    const n = Math.min(Math.max(Math.round(r.qty || 0), 0), 24);
    const low = f === o.lowFlag;
    for (let k = 0; k < n; k++) {
      const row = Math.floor(k / 8), c = k % 8, it = K.B(0.46, 0.5, 0.7, col, x - 2.0 + c * 0.57, 1.2 + row * 1.15, z, { ghost, emis: low ? 0.25 : 0 });
      if (low) K.A((t) => { it.emis = 0.15 + 0.25 * Math.abs(Math.sin(t * 3 + c)); return false; });
    }
    const tag = `<b>${esc(r.name)}</b><br>${r.qty === undefined ? "?" : fmt(r.qty)} ${esc(o.unit)}${r.rate !== undefined ? " · " + esc(W.th.rp) + fmt(r.rate) + esc(W.th.rs) : ""}`;
    K.L(K.B(0.01, 0.01, 0.01, "#000", x, 4.0, z, { alpha: 0 }), tag + (low ? `<br><span class="bad">${esc(o.lowText)}</span>` : f ? `<br><span class="good">${esc(o.okText)}</span>` : ""), ghost ? "ghost" : low ? "warn" : "info", i % 2 ? 1.7 : 0.2);
  };

  const S = {};

  // ---------------------------------------------------------------- networking: Packet Tracer style
  const NET = { console: [-12, 0.5, -6.5], router: [0, 0.7, -7], server: [7, 0.8, -7], cloud: [0, 2.2, -12] };
  S.networking = {
    bg: ["#0d1b33", "#142b4d"], home: { yaw: 0.3, pitch: 0.78, dist: 25, target: [0, 0, 0] },
    setup(E) {
      fill(E, [0.07, 0.12, 0.22]);
      E.plane(60, 44, "#16294a", { grid: 1.5 });
      [[-1.2, 0], [0, 0.4], [1.3, -0.2]].forEach(([x, z], i) => E.sphere(1.4 - i * 0.15, "#e8f1ff", { pos: [x * 1.6 + NET.cloud[0], NET.cloud[1] + (i === 1 ? 0.5 : 0), NET.cloud[2] + z], alpha: 0.92 }));
      E.label(E.sphere(0.01, "#fff", { pos: NET.cloud, alpha: 0 }), "Internet", { cls: "dev", dy: 2.4 });
      E.box(2.8, 0.55, 1.5, "#1fa89a", { pos: NET.router, emis: 0.1 });
      [-0.9, 0, 0.9].forEach((x) => E.cyl(0.05, 0.9, "#cfe9e6", { pos: [NET.router[0] + x, 1.3, NET.router[2] - 0.4] }));
      E.label(E.stat.children[E.stat.children.length - 1], "Core router", { cls: "dev", dy: 0.8 });
      E.box(1.6, 2.4, 1.3, "#566a8f", { pos: [NET.server[0], 1.2, NET.server[2]] });
      for (let k = 0; k < 5; k++) E.box(1.3, 0.12, 0.05, k % 2 ? "#2fb67c" : "#5ba4ff", { pos: [NET.server[0], 0.5 + k * 0.4, NET.server[2] + 0.67], emis: 0.8 });
      E.label(E.stat.children[E.stat.children.length - 1], "Server", { cls: "dev", dy: 1.6 });
      E.box(1.7, 1.0, 1.1, "#3a4a69", { pos: [NET.console[0], 0.5, NET.console[2]] }); E.box(1.3, 0.8, 0.12, "#0b1220", { pos: [NET.console[0], 1.4, NET.console[2]], emis: 0.4 });
      E.label(E.stat.children[E.stat.children.length - 1], "Technician PC", { cls: "dev", dy: 0.7 });
      E.cable(NET.cloud, NET.router, "#5ba4ff", 0.07); E.cable(NET.router, NET.server, "#5ba4ff", 0.07);
    },
    actions: [{ label: "Send ping", fn: (E, W) => S.networking.onOutput(E, W, "ping") }],
    render(E, W, d) {
      const K = kit(E, d), xs = [-10.5, -3.5, 3.5, 10.5];
      sign(E, K, W, 0, 5.3, -10, 9, "#0e1a2e");
      const link = W.err ? "#ff6b5e" : "#2bd4c0";
      const c = E.cable(NET.console, NET.router, link, 0.05, { parent: d, emis: 0.6 });
      if (W.err) K.L(K.B(0.01, 0.01, 0.01, "#000", NET.console[0], 2, NET.console[2], { alpha: 0 }), "Request timed out<br>(your code raised an error)", "bad", 0.2);
      probe(E, K, W, -5.5, -7.5, "signal probe: not built yet");
      W.records.forEach((r, i) => {
        const x = xs[i], z = i % 2 ? 3.5 : 1, ghost = !r.real, n = Math.min(Math.round(r.qty || 0), 12);
        const sw = K.B(2.6, 0.4, 1.1, "#3b82f6", x, 0.25, z, { ghost, emis: 0.1 });
        sw.info = rinfo(W, r);
        const limit = W.hasLevel ? W.level : 24, lit = Math.round(Math.min((r.qty || 0) / limit, 1) * 8);
        for (let p = 0; p < 8; p++) K.B(0.2, 0.08, 0.05, p < lit ? "#2fb67c" : "#2b3d5c", x - 1.0 + p * 0.29, 0.28, z + 0.56, { emis: p < lit && !ghost ? 0.9 : 0, ghost });
        E.cable([x, 0.3, z], NET.router, ghost ? "#6fb3ff" : link, 0.05, { parent: d, emis: ghost ? 0 : 0.5, ghost });
        for (let k = 0; k < n; k++) {
          const px = x - 2.1 + (k % 6) * 0.84, pz = z + 2.6 + Math.floor(k / 6) * 1.5;
          K.B(0.62, 0.45, 0.1, "#0b1220", px, 0.95, pz, { ghost, emis: 0.35 }); K.B(0.3, 0.4, 0.3, "#5d6f94", px, 0.2, pz, { ghost });
          E.cable([x + (k % 6 - 2.5) * 0.3, 0.3, z + 0.5], [px, 0.3, pz], ghost ? "#6fb3ff" : "#8fa3c7", 0.02, { parent: d, ghost });
        }
        const f = flag(W.th, W, r);
        if (f === "gt") {
          K.B(2.6, 0.4, 1.1, "#f2a03d", x + 3.1, 0.25, z); E.cable([x + 1.3, 0.3, z], [x + 1.8, 0.3, z], "#f2a03d", 0.05, { parent: d });
        }
        K.L(sw, `<b>${esc(r.name)}</b><br>${r.qty === undefined ? "?" : fmt(r.qty)} devices${r.rate !== undefined ? " · " + fmt(r.rate) + " Mbps each" : ""}` + (f === "gt" ? `<br><span class="bad">ADD SWITCH (over ${W.level} ports)</span>` : f ? `<br><span class="good">1 switch is enough</span>` : ""), ghost ? "ghost" : f === "gt" ? "warn" : "info", i % 2 ? 0.7 : 2.3);
        if (!ghost && !W.err) {
          const cnt = Math.min(3, 1 + Math.floor(((r.qty || 0) * (r.rate || 1)) / 90));
          for (let q = 0; q < cnt; q++) E.mover(K.S(0.16, "#ffd479", x, 0.6, z, { emis: 0.9 }), [[x, 0.6, z], [NET.router[0], 1.1, NET.router[2]], [NET.server[0], 1.1, NET.server[2]]], 3.2, { loop: true, delay: q * 1.4 + i * 0.5, owner: d });
        }
      });
    },
    onOutput(E, W, line) {
      const go = [NET.console, NET.router, NET.server], back = [...go].reverse();
      fx(E, "sphere", "#5bffb0", go, 7, { onDone: () => { bubble(E, [NET.server[0], 3.2, NET.server[2]], `Reply from server:<br><b>${esc(String(line).slice(0, 60))}</b>`, "ok"); fx(E, "sphere", "#ffd479", back, 7); } });
    },
  };

  // ---------------------------------------------------------------- retail: corner shop
  S.retail = {
    bg: ["#2a2118", "#4a3a28"], home: { yaw: 0.25, pitch: 0.5, dist: 27, target: [0, 1.5, 0] },
    setup(E, th) {
      fill(E, [0.16, 0.13, 0.1]); E.plane(60, 44, "#cdb98f", { grid: 2 });
      E.box(36, 7, 0.4, "#efe6d2", { pos: [0, 3.5, -9] });
      E.box(6.5, 1.1, 1.8, "#8a5a33", { pos: [0, 0.55, 6] }); E.box(1.1, 0.7, 0.9, "#2b3a55", { pos: [-1.8, 1.45, 6], emis: 0.1 });
      E.label(E.stat.children[E.stat.children.length - 1], (th && th.world_text && th.world_text.counter) || "Till", { cls: "dev", dy: 0.7 });
      E.box(2.6, 2.2, 1.6, "#eef6fb", { pos: [15, 1.1, -4] }); E.box(2.4, 0.1, 1.4, "#8fd9ff", { pos: [15, 2.25, -4], alpha: 0.55 });
    },
    actions: [{ label: "Customer arrives", fn: (E, W) => S.retail.onOutput(E, W, "customer") }],
    render(E, W, d) {
      const K = kit(E, d), xs = [-10, -3.4, 3.4, 10];
      sign(E, K, W, 0, 6.2, -8.6, 10, "#3a2b1c");
      W.records.forEach((r, i) => shelfUnit(E, K, W, i, xs[i], -5.5, { itemColor: (k) => PAL[k], frame: "#6b4a2b", board: "#8a6a45", unit: tx(W, "unit", W.th.qty_unit || "in stock"), lowFlag: "le", lowText: tx(W, "low", "REORDER"), okText: tx(W, "ok", "well stocked") }));
      probe(E, K, W, 12.5, -2, "freezer probe: not built yet");
      if (W.stage > 0) { const cu = K.C(0.35, 1.3, "#e57373", -6, 0.8, 9), hd = K.S(0.3, "#f3d6b6", -6, 1.7, 9); E.mover(cu, [[-6, 0.8, 9], [-1.8, 0.8, 8], [-1.8, 0.8, 8]], 1.6, { loop: true, owner: d }); E.mover(hd, [[-6, 1.7, 9], [-1.8, 1.7, 8], [-1.8, 1.7, 8]], 1.6, { loop: true, owner: d }); }
    },
    onOutput(E, W, line) {
      const p = [[-8, 0.8, 9], [-2.4, 0.8, 7.2]];
      fx(E, "box", "#f2b01e", [[-3.4, 2.4, -5.5], [-3.4, 4.2, 0], [-1.6, 1.6, 6]], 7, { onDone: () => bubble(E, [-1.6, 2.6, 6], `Sold!<br><b>${esc(String(line).slice(0, 50))}</b>`, "ok") });
    },
  };

  // ---------------------------------------------------------------- pharmacy: dispensary
  S.pharmacy = {
    bg: ["#0f2a2a", "#17403d"], home: { yaw: 0.3, pitch: 0.5, dist: 27, target: [0, 1.5, 0] },
    setup(E, th) {
      fill(E, [0.08, 0.17, 0.17]); E.plane(60, 44, "#dfece8", { grid: 2 });
      E.box(36, 7, 0.4, "#f4fbf8", { pos: [0, 3.5, -9] });
      E.box(0.7, 2.4, 0.2, "#1fb872", { pos: [-15, 4.6, -8.7], emis: 0.6 }); E.box(2.4, 0.7, 0.2, "#1fb872", { pos: [-15, 4.6, -8.7], emis: 0.6 });
      E.box(8, 1.1, 1.8, "#cfd9d6", { pos: [0, 0.55, 6] });
      E.label(E.stat.children[E.stat.children.length - 1], (th && th.world_text && th.world_text.counter) || "Dispensing counter", { cls: "dev", dy: 0.7 });
      E.box(2.4, 3, 1.5, "#bfeaf5", { pos: [15, 1.5, -4], alpha: 0.7, emis: 0.2 });
    },
    actions: [{ label: "Dispense a pack", fn: (E, W) => S.pharmacy.onOutput(E, W, "dispensed") }],
    render(E, W, d) {
      const K = kit(E, d), xs = [-10, -3.4, 3.4, 10];
      sign(E, K, W, 0, 6.2, -8.6, 10, "#123b36");
      W.records.forEach((r, i) => shelfUnit(E, K, W, i, xs[i], -5.5, { itemColor: () => "#f5fbf9", frame: "#a9bdb8", board: "#c9d6d2", unit: tx(W, "unit", "packs"), lowFlag: "le", lowText: tx(W, "low", "REORDER NOW"), okText: tx(W, "ok", "stocked") }));
      probe(E, K, W, 12.5, -2, "vaccine freezer probe: not built yet");
      if (W.stage > 0) { K.C(0.4, 1.4, "#ffffff", 0, 1.8, 7.6); K.S(0.32, "#f3d6b6", 0, 2.7, 7.6); }
    },
    onOutput(E, W, line) {
      fx(E, "box", "#1fb872", [[-10, 2.0, -5.5], [-6, 4.4, 0], [0, 1.6, 6]], 7, { onDone: () => bubble(E, [0, 3.2, 6], `Dispensed<br><b>${esc(String(line).slice(0, 50))}</b>`, "ok") });
    },
  };

  // ---------------------------------------------------------------- logistics: freight yard
  const truck = (K, x, z, ghost, col) => {
    const cab = K.B(2.6, 2.2, 2.0, col, x - 3.4, 1.4, z, { ghost }); K.B(0.2, 1.0, 1.6, "#bfe1ff", x - 4.75, 1.8, z, { ghost, emis: 0.2 }); K.B(5.6, 2.8, 2.2, "#e9eef7", x + 0.4, 1.7, z, { ghost });
    [-4, -1.2, 1.6, 2.6].forEach((wx) => { K.C(0.55, 0.4, "#1a1a1a", x + wx, 0.55, z - 1.1, { ghost, rot: [Math.PI / 2, 0, 0] }); K.C(0.55, 0.4, "#1a1a1a", x + wx, 0.55, z + 1.1, { ghost, rot: [Math.PI / 2, 0, 0] }); });
    return cab;
  };
  S.logistics = {
    bg: ["#16202e", "#2a3a4f"], home: { yaw: 0.4, pitch: 0.55, dist: 30, target: [0, 1, 0] },
    setup(E) {
      fill(E, [0.1, 0.14, 0.2]); E.plane(70, 50, "#3b4452", { grid: 3 });
      E.box(34, 6, 5, "#8b97aa", { pos: [0, 3, -12] }); [-11, -4, 4, 11].forEach((x) => E.box(4.6, 4.4, 0.2, "#cdd6e3", { pos: [x, 2.2, -9.4] }));
      E.plane(70, 5, "#2a313c", { pos: [0, 0.02, 11] });
    },
    actions: [{ label: "Load a truck", fn: (E, W) => S.logistics.onOutput(E, W, "loaded") }],
    render(E, W, d) {
      const K = kit(E, d), xs = [-12, -4, 4, 12];
      sign(E, K, W, 0, 7.2, -9.4, 10, "#101a2a");
      W.records.forEach((r, i) => {
        const x = xs[i], ghost = !r.real, f = flag(W.th, W, r), stack = Math.min(Math.ceil((r.qty || 0) / 6), 7);
        for (let k = 0; k < stack; k++) K.B(1.5, 0.9, 1.5, PAL[i], x + (k % 2) * 1.6 - 0.8, 0.45 + Math.floor(k / 2) * 0.95, -6, { ghost });
        const tz = 2.5;
        truck(K, x + 0.6, tz, ghost || f === "le", f === "gt" ? "#2fb67c" : "#d99a29").info = rinfo(W, r);
        if (!ghost && f === "gt") K.S(0.25, "#2fb67c", x - 3.0, 2.9, tz, { emis: 0.9 });
        if (!ghost && f === "le") K.S(0.25, "#f2a03d", x - 3.0, 2.9, tz, { emis: 0.9 });
        K.L(K.B(0.01, 0.01, 0.01, "#000", x, 3.6, tz, { alpha: 0 }), `<b>${esc(r.name)}</b><br>${r.qty === undefined ? "?" : fmt(r.qty)} tonnes${r.rate !== undefined ? " · " + esc(W.th.rp) + fmt(r.rate) + " per tonne" : ""}` + (f === "gt" ? `<br><span class="good">GO: ready to ship</span>` : f === "le" ? `<br><span class="bad">HOLD: under minimum load</span>` : ""), ghost ? "ghost" : f === "le" ? "warn" : "info", i % 2 ? 1.7 : 0.2);
      });
      probe(E, K, W, 0, 7.5, "reefer GPS probe: not built yet");
    },
    onOutput(E, W, line) {
      fx(E, "box", "#f2b01e", [[-4, 0.9, -6], [-4, 3.2, -1.5], [-1, 2.4, 2.5]], 6, { onDone: () => bubble(E, [-1, 4, 2.5], `Loaded<br><b>${esc(String(line).slice(0, 50))}</b>`, "ok") });
    },
  };

  // ---------------------------------------------------------------- farm: harvest planner
  S.farm = {
    bg: ["#16314a", "#3a7a6a"], home: { yaw: 0.45, pitch: 0.7, dist: 29, target: [0, 0, 0] },
    setup(E) {
      fill(E, [0.35, 0.55, 0.65]); E.plane(80, 60, "#6aa84f", { grid: 4 });
      E.box(6, 3.4, 4, "#b5483a", { pos: [-14, 1.7, -11] }); E.cone(4.6, 2.2, "#7a2f27", { pos: [-14, 4.5, -11], rot: [0, Math.PI / 4, 0] });
      E.sphere(1.6, "#ffe27a", { pos: [18, 14, -20], emis: 0.9 });
    },
    actions: [{ label: "Send harvest crew", fn: (E, W) => S.farm.onOutput(E, W, "harvest") }],
    render(E, W, d) {
      const K = kit(E, d), cells = [[-7, -2], [7, -2], [-7, 8], [7, 8]], crops = ["#e5c64d", "#7ec46a", "#b98a4e", "#d1a064"];
      sign(E, K, W, -14, 6.6, -11, 8, "#2a1410");
      W.records.forEach((r, i) => {
        const [cx, cz] = cells[i], ghost = !r.real, ha = r.qty || 0, w = Math.max(3, Math.min(Math.sqrt(ha) * 1.9, 11)), f = flag(W.th, W, r);
        K.B(w, 0.12, w * 0.8, "#8c6d46", cx, 0.07, cz, { ghost }).info = rinfo(W, r);
        for (let k = 0; k < 6; k++) K.B(w * 0.92, 0.35, 0.28, ghost ? "#6fb3ff" : crops[i], cx, 0.3, cz - w * 0.32 + k * (w * 0.128), { ghost });
        const piles = Math.min(Math.round(((r.qty || 0) * (r.rate || 0)) / 12), 6);
        for (let k = 0; k < piles; k++) K.K(0.55, 0.9, "#e8c75a", cx - w / 2 + 0.7 + k * 0.7, 0.55, cz + w * 0.5, { ghost });
        K.L(K.B(0.01, 0.01, 0.01, "#000", cx, 0.4, cz, { alpha: 0 }), `<b>${esc(r.name)}</b><br>${r.qty === undefined ? "?" : fmt(r.qty)} ha${r.rate !== undefined ? " · " + fmt(r.rate) + " t/ha" : ""}` + (f === "gt" ? `<br><span class="good">SEND CREW</span>` : f === "le" ? `<br><span class="bad">BY HAND</span>` : ""), ghost ? "ghost" : "info", 1.6);
        if (!ghost && f === "gt") { const m = K.B(1.6, 1.1, 1.2, "#2f8f46", cx, 0.9, cz); K.B(0.2, 0.9, 2.4, "#cfd6dd", cx + 0.9, 0.9, cz); E.mover(m, [[cx - w / 2 + 1, 0.9, cz - w * 0.3], [cx + w / 2 - 1, 0.9, cz - w * 0.3], [cx + w / 2 - 1, 0.9, cz + w * 0.3], [cx - w / 2 + 1, 0.9, cz + w * 0.3]], 1.6, { loop: true, owner: d }); m.visible = true; }
        if (!ghost && f === "le") for (let k = 0; k < 2; k++) { K.C(0.25, 0.9, "#c0392b", cx - 1 + k, 0.55, cz); K.S(0.22, "#f3d6b6", cx - 1 + k, 1.2, cz); }
      });
      probe(E, K, W, 0, -10, "frost probe: not built yet");
    },
    onOutput(E, W, line) {
      fx(E, "sphere", "#ffe27a", [[-7, 1, -2], [-7, 4, 3], [-14, 3, -9]], 7, { onDone: () => bubble(E, [-14, 8, -11], `Barn updated<br><b>${esc(String(line).slice(0, 50))}</b>`, "ok") });
    },
  };

  // ---------------------------------------------------------------- support desk
  S.support = {
    bg: ["#1b2236", "#2d3556"], home: { yaw: 0.2, pitch: 0.6, dist: 27, target: [0, 1, 0] },
    setup(E) {
      fill(E, [0.11, 0.13, 0.21]); E.plane(60, 44, "#26304d", { grid: 2 });
      E.box(32, 5, 0.3, "#34406a", { pos: [0, 2.5, -10] });
    },
    actions: [{ label: "New ticket", fn: (E, W) => S.support.onOutput(E, W, "ticket") }],
    render(E, W, d) {
      const K = kit(E, d), xs = [-10.5, -3.5, 3.5, 10.5];
      sign(E, K, W, 0, 6.2, -9.7, 10, "#16203a");
      W.records.forEach((r, i) => {
        const x = xs[i], ghost = !r.real, f = flag(W.th, W, r), n = Math.min(Math.round(r.qty || 0), 16);
        for (let k = 0; k < n; k++) K.B(1.7, 0.08, 1.05, PAL[i], x - 0.6, 0.12 + (k % 4) * 0.1, 5.5 - Math.floor(k / 4) * 1.15, { ghost, rot: [0, ((k * 37) % 9 - 4) * 0.02, 0] });
        const agents = Math.max(1, Math.min(3, Math.ceil((r.qty || 0) / (W.hasLevel ? W.level : 10))));
        for (let a = 0; a < agents; a++) { const ax = x + 1.9 + a * 1.2 - (agents - 1) * 0.6; K.B(1.1, 0.8, 0.7, "#516089", ax, 0.4, -3.4, { ghost }); K.C(0.32, 1.2, "#7aa7ff", ax, 1.4, -4.1, { ghost }); K.S(0.28, "#f3d6b6", ax, 2.25, -4.1, { ghost }); }
        const bar = Math.min(((r.qty || 0) * (r.rate || 0)) / 40, 6);
        K.B(0.8, bar + 0.1, 0.8, f === "gt" ? "#f2a03d" : "#2fb67c", x - 2.6, (bar + 0.1) / 2, -0.5, { ghost, emis: 0.2 }).info = rinfo(W, r);
        K.L(K.B(0.01, 0.01, 0.01, "#000", x, 0.4, 7.8, { alpha: 0 }), `<b>${esc(r.name)}</b><br>${r.qty === undefined ? "?" : fmt(r.qty)} ${tx(W, "unit", "tickets")}${r.rate !== undefined ? " · " + fmt(r.rate) + " " + tx(W, "rate", "min each") : ""}` + (f === "gt" ? `<br><span class="bad">${esc(tx(W, "low", "ADD AGENT"))}</span>` : f ? `<br><span class="good">${esc(tx(W, "ok", "one agent is enough"))}</span>` : ""), ghost ? "ghost" : f === "gt" ? "warn" : "info", i % 2 ? 1.7 : 0.2);
        if (!ghost) E.mover(K.B(1.0, 0.1, 0.65, "#ffffff", x, 0.9, 5, { emis: 0.5 }), [[x - 0.6, 0.6, 3], [x + 1.9, 1.1, -3]], 2.2, { loop: true, delay: i * 0.6, owner: d });
      });
      probe(E, K, W, 0, -7.5, "SLA monitor: not built yet");
    },
    onOutput(E, W, line) {
      fx(E, "box", "#2fb67c", [[-3.5, 0.9, 5], [-2, 2.6, 0], [-1.6, 1.2, -3.6]], 6, { onDone: () => bubble(E, [-1.6, 3.4, -4], `Resolved<br><b>${esc(String(line).slice(0, 50))}</b>`, "ok") });
    },
  };

  // ---------------------------------------------------------------- applied AI: data centre
  S.ai = {
    bg: ["#0a0f1e", "#1a1440"], home: { yaw: 0.3, pitch: 0.5, dist: 28, target: [0, 2, 0] },
    setup(E) {
      fill(E, [0.04, 0.05, 0.12]); E.plane(70, 50, "#101a2f", { grid: 2 });
      E.sphere(1.9, "#8e8cff", { pos: [0, 4, -8], emis: 0.5 }); E.sphere(2.6, "#8e8cff", { pos: [0, 4, -8], alpha: 0.18 });
      E.label(E.stat.children[E.stat.children.length - 2], "Model", { cls: "dev", dy: 2.8 });
    },
    actions: [{ label: "Run an experiment", fn: (E, W) => S.ai.onOutput(E, W, "experiment") }],
    render(E, W, d) {
      const K = kit(E, d), xs = [-10.5, -3.5, 3.5, 10.5];
      sign(E, K, W, 0, 9.2, -8, 10, "#0b1226");
      W.records.forEach((r, i) => {
        const x = xs[i], ghost = !r.real, f = flag(W.th, W, r), n = Math.min(Math.round((r.qty || 0) / 6) + (r.qty ? 1 : 0), 8);
        K.B(2.6, 5, 1.6, "#1b2540", x, 2.5, 1, { ghost }).info = rinfo(W, r);
        for (let k = 0; k < 8; k++) { const on = k < n; for (let c = 0; c < 4; c++) { const led = K.B(0.3, 0.2, 0.05, !on ? "#26324d" : f === "le" ? "#ff6b5e" : "#2fb67c", x - 0.9 + c * 0.6, 0.6 + k * 0.55, 1.83, { ghost, emis: on && !ghost ? 0.9 : 0 }); if (on && !ghost) K.A((t) => { led.emis = 0.5 + 0.5 * Math.abs(Math.sin(t * (2 + c) + k)); return false; }); } }
        E.cable([x, 5, 1], [0, 4, -8], ghost ? "#6fb3ff" : "#8e8cff", 0.04, { parent: d, ghost, emis: 0.4 });
        K.L(K.B(0.01, 0.01, 0.01, "#000", x, 5.2, 1, { alpha: 0 }), `<b>${esc(r.name)}</b><br>${r.qty === undefined ? "?" : fmt(r.qty)} left${r.rate !== undefined ? " · " + esc(W.th.rp) + fmt(r.rate) + " each" : ""}` + (f === "le" ? `<br><span class="bad">TOP UP</span>` : f ? `<br><span class="good">quota healthy</span>` : ""), ghost ? "ghost" : f === "le" ? "warn" : "info", i % 2 ? 1.8 : 0.3);
        if (!ghost) E.mover(K.S(0.18, "#79e0ff", x, 5, 1, { emis: 0.9 }), [[x, 5, 1], [0, 4, -8]], 3.2, { loop: true, delay: i * 0.7, owner: d });
      });
      probe(E, K, W, -15, 6, "loss probe: not built yet");
    },
    onOutput(E, W, line) {
      fx(E, "sphere", "#ffffff", [[0, 4, -8], [0, 8, -8], [0, 9.8, -8]], 6, { r: 0.35, onDone: () => bubble(E, [0, 11, -8], `Model says<br><b>${esc(String(line).slice(0, 50))}</b>`, "ok") });
    },
  };

  global.Scenes = S;
})(window);
