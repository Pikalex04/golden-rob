from json import dump, load


def json_dump(n, d):
    with open(n, 'w+') as f:
        dump(d, f)
        f.close()


def json_load(n):
    with open(n, 'r') as f:
        a = load(f)
        f.close()
    return a
