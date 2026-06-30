import shutil
FOV = 90

def render(objects,facing):
    WIDTH, HEIGHT = shutil.get_terminal_size()
    HEIGHT -= 4

    screen = [[" "] * WIDTH for _ in range(HEIGHT)]

    background = [o for o in objects if o.type == "star"]
    important = [o for o in objects if o.type == "important_star"]
    planets = [o for o in objects if o.type == "planet"]

    # Background stars
    for o in background:
        delta = (o.azimuth - facing + 540) % 360 - 180

        if abs(delta) > FOV / 2:
            continue

        x = int(((delta + FOV / 2) / FOV) * (WIDTH - 1))
        y = int(((90 - o.altitude) / 90) * (HEIGHT - 1))

        x = max(0, min(WIDTH - 1, x))
        y = max(0, min(HEIGHT - 1, y))

        if screen[y][x] == " ":
            screen[y][x] = "*"

    # Important stars + planets
    for o in important + planets:
        x = int((o.azimuth / 360) * (WIDTH - 1))
        y = int(((90 - o.altitude) / 90) * (HEIGHT - 1))

        x = max(0, min(WIDTH - 1, x))
        y = max(0, min(HEIGHT - 1, y))

        if o.name == "Sun":
            label = "☉ Sun"
        elif o.name == "Moon":
            label = "☾ Moon"
        elif o.type == "planet":
            label = "○ " + o.name
        else:
            label = "✦ " + o.name

        x = min(x, WIDTH - len(label))

        for i, ch in enumerate(label):
            if 0 <= x + i < WIDTH:
                screen[y][x + i] = ch

    print("\n".join("".join(row) for row in screen))