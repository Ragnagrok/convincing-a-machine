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

    for number, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            if strict == True:
                raise ValueError("line " + str(number) + ": missing '='")
            continue

        key, value = (part.strip() for part in line.split("=", 1))
        config[key] = _convert(value)

    return config
