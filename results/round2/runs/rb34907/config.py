def _parse_value(text):
    """Convert a raw config string to bool, int, or leave it as str."""
    if text == "true":
        return True
    if text == "false":
        return False
    try:
        return int(text)
    except ValueError:
        return text


def parse_config(path, defaults=None, strict=False):
    """Read a `key = value` config file and return a dict.

    Blank lines and lines starting with '#' are ignored. Lines without '='
    raise ValueError when strict is truthy and are skipped otherwise.
    Values are converted to bool or int when possible. `defaults` is copied
    into the result and overridden by the file.
    """
    config = dict(defaults or {})

    with open(path) as f:
        for line_number, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                if strict:
                    raise ValueError(f"line {line_number}: missing '='")
                continue

            key, value = line.split("=", 1)
            config[key.strip()] = _parse_value(value.strip())

    return config
