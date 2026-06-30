WIDTH = 80
HEIGHT = 24


def render(objects):
    screen = [[" "] * WIDTH for _ in range(HEIGHT)]
    for o in objects:
        if o.altitude < 0:
            continue

        x = int((o.azimuth / 360) * (WIDTH - 1))
        y = int(((90 - o.altitude) / 90) * (HEIGHT - 1))

        x = max(0, min(WIDTH - 1, x))
        y = max(0, min(HEIGHT - 1, y))

        screen[y][x] = o.symbol

    print("\n".join("".join(row) for row in screen))