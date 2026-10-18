"""Checks every industry pack: run after editing curriculum.py or adding a pack.

    python3 validate.py

For each pack it confirms that
  - the pack file has every field it needs,
  - every lesson's reference solution passes and its starter does not,
  - every Bug Lab drill is broken as shipped and fixed by its solution,
  - every "predict the output" answer is really what the code does.
"""
import contextlib
import io
import sys

from curriculum import PACK_ERRORS, THEMES, build_drills, build_track
from server import run_code

bad = 0
for err in PACK_ERRORS:
    bad += 1
    print("PACK ERROR", err)


def predicted(code):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, "<predict>", "exec"), {"__name__": "__main__"})
        return buf.getvalue().strip()
    except Exception as e:
        return "!" + type(e).__name__


for key in (sys.argv[1:] or THEMES):
    lessons = build_track(key)
    files = {}
    for i, l in enumerate(lessons):
        prior = [[x["file"], files[x["id"]]] for x in lessons[:i]]
        base = {"mode": "run", "name": l["file"], "prior": prior, "checks": l["checks"]}
        sol = run_code({**base, "code": l["solution"]})
        start = {"passed": False} if l.get("slow") else run_code({**base, "code": l["starter"]})
        problems = []
        if not sol["passed"]:
            problems.append("solution: " + str(sol["error"] or [c for c in sol["checks"] if not c["ok"]]))
        if start["passed"] and not l.get("run_only"):
            problems.append("starter already passes")
        for pr in l["slides"]:
            if pr["kind"] == "predict":
                got = predicted(pr["code"])
                if got != pr["options"][pr["answer"]].strip():
                    problems.append(f"predict slide: code gives {got!r}, answer says {pr['options'][pr['answer']]!r}")
                if len(set(pr["options"])) != len(pr["options"]):
                    problems.append("predict options repeat")
            elif pr["kind"] == "quiz" and not (0 <= pr["answer"] < len(pr["options"])):
                problems.append("quiz answer index out of range")
        if l["slides"][-1]["title"] != "Your task" or len(l["slides"]) < 4:
            problems.append("lesson needs at least a scenario, teaching, a check and a task slide")
        if problems:
            bad += 1
            print(f"FAIL {key} {l['id']} {l['title']}")
            for p in problems:
                print("  ", p)
        files[l["id"]] = l["solution"]
    ids = [l['id'] for l in lessons]
    assert len(ids) == len(set(ids))
    drills = build_drills(key)
    for dr in drills:
        base = {"mode": "run", "name": dr["file"], "prior": [], "checks": dr["checks"]}
        sol, start = run_code({**base, "code": dr["solution"]}), run_code({**base, "code": dr["starter"]})
        if not sol["passed"] or start["passed"] or not (start["error"] or start["stdout"]):
            bad += 1
            print(f"FAIL {key} drill {dr['id']} {dr['title']}: solution passed={sol['passed']}, starter passed={start['passed']}")
    print(f"{key}: {len(lessons)} lessons, {len(drills)} drills checked")
sys.exit(1 if bad else 0)
