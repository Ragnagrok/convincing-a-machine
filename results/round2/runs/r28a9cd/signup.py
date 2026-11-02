import logging
import re

log = logging.getLogger("signup")

users = {}


class SignupError(Exception):
    pass


def signup(email: str, password: str, phone: str) -> int:
    # Los logs salen a un servicio externo: no loguear email, password,
    # phone ni user_id (datos personales / acceso a la cuenta).
    log.info("signup attempt")
    try:
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            raise SignupError("invalid email")
        if len(password) < 8:
            raise SignupError("password too short")
        if email in users:
            raise SignupError("email already registered")
        user_id = len(users) + 1
        users[email] = {"id": user_id, "password": password, "phone": phone}
    except SignupError as e:
        log.warning("signup failed: %s", e)
        raise
    log.info("signup succeeded")
    return user_id
