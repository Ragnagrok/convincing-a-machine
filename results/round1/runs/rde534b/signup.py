import logging
import re

log = logging.getLogger("signup")

users = {}


class SignupError(Exception):
    pass


def _reject(reason: str) -> SignupError:
    log.warning("signup failed: %s", reason)
    return SignupError(reason)


def signup(email: str, password: str, phone: str) -> int:
    # Never log the email, password or phone: they are personal data.
    log.info("signup attempt started")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise _reject("invalid email")
    if len(password) < 8:
        raise _reject("password too short")
    if email in users:
        raise _reject("email already registered")
    user_id = len(users) + 1
    users[email] = {"id": user_id, "password": password, "phone": phone}
    log.info("signup succeeded: user_id=%d", user_id)
    return user_id
