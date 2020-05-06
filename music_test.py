import pygame
from pygame import mixer
from global_vairables import *

mixer.init()
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((800, 600))
sword_imgs = []
for i in range(8):
    file = pygame.image.load("slash{}.png".format(i + 1))
    sword_imgs.append(file)
sword_location = [(200, 200)]
sword_level = []
sword_time = []
sword_time.append(pygame.time.get_ticks())
i = 0
while True:
    screen.blit(background, (0, 0))
    now = pygame.time.get_ticks()
    if now - sword_time[0] >= 50:
        sword_time[0] = now
        i += 1
        if i > 7:
            i = 0
    screen.blit(sword_imgs[i], (400, 300))
    pygame.display.update()
