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
    config = dict(defaults or {})
    with open(path) as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                if strict:
                    raise ValueError(f"line {line_no}: missing '='")
                continue
            key, raw_value = line.split("=", 1)
            config[key.strip()] = _parse_value(raw_value.strip())
    return config
