"""Runs learner code in a separate process and grades it.

Usage: python runner.py request.json result.json

The request holds earlier lesson files ("prior"), the current code, and the
checks for the lesson. Earlier lessons run silently so their variables and
functions exist, but only the current lesson's output reaches the terminal.
Not a hardened sandbox: code runs as your own user, so only run code you trust.
"""
import ast
import builtins
import contextlib
import io
import json
import linecache
import math
import re
import sys
import types
import traceback

try:
    import resource

    resource.setrlimit(resource.RLIMIT_AS, (1 << 30, 1 << 30))
except Exception:  # not on Linux, or limits unavailable
    pass


def norm(text):
    text = re.sub(r"in \d+\.\d+s", "in 0.000s", str(text))   # unittest prints how long the run took
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def purge_tests(g):
    """Test classes from earlier lessons are dropped so each lesson's test run only shows its own tests."""
    import unittest
    for k, v in list(g.items()):
        if isinstance(v, type) and issubclass(v, unittest.TestCase) and v.__module__ == "__main__":
            del g[k]


def run_class(g, name):
    """Runs one unittest.TestCase class quietly. Returns (tests run, failures + errors) or None if it is missing."""
    import unittest
    cls = g.get(name)
    if not (isinstance(cls, type) and issubclass(cls, unittest.TestCase)):
        return None
    res = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    return res.testsRun, len(res.failures) + len(res.errors)


def simple(v, depth=0):
    """Makes a value safe to send to the browser, or returns the marker NO."""
    if v is None or isinstance(v, (bool, int, str)):
        return v if not isinstance(v, str) else v[:300]
    if isinstance(v, float):
        return v if math.isfinite(v) else str(v)
    if depth < 2 and isinstance(v, (list, tuple, set)) and len(v) <= 60:
        items = [simple(x, depth + 1) for x in v]
        return NO if any(i is NO for i in items) else items
    if depth < 2 and isinstance(v, dict) and len(v) <= 60 and all(isinstance(k, (str, int)) for k in v):
        items = {str(k): simple(x, depth + 1) for k, x in v.items()}
        return NO if any(i is NO for i in items.values()) else items
    return NO


NO = object()


def snapshot(g):
    """A JSON-safe picture of the program's variables, functions and classes (drives the 3D preview)."""
    out, funcs, classes = {}, [], []
    for k, v in list(g.items()):
        if k.startswith("__"):
            continue
        if isinstance(v, types.FunctionType) and v.__module__ == "__main__":
            funcs.append(k)
        elif isinstance(v, type) and v.__module__ == "__main__":
            classes.append(k)
        elif isinstance(v, (types.ModuleType, types.BuiltinFunctionType)):
            continue
        else:
            sv = simple(v)
            if sv is NO and hasattr(v, "__dict__") and type(v).__module__ == "__main__":
                attrs = {a: simple(x) for a, x in vars(v).items()}
                sv = {"__class__": type(v).__name__, **{a: x for a, x in attrs.items() if x is not NO}}
            if sv is not NO:
                out[k] = sv
    return {"vars": out, "functions": funcs, "classes": classes}


def format_error(exc, names):
    frames = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename in names]
    lines = []
    if frames:
        lines.append("Traceback (most recent call last):\n")
        lines += traceback.format_list(frames)
    lines += traceback.format_exception_only(type(exc), exc)
    return "".join(lines).rstrip()


def grade(checks, g, out, code):
    results = []
    for c in checks:
        kind, label = c["type"], c["label"]
        ok, detail = False, ""
        try:
            if kind == "stdout_equals":
                ok = norm(out) == norm(c["value"])
                if not ok:
                    detail = "Expected:\n" + norm(c["value"]) + "\n\nGot:\n" + (norm(out) or "(nothing printed)")
            elif kind == "var_equals":
                name = c["name"]
                if name not in g:
                    detail = f"`{name}` is not defined yet."
                else:
                    want, got = c["value"], g[name]
                    if isinstance(got, tuple) and isinstance(want, list):
                        want = tuple(want)
                    elif isinstance(got, (set, frozenset)) and isinstance(want, list):
                        want = type(got)(want)
                    ok = got == want and (not c.get("strict") or type(got) is type(want))
                    if not ok:
                        detail = f"`{name}` is {got!r} ({type(got).__name__}), expected {want!r} ({type(want).__name__})."
            elif kind == "stdout_has":
                ok = norm(c["value"]) in norm(out)
                if not ok:
                    detail = f"The output should contain: {c['value']}"
            elif kind == "var_absent":
                ok = c["name"] not in g
                if not ok:
                    detail = f"`{c['name']}` should not exist any more."
            elif kind == "stdout_last":
                lines = [x for x in norm(out).splitlines() if x.strip()]
                ok = bool(lines) and lines[-1] == norm(c["value"])
                if not ok:
                    detail = f"The last line should be: {norm(c['value'])}"
            elif kind == "source_count":
                n = len(re.findall(c["pattern"], code, re.M))
                ok = n >= c["min"]
                if not ok:
                    detail = f"Found {n}, need at least {c['min']}."
            elif kind == "ast_count":
                tree = ast.parse(code)
                if c.get("func"):
                    n = sum(1 for x in ast.walk(tree) if isinstance(x, ast.Call) and isinstance(x.func, ast.Name) and x.func.id == c["func"])
                else:
                    n = sum(1 for x in ast.walk(tree) if isinstance(x, getattr(ast, c["node"])))
                ok = n >= c["min"]
                if not ok:
                    detail = f"Found {n}, need at least {c['min']}."
            elif kind == "func_tests":
                fn = g.get(c["name"])
                if not callable(fn):
                    detail = f"`{c['name']}` is not a function yet."
                else:
                    ok = True
                    for args, expected in c["tests"]:
                        got = fn(*args)
                        if isinstance(got, tuple):
                            got = list(got)
                        if got != expected:
                            ok = False
                            shown = ", ".join(repr(a) for a in args)
                            detail = f"{c['name']}({shown}) returned {got!r}, expected {expected!r}."
                            break
            elif kind == "func_output":
                fn = g.get(c["name"])
                if not callable(fn):
                    detail = f"`{c['name']}` is not a function yet."
                else:
                    sink = io.StringIO()
                    with contextlib.redirect_stdout(sink):
                        fn(*c.get("args", []))
                    ok = norm(sink.getvalue()) == norm(c["value"])
                    if not ok:
                        shown = ", ".join(repr(a) for a in c.get("args", []))
                        detail = f"{c['name']}({shown}) printed {norm(sink.getvalue())!r}, expected {norm(c['value'])!r}."
            elif kind == "unit_class":
                r = run_class(g, c["name"])
                if r is None:
                    detail = f"`{c['name']}` is not a unittest.TestCase class yet."
                else:
                    ran, bad = r
                    ok = ran >= c.get("min_tests", 1) and (bad == 0 if c.get("all_pass", True) else bad > 0)
                    if not ok:
                        detail = f"{c['name']} ran {ran} test(s) with {bad} failing; needs at least {c.get('min_tests', 1)} and " + ("all passing." if c.get("all_pass", True) else "at least one failing.")
            elif kind == "unit_catches":
                # The learner's tests must FAIL when the function is replaced by each broken version.
                caught = []
                for src in c["bad"]:
                    scratch = {"__builtins__": builtins, "__name__": "__main__"}
                    exec(compile(src, "<bad>", "exec"), scratch)
                    saved = {k: g[k] for k in scratch if k in g and not k.startswith("__")}
                    g.update({k: v for k, v in scratch.items() if not k.startswith("__")})   # the tests look names up in g
                    try:
                        r = run_class(g, c["name"])
                    finally:
                        g.update(saved)
                    caught.append(bool(r and r[1] > 0))
                ok = all(caught)
                if not ok:
                    detail = f"Your tests did not catch {caught.count(False)} of {len(caught)} broken version(s) of the function. Add tests that would fail on them."
            elif kind == "func_doc":
                fn = g.get(c["name"])
                doc = getattr(fn, "__doc__", None) if callable(fn) else None
                ok = bool(doc and len(doc.strip()) >= c.get("min", 20))
                if not ok:
                    detail = f"`{c['name']}` needs a docstring of at least {c.get('min', 20)} characters, as its first line."
            elif kind == "expr_equals":
                got = eval(c["expr"], g)
                ok = got == c["value"] and type(got) is type(c["value"])
                if not ok:
                    detail = f"{c['expr']} gave {got!r}, expected {c['value']!r}."
            elif kind == "expr_raises":
                try:
                    eval(c["expr"], g)
                    detail = f"{c['expr']} should raise {c['exc']} but it did not."
                except BaseException as e:
                    ok = type(e).__name__ == c["exc"]
                    if not ok:
                        detail = f"Expected {c['exc']} but got {type(e).__name__}."
            elif kind == "ast_has":
                node = getattr(ast, c["node"])
                ok = any(isinstance(n, node) for n in ast.walk(ast.parse(code)))
                if not ok:
                    detail = f"Your code needs {c.get('what', c['node'])}."
        except Exception as e:  # a failing test call is a failed check, not a crash
            detail = f"{type(e).__name__}: {e}"
        results.append({"ok": ok, "label": label, "detail": detail})
    return results


def lock_down():
    """Switches off network access and system commands inside the learner's Python. A teaching safeguard, not a security boundary."""
    import os
    import socket
    import subprocess

    def blocked(*args, **kwargs):
        raise PermissionError("Network access and system commands are switched off in this course.")

    for mod, names in ((socket, ["socket", "create_connection", "getaddrinfo", "gethostbyname"]),
                       (subprocess, ["Popen", "run", "call", "check_call", "check_output"]),
                       (os, ["system", "popen", "fork", "execv", "execve", "execl", "execlp", "execvp", "kill", "spawnl", "spawnv"])):
        for n in names:
            if hasattr(mod, n):
                setattr(mod, n, blocked)


def install_input(text):
    """input() reads from the lines typed in the Input box and echoes them like a terminal."""
    lines = str(text or "").splitlines()

    def fake_input(prompt=""):
        print(prompt, end="")
        if not lines:
            raise EOFError("input() was called but there is no more input. Type your input lines in the Input box under the terminal, one line for each input() call.")
        value = lines.pop(0)
        print(value)
        return value

    builtins.input = fake_input
    sys.stdin = io.StringIO("\n".join(str(text or "").splitlines()) + "\n")


def main():
    with open(sys.argv[1]) as fh:
        req = json.load(fh)
    try:
        cpu = int(req.get("cpu", 5))
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))
        resource.setrlimit(resource.RLIMIT_FSIZE, (5_000_000, 5_000_000))
    except Exception:
        pass
    lock_down()
    install_input(req.get("stdin", ""))
    mod = types.ModuleType("__main__")      # a real module, so unittest.main() can find the learner's tests
    g = mod.__dict__
    g["__builtins__"] = builtins
    sys.modules["__main__"] = mod
    cap, names = io.StringIO(), set()
    result = {"stdout": "", "error": None, "checks": [], "passed": False}
    build = req["mode"] in ("build", "preview")

    def run_source(name, src, show):
        names.add(name)
        linecache.cache[name] = (len(src), None, src.splitlines(True), name)
        sink = cap if show else io.StringIO()
        with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
            exec(compile(src, name, "exec"), g)

    try:
        for name, src in req["prior"]:
            run_source(name, src, build)
            purge_tests(g)
        if not build:
            run_source(req["name"], req["code"], True)
    except SystemExit:
        pass
    except BaseException as exc:
        result["error"] = format_error(exc, names)

    result["stdout"] = cap.getvalue()
    result["snapshot"] = snapshot(g)
    if not build and result["error"] is None:
        result["checks"] = grade(req["checks"], g, result["stdout"], req["code"])
        result["passed"] = all(c["ok"] for c in result["checks"])
    with open(sys.argv[2], "w") as fh:
        json.dump(result, fh)


if __name__ == "__main__":
    main()
