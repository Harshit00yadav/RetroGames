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


def blit_ascii_stdout(y, x, ascii, stdscr):
    for i, line in enumerate(ascii):
        stdscr.addstr(y+i, x, line)


def populate_windows(stdscr):
    while True:
        try:
            stdscr.addch('0')
        except Exception:
            break
