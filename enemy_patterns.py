from global_vairables import *

import pygame



# General Enemy FUnctions
def enemy_count_increase(x):
    global enemy_in_progress,no_of_enemies
    no_of_enemies += x
    #print(no_of_enemies)
    enemy_in_progress = False

def enemy_death(x=None,y=None,z=False):
    global  no_of_enemies,explosion_size,explosion_level,contact_time,contact_location,score
    #print("Enemy death called")
    add_score()
    if z==True:
        contact_location.append((x,y))
        contact_time.append(pygame.time.get_ticks())
        explosion_level.append(-1)
        explosion_size.append("small")
    no_of_enemies -=1
    t = random.randint(1, 5)
    while enemy_in_progress == True :
        pass
    x = threading.Thread(target=enemy_generation, args=(t,))
    x.start()


def enemy_generation(t):
    time.sleep(t)
    global time_slowed, score, enemy, no_of_enemies, battalion_in_progress,enemy_in_progress,time_slow_coefficient,enemyImg
    if (no_of_enemies <= max_no_of_enemies) and enemy_in_progress == False:
        enemy_in_progress =True
        temp_enemy = random.randint(1, 2)
        if temp_enemy == 2 and (not battalion_in_progress) and ((no_of_enemies + 5) < max_no_of_enemies):
            battlion_in_progress = True
            enemy_count_increase(5)
            if battlion_in_progress:
                enemy_2_spawn()
                #print("Enemy 2 generated!")
                battalion_in_progress = False
        else:
            #print("enemy 1 generated")
            enemy_in_screen = False
            enemy_health = 50
            if time_slowed:
                i = time_slow_coefficient
            else:
                i = 1

            temp = random.randint(0, 1)
            if temp:
                enemy_1_X_change = 2 / i
                enemy_1_X = random.randint(-100, 0)
            else:
                enemy_1_X_change = -2 / i
                enemy_1_X = random.randint(736, 836)
            enemy_1_Y_change = 20
            enemy_1_Y = random.randint(32, 300)
            enemies.append([1, enemy_1_X, enemy_1_Y, enemy_1_X_change, enemy_1_Y_change, enemy_in_screen, True, enemy_health])
            enemy_count_increase(1)


def enemy_1_fire_bullet(x):
    ebulletX = x[1]
    ebulletY = x[2]
    enemy_bullets.append([ebulletX + 16, ebulletY + 16])


def enemy_2_fire_bullet(x):
    for i in x:
        ebulletX = i[0]
        ebulletY = i[1]
        enemy_bullets.append([ebulletX + 16, ebulletY + 16])


# Enemy 1
def enemy_1_motion(i):
    global no_of_enemies
    if i[5] == False:
        i[1] += i[3]
        if i[1] > -32 or i[1] < 830:
            i[5] = True
    elif i[5] == True:
        i[1] += i[3]

        if i[1] > 748 and i[1] > 0:
            i[1] = 748
            i[3] *= -1
            i[2] += i[4]
        elif i[1] < 0 and i[3] < 0:
            i[1] = 0
            i[3] *= -1
            i[2] += i[4]

            if i[2] > 600:
                enemies.pop(enemies.index(i))
                #print("popped enemy 1")
                enemy_death(z=False)
                return

        screen.blit(enemyImg, (i[1], i[2]))
        x = random.randint(1, 600)
        if x == 600:
            enemy_1_fire_bullet(i)


enemy_2_Img = pygame.image.load("11.png")
enemy_2_battalion = []


def enemy_2_spawn():
    squad = []
    global gap
    health = 100
    x_target = random.randint(30, 400)
    y_target = random.randint(30, 200)
    on_position = False

    for i in range(5):
        dice_roll = random.randint(0, 2)
        if dice_roll == 0:
            x_source = random.randint(-200, -50)
            y_source = random.randint(0, 200)
        elif dice_roll == 1:
            x_source = random.randint(0, 350)
            while(x_source == x_target):
                x_source = random.randint(0,350)
            y_source = random.randint(-200, -100)
        else:
            x_source = random.randint(900, 1000)
            y_source = random.randint(0, 200)

        x_change = ((x_target + gap * i - x_source) // abs(x_target + gap * i - x_source)) * 1
        y_change = ((y_target - y_source) // abs(y_target - y_source)) * 1
        slope = (y_target - y_source) / (x_target - x_source)
        squad.append([x_source, y_source, x_target + gap * i, y_target, x_change, y_change, slope, on_position, health])
    ships_on_position = 0
    #print(squad)
    dead_ships = 0
    enemies.append([2, squad, ships_on_position,dead_ships])


def enemy_2_motion(x):
    global no_of_enemies
    for i in x[1]:
        distance = math.sqrt(math.pow(i[0] - i[2], 2) + math.pow(i[1] - i[3], 2))
        if i[7] == False:
            if distance < 5:
                i[0] = i[2]
                i[1] = i[3]
                i[7] = True
                x[2] += 1
            else:
                i[0] = i[0] + i[4]
                i[1] = i[6] * (i[0] - i[2]) + i[3]
        if i[7] == True:
            if x[2] == 5:
                i[1] += enemy_2_move_speed

                if i[1] >= 600:
                    enemies.pop(enemies.index(x))
                    #print("battlion pop successfull")
                    for i in range(5):
                        enemy_death(z=False)
                    return
                m = random.randint(1, 600)

                if m == 600:
                    enemy_2_fire_bullet(x[1])
        screen.blit(enemy_2_Img, (i[0], i[1]))
