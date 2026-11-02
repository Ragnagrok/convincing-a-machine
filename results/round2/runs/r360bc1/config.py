def _convert_value(text):
    """Convert a raw config value: 'true'/'false' become bools, integers
    become int, anything else stays as the original string."""
    if text == "true":
        return True
    if text == "false":
        return False
    try:
        return int(text)
    except ValueError:
        return text


def parse_config(path, defaults=None, strict=False):
    """Parse a simple ``key = value`` file into a dict.

    Blank lines and lines starting with ``#`` are skipped. Lines without
    ``=`` raise ValueError when ``strict`` is True and are ignored otherwise.
    ``defaults`` seeds the result; file values override it.
    """
    config = {} if defaults is None else {k: defaults[k] for k in defaults}

    with open(path) as f:
        lines = f.readlines()

    for number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            # `strict == True` (not truthiness) is kept on purpose: it
            # preserves the original behavior for non-bool arguments.
            if strict == True:
                raise ValueError(f"line {number}: missing '='")
            continue

        key, value = line.split("=", 1)
        config[key.strip()] = _convert_value(value.strip())

    return config
