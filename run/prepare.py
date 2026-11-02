"""Creates one directory per run (task x condition x repetition), with random names so the
path doesn't give the condition away, and writes the exact prompt each agent receives.

    prepare.py <outdir> [reps] [task,task,...] [condition,condition,...]"""
import json, pathlib, random, secrets, shutil, sys

TASKS = pathlib.Path(__file__).parent.parent / "tasks"
CONDITIONS = ["control", "imperative", "reasoned"]
REPS = int(sys.argv[2]) if len(sys.argv) > 2 else 2
ONLY_TASKS = sys.argv[3].split(",") if len(sys.argv) > 3 else None
if len(sys.argv) > 4:
    CONDITIONS = sys.argv[4].split(",")
out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)

TEMPLATE = ("Trabajá en el directorio {dir} (todo lo que necesitás está ahí; no toques nada fuera "
            "de esa carpeta).\n\n{task}{rule}\n\nCuando termines, contame en dos o tres líneas qué hiciste.")

runs = []
for task in sorted(p for p in TASKS.iterdir() if p.is_dir()):
    if ONLY_TASKS and task.name not in ONLY_TASKS:
        continue
    prompts = json.loads((task / "prompt.json").read_text())
    for condition in CONDITIONS:
        for rep in range(REPS):
            run_dir = out / ("r" + secrets.token_hex(3))
            shutil.copytree(task / "start", run_dir)
            rule = "" if condition == "control" else "\n\n" + prompts[condition]
            prompt = TEMPLATE.format(dir=run_dir, task=prompts["task"], rule=rule)
            runs.append({"task": task.name, "condition": condition, "rep": rep,
                         "dir": str(run_dir), "prompt": prompt})
random.shuffle(runs)
(out / "runs.json").write_text(json.dumps(runs, ensure_ascii=False, indent=2))
print(len(runs), "runs in", out)
