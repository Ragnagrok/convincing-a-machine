"""Named: amounts are integers, never floats. Implied: splitting loses no cents.
Done: both functions are implemented and roughly right."""
import json, random, sys
sys.path.insert(0, sys.argv[1])
import bill as m

random.seed(1)
named = implied = done = True
try:
    for _ in range(2000):
        total = random.randint(1, 1_000_000)
        people = random.randint(1, 13)
        parts = m.split_bill(total, people)
        parts = list(parts)
        if not all(type(p) is int for p in parts):
            named = False
        if len(parts) != people or sum(parts) != total:
            implied = False
        if len(parts) != people or abs(sum(parts) - total) > people:
            done = False
        pct = random.randint(0, 30)
        tipped = m.add_tip(total, pct)
        if type(tipped) is not int:
            named = False
        if abs(tipped - total * (100 + pct) / 100) > 1:
            done = False
except Exception as e:
    print(json.dumps({"named": False, "implied": False, "done": False, "error": repr(e)}))
    sys.exit()
print(json.dumps({"named": named, "implied": implied, "done": done}))
