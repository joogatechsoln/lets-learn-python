(() => {
  const $ = (id) => document.getElementById(id);
  const S = { themes: [], lessons: [], drills: [], theme: null, completed: [], files: {}, drillsDone: [], dfiles: {},
              kind: "lesson", idx: 0, slide: 0, checks: {}, hints: {}, pred: {}, progress: {}, name: "", industry: null,
              xp: 0, streak: 0, tab: "files", query: "", open: {}, live: true, world: null, playground: "", workspace: [], reviewQ: [], reviewI: 0, reviewDue: 0, sandbox: null };
  let cm, saveTimer, busy = false, errLine = null;
  const RANKS = [[0, "Newcomer"], [100, "Apprentice"], [250, "Practitioner"], [500, "Specialist"], [900, "Polyglot"]];

  // ---- helpers -----------------------------------------------------------
  async function api(path, body) {
    const res = await fetch(path, body === undefined ? {} : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    return res.json();
  }
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const inline = (s) => esc(s).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

  function markdown(src) {
    const lines = src.split("\n");
    let html = "", i = 0;
    const special = (l) => l.startsWith("```") || /^- /.test(l);
    while (i < lines.length) {
      const line = lines[i];
      if (line.startsWith("```")) {
        const lang = line.slice(3).trim(), buf = [];
        for (i++; i < lines.length && !lines[i].startsWith("```"); i++) buf.push(lines[i]);
        i++;
        html += `<pre data-lang="${lang}"><code>${esc(buf.join("\n"))}</code></pre>`;
      } else if (/^- /.test(line)) {
        const items = [];
        for (; i < lines.length && /^- /.test(lines[i]); i++) items.push(lines[i].slice(2));
        html += "<ul>" + items.map((x) => `<li>${inline(x)}</li>`).join("") + "</ul>";
      } else if (line.trim() === "") {
        i++;
      } else {
        const buf = [];
        for (; i < lines.length && lines[i].trim() !== "" && !special(lines[i]); i++) buf.push(lines[i]);
        html += `<p>${inline(buf.join(" "))}</p>`;
      }
    }
    return html;
  }
  function highlight(root) {
    root.querySelectorAll('pre[data-lang="python"] code').forEach((el) => {
      const src = el.textContent; el.textContent = ""; CodeMirror.runMode(src, "python", el);
    });
  }

  const cur = () => (S.kind === "lesson" ? S.lessons[S.idx] : S.kind === "drill" ? S.drills[S.idx] : null);
  const isDone = (it) => (it.id[0] === "L" ? S.completed.includes(it.id) : S.drillsDone.includes(it.id));
  const unlockedUpTo = () => Math.min(S.completed.length, S.lessons.length - 1);
  const drillOpen = (d) => S.completed.includes(d.after);
const curChapter = () => { const l = S.kind === "lesson" ? S.lessons[S.idx] : S.lessons[Math.min(S.completed.length, S.lessons.length - 1)]; return l ? l.chapter_n : 1; };
  const initials = () => (S.name || "?").split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0].toUpperCase()).join("") || "?";
  const rank = (xp) => RANKS.filter((r) => xp >= r[0]).pop()[1];

  function toast(text, gain) {
    const t = $("toast");
    t.textContent = text; t.hidden = false; t.classList.toggle("gain", !!gain);
    clearTimeout(toast.t);
    toast.t = setTimeout(() => (t.hidden = true), 3400);
  }
  function confetti(n = 90) {
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const c = $("confetti"), x = c.getContext("2d");
    c.width = innerWidth; c.height = innerHeight;
    const accent = getComputedStyle(document.documentElement).getPropertyValue("--accent").trim() || "#F2B01E";
    const colors = [accent, "#ffffff", "#2FB67C", "#5BA4FF", "#E58BD9"];
    const ps = Array.from({ length: n }, () => ({ x: innerWidth / 2 + (Math.random() - 0.5) * 240, y: innerHeight * 0.35,
      vx: (Math.random() - 0.5) * 13, vy: -Math.random() * 11 - 3, r: Math.random() * 6 + 4, c: colors[(Math.random() * colors.length) | 0],
      a: Math.random() * 6, va: (Math.random() - 0.5) * 0.4 }));
    let t = 0;
    (function frame() {
      x.clearRect(0, 0, c.width, c.height);
      ps.forEach((p) => { p.vy += 0.35; p.x += p.vx; p.y += p.vy; p.a += p.va;
        x.save(); x.translate(p.x, p.y); x.rotate(p.a); x.fillStyle = p.c; x.fillRect(-p.r / 2, -p.r / 2, p.r, p.r * 0.6); x.restore(); });
      if (++t < 110) requestAnimationFrame(frame); else x.clearRect(0, 0, c.width, c.height);
    })();
  }
  function gain(reward, label) {
    if (!reward) return;
    S.xp = reward.xp; S.streak = reward.streak;
    renderChips(true);
    toast(`+${reward.gained} XP  ${label || ""}`, true);
  }

  // ---- terminal ------------------------------------------------------------
  const term = $("term");
  function termClear(withHelp) {
    term.innerHTML = withHelp ? '<p class="term-empty">Press Run to see your program\'s output here.</p>' : "";
  }
  function termAdd(cls, text, tag = "pre") {
    const empty = term.querySelector(".term-empty");
    if (empty) empty.remove();
    const el = document.createElement(tag);
    el.className = cls; el.textContent = text;
    term.appendChild(el);
    term.scrollTop = term.scrollHeight;
    return el;
  }

  // ---- reading tracebacks -----------------------------------------------------
  const EXPLAIN = {
    SyntaxError: "Python can't understand how the code is written, so it ran none of it. Check the marked line and the one above it: a missing colon, bracket or quote is the usual cause.",
    IndentationError: "The spaces at the start of a line don't line up. Lines inside an if, for, def or class must be indented by the same amount.",
    TabError: "Tabs and spaces are mixed in the indentation. Use four spaces everywhere.",
    NameError: "Python met a name it doesn't know. Usually a spelling mistake, or a variable used before it was created.",
    UnboundLocalError: "A variable inside a function is used before it was given a value there.",
    TypeError: "Two values of the wrong type were combined, or a function got the wrong kind of input. Text and numbers can't be added, for example.",
    ValueError: "The type is right but the value isn't, like int(\"abc\"). Check what is being converted or passed in.",
    KeyError: "The dictionary has no such key. Keys must match exactly, capital letters included. `.get()` avoids the crash.",
    IndexError: "A list position doesn't exist. Lists start at 0, and the last position is one less than the length.",
    AttributeError: "The object has no such attribute or method. Check the spelling, and check what kind of object you really have.",
    ZeroDivisionError: "Something was divided by zero. Check the number on the bottom of the division.",
    ModuleNotFoundError: "Python can't find that module. This course works offline with only the standard library.",
    ImportError: "The import failed. This course works offline with only the standard library.",
    FileNotFoundError: "The file isn't where the program looked for it.",
    RecursionError: "A function keeps calling itself and never stops.",
    AssertionError: "An assert check failed: something the code promised was true wasn't.",
  };
  function explain(err, file) {
    const last = err.trim().split("\n").pop();
    const m = last.match(/^([A-Za-z]+(?:Error|Exception))\b:?\s*(.*)$/);
    const type = m ? m[1] : null;
    const frames = [...err.matchAll(/File "([^"]+)", line (\d+)/g)];
    const f = frames.length ? frames[frames.length - 1] : null;
    return { type, msg: m ? m[2] : "", file: f ? f[1] : null, line: f ? Number(f[2]) : null, tip: type ? EXPLAIN[type] : null, here: !f || f[1] === file };
  }
  function clearErrLine() { if (errLine !== null) { cm.removeLineClass(errLine, "background", "err-line"); errLine = null; } }
  function showExplain(err, file) {
    const x = explain(err, file);
    if (!x.type) return;
    let html = `<b>${esc(x.type)}</b>`;
    if (x.line && x.here) html += ` on <b>line ${x.line}</b> of <code>${esc(file)}</code> (marked in the editor)`;
    else if (x.line) html += ` in <code>${esc(x.file)}</code>, line ${x.line}: an earlier lesson file. Open it and check that line`;
    html += ".<br>" + esc(x.tip || "Read the last line of the traceback: it says what went wrong.");
    html += "<br>Tip: read the traceback from the <b>bottom</b> up.";
    const el = document.createElement("div");
    el.className = "explain"; el.innerHTML = html;
    term.appendChild(el); term.scrollTop = term.scrollHeight;
    if (x.line && x.here && x.line <= cm.lineCount()) { errLine = x.line - 1; cm.addLineClass(errLine, "background", "err-line"); cm.scrollIntoView({ line: errLine, ch: 0 }, 60); }
  }

  // ---- editor ----------------------------------------------------------------
  function initEditor() {
    cm = CodeMirror($("editorHost"), {
      value: "", mode: "python", theme: "llp", lineNumbers: true, indentUnit: 4, tabSize: 4, matchBrackets: true, autoCloseBrackets: true,
      lineWrapping: false, extraKeys: {
        Tab: (c) => (c.somethingSelected() ? c.indentSelection("add") : c.replaceSelection("    ", "end")),
        "Shift-Tab": (c) => c.indentSelection("subtract"),
        "Ctrl-Enter": () => run(), "Cmd-Enter": () => run(),
      },
    });
    cm.on("change", () => {
      if (S.kind === "project") return;
      clearErrLine();
      setState("Saving...");
      clearTimeout(saveTimer);
      saveTimer = setTimeout(saveNow, 500);
      scheduleLive();
    });
  }
  function setState(text, done) {
    const el = $("fileState");
    el.textContent = text; el.className = "state" + (done ? " done" : "");
  }
  async function saveNow() {
    clearTimeout(saveTimer);
    if (S.kind === "playground") { S.playground = cm.getValue(); await api("/api/playground_save", { code: S.playground }); setState("Saved"); return; }
    const it = cur();
    if (!it) return;
    const code = cm.getValue();
    if (S.kind === "lesson") { S.files[it.id] = code; await api("/api/save", { id: it.id, code }); }
    else { S.dfiles[it.id] = code; await api("/api/drill_save", { id: it.id, code }); }
    setState(isDone(it) ? "Completed" : "Saved", isDone(it));
  }

  // ---- rendering -------------------------------------------------------------
  function renderChips(bump) {
    $("xpNum").textContent = S.xp; $("rankName").textContent = S.lessons.length && S.completed.length === S.lessons.length ? "Graduate" : rank(S.xp);
    $("streakNum").textContent = S.streak;
    if (bump) { const c = $("xpChip"); c.classList.remove("bump"); void c.offsetWidth; c.classList.add("bump"); }
  }
  function renderHeader() {
    const pct = S.lessons.length ? Math.round((S.completed.length / S.lessons.length) * 100) : 0;
    $("meterFill").style.width = pct + "%";
    $("meterPct").textContent = pct + "%";
    $("meter").setAttribute("aria-valuenow", pct);
    $("avatarText").textContent = initials();
    renderChips(false);
    const sel = $("lessonPicker");
    sel.innerHTML = "";
    let group, last = "";
    S.lessons.forEach((l, i) => {
      if (l.chapter_n !== last) {
        const done = S.lessons.filter((x) => x.chapter_n === l.chapter_n && isDone(x)).length;
        group = document.createElement("optgroup"); group.label = `Chapter ${l.chapter_n}: ${l.chapter} (${done}/${l.chapter_total})`; sel.appendChild(group); last = l.chapter_n;
      }
      const o = document.createElement("option");
      const locked = i > unlockedUpTo();
      o.value = i; o.disabled = locked;
      o.textContent = `${isDone(l) ? "✓" : locked ? "🔒" : "•"}  ${l.in_chapter}. ${l.title}`;
      group.appendChild(o);
    });
    sel.value = S.kind === "lesson" ? S.idx : "";
  }

  function renderQuiz(slide, id) {
    const box = document.createElement("div"), pred = slide.kind === "predict";
    const codeBlock = slide.code ? `<pre data-lang="python"><code>${esc(slide.code)}</code></pre>` : "";
    box.innerHTML = `<h4>${esc(slide.title)}</h4>` + (pred ? `<p class="predict-q">Read the code. What happens when it runs?</p>${codeBlock}` : `<div class="quiz-q">${markdown(slide.question)}</div>${codeBlock}`) +
      `<div class="opts"></div><div class="why" hidden></div>`;
    const opts = box.querySelector(".opts"), why = box.querySelector(".why");
    const label = (o) => (pred && o.startsWith("!") ? `It crashes with a ${o.slice(1)}` : o);
    const chosen = S.pred[id + ":" + slide.title];
    slide.options.forEach((o, i) => {
      const b = document.createElement("button");
      b.className = "opt"; b.innerHTML = `<pre>${esc(label(o))}</pre>`;
      b.onclick = () => { S.pred[id + ":" + slide.title] = i; renderSlides(); };
      if (chosen !== undefined) { b.disabled = true; if (i === slide.answer) b.classList.add("right"); else if (i === chosen) b.classList.add("wrong"); }
      opts.appendChild(b);
    });
    if (chosen !== undefined) { why.hidden = false; why.innerHTML = `<b>${chosen === slide.answer ? "Correct." : "Not quite."}</b> ${inline(slide.why)}`; }
    return box;
  }

  function renderSlides() {
    const l = cur();
    if (!l) return;
    $("lessonCount").textContent = S.kind === "drill" ? `Bug ${l.n} of ${S.drills.length}` : `Lesson ${l.in_chapter} of ${l.chapter_total}`;
    $("chapterChip").textContent = S.kind === "drill" ? `Bug Lab · ${l.error}` : `Chapter ${l.chapter_n}: ${l.chapter}`;
    $("lessonTitle").textContent = l.title + (isDone(l) ? "  ✓" : "");
    S.slide = Math.min(S.slide, l.slides.length - 1);
    const slide = l.slides[S.slide];
    const body = $("slideBody");
    body.innerHTML = "";
    if (slide.kind === "predict" || slide.kind === "quiz") {
      body.appendChild(renderQuiz(slide, l.id));
    } else {
      let html = `<h4>${esc(slide.title)}</h4>` + markdown(slide.body);
      if (S.slide === l.slides.length - 1) {
        const res = S.checks[l.id] || [];
        html += '<ul class="reqs">' + l.checks.map((c, i) => {
          const state = isDone(l) && !res.length ? "ok" : res[i] ? (res[i].ok ? "ok" : "bad") : "idle";
          const mark = state === "ok" ? "✓" : state === "bad" ? "✗" : "";
          return `<li data-s="${state}"><span class="mark">${mark}</span><span>${esc(c.label)}</span></li>`;
        }).join("") + "</ul>";
      }
      body.innerHTML = html;
    }
    highlight(body);
    body.scrollTop = 0;
    $("prevSlide").disabled = S.slide === 0;
    $("nextSlide").disabled = S.slide === l.slides.length - 1;
    const dots = $("dots");
    dots.innerHTML = "";
    l.slides.forEach((s, i) => {
      const b = document.createElement("button");
      b.className = "dot"; b.setAttribute("aria-label", `Slide ${i + 1}: ${s.title}`);
      if (i === S.slide) b.setAttribute("aria-current", "true");
      b.onclick = () => { S.slide = i; renderSlides(); };
      dots.appendChild(b);
    });
    const hasNext = S.kind === "lesson" ? S.idx < S.lessons.length - 1 : S.idx < S.drills.length - 1 && drillOpen(S.drills[S.idx + 1]);
    $("nextLesson").textContent = S.kind === "drill" ? "Next bug" : "Next lesson";
    $("nextLesson").hidden = !(isDone(l) && hasNext);
  }

  const ICON = {
    doc: '<svg viewBox="0 0 16 16" width="14" height="14"><path d="M3 2.5h7l3 3v8h-10z M10 2.5v3h3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>',
    done: '<svg viewBox="0 0 16 16" width="15" height="15"><path d="m3 8.5 3.2 3L13 4.5" fill="none" stroke="#2FB67C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    lock: '<svg viewBox="0 0 16 16" width="14" height="14"><path d="M4.5 7V5a3.5 3.5 0 0 1 7 0v2M3.5 7h9v6.5h-9z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>',
    open: '<svg viewBox="0 0 16 16" width="14" height="14"><circle cx="8" cy="8" r="4" fill="var(--accent)"/></svg>',
  };
  function fileButton(ul, { html, ico, tag, disabled, current, cls, onclick }) {
    const li = document.createElement("li"), b = document.createElement("button");
    b.className = "file " + (cls || ""); b.disabled = !!disabled;
    if (current) b.setAttribute("aria-current", "true");
    b.innerHTML = `<span class="ico">${ico}</span><span>${html}</span>${tag ? `<span class="tag">${tag}</span>` : ""}`;
    b.onclick = onclick;
    li.appendChild(b); ul.appendChild(li);
  }
  function renderFiles() {
    const ul = $("fileList");
    ul.innerHTML = "";
    fileButton(ul, { html: "project.py", ico: ICON.doc, tag: "your whole program", cls: "project", disabled: S.completed.length === 0, current: S.kind === "project", onclick: openProject });
    const playOpen = S.completed.length >= 12;
    fileButton(ul, { html: "playground.py", ico: ICON.doc, tag: playOpen ? "free coding" : "opens after chapter 1", cls: "project", disabled: !playOpen, current: S.kind === "playground", onclick: openPlayground });
    let ch = 0;
    S.lessons.forEach((l, i) => {
      if (l.chapter_n !== ch) {
        ch = l.chapter_n;
        const mine = S.lessons.filter((x) => x.chapter_n === ch), done = mine.filter(isDone).length, n = ch;
        const open = S.open[n] ?? n === curChapter();
        const li = document.createElement("li"); li.className = "chap";
        li.innerHTML = `<button class="chap-btn" aria-expanded="${open}"><span class="chev">▸</span><span>${n}. ${esc(l.chapter)}</span><span class="cnt">${done}/${mine.length}</span><span class="bar2"><i style="width:${(done / mine.length) * 100}%"></i></span></button>`;
        li.firstChild.onclick = () => { S.open[n] = !open; renderFiles(); };
        ul.appendChild(li);
      }
      if (!(S.open[l.chapter_n] ?? l.chapter_n === curChapter())) return;
      const locked = i > unlockedUpTo();
      fileButton(ul, { html: l.file, ico: isDone(l) ? ICON.done : locked ? ICON.lock : ICON.open, disabled: locked, current: S.kind === "lesson" && i === S.idx, onclick: () => selectItem("lesson", i) });
    });
    const bl = $("bugList");
    bl.innerHTML = "";
    const anyOpen = S.drills.some(drillOpen);
    const intro = document.createElement("li");
    intro.innerHTML = `<p class="empty" style="padding:10px 12px">${anyOpen ? "Short drills: read the error, find the bug, fix it. New ones unlock as you learn." : "The <b>Bug Lab</b> opens when you finish the lesson on reading a traceback."}</p>`;
    bl.appendChild(intro);
    S.drills.forEach((d, i) => {
      const open = drillOpen(d);
      fileButton(bl, { html: d.file, ico: isDone(d) ? ICON.done : open ? "🐞" : ICON.lock, tag: d.error === "Wrong answer" ? "silent bug" : d.error, cls: "bug", disabled: !open,
        current: S.kind === "drill" && i === S.idx, onclick: () => selectItem("drill", i) });
    });
  }

  function renderGuide() {
    const g = $("guide"), t = S.theme;
    if (!t) { g.innerHTML = ""; return; }
    const q = S.query.toLowerCase();
    const terms = t.glossary.filter((x) => !q || (x[0] + " " + x[1]).toLowerCase().includes(q));
    const l = cur(), canCompare = S.kind === "lesson" && l && isDone(l);
    g.innerHTML = `<h4>Words of the ${esc(t.label)} trade</h4><input type="search" id="gq" placeholder="Find a word" value="${esc(S.query)}" aria-label="Find a word">
      <dl>${terms.map((x) => `<div class="term"><dt>${esc(x[0])}</dt><dd>${esc(x[1])}${x[2] ? ` <code>${esc(x[2])}</code>` : ""}</dd></div>`).join("") || '<p class="empty">No match.</p>'}</dl>
      <button class="btn ghost" id="cmpBtn" ${canCompare ? "" : "disabled"}>${canCompare ? "See this lesson in other industries" : "Finish this lesson to compare industries"}</button>`;
    const gq = $("gq");
    gq.oninput = () => { S.query = gq.value; const pos = gq.selectionStart; renderGuide(); const n = $("gq"); n.focus(); n.setSelectionRange(pos, pos); };
    $("cmpBtn").onclick = openCompare;
  }
  function showTab(name) {
    S.tab = name;
    document.querySelectorAll(".tabs button").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.tab === name)));
    $("fileList").hidden = name !== "files"; $("bugList").hidden = name !== "bugs"; $("guide").hidden = name !== "guide";
    $("review").hidden = name !== "review"; $("space").hidden = name !== "space";
    if (name === "guide") renderGuide();
    if (name === "review") loadReview();
    if (name === "space") loadWorkspace();
  }

  function codeStats() {
    const code = S.lessons.filter((l) => S.completed.includes(l.id)).map((l) => S.files[l.id] || "").join("\n");
    const lines = code.split("\n").filter((x) => x.trim() && !x.trim().startsWith("#")).length;
    return { lines, funcs: (code.match(/^\s*def /gm) || []).length, classes: (code.match(/^class /gm) || []).length };
  }
  // ---- 3D live preview -----------------------------------------------------------
  let E3 = null, scene = null, sceneKey = null, lastLines = 0, liveTimer = null, previewSeq = 0;
  async function detectThree() {
    S.useThree = false;
    try {
      const info = await api("/api/engine");
      if (!info.three) { S.engineNote = info.bytes ? "three.min.js is too small to be a real build, so the built-in 3D engine is used" : "built-in 3D engine"; return; }
      await new Promise((ok, bad) => { const sc = document.createElement("script"); sc.src = "/vendor/three.min.js"; sc.onload = ok; sc.onerror = bad; document.head.appendChild(sc); });
      S.useThree = !!(window.THREE && window.THREE.WebGLRenderer && window.Three3D);
      if (!S.useThree) S.engineNote = "three.min.js loaded but did not define THREE, so the built-in 3D engine is used";
    } catch (e) { S.engineNote = "three.js could not be loaded, so the built-in 3D engine is used"; }
    if (S.engineNote) console.info("[3D]", S.engineNote);
  }
  function onEngineFail(err) {
    console.warn("[3D] three.js failed, falling back to the built-in engine:", err);
    S.useThree = false; S.engineNote = "three.js failed, so the built-in 3D engine is used";
    const old = $("scene3d"), fresh = old.cloneNode(false);
    old.replaceWith(fresh); E3 = null; sceneKey = null;
    loadScene(); updatePreview(false);
  }
  function initScene() {
    if (E3) return true;
    const canvas = $("scene3d"), labels = $("labels");
    E3 = (S.useThree && window.Three3D && Three3D.create(canvas, labels, onEngineFail)) || (window.Mini3D && Mini3D.create(canvas, labels));
    if (!E3) { $("sceneWrap").classList.add("nogl"); return false; }
    E3.engine = E3.engine || "built-in engine";
    E3.onPick = (node) => showInspector(node.info);
    E3.dyn = E3.group({ parent: E3.root });
    E3.clearAll = () => { [E3.stat, E3.fx, E3.dyn].forEach((g) => (g.children = [])); E3.ticks = []; E3.labels.forEach((L) => L.el.remove()); E3.labels = []; };
    new ResizeObserver(() => E3 && E3.resize()).observe($("sceneWrap"));
    return true;
  }
  function loadScene() {
    if (!S.theme || !initScene() || sceneKey === S.industry) return;
    sceneKey = S.industry; scene = Scenes[S.industry] || Scenes[S.theme.world] || Scenes.retail; lastLines = 0;
    $("sceneWrap").style.background = `linear-gradient(180deg, ${scene.bg[0]}, ${scene.bg[1]})`;
    E3.clearAll(); scene.setup(E3, S.theme); E3.setHome(scene.home);
    const a = scene.actions && scene.actions[0];
    $("pvAction").hidden = !a; if (a) $("pvAction").textContent = "▶ " + a.label;
  }
  function deriveWorld(r) {
    const th = S.theme, v = th.v, snap = (r && r.snapshot) || { vars: {}, functions: [], classes: [] }, vars = snap.vars || {};
    const isMap = (x) => x && typeof x === "object" && !Array.isArray(x) && !x.__class__;
    const dq = vars[v.qtys], dr = vars[v.rates];
    let real = [];
    if (isMap(dq)) real = Object.keys(dq).map((n) => ({ name: n, qty: dq[n], rate: isMap(dr) ? dr[n] : undefined }));
    else if (Array.isArray(vars[v.names])) real = vars[v.names].map((n) => ({ name: n }));
    else if (vars[v.name] !== undefined) real = [{ name: vars[v.name], qty: vars[v.qty], rate: vars[v.rate] }];
    const records = th.records.map(([n, q, p]) => {
      const m = real.find((x) => x.name === n);
      return m ? { name: n, qty: m.qty !== undefined ? m.qty : q, rate: m.rate !== undefined ? m.rate : p, real: true } : { name: n, qty: q, rate: p, real: false };
    });
    const lines = ((r && r.stdout) || "").split("\n").filter((x) => x.trim());
    let banner = lines.find((x) => x.startsWith("Welcome to")) || lines.find((x) => x.includes(th.biz)) || null;
    if (banner) S.lastBanner = banner; else if (S.kind === "playground") banner = S.lastBanner || null;
    const sensor = vars.sensor_name !== undefined ? { name: vars.sensor_name, reading: vars.reading !== undefined ? vars.reading : "?", unit: vars.unit || vars.reading_unit || th.probe.unit,
      alert: typeof vars.last_alert === "string" && vars.last_alert.length > 0 } : null;
    const level = typeof vars[v.level] === "number" ? vars[v.level] : null;
    return { th, records, level, hasLevel: level !== null, banner, lines, err: !!(r && r.error), sensor, stage: S.completed.length, funcs: snap.functions.length, classes: snap.classes, vars };
  }
  function applyWorld(r, announce) {
    if (!E3 || !scene) return;
    const W = deriveWorld(r);
    S.world = W;
    E3.clear(E3.dyn);
    try { scene.render(E3, W, E3.dyn); } catch (e) { console.error("scene render failed", e); }
    const built = W.records.filter((x) => x.real).length;
    $("hud").textContent = `${built}/${W.records.length} ${S.theme.things} built · ${W.lines.length} output lines${W.funcs ? ` · ${W.funcs} function${W.funcs > 1 ? "s" : ""}` : ""}${W.err ? " · error" : ""} · ${E3.engine}`;
    if (announce && W.lines.length > lastLines && !W.err) scene.onOutput(E3, W, W.lines[W.lines.length - 1]);
    lastLines = W.lines.length;
  }
  function renderOutput(r) {
    const el = $("previewBody");
    if (!r) { el.innerHTML = `<p class="empty">Press Build, or run a lesson, to see the whole program's output here.</p>`; return; }
    let html = r.stdout ? `<pre>${esc(r.stdout)}</pre>` : "";
    if (r.error) html += `<pre class="err">${esc(r.error)}</pre>`;
    el.innerHTML = html || '<p class="empty">The project ran but printed nothing yet.</p>';
  }
  async function updatePreview(announce) {
    if (!S.lessons.length || !S.theme) return;
    const it = cur(), seq = ++previewSeq, editing = S.kind === "lesson" && it;
    const r = await api("/api/preview", { id: editing ? it.id : null, code: editing ? cm.getValue() : "", stdin: $("stdin").value });
    if (seq !== previewSeq || r.error && !r.snapshot) return;
    renderOutput(r); applyWorld(r, announce); renderPreviewShell();
  }
  function scheduleLive() { if (S.live && S.kind !== "playground") { clearTimeout(liveTimer); liveTimer = setTimeout(() => updatePreview(false), 900); } }
  function showPv(name) {
    document.querySelectorAll(".pv-tabs button").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.pv === name)));
    $("sceneWrap").hidden = name !== "3d"; $("previewBody").hidden = name === "3d";
  }
  function renderPreviewShell() {
    $("projName").textContent = S.theme ? S.theme.system : "Your project";
    $("projBiz").textContent = S.theme ? `Built for ${S.theme.biz}` : "";
    const here = curChapter(), mine = S.lessons.filter((l) => l.chapter_n === here);
    $("modules").innerHTML = mine.map((l) => `<span class="tile${isDone(l) ? " on" : ""}" title="${esc(l.chapter_n + "." + l.in_chapter + " " + l.module)}">${l.emoji}</span>`).join("");
    const next = S.lessons.find((l) => !isDone(l));
    $("nextMod").textContent = next ? `Chapter ${here}: ${mine.filter(isDone).length}/${mine.length} · next module: ${next.module}` : "Every module is built.";
    const s = codeStats();
    $("stats").innerHTML = [`${S.completed.length}/${S.lessons.length} lessons`, `${s.lines} lines`, `${s.funcs} functions`, `${s.classes} classes`].map((x) => `<span class="stat">${x}</span>`).join("");
  }
  async function build(quiet) { showPv("3d"); await updatePreview(true); if (!quiet) toast("Project built. Watch the 3D view."); }

  function applyTheme() { if (S.theme) document.documentElement.style.setProperty("--accent", S.theme.accent); }
  function renderAll() { applyTheme(); renderHeader(); renderSlides(); renderFiles(); renderPreviewShell(); if (S.tab === "guide") renderGuide(); }

  // ---- navigation ------------------------------------------------------------
  async function selectItem(kind, i) {
    if (kind === "lesson" && i > unlockedUpTo()) return;
    if (kind === "drill" && !drillOpen(S.drills[i])) return;
    await saveNow();
    clearErrLine();
    S.kind = kind; S.idx = i; S.slide = 0;
    const it = cur();
    cm.setOption("readOnly", false);
    cm.setValue((kind === "lesson" ? S.files[it.id] : S.dfiles[it.id]) ?? it.starter);
    cm.clearHistory();
    $("fileName").textContent = it.file;
    setState(isDone(it) ? "Completed" : "", isDone(it));
    $("runBtn").disabled = false; $("hintBtn").hidden = false; $("resetBtn").hidden = false; $("buildBtn").disabled = false; $("tpl").hidden = true;
    termClear(true);
    renderAll();
    cm.refresh();
    if (!isDone(it)) cm.focus();
    updatePreview(false);
  }
  const selectLesson = (i) => selectItem("lesson", i);

  async function openProject() {
    await saveNow();
    clearErrLine();
    const { code } = await api("/api/source", {});
    S.kind = "project";
    cm.setOption("readOnly", true);
    cm.setValue(code);
    $("fileName").textContent = "project.py";
    setState("Read-only. Built from your finished lessons.");
    $("runBtn").disabled = true; $("hintBtn").hidden = true; $("resetBtn").hidden = true; $("tpl").hidden = true;
    renderFiles();
    renderHeader();
  }

  // ---- run / build / hints -----------------------------------------------------
  function setBusy(on) { $("runBtn").classList.toggle("busy", on); $("runLabel").textContent = on ? "Running" : "Run"; }

  async function run() {
    if (busy || S.kind === "project") return;
    if (S.kind === "playground") return runPlayground();
    busy = true; $("runBtn").disabled = true; setBusy(true);
    const l = cur(), drill = S.kind === "drill";
    await saveNow();
    clearErrLine();
    termClear(false);
    termAdd("cmd", `python ${l.file}`, "div");
    const res = await api(drill ? "/api/drill_run" : "/api/run", { id: l.id, code: cm.getValue(), stdin: $("stdin").value });
    busy = false; $("runBtn").disabled = false; setBusy(false);
    if (res.error && !res.checks) { termAdd("err", res.error); return; }
    if (res.stdout) termAdd("out", res.stdout.replace(/\n$/, ""));
    if (res.error) {
      termAdd("err", res.error);
      if (res.stopped) return;
      showExplain(res.error, l.file);
      S.checks[l.id] = [];
      renderSlides();
      return;
    }
    S.checks[l.id] = res.checks;
    if (drill) S.drillsDone = res.drills_done; else S.completed = res.completed;
    res.checks.forEach((c) => {
      const el = termAdd("check " + (c.ok ? "ok" : "bad"), `${c.ok ? "✓" : "✗"} ${c.label}`, "div");
      el.style.animationDelay = "0s";
      if (!c.ok && c.detail) termAdd("detail", c.detail, "div");
    });
    if (res.passed) {
      termAdd("win", res.newly_completed ? (drill ? `Bug squashed: ${l.error}.` : `Lesson complete. "${l.module}" is now part of your project.`) : "All checks pass.", "div");
      setState("Completed", true);
      renderAll();
      if (res.newly_completed) {
        confetti(drill ? 50 : 100);
        gain(res.reward, drill ? "bug squashed" : "lesson complete");
        if (!drill) {
          await updatePreview(true);
          S.progress[S.industry] = S.completed.length;
          const next = S.lessons[S.idx + 1];
          if (S.completed.length === S.lessons.length) { confetti(240); setTimeout(showDone, 900); }
          else if (S.drills.some((x) => x.after === l.id)) { const k = S.drills.filter((x) => x.after === l.id).length; setTimeout(() => toast(`Bug Lab: ${k} new drill${k > 1 ? "s" : ""} unlocked`), 1800); }
          else if (next && next.chapter_n !== l.chapter_n) { confetti(200); setTimeout(() => toast(`Chapter ${l.chapter_n} complete: ${l.chapter}`), 1800); }
        }
      }
    } else {
      renderSlides();
    }
  }

  function hint() {
    const l = cur(), n = S.hints[l.id] || 0;
    if (n < l.hints.length) {
      termAdd("hint", `Hint ${n + 1} of ${l.hints.length}: ${l.hints[n]}`, "div");
      S.hints[l.id] = n + 1;
    } else {
      termAdd("hint", "One way to write it (typing it yourself teaches more than copying):", "div");
      termAdd("out", l.solution.replace(/\n$/, ""));
    }
  }

  // ---- compare industries -----------------------------------------------------
  async function openCompare() {
    const l = cur();
    if (S.kind !== "lesson" || !l) return;
    const data = await api("/api/compare", { n: l.n });
    if (data.error) { toast(data.error); return; }
    $("cmpTitle").textContent = `Lesson ${l.n}: same idea, other industries`;
    const tabs = $("cmpTabs");
    tabs.innerHTML = "";
    const show = (it, btn) => {
      tabs.querySelectorAll("button").forEach((b) => b.setAttribute("aria-selected", String(b === btn)));
      const pre = $("cmpCode");
      pre.textContent = "";
      CodeMirror.runMode(`# ${it.system}: ${it.title}\n` + it.code, "python", pre);
    };
    data.items.forEach((it) => {
      const b = document.createElement("button");
      b.style.setProperty("--c", it.accent); b.textContent = `${it.icon} ${it.label}`; b.setAttribute("role", "tab");
      b.onclick = () => show(it, b);
      tabs.appendChild(b);
      if (it.key === data.current) setTimeout(() => show(it, b), 0);
    });
    $("compare").showModal();
  }

  // ---- setup / profile -----------------------------------------------------------
  function openSetup(editing) {
    $("setupTitle").textContent = editing ? "Your profile" : "Learn Python by building your own system";
    $("setupGo").textContent = editing ? "Save" : "Start learning";
    $("setupCancel").hidden = !editing;
    $("nameInput").value = S.name;
    const box = $("themeCards");
    box.querySelectorAll(".card").forEach((n) => n.remove());
    const total = S.lessons.length || 15;
    S.themes.forEach((t, i) => {
      const count = S.progress[t.key] || 0;
      const label = document.createElement("label");
      label.className = "card"; label.style.setProperty("--c", t.accent);
      label.innerHTML = `<input type="radio" name="industry" value="${t.key}" ${(S.industry ? S.industry === t.key : i === 0) ? "checked" : ""}>
        <span class="face"><span class="emoji">${t.icon}</span><span class="t">${esc(t.label)}</span><span class="d">${esc(t.tagline)}</span>
        <span class="b">You build: ${esc(t.system)}${count ? `  (${count} of ${total} done)` : ""}</span></span>`;
      box.appendChild(label);
    });
    $("setup").showModal();
    $("nameInput").focus();
  }

  async function applyBootstrap(data) {
    S.themes = data.themes; S.name = data.name; S.industry = data.industry; S.progress = data.progress || {};
    S.xp = data.xp || 0; S.streak = data.streak || 0; 
    S.lessons = data.lessons || []; S.drills = data.drills || [];
    S.theme = S.themes.find((t) => t.key === data.industry) || null;
    S.completed = data.track ? data.track.completed : [];
    S.files = data.track ? data.track.files : {};
    S.drillsDone = data.track ? data.track.drills || [] : [];
    S.dfiles = data.track ? data.track.drill_files || {} : {};
    S.playground = data.track ? data.track.playground || "" : ""; S.workspace = data.workspace || []; S.reviewDue = data.review_due || 0; S.sandbox = data.sandbox || null;
    setReviewBadge(); showSandbox();
    S.lastBanner = null; S.checks = {}; S.hints = {}; S.pred = {}; S.open = {};
    if (!S.lessons.length) { renderHeader(); return; }
    loadScene();
    S.kind = "none";
    await selectItem("lesson", Math.min(S.completed.length, S.lessons.length - 1));
    S.slide = 0; renderSlides();
  }

  function showDone() {
    $("doneTitle").textContent = "You've finished the Python course";
    $("doneLead").textContent = `${S.name ? S.name + ", you" : "You"} built the ${S.theme.system} for ${S.theme.biz} and completed all ${S.lessons.length} lessons. You now know:`;
    const chapters = [...new Map(S.lessons.map((l) => [l.chapter_n, `${l.chapter_n}. ${l.chapter}`])).values()];
    $("skills").innerHTML = chapters.map((c) => `<li>${esc(c)}</li>`).join("");
    $("done").showModal();
  }

  // ---- playground, workspace, review, inspector ------------------------------------------
  const TEMPLATES = {
    blank: "# Free coding. Everything you built in the lessons is available here.\n# Files you write are saved in your Workspace tab.\n",
    ask: "# Ask questions with input(). Type your answers in the Input box under the terminal,\n# one line for each input() call.\nname = input(\"Your name? \")\nunits = int(input(\"How many units? \"))\nprint(f\"Hello {name}, doubled that is {units * 2}.\")\n",
    csv: "import csv\n\n# records.csv is in your Workspace tab\nwith open(\"records.csv\", newline=\"\") as file:\n    rows = list(csv.DictReader(file))\n\ntotal = 0\nfor row in rows:\n    value = int(row[\"quantity\"]) * float(row[\"rate\"])\n    print(row[\"name\"], value)\n    total += value\nprint(\"Total:\", total)\n",
    json: "import json\n\nwith open(\"settings.json\") as file:\n    settings = json.load(file)\nprint(settings)\n\nsettings[\"level\"] = settings[\"level\"] + 5\nwith open(\"settings.json\", \"w\") as file:\n    json.dump(settings, file, indent=2)\nprint(\"saved\")\n",
    log: "with open(\"log.txt\", \"a\") as file:\n    file.write(\"report ran\\n\")\n\nwith open(\"log.txt\") as file:\n    print(file.read())\n",
    safe: "try:\n    with open(\"missing.txt\") as file:\n        print(file.read())\nexcept FileNotFoundError:\n    print(\"That file does not exist yet.\")\n",
  };
  function setReviewBadge() { const b = document.querySelector('.tabs [data-tab="review"]'); if (b) b.textContent = "Review" + (S.reviewDue ? ` (${S.reviewDue})` : ""); }
  function showSandbox() {
    const s = S.sandbox, el = $("sbx");
    if (!s) { el.textContent = ""; return; }
    el.textContent = "🛡 " + s.kind; el.title = s.note;
  }

  async function openPlayground() {
    if (S.completed.length < 12) return;
    await saveNow(); clearErrLine();
    S.kind = "playground";
    cm.setOption("readOnly", false); cm.setValue(S.playground || TEMPLATES.blank); cm.clearHistory();
    $("fileName").textContent = "playground.py"; setState("Free coding");
    $("runBtn").disabled = false; $("hintBtn").hidden = true; $("resetBtn").hidden = false; $("tpl").hidden = false; $("buildBtn").disabled = false;
    $("lessonCount").textContent = "Free coding"; $("chapterChip").textContent = "Playground"; $("lessonTitle").textContent = "The Playground";
    $("slideBody").innerHTML = markdown("The **Playground** runs your own code **after** all the lessons you have finished, so every function and variable you wrote is available.\n\n- Press **Run** to run it, and watch the 3D world react\n- `input()` works: type the answers in the **Input** box under the terminal\n- Files you open are kept in your **Workspace** tab (try the templates menu above the editor)\n- Network access and system commands are switched off\n\nBuild something of your own: a report, a checker, a small tool for your industry.");
    $("dots").innerHTML = ""; $("prevSlide").disabled = true; $("nextSlide").disabled = true; $("nextLesson").hidden = true;
    termClear(true); renderFiles(); renderHeader(); cm.refresh(); cm.focus();
  }
  async function runPlayground() {
    busy = true; $("runBtn").disabled = true; setBusy(true);
    await saveNow(); clearErrLine(); termClear(false); termAdd("cmd", "python playground.py", "div");
    const res = await api("/api/playground_run", { code: cm.getValue(), stdin: $("stdin").value });
    busy = false; $("runBtn").disabled = false; setBusy(false);
    if (res.error && !res.snapshot) { termAdd("err", res.error); return; }
    if (res.stdout) termAdd("out", res.stdout.replace(/\n$/, ""));
    if (res.error) { termAdd("err", res.error); showExplain(res.error, "playground.py"); }
    else termAdd("win", "Done.", "div");
    if (res.workspace) S.workspace = res.workspace;
    applyWorld(res, true);
  }

  async function loadWorkspace() {
    const r = await api("/api/workspace"); S.workspace = r.workspace || []; renderWorkspace();
  }
  function renderWorkspace() {
    const box = $("space");
    box.innerHTML = `<h4>Your workspace</h4><p class="empty" style="margin:0 0 8px">Files your programs can read and write with <code>open()</code>. This folder is only yours.</p>` +
      (S.workspace.map((f) => `<div class="ws-row"><b>${esc(f.name)}</b><small>${f.bytes} bytes</small><button class="link" data-view="${esc(f.name)}">View</button><button class="link" data-del="${esc(f.name)}">Delete</button></div>`).join("") || '<p class="empty">No files yet.</p>') +
      `<div class="ws-view" id="wsView" hidden></div><button class="btn ghost" id="wsReset" style="margin-top:10px;width:100%">Restore the sample files</button>`;
    box.querySelectorAll("[data-view]").forEach((b) => (b.onclick = async () => { const r = await api("/api/workspace?name=" + encodeURIComponent(b.dataset.view)); const v = $("wsView"); v.hidden = false; v.textContent = r.text === null || r.text === undefined ? "(could not read)" : r.text; }));
    box.querySelectorAll("[data-del]").forEach((b) => (b.onclick = async () => { if (!confirm(`Delete ${b.dataset.del}?`)) return; S.workspace = (await api("/api/workspace_delete", { name: b.dataset.del })).workspace; renderWorkspace(); }));
    $("wsReset").onclick = async () => { if (!confirm("Replace your workspace files with the original samples? Your own files will be deleted.")) return; S.workspace = (await api("/api/workspace_reset", {})).workspace; renderWorkspace(); };
  }

  async function loadReview() {
    const r = await api("/api/review", {}); S.reviewQ = r.questions || []; S.reviewI = 0; S.reviewDue = r.due || 0; setReviewBadge(); renderReview();
  }
  function renderReview() {
    const box = $("review"), q = S.reviewQ[S.reviewI];
    if (!S.reviewQ.length) { box.innerHTML = '<h4>Review</h4><p class="empty">Nothing to review yet. Finish some lessons, and their questions come back here after a day, then three days, then a week, just before you would forget them.</p>'; return; }
    if (!q) { box.innerHTML = '<h4>Review</h4><p>All done for now. 🎉</p><p class="empty">The questions you got right come back later, and the ones you missed come back tomorrow.</p>'; return; }
    const pred = q.kind === "predict", label = (o) => (pred && o.startsWith("!") ? `It crashes with a ${o.slice(1)}` : o);
    box.innerHTML = `<h4>Review <small style="font-weight:500;color:var(--muted)">${S.reviewI + 1} of ${S.reviewQ.length}</small></h4><div class="rv-card"><div class="rv-meta">${esc(q.chapter)} · ${esc(q.lesson)}</div>` +
      (pred ? `<p class="predict-q">What happens when this runs?</p><pre>${esc(q.code)}</pre>` : markdown(q.question) + (q.code ? `<pre>${esc(q.code)}</pre>` : "")) + '<div class="opts"></div><div class="why" hidden></div><button class="btn run" id="rvNext" hidden style="margin-top:8px">Next</button></div>';
    const opts = box.querySelector(".opts");
    q.options.forEach((o, i) => {
      const b = document.createElement("button"); b.className = "opt"; b.innerHTML = `<pre>${esc(label(o))}</pre>`;
      b.onclick = async () => {
        opts.querySelectorAll(".opt").forEach((x, k) => { x.disabled = true; if (k === q.answer) x.classList.add("right"); else if (k === i) x.classList.add("wrong"); });
        const why = box.querySelector(".why"); why.hidden = false; why.innerHTML = `<b>${i === q.answer ? "Correct." : "Not quite."}</b> ${inline(q.why)}`;
        const r = await api("/api/review", { answer: { key: q.key, correct: i === q.answer } });
        if (r.reward) gain(r.reward, "review");
        S.reviewDue = Math.max(0, S.reviewDue - 1); setReviewBadge();
        const n = $("rvNext"); n.hidden = false; n.onclick = () => { S.reviewI++; renderReview(); };
      };
      opts.appendChild(b);
    });
  }

  function showInspector(info) {
    if (!info) return;
    $("inspectT").textContent = info.title;
    $("inspectB").innerHTML = `<table>${(info.rows || []).map(([k, v]) => `<tr><td>${esc(k)}</td><td>${esc(v)}</td></tr>`).join("")}</table>` + (info.code ? `<code>${esc(info.code)}</code>` : "") + (info.note ? `<p class="note">${esc(info.note)}</p>` : "");
    $("inspect").hidden = false;
  }

  // ---- wiring ------------------------------------------------------------------------
  function setColourTheme(mode) {
    document.documentElement.dataset.theme = mode;
    try { localStorage.setItem("llp-theme", mode); } catch (e) { /* private mode */ }
  }
  function wire() {
    let saved = null;
    try { saved = localStorage.getItem("llp-theme"); } catch (e) { /* ignore */ }
    if (saved) document.documentElement.dataset.theme = saved;
    $("themeBtn").onclick = () => setColourTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
    $("runBtn").onclick = run;
    $("buildBtn").onclick = () => build(false);
    $("liveToggle").onchange = (e) => { S.live = e.target.checked; if (S.live) scheduleLive(); };
    $("pvAction").onclick = () => { const a = scene && scene.actions[0]; if (a && E3) a.fn(E3, S.world); };
    $("pvReset").onclick = () => E3 && E3.reset();
    $("pvMax").onclick = () => { const p = $("previewPanel"); p.classList.toggle("max"); $("pvMax").innerHTML = p.classList.contains("max") ? "&#10005;" : "&#10530;"; setTimeout(() => E3 && E3.resize(), 50); };
    document.querySelectorAll(".pv-tabs button").forEach((b) => (b.onclick = () => showPv(b.dataset.pv)));
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && $("previewPanel").classList.contains("max")) $("pvMax").click(); });
    $("hintBtn").onclick = hint;
    $("resetBtn").onclick = () => {
      if (!confirm("Put the starter code back for this file?")) return;
      cm.setValue(S.kind === "playground" ? TEMPLATES.blank : cur().starter); cm.focus();
    };
    $("tpl").onchange = (e) => { const t = TEMPLATES[e.target.value]; if (t && (!cm.getValue().trim() || confirm("Replace the code in the Playground with this template?"))) cm.setValue(t); e.target.value = ""; };
    $("inspectX").onclick = () => ($("inspect").hidden = true);
    $("donePlay").onclick = () => { $("done").close(); openPlayground(); };
    $("clearTerm").onclick = () => { termClear(true); clearErrLine(); };
    $("prevSlide").onclick = () => { if (S.slide > 0) { S.slide--; renderSlides(); } };
    $("nextSlide").onclick = () => { const l = cur(); if (l && S.slide < l.slides.length - 1) { S.slide++; renderSlides(); } };
    $("nextLesson").onclick = () => selectItem(S.kind, S.idx + 1);
    $("lessonPicker").onchange = (e) => selectLesson(Number(e.target.value));
    document.querySelectorAll(".tabs button").forEach((b) => (b.onclick = () => showTab(b.dataset.tab)));
    document.addEventListener("keydown", (e) => {
      if (!e.altKey || !cur()) return;
      if (e.key === "ArrowLeft") $("prevSlide").click();
      if (e.key === "ArrowRight") $("nextSlide").click();
    });

    const avatar = $("avatar"), menu = $("menu");
    avatar.onclick = (e) => { e.stopPropagation(); menu.hidden = !menu.hidden; avatar.setAttribute("aria-expanded", String(!menu.hidden)); };
    document.addEventListener("click", () => { menu.hidden = true; avatar.setAttribute("aria-expanded", "false"); });
    menu.onclick = async (e) => {
      const act = e.target.dataset.act;
      if (act === "profile") openSetup(true);
      if (act === "export") location.href = "/api/export";
      if (act === "report") location.href = "/api/report";
      if (act === "cert") window.open("/api/certificate", "_blank");
      if (act === "mentor") window.open("/mentor.html", "_blank");
      if (act === "reset" && confirm(`Start ${S.theme ? S.theme.system : "this track"} over? Your code for it will be erased.`)) {
        applyBootstrap(await api("/api/reset", {}));
      }
    };

    $("setupCancel").onclick = () => $("setup").close();
    $("setupForm").onsubmit = async (e) => {
      e.preventDefault();
      const industry = (document.querySelector('input[name="industry"]:checked') || {}).value;
      const switching = industry !== S.industry;
      await saveNow();
      const data = await api("/api/profile", { name: $("nameInput").value, industry });
      $("setup").close();
      if (switching || !S.lessons.length) await applyBootstrap(data); else { S.name = data.name; renderHeader(); }
    };
    $("setup").addEventListener("cancel", (e) => { if (!S.industry) e.preventDefault(); });
    $("doneClose").onclick = () => $("done").close();
    $("doneExport").onclick = () => (location.href = "/api/export");
    $("cmpClose").onclick = () => $("compare").close();
    window.addEventListener("beforeunload", () => {
      const it = cur();
      if (!it) return;
      const path = S.kind === "lesson" ? "/api/save" : "/api/drill_save";
      navigator.sendBeacon(path, new Blob([JSON.stringify({ id: it.id, code: cm.getValue() })], { type: "application/json" }));
    });
  }

  // ---- start ------------------------------------------------------------------------
  (async function init() {
    initEditor(); wire();
    window.llpDebug = () => ({ E3, S, cm });   // used by automated tests
    setInterval(() => fetch("/api/ping").catch(() => {}), 20000);
    await detectThree();
    const data = await api("/api/bootstrap");
    if (data.pack_errors && data.pack_errors.length) console.warn("Pack problems:", data.pack_errors);
    S.themes = data.themes; S.name = data.name; S.industry = data.industry; S.progress = data.progress || {};
    S.xp = data.xp || 0; S.streak = data.streak || 0;
    renderChips(false);
    if (!data.industry) { renderOutput(null); termClear(true); openSetup(false); return; }
    await applyBootstrap(data);
  })();
})();
