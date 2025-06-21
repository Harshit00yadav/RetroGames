import curses
import random


class Apple:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def render(self, stdscr):
        stdscr.addch(self.y, self.x, '@')

    def respawn(self, width, height):
        self.x = random.randint(2, width - 2)
        self.y = random.randint(2, height - 2)


class Snake:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.direction = [0, 1]
        self.ch = "0"
        self.body = []
        self.body_len = 10
        self.gameover = False

    def render(self, stdscr):
        for x, y, ch in self.body:
            stdscr.addch(int(y), x, ch)

    def movement(self, apple, width, height):
        self.x += self.direction[1]
        self.y += self.direction[0]/2
        if (self.x, self.y, self.ch) in self.body:
            self.gameover = True
        self.body.append((self.x, self.y, self.ch))
        if (self.x == apple.x and int(self.y) == apple.y):
            self.body_len += 3
            apple.respawn(width, height)
            return 1
        if len(self.body) > self.body_len:
            self.body.pop(0)
        return 0


def check_inputs(key, snake):
    if key == ord('q'):
        snake.gameover = True
    elif key == ord('w'):
        if snake.direction[0] != 1:
            snake.direction[0] = -1
            snake.direction[1] = 0
    elif key == ord('a'):
        if snake.direction[1] != 1:
            snake.direction[1] = -1
            snake.direction[0] = 0
    elif key == ord('s'):
        if snake.direction[0] != -1:
            snake.direction[0] = 1
            snake.direction[1] = 0
    elif key == ord('d'):
        if snake.direction[1] != -1:
            snake.direction[1] = 1
            snake.direction[0] = 0


def start_snake_game(stdscr):
    score = 0
    height, width = stdscr.getmaxyx()
    snake = Snake(width//2, height//2)
    apple = Apple(random.randint(2, width - 2), random.randint(2, height - 2))
    while not snake.gameover:
        stdscr.clear()
        score += snake.movement(apple, width, height)
        try:
            snake.render(stdscr)
            apple.render(stdscr)
            stdscr.addstr(0, 0, f"score: {score}")
        except Exception:
            break

        stdscr.refresh()
        try:
            stdscr.timeout(100)
            key = stdscr.getch()
        except curses.ERR:
            pass
        check_inputs(key, snake)
