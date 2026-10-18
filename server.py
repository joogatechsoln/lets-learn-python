#!/usr/bin/env python3
"""Let's Learn Python: a local, offline Python course.

Run:  python3 server.py   then open http://127.0.0.1:8765
Only the Python standard library is used. Progress lives in ~/.letslearnpython.
"""
import datetime
import json
import mimetypes
import os
import subprocess
import sys
import tempfile
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import support
from curriculum import PACK_ERRORS, THEMES, build_drills, build_track, public_themes

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
RUNNER = ROOT / "runner.py"
HOME = Path(os.environ.get("LLP_HOME", Path.home() / ".letslearnpython"))
STATE_FILE = HOME / "state.json"
TIMEOUT = 6
LAST_SEEN = [0.0]
LOCK = threading.Lock()
TRACKS = {}
DRILLS = {}
VERSION = 3
XP_LESSON, XP_DRILL = 15, 10
PLAYGROUND_AFTER = 12


def lessons_for(key):
    if key not in TRACKS:
        TRACKS[key] = build_track(key)
    return TRACKS[key]


def drills_for(key):
    if key not in DRILLS:
        DRILLS[key] = build_drills(key)
    return DRILLS[key]


# ---- state ---------------------------------------------------------------

def fresh_state():
    return {"version": VERSION, "name": "", "industry": None, "tracks": {}, "xp": 0, "streak": 0, "last_day": ""}


def load_state():
    try:
        state = json.loads(STATE_FILE.read_text())
    except (OSError, ValueError):
        return fresh_state()
    if state.get("version") != VERSION:  # older course layout: keep a copy, keep name and industry, restart tracks
        try:
            HOME.mkdir(parents=True, exist_ok=True)
            (HOME / f"state.v{state.get('version', 1)}.json").write_text(json.dumps(state, indent=2))
        except OSError:
            pass
        new = fresh_state()
        new["name"] = state.get("name", "")
        new["industry"] = state.get("industry") if state.get("industry") in THEMES else None
        return new
    return state


def save_state(state):
    HOME.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2))
    tmp.replace(STATE_FILE)


def track_of(state, key=None):
    key = key or state["industry"]
    tr = state["tracks"].setdefault(key, {"completed": [], "files": {}, "drills": [], "drill_files": {}})
    tr.setdefault("drills", [])
    tr.setdefault("drill_files", {})
    return tr


def award(state, amount):
    """Adds XP and keeps the day streak. Returns the new totals."""
    today = datetime.date.today()
    last = state.get("last_day") or ""
    if last != today.isoformat():
        yesterday = (today - datetime.timedelta(days=1)).isoformat()
        state["streak"] = state.get("streak", 0) + 1 if last == yesterday else 1
        state["last_day"] = today.isoformat()
    state["xp"] = state.get("xp", 0) + amount
    return {"xp": state["xp"], "streak": state["streak"], "gained": amount}


RANKS = [(0, "Newcomer"), (100, "Apprentice"), (250, "Practitioner"), (500, "Specialist"), (900, "Polyglot")]


def rank_name(xp):
    return [n for t, n in RANKS if xp >= t][-1]


def bootstrap(state):
    key = state["industry"]
    out = {"name": state["name"], "industry": key, "themes": public_themes(), "lessons": [], "drills": [], "track": None,
           "xp": state.get("xp", 0), "streak": state.get("streak", 0), "pack_errors": PACK_ERRORS,
           "progress": {k: len(v["completed"]) for k, v in state["tracks"].items()}}
    if key in THEMES:
        out["lessons"] = lessons_for(key)
        out["drills"] = drills_for(key)
        out["track"] = track_of(state, key)
        out["workspace"] = support.list_workspace(support.workspace_dir(HOME, THEMES[key]))
        out["review_due"] = support.due_items(out["lessons"], out["track"], datetime.date.today().isoformat())[2]
    out["sandbox"] = dict(support.SANDBOX)
    return out


# ---- running code --------------------------------------------------------

def run_code(req, workspace=None, stdin=""):
    """Runs the runner in a separate process. With a workspace the program can read and write files there."""
    run_root = HOME / "run"
    run_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=str(run_root)) as tmp:
        req = dict(req, stdin=stdin)
        req_path, out_path = os.path.join(tmp, "req.json"), os.path.join(tmp, "out.json")
        with open(req_path, "w") as fh:
            json.dump(req, fh)
        inner = [sys.executable, str(RUNNER), req_path, out_path]
        cwd = str(workspace) if workspace else tmp
        cmd = support.bwrap_command(inner, tmp, workspace or tmp, ROOT) if support.SANDBOX["kind"] == "bubblewrap" else inner
        try:
            subprocess.run(cmd, cwd=cwd, timeout=TIMEOUT, stdin=subprocess.DEVNULL, capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            return {"stdout": "", "checks": [], "passed": False, "stopped": True,
                    "error": f"Stopped after {TIMEOUT - 1} seconds. Look for a loop that never ends."}
        if os.path.exists(out_path):
            with open(out_path) as fh:
                return json.load(fh)
        return {"stdout": "", "checks": [], "passed": False, "stopped": True,
                "error": "Your program ran for too long or used too much memory, so it was stopped. "
                         "Look for a loop that never ends."}


def prior_files(lessons, files, upto):
    return [[l["file"], files.get(l["id"], "")] for l in lessons[:upto]]


def combined_source(lessons, files, completed, theme=None):
    head = "# Built with Let's Learn Python. Each section is one lesson.\n"
    if theme:
        head = f"# {theme['system']} for {theme['biz']}\n# Built with Let's Learn Python. Each section is one lesson.\n"
    parts = [head]
    for l in lessons:
        if l["id"] in completed:
            parts.append(f"\n# ---- {l['n']:02d} {l['title']} ----\n{files.get(l['id'], '').rstrip()}\n")
    return "".join(parts)


# ---- HTTP ----------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    server_version = "LetsLearnPython"

    def log_message(self, *args):
        pass

    def send_json(self, obj, status=200):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def body(self):
        length = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self):
        path = self.path.split("?")[0]
        LAST_SEEN[0] = time.time()
        if path == "/api/ping":
            return self.send_json({"ok": True})
        if path == "/api/bootstrap":
            with LOCK:
                return self.send_json(bootstrap(load_state()))
        if path == "/api/export":
            with LOCK:
                state = load_state()
                if state["industry"] not in THEMES:
                    return self.send_json({"error": "Pick an industry first."}, 400)
                lessons, tr = lessons_for(state["industry"]), track_of(state)
                text = combined_source(lessons, tr["files"], tr["completed"], THEMES[state["industry"]])
            data = text.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/x-python; charset=utf-8")
            self.send_header("Content-Disposition", 'attachment; filename="project.py"')
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            return self.wfile.write(data)
        if path == "/api/engine":
            f = STATIC / "vendor" / "three.min.js"
            size = f.stat().st_size if f.is_file() else 0
            return self.send_json({"three": size > 100000, "bytes": size, "sandbox": support.SANDBOX})
        if path == "/api/workspace":
            with LOCK:
                state = load_state()
                if state["industry"] not in THEMES:
                    return self.send_json({"error": "Pick an industry first."}, 400)
                ws = support.workspace_dir(HOME, THEMES[state["industry"]])
            name = self.path.split("name=")[1] if "name=" in self.path else None
            if name:
                from urllib.parse import unquote
                text = support.read_workspace(ws, unquote(name))
                return self.send_json({"name": unquote(name), "text": text}, 200 if text is not None else 404)
            return self.send_json({"workspace": support.list_workspace(ws)})
        if path == "/api/certificate":
            with LOCK:
                state = load_state()
                key = state["industry"]
                if key not in THEMES:
                    return self.send_json({"error": "Pick an industry first."}, 400)
                lessons, tr = lessons_for(key), track_of(state)
                page = support.certificate_html(state["name"], THEMES[key], len(tr["completed"]), len(lessons), state.get("xp", 0),
                                                rank_name(state.get("xp", 0)), len(tr.get("drills", [])), datetime.date.today().isoformat()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            return self.wfile.write(page)
        if path == "/api/report":
            with LOCK:
                state = load_state()
            rep = {"name": state["name"], "xp": state.get("xp", 0), "rank": rank_name(state.get("xp", 0)), "streak": state.get("streak", 0),
                   "generated": datetime.date.today().isoformat(), "tracks": {}}
            for key, tr in state["tracks"].items():
                if key in THEMES:
                    ls = lessons_for(key)
                    chapters = {}
                    for l in ls:
                        c = chapters.setdefault(l["chapter_n"], {"n": l["chapter_n"], "title": l["chapter"], "done": 0, "total": 0})
                        c["total"] += 1
                        c["done"] += l["id"] in tr["completed"]
                    rep["tracks"][key] = {"industry": THEMES[key]["label"], "lessons_done": len(tr["completed"]), "lessons_total": len(ls),
                                          "bug_drills_done": len(tr.get("drills", [])), "bug_drills_total": len(drills_for(key)),
                                          "chapters": list(chapters.values()), "reviews_done": len(tr.get("review", {}))}
            data = json.dumps(rep, indent=2).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Disposition", 'attachment; filename="progress-report.json"')
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            return self.wfile.write(data)
        target = (STATIC / ("index.html" if path == "/" else path.lstrip("/"))).resolve()
        if STATIC not in target.parents and target != STATIC / "index.html" or not target.is_file():
            return self.send_json({"error": "not found"}, 404)
        data = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(str(target))[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        path, data = self.path.split("?")[0], self.body()
        with LOCK:
            state = load_state()
            if path == "/api/profile":
                if "name" in data:
                    state["name"] = str(data["name"]).strip()[:40]
                if data.get("industry") in THEMES:
                    state["industry"] = data["industry"]
                save_state(state)
                return self.send_json(bootstrap(state))
            if state["industry"] not in THEMES:
                return self.send_json({"error": "Pick an industry first."}, 400)
            lessons, tr = lessons_for(state["industry"]), track_of(state)
            by_id = {l["id"]: (i, l) for i, l in enumerate(lessons)}
            ws = support.workspace_dir(HOME, THEMES[state["industry"]])
            rc = lambda req: run_code(req, workspace=ws, stdin=str(data.get("stdin", "")))

            if path == "/api/save":
                if data.get("id") in by_id:
                    tr["files"][data["id"]] = str(data.get("code", ""))
                    save_state(state)
                return self.send_json({"ok": True})

            if path == "/api/run":
                if data.get("id") not in by_id:
                    return self.send_json({"error": "Unknown lesson."}, 400)
                idx, lesson = by_id[data["id"]]
                if any(l["id"] not in tr["completed"] for l in lessons[:idx]):
                    return self.send_json({"error": "Finish the earlier lessons first."}, 400)
                code = str(data.get("code", ""))
                tr["files"][lesson["id"]] = code
                result = rc({"mode": "run", "name": lesson["file"], "code": code,
                                   "prior": prior_files(lessons, tr["files"], idx), "checks": lesson["checks"]})
                result["newly_completed"] = bool(result["passed"] and lesson["id"] not in tr["completed"])
                if result["newly_completed"]:
                    tr["completed"].append(lesson["id"])
                    result["reward"] = award(state, XP_LESSON)
                save_state(state)
                result["completed"] = tr["completed"]
                return self.send_json(result)

            if path == "/api/build":
                done = [l for l in lessons if l["id"] in tr["completed"]]
                result = rc({"mode": "build", "prior": [[l["file"], tr["files"].get(l["id"], "")] for l in done]})
                result["modules"] = [l["module"] for l in done]
                return self.send_json(result)

            if path == "/api/preview":
                # Runs everything finished so far, with the current editor code in place of its saved file (not graded).
                cur_id, code = data.get("id"), str(data.get("code", ""))
                seq = []
                for l in lessons:
                    if l["id"] == cur_id:
                        seq.append([l["file"], code])
                    elif l["id"] in tr["completed"]:
                        seq.append([l["file"], tr["files"].get(l["id"], "")])
                result = rc({"mode": "preview", "prior": seq, "checks": [], "cpu": 2})
                result["completed"] = len(tr["completed"])
                return self.send_json(result)

            if path == "/api/playground_save":
                tr["playground"] = str(data.get("code", ""))[:50000]
                save_state(state)
                return self.send_json({"ok": True})

            if path == "/api/playground_run":
                if len(tr["completed"]) < PLAYGROUND_AFTER:
                    return self.send_json({"error": "The Playground opens when you finish chapter 1."}, 400)
                code = str(data.get("code", ""))
                tr["playground"] = code[:50000]
                seq = [[l["file"], tr["files"].get(l["id"], "")] for l in lessons if l["id"] in tr["completed"]]
                result = rc({"mode": "run", "name": "playground.py", "code": code, "prior": seq, "checks": []})
                result["workspace"] = support.list_workspace(ws)
                save_state(state)
                return self.send_json(result)

            if path == "/api/workspace_delete":
                support.delete_workspace(ws, data.get("name"))
                return self.send_json({"workspace": support.list_workspace(ws)})

            if path == "/api/workspace_reset":
                for p in list(ws.iterdir()):
                    if p.is_file():
                        p.unlink()
                support.seed_workspace(ws, THEMES[state["industry"]])
                return self.send_json({"workspace": support.list_workspace(ws)})

            if path == "/api/review":
                today = datetime.date.today().isoformat()
                if data.get("answer"):
                    a = data["answer"]
                    pool = support.review_pool(lessons, tr["completed"])
                    reward = None
                    if a.get("key") in pool:
                        support.record_review(tr, a["key"], bool(a.get("correct")), today)
                        if a.get("correct"):
                            reward = award(state, 2)
                        save_state(state)
                    return self.send_json({"ok": True, "reward": reward})
                pool, keys, due = support.due_items(lessons, tr, today)
                return self.send_json({"questions": [support.review_question(pool, k) for k in keys], "due": due})

            if path == "/api/source":
                return self.send_json({"code": combined_source(lessons, tr["files"], tr["completed"], THEMES[state["industry"]])})

            if path == "/api/drill_save":
                if data.get("id") in {x["id"] for x in drills_for(state["industry"])}:
                    tr["drill_files"][data["id"]] = str(data.get("code", ""))
                    save_state(state)
                return self.send_json({"ok": True})

            if path == "/api/drill_run":
                drills = {x["id"]: x for x in drills_for(state["industry"])}
                drill = drills.get(data.get("id"))
                if not drill:
                    return self.send_json({"error": "Unknown drill."}, 400)
                if drill["after"] not in tr["completed"]:
                    return self.send_json({"error": "Finish the lesson that unlocks this drill first."}, 400)
                code = str(data.get("code", ""))
                tr["drill_files"][drill["id"]] = code
                result = rc({"mode": "run", "name": drill["file"], "code": code, "prior": [], "checks": drill["checks"]})
                result["newly_completed"] = bool(result["passed"] and drill["id"] not in tr["drills"])
                if result["newly_completed"]:
                    tr["drills"].append(drill["id"])
                    result["reward"] = award(state, XP_DRILL)
                save_state(state)
                result["drills_done"] = tr["drills"]
                return self.send_json(result)

            if path == "/api/compare":
                n = int(data.get("n", 0))
                mine = [l for l in lessons if l["n"] == n]
                if not mine or mine[0]["id"] not in tr["completed"]:
                    return self.send_json({"error": "Finish this lesson to compare it with other industries."}, 400)
                out = []
                for key, th in THEMES.items():
                    them = lessons_for(key)
                    if n <= len(them):
                        out.append({"key": key, "label": th["label"], "icon": th["icon"], "accent": th["accent"],
                                    "system": th["system"], "title": them[n - 1]["title"], "code": them[n - 1]["solution"]})
                return self.send_json({"n": n, "items": out, "current": state["industry"]})

            if path == "/api/reset":
                state["tracks"][state["industry"]] = {"completed": [], "files": {}}
                save_state(state)
                return self.send_json(bootstrap(state))
        return self.send_json({"error": "not found"}, 404)


def main():
    port = int(os.environ.get("PORT", "8765"))
    url = f"http://127.0.0.1:{port}"
    HOME.mkdir(parents=True, exist_ok=True)
    try:
        httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    except OSError:
        print(f"Let's Learn Python is already running at {url}. Opening it.")
        if "--no-browser" not in sys.argv:
            webbrowser.open(url)
        return
    box = support.detect_sandbox(RUNNER, HOME)
    print(f"Sandbox: {box['kind']}. {box['note']}")
    print(f"Let's Learn Python is running at {url}  (Ctrl+C to stop)")
    if "--no-browser" not in sys.argv:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    idle = float(os.environ.get("LLP_IDLE_MINUTES", "0") or 0)   # the desktop launcher sets this so closing the tab ends the app
    if idle > 0:
        LAST_SEEN[0] = time.time()

        def watch():
            while True:
                time.sleep(15)
                if time.time() - LAST_SEEN[0] > idle * 60:
                    print("No browser tab is open any more. Stopping.")
                    httpd.shutdown()
                    return
        threading.Thread(target=watch, daemon=True).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
