import pygame
import time
import random


projectiles = list()


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


def image_load():
    idle = list()
    idle_left = list()

    projectiles = list()

    hit = list()
    hit_left = list()

    shoot = list()
    shoot_left = list()

    run = list()
    run_left = list()

    jump = list()
    jump_left = list()

    run_shoot = list()
    run_shoot_left = list()

    death = list()

    dash = list()
    dash_left = list()

    intro_p = list()
    intro_f = list()

    health = list()

    for i in range(5):  # IDLE
        img = pygame.image.load(f"Assets/Sprites/Player/Idle/{i}.png")
        img = pygame.transform.scale(img, (65, 95))
        idle.append(img)
        img = pygame.transform.flip(img, True, False)
        idle_left.append(img)

    for i in range(6):  # SHOOT
        img = pygame.image.load(f"Assets/Sprites/Player/Shoot/{i}.png")
        img = pygame.transform.scale(img, (85, 95))
        shoot.append(img)
        img = pygame.transform.flip(img, True, False)
        shoot_left.append(img)

    for i in range(16):  # RUN + RUN 'N' SHOOT
        img = pygame.image.load(f"Assets/Sprites/Player/Run/Normal/{i}.png")
        img = pygame.transform.scale(img, (85, 95))
        run.append(img)
        img = pygame.transform.flip(img, True, False)
        run_left.append(img)

        img = pygame.image.load(f"Assets/Sprites/Player/Run/Shooting/{i}.png")
        img = pygame.transform.scale(img, (85, 95))
        run_shoot.append(img)
        img = pygame.transform.flip(img, True, False)
        run_shoot_left.append(img)

    for i in range(5):  # JUMP
        img = pygame.image.load(f"Assets/Sprites/Player/Jump/{i}.png")
        img = pygame.transform.scale(img, (65, 75))
        jump.append(img)
        img = pygame.transform.flip(img, True, False)
        jump_left.append(img)

    for i in range(6):  # HIT
        img = pygame.image.load(f"Assets/Sprites/Player/Hit/{i}.png")
        img = pygame.transform.scale(img, (85, 95))
        hit.append(img)
        img = pygame.transform.flip(img, True, False)
        hit_left.append(img)

    for i in range(16):  # DEATH
        img = pygame.image.load(f"Assets/Sprites/Player/Death/{i}.png")
        img = pygame.transform.scale(img, (85, 95))
        death.append(img)

    for i in range(46):  # FLEX intro
        img = pygame.image.load(f"Assets/Sprites/Player/Intros/Flex/{i}.png")
        img = pygame.transform.scale(img, (85, 95))
        intro_f.append(img)

    for i in range(28):  # PANTS intro
        img = pygame.image.load(f"Assets/Sprites/Player/Intros/Pants/{i}.png")
        img = pygame.transform.scale(img, (85, 95))
        intro_p.append(img)

    for i in range(7):  # PROJECTILES
        img = pygame.image.load(f"Assets/Sprites/Projectile/{i}.png")
        img = pygame.transform.scale(img, (50, 20))
        projectiles.append(img)

    # for i in range(8):  # DASH
    #     imgA = pygame.image.load(f"Assets/Sprites/Player/Dash/Air/{i}.png")
    #     imgG = pygame.image.load(f"Assets/Sprites/Player/Dash/Ground/{i}.png")
    #     imgA_res = imgA.get_size()
    #     imgG_res = imgG.get_size()
    #
    #     imgA = pygame.transform.scale(imgA, imgA_res)
    #     self.images["Dash_A"].append(imgA)
    #     imgA = pygame.transform.flip(imgA, True, False)
    #     self.images_left["Dash_A"].append(imgA)
    #
    #     imgG = pygame.transform.scale(imgG, imgG_res)
    #     self.images["Dash_G"].append(imgG)
    #     imgG = pygame.transform.flip(imgG, True, False)
    #     self.images_left["Dash_G"].append(imgG)

    f_idle = 0
    f_shoot = 0
    f_jump = 0
    f_run = 0
    f_run_shoot = 0
    f_hit = 0
    #  TODO: REARRANGE THIS BULLSHIT
    return (idle, idle_left, shoot, shoot_left, run, run_left, f_idle, f_shoot, f_run, f_run_shoot, jump, jump_left,
            f_jump, f_run_shoot, run_shoot, run_shoot_left, f_hit, hit)


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.health_huds = list()
        for i in range(4):  # HEALTH
            img = pygame.image.load(f"Assets/Sprites/Player/HP/{i}.png")
            self.health_huds.append(img)
        self.health = 3
        self.health_max = 3
        self.damage = 1
        self.all_projectiles = pygame.sprite.Group()
        self.attack = 5
        self.game = Game()
        self.velocity = 35
        self.image = pygame.image.load(
            "Assets/Sprites/Player/Idle/0.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 370
        self.health_hud = self.health_huds[self.health]
        self.health_hud_rect = self.health_hud.get_rect()
        self.health_hud.x = 10
        self.health_hud.y = 530
        self.time_last_colistion = time.monotonic() - 4
        self.facing = True
        self.jump_state = False
        self.jump_gravity = 10
        self.jump_height = 60
        self.jump_velocity = self.jump_height

    def spawn_projectile(self):
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
    def __init__(self, player, facing_right):
        super().__init__()

        self.velocity = 50
        self.player = player
        self.facing_right = facing_right

        self.current_frame = 0
        self.image = pygame.image.load("Assets/Sprites/Projectile/0.png")
        self.image = pygame.transform.scale(self.image, (50, 20))
        self.rect = self.image.get_rect()
        if self.facing_right:
            self.rect.x = player.rect.x + 70
        else:
            self.rect.x = player.rect.x - 45
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect.y = player.rect.y + 25 + random.randint(1, 20)
        self.direction = 0  # 0 = None, 1 = Right, 2 = Left

    def move(self):
        if self.direction == 0 or self.direction == 1:
            self.rect.x += self.velocity
            self.current_frame = (self.current_frame + 1) % len(projectiles)
            self.image = projectiles[self.current_frame]
            for monster in self.Player.game.check_collition(self, self.Player.game.all_ennemy):
                self.Player.all_Projectiles.remove(self)
                monster.damage(self.Player.attack)
            self.direction = 1
            if self.rect.x > 1024 or self.Player.game.check_collition(self, self.Player.game.all_ennemy):
                self.Player.all_Projectiles.remove(self)

    def move_left(self):
        if self.direction == 0 or self.direction == 2:
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


class Game:
    def __init__(self):
        self.all_player = pygame.sprite.Group()
        self.Player = Player(self)
        self.all_player.add(self.Player)

        self.son = pygame.mixer.Sound(
            './assets/son/Cuphead-Menu-Original-Theme-Song.mp3')

        # groupe de monstre
        self.all_ennemy = pygame.sprite.Group()
        self.pressed = {}
        self.is_Playing = False

    def game_start(self):
        self.spawn_Ennemy(flowergunt)
        self.spawn_Ennemy(flowergunt)

        # self.spawn_Ennemy()
        self.is_Playing = True

    def game_over(self):
        self.all_ennemy = pygame.sprite.Group()
        self.Player.health = self.Player.max_health
        self.son.play(loops=-1)
        self.fpsTitle = 0
        self.is_Playing = False

    def update(self, game, screen, player_idle, player_idleLeft, player_idleRight, Shoot, ShootLeft, run, runRev, current_frame, current_frame_Shoot, current_frame_run):
        # game.Player.update_health_bar(screen)
        screen.blit(game.Player.pvimg, game.Player.pvrect)

        # Pour Courire vers la droite
        if game.pressed.get(pygame.K_RIGHT) and not game.pressed.get(pygame.K_LEFT):
            screen.blit(run[current_frame_run], game.Player.rect)
            current_frame_run = (current_frame_run + 1) % len(run)
            player_idle = player_idleRight
            if game.Player.rect.x < 880:
                game.Player.moveRight()

            # Pour Courire vers la Gauche
        if game.pressed.get(pygame.K_LEFT) and not game.pressed.get(pygame.K_RIGHT):
            screen.blit(runRev[current_frame_run], game.Player.rect)
            current_frame_run = (current_frame_run + 1) % len(runRev)
            player_idle = player_idleLeft
            if game.Player.rect.x > 60:
                game.Player.moveLeft()
        # On definit si le projectile vas ver la droite ou vers la gauche
        for projectile in game.Player.all_Projectiles:
            if Projectile.direction == "none":
                if player_idle == player_idleRight:

                    projectile.move()
                else:
                    projectile.moveLeft()
            elif Projectile.direction == "Right":
                projectile.move()
            elif Projectile.direction == "Left":
                projectile.moveLeft()

        # Lancer Projectile et Animation Idle du player
        if game.pressed.get(pygame.K_z):
            # Lancer le projectile
            game.Player.Lancer_Projectile()
            # idle vers la gauche
            if player_idle == player_idleLeft:
                tmp = pygame.transform.flip(
                    Shoot[current_frame_Shoot], True, False)
                screen.blit(tmp, game.Player.rect)
                current_frame_Shoot = (current_frame_Shoot + 1) % len(Shoot)
            # idle vers la droite
            else:
                screen.blit(Shoot[current_frame_Shoot], game.Player.rect)
                current_frame_Shoot = (current_frame_Shoot + 1) % len(Shoot)
            # recuperer les projectile du joueur

        elif (not game.pressed.get(pygame.K_RIGHT) and not game.pressed.get(pygame.K_LEFT)) or (game.pressed.get(pygame.K_RIGHT) and game.pressed.get(pygame.K_LEFT)):
            game.Player.image = player_idle[current_frame]
            screen.blit(game.Player.image, game.Player.rect)
            current_frame = (current_frame + 1) % len(player_idle)

        for monster in game.all_ennemy:
            monster.forward()
            # monster.update_health_bar(screen)

        game.Player.all_Projectiles.draw(screen)

        # appliquer l'ensemble des image de mon groupe d'enemy
        game.all_ennemy.draw(screen)
        pygame.time.wait(70)

    def spawn_Ennemy(self, Ennemy_class_name):
        ennemy = Ennemy_class_name(self)
        self.all_ennemy.add(ennemy)

    def check_collition(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
