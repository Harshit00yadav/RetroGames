import curses
from src.utils import load_sprites, blit_spite_stdout


class Map:
    def __init__(self, glevel: int, width: int) -> None:
        self.glevel = glevel
        self.width = width

    def render(self, stdscr) -> None:
        stdscr.addstr(self.glevel, 0, "-" * self.width)


class Player:
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x
        self.sprites = {
            "walk": {},
            "idle": {},
            "jump": {}
        }
        self.can_jump = True
        self.sprite_type = "idle"
        self.frame_no = 0
        self.sprites["walk"]["meta"], self.sprites["walk"]["data"] = load_sprites("resources/man_walk.txt")
        self.sprites["idle"]["meta"], self.sprites["idle"]["data"] = load_sprites("resources/man_idle.txt")
        self.sprites["jump"]["meta"], self.sprites["jump"]["data"] = load_sprites("resources/man_jump.txt")

    def update(self):
        self.frame_no += 1
        if self.sprite_type == "jump" and self.frame_no >= self.sprites[self.sprite_type]["meta"]["frames"]:
            self.sprite_type = "walk"
            self.y += 1
            self.can_jump = True
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
    elif key == ord(' ') and player.can_jump:
        player.sprite_type = "jump"
        player.frame_no = 0
        player.y -= 1
        player.can_jump = False


def start_shooter_game(stdscr):
    global EXIT
    EXIT = False
    score = 0
    height, width = stdscr.getmaxyx()
    player = Player(height//2 - 2, width//5)
    level_1 = Map(height//2 + 2, width)
    while not EXIT:
        stdscr.clear()
        player.update()
        player.render(stdscr)
        level_1.render(stdscr)
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
