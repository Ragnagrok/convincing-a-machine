def parse_config(path, defaults=None, strict=False):
    d = {}
    if defaults != None:
        for k in defaults:
            d[k] = defaults[k]
    f = open(path)
    lines = f.readlines()
    f.close()
    n = 0
    for line in lines:
        n = n + 1
        line = line.strip()
        if line == "" or line[0] == "#":
            continue
        if not "=" in line:
            if strict == True:
                raise ValueError("line " + str(n) + ": missing '='")
            else:
                continue
        parts = line.split("=", 1)
        key = parts[0].strip()
        value = parts[1].strip()
        if value == "true":
            value = True
        elif value == "false":
            value = False
        else:
            try:
                value = int(value)
            except:
                pass
        d[key] = value
    return d
