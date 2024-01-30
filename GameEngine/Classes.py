import pygame
import time
import random


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
        self.select_sound = pygame.mixer.Sound("Assets/Sounds/Effects/select.wav")

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
        self.level_img_b = pygame.transform.scale(self.level_img_b,
                                                  (screen_res[0] * 0.2, screen_res[0] * 0.2 * 0.726))
        self.level_b = Button(self.level_img_b, (screen_res[0] // 4, screen_res[1] // 2))

        self.level_img_f = pygame.image.load("Assets/Sprites/Level_Boards/flower.png")
        self.level_img_f = pygame.transform.scale(self.level_img_f,
                                                  (screen_res[0] * 0.2, screen_res[0] * 0.2 * 0.726))
        self.level_f = Button(self.level_img_f, (screen_res[0] // 2, screen_res[1] // 2))

        self.level_img_fg = pygame.image.load("Assets/Sprites/Level_Boards/frogs.png")
        self.level_img_fg = pygame.transform.scale(self.level_img_fg,
                                                  (screen_res[0] * 0.2, screen_res[0] * 0.2 * 0.726))
        self.level_fg = Button(self.level_img_fg, (screen_res[0] // 1.33, screen_res[1] // 2))

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
        self.screen.blit(self.level_img_f, self.level_f.rect.topleft)
        self.screen.blit(self.level_img_fg, self.level_fg.rect.topleft)


class Player_Imgs(pygame.sprite.Sprite):
    def __init__(self, image_paths, position, *groups):
        super().__init__(*groups)

        self.images = dict()  # images of the player
        self.images["Idle"] = []
        self.images["Aim"] = []
        self.images["Dash_G"] = []
        self.images["Dash_A"] = []
        self.images["Hit_G"] = []
        self.images["Hit_A"] = []
        self.images["Jump"] = []

        self.images["Death"] = []
        self.images["HP"] = []
        self.images["Flex"] = []
        self.images["Pants"] = []

        self.images_left = dict()  # mirrored images of the player
        self.images_left["Idle"] = []
        self.images_left["Aim"] = []
        self.images_left["Dash_G"] = []
        self.images_left["Dash_A"] = []
        self.images_left["Hit_G"] = []
        self.images_left["Hit_A"] = []
        self.images_left["Jump"] = []

        for i in range(5):  # IDLE
            img = pygame.image.load(f"Assets/Sprites/Player/Idle/{i}.png")
            img_res = img.get_size()
            img = pygame.transform.scale(img, img_res)
            self.images["Idle"].append(img)
            img = pygame.transform.flip(img, True, False)
            self.images_left["Idle"].append(img)

        for i in range(5):  # AIM
            img = pygame.image.load(f"Assets/Sprites/Player/Idle/{i}.png")
            img_res = img.get_size()
            img = pygame.transform.scale(img, img_res)
            self.images["Idle"].append(img)
            img = pygame.transform.flip(img, True, False)
            self.images_left["Idle"].append(img)

        for i in range(4):  # HEALTH
            img = pygame.image.load(f"Assets/Sprites/Player/HP/{i}.png")
            img_res = img.get_size()
            img = pygame.transform.scale(img, img_res)
            self.images["HP"].append(img)

        for i in range(8):  # DASH
            imgA = pygame.image.load(f"Assets/Sprites/Player/Dash/Air/{i}.png")
            imgG = pygame.image.load(f"Assets/Sprites/Player/Dash/Ground/{i}.png")
            imgA_res = imgA.get_size()
            imgG_res = imgG.get_size()

            imgA = pygame.transform.scale(imgA, imgA_res)
            self.images["Dash_A"].append(imgA)
            imgA = pygame.transform.flip(imgA, True, False)
            self.images_left["Dash_A"].append(imgA)

            imgG = pygame.transform.scale(imgG, imgG_res)
            self.images["Dash_G"].append(imgG)
            imgG = pygame.transform.flip(imgG, True, False)
            self.images_left["Dash_G"].append(imgG)

        for i in range(15):  # DEATH
            img = pygame.image.load(f"Assets/Sprites/Player/Death/{i}.png")
            img_res = img.get_size()
            img = pygame.transform.scale(img, img_res)
            self.images["Death"].append(img)

        for i in range(6):  # HIT
            imgA = pygame.image.load(f"Assets/Sprites/Player/Hit/Air/{i}.png")
            imgG = pygame.image.load(f"Assets/Sprites/Player/Hit/Ground/{i}.png")
            imgA_res = imgA.get_size()
            imgG_res = imgG.get_size()

            imgA = pygame.transform.scale(imgA, imgA_res)
            self.images["Hit_A"].append(imgA)
            imgA = pygame.transform.flip(imgA, True, False)
            self.images_left["Hit_A"].append(imgA)

            imgG = pygame.transform.scale(imgG, imgG_res)
            self.images["Hit_G"].append(imgG)
            imgG = pygame.transform.flip(imgG, True, False)
            self.images_left["Hit_G"].append(imgG)

        for i in range(46):  # FLEX intro
            img = pygame.image.load(f"Assets/Sprites/Player/Intros/Flex/{i}.png")
            img_res = img.get_size()
            img = pygame.transform.scale(img, img_res)
            self.images["Flex"].append(img)

        for i in range(28):  # PANTS intro
            img = pygame.image.load(f"Assets/Sprites/Player/Intros/Pants/{i}.png")
            img_res = img.get_size()
            img = pygame.transform.scale(img, img_res)
            self.images["Pants"].append(img)

        for i in range(5):  # JUMP
            img = pygame.image.load(f"Assets/Sprites/Player/Jump/{i}.png")
            img_res = img.get_size()
            img = pygame.transform.scale(img, img_res)
            self.images["Jump"].append(img)
            img = pygame.transform.flip(img, True, False)
            self.images_left["Jump"].append(img)

        self.health = 3
        self.health_max = 3
        self.damage = 1
        self.all_Projectiles = pygame.sprite.Group()
        self.attack = 5
        self.game = Game()
        self.velocity = 35
        self.image = pygame.image.load(
            "./assets/Player/idle/cuphead_idle_0001.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 370
        self.pvimgs = []
        for i in range(0, 4):
            image = pygame.image.load(
                f'./assets/Sprites/Player/HP/{i}.png')
            self.pvimgs.append(image)
        self.pvimg = self.pvimgs[self.health]
        self.pvrect = self.pvimg.get_rect()
        self.pvrect.x = 10
        self.pvrect.y = 530
        self.time_last_colistion = time.monotonic() - 4
        self.Right = True
        self.is_jumping = False
        self.jumpGravity = 10
        self.jump_height = 60
        self.jump_Velocity = self.jump_height

    def Lancer_Projectile(self):
        if self.Right:
            self.all_Projectiles.add(Projectile(self, True))
        else:
            self.all_Projectiles.add(Projectile(self, False))

    def moveRight(self):
        if not self.game.check_collition(self, self.game.all_ennemy):
            self.rect.x += self.velocity
            self.Right = True

    def PlayerJump(self):
        self.rect.y -= self.jump_Velocity
        self.jump_Velocity -= self.jumpGravity
        if self.jump_Velocity < - self.jump_height:
            self.jump_Velocity = self.jump_height
            self.is_jumping = False

    def moveLeft(self):
        if not self.game.check_collition(self, self.game.all_ennemy):
            self.Right = False
            self.rect.x -= self.velocity



class Projectile(pygame.sprite.Sprite):

    def __init__(self, Player, Right):
        super().__init__()
        self.Bullet = []
        for i in range(1, 8):
            image = pygame.image.load(
                f'./assets/Arme/BNorm_{i}.png')
            image = pygame.transform.scale(image, (50, 20))
            self.Bullet.append(image)

        self.velocity = random.randint(57, 60)
        self.Player = Player
        self.Right = Right

        self.current_frame = 0
        self.image = pygame.image.load("./assets/Arme/BNorm_1.png")
        self.image = pygame.transform.scale(self.image, (50, 20))
        self.rect = self.image.get_rect()
        if self.Right:
            self.rect.x = Player.rect.x+70
        else:
            self.rect.x = Player.rect.x-45
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect.y = Player.rect.y+25+random.randint(1, 20)
        self.direction = "none"

    def move(self):
        if self.direction == "none" or self.direction == "Right":
            self.rect.x += self.velocity
            self.current_frame = (self.current_frame + 1) % len(self.Bullet)
            self.image = self.Bullet[self.current_frame]
            for monster in self.Player.game.check_collition(self, self.Player.game.all_ennemy):
                self.Player.all_Projectiles.remove(self)
                monster.damage(self.Player.attack)
            self.direction = "Right"
            if self.rect.x > 1024 or self.Player.game.check_collition(self, self.Player.game.all_ennemy):
                self.Player.all_Projectiles.remove(self)

    def moveLeft(self):
        if self.direction == "none" or self.direction == "Left":
            self.rect.x -= self.velocity
            self.current_frame = (self.current_frame + 1) % len(self.Bullet)
            self.image = pygame.transform.flip(
                self.Bullet[self.current_frame], True, False)
            for monster in self.Player.game.check_collition(self, self.Player.game.all_ennemy):
                self.Player.all_Projectiles.remove(self)
                monster.damage(self.Player.attack)
            if self.rect.x < 0 or self.Player.game.check_collition(self, self.Player.game.all_ennemy):
                self.Player.all_Projectiles.remove(self)
            self.direction = "Left"


class Game:
    def __init__(self):
        pass
