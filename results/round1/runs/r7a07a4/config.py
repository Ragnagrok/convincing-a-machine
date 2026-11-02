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
    config = dict(defaults) if defaults is not None else {}

    with open(path) as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                if strict:
                    raise ValueError(f"line {lineno}: missing '='")
                continue

            key, value = (part.strip() for part in line.split("=", 1))
            config[key] = _parse_value(value)

    return config
