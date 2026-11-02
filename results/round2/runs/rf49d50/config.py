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
        lines = f.readlines()

    for number, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            if strict:
                raise ValueError(f"line {number}: missing '='")
            continue

        key, raw_value = line.split("=", 1)
        config[key.strip()] = _parse_value(raw_value.strip())

    return config
