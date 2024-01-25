import pygame
from GameEngine.Classes import MainMenu

pygame.init()

# screen_width = 1920
# screen_height = 1080

screen_width = 1280  # MAIN RESOLUTION (16:9)
screen_height = 720

screen_res = (screen_width, screen_height)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cuphead")
pygame.display.set_icon(pygame.image.load("Assets/Sprites/TitleScreen/logo.png"))


clock = pygame.time.Clock()

running = True

game_state = "T"  # GAME STATE: T = Title Screen, M = Menu, H = Help, L = Level Select, G = Game
transition_state = "N"  # TRANSITION STATE: None = Nothing, F = Fading, U = Unfading
game_state_last = None
quit_check = False
music_state = True

m = MainMenu(screen, screen_res, game_state)

while running:
    clock.tick(60)
    mouse_LMB = False
    keyboard_ESC = False
    mouse_POS = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_LMB = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            keyboard_ESC = True
        if event.type == pygame.KEYDOWN and not event.key == pygame.K_ESCAPE:
            if game_state == "T":
                transition_state = "F"
                game_state = "M"
                game_state_last = "T"

    if not music_state:
        m.music_handler(game_state)
        music_state = True

    if game_state != "G" or game_state != "L":
        pass

    if game_state == "T":
        screen.fill((0, 0, 0))
        m.draw_title()
        if keyboard_ESC or quit_check:
            quit_check = True
            m.draw_title()
            m.draw_transition_fade()
            if m.current_transition_index == 0:
                m.draw_transition_unfade()
                running = False

        if transition_state == "F":
            m.draw_menu()
            m.draw_transition_fade()
            if m.current_transition_index == 0:
                transition_state = "U"

        elif transition_state == "U":
            m.draw_transition_unfade()
            if m.current_transition_index == 15:
                transition_state = "N"

    if game_state == "M":
        m.draw_menu()
        if transition_state == "F":
            if game_state_last == "T":
                m.draw_title()
            elif game_state_last == "H":
                m.draw_help()
            elif game_state_last == "L":
                m.draw_level_menu()
            m.draw_transition_fade()
            if m.current_transition_index == 0:
                transition_state = "U"

        elif transition_state == "U":
            m.draw_transition_unfade()
            if m.current_transition_index == 15:
                transition_state = "N"

        elif mouse_LMB and m.button_help.input_check(mouse_POS):
            game_state = "H"
            music_state = False
            transition_state = "F"

        elif mouse_LMB and m.button_play.input_check(mouse_POS):
            game_state = "L"
            music_state = False
            transition_state = "F"

        elif keyboard_ESC:
            transition_state = "F"
            game_state = "T"

    if game_state == "L":
        m.draw_level_menu()
        if transition_state == "F":
            m.draw_menu()
            m.draw_transition_fade()
            if m.current_transition_index == 0:
                transition_state = "U"

        elif transition_state == "U":
            m.draw_transition_unfade()
            if m.current_transition_index == 15:
                transition_state = "N"

        elif mouse_LMB and m.level_b.input_check(mouse_POS):
            pygame.mixer.Sound.play(m.select_sound)

        elif keyboard_ESC:
            game_state = "M"
            music_state = False
            game_state_last = "L"
            transition_state = "F"

    if game_state == "H":
        m.draw_help()
        if transition_state == "F":
            m.draw_menu()
            m.draw_transition_fade()
            if m.current_transition_index == 0:
                transition_state = "U"

        elif transition_state == "U":
            m.draw_transition_unfade()
            if m.current_transition_index == 15:
                transition_state = "N"

        elif keyboard_ESC:
            game_state = "M"
            music_state = False
            game_state_last = "H"
            transition_state = "F"

    pygame.display.update()

pygame.quit()
