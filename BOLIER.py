import pygame
import random
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image
    return image


pygame.init()
clock = pygame.time.Clock()

w, h = 600, 600
FPS = 50
rects = []
x_pos = w // 2
y_pos = h - 60
range_between = 40
running = True
count = 0
width_of_rect = 15
height_of_rect = 80
boiler_count = h + 10
width_of_image = 25
height_of_image = 40

size = width, height = w, h
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
mario_sprite = pygame.sprite.Group()


class Ball(pygame.sprite.Sprite):
    def __init__(self, xx, yy, ww, hh, vy, colorr):
        super().__init__(all_sprites)
        self.image = pygame.Surface((ww, hh))
        pygame.draw.rect(self.image, colorr, [xx, yy, ww, hh], 0)
        self.rect = pygame.Rect(xx, yy, ww, hh)
        self.vy = vy

    def update(self):
        self.rect = self.rect.move(0, self.vy)


class Mario(pygame.sprite.Sprite):
    image = load_image('mar.png')

    def __init__(self, ww, hh, wi_of_im, he_of_im):
        super().__init__(mario_sprite)
        self.w = ww
        self.h = hh
        self.image = Mario.image
        self.rect = self.image.get_rect()
        self.rect.y = hh - 100
        self.rect.x = ww // 2
        self.w_of_im = wi_of_im
        self.he_of_im = he_of_im

    def update(self, direction):
        if direction == 'left':
            if self.rect.x + 8 > self.w - self.w_of_im:
                self.rect.x = self.w - self.w_of_im
            else:
                self.rect = self.rect.move(8, 0)
        elif direction == 'right':
            if self.rect.x - 8 < 0:
                self.rect.x = 0
            else:
                self.rect = self.rect.move(-8, 0)
        elif direction == 'up':
            if self.rect.y + 8 > self.h - self.he_of_im:
                self.rect.y = self.h - self.he_of_im
            else:
                self.rect = self.rect.move(0, 8)
        elif direction == 'down':
            if self.rect.y - 8 < 0:
                self.rect.y = 0
            else:
                self.rect = self.rect.move(0, -8)

        if direction == 1:
            if pygame.sprite.spritecollideany(self, all_sprites):
                start_screen()


color = pygame.Color(90, 200, 90)
boiler = pygame.transform.scale(load_image('boiler.png', -1), (w, h))
Mario(w, h, width_of_image, height_of_image)

for i in range(250):
    x = random.randint(0, w - height_of_rect)
    if i == 0:
        y = random.randint(-h - range_between * i, -1 * width_of_rect - 140)
    else:
        y = random.randint(-h - range_between * i * 2, rects[i - 1][1] - range_between)
    rects.append([x, y])
    Ball(x, y, height_of_rect, width_of_rect, 5, color)


def first_level():
    global count, FPS, x_pos, y_pos, boiler_count
    flag = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        if count % 1000 == 0 and FPS < 110:
            FPS += 3
        count += 8

        if pygame.key.get_pressed()[275]:
            mario_sprite.update('left')
        elif pygame.key.get_pressed()[276]:
            mario_sprite.update('right')
        elif pygame.key.get_pressed()[274]:
            mario_sprite.update('up')
        elif pygame.key.get_pressed()[273]:
            mario_sprite.update('down')

        if boiler_count > 200 and flag:
            boiler_count -= 7
        else:
            boiler_count += 7
        if boiler_count < 200:
            flag = False

        all_sprites.update()
        screen.fill((90, 140, 30))
        screen.blit(boiler, (0, boiler_count))
        if boiler_count > h:
            mario_sprite.draw(screen)
        mario_sprite.update(1)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = [""]

    fon = pygame.transform.scale(load_image('fon1.jpg'), (w, h))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                first_level()
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
