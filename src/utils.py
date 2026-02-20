import json


def draw_border(stdscr, start, dimentions):
    stdscr.addstr(start[0], start[1], "┌"+"─"*(dimentions[1]-1)+"┐")
    for i in range(start[0] + 1, start[0]+dimentions[0]):
        stdscr.addstr(i, start[1], "│")
        stdscr.addstr(i, start[1] + dimentions[1], "│")
    stdscr.addstr(
        start[0] + dimentions[0],
        start[1],
        "└"+"─"*(dimentions[1]-1)+"┘"
    )


def load_ascii(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    return lines


def load_sprites(file_path):
    with open(file_path, "r") as f:
        meta = f.readline().strip()
        data = f.read().split('\n')
    meta = json.loads(meta)
    return meta, data


def blit_spite_stdout(y, x, meta, data, frame_no, stdscr):
    start = frame_no * meta["height"]
    end = start + meta["height"]
    max_y, max_x = stdscr.getmaxyx()
    for i, line in enumerate(data[start:end]):
        if x + len(line) < 0 or y + i < 0:
            continue
        rendered_line = line[max(0, -x):] if x < 0 else line
        if x >= max_x:
            continue
        rendered_line = rendered_line[:max_x - x]
        stdscr.addstr(y+i, max(0, x), rendered_line)


def blit_ascii_stdout(y, x, ascii, stdscr):
    for i, line in enumerate(ascii):
        stdscr.addstr(y+i, x, line)


def populate_windows(stdscr):
    while True:
        try:
            stdscr.addch('0')
        except Exception:
            break


if __name__ == "__main__":
    meta, data = load_sprites("resources/man_walk.txt")
    blit_spite_stdout(10, 10, meta, data, 3, None)
