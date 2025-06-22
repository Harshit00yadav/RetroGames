import curses
from src.utils import load_sprites, blit_spite_stdout


class Player:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.sprites = {
            "walk": {},
            "idle": {}
        }
        self.sprite_type = "idle"
        self.frame_no = 0
        self.sprites["walk"]["meta"], self.sprites["walk"]["data"] = load_sprites("resources/man_walk.txt")
        self.sprites["idle"]["meta"], self.sprites["idle"]["data"] = load_sprites("resources/man_idle.txt")

    def update(self):
        self.frame_no += 1
        self.frame_no %= self.sprites[self.sprite_type]["meta"]["frames"]

    def render(self, stdscr):
        blit_spite_stdout(
            self.y,
            self.x,
            self.sprites[self.sprite_type]["meta"],
            self.sprites[self.sprite_type]["data"],
            self.frame_no,
            stdscr
        )


def check_inputs(key, player):
    global EXIT
    if key == ord('q'):
        EXIT = True
    elif key == ord('w'):
        player.y -= 1
    elif key == ord('s'):
        player.y += 1
    elif key == ord('d'):
        player.sprite_type = "walk"
        player.x += 1
    elif key == ord('a'):
        player.x -= 1


def start_shooter_game(stdscr):
    global EXIT
    EXIT = False
    score = 0
    height, width = stdscr.getmaxyx()
    player = Player(height//2 - 2, width//5)
    while not EXIT:
        stdscr.clear()
        player.update()
        player.render(stdscr)
        try:
            stdscr.addstr(0, 0, f"score: {score}")
        except Exception as e:
            print(e)
            break

        stdscr.refresh()
        try:
            stdscr.timeout(100)
            key = stdscr.getch()
        except curses.ERR:
            pass
        check_inputs(key, player)
