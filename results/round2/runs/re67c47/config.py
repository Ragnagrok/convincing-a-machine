def _parse_value(text):
    if text == "true":
        return True
    if text == "false":
        return False
    try:
        return int(text)
    except ValueError:
        return text


def parse_config(path, defaults=None, strict=False):
    config = {} if defaults is None else {key: defaults[key] for key in defaults}

    with open(path) as f:
        lines = f.readlines()

    for lineno, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            # `== True` (not a truthiness test) is kept on purpose to preserve
            # the original behaviour for non-bool values of `strict`.
            if strict == True:  # noqa: E712
                raise ValueError(f"line {lineno}: missing '='")
            continue

        key, _, value = line.partition("=")
        config[key.strip()] = _parse_value(value.strip())

    return config
