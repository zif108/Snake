import pygame
from random import randrange

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

pygame.display.set_caption('Snake')

x = randrange(0, COUNT_BLOCKS - 1)
y = randrange(0, COUNT_BLOCKS - 1)
snake_blocks = []
snake_chis = []
apple = (randrange(0, COUNT_BLOCKS - 1), randrange(0, COUNT_BLOCKS - 1))
d_x = 0
d_y = 0
lenght = 1
score = 0
fps = 8
clock = pygame.time.Clock()
pygame.init()


class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_in_field(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def eating_yourself(self):
        pass


def draw_block(color, row, col):
    pygame.draw.rect(screen, color, [BLOCK_SIZE + col * BLOCK_SIZE + MARGIN * (col + 1),
                                     HEADER_MARGIN + BLOCK_SIZE + row * BLOCK_SIZE + MARGIN * (
                                             row + 1), BLOCK_SIZE,
                                     BLOCK_SIZE])


while True:
    print(score)
    clock.tick(fps)
    # Рисование поля
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, HEADER_COLOR, [0, 0, SIZE[0], HEADER_MARGIN])

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
    head = snake_blocks[-1]

    for el in snake_blocks:
        draw_block((80, 126, 244), el.x, el.y)

    draw_block(APPLE_COLOR, apple[0], apple[1])

    # змея ест яблоко

    if snake_blocks[-1].x == list(apple)[0] and snake_blocks[-1].y == list(apple)[1]:
        apple = (randrange(0, COUNT_BLOCKS - 1), randrange(0, COUNT_BLOCKS - 1))
        snake_blocks.append(Snake(apple[0], apple[1]))
        lenght += 1
        fps += 0.5
        score += 1

    # Проигрыш
    if not snake_blocks[-1].is_in_field():
        d_x = 0
        d_y = 0

    if snake_chis[-1] in snake_chis[:-1]:
        d_x = 0
        d_y = 0

    # События
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if key[pygame.K_w] and btns['w']:
        d_x, d_y = -1, 0
        btns = {'w': True, 's': False, 'a': True, 'd': True}
        print(btns)
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
