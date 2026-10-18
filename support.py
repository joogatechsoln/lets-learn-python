"""Server helpers: sandbox detection, per-learner workspace folders, spaced review and the certificate page."""
import csv
import datetime
import html
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ---- sandbox -----------------------------------------------------------------------------------------

SANDBOX = {"kind": "basic limits", "note": "CPU and memory limits, network and system commands switched off inside Python"}


def bwrap_command(inner, run_dir, workspace, app_dir):
    """The bubblewrap command line: no network, a read-only system, and write access to the workspace only."""
    cmd = ["bwrap", "--unshare-all", "--die-with-parent", "--new-session", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp"]
    for p in ("/usr", "/lib", "/lib64", "/lib32", "/bin", "/sbin", "/etc/alternatives", "/etc/ld.so.cache", "/etc/localtime"):
        cmd += ["--ro-bind-try", p, p]
    for p in {sys.prefix, sys.base_prefix, str(app_dir)}:
        if not p.startswith("/usr"):
            cmd += ["--ro-bind-try", p, p]
    cmd += ["--bind", str(run_dir), str(run_dir), "--bind", str(workspace), str(workspace), "--chdir", str(workspace), "--setenv", "HOME", str(workspace)]
    return cmd + inner


def detect_sandbox(runner, home):
    """Uses bubblewrap when it is installed AND passes a real smoke test. Otherwise stays on the basic limits."""
    mode = os.environ.get("LLP_SANDBOX", "auto").lower()
    SANDBOX.update(kind="basic limits", note="CPU and memory limits, network and system commands switched off inside Python")
    if mode == "off" or not shutil.which("bwrap"):
        return SANDBOX
    try:
        run_dir = Path(tempfile.mkdtemp(prefix="llp-smoke-", dir=str(home))) if home.exists() else Path(tempfile.mkdtemp(prefix="llp-smoke-"))
        ws = run_dir / "ws"
        ws.mkdir()
        req, out = run_dir / "req.json", run_dir / "out.json"
        req.write_text(json.dumps({"mode": "run", "name": "t.py", "code": "print('ok')", "prior": [], "checks": []}))
        cmd = bwrap_command([sys.executable, str(runner), str(req), str(out)], run_dir, ws, runner.parent)
        subprocess.run(cmd, timeout=10, capture_output=True, stdin=subprocess.DEVNULL)
        good = out.exists() and json.loads(out.read_text()).get("stdout") == "ok\n"
        shutil.rmtree(run_dir, ignore_errors=True)
        if good:
            SANDBOX.update(kind="bubblewrap", note="Your code runs with no network, a read-only system and write access to your workspace only")
        else:
            SANDBOX["note"] += " (bubblewrap is installed but did not start here)"
    except Exception as e:  # any failure keeps the safe default
        SANDBOX["note"] += f" (bubblewrap check failed: {e.__class__.__name__})"
    return SANDBOX


# ---- workspace (files the learner's programs can read and write) ----------------------------------------

MAX_FILE = 200_000


def workspace_dir(home, theme):
    ws = Path(home) / "workspace" / theme["key"]
    if not ws.exists():
        ws.mkdir(parents=True)
        seed_workspace(ws, theme)
    return ws


def seed_workspace(ws, theme):
    with open(ws / "records.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["name", "quantity", "rate"])
        w.writerows(theme["records"])
    (ws / "settings.json").write_text(json.dumps({"business": theme["biz"], "system": theme["system"], "level": theme["level"]}, indent=2))
    (ws / "notes.txt").write_text(f"Welcome to the {theme['system']} workspace.\nPrograms you run here can read and write these files.\n")


def list_workspace(ws):
    return [{"name": p.name, "bytes": p.stat().st_size} for p in sorted(ws.iterdir()) if p.is_file()]


def safe_name(name):
    name = os.path.basename(str(name))
    return name if name and not name.startswith(".") else None


def read_workspace(ws, name):
    name = safe_name(name)
    f = ws / name if name else None
    if not f or not f.is_file():
        return None
    return f.read_bytes()[:MAX_FILE].decode("utf-8", "replace")


def delete_workspace(ws, name):
    name = safe_name(name)
    f = ws / name if name else None
    if f and f.is_file():
        f.unlink()
        return True
    return False


# ---- spaced review ---------------------------------------------------------------------------------------

INTERVALS = [0, 1, 3, 7, 14, 30]     # days until a question returns, by box (box 0 is "never asked")


def review_pool(lessons, completed):
    pool = {}
    for l in lessons:
        if l["id"] in completed:
            for i, s in enumerate(l["slides"]):
                if s["kind"] in ("predict", "quiz"):
                    pool[f"{l['id']}:{i}"] = (l, s)
    return pool


def due_items(lessons, tr, today, limit=8):
    pool, state = review_pool(lessons, tr["completed"]), tr.setdefault("review", {})
    seen, new = [], []
    for key in pool:
        st = state.get(key)
        if st is None:
            new.append(key)
        elif st["due"] <= today:
            seen.append((st["due"], key))
    keys = [k for _, k in sorted(seen)] + new[: max(0, 5)]
    return pool, keys[:limit], len(seen) + min(len(new), 5)


def review_question(pool, key):
    l, s = pool[key]
    q = {k: s.get(k) for k in ("kind", "title", "code", "question", "options", "answer", "why")}
    q.update(key=key, lesson=l["title"], chapter=l["chapter"])
    return q


def record_review(tr, key, correct, today):
    state = tr.setdefault("review", {})
    box = min(state.get(key, {"box": 0})["box"] + 1, 5) if correct else 1
    due = (datetime.date.fromisoformat(today) + datetime.timedelta(days=INTERVALS[box])).isoformat()
    state[key] = {"box": box, "due": due}
    return state[key]


# ---- certificate -----------------------------------------------------------------------------------------

def certificate_html(name, theme, done, total, xp, rank, drills, today):
    e = html.escape
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Certificate: {e(name or 'Learner')}</title>
<style>
 body{{margin:0;font-family:Georgia,'Times New Roman',serif;background:#eef1f6;color:#13203a}}
 .page{{width:min(980px,96vw);margin:24px auto;background:#fff;border:14px double {e(theme['accent'])};padding:56px 64px;text-align:center;box-sizing:border-box}}
 h1{{font-size:44px;margin:0 0 6px;letter-spacing:.04em}} h2{{font-weight:400;font-size:20px;margin:0 0 34px;color:#4b5a78}}
 .name{{font-size:48px;margin:18px 0;border-bottom:2px solid {e(theme['accent'])};display:inline-block;padding:0 28px 6px}}
 p{{font-size:19px;line-height:1.6;margin:10px 0}} .stats{{display:flex;justify-content:center;gap:34px;margin:30px 0;flex-wrap:wrap}}
 .stats b{{display:block;font-size:30px;color:#13203a}} .stats span{{font-size:14px;color:#4b5a78;font-family:system-ui,sans-serif}}
 .foot{{margin-top:38px;font-size:15px;color:#4b5a78}} button{{font:600 15px system-ui;padding:10px 22px;border-radius:10px;border:0;background:#13203a;color:#fff;cursor:pointer;margin:10px}}
 @media print{{body{{background:#fff}} .page{{margin:0;width:auto;border-width:12px}} button{{display:none}}}}
</style></head><body><div class="page">
<h1>Certificate of Completion</h1><h2>Let's Learn Python</h2>
<p>This certifies that</p><div class="name">{e(name or 'A Learner')}</div>
<p>has completed the Python course in the <b>{e(theme['label'])}</b> track,<br>building the <b>{e(theme['system'])}</b> for <b>{e(theme['biz'])}</b>.</p>
<div class="stats"><div><b>{done}/{total}</b><span>lessons completed</span></div><div><b>{drills}</b><span>Bug Lab drills</span></div><div><b>{xp}</b><span>experience points</span></div><div><b>{e(rank)}</b><span>rank</span></div></div>
<p>Skills: variables and data types, functions and scope, unit testing, comparisons, loops, lists, dictionaries, sets, and error handling.</p>
<p class="foot">Issued {e(today)}</p><button onclick="window.print()">Print or save as PDF</button></div></body></html>"""
