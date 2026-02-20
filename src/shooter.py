import curses
from src.utils import load_sprites, blit_spite_stdout


class Map:
    def __init__(self, glevel: int, width: int) -> None:
        self.glevel = glevel
        self.width = width

    def render(self, stdscr) -> None:
        stdscr.addstr(self.glevel, 0, "-" * self.width)


class WorldObject:
    def __init__(self, y, x):
        self.y, self.x = y, x
        self.frame_counter = 0

    def update(self, after_frames=5):
        self.frame_counter += 1
        if self.frame_counter % after_frames == 0:
            self.frame_counter = 0
            return True
        return False

    def move_left(self, speed):
        self.x -= speed

    def render(self, stdscr):
        pass


class Player(WorldObject):
    def __init__(self, y, x) -> None:
        super().__init__(y, x)
        self.sprites = {
            "walk": {},
            "idle": {},
            "jump": {}
        }
        self.can_jump = True
        self.jump_hight = 3
        self.sprite_type = "idle"
        self.frame_no = 0
        self.sprites["walk"]["meta"], self.sprites["walk"]["data"] = load_sprites("resources/man_walk.txt")
        self.sprites["idle"]["meta"], self.sprites["idle"]["data"] = load_sprites("resources/man_idle.txt")
        self.sprites["jump"]["meta"], self.sprites["jump"]["data"] = load_sprites("resources/man_jump.txt")

    def update(self):
        self.frame_no += 1
        if self.sprite_type == "jump" and self.frame_no >= self.sprites[self.sprite_type]["meta"]["frames"]:
            self.sprite_type = "walk"
            self.y += self.jump_hight
            self.can_jump = True
        self.frame_no %= self.sprites[self.sprite_type]["meta"]["frames"]

    def get_bbox(self):
        meta = self.sprites[self.sprite_type]["meta"]
        return (self.y, self.x, self.y + meta["height"], self.x + meta["width"])

    def render(self, stdscr):
        blit_spite_stdout(
            self.y,
            self.x,
            self.sprites[self.sprite_type]["meta"],
            self.sprites[self.sprite_type]["data"],
            self.frame_no,
            stdscr
        )


class Hurdle(WorldObject):
    def __init__(self, y, x):
        super().__init__(y, x)
        self.sprite = {}
        self.sprite["meta"], self.sprite["data"] = load_sprites("resources/hurdle.txt")
        self.frame_no = 0

    def update(self):
        if super().update(after_frames=5):
            self.frame_no += 1
            self.frame_no %= self.sprite["meta"]["frames"]

    def get_bbox(self):
        return (self.y, self.x, self.y + self.sprite["meta"]["height"], self.x + self.sprite["meta"]["width"])

    def render(self, stdscr):
        if self.x + self.sprite["meta"]["width"] < 0:
            return
        blit_spite_stdout(
            self.y,
            self.x,
            self.sprite["meta"],
            self.sprite["data"],
            self.frame_no,
            stdscr
        )

    def is_off_screen(self, screen_width):
        return self.x + self.sprite["meta"]["width"] < 0


def check_inputs(key, player):
    global EXIT
    if key == ord('q'):
        EXIT = True
    elif key == ord(' ') and player.can_jump:
        player.sprite_type = "jump"
        player.frame_no = 0
        player.y -= player.jump_hight
        player.can_jump = False


def check_collision(player, hurdle):
    p_bbox = player.get_bbox()
    h_bbox = hurdle.get_bbox()
    # Check if bounding boxes overlap
    return not (p_bbox[2] <= h_bbox[0] or  # player bottom <= hurdle top
                p_bbox[0] >= h_bbox[2] or  # player top >= hurdle bottom
                p_bbox[3] <= h_bbox[1] or  # player right <= hurdle left
                p_bbox[1] >= h_bbox[3])    # player left >= hurdle right


def reset_game(stdscr, player, wordobjects):
    """Reset game state without recursion - avoids stack buildup"""
    height, width = stdscr.getmaxyx()
    player.y = height//2 - 2
    player.x = width//5
    player.sprite_type = "idle"
    player.frame_no = 0
    player.can_jump = True
    wordobjects.clear()
    wordobjects.append(player)
    wordobjects.append(Hurdle(height//2 - 1, width))
    return 0  # Reset score


def start_shooter_game(stdscr):
    global EXIT
    EXIT = False
    game_over = False
    score = 0
    height, width = stdscr.getmaxyx()
    player = Player(height//2 - 2, width//5)
    wordobjects = []
    level_1 = Map(height//2 + 2, width)

    # _________ initializing entities _____________
    wordobjects.append(player)
    wordobjects.append(Hurdle(height//2 - 1, width))
    # _____________________________________________

    while not EXIT:
        stdscr.clear()
        if game_over:
            stdscr.addstr(height//2, width//2 - 5, "GAME OVER!")
            stdscr.addstr(height//2 + 1, width//2 - 4, f"Score: {score}")
            stdscr.addstr(height//2 + 2, width//2 - 10, "Press 'r' to restart")
            stdscr.refresh()
            stdscr.timeout(-1)  # Blocking input - no timeout
            key = stdscr.getch()
            if key == ord('r'):
                score = reset_game(stdscr, player, wordobjects)
                game_over = False
            elif key == ord('q'):
                EXIT = True
            continue  # Skip rest of game loop

        for obj in wordobjects:
            if ((player.sprite_type == "walk" or player.sprite_type == "jump") and obj != player):
                obj.move_left(3)
            obj.update()
            obj.render(stdscr)
            if isinstance(obj, Hurdle) and obj.is_off_screen(width):
                wordobjects.remove(obj)
                wordobjects.append(Hurdle(height//2 - 1, width))
                score += 1

        # Check collision with hurdles
        for obj in wordobjects:
            if isinstance(obj, Hurdle) and check_collision(player, obj):
                game_over = True

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
