def _parse_value(raw):
    """Convert a raw string into True, False, an int, or leave it as str."""
    if raw == "true":
        return True
    if raw == "false":
        return False
    try:
        return int(raw)
    except ValueError:
        return raw


def _iter_entries(lines, strict):
    """Yield (key, raw_value) pairs for each meaningful line.

    Blank lines and comments are skipped. Lines without '=' raise ValueError
    when strict is set, otherwise they are skipped.
    """
    for number, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            if strict:
                raise ValueError(f"line {number}: missing '='")
            continue
        key, raw_value = line.split("=", 1)
        yield key.strip(), raw_value.strip()


def parse_config(path, defaults=None, strict=False):
    config = dict(defaults) if defaults is not None else {}

    with open(path) as f:
        lines = f.readlines()

    for key, raw_value in _iter_entries(lines, strict):
        config[key] = _parse_value(raw_value)

    return config
