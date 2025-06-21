def start_snake_game(stdscr):
    height, width = stdscr.getmaxyx()
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "press q to exit")
        stdscr.refresh()
        key = stdscr.getch()
        if key == ord('q'):
            break
