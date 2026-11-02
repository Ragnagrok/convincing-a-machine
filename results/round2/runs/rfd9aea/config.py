def _convert(value):
    if value == "true":
        return True
    if value == "false":
        return False
    try:
        return int(value)
    except ValueError:
        return value


def parse_config(path, defaults=None, strict=False):
    config = dict(defaults) if defaults is not None else {}

    with open(path) as f:
        for number, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                if strict:
                    raise ValueError(f"line {number}: missing '='")
                continue

            key, value = (part.strip() for part in line.split("=", 1))
            config[key] = _convert(value)

    return config
