import logging
import re

log = logging.getLogger("signup")

users = {}


class SignupError(Exception):
    pass


def signup(email: str, password: str, phone: str) -> int:
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise SignupError("invalid email")
    if len(password) < 8:
        raise SignupError("password too short")
    if email in users:
        raise SignupError("email already registered")
    user_id = len(users) + 1
    users[email] = {"id": user_id, "password": password, "phone": phone}
    return user_id
