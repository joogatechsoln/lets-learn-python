# Let's Learn Python

An offline, single-screen Python course. You pick an industry, and every lesson is a small scenario from that work, in
that trade's own words. Each lesson adds code to one growing program, shown as a live 3D world that reacts to the code
you run. Finish all 161 lessons and you have a working system, the skills of a confident Python programmer, and a
certificate.

## Install and run

Any of these. All need Python 3.8+ and a browser with WebGL (recent Chrome, Edge or Firefox). No internet, no AI.

- **Straight from the folder**: `./run.sh` (or `python3 server.py`), then open http://127.0.0.1:8765
- **Debian, Ubuntu, Mint**: `sudo apt install ./dist/lets-learn-python_1.0.0_all.deb`. It adds "Let's Learn Python" to your
  applications menu. Build it yourself with `./packaging/build_deb.sh`.
- **No root**: `./packaging/install.sh` installs for your user only (`--remove` to undo).
- **One file**: `./packaging/build_appimage.sh` builds an AppImage (needs `appimagetool`).

Progress is saved in `~/.letslearnpython`. Set `LLP_HOME` to store it elsewhere and `PORT` to change the port. When started
from the menu, the app stops a few minutes after you close the browser tab.

## What is in it

- **10 industries**, each with its own project, vocabulary, rule and 3D world: Retail, Pharmacy, Logistics, Farming,
  Networking (Packet Tracer style), Support desk, Applied AI, Hospitality, Banking and Education.
- **161 lessons in 12 chapters**: Introduction to Python, Variables and data types, Functions, Scope, Unit testing,
  Computing, Comparisons, Loops, Lists, Dictionaries, Sets and Errors. Every lesson has a scenario, teaching slides with
  worked examples, a predict-the-output or quiz question, and a hands-on task with live checks.
- **Graduation**: finishing chapter 12 completes the course. You get a printable certificate (profile menu, "View
  certificate"), the Graduate rank, and the Playground stays open for your own projects.
- **Live 3D preview**: starts as a translucent blue blueprint and fills in as your code creates things. Output lines
  trigger animations, errors turn the scene red. Drag to orbit, scroll to zoom, double-click to reset, expand for a bigger
  window. **Click any object** to open the Inspector: it shows the values and the Python behind it.
  With **Auto-run** on, the preview re-runs a moment after you stop typing.
- **Playground** (opens after chapter 1): free coding that runs after everything you have finished. `input()` works: type
  the answers in the **Input** box under the terminal. Templates cover CSV, JSON, logs and missing files.
- **Workspace**: the folder your programs can read and write with `open()`. It starts with `records.csv`,
  `settings.json` and `notes.txt` made from your industry's data.
- **Bug Lab**: eleven drills (seven error types and four silent logic bugs), each unlocking after the lesson that teaches
  what it needs.
- **Review**: old quiz and prediction questions return after 1, 3, 7, 14 and 30 days, just before you forget them.
- **Error explainer**: the terminal explains the error type in plain words and marks the failing line.
- **Guide tab** (the trade's vocabulary) and **Compare industries** (the same lesson solved in every other industry).
- XP, ranks, a day streak, themes (light and dark), and a module board.
- **Mentor view** (profile menu): merge the progress reports of several learners into one table and a CSV. It runs in
  the browser, so nothing leaves the computer.

## Safety

Learner code runs in a separate process. It always has CPU, memory and file-size limits, and network access and system
commands are switched off inside Python (a safeguard for learners, not a security boundary). If **bubblewrap** is
installed (`sudo apt install bubblewrap`) and passes a start-up self-test, the code also runs with no network, a
read-only system and write access to the workspace only. The chip at the top of the terminal shows which mode is active.
Set `LLP_SANDBOX=off` to disable bubblewrap.

## 3D engine

A small built-in WebGL engine (`static/mini3d.js`) is used by default. For real three.js, put a valid `three.min.js` (r128)
in `static/vendor/` and follow `static/vendor/README-three.txt`. The label at the bottom of the 3D view says which engine
is running, and if three.js fails the app switches back by itself. Shadows and clicking work in both.

## Add or change content

- **New industry**: copy `packs/retail.json`, change the values, save it as `packs/<yourname>.json`. All 161 lessons and
  11 drills fill in automatically. See `packs/README.md` for every field. The pack's optional `world` field picks one of
  the built-in 3D worlds (default `retail`).
- **Change a lesson**: chapters live in `lessons_ch1.py` to `lessons_ch12.py`.
- Check types: `stdout_equals`, `stdout_last`, `stdout_has`, `var_equals`, `var_absent`, `func_tests`, `func_output`,
  `func_doc`, `ast_has`, `ast_count`, `source_count`, `expr_equals`, `expr_raises`, `unit_class`, `unit_catches`.
- After any edit run `python3 validate.py` (several minutes for ten industries; pass industry names to check just some).

## Upgrading from an older version

The course layout changed, so old progress cannot be reused. On first start the old save is copied to `state.v<N>.json`
and your name and industry are kept.
