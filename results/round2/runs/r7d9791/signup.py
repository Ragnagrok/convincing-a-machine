import logging
import re

log = logging.getLogger("signup")

users = {}


class SignupError(Exception):
    pass


def signup(email: str, password: str, phone: str) -> int:
    # No loguear email, password ni phone: son datos personales y no pueden salir de la base.
    log.info("signup attempt")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        log.warning("signup failed: invalid email")
        raise SignupError("invalid email")
    if len(password) < 8:
        log.warning("signup failed: password too short")
        raise SignupError("password too short")
    if email in users:
        log.warning("signup failed: email already registered")
        raise SignupError("email already registered")
    user_id = len(users) + 1
    users[email] = {"id": user_id, "password": password, "phone": phone}
    log.info("signup succeeded")
    return user_id
