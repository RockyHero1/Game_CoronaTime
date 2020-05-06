# Player Info
import pygame
import math
import random
import threading
import time

from pygame.rect import Rect

pygame.mixer.pre_init(22000, -16, 2, 1024)

pygame.init()

screen = pygame.display.set_mode((800, 600))
image1_pointer = 0
image2_pointer = -590

# Background
background = pygame.image.load("background.png")


def move_background():
    global image1_pointer, image2_pointer
    image1_pointer += 0.3
    image2_pointer += 0.3
    if image1_pointer > 590:
        image1_pointer = -590
    if image2_pointer > 590:
        image2_pointer = -590
    screen.blit(background, (0, image1_pointer))
    screen.blit(background, (0, image2_pointer))



pygame.mixer.quit()
# Background music
pygame.mixer.init(22050, -16, 2, 1024)

# Thread info
thread_in_progress = False
# semaphor for enemy 2 generation

playerImg = pygame.image.load("modi.png")
playerImg = pygame.transform.scale(playerImg, (128, 128))
# Player info [(PlayerX,playerY,playerX_cahnge,playery_Change,firemode,rate of fire)]
playerInfo = [360, 500, 0, 0]
playerX = 360
playerY = 500
playerX_change = 0
playerY_change = 0
move_speed = 3
base_rate_of_fire = 1000
fire_rate_limit = 500
base_bullet_damage = 50
damage_upgrade_rate = 25
fire_rate_upgrade_rate = 1000 / 15
bullet_speed_upgrade_rate = 5 / 15
rate_of_fire = 1000
base_bullet_speed = 5
fire_mode = 0
fire_ready = 1
firing = False
# firing =0 means space is not hld down
# firing=1 means space is held down meanng bullets fier automatically

# Upgrades
upgrade_1_count = 0
upgrade_2_count = 0
upgrade_3_count = 0
# Lock on for homing
lock_on_target_info = [1000, (0, 0)]

# Explosion sprites
explosionImgs = []

explosionImgs_small=[]
for i in range(9):
    file = pygame.image.load("regularExplosion0{}.png".format(i))
    file_new = pygame.transform.scale(file, (200, 200))
    file_new_2 = pygame.transform.scale(file,(64,64))
    explosionImgs.append(file_new)
    explosionImgs_small.append(file_new_2)
frame_rate = 60
#a LIST OF ALL EXPLOSIONS INTIAL COORDINATES(CENTERS)
contact_location=[]
contact_time=[]
explosion_level=[]
explosion_size=[]


entry_info= "C O R O N A T I M E"
class textWavey:
    def __init__(self, font, message, fontcolor, amount=10):
        self.base = font.render(message, 0, fontcolor)
        self.steps = range(0, self.base.get_width(), 2)
        self.amount = amount
        self.size = self.base.get_rect().inflate(0, amount).size
        self.offset = 0.0

    def animate(self):
        s = pygame.Surface(self.size)
        height = self.size[1]
        self.offset += 0.1
        for step in self.steps:
            src = Rect(step, 0, 2, height)
            dst = src.move(0, math.cos(self.offset + step * .02) * self.amount)
            s.blit(self.base, dst, src)
        return s


bigfont = pygame.font.Font("Lato-BlackItalic.ttf", 60)
white = 255, 255, 255
renderer = textWavey(bigfont, entry_info, white, 16)
text = renderer.animate()
#Sword related variables
sword_imgs=[]
slash_time=[]
slash_level=[]
slash_location=[]
for i in range(8):
    file=pygame.image.load("slash{}.png".format(i+1))
    file2=pygame.transform.scale(file,(200,200))
    sword_imgs.append(file2)

# Time manipualtion related variables
time_slowed = False
time_slow_coefficient = 2
# Score
score = 0
def add_score():
    global score
    score += 100
def get_score():
    global score
    return score
def reset_score():
    global  score
    score = 0

def upgrade_fire_rate():
    global  rate_of_fire,fire_rate_upgrade_rate,upgrade_1_count
    if rate_of_fire - fire_rate_upgrade_rate > fire_rate_limit:
        rate_of_fire -= fire_rate_upgrade_rate
        upgrade_1_count += 1

def upgrade_damage():
    global bullet_damage,damage_upgrade_rate,upgrade_2_count
    pass

def upgrade_speed():
    global bullet_speed,bullet_speed_upgrade_rate,upgrade_3_count
    bullet_speed += bullet_speed_upgrade_rate
    upgrade_3_count += 1
font = pygame.font.Font('Gilroy-ExtraBold.otf', 32)

# Health
health = 3
healthImg = pygame.image.load("heart.png")




# SCORE REQUIRED TO LEVEL UO\p is called experience HERE
experience = 300
level = 1

# Sound Effects
enemy_hit = pygame.mixer.Sound("enemy_hit_sound.wav")

# Bulletds
bulletImg = pygame.image.load("bullet.png")
no_of_bullets = 0
bullets = []
bulletX = []
bulletY = []
bullet_speed = 5
bulletX_change = []
bulletY_change = []
bullet_damage = 50
limiting_factor = 2.5 / 55
bullet_fire_delay_switch = True

last_fire_shot = pygame.time.get_ticks()
# Enemies
max_no_of_enemies = 5
no_of_enemies = 0
enemy_in_progress = False
# Enemy 1
enemyImg = pygame.image.load("11.png")
enemyImg=pygame.transform.scale(enemyImg, (80, 80))
enemies = []
enemy_1_Y = 0

# Enemy 2 info
battalion_in_progress = False
enemy_2_move_speed = 0.5
enemy_2_bullet_speed = 0.8
# gap is the space between each ship in a battalion
gap = 70
# Enemy bullets

enemy_bullets = []
enemy_1_bullet_speed = 1
enemy_bulletImg = pygame.image.load("enemy_bullet.png")

def bullet_fire_delay_switch_flip():
    global bullet_fire_delay_switch
    print("hohohohoh")
    bullet_fire_delay_switch = not bullet_fire_delay_switch

# pause=true means game is paused
game_pause = True
menu_screen_pause = False
upgrade_screen_pause = False
upgrade_pointer = 1
upgrade_1_selected = 5
upgrade_2_selected = 1
upgrade_3_selected = 1
