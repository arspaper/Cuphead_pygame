import pygame


class Board:
    def __init__(self, width, height):
        self.cell_size = None
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.offset_top = 10
        self.offset_left = 10

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        pygame.draw.rect(screen, "FFFFFF", pygame.Rect(30, 30, 60, 60))


screen = pygame.display.set_mode((800, 800))

board = Board(5, 7)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()