import curses


def start_menu_loop(stdscr, games):
    selected = 0
    height, width = stdscr.getmaxyx()
    while True:
        stdscr.clear()
        for i, g in enumerate(games):
            if i == selected:
                stdscr.addstr(i, width//2-len(g)//2, g, curses.A_REVERSE)
            else:
                stdscr.addstr(i, width//2-len(g)//2, g)
        stdscr.refresh()
        key = stdscr.getch()

        if key == ord('j'):
            selected += 1
            if selected >= len(games):
                selected = 0
        elif key == ord('k'):
            selected -= 1
            if selected < 0:
                selected = len(games) - 1
        elif key == ord('\n'):
            return selected
