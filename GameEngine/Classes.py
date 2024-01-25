import pygame, random


class MainMenu:
    def __init__(self, screen, screen_res):
        self.title_background = pygame.image.load("Assets/Sprites/TitleScreen/Background/title_screen_background.png")
        self.title_background = pygame.transform.scale(self.title_background, screen_res)
        pygame.mixer.music.load("Assets/Sounds/menu_theme.mp3")
        pygame.mixer.music.play(-1)
        self.screen = screen
        self.screen_res = screen_res
        self.title_cups = list()
        self.cup_res = (int(self.screen_res[0] * 0.67578125), int(self.screen_res[1] * 0.694))

        for i in range(1, 35):  # loading filenames of CUPHEAD and MUGMAN images into title_cups
            title_cup = pygame.image.load(f"Assets/Sprites/TitleScreen/Cups/cuphead_title_screen_{i:04}.png")
            title_cup = pygame.transform.scale(title_cup, self.cup_res)
            self.title_cups.append(title_cup)

        self.current_cup_index = 0  # current index of cup image
        self.cup_display_timer = 0  # timer to control how long each cup will be displayed
        self.cup_display_duration = 2  # display duration

    def update_title(self):
        self.cup_display_timer += 1
        if self.cup_display_timer >= self.cup_display_duration:
            self.cup_display_timer = 0
            self.current_cup_index = (self.current_cup_index + 1) % len(self.title_cups)

    def draw_title(self):
        self.screen.blit(self.title_background, (0, 0))
        current_cup = self.title_cups[self.current_cup_index]
        self.screen.blit(current_cup, (((self.screen_res[0] - self.cup_res[0]) // 2), self.screen_res[1] - self.cup_res[1]))
        self.update_title()
        pygame.display.update()

