import math


def getHeuristics(Cx, Cy, Gx, Gy, step, max, count):
    options = []
    if Cx + step < count: options.append((Cx + step, Cy))
    if Cx - step >= 0: options.append((Cx - step, Cy))
    if Cy + step < count: options.append((Cx, Cy + step))
    if Cy - step >= 0: options.append((Cx, Cy - step))

    minHop = 1000000
    for option in options:
        hop_x = math.fabs(Gx - option[0]) / max
        hop_y = math.fabs(Gy - option[1]) / max
        if minHop > hop_y + hop_x:
            minHop = hop_x + hop_y

    return minHop + 1


print(getHeuristics(0, 0, 6, 5, 6, 6, 7))
