from utilities import *
from sprites import *

class SceneBase:
    mouse = Mouse()
    general_group = pygame.sprite.Group()
    general_group.add(mouse)

    def render_cursor(self, screen):
        self.general_group.draw(screen)
        self.general_group.update()

    def __init__(self):
        self.next = self

    def input(self, events, pressed_keys):
        print("ProcessInputClass")

    def update(self):
        print("UpdateClass")

    def render(self, screen):
        print("RenderClass")

    def switch_scene(self, scene):
        self.next = scene

    def terminate(self):
        self.switch_scene(None)

class Game(SceneBase):
    find = 0
    moves = 0
    lives = 10

    global_position_list = []
    enemy_position_list = []
    player_direction_history = []
    enemy_direction_history = []
    setup = draw_field(558, 138)
    field_group = setup[0]

    sudoku_list = []
    for i in range(len(setup[1][1])):
        for j in range(len(setup[1][1][i])):
            if setup[1][1][i][j] != setup[1][0][i][j]:
                sudoku_list.append(setup[1][1][i][j])
    find = rng.choice(sudoku_list)
    player = Snake(558, 138, player = True, head = True)
    enemy = Snake(558+800, 138+800, player = False, head = True)
    enemygroup = pygame.sprite.Group()
    snake_group = pygame.sprite.Group()

    def __init__(self):
        SceneBase.__init__(self)
        self.enemygroup.add(self.enemy)
        self.snake_group.add(self.player, self.enemy)
        pygame.mixer.music.load('Assets/sounds/sandadder_slow.mp3')
        pygame.mixer.music.play(-1)
        timer(3)
        for i in range(10):
            self.global_position_list.append([self.player.x, self.player.y])
            self.enemy_position_list.append([self.enemy.x, self.enemy.y])
            self.player_direction_history.append(self.player.moves_currently)
            self.enemy_direction_history.append(self.enemy.moves_currently)

    def collision_handler(self):
        fields = pygame.sprite.spritecollide(self.player, self.field_group, False)
        just_a_fleshwound = pygame.sprite.spritecollide(self.player, self.player.segments, False)
        snake_eats_snake = pygame.sprite.spritecollide(self.player, self.enemy.segments, False)
        enemy_eats_egg = pygame.sprite.spritecollide(self.enemy, self.field_group, False)
        enemy_kills = pygame.sprite.spritecollide(self.player, self.enemygroup, False)

        if self.player.moves_currently == "l":
            for field in fields:
                field.occupied_by_player = False

            self.player.back, self.player.left, self.player.right, self.player.up = [100, 0], [0, 100], [0, -100], [-100, 0]
        if self.player.moves_currently == "r":
            for field in fields:
                field.occupied_by_player = False

            self.player.back, self.player.left, self.player.right, self.player.up = [-100, 0], [0, -100], [0, 100], [100, 0]
        if self.player.moves_currently == "u":
            for field in fields:
                field.occupied_by_player = False

            self.player.back, self.player.left, self.player.right, self.player.up = [0, 100], [-100, 0], [100, 0], [0, -100]
        if self.player.moves_currently == "d":
            for field in fields:
                field.occupied_by_player = False

            self.player.back, self.player.left, self.player.right, self.player.up = [0, -100], [100, 0], [-100, 0], [0, 100]

        if self.enemy.moves_currently == "l":
            self.enemy.back, self.enemy.left, self.enemy.right, self.enemy.up = [100, 0], [0, 100], [0, -100], [-100, 0]
        if self.enemy.moves_currently == "r":
            self.enemy.back, self.enemy.left, self.enemy.right, self.enemy.up = [-100, 0], [0, -100], [0, 100], [100, 0]
        if self.enemy.moves_currently == "u":
            self.enemy.back, self.enemy.left, self.enemy.right, self.enemy.up = [0, 100], [-100, 0], [100, 0], [0, -100]
        if self.enemy.moves_currently == "d":
            self.enemy.back, self.enemy.left, self.enemy.right, self.enemy.up = [0, -100], [100, 0], [-100, 0], [0, 100]

        for any in snake_eats_snake:
            if any.x == self.player.x and any.y == self.player.y:
                self.switch_scene(Lose())

        for any in enemy_kills:
            if any.x == self.player.x and any.y == self.player.y:
                pygame.mixer.music.stop()
                self.switch_scene(Lose())

        for segment in snake_eats_snake:
            if segment.x == self.enemy.x and segment.y == self.enemy.y:
                self.switch_scene(Lose())

        for collider in just_a_fleshwound:
            if collider.x == self.player.x and collider.y == self.player.y:
                play_sound("Assets/sounds/hiss.mp3")
                play_sound("Assets/sounds/ouch.mp3")
                pygame.mixer.music.stop()
                self.switch_scene(Lose())

        for egg in enemy_eats_egg:
            if egg.rect.centerx == self.enemy.x and egg.rect.centery == self.enemy.y:
                egg.occupied_by_enemy = True
            else:
                egg.occupied_by_enemy = False

            if egg.egg_placed and egg.rect.center[0] == self.enemy.x and egg.rect.center[1] == self.enemy.y:
                self.enemy.add_segment()
                egg.wrongen()
                egg.eggbreak()
                self.lives -= 1
                if len(self.sudoku_list) > 1:
                    play_sound("Assets/sounds/ouch.mp3")

        for field in fields:
            if field.rect.centerx == self.player.x and field.rect.centery == self.player.y:
                field.occupied_by_player = True
            else:
                field.occupied_by_player = False

            if field.egg_placed and field.rect.center[0] == self.player.x and field.rect.center[1] == self.player.y:
                self.enemy.add_segment()
                field.wrongen()
                field.eggbreak()
                self.lives -= 1
                if len(self.sudoku_list) > 1:
                    play_sound("Assets/sounds/ouch.mp3")

    def enemy_mover(self):
        moves = self.enemy.get_current_moves()
        decision = rng.choice(moves)
        if decision == "u":
            if self.enemy.y != 138:
                self.enemy.y -= 100
                self.enemy.animate("move")
            else:
                self.enemy.animate("born")
                self.enemy.y = 138+800
        elif decision == "d":
            if self.enemy.y != 138+800:
                self.enemy.y += 100
                self.enemy.animate("move")
            else:
                self.enemy.animate("born")
                self.enemy.y = 138
        elif decision == "r":
            if self.enemy.x != 558+800:
                self.enemy.x += 100
                self.enemy.animate("move")
            else:
                self.enemy.animate("born")
                self.enemy.x = 558

        elif decision == "l":
            if self.enemy.x != 558:
                self.enemy.x -= 100
                self.enemy.animate("move")
            else:
                self.enemy.animate("born")
                self.enemy.x = 558+800
        self.enemy.moves_currently = decision
        self.enemy.last_position = [self.enemy.x, self.enemy.y]
        self.enemy_position_list.insert(0, self.enemy.last_position)
        if len(self.enemy_position_list) > 10:
            self.enemy_position_list.pop()
        self.enemy_direction_history.insert(0, decision)
        if len(self.enemy_direction_history) > 10:
            self.enemy_direction_history.pop()

    def movements(self, events, pressed_keys, zahl1=558, zahl2 = 138, zahl3 = 100, zahl4 = 800):
        self.events, self.pressed_keys = events, pressed_keys
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.player_direction_history.insert(0, self.player.moves_currently)
                if event.key == pygame.K_LEFT and not self.player.moves_currently == "r":
                    if self.player.x == zahl1:
                        self.player.animate("born")
                        self.player.x = zahl1 + zahl4
                    else:
                        self.player.x -= zahl3
                        self.player.animate("move")
                    self.player.last_position = [self.player.x, self.player.y]
                    self.player.moves_currently = "l"
                    play_sound("Assets/sounds/unclick.mp3")
                    self.moves += 1


                if event.key == pygame.K_RIGHT and not self.player.moves_currently == "l":
                    if self.player.x == zahl1 + zahl4:
                        self.player.animate("born")
                        self.player.x = zahl1
                    else:
                        self.player.x += zahl3
                        self.player.animate("move")
                    self.player.last_position = [self.player.x, self.player.y]
                    self.player.moves_currently = "r"
                    play_sound("Assets/sounds/unclick.mp3")
                    self.moves += 1


                if event.key == pygame.K_UP and not self.player.moves_currently == "d":
                    if self.player.y == zahl2:
                        self.player.animate("born")
                        self.player.y = zahl2 + zahl4
                    else:
                        self.player.y -= zahl3
                        self.player.animate("move")
                    self.player.last_position = [self.player.x, self.player.y]
                    self.player.moves_currently = "u"
                    play_sound("Assets/sounds/unclick.mp3")
                    self.moves += 1

                if event.key == pygame.K_DOWN and not self.player.moves_currently == "u":
                    if self.player.y == zahl2 + zahl4:
                        self.player.animate("born")
                        self.player.y = zahl2
                    else:
                        self.player.y += zahl3
                        self.player.animate("move")
                    self.player.last_position = [self.player.x, self.player.y]
                    self.player.moves_currently = "d"
                    play_sound("Assets/sounds/unclick.mp3")
                    self.moves += 1


                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:

                    self.enemy_mover()
                    self.player.last_position = [self.player.x, self.player.y]
                    self.global_position_list.insert(0, self.player.last_position)
                    if len(self.global_position_list) > 10:
                        self.global_position_list.pop()
                    if len(self.player_direction_history) > 10:
                        self.player_direction_history.pop()

                    for field in self.field_group:
                        if field.egg_counter > 0:
                            field.egg_counter -= 1
                        elif field.egg_counter == 0:
                            field.egg_counter = -1
                            self.player.add_segment()
                            field.egged()
                            field.egg_sploded = 5
                        if field.egg_sploded > 0:
                            field.egg_sploded -= 1
                        elif field.egg_sploded == 0:
                            field.eggbreak()
                            field.egg_sploded = -1
                    for element in self.enemy.segments:
                        element.x, element.y = self.enemy_position_list[element.id][0], self.enemy_position_list[element.id][1]
                        element.moves_currently = self.enemy_direction_history[element.id]
                    for element in self.player.segments:
                        element.x, element.y = self.global_position_list[element.id][0], self.global_position_list[element.id][1]
                        element.moves_currently = self.player_direction_history[element.id]

    def input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    for field in self.field_group:
                        if field.occupied_by_player:
                            if field.hidden and field.number == self.find:
                                field.egg_counter = self.player.length
                                play_sound("Assets/sounds/egg.mp3")
                                if len(self.sudoku_list) > 1:
                                    self.sudoku_list.remove(self.find)
                                    self.find = rng.choice(self.sudoku_list)
                            elif field.hidden and field.number != self.find:
                                play_sound("Assets/sounds/hiss.mp3")
                                self.enemy.add_segment()
                        else:
                            pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse.click()
        self.movements(events, pressed_keys)

    def update(self):
        counter["Lives"] = self.lives
        counter["Moves"] = self.moves
        if self.lives == 0:
            self.switch_scene(Lose())
        self.collision_handler()

        if len(self.sudoku_list)==1:
            pygame.mixer.music.stop()
            self.switch_scene(Win())
        for item in self.field_group:
            item.egggroup.update()

        for item in self.snake_group:
            item.segments.update()
            item.update()

    def render(self, screen):
        screen.blit(get_image('Assets/sprites/environment/full_gameboard.png'), (0, 0))

        text = create_text("FIND:", ["fatskellyregular"], 64, (170, 255, 170))
        screen.blit(text, (8, 64))
        screen.blit(get_image('Assets/sprites/environment/ui.png'), (0, 120))
        text = create_text(f"{self.find}", ["sidewinder2022regular"], 140, (20, 86, 20))
        screen.blit(text, (40, 140))

        text = create_text("moves:", ["fatskellyregular"], 60, (170, 200, 170))
        screen.blit(text, (8, 64+128+128))
        screen.blit(get_image('Assets/sprites/environment/ui.png'), (0, 128+ 120 +120))
        text = create_text(f"{self.moves}", ["sidewinder2022regular"], 140, (20, 86, 20))
        screen.blit(text, (40, 140 + 128 + 120))

        text = create_text("lives:", ["fatskellyregular"], 60, (170, 200, 170))
        screen.blit(text, (8, 64 + 128 + 128 +128 +128-8))
        screen.blit(get_image('Assets/sprites/environment/ui.png'), (0, 128+ 128+ 120 + 120 + 120))
        text = create_text(f"{self.lives}", ["sidewinder2022regular"], 140, (20, 86, 20))
        screen.blit(text, (40, 140 + 128 + 120+ 128 +120))

        for item in self.field_group:
            item.egggroup.draw(screen)
            color = (0, 0, 0)
            size = 0
            if item.wrong:
                color = (255, 60, 50)
                size = 128
            elif item.hidden or item.egg_placed:
                pass
            elif item.solved:
                color = (140, 200, 130)
                size = 128
            else:
                color = (21, 27, 12)
                size = 128

            text = create_text(f"{item.number}", ["sidewinder2022regular"], size, color)
            screen.blit(text, (item.rect.x-25, item.rect.y-50))
        for item in self.snake_group:
            item.segments.draw(screen)
        self.snake_group.draw(screen)
        self.field_group.draw(screen)
        self.render_cursor(screen)

class Title(SceneBase):
    grouped = pygame.sprite.Group()
    tongue = Tongue()
    grouped.add(tongue)

    def __init__(self):
        SceneBase.__init__(self)
        pygame.mixer.music.load('Assets/sounds/sandadder.mp3')
        pygame.mixer.music.play(-1)

    def input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.stop()
                self.switch_scene(Game())

    def update(self):
        for tongue in self.grouped:
            tongue.update()

    def render(self, screen):
        text = create_text("SUPER SNAKE SUDOKU:", ["thinpharaoregular"], 128, (44, 144, 58))
        text2 = create_text("Strange Sneaky Skilled Snake", ["thinpharaoregular"], 128, (57, 186, 75))
        text3 = create_text("invader", ["thinpharaoregular"], 128, (70, 228, 92))

        screen.blit(get_image("Assets/sprites/environment/background.png"), (0, 0))
        screen.blit(text, (800 // 2, 240 - text.get_height() // 2))
        screen.blit(text2, (400 // 2, 360 - text2.get_height() // 2))
        screen.blit(text3, (180 // 2, 480 - text2.get_height() // 2))
        screen.blit(get_image("Assets/sprites/environment/accessoire.png"), (80, 550))
        self.grouped.draw(screen)
        self.render_cursor(screen)


class Lose(SceneBase):
    score = int(100+1*(counter["Moves"] * -100) + (counter["Lives"] * 400) * (10000 - counter["Time"]))

    def __init__(self):
        SceneBase.__init__(self)

    def input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.switch_scene(Title())

    def update(self):
        pass

    def render(self, screen):
        screen.blit(get_image("Assets/sprites/environment/lost.png"), (0, 0))

        text = create_text(f"{counter['Moves']}", ["sidewinder2022regular"], 200, (255, 255, 255))
        screen.blit(text, (360, 400-60))
        text = create_text(f"{counter['Lives']}", ["sidewinder2022regular"], 200, (255, 255, 255))
        screen.blit(text, (800, 400))
        text = create_text(f"{int(1000 - counter['Time'])}", ["sidewinder2022regular"], 200, (255, 255, 255))
        screen.blit(text, (1200, 420))
        text = create_text(f"{self.score}", ["sidewinder2022regular"], 240, (255, 255, 255))
        screen.blit(text, (280+ 280 +140 +280 -60, 280 + 140 +140 ))


class Score(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.switch_scene(Title())

    def update(self):
        pass

    def render(self, screen):
        screen.fill((0, 255, 0))


class Win(SceneBase):
    score = int(888 + 1 * (counter["Moves"] * -100) + (counter["Lives"] * 400) * (10000 - counter["Time"]))

    def __init__(self):
        SceneBase.__init__(self)

    def input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.switch_scene(Score())

    def update(self):
        pass

    def render(self, screen):
        screen.blit(get_image("Assets/sprites/environment/won.png"), (0, 0))

        text = create_text(f"{counter['Moves']}", ["sidewinder2022regular"], 200, (255, 255, 255))
        screen.blit(text, (360+256, 400 - 10))
        text = create_text(f"{counter['Lives']}", ["sidewinder2022regular"], 200, (255, 255, 255))
        screen.blit(text, (800+64+16, 400-20))
        text = create_text(f"{int(1000 - counter['Time'])}", ["sidewinder2022regular"], 200, (255, 255, 255))
        screen.blit(text, (1200+64, 420))
        text = create_text(f"{self.score}", ["sidewinder2022regular"], 240, (255, 255, 255))
        screen.blit(text, (1250, 600))


class Splash(SceneBase):
    def __init__(self, version=0):
        SceneBase.__init__(self)
        self.version = version
        if self.version == 1:
            timer(6)
            pygame.mixer.music.load(("Assets/sounds/bartunes_intro.ogg"))
            pygame.mixer.music.play(0)
        else:
            timer(4)

    def input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN or event.type == pygame.USEREVENT + 0 or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.stop()
                if self.version == 1:
                    self.switch_scene(Title())
                else:
                    self.switch_scene(Splash(1))

    def update(self):
        pass

    def render(self, screen):
        screen.fill((0, 0, 0))
        if self.version == 1:
            screen.blit(get_image('Assets/sprites/environment/trexxak.png'), centralize(get_image(
                'Assets/sprites/environment/trexxak.png')))
        else:
            screen.blit(get_image('Assets/sprites/environment/splash.png'), centralize(get_image(
                'Assets/sprites/environment/splash.png')))
