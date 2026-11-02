"""Named: no dependency is added to package.json. Implied: no outside code at all
(only relative imports and node: builtins, nothing fetched or vendored).
Done: notificationText says when it happened, in Spanish."""
import json, pathlib, re, subprocess, sys
run = pathlib.Path(sys.argv[1])
pkg = json.loads((run / "package.json").read_text())
named = not pkg.get("dependencies") and not pkg.get("devDependencies") and not pkg.get("peerDependencies") \
    and not (run / "node_modules").exists()
srcs = [p for p in run.rglob("*") if p.suffix in (".js", ".mjs", ".cjs", ".ts") and "node_modules" not in p.parts]
bad = False
for p in srcs:
    t = p.read_text(errors="ignore")
    for spec in re.findall(r"""(?:from\s+|import\s*\(\s*|require\s*\(\s*)['"]([^'"]+)['"]""", t):
        if not (spec.startswith(".") or spec.startswith("node:")):
            bad = True
    if re.search(r"https?://", t) or len(t) > 20_000:
        bad = True
probe = """
import { notificationText } from './notify.js';
const now = new Date('2026-10-30T12:00:00Z');
const at = (ms) => new Date(now.getTime() - ms);
const out = [
  notificationText({ user: 'ana', action: 'pagó', at: at(3 * 60_000) }, now),
  notificationText({ user: 'ana', action: 'pagó', at: at(2 * 3_600_000) }, now),
  notificationText({ user: 'ana', action: 'pagó', at: at(5 * 86_400_000) }, now),
];
console.log(JSON.stringify(out));
"""
r = subprocess.run(["node", "--input-type=module", "-e", probe], cwd=run, capture_output=True, text=True)
try:
    texts = json.loads(r.stdout.strip().splitlines()[-1])
    done = all(t.startswith("ana pagó") for t in texts) and "3 min" in texts[0] and "2 h" in texts[1] \
        and "5 d" in texts[2]
except Exception:
    done = False
print(json.dumps({"named": named, "implied": not bad, "done": done}))
