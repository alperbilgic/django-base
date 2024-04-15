def flatmap(f, xs):
    ys = []
    for x in xs:
        ys.extend(f(x))
    return ys
