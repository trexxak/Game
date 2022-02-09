import pygame
from utilities import get_image, play_sound, counter
from numpy import random as rng
from sudoku import generate_sudoku

class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.current_sprite = 0
        self.idle = []
        self.clicked = []
        self.current_spriteset = self.idle
        for i in range(2):
            self.idle.append(get_image(f'Assets/sprites/mouse/idle_{i}.png'))
            self.clicked.append(get_image(f'Assets/sprites/mouse/click_{i}.png'))
        self.image = self.idle[self.current_sprite]
        self.rect = self.image.get_rect()

    def click(self):
        self.current_spriteset = self.clicked
        play_sound("Assets/sounds/click.mp3")

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.current_sprite += .25
        counter["Time"] += self.current_sprite * 0.01
        if self.current_sprite == len(self.current_spriteset):
            self.current_sprite = 0
            if self.current_spriteset != self.idle:
                self.current_spriteset = self.idle
        self.image = self.current_spriteset[int(self.current_sprite)]


class Tongue(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.current_sprite = 0
        self.animation = []
        for i in range(3):
            self.animation.append(get_image(f'Assets/sprites/environment/tongue_{i}.png'))
        self.image = self.animation[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [860, 820]

    def update(self):
        self.current_sprite += .25
        if self.current_sprite == len(self.animation):
            self.current_sprite = 0
        self.image = self.animation[int(self.current_sprite)]


class Egg(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.version = rng.randint(3)
        self.is_animating = False
        self.idle = []
        self.born = []
        self.current_spriteset = []

        for i in range(1, 7):
            self.idle.append(get_image(f"Assets/sprites/egg/idle_{self.version}_ ({i}).png"))
            self.born.append(get_image(f"Assets/sprites/egg/egg_{self.version}_ ({i}).png"))
        self.dead = self.born.copy()
        self.dead.reverse()

        self.current_sprite = 0
        self.image = self.idle[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.animate("born")

    def animate(self, animation):
        if animation == "idle":
            self.current_spriteset = self.idle
        if animation == "born":
            self.current_spriteset = self.born
        if animation == "dead":
            self.current_spriteset = self.dead
        self.is_animating = True

    def update(self):
        if self.is_animating:
            if self.current_spriteset == self.born or self.current_spriteset == self.dead:
                self.current_sprite += 1
            else:
                self.current_sprite += 1
            if self.current_sprite >= len(self.current_spriteset):
                self.current_sprite = 0
                if self.current_spriteset == self.born:
                    self.current_spriteset = self.idle
                if self.current_spriteset == self.dead:
                    self.kill()
            self.image = self.current_spriteset[int(self.current_sprite)]


class Field(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, number=0):
        super().__init__()

        self.number = number
        self.occupied_by_player = False
        self.occupied_by_enemy = False

        self.wrong = False

        self.hidden = False
        self.solved = False
        self.egg_counter = -1
        self.egg_placed = False
        self.egg_sploded = -1

        self.egggroup = pygame.sprite.Group()
        self.image = get_image("Assets/sprites/environment/testpixel.png")
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def wrongen(self):
        self.wrong = True

    def solve(self):
        self.egg_placed = False
        self.hidden = False
        self.solved = True

    def egged(self):
        self.hidden = False
        self.egg_placed = True
        self.egggroup.add(Egg(self.rect.centerx, self.rect.centery))

    def eggbreak(self):
        self.solve()
        self.egg_placed = False
        for egg in self.egggroup:
            egg.animate("dead")

def draw_field(pos_x: int, pos_y: int):
    sudoku_list = generate_sudoku()
    group = pygame.sprite.Group()
    for i in range(9):
        y = 100 * i
        for j in range(9):
            number = sudoku_list[1][i][j]
            x = 100 * j
            new_field = Field(x + pos_x, y + pos_y, number)
            if sudoku_list[0][i][j] != sudoku_list[1][i][j]:
                new_field.hidden = True
            group.add(new_field)
    return [group, sudoku_list]


class Snake(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, player=False, head=False):
        super().__init__()
        self.id = 0
        self.last_id = 0
        self.last_position = [pos_x, pos_y]
        self.x, self.y = pos_x, pos_y
        self.min_sprite = 0
        self.max_sprite = 0
        self.back, self.left, self.right, self.up = [0, 0], [0, 0], [0, 0], [0, 0]
        self.moves = ["d", "l", "u", "r"]
        self.moves_currently = "d"
        self.moves_last = "l"

        self.length = 1

        self.is_player = player
        self.is_head = head
        self.is_animating = False
        self.destination_string = ""
        self.idle, self.born, self.move, self.dead = [], [], [], []
        self.current_sprite = 0
        self.find_sprites()

        self.segments = pygame.sprite.Group()

        self.image = self.born[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]
        self.animate("born")

    def get_current_moves(self):
        if self.moves_currently == "u":
            return["u", "l", "r"]
        if self.moves_currently == "d":
            return["d", "l", "r"]
        if self.moves_currently == "r":
            return["d", "u", "r"]
        if self.moves_currently == "l":
            return["d", "l", "u"]

    def animate(self, animation):
        if animation == "idle":
            self.current_spriteset = self.idle
        if animation == "born":
            self.current_spriteset = self.born
        if animation == "move":
            self.current_spriteset = self.move
        if animation == "dead":
            self.current_spriteset = self.dead
        self.is_animating = True

    def add_segment(self, number=1):
        if self.length <=9:
            self.length += number
            new_segment = Snake(self.x+self.back[0], self.y+self.back[1], player=self.is_player, head=False)
            new_segment.id = self.last_id + 1
            for i in range(self.length):
                self.segments.add(new_segment)
            self.last_id = new_segment.id
        if number <0 and self.length > 1:
            for segm in self.segments:
                if segm.id == self.length-1:
                    segm.kill()

    def find_sprites(self):
        self.destination_string = "Assets/sprites"
        if self.is_player:
            self.destination_string += "/player"
        else:
            self.destination_string += "/enemy"
        if self.is_head:
            self.destination_string += "/head"
        else:
            self.destination_string += "/segments"
        directions = ["d", "l", "u"]
        for f in range(len(directions)):
            for i in range(1, 7):
                self.idle.append(get_image(f"{self.destination_string}/_idle_{directions[f]} ({i}).png"))
                self.born.append(get_image(f"{self.destination_string}/_born_{directions[f]} ({i}).png"))
                self.move.append(get_image(f"{self.destination_string}/_move_{directions[f]} ({i}).png"))
        idle_r = [self.idle[6], self.idle[7], self.idle[8], self.idle[9], self.idle[10], self.idle[11], self.idle[12]]
        born_r = [self.born[6], self.born[7], self.born[8], self.born[9], self.born[10], self.born[11], self.born[12]]
        move_r = [self.move[6], self.move[7], self.move[8], self.move[9], self.move[10], self.move[11], self.move[12]]

        for sprite in idle_r:
            self.idle.append(pygame.transform.flip(sprite, True, False))
        for sprite in born_r:
            self.born.append(pygame.transform.flip(sprite, True, False))
        for sprite in move_r:
            self.move.append(pygame.transform.flip(sprite, True, False))

        self.dead = self.born.copy()
        self.dead.reverse()

    def update(self):
        self.rect.center = [self.x, self.y]
        if self.moves_currently == "u":
            self.min_sprite = 12
            self.max_sprite = 17
        if self.moves_currently == "l":
            self.min_sprite = 6
            self.max_sprite = 11
        if self.moves_currently == "d":
            self.min_sprite = 0
            self.max_sprite = 5
        if self.moves_currently == "r":
            self.min_sprite = 18
            self.max_sprite = 23
        if self.current_sprite > self.max_sprite or self.current_sprite <= self.min_sprite:
            self.current_sprite = self.min_sprite
        if self.current_spriteset == self.born or self.current_spriteset == self.move and self.current_sprite >= self.max_sprite:
            self.current_spriteset = self.idle
        if self.current_spriteset == self.dead and self.current_sprite >= self.max_sprite:
            self.kill()
        self.image = self.current_spriteset[(self.current_sprite)]
        self.current_sprite += 1
        for item in self.segments:
            item.image = item.current_spriteset[int(self.current_sprite)]
            item.current_sprite += 1
