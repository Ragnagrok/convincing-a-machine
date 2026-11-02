import logging
import re

log = logging.getLogger("signup")

users = {}


class SignupError(Exception):
    pass


def signup(email: str, password: str, phone: str) -> int:
    # Logs must not contain personal data (email, password, phone, user id).
    # Only the outcome and the failure reason are logged.
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
    except SignupError as exc:
        log.warning("signup failed: reason=%s", exc)
        raise
    except Exception as exc:
        # Log only the exception type: its message could contain input data.
        log.error("signup failed: unexpected error type=%s", type(exc).__name__)
        raise
    log.info("signup succeeded")
    return user_id
