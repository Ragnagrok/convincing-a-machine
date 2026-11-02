def _parse_value(raw):
    if raw == "true":
        return True
    if raw == "false":
        return False
    try:
        return int(raw)
    except ValueError:
        return raw


def parse_config(path, defaults=None, strict=False):
    config = {} if defaults is None else {k: defaults[k] for k in defaults}

    with open(path) as f:
        lines = f.readlines()

    for lineno, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            # `strict == True` (not `if strict`) is kept on purpose: only values
            # that compare equal to True enable strict mode, as before.
            if strict == True:
                raise ValueError(f"line {lineno}: missing '='")
            continue

        key, raw = line.split("=", 1)
        config[key.strip()] = _parse_value(raw.strip())

    return config
