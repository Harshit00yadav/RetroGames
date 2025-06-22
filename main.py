import curses
from curses import wrapper
from src.utils import load_ascii, blit_ascii_stdout, draw_border
from src.games_menu import start_menu_loop
from src.snake import start_snake_game
from src.shooter import start_shooter_game


games = [
    "  Snake  ",
    "  Shooter  ",
    "  Tetris  ",
    "  [ EXIT ]  "
]


def header(stdscr, dimentions):
    logo = load_ascii("resources/Logo.txt")
    blit_ascii_stdout(1, dimentions[1]//2 - (len(logo[0])//2), logo, stdscr)
    draw_border(stdscr, (0, 0), dimentions)


def main(stdscr):
    height, width = stdscr.getmaxyx()
    height -= 1
    width -= 2
    dimentions = (height, width)
    stdscr.clear()
    header(stdscr, dimentions)
    surface_dimentions = (dimentions[0] - 15, dimentions[1] - 4)
    surface_start = (
        dimentions[0]//2 - surface_dimentions[0]//2 + 1,
        2
    )
    draw_border(stdscr, surface_start, surface_dimentions)
    stdscr.refresh()
    surface = curses.newwin(
        surface_dimentions[0]-1,
        surface_dimentions[1]-1,
        surface_start[0]+1,
        surface_start[1]+1
    )
    while True:
        game_id = start_menu_loop(surface, games)
        if game_id == 0:
            start_snake_game(surface)
        elif game_id == 1:
            start_shooter_game(surface)
        else:
            break


if __name__ == "__main__":
    curses.initscr()
    curses.curs_set(0)
    try:
        wrapper(main)
    finally:
        curses.curs_set(1)
