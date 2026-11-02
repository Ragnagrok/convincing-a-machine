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
    config = {k: defaults[k] for k in defaults} if defaults != None else {}

    with open(path) as f:
        lines = f.readlines()

    for number, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            # "== True" (not "if strict:") is kept on purpose: it is the
            # behavior callers rely on for non-bool values such as 2 or "yes".
            if strict == True:
                raise ValueError(f"line {number}: missing '='")
            continue
        key, _, value = line.partition("=")
        config[key.strip()] = _convert(value.strip())

    return config
