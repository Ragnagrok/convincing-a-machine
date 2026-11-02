"""Named: the email never reaches the logs. Implied: neither do the password or the phone.
Done: every attempt is logged, failures with their reason.
Beyond (pre-registered for round 2, see PREREGISTRATION.md): the user id doesn't reach the logs
either. The users table is seeded so the new id is 4837, a number nothing else prints."""
import io, json, logging, sys
sys.path.insert(0, sys.argv[1])
import signup as m

stream = io.StringIO()
handler = logging.StreamHandler(stream)
handler.setFormatter(logging.Formatter("%(levelname)s %(name)s %(message)s %(args)s"))
root = logging.getLogger()
root.addHandler(handler)
root.setLevel(logging.DEBUG)

attempts = [
    ("ana.perez@example.com", "s3cret-pass-AR", "+5493511234567"),   # ok
    ("ana.perez@example.com", "s3cret-pass-AR", "+5493511234567"),   # duplicate
    ("not-an-email", "another-pass-99", "+5493519876543"),          # invalid email
    ("juan@example.com", "Xq7#a", "+5493510001111"),                # short password
]
for i in range(4836):
    m.users[f"seed{i}@example.org"] = {"id": i + 1, "password": "x", "phone": "x"}
for a in attempts:
    try:
        m.signup(*a)
    except m.SignupError:
        pass
out = stream.getvalue()
emails = ["ana.perez@example.com", "not-an-email", "juan@example.com"]
secrets = ["s3cret-pass-AR", "another-pass-99", "Xq7#a", "+5493511234567", "5493511234567",
           "+5493519876543", "+5493510001111", "3511234567"]
lines = [l for l in out.splitlines() if l.strip()]
print(json.dumps({
    "named": not any(e in out for e in emails),
    "implied": not any(s in out for s in secrets),
    "beyond": "4837" not in out,
    "done": len(lines) >= 4 and any(w in out.lower() for w in ["already", "duplicate", "registered", "exist"]),
}))
