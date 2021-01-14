import pygame
import pygame_menu
import sqlite3
from random import randrange

pygame.init()
con = sqlite3.connect("Data base/Snake.db")
cur = con.cursor()
LIGHT_GREEN = (170, 215, 81)
DARK_GREEN = (162, 209, 73)
HEADER_COLOR = (74, 117, 44)
BACKGROUND_COLOR = (87, 138, 52)
APPLE_COLOR = (247, 42, 15)
BLOCK_SIZE = 20
MARGIN = 1
HEADER_MARGIN = 70
SIZE = (460, 530)
COUNT_BLOCKS = 20
btns = {'w': True, 's': True, 'a': True, 'd': True}
screen = pygame.display.set_mode(SIZE)
init_speed = 20
dif = 'H'
name = 'John Doe'
a = cur.execute("""SELECT * FROM scores""").fetchall()
print(a)
s = [i[1] for i in a]
m = 0
if s != []:
    print(max(s))
    m = max(s)

pygame.display.set_caption('Snake')


def draw_block(color, row, col):
    pygame.draw.rect(screen, color, [BLOCK_SIZE + col * BLOCK_SIZE + MARGIN * (col + 1),
                                     HEADER_MARGIN + BLOCK_SIZE + row * BLOCK_SIZE + MARGIN * (
                                             row + 1), BLOCK_SIZE,
                                     BLOCK_SIZE])


class Apple:
    def __init__(self, x, y, color, func, ):
        self.x = x
        self.y = y
        self.color = color
        self.func = func
        # self.lenght = lenght
        # self.fps = fps
        # self.score = score

    def draw(self):
        draw_block(self.color, self.x, self.y)

    # def apply_function(self):
    #     if self.func == 'default':
    #         self.lenght += 1
    #         self.fps += 0.5
    #         # print(self.fps)
    #         self.score += 1


def start_the_game():
    global btns
    global init_speed
    global name
    global m
    print(init_speed)

    x = randrange(0, COUNT_BLOCKS - 1)
    y = randrange(0, COUNT_BLOCKS - 1)
    snake_blocks = []
    snake_chis = []

    d_x = 0
    d_y = 0
    lenght = 1
    fps = init_speed
    score = 0
    once = True
    apple = Apple(randrange(0, COUNT_BLOCKS - 1), randrange(0, COUNT_BLOCKS - 1), APPLE_COLOR,
                  'default')
    record = m
    shield = record
    doub_apple = randrange(1, record)

    clock = pygame.time.Clock()
    print(fps)
    print(dif)

    font = pygame.font.SysFont('Palatino Linotype', 32)
    while True:

        clock.tick(fps)

        # Рисование поля
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, SIZE[0], HEADER_MARGIN])
        text_score = font.render(f'Score: {score}', False, (253, 192, 1))
        if score >= record:
            record = score
            print(record)
            text_record = font.render(f'Max: {score}', False, (253, 192, 1))
        else:
            text_record = font.render(f'Max: {record}', False, (253, 192, 1))
        screen.blit(text_score, (20, 20))
        screen.blit(text_record, (325, 20))

        for row in range(COUNT_BLOCKS):
            for col in range(COUNT_BLOCKS):
                if (row + col) % 2 == 0:
                    color = LIGHT_GREEN
                else:
                    color = DARK_GREEN

                draw_block(color, row, col)

        # Рисование змеи и яблока
        x += d_x
        y += d_y
        snake_blocks.append(Snake(x, y))
        snake_chis.append([x, y])
        snake_blocks = snake_blocks[-lenght:]
        snake_chis = snake_chis[-lenght:]

        for el in snake_blocks:
            draw_block((80, 126, 244), el.x, el.y)

        Apple.draw(apple)
        # змея ест яблоко

        if snake_blocks[-1].x == apple.x and snake_blocks[-1].y == apple.y:
            print(doub_apple, score)
            if apple.func == 'default':
                lenght += 1
                if dif == 'H':
                    fps += 1.25
                elif dif == 'M':
                    fps += 0.8
                elif dif == 'E':
                    fps += 0.5
                score += 1
            elif apple.func == '2x_score':
                lenght += 1
                fps += 0.5
                score = score * 2
            elif apple.func == 'shield':
                lenght += 1
                if dif == 'H':
                    fps -= 5
                elif dif == 'M':
                    fps += 2.5
                elif dif == 'E':
                    fps -= 1
                score += 1
                once = False

            if doub_apple == score:
                apple = Apple(randrange(0, COUNT_BLOCKS - 1), randrange(0, COUNT_BLOCKS - 1),
                              (255, 223, 0), '2x_score')

            elif shield <= score and once:
                apple = Apple(randrange(0, COUNT_BLOCKS - 1), randrange(0, COUNT_BLOCKS - 1),
                              (128, 0, 255), 'shield')


            else:
                apple = Apple(randrange(0, COUNT_BLOCKS - 1), randrange(0, COUNT_BLOCKS - 1),
                              APPLE_COLOR, 'default')

            snake_blocks.append(Snake(apple.x, apple.y))

            # Проигрыш
        if not snake_blocks[-1].is_in_field():
            d_x = 0
            d_y = 0
            text_game_over = font.render('Game over', False, (186, 54, 54))
            screen.blit(text_game_over, (150, 265))
            print('a')
            break


        if snake_chis[-1] in snake_chis[:-1]:
            d_x = 0
            d_y = 0
            text_game_over = font.render('Game over', False, (186, 54, 54))
            screen.blit(text_game_over, (150, 265))

        # События
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        if key[pygame.K_w] and btns['w']:
            d_x, d_y = -1, 0
            btns = {'w': True, 's': False, 'a': True, 'd': True}
        if key[pygame.K_s] and btns['s']:
            d_x, d_y = 1, 0
            btns = {'w': False, 's': True, 'a': True, 'd': True}
        if key[pygame.K_a] and btns['a']:
            d_x, d_y = 0, -1
            btns = {'w': True, 's': True, 'a': True, 'd': False}
        if key[pygame.K_d] and btns['d']:
            d_x, d_y = 0, 1
            btns = {'w': True, 's': True, 'a': False, 'd': True}
        pygame.display.flip()
    cur.execute("""INSERT INTO scores(player, score) VALUES(?, ?)""", (name, score))
    con.commit()
    m = record

class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_in_field(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def eating_yourself(self):
        pass


def set_difficulty(value, difficulty):
    global init_speed
    global dif
    if difficulty == 1:
        init_speed = 10
        dif = 'H'
    elif difficulty == 2:
        init_speed = 8
        dif = 'M'
    elif difficulty == 3:
        init_speed = 5
        dif = 'E'


def check_name(name_):
    global name
    name = name_
    # cur.execute("""INSERT INTO scores(player) VALUES(?)""", (name,))

    # con.commit()

menu = pygame_menu.Menu(300, 400, 'Welcome',
                        theme=pygame_menu.themes.THEME_GREEN)

menu.add_text_input('Name :', default='John Doe', onreturn=check_name)
menu.add_selector('Difficulty :', [('Hard', 1), ('Medium', 2), ('Easy', 3)], onchange=set_difficulty)
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)
while True:

    screen.fill(BACKGROUND_COLOR)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
