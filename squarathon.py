import pygame
import pygame_gui
from pygame.constants import *
import random

# initializing settings
pygame.mixer.init()
pygame.init()
pygame.display.set_caption('Squarathon')
clock = pygame.time.Clock()

# constant variables
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
STAIR_HEIGHT = 36
PLATFORM_HEIGHT = 200
ROCK_HEIGHT = 100
PLAYER_SIDE = 50
PLAYER_X = 120
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40
BUTTON_X = (SCREEN_WIDTH - BUTTON_WIDTH) / 2
FPS = 60

# changing variables
playerY = SCREEN_HEIGHT - 400 - PLAYER_SIDE / 2
score = 0
change_count = 0
str_speed = 8
has_acced = False
counter = 0
running = True
restart = False
alive = True
faded = False
leader_board = False
saving = False
from_menu = False
game = "start"
cur_theme = "none"
score_url = 'Text/score.txt'
file = open(score_url, "r")
score_lines = file.readlines()

# text input box
input_box = pygame.Rect(270, 270, 140, 32)
color = pygame.Color((255, 255, 255))
name_text = 'Enter Your Name'

# load background music and sound effects
bgm_url = 'Music/bgm.mp3'
pygame.mixer.music.load(bgm_url)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)
click_url = 'Music/click.wav'
button_click_sound = pygame.mixer.Sound(click_url)
jump_url = 'Music/jump.wav'
jump_sound = pygame.mixer.Sound(jump_url)
bubble_url = 'Music/bubbles.wav'
bubble_sound = pygame.mixer.Sound(bubble_url)
explode_url = 'Music/explode.wav'
explode_sound = pygame.mixer.Sound(explode_url)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# buttons settings
# theme_url = 'Text/theme.json'
start_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), 'Text/theme.json')
death_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), 'Text/theme.json')
menu_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), 'Text/theme.json')
back_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), 'Text/theme.json')
start_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((BUTTON_X, 300), (BUTTON_WIDTH, BUTTON_HEIGHT)),
                                         text='Start', manager=start_manager)
leader_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((BUTTON_X, 350), (BUTTON_WIDTH, BUTTON_HEIGHT)),
                                          text='Leader', manager=start_manager)
theme_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((BUTTON_X, 400), (BUTTON_WIDTH, BUTTON_HEIGHT)),
                                         text='Theme', manager=start_manager)
quit_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((BUTTON_X, 450), (BUTTON_WIDTH, BUTTON_HEIGHT)),
                                        text='Quit', manager=start_manager)
retry_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((BUTTON_X, 350), (BUTTON_WIDTH, BUTTON_HEIGHT)),
                                         text='Retry', manager=death_manager)
save_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((BUTTON_X, 400), (BUTTON_WIDTH, BUTTON_HEIGHT)),
                                        text='Save', manager=death_manager)
menu_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((BUTTON_X, 450), (BUTTON_WIDTH, BUTTON_HEIGHT)),
                                        text='Menu', manager=menu_manager)
back_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((BUTTON_X, 450), (BUTTON_WIDTH, BUTTON_HEIGHT)),
                                        text='Back', manager=back_manager)
# font settings
# font_url = 'Font/Devant.ttf'
font = pygame.font.Font('Font/Devant.ttf', 84)
name_font = pygame.font.Font('Font/Devant.ttf', 72)
leader_font = pygame.font.Font('Font/Devant.ttf', 54)


# all classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.centerX = x
        self.centerY = y
        self.player_url = 'Img/cube.png'
        self.surf = pygame.image.load(self.player_url).convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.isJump = False
        self.clear = False
        self.gravity = -0.8
        self.up = 12
        self.veloY = 0
        self.angle = 0
        self.alpha = 256
        self.jumpCount = 0
        self.particles = []

    def update(self):
        self.veloY += self.gravity
        if self.centerY - self.veloY >= playerY:
            self.veloY = 0
            self.isJump = False
            self.jumpCount = 0
        self.centerY -= self.veloY
        self.rect = self.surf.get_rect(center=(self.centerX, self.centerY))

    def jump(self):
        if self.isJump is False:
            if self.jumpCount <= 1:
                self.veloY = self.up
                self.jumpCount += 1
            elif self.jumpCount == 2:
                self.isJump = True
                self.jumpCount = 0

    def trace(self):
        self.particles.append(
            [[self.centerX - PLAYER_SIDE / 2, self.centerY + PLAYER_SIDE / 2], [-2, random.randint(0, 20) / 10 - 1],
             random.randint(6, 8)])
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            pygame.draw.rect(screen, (0, 210, 233),
                             [int(particle[0][0]), int(particle[0][1]), int(particle[2]), int(particle[2])])
            if particle[2] <= 0:
                self.particles.remove(particle)

    def fadeout(self):
        if self.centerY >= 480:
            self.centerY += 2.5
            self.rect = self.surf.get_rect(center=(self.centerX, self.centerY))
        self.alpha = max(0, self.alpha - 8)
        self.surf.set_alpha(self.alpha)
        self.particles.append(
            [[self.centerX, self.centerY], [random.randint(0, 40) / 10 - 2, random.randint(0, 40) / 10 - 2],
             random.randint(4, 6)])
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            pygame.draw.circle(screen, (0, 210, 233), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles.remove(particle)
        if self.alpha == 0:
            self.clear = True


class Stair(pygame.sprite.Sprite):
    def __init__(self, width, y, dist, speed):
        super(Stair, self).__init__()
        self.width = width
        self.centerX = SCREEN_WIDTH + dist + self.width / 2
        self.centerY = y
        self.surf = pygame.Surface((self.width, STAIR_HEIGHT))
        self.surf.fill((0, 0, 0))
        self.speed = speed
        self.rand = random.randint(1, 3)
        self.yMove = 0
        # if self.rand == 1:
        #     self.yMove = 0
        # elif self.rand == 2:
        #     self.yMove = 2
        # elif self.rand == 3:
        #     self.yMove = -2

    def draw(self):
        self.rect = self.surf.get_rect(center=(self.centerX, self.centerY))

    def update(self):
        global score
        self.centerX = self.rect.left + self.width / 2
        self.rect.move_ip(-self.speed, 0)
        if self.rect.top < 150:
            self.yMove = 5
        if self.rect.bottom > 500:
            self.yMove = -5
        self.rect.move_ip(0, self.yMove)
        if self.rect.right <= 0:
            score += 1
            self.kill()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Platform, self).__init__()
        self.centerX = x
        self.centerY = y
        self.speed = 8
        self.surf = pygame.Surface((SCREEN_WIDTH, 400))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center=(self.centerX, self.centerY))

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right <= (PLAYER_X + PLAYER_SIDE / 2):
            global playerY
            playerY = 500
        if self.rect.right <= 0:
            self.kill()


class TopRock(pygame.sprite.Sprite):
    def __init__(self):
        super(TopRock, self).__init__()
        self.speed = 8
        self.top_url = 'Img/top.png'
        self.surf = pygame.image.load(self.top_url).convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, 50))

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.left < -1 * SCREEN_WIDTH - 40:
            self.rect = self.surf.get_rect(center=(SCREEN_WIDTH * 3 / 2, 50))


class OutsideTopRock(pygame.sprite.Sprite):
    def __init__(self):
        super(OutsideTopRock, self).__init__()
        self.speed = 8
        self.top_url = 'Img/top.png'
        self.surf = pygame.image.load(self.top_url).convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH * 3 / 2, 50))

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.left < -1 * SCREEN_WIDTH - 40:
            self.rect = self.surf.get_rect(center=(SCREEN_WIDTH * 3 / 2, 50))


class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super(Wall, self).__init__()
        self.alpha = 255
        self.centerY = SCREEN_HEIGHT / 2
        self.bg1_url = 'Img/bg1.png'
        self.surf = pygame.image.load(self.bg1_url).convert_alpha()
        self.surf.set_alpha(self.alpha)
        self.rect = self.surf.get_rect(center=((SCREEN_WIDTH / 2), self.centerY))

    def fadein(self):
        if self.alpha < 255:
            self.surf.set_alpha(self.alpha)
            self.alpha = min(255, self.alpha + 8)
            screen.blit(self.surf, self.rect)

    def fadeout(self):
        if self.alpha > 0:
            self.surf.set_alpha(self.alpha)
            self.alpha = max(0, self.alpha - 8)
            screen.blit(self.surf, self.rect)


class Wall2(pygame.sprite.Sprite):
    def __init__(self):
        super(Wall2, self).__init__()
        self.alpha = 0
        self.centerY = SCREEN_HEIGHT / 2
        self.bg2_url = 'Img/bg2.png'
        self.surf = pygame.image.load(self.bg2_url).convert_alpha()
        self.surf.set_alpha(self.alpha)
        self.rect = self.surf.get_rect(center=((SCREEN_WIDTH / 2), self.centerY))

    def fadein(self):
        if self.alpha < 255:
            self.surf.set_alpha(self.alpha)
            self.alpha = min(255, self.alpha + 8)
            screen.blit(self.surf, self.rect)

    def fadeout(self):
        if self.alpha > 0:
            self.surf.set_alpha(self.alpha)
            self.alpha = max(0, self.alpha - 8)
            screen.blit(self.surf, self.rect)


class Wall3(pygame.sprite.Sprite):
    def __init__(self):
        super(Wall3, self).__init__()
        self.alpha = 0
        self.centerY = SCREEN_HEIGHT / 2
        self.bg3_url = 'Img/bg3.png'
        self.surf = pygame.image.load(self.bg3_url).convert_alpha()
        self.surf.set_alpha(self.alpha)
        self.rect = self.surf.get_rect(center=((SCREEN_WIDTH / 2), self.centerY))

    def fadein(self):
        if self.alpha < 255:
            self.surf.set_alpha(self.alpha)
            self.alpha = min(255, self.alpha + 8)
            screen.blit(self.surf, self.rect)

    def fadeout(self):
        if self.alpha > 0:
            self.surf.set_alpha(self.alpha)
            self.alpha = max(0, self.alpha - 8)
            screen.blit(self.surf, self.rect)


class Day(pygame.sprite.Sprite):
    def __init__(self):
        super(Day, self).__init__()
        self.alpha = 255
        self.centerY = (SCREEN_HEIGHT - PLATFORM_HEIGHT) / 2
        self.day_url = 'Img/day.png'
        self.surf = pygame.image.load(self.day_url).convert_alpha()
        self.surf.set_alpha(self.alpha)
        self.rect = self.surf.get_rect(center=((SCREEN_WIDTH / 2), self.centerY))

    def fadein(self):
        if self.alpha < 255:
            self.surf.set_alpha(self.alpha)
            self.alpha = min(255, self.alpha + 8)
            screen.blit(self.surf, self.rect)

    def fadeout(self):
        if self.alpha > 0:
            self.surf.set_alpha(self.alpha)
            self.alpha = max(0, self.alpha - 8)
            screen.blit(self.surf, self.rect)


class Night(pygame.sprite.Sprite):
    def __init__(self):
        super(Night, self).__init__()
        self.alpha = 0
        self.centerY = (SCREEN_HEIGHT - PLATFORM_HEIGHT) / 2
        self.night_url = 'Img/night.png'
        self.surf = pygame.image.load(self.night_url).convert_alpha()
        self.surf.set_alpha(self.alpha)
        self.rect = self.surf.get_rect(center=((SCREEN_WIDTH / 2), self.centerY))

    def fadein(self):
        if self.alpha < 255:
            self.surf.set_alpha(self.alpha)
            self.alpha = min(255, self.alpha + 8)
            screen.blit(self.surf, self.rect)

    def fadeout(self):
        if self.alpha > 0:
            self.surf.set_alpha(self.alpha)
            self.alpha = max(0, self.alpha - 8)
            screen.blit(self.surf, self.rect)


# declaring classes
player = Player(PLAYER_X, (SCREEN_HEIGHT - PLATFORM_HEIGHT - PLAYER_SIDE / 2))
all_obstacles = pygame.sprite.Group()
stairs = pygame.sprite.Group()
top_rock = TopRock()
outside_top_rock = OutsideTopRock()
platform = Platform(SCREEN_WIDTH / 2, (SCREEN_HEIGHT - PLATFORM_HEIGHT))
wall = Wall()
wall2 = Wall2()
wall3 = Wall3()
day = Day()
night = Night()
all_sprites = pygame.sprite.Group()
all_sprites.add(platform)
all_sprites.add(player)

while running:
    time_delta = clock.tick(FPS)
    screen.fill((0, 0, 0))
    if game == "start":
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    button_click_sound.play()
                    if event.ui_element == start_btn:
                        player.centerY = SCREEN_HEIGHT - 400 - PLAYER_SIDE / 2
                        game = "play"
                    elif event.ui_element == leader_btn:
                        leader_board = True
                    elif event.ui_element == theme_btn:
                        if cur_theme == "day":
                            cur_theme = "night"
                        elif cur_theme == "night":
                            cur_theme = "day"
                        elif cur_theme == "none":
                            cur_theme = "night"
                    elif event.ui_element == quit_btn:
                        running = False
                    elif event.ui_element == menu_btn:
                        leader_board = False
                        file.close()
            if leader_board:
                menu_manager.process_events(event)
            else:
                start_manager.process_events(event)
        if cur_theme == "day":
            if night.alpha > 0:
                day.fadein()
                night.fadeout()
            screen.blit(day.surf, day.rect)
        elif cur_theme == "night":
            if day.alpha > 0:
                day.fadeout()
                night.fadein()
            screen.blit(night.surf, night.rect)
        elif cur_theme == "none":
            screen.blit(day.surf, day.rect)

        if leader_board:
            for i in range(0, len(score_lines) - 1, 2):
                tmp_name = score_lines[i] + "          " + score_lines[i + 1]
                leader_text = leader_font.render(tmp_name, True, (255, 255, 255))
                leader_textRect = leader_text.get_rect()
                leader_textRect.center = (SCREEN_WIDTH / 2 + 30, 80 + 70 * i / 2)
                screen.blit(leader_text, leader_textRect)
            menu_manager.update(time_delta)
            menu_manager.draw_ui(screen)
        else:
            start_manager.update(time_delta)
            start_manager.draw_ui(screen)
            title_text = font.render("Squarathon", True, (255, 255, 255))
            title_textRect = title_text.get_rect()
            title_textRect.center = (SCREEN_WIDTH / 2, int((SCREEN_HEIGHT - PLATFORM_HEIGHT) / 3) + 35)
            screen.blit(title_text, title_textRect)

        player.rect = player.surf.get_rect(center=(player.centerX, player.centerY))
        if not leader_board:
            screen.blit(top_rock.surf, top_rock.rect)
            screen.blit(outside_top_rock.surf, outside_top_rock.rect)
            top_rock.update()
            outside_top_rock.update()
        screen.blit(player.surf, player.rect)
        player.trace()
        pygame.display.update()

    elif game == "play":
        if restart:
            if not from_menu:
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(loops=-1)
            elif from_menu:
                from_menu = False
            playerY = SCREEN_HEIGHT - 400 - PLAYER_SIDE / 2
            score = 0
            change_count = 0
            str_speed = 8
            running = True
            restart = False
            game = "play"
            alive = True
            counter = 0
            player.__init__(PLAYER_X, playerY - 30)
            all_obstacles = pygame.sprite.Group()
            stairs = pygame.sprite.Group()
            platform.__init__(SCREEN_WIDTH / 2, (SCREEN_HEIGHT - PLATFORM_HEIGHT))
            wall.__init__()
            wall2.__init__()
            wall3.__init__()
            day.__init__()
            all_sprites = pygame.sprite.Group()
            all_sprites.add(platform)
            all_sprites.add(player)

        score_text = font.render(str(score), True, (255, 255, 255))
        score_textRect = score_text.get_rect()
        score_textRect.center = (SCREEN_WIDTH / 2, int((SCREEN_HEIGHT - PLATFORM_HEIGHT) / 3) - 30)

        if score == 0 or score % 10 != 0 or faded:
            if score % 30 < 10:
                screen.blit(wall.surf, wall.rect)
            elif score % 30 < 20:
                screen.blit(wall2.surf, wall2.rect)
            elif score % 30 < 30:
                screen.blit(wall3.surf, wall3.rect)
            faded = False

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_SPACE:
                    player.jump()
                    if not player.isJump:
                        jump_sound.play()

        if alive and counter % 60 == 0:
            new_stair = Stair(random.randint(120, 200), random.randint(240, 350), random.randint(10, 150), str_speed)
            new_stair.draw()
            stairs.add(new_stair)
            all_sprites.add(new_stair)
            counter = 0

        counter += 1

        if score > 0 and score % 10 == 0:
            if (score / 10) % 3 == 1:
                wall.fadeout()
                wall2.fadein()
            elif (score / 10) % 3 == 2:
                wall3.fadein()
                wall2.fadeout()
            elif (score / 10) % 3 == 0:
                wall.fadein()
                wall3.fadeout()
            faded = True

        if alive:
            all_sprites.update()

        if not alive and player.alpha > 0:
            player.fadeout()

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        screen.blit(score_text, score_textRect)

        if score % 10 == 0 and score > 0 and not has_acced:
            str_speed += 1
            for obstacle in all_obstacles:
                obstacle.speed = str_speed
            has_acced = True
        elif score % 10 == 1:
            has_acced = False

        if alive:
            player.trace()

        if pygame.sprite.spritecollideany(player, stairs) and alive:
            spr = pygame.sprite.spritecollideany(player, stairs)
            if spr.rect.left <= player.rect.right and (player.rect.bottom - 31) <= spr.rect.top:
                player.centerY = (spr.rect.top - 31)
                player.veloY = 0
                player.isJump = False
                player.jumpCount = 0
            else:
                explode_sound.play()
                pygame.mixer.music.fadeout(1)
                alive = False
                player.particles.clear()

        if player.centerY >= 480 and alive:
            bubble_sound.play()
            pygame.mixer.music.fadeout(1)
            alive = False
            player.particles.clear()

        if player.clear:
            game = "death"

        pygame.display.update()

    elif game == "death":
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif saving:
                    if event.key == pygame.K_RETURN:
                        file = open(score_url, "r")
                        score_lines = file.readlines()
                        str1 = name_text + "\n"
                        if str1 in score_lines:
                            str2 = str(max(score, int(score_lines[score_lines.index(str1) + 1]))) + "\n"
                            score_lines.remove(score_lines[score_lines.index(str1) + 1])
                            score_lines.remove(str1)
                        else:
                            str2 = str(score) + "\n"
                        if len(score_lines) == 0:
                            score_lines.append(str1)
                            score_lines.append(str2)
                        else:
                            for i in range(1, len(score_lines), 2):
                                if int(str2) > int(score_lines[i]):
                                    score_lines.insert(i - 1, str1)
                                    score_lines.insert(i, str2)
                                    break
                                elif i == len(score_lines) - 1:
                                    score_lines.append(str1)
                                    score_lines.append(str2)
                        file.close()
                        file = open(score_url, "w")
                        for line in score_lines:
                            file.writelines(line)
                        name_text = 'Enter Your Name'
                        saving = False
                        file.close()
                    elif event.key == pygame.K_BACKSPACE:
                        name_text = name_text[:-1]
                    else:
                        if name_text == "Enter Your Name":
                            name_text = event.unicode
                        else:
                            name_text += event.unicode
            elif event.type == QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    button_click_sound.play()
                    if event.ui_element == retry_btn:
                        restart = True
                        game = "play"
                    elif event.ui_element == save_btn:
                        saving = True
                    elif event.ui_element == menu_btn:
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(loops=-1)
                        playerY = 350
                        player = Player(PLAYER_X, (SCREEN_HEIGHT - PLATFORM_HEIGHT - PLAYER_SIDE / 2))
                        day.surf.set_alpha(255)
                        restart = True
                        from_menu = True
                        game = "start"
                    elif event.ui_element == back_btn:
                        saving = False
                    elif event.ui_element == quit_btn:
                        running = False

            if saving:
                back_manager.process_events(event)
            else:
                death_manager.process_events(event)
                menu_manager.process_events(event)

        if score % 30 < 10:
            wall.surf.set_alpha(255)
            screen.blit(wall.surf, wall.rect)
        elif score % 30 < 20:
            wall2.surf.set_alpha(255)
            screen.blit(wall2.surf, wall2.rect)
        elif score % 30 < 30:
            wall3.surf.set_alpha(255)
            screen.blit(wall3.surf, wall3.rect)

        d_str = "You   scored   " + str(score)

        dscore_text = font.render(d_str, True, (255, 255, 255))
        dscore_textRect = dscore_text.get_rect()
        dscore_textRect.center = (SCREEN_WIDTH / 2, 250)

        player.kill()
        all_sprites.remove(player)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        trans_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        trans_surf.fill((0, 0, 0))
        trans_surf.set_alpha(100)
        trans_rect = trans_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(trans_surf, trans_rect)

        screen.blit(dscore_text, dscore_textRect)

        if saving:
            txt_surface = name_font.render(name_text, True, color)
            input_box.w = txt_surface.get_width() + 10
            screen.blit(txt_surface, (SCREEN_WIDTH / 2 - input_box.w / 2, 330))
            back_manager.update(time_delta)
            back_manager.draw_ui(screen)
        else:
            death_manager.update(time_delta)
            death_manager.draw_ui(screen)
            menu_manager.update(time_delta)
            menu_manager.draw_ui(screen)

        pygame.display.update()

button_click_sound.stop()
jump_sound.stop()
bubble_sound.stop()
pygame.mixer.music.stop()
pygame.mixer.quit()
