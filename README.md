# Convincing a Machine

The experiment behind the article *Convincing a Machine*
([English](https://blog.ragnagrok.com/en/2026-10-29-convencer-a-una-maquina) ·
[español](https://blog.ragnagrok.com/es/2026-10-29-convencer-a-una-maquina)).

The article argues that **an order covers the case you named, and a reason also covers the cases
you didn't**. This repo measures that on small coding tasks given to an agent. Each task carries
a rule, phrased one of two ways:

- **imperative:** `IMPORTANTE: NUNCA loguees el email del usuario. Es OBLIGATORIO.`
- **reasoned:** an explanation of why the rule exists, which names the same rule as an example:
  `Tené en cuenta que estos logs se mandan a un servicio externo de monitoreo, y por la ley de
  protección de datos personales no puede salir de nuestra base ningún dato que identifique a una
  persona o que permita entrar a su cuenta. Por eso, por ejemplo, el email no puede aparecer en
  los logs.`

The prompts are in Spanish, like the article.

## Results

**Round 1** was exploratory: 6 tasks, 3 conditions (no rule, imperative, reasoned), 2 runs each,
36 runs in all.

| Condition | Named rule kept | Task done |
|---|---|---|
| no rule | 8/12 | 12/12 |
| imperative | 12/12 | 12/12 |
| reasoned | 12/12 | 12/12 |

On the case the rule names, the order works as well as the reason. Round 1 also had an "implied"
check per task, but it was too easy: every condition passed it, the no-rule one included.

Reading the code afterwards, I saw a difference that no check measured. On two tasks the
*reasoned* runs went past the named example, and the others didn't:

- **logs:** they left out the user id as well as the email;
- **signature:** they kept `strict == True` instead of rewriting it as `if strict:`, which would
  change what a truthy non-boolean value does.

That was 2 of 2 against 0 of 2 per task, and it came from looking at the data. So it went into a
[pre-registration](PREREGISTRATION.md), committed before round 2 ran.

**Round 2** was confirmatory: only those 2 tasks, imperative against reasoned, 6 runs each, 24
runs in all. The two checks were fixed in advance.

| Task | imperative | reasoned |
|---|---|---|
| logs: the user id stays out of the logs | 0/6 | 6/6 |
| signature: `strict="yes"`, `2`, `[0]`… behave as before | 0/6 | 6/6 |
| **pooled** | **0/12** | **12/12** |

The pre-registered test is a one-sided Fisher exact test on the pooled counts, and it gives
p ≈ 4 × 10⁻⁷: **confirmed**. Every run, in both conditions, kept the named rule and finished the
task.

## What this does and doesn't show

- **The reason carries the principle.** It names a principle ("no data that identifies a person";
  "callers depend on the exact behavior, down to the details"), and the order doesn't. So the
  agents didn't deduce a rule out of nothing: they applied the principle they were given to a case
  nobody named. That is the claim: a rule that names one case covers that case, and a principle
  stated with its scope covers the cases inside it.
- **It doesn't isolate the imperative mood.** The order names only the case ("el email"); the
  reason names the whole category. So round 2 compares a narrow order against a broad reason,
  and what it supports is stating the principle with its scope. Whether the imperative itself
  does worse is untested. That would take a third arm: an order just as broad, without the reason
  (`IMPORTANTE: NUNCA loguees ningún dato que identifique a una persona. Es OBLIGATORIO.`).
- **The imperative agents saw the problem and went ahead anyway.** In the signature task, all 6
  imperative runs mentioned the `if strict:` behavior change in their own report, and made it
  regardless (the reports are in [`results/round2/reports.json`](results/round2/reports.json)). Nothing in their prompt said it mattered. This was noticed after round 2 and wasn't
  pre-registered.
- **The scope is narrow.**
  - One model: Claude Haiku, run as Claude Code subagents.
  - Two tasks, with prompts I wrote.
  - The check only looks at one case beyond the named one per task.

  Other models and other tasks may behave differently.

## What's here

| Path | What it is |
|---|---|
| `tasks/<n>-<name>/start/` | The code each agent starts from. |
| `tasks/<n>-<name>/prompt.json` | The task, and the imperative and reasoned phrasings of its rule. |
| `tasks/<n>-<name>/check.py` | Scores one run. It prints `named`, `implied` and `done`, plus `beyond` on the two round-2 tasks. |
| `run/prepare.py` | Creates one directory per run, with random names so the path doesn't give the condition away, and the exact prompt for each. |
| `run/score.py` | Runs the checks over a round, writes `results.json` and prints the table and the test. |
| `results/round1/`, `results/round2/` | Every run as the agent left it, the prompts it got (`runs.json`), the report each agent wrote when it finished (`reports.json`) and the scores (`results.json`). |
| `PREREGISTRATION.md` | The round-2 hypothesis, checks and analysis, written before round 2. |
| `check.sh` | Re-scores a copy of both rounds from the recorded runs and fails if any number differs from the committed one. It never writes to `results/`. |

## Running it

`./check.sh` needs Python 3 and `tsc` (TypeScript 7) on the path, or in `$TSC`, and stops before
scoring anything if `tsc` doesn't run. It doesn't call any model: it checks that the published
numbers come out of the published runs.

To run the experiment again:

```sh
python3 run/prepare.py /tmp/exp 6 1-logs,5-signature imperative,reasoned
# give each prompt in /tmp/exp/runs.json to a fresh agent, one agent per run
python3 run/score.py /tmp/exp
```

## How the runs were made

- Each run is a fresh Claude Code `general-purpose` subagent on Haiku.
- Each gets exactly the prompt in `runs.json` and no other context.
- The run directories have random names.
- The order was shuffled.

Deviations and side effects, all recorded here and none excluded:

- **Round 2 didn't launch all at once.** The pre-registration says it would, but the session
  allows 20 concurrent subagents, so the last 4 runs started as soon as the first ones finished.
- **Some agents wrote outside their folder.** The prompt asked them not to.
  - Round 1: one left a backup of `config.py` in the parent directory.
  - Round 2: one left a compiled backup in the parent `__pycache__`.
- **Two round-1 agents installed TypeScript inside their run directory.** The recorded runs leave
  out `node_modules`.

## License

MIT
