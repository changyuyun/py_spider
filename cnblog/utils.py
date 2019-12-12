def str2dict(s):
    eachs = s.split("\n")
    d = {}
    for each in eachs:
        if each.strip():
            each_list = each.split(": ")
            key = each_list[0].strip()
            value = each_list[1].strip()
            d[key] = value
    return d