import pygame
import pygame_menu
import sqlite3
from random import randrange

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
con = sqlite3.connect("Data base/Snake.db")
cur = con.cursor()
LIGHT_GREEN = (170, 215, 81)
DARK_GREEN = (162, 209, 73)
HEADER_COLOR = (74, 117, 44)
BACKGROUND_COLOR = (87, 138, 52)
APPLE_COLOR = (247, 42, 15)
GOLD_COLOR = (255, 223, 0)
PURPLE_COLOR = 128, 0, 255
BLOCK_SIZE = 20
MARGIN = 1
HEADER_MARGIN = 70
SIZE = (460, 530)
COUNT_BLOCKS = 20
btns = {'w': True, 's': True, 'a': True, 'd': True}
btns1 = {'w': True, 's': True, 'a': True, 'd': True}
action_au = {'w': True, 's': True, 'a': True, 'd': True}
s_up = pygame.mixer.Sound('Sounds/up1.mp3')
s_down = pygame.mixer.Sound('Sounds/down1.mp3')
s_left = pygame.mixer.Sound('Sounds/left1.mp3')
s_right = pygame.mixer.Sound('Sounds/right1.mp3')
s_eating = pygame.mixer.Sound('Sounds/eating.mp3')
s_death = pygame.mixer.Sound('Sounds/death.mp3')
screen = pygame.display.set_mode(SIZE)
init_speed = 15
dif = 'H'
name = 'John Doe'
selec = cur.execute("""SELECT * FROM scores""").fetchall()
scores_ = [i[1] for i in selec]
max_score = max(scores_)

pygame.display.set_caption('Snake')


def draw_block(color, row, col):
    pygame.draw.rect(screen, color, [BLOCK_SIZE + col * BLOCK_SIZE + MARGIN * (col + 1),
                                     HEADER_MARGIN + BLOCK_SIZE + row * BLOCK_SIZE + MARGIN * (
                                             row + 1), BLOCK_SIZE,
                                     BLOCK_SIZE])


class Apple:
    def __init__(self, x, y, color, func):
        self.x = x
        self.y = y
        self.color = color
        self.func = func

    def draw(self):
        draw_block(self.color, self.x, self.y)


class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_in_field(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS


def start_the_game():
    global btns
    global btns1
    global action_au
    global init_speed
    global name
    global max_score

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
    while True:
        apple = Apple(randrange(0, COUNT_BLOCKS - 1), randrange(0, COUNT_BLOCKS - 1), APPLE_COLOR,
                      'default')
        if apple.x == x and apple.y == y:
            continue
        else:
            break
    record = max_score
    shield = record
    doub_apple = randrange(1, record)

    clock = pygame.time.Clock()

    font = pygame.font.SysFont('Palatino Linotype', 32)
    while True:

        clock.tick(fps)

        # Рисование поля
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, SIZE[0], HEADER_MARGIN])
        text_score = font.render(f'Score: {score}', False, (253, 192, 1))
        if score >= record:
            record = score
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
            s_eating.play(loops=0, maxtime=0)
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
                if dif == 'H':
                    lenght -= 3
                    snake_blocks = snake_blocks[3:]
                    snake_chis = snake_chis[3:]
                elif dif == 'M':
                    lenght -= 2
                    snake_blocks = snake_blocks[2:]
                    snake_chis = snake_chis[2:]
                elif dif == 'E':
                    lenght -= 1
                    snake_blocks = snake_blocks[1:]
                    snake_chis = snake_chis[1:]
                score += 1
                once = False
            if doub_apple == score:
                apple = choose(snake_blocks, '2x_score')

            elif shield <= score and once:
                apple = choose(snake_blocks, 'shield')

            else:
                apple = choose(snake_blocks, 'default')

            snake_blocks.append(Snake(apple.x, apple.y))

            # Проигрыш
        if not snake_blocks[-1].is_in_field():
            s_death.play()
            break

        if snake_chis[-1] in snake_chis[:-1]:
            s_death.play()
            break

        # События
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and btns1['w']:
                    if action_au['w']:
                        s_up.play()
                        action_au = {'w': False, 's': True, 'a': True, 'd': True}
                    btns1 = {'w': True, 's': False, 'a': True, 'd': True}
                elif event.key == pygame.K_s and btns1['s']:
                    if action_au['s']:
                        s_down.play()
                        action_au = {'w': True, 's': False, 'a': True, 'd': True}
                    btns1 = {'w': False, 's': True, 'a': True, 'd': True}
                elif event.key == pygame.K_a and btns1['a']:
                    if action_au['a']:
                        s_left.play()
                        action_au = {'w': True, 's': True, 'a': False, 'd': True}
                    btns1 = {'w': True, 's': True, 'a': True, 'd': False}
                elif event.key == pygame.K_d and btns1['d']:
                    if action_au['d']:
                        s_right.play()
                        action_au = {'w': True, 's': True, 'a': True, 'd': False}
                    btns1 = {'w': True, 's': True, 'a': False, 'd': True}

        if key[pygame.K_w] and btns['w']:
            d_x, d_y = -1, 0
            btns = {'w': True, 's': False, 'a': True, 'd': True}

        elif key[pygame.K_s] and btns['s']:
            d_x, d_y = 1, 0
            btns = {'w': False, 's': True, 'a': True, 'd': True}
        elif key[pygame.K_a] and btns['a']:
            d_x, d_y = 0, -1
            btns = {'w': True, 's': True, 'a': True, 'd': False}
        elif key[pygame.K_d] and btns['d']:
            d_x, d_y = 0, 1
            btns = {'w': True, 's': True, 'a': False, 'd': True}
        elif key[pygame.K_ESCAPE]:
            main_menu()

        pygame.display.flip()
    btns = {'w': True, 's': True, 'a': True, 'd': True}
    btns1 = {'w': True, 's': True, 'a': True, 'd': True}
    action_au = {'w': True, 's': True, 'a': True, 'd': True}
    cur.execute("""INSERT INTO scores(player, score) VALUES(?, ?)""", (name, score))
    con.commit()
    max_score = record
    the_end()


def choose(snake, func):
    x = [i.x for i in snake]
    y = [i.y for i in snake]
    apple = Apple(randrange(0, COUNT_BLOCKS - 1), randrange(0, COUNT_BLOCKS - 1), APPLE_COLOR,
                  func)
    while True:
        if func == 'default':
            apple = Apple(randrange(0, COUNT_BLOCKS - 1), randrange(0, COUNT_BLOCKS - 1),
                          APPLE_COLOR,
                          func)
        elif func == '2x_score':
            apple = Apple(randrange(0, COUNT_BLOCKS - 1), randrange(0, COUNT_BLOCKS - 1),
                          GOLD_COLOR,
                          func)
        elif func == 'shield':
            apple = Apple(randrange(0, COUNT_BLOCKS - 1), randrange(0, COUNT_BLOCKS - 1),
                          PURPLE_COLOR,
                          func)
        if apple.x in x and apple.y in y:
            continue
        else:
            break
    return apple


def the_end():
    while True:
        font = pygame.font.SysFont('Palatino Linotype', 32)
        bg = pygame.image.load("Images/go.jpg")

        screen.blit(bg, (80, 180))
        text_game_over = font.render('Press F', False, (0, 0, 0))
        screen.blit(text_game_over, (185, 290))

        events = pygame.event.get()
        key = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        if key[pygame.K_f]:
            start_the_game()
        elif key[pygame.K_ESCAPE]:
            main_menu()
        pygame.display.flip()


def set_difficulty(value, difficulty):
    global init_speed
    global dif
    if difficulty == 1:
        init_speed = 15
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


menu = pygame_menu.Menu(300, 400, 'Welcome',
                        theme=pygame_menu.themes.THEME_GREEN)

menu.add_text_input('Name :', default='John Doe', onreturn=check_name)
menu.add_selector('Difficulty :', [('Hard', 1), ('Medium', 2), ('Easy', 3)], onchange=set_difficulty)
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)


def main_menu():
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


main_menu()
