"""Industry packs and the shared lesson path.

Each industry lives in packs/<key>.json (data only). Every pack fills the same
15 lessons with its own business, vocabulary, numbers, rule and class, so adding
an industry means adding one JSON file. Text uses <<token>> placeholders that are
filled from the pack. See packs/README.md for every field.
"""
import builtins
import contextlib
import io
import json
import operator
import sys
import types
from pathlib import Path

PACK_DIR = Path(__file__).resolve().parent / "packs"
REQUIRED = ["key", "label", "icon", "accent", "tagline", "biz", "system", "role", "thing", "things", "records",
            "qty_unit", "rate_unit", "rp", "rs", "tp", "ts", "level", "msg_le", "msg_gt", "missing", "missing_msg",
            "delivery", "delivery_note", "stock_noun", "total_label", "vw", "alert_name", "opening", "rule", "scene",
            "v", "cls", "glossary", "probe", "py_uses"]
V_KEYS = ["name", "qty", "rate", "total", "level", "names", "qtys", "rates", "value_fn", "report_fn", "find_fn", "read_fn", "new"]
CLS_KEYS = ["name", "qty", "rate", "value", "action"]
OPS = {">": operator.gt, "<=": operator.le}
CHAPTERS = ["The basics", "Making decisions", "Collections", "Functions", "Debugging", "Putting it together",
            "Safe and structured", "Final check"]
EMOJI = ["👋", "📦", "🧮", "🧾", "🚨", "📋", "🔁", "🗂️", "⚙️", "🐞", "📊", "🔎", "🛡️", "🧱", "✅"]


def check_pack(p):
    """Returns a list of problems with a pack (empty when it is fine)."""
    bad = [f"missing field '{k}'" for k in REQUIRED if k not in p]
    if bad:
        return bad
    bad += [f"v.{k} missing" for k in V_KEYS if k not in p["v"]]
    bad += [f"cls.{k} missing" for k in CLS_KEYS if k not in p["cls"]]
    if len(p["records"]) != 4 or any(len(r) != 3 for r in p["records"]):
        bad.append("records needs exactly 4 rows of [name, quantity, rate]")
    act = p["cls"].get("action", {})
    if act.get("kind") not in ("add", "take", "check"):
        bad.append("cls.action.kind must be add, take or check")
    if act.get("kind") == "check" and act.get("cmp") not in OPS:
        bad.append("cls.action.cmp must be > or <=")
    if act.get("kind") == "take" and "err" not in act:
        bad.append("cls.action.err is needed for kind 'take'")
    return bad


def load_packs():
    themes, errors = {}, []
    for f in sorted(PACK_DIR.glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            p = json.loads(f.read_text(encoding="utf-8"))
        except ValueError as e:
            errors.append(f"{f.name}: not valid JSON ({e})")
            continue
        problems = check_pack(p)
        if problems:
            errors.append(f"{f.name}: " + "; ".join(problems))
            continue
        themes[p["key"]] = p
    ordered = sorted(themes.values(), key=lambda p: (p.get("order", 99), p["key"]))
    return {p["key"]: p for p in ordered}, errors


THEMES, PACK_ERRORS = load_packs()


def fill(text, ctx):
    for _ in range(4):
        for key, val in ctx.items():
            text = text.replace(f"<<{key}>>", str(val))
    return text


def capture(code, prelude=""):
    """Runs trusted course code and returns what it printed (used to compute expected output)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(prelude + code, "<capture>", "exec"), {"__name__": "__main__"})
    return buf.getvalue()


def public_themes():
    keep = ["label", "icon", "accent", "tagline", "biz", "system", "glossary", "v", "cls", "records", "level", "msg_le", "msg_gt",
            "probe", "qty_unit", "thing", "things", "delivery", "total_label", "rp", "rs", "tp", "ts"]
    return [{"key": k, **{f: t[f] for f in keep}, "world": t.get("world", "retail"), "world_text": t.get("world_text", {})} for k, t in THEMES.items()]


def typo(s):
    return s[:-2] + s[-1]


def make_ctx(t):
    rec, V, C = t["records"], t["v"], t["cls"]
    names = [r[0] for r in rec]
    ctx = {k: v for k, v in t.items() if isinstance(v, (str, int, float))}
    R = lambda x: f"{t['rp']}{x}{t['rs']}"
    T = lambda x: f"{t['tp']}{x}{t['ts']}"
    ctx.update(vn=V["name"], vq=V["qty"], vr=V["rate"], vt=V["total"], vl=V["level"], vnames=V["names"], vstock=V["qtys"],
               vrates=V["rates"], vfn=V["value_fn"], vrep=V["report_fn"], vfind=V["find_fn"], vread=V["read_fn"], vnew=V["new"],
               vnew_typo=typo(V["new"]), vq_typo=typo(V["qty"]), cls=C["name"], aq=C["qty"], ar=C["rate"], cval=C["value"],
               cact=C["action"]["name"], cdoc=C["action"].get("doc", ""), cerr=C["action"].get("err", ""),
               cmp=C["action"].get("cmp", ""))
    for i, (n, q, p) in enumerate(rec, 1):
        ctx.update({f"n{i}": n, f"q{i}": q, f"p{i}": p, f"R{i}": R(p), f"T{i}": T(q * p)})
    grand = 0
    for _, q, p in rec:
        grand += q * p
    d = t["delivery"]
    ctx.update(total=rec[0][1] * rec[0][2], grand=grand, d=d, final=rec[0][1] + d, GT=T(grand), names_all=", ".join(names),
               first3=", ".join(f'"{n}"' for n in names[:3]), n1_lower=names[0].lower(),
               rate_phrase=R(rec[0][2]) + (" " + t["rate_unit"] if t["rate_unit"] else ""))
    P = t["probe"]
    ctx.update(sn=P["name"], stag=P["tag"], sid=P["id"], sunit=P["unit"], sread=P["reading"], starget=P["target"], sraw=P["raw_label"],
               stext=P["text_reading"], sx=P["pos"][0], sy=P["pos"][1], spos=P["pos_label"], bw=P["batch_word"], bsz=P["batch_size"],
               VL=V["level"].upper(), use1=t["py_uses"][0], use2=t["py_uses"][1], use3=t["py_uses"][2], sreads=P["readings"])
    qs, ps = [r[1] for r in rec], [r[2] for r in rec]
    ctx.update(all4=", ".join(f'"{n}"' for n in names), nlist="[" + ", ".join(f'"{n}"' for n in names) + "]", qlist=str(qs), plist=str(ps),
               sensor_list=str(P["readings"]))
    ctx["msg_le_f"], ctx["msg_gt_f"] = fill(t["msg_le"], ctx), fill(t["msg_gt"], ctx)
    ctx["w_le"], ctx["w_gt"] = ctx["msg_le_f"].split(":")[0], ctx["msg_gt_f"].split(":")[0]
    ctx["missing_msg_f"] = fill(t["missing_msg"], ctx)
    return ctx, R, T


def T(title, body):
    return {"kind": "text", "title": title, "body": body}


def P(code, right, wrong, why):
    """Predict the output. `right` is the exact printed text, or !ErrorName when the code crashes."""
    return {"kind": "predict", "title": "Predict the output", "code": code, "right": right, "wrong": list(wrong), "why": why}


def Q(question, options, answer, why, code=None, title="Check yourself"):
    return {"kind": "quiz", "title": title, "question": question, "options": list(options), "answer": answer, "why": why, "code": code}


def jsonable(v):
    if isinstance(v, (set, frozenset)):
        return sorted(v, key=lambda x: (type(x).__name__, str(x)))
    return list(v) if isinstance(v, tuple) else v


class Course:
    """Builds one industry's lessons in order. Solutions run in one shared namespace, exactly like the runner does."""

    def __init__(self, key):
        self.key = key
        self.t = THEMES[key]
        self.ctx, self.R, self.T = make_ctx(self.t)
        self.lessons, self.chapters = [], []
        self.mod = types.ModuleType("__main__")
        self.g = self.mod.__dict__

    def f(self, s):
        return fill(s, self.ctx)

    def set_chapter(self, title):
        if title not in self.chapters:
            self.chapters.append(title)
        self.chapter = title

    def run(self, code):
        buf, saved = io.StringIO(), sys.modules.get("__main__")
        sys.modules["__main__"] = self.mod
        try:
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                exec(compile(code, "<course>", "exec"), self.g)
        finally:
            sys.modules["__main__"] = saved
        import unittest
        for k, v in list(self.g.items()):
            if isinstance(v, type) and issubclass(v, unittest.TestCase) and v.__module__ == "__main__":
                del self.g[k]
        return buf.getvalue()

    def _slide(self, s, n):
        s = dict(s)
        for k in ("title", "body", "question", "why", "code", "right"):
            if isinstance(s.get(k), str) and not (k == "right" and s[k].startswith("!")):
                s[k] = self.f(s[k])
        if s["kind"] == "predict":
            wrong = [self.f(w) if isinstance(w, str) else w for w in s.pop("wrong")]
            pos = n % (len(wrong) + 1)
            wrong.insert(pos, s.pop("right"))
            s["options"], s["answer"] = wrong, pos
        elif s["kind"] == "quiz":
            s["options"] = [self.f(o) for o in s["options"]]
        return s

    def _append(self, slug, title, module, skill, slides, task, starter, sol, checks, hints, emoji, run_only, slow=False):
        n = len(self.lessons) + 1
        slides = [self._slide(s, n) for s in slides] + [{"kind": "text", "title": "Your task", "body": task}]
        self.lessons.append({
            "id": f"L{n:02d}", "n": n, "slug": slug, "file": f"{n:02d}_{slug}.py", "title": self.f(title), "chapter": self.chapter,
            "chapter_n": self.chapters.index(self.chapter) + 1, "module": self.f(module), "skill": skill, "emoji": emoji,
            "slides": slides, "starter": starter, "checks": checks, "hints": [self.f(h) for h in hints], "solution": sol,
            "run_only": run_only, "slow": slow})

    def add(self, slug, title, module, skill, slides, task, starter, solution, checks=(), hints=(), emoji="📘", last_only=False, run_only=False, no_out=False, slow=False):
        """A full lesson. `checks` may hold dicts or short specs resolved against the solution:
        ("var", name[, strict]), ("absent", name), ("ast", Node, what), ("prints", n), ("comments", n), ("last",)"""
        sol = self.f(solution)
        out = self.run(sol).strip()
        res = []
        for ck in checks:
            if isinstance(ck, dict):
                res.append(ck)
                continue
            kind = ck[0]
            if kind == "var":
                val = self.g[ck[1]]
                res.append({"type": "var_equals", "name": ck[1], "value": jsonable(val), "strict": len(ck) > 2 and ck[2], "label": f"{ck[1]} is {val!r}"})
            elif kind == "absent":
                res.append({"type": "var_absent", "name": ck[1], "label": f"{ck[1]} no longer exists"})
            elif kind == "ast":
                res.append({"type": "ast_has", "node": ck[1], "what": ck[2], "label": f"Uses {ck[2]}"})
            elif kind == "prints":
                res.append({"type": "ast_count", "func": "print", "min": ck[1], "label": f"Calls print at least {ck[1]} times"})
            elif kind == "fout":    # ("fout", function name, [args]): what calling it prints
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    self.g[ck[1]](*(ck[2] if len(ck) > 2 else []))
                res.append({"type": "func_output", "name": ck[1], "args": list(ck[2]) if len(ck) > 2 else [], "value": buf.getvalue().strip(),
                            "label": f"{ck[1]}() prints the right thing"})
            elif kind == "ftest":   # ("ftest", name, [[args, expected], ...])
                res.append({"type": "func_tests", "name": ck[1], "tests": [[a, jsonable(e)] for a, e in ck[2]], "label": f"{ck[1]}() gives the right answers"})
            elif kind == "unit":    # ("unit", class name, minimum tests)
                res.append({"type": "unit_class", "name": ck[1], "min_tests": ck[2], "all_pass": True, "label": f"{ck[1]} has at least {ck[2]} passing tests"})
            elif kind == "catches": # ("catches", class name, [broken source, ...])
                res.append({"type": "unit_catches", "name": ck[1], "bad": ck[2], "label": "Your tests catch the broken versions"})
            elif kind == "has":     # ("has", "text"): the output must contain this
                res.append({"type": "stdout_has", "value": ck[1], "label": f"The output contains {ck[1]}"})
            elif kind == "doc":
                res.append({"type": "func_doc", "name": ck[1], "min": 30, "label": f"{ck[1]}() has a docstring"})
            elif kind == "comments":
                res.append({"type": "source_count", "pattern": r"^\s*#", "min": ck[1], "label": f"Has at least {ck[1]} comment lines of its own"})
        if (out or not res) and not no_out:
            last = out.splitlines()[-1] if out else ""
            res.append({"type": "stdout_last", "value": last, "label": "The last line is right"} if last_only else
                       {"type": "stdout_equals", "value": out, "label": "Prints exactly the expected output"})
        task = self.f(task).replace("<<OUT>>", "```text\n" + out + "\n```")
        self._append(slug, title, module, skill, slides, task, self.f(starter), sol, res, hints, emoji, run_only, slow)

    def legacy(self, slug, title, chapter, module, skill, scenario, concept, pred, task, starter, checks, hints, solution):
        """The first version's compact lesson signature (chapters 3 to 9)."""
        self.set_chapter(chapter)
        sol = self.f(solution)
        self.run(sol)
        n = len(self.lessons) + 1
        emoji = ["🚨", "📋", "🔁", "🗂️", "⚙️", "🐞", "📊", "🔎", "🛡️", "🧱", "✅"][min(n - 34, 10)] if n >= 34 else "📘"
        self._append(slug, title, module, skill, [T("The scenario", scenario), T("The idea", concept), P(*pred)], self.f(task), self.f(starter),
                     sol, checks, hints, emoji, False)


def build_track(key):
    import lessons_ch1, lessons_ch2, lessons_ch3, lessons_ch4, lessons_ch5, lessons_ch6, lessons_ch7, lessons_ch8, lessons_ch9, lessons_ch10, lessons_ch11, lessons_ch12
    c = Course(key)
    lessons_ch1.build(c)
    lessons_ch2.build(c)
    lessons_ch3.build(c)
    lessons_ch4.build(c)
    lessons_ch5.build(c)
    lessons_ch6.build(c)
    lessons_ch7.build(c)
    lessons_ch8.build(c)
    lessons_ch9.build(c)
    lessons_ch10.build(c)
    lessons_ch11.build(c)
    lessons_ch12.build(c)
    totals = {}
    for l in c.lessons:
        totals[l["chapter_n"]] = totals.get(l["chapter_n"], 0) + 1
        l["in_chapter"] = totals[l["chapter_n"]]
    for l in c.lessons:
        l["chapter_total"] = totals[l["chapter_n"]]
    return c.lessons


def build_drills(key):
    """Eight standalone bug-hunt drills. Each unlocks after the lesson that teaches what it needs."""
    t = THEMES[key]
    ctx, R, Tt = make_ctx(t)
    f = lambda s: fill(s, ctx)
    rec = t["records"]
    q3 = [r[1] for r in rec[:3]]
    after_ids = {l["slug"]: l["id"] for l in build_track(key)}
    drills = []

    def drill(slug, after, err, title, report, starter, solution, hints):
        n = len(drills) + 1
        sol, start = f(solution), f(starter)
        want = capture(sol).strip()
        drills.append({
            "id": f"B{n}", "n": n, "file": f"bug_{n}_{slug}.py", "title": title, "chapter": "Bug Lab", "module": title, "error": err,
            "after": after_ids[after], "skill": f"spot a {err}" if err != "Wrong answer" else "find a silent logic bug",
            "slides": [{"kind": "text", "title": "The bug report", "body": f(report)},
                       {"kind": "text", "title": "Your task", "body": "Run the program, read what Python tells you, and fix the bug so it prints:\n\n```text\n" + want + "\n```\n\nChange as little as you can."}],
            "starter": start, "checks": [{"type": "stdout_equals", "value": want, "label": "Prints the expected output"}],
            "hints": [f(h) for h in hints], "solution": sol,
        })

    drill("typo", "reading_the_traceback", "NameError", "The missing variable",
          "The report should say \"<<n1>>\" but the program crashes before printing it. A **NameError** means Python met a name it has never seen. Check the spelling.",
          "<<vq>> = <<q1>>\nprint(f\"<<n1>>: {<<vq_typo>>}\")\n", "<<vq>> = <<q1>>\nprint(f\"<<n1>>: {<<vq>>}\")\n",
          ["The error names the missing word. Compare it with the variable defined on line 1.", "One letter is missing from the name in the print line."])
    drill("zero", "reading_the_traceback", "ZeroDivisionError", "The empty period",
          "The daily average for the <<things>> crashes. A **ZeroDivisionError** means something was divided by zero. Find which number is on the bottom.",
          "days = 0\nprint(<<q1>> / days)\n", "days = 4\nprint(<<q1>> / days)\n",
          ["The traceback shows the line. Which variable is being divided by?", "The period was 4 days. Fix the value of `days`."])
    drill("text_number", "data_types_trap", "TypeError", "Text is not a number",
          "The count came from <<delivery_note>> and was kept as text. Adding the new delivery of <<d>> crashes. A **TypeError** means you mixed types that don't go together.",
          "<<vq>> = \"<<q1>>\"      # copied from a note, so it is text\n<<vnew>> = <<vq>> + <<d>>\nprint(<<vnew>>)\n",
          "<<vq>> = \"<<q1>>\"      # copied from a note, so it is text\n<<vnew>> = int(<<vq>>) + <<d>>\nprint(<<vnew>>)\n",
          ["The last line of the traceback says which two types clashed.", "Turn the text into a number with `int(...)` before adding."])
    drill("bad_number", "shape_shifting", "ValueError", "The word that isn't a number",
          "Someone typed a word into <<delivery_note>>. Converting it crashes. A **ValueError** means the type is right but the value can't be used, like int(\"twenty\").",
          "delivery = int(\"twenty\")\nprint(<<q1>> + delivery)\n", "delivery = int(\"<<d>>\")\nprint(<<q1>> + delivery)\n",
          ["`int(...)` only accepts text made of digits.", "The note should say <<d>>, written with digits."])
    drill("average", "telemetry_averages", "Wrong answer", "The average that looks wrong",
          "No crash this time, but the average of the first three <<things>> is far too big. Silent bugs like this only show in the output. Think about which part Python calculates first.",
          f"counts = [{q3[0]}, {q3[1]}, {q3[2]}]\naverage = counts[0] + counts[1] + counts[2] / 3\nprint(average)\n",
          f"counts = [{q3[0]}, {q3[1]}, {q3[2]}]\naverage = (counts[0] + counts[1] + counts[2]) / 3\nprint(average)\n",
          ["Division happens before addition. Which number is being divided?", "Wrap the three numbers in brackets before dividing by 3."])
    drill("colon", "for_loop", "SyntaxError", "The loop that won't start",
          "A colleague's loop over the <<things>> won't even start. Python refuses to run the file and points at a line. A **SyntaxError** means the code is written wrongly, so nothing runs at all.",
          "names = [<<first3>>]\nfor name in names\n    print(name)\n", "names = [<<first3>>]\nfor name in names:\n    print(name)\n",
          ["Look at the line Python points to. What does a `for` line end with?", "Add a colon at the end of the `for` line."])
    drill("off_by_one", "range_function", "IndexError", "One step too far",
          "The numbered list of <<things>> prints fine, then crashes at the very end. An **IndexError** means you asked a list for a position that isn't there. Lists start at 0 and the last position is one less than the length.",
          "names = [<<first3>>]\nfor i in range(len(names) + 1):\n    print(i + 1, names[i])\n",
          "names = [<<first3>>]\nfor i in range(len(names)):\n    print(i + 1, names[i])\n",
          ["Count how many times the loop runs, and how many names there are.", "`range(len(names) + 1)` goes one too far. Remove the `+ 1`."])
    drill("wrong_key", "dict_access", "KeyError", "The key that isn't there",
          "Looking up \"<<n1_lower>>\" crashes the program. A **KeyError** means the dictionary has no such key. Keys must match exactly, capital letters included.",
          "<<vstock>> = {" + ", ".join(f'"{r[0]}": {r[1]}' for r in rec[:3]) + "}\nprint(<<vstock>>[\"<<n1_lower>>\"])\n",
          "<<vstock>> = {" + ", ".join(f'"{r[0]}": {r[1]}' for r in rec[:3]) + "}\nprint(<<vstock>>[\"<<n1>>\"])\n",
          ["The error shows the key Python looked for. Compare it with the keys in the dictionary.", "Spell the key exactly as it appears in the dictionary."])
    drill("eq", "equality", "SyntaxError", "One equals sign too few",
          "The check on the count never runs. Python points at the `if` line. **SyntaxError: invalid syntax** here usually means `=` (store a value) was written where `==` (compare) was meant.",
          "units = <<q1>>\nif units = <<q1>>:\n    print(\"match\")\n", "units = <<q1>>\nif units == <<q1>>:\n    print(\"match\")\n",
          ["A single = stores a value. Which sign compares two values?", "Change the = in the if line to =="])
    drill("boundary", "greater_less", "Wrong answer", "The boundary that slips through",
          "The rule says a count of <<level>> **or fewer** is LOW, but a count of exactly <<level>> is reported OK. No error: silent bugs love boundaries.",
          "count = <<level>>\nif count < <<level>>:\n    print(\"LOW\")\nelse:\n    print(\"OK\")\n", "count = <<level>>\nif count <= <<level>>:\n    print(\"LOW\")\nelse:\n    print(\"OK\")\n",
          ["Which comparison also accepts equal values?", "Use <= instead of <."])
    drill("alias", "copying_lists", "Wrong answer", "The backup that changed",
          "The backup list shows the new value too. Nothing crashed: assignment **shares** a list instead of copying it.",
          "original = <<qlist>>\nbackup = original\noriginal[0] = 0\nprint(backup)\n", "original = <<qlist>>\nbackup = original.copy()\noriginal[0] = 0\nprint(backup)\n",
          ["backup and original are the same list. How do you make a separate one?", "Use original.copy()."])
    return drills
