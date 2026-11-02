def parse_config(path, defaults=None, strict=False):
    config = {} if defaults is None else {key: defaults[key] for key in defaults}

    with open(path) as f:
        for lineno, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                # Se compara con == (no con truthiness) para mantener el
                # comportamiento original con valores no booleanos.
                if strict == True:  # noqa: E712
                    raise ValueError(f"line {lineno}: missing '='")
                continue

            key, _, value = line.partition("=")
            config[key.strip()] = _parse_value(value.strip())

    return config


def _parse_value(text):
    if text == "true":
        return True
    if text == "false":
        return False
    try:
        return int(text)
    except ValueError:
        return text
