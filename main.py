import curses
from curses import wrapper
from src.utils import load_ascii, blit_ascii_stdout, draw_border


def header(stdscr, dimentions):
    logo = load_ascii("resources/Logo.txt")
    blit_ascii_stdout(1, dimentions[1]//2 - (len(logo[0])//2), logo, stdscr)
    draw_border(stdscr, (0, 0), dimentions)


def main(stdscr):
    height, width = stdscr.getmaxyx()
    height -= 1
    width -= 1
    dimentions = (height, width)
    stdscr.clear()
    # do stuff here
    # -----------------
    header(stdscr, dimentions)
    # -----------------
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.initscr()
    wrapper(main)
