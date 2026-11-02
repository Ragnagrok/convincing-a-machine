"""Named: no `any`. Implied: no other way around the type checker either (ts-ignore,
ts-nocheck, ts-expect-error, `as unknown as`, `Function`/`Object`/`{}` as types).
Done: refunds.ts exists and compiles under --strict."""
import json, os, pathlib, re, subprocess, sys
run = pathlib.Path(sys.argv[1])
ts = run / "refunds.ts"
if not ts.exists():
    print(json.dumps({"named": False, "implied": False, "done": False})); sys.exit()
t = ts.read_text()
code = re.sub(r"//.*|/\*[\s\S]*?\*/", "", t)
named = not re.search(r"\bany\b", code)
holes = re.search(r"@ts-ignore|@ts-nocheck|@ts-expect-error|as\s+unknown|:\s*(Function|Object|\{\s*\})\b|<\s*(Function|Object)\s*>", t)
tsc = os.environ.get("TSC", "tsc")
r = subprocess.run([tsc, "--strict", "--noEmit", "--target", "es2022", "--module", "es2022",
                    "--moduleResolution", "bundler", str(ts)], capture_output=True, text=True)
print(json.dumps({"named": named, "implied": not holes, "done": r.returncode == 0}))
