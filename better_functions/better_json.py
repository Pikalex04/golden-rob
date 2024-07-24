from json import dump, load


def json_dump(n, d):
    with open(n, 'w+', encoding='utf-8') as f:
        dump(d, f, ensure_ascii=False)
        f.close()


def json_load(n):
    with open(n, 'r', encoding='utf-8') as f:
        a = load(f)
        f.close()
    return a
