class Snake:
    def __init__(self, x, y):
        self.x, self.y = x,y
        self.direction = [0,0]

    def render(self, stdscr):
        stdscr.addch(self.y, self.x, '@')

    def movement(self):
        self.x += self.direction[1]
        self.y += self.direction[0]
        



def start_snake_game(stdscr):
    height, width = stdscr.getmaxyx()
    snake = Snake(1,1)
    while True:
        stdscr.clear()
        snake.movement()
        snake.render(stdscr)

        stdscr.refresh()
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('w'):
            snake.direction[0]=-1
            snake.direction[1]=0
        elif key == ord('a'):
            snake.direction[1]=-1
            snake.direction[0]=0
        elif key == ord('s'):
            snake.direction[0]=1
            snake.direction[1]=0
        elif key == ord('d'):
            snake.direction[1]=1
            snake.direction[0]=0
            
            