import logging
import re

log = logging.getLogger("signup")

users = {}


class SignupError(Exception):
    pass


def signup(email: str, password: str, phone: str) -> int:
    # Los logs van a un servicio externo: no registrar email, password,
    # teléfono ni id de usuario, sólo el resultado y el motivo.
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
        log.warning("signup failed: reason=%s", e)
        raise
    except Exception as e:
        log.error("signup failed: reason=unexpected_error type=%s", type(e).__name__)
        raise
    log.info("signup succeeded")
    return user_id
