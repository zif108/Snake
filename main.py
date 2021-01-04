import pygame

LIGHT_GREEN = (120, 255, 142)
DARK_GREEN = (32, 212, 62)
HEADER_COLOR = (0, 176, 29)
BACKGROUND_COLOR = (0, 140, 23)
BLOCK_SIZE = 20
MARGIN = 1
HEADER_MARGIN = 70
SIZE = [460, 530]
COUNT_BLOCKS = 20
screen = pygame.display.set_mode(SIZE)

pygame.display.set_caption('Snake')


def draw_block(color, row, col):
    pygame.draw.rect(screen, color, [BLOCK_SIZE + col * BLOCK_SIZE + MARGIN * (col + 1),
                                     HEADER_MARGIN + BLOCK_SIZE + row * BLOCK_SIZE + MARGIN * (
                                                 row + 1), BLOCK_SIZE,
                                     BLOCK_SIZE])


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, HEADER_COLOR, [0, 0, SIZE[0], HEADER_MARGIN])

    for row in range(COUNT_BLOCKS):
        for col in range(COUNT_BLOCKS):
            if (row + col) % 2 == 0:
                color = LIGHT_GREEN
            else:
                color = DARK_GREEN

            draw_block(color, row, col)

    pygame.display.flip()
