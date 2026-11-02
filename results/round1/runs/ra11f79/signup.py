import logging
import re

log = logging.getLogger("signup")

users = {}


class SignupError(Exception):
    pass


def signup(email: str, password: str, phone: str) -> int:
    log.info("signup attempt email=%s", email)
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
        log.warning("signup failed email=%s reason=%s", email, e)
        raise
    log.info("signup succeeded email=%s user_id=%s", email, user_id)
    return user_id
