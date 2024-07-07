

def cut_in(x, y):  # cuts everything in x behind y and then strips the final text
    return x[x.find(y):].strip()


def cut_out(x, y):  # cuts everything in x after y and then strips the final text
    return x[:x.find(y)].strip()


def scrap(x, y, z):  # cuts what is between y and z in x and then strips the cut text
    x = cut_in(x, y)
    return x[x.find(y) + len(y):x.find(z)].strip()


def xcut_in(x, y):  # cuts everything in x behind y and y and then strips the final text
    return x[x.find(y) + len(y):].strip()


def zscrap(x, *args):  # cuts many fields from x always using the initially newly-cut text from y and returns the
    # values between each y and z; useful for lists of <td>'s
    results = []
    for arg in args:
        x = xcut_in(x, arg[0])
        results.append(x[:x.find(arg[1])])
    return results
