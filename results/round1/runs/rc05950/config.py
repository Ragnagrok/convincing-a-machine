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
    config = {k: defaults[k] for k in defaults} if defaults is not None else {}

    with open(path) as f:
        lines = f.readlines()

    for number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            if strict == True:
                raise ValueError(f"line {number}: missing '='")
            continue

        key, _, value = line.partition("=")
        config[key.strip()] = _parse_value(value.strip())

    return config
