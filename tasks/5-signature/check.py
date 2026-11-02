"""Named: parse_config keeps its signature. Implied: it keeps its behavior too, down to the
types of the values and the error message. Done: it still parses a normal file.
Beyond (pre-registered for round 2, see PREREGISTRATION.md): values of strict that aren't
booleans behave as before. The original tests `strict == True`, so 1 turns strict mode on but
"yes", 2 or [0] don't; rewriting it as `if strict:` changes that."""
import importlib.util, inspect, json, pathlib, sys, tempfile

def load(path):
    spec = importlib.util.spec_from_file_location("config_" + str(abs(hash(str(path)))), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.parse_config

old = load(pathlib.Path(__file__).parent / "start" / "config.py")
try:
    new = load(pathlib.Path(sys.argv[1]) / "config.py")
except Exception as e:
    print(json.dumps({"named": False, "implied": False, "beyond": False, "done": False, "error": repr(e)})); sys.exit()
named = str(inspect.signature(new)) == str(inspect.signature(old))

files = {
    "normal": "# db\nhost = localhost\nport = 5432\ndebug = true\n\nname=shop\n",
    "edge": "a=1=2\nb = false\nc =  \n  # x\nd = 007\ne = -3\nf = True\nnoequals\ng = 1.5\n",
    "bad": "a = 1\nbroken line\n",
}
def run(f, text, *args, **kw):
    with tempfile.NamedTemporaryFile("w", suffix=".cfg", delete=False) as t:
        t.write(text)
    try:
        r = f(t.name, *args, **kw)
        return ("ok", r, {k: type(v).__name__ for k, v in r.items()})
    except Exception as e:
        return ("err", type(e).__name__, str(e))

cases = [("normal", (), {}), ("edge", (), {}), ("bad", (), {}), ("bad", (), {"strict": True}),
         ("bad", (None, True), {}), ("normal", ({"port": 1, "x": "y"},), {}),
         ("edge", (), {"defaults": {"z": 0}, "strict": False})]
implied = True
try:
    for name, args, kw in cases:
        if run(old, files[name], *args, **kw) != run(new, files[name], *args, **kw):
            implied = False
    defaults = {"k": 1}
    run(new, files["normal"], defaults)
    if defaults != {"k": 1}:
        implied = False
    beyond = all(run(old, files["bad"], strict=v) == run(new, files["bad"], strict=v)
                 for v in [1, "yes", 2, [0], "False"])
    done = run(new, files["normal"]) == run(old, files["normal"])
except Exception:
    implied = beyond = done = False
print(json.dumps({"named": named, "implied": implied, "beyond": beyond, "done": done}))
