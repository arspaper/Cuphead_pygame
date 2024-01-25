import pygame
from GameEngine.Classes import MainMenu

pygame.init()

screen_width = 1280
screen_height = 720
screen_res = (screen_width, screen_height)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cuphead")


main_menu = MainMenu(screen, screen_res)
clock = pygame.time.Clock()

running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    main_menu.draw_title()
pygame.quit()
