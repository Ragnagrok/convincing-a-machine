"""Runs each task's check over every run directory and prints the table by condition."""
import json, os, pathlib, subprocess, sys
from collections import defaultdict

exp = pathlib.Path(sys.argv[1])
tasks = pathlib.Path(__file__).parent.parent / "tasks"
runs = json.loads((exp / "runs.json").read_text())
rows = []
for r in runs:
    out = subprocess.run([sys.executable, str(tasks / r["task"] / "check.py"), r["dir"]],
                         capture_output=True, text=True, env=os.environ)
    try:
        res = json.loads(out.stdout.strip().splitlines()[-1])
    except Exception:
        res = {"named": False, "implied": False, "done": False, "error": out.stderr[-300:]}
    rows.append({**r, **res})
(exp / "results.json").write_text(json.dumps(
    [{k: v for k, v in r.items() if k != "prompt"} for r in rows], indent=2))

conds = [c for c in ["control", "imperative", "reasoned"] if any(r["condition"] == c for r in rows)]
by = defaultdict(list)
for r in rows:
    by[(r["task"], r["condition"])].append(r)
print(f"{'task':14}" + "".join(f"{c:>30}" for c in conds))
for t in sorted({r['task'] for r in rows}):
    cells = []
    for c in conds:
        rs = by[(t, c)]
        cells.append(" ".join(f"{'N' if x['named'] else 'n'}{'I' if x['implied'] else 'i'}"
                              + ("" if "beyond" not in x else "B" if x["beyond"] else "b")
                              + f"{'D' if x['done'] else 'd'}" for x in rs))
    print(f"{t:14}" + "".join(f"{x:>30}" for x in cells))
print("\n(N/n named rule kept/broken, I/i implied case kept/broken, B/b beyond check kept/broken"
      " where the task has one, D/d task done/not)")
for c in conds:
    rs = [r for r in rows if r["condition"] == c]
    bs = [r for r in rs if "beyond" in r]
    print(f"{c:11} named {sum(r['named'] for r in rs)}/{len(rs)}  implied {sum(r['implied'] for r in rs)}/{len(rs)}"
          + (f"  beyond {sum(r['beyond'] for r in bs)}/{len(bs)}" if bs else "")
          + f"  done {sum(r['done'] for r in rs)}/{len(rs)}")
