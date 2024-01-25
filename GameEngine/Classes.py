import pygame


class Button:
    def __init__(self, image, pos):
        self.image = image
        self.image = image
        self.rect = self.image.get_rect(center=pos)

    def input_check(self, position):
        if self.rect.collidepoint(position):
            return True
        return False


class MainMenu:
    def __init__(self, screen, screen_res, game_state):
        pygame.mixer.music.load("Assets/Sounds/menu_theme.mp3")
        pygame.mixer.music.play()

        self.title_background = pygame.image.load("Assets/Sprites/TitleScreen/Background/title_screen_background.png")
        self.title_background = pygame.transform.scale(self.title_background, screen_res)

        self.menu_background = pygame.image.load("Assets/Sprites/TitleScreen/Background/main_menu_background.png")
        self.menu_background = pygame.transform.scale(self.menu_background, screen_res)

        self.help_background = pygame.image.load("Assets/Sprites/TitleScreen/Background/help_background.png")
        self.help_background = pygame.transform.scale(self.help_background, screen_res)

        self.help_board = pygame.image.load("Assets/Sprites/TitleScreen/help.png")
        self.help_board = pygame.transform.scale(self.help_board, screen_res)

        self.button_help_img = pygame.image.load("Assets/Sprites/Buttons/info.png")
        self.button_help_img = pygame.transform.scale(self.button_help_img, (screen_res[0] * 0.1, screen_res[0] * 0.1))
        self.button_help_pos = (self.button_help_img.get_size()[0] // 2, self.button_help_img.get_size()[1] // 2)
        self.button_help = Button(self.button_help_img, (self.button_help_pos[0], self.button_help_pos[1]))

        self.button_play_img = pygame.image.load("Assets/Sprites/Buttons/play.png")
        self.button_play_img = pygame.transform.scale(self.button_play_img, (screen_res[0] * 0.1, screen_res[0] * 0.1))
        self.button_play_pos = (screen_res[0] // 2, screen_res[1] // 2)
        self.button_play = Button(self.button_play_img, self.button_play_pos)

        self.level_img_b = pygame.image.load("Assets/Sprites/Level_Boards/blueberry.png")
        self.level_img_b = pygame.transform.scale(self.level_img_b, (screen_res[0] * 0.3, screen_res[0] * 0.3))
        self.level_b = Button(self.button_play_img, (screen_res[0] // 2, screen_res[1] // 2))

        self.mode = game_state

        self.screen = screen
        self.screen_res = screen_res

        self.title_cups = list()
        self.transitions = list()

        self.cup_res = (int(self.screen_res[0] * 0.77), int(self.screen_res[1] * 0.8))

        for i in range(1, 35):  # loading filenames of CUPHEAD and MUGMAN images into title_cups
            title_cup = pygame.image.load(f"Assets/Sprites/TitleScreen/Cups/cuphead_title_screen_{i:04}.png")
            title_cup = pygame.transform.scale(title_cup, self.cup_res)
            self.title_cups.append(title_cup)

        for i in range(1, 17):  # loading filenames of the cirlce transition
            transition = pygame.image.load(f"Assets/Sprites/Effects/Transitions/Layer {i}.png")
            transition = pygame.transform.scale(transition, self.screen_res)
            self.transitions.append(transition)

        self.current_cup_index = 0  # current index of cup image
        self.cup_display_timer = 0  # timer to control how long each cup will be displayed
        self.cup_display_duration = 3  # cup display duration

        self.current_transition_index = len(self.transitions) - 1
        self.transition_display_timer = 0
        self.transition_display_duration = 0

    def music_handler(self, mode="N"):
        pygame.mixer.music.stop()
        if mode == "N" or mode == "M":
            pygame.mixer.music.unload()
            pygame.mixer.music.load("Assets/Sounds/menu_theme.mp3")
        if mode == "L":
            pygame.mixer.music.unload()
            pygame.mixer.music.load("Assets/Sounds/level_board.mp3")
        if mode == "H":
            pygame.mixer.music.unload()
            pygame.mixer.music.load("Assets/Sounds/help.mp3")

        pygame.mixer.music.play(-1)

    def update_title(self):
        self.cup_display_timer += 1
        if self.cup_display_timer >= self.cup_display_duration:
            self.cup_display_timer = 0
            self.current_cup_index = (self.current_cup_index + 1) % len(self.title_cups)

    def draw_title(self):
        self.screen.blit(self.title_background, (0, 0))
        current_cup = self.title_cups[self.current_cup_index]
        self.screen.blit(
            current_cup, (((self.screen_res[0] - self.cup_res[0]) // 2), self.screen_res[1] - self.cup_res[1]))
        if self.current_cup_index > 17:
            start_bg = pygame.font.SysFont("Fink Heavy", int(self.screen_res[0] * 0.0390625 * 1.05))
            text_bg = start_bg.render("Press Any Button", True, (0, 0, 0))
            self.screen.blit(
                text_bg,
                (((self.screen_res[0] - text_bg.get_size()[0]) // 2), self.screen_res[1] * 0.9 - text_bg.get_size()[1]))

            start = pygame.font.SysFont("Fink Heavy", int(self.screen_res[0] * 0.0390625))
            text = start.render("Press Any Button", True, (231, 188, 76))
            self.screen.blit(
                text,
                (((self.screen_res[0] - text.get_size()[0]) // 2), self.screen_res[1] * 0.9 - text.get_size()[1]))
        self.update_title()

    def update_transition_fade(self):
        self.transition_display_timer += 1
        if self.transition_display_timer > self.transition_display_duration:
            self.transition_display_timer = 0
            self.current_transition_index -= 1

    def draw_transition_fade(self):
        self.update_transition_fade()
        current_transition = self.transitions[self.current_transition_index]
        self.screen.blit(current_transition, (0, 0))

    def update_transition_unfade(self):
        self.transition_display_timer += 1
        if self.transition_display_timer > self.transition_display_duration:
            self.transition_display_timer = 0
            self.current_transition_index += 1

    def draw_transition_unfade(self):
        self.update_transition_unfade()
        current_transition = self.transitions[self.current_transition_index]
        self.screen.blit(current_transition, (0, 0))

    def draw_menu(self):
        self.screen.blit(self.menu_background, (0, 0))
        # self.screen.blit(self.button_play.image, self.button_play.rect)
        self.screen.blit(self.button_play.image, self.button_play.rect.topleft)
        self.screen.blit(self.button_help.image, self.button_help.rect)

    def draw_help(self):
        self.screen.blit(self.help_background, (0, 0))
        self.screen.blit(
            self.help_board, ((self.screen_res[0] - self.help_board.get_size()[0]) // 2,
                              (self.screen_res[0] - self.help_board.get_size()[0]) // 2))

    def draw_level_menu(self):
        self.screen.blit(self.help_background, (0, 0))
        self.screen.blit(self.level_img_b, self.level_b.rect.topleft)
