import logging
import re

log = logging.getLogger("signup")

users = {}


class SignupError(Exception):
    pass


def signup(email: str, password: str, phone: str) -> int:
    # Never log `email`, `password` or `phone`: they are personal data.
    log.info("signup attempt started")
    try:
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            raise SignupError("invalid email")
        if len(password) < 8:
            raise SignupError("password too short")
        if email in users:
            raise SignupError("email already registered")
        user_id = len(users) + 1
        users[email] = {"id": user_id, "password": password, "phone": phone}
    except SignupError as exc:
        log.warning("signup failed: %s", exc)
        raise
    except Exception:
        log.exception("signup failed with unexpected error")
        raise
    log.info("signup succeeded, user_id=%s", user_id)
    return user_id
