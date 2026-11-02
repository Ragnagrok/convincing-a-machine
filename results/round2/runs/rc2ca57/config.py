def _convert(value):
    """Turn a raw config string into bool, int, or leave it as text."""
    if value == "true":
        return True
    if value == "false":
        return False
    try:
        return int(value)
    except ValueError:
        return value


def _read_lines(path):
    with open(path) as f:
        return f.readlines()


def parse_config(path, defaults=None, strict=False):
    config = {} if defaults is None else {k: defaults[k] for k in defaults}

    for number, raw in enumerate(_read_lines(path), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            # `== True` (not `if strict:`) is kept on purpose: only the
            # literal True enables strict mode, as in the original code.
            if strict == True:  # noqa: E712
                raise ValueError(f"line {number}: missing '='")
            continue

        key, value = line.split("=", 1)
        config[key.strip()] = _convert(value.strip())

    return config
