import logging
import re

log = logging.getLogger("signup")

users = {}


class SignupError(Exception):
    pass


def _fail(email: str, reason: str) -> SignupError:
    log.warning("signup failed email=%s reason=%s", email, reason)
    return SignupError(reason)


def signup(email: str, password: str, phone: str) -> int:
    # Password and phone are deliberately not logged.
    log.info("signup attempt email=%s", email)
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise _fail(email, "invalid email")
    if len(password) < 8:
        raise _fail(email, "password too short")
    if email in users:
        raise _fail(email, "email already registered")
    user_id = len(users) + 1
    users[email] = {"id": user_id, "password": password, "phone": phone}
    log.info("signup succeeded email=%s user_id=%d", email, user_id)
    return user_id
