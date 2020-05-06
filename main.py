import pygame
import random
import math
from pygame import mixer
import threading
import time
from global_vairables import *
from enemy_patterns import *
from fire_modes import *

pygame.mixer.music.load("background.wav")
# pygame.mixer.music.play(-1)

# Music effects
pause_time = pygame.mixer.Sound("slow_time.wav")
resume_time = pygame.mixer.Sound("normalize_time.wav")

pygame.display.set_caption("CORONATIME")
menu_image=pygame.image.load("menu_background.jpg")

img1=pygame.image.load("injection.png")
img1 = pygame.transform.scale(img1, (128, 128))
img2=pygame.image.load("upgrade_damage.png")
img2 = pygame.transform.scale(img2, (128, 128))
img3=pygame.image.load("file.png")
img3 = pygame.transform.scale(img3, (128, 128))
weapon1=pygame.image.load("first-aid-kit.png")
weapon2=pygame.image.load("defribillator.png")
weapon3=pygame.image.load("eye-drop.png")



# icon = pygame.image.load("spaceship.png")

# pygame.display.set_icon(icon)


# Thread info


def health_display():
    global running
    if health == 0:
        exit()
    for i in range(health):
        screen.blit(healthImg, (688 + 36 * i, 10))


# Score and Level Display

def score_display():
    global score, level, experience, upgrade_screen_pause, game_pause, bullet_fire_delay_switch
    score=get_score()
    score_img = font.render("Score: " + str(score), True, (255, 255, 255))
    level_img = font.render("Level: " + str(level), True, (255, 255, 255))
    if score >= experience:
        reset_score()
        level += 1
        experience += 500

        upgrade_screen_pause = True
        game_pause = True
        pygame.mixer.music.set_volume(0.5)
    screen.blit(score_img, (10, 10))
    screen.blit(level_img, (350, 10))


# Spawn enemies after level up
def enemy_level_up_spawn():
    for i in range(2):
        enemy_health = 50
        enemy_1_Y = 0
        enemy_in_screen = False
        temp = random.randint(0, 1)

        if time_slowed:
            i = time_slow_coefficient
        else:
            i = 1
        if temp:
            enemy_1_X_change = 3 / i
            enemy_1_X = random.randint(-100, 0)
        else:
            enemy_1_X_change = -3 / i
            enemy_1_X = random.randint(800, 900)
        enemy_1_Y_change = 40
        enemy_1_Y == random.randint(32, 300)
        enemies.append(
            [1, enemy_1_X, enemy_1_Y, enemy_1_X_change, enemy_1_Y_change, enemy_in_screen, True, enemy_health])


# Initial enemy spawn

def enemy_initial_spawn():
    global time_slowed,no_of_enemies,time_slow_coefficient
    for i in range(max_no_of_enemies):
        enemy_health = 50
        enemy_1_Y = random.randint(32, 300)
        enemy_count_increase(1)
        enemy_in_screen = False
        if time_slowed:
            i=time_slow_coefficient
        else:
            i=1
        temp = random.randint(0, 1)
        if temp:
            enemy_1_X_change = 2/i
            enemy_1_X = random.randint(-1000, 0)
        else:
            enemy_1_X_change = -2/i
            enemy_1_X = random.randint(800, 1800)
        enemy_1_Y_change = 40

        enemies.append(
            [1, enemy_1_X, enemy_1_Y, enemy_1_X_change, enemy_1_Y_change, enemy_in_screen, True, enemy_health])


# VARIABLE TO fix max threads possible for firing bullets

def player():
    global playerInfo, thread_limit
    # Here temp is just a variable which stops the program to make infinite threads to hang the program
    playerInfo[0] += playerInfo[2]
    playerInfo[1] += playerInfo[3]
    screen.blit(playerImg, (playerInfo[0], playerInfo[1]))

    if playerInfo[0] < 0:
        playerInfo[0] = 0
    elif playerInfo[0] > 736:
        playerInfo[0] = 736
    if playerInfo[1] > 540:
        playerInfo[1] = 540
    elif playerInfo[1] < 60:
        playerInfo[1] = 60
    if no_of_bullets:
        if fire_mode != 3:
            bullet_motion()


def fire_bullet():
    global playerInfo, bullet_speed, bullets, no_of_bullets, fire_ready, fire_mode,last_fire_shot
    now = pygame.time.get_ticks()
    if now - last_fire_shot >rate_of_fire :
        last_fire_shot = now
        no_of_bullets += 1
        temp = [playerInfo[0] + 16, playerInfo[1] - 16, 0, bullet_speed]
        bullets.append(temp)


def bullet_motion():
    global bullets, bullet_speed, no_of_bullets, thread_limit

    dead_bullets = 0
    if fire_mode == 0 or fire_mode == 1 or fire_mode == 2:
        if no_of_bullets > 0:
            for i in bullets:

                i[1] -= bullet_speed
                # Add bullet y change to bullet Y
                if i[1] <= 0:
                    no_of_bullets -= 1
                    bullets.pop(bullets.index(i))
                    continue
                screen.blit(bulletImg, (i[0], i[1]))


def enemy_bullet_motion():
    for i in enemy_bullets:
        i[1] += enemy_1_bullet_speed
        if i[1] > 600:
            enemy_bullets.pop(enemy_bullets.index(i))
            continue
        screen.blit(enemy_bulletImg, (i[0], i[1]))


def enemy():
    global enemies
    # print(enemies)
    for i in enemies:
        # IF ENMEY IS OF TYPE 1 i.e Most basic enemt
        if i[0] == 1:
            enemy_1_motion(i)
        elif i[0] == 2:
            enemy_2_motion(i)
    enemy_bullet_motion()


# Collison Function
def bullet_enemy_collision_check():
    global score, enemies, bullets, no_of_bullets, no_of_enemies, thread_limit, current_time
    if fire_mode != 3:
        for n in enemies:
            for m in bullets:
                # If enemy is the most Basic enemy
                if n[0] == 1:
                    if n[7] <= 0:
                        enemies.pop(enemies.index(n))
                        enemy_death(n[1], n[2], True)
                        break
                    distance = math.sqrt(math.pow(n[1] - m[0], 2) + math.pow(n[2] - m[1], 2))
                    if distance < 30:
                        pygame.mixer.Sound.play(enemy_hit)
                        pygame.mixer.Sound(enemy_hit)
                        no_of_bullets -= 1
                        n[7] -= bullet_damage

                        if fire_mode == 2:
                            contact_location.append((n[1], n[2]))
                            contact_time.append(pygame.time.get_ticks())
                            explosion_level.append(-1)
                            explosion_size.append("large")
                            for l in enemies:
                                if l[0] == 1:
                                    temp_distance = math.sqrt(math.pow(l[1] - m[0], 2) + math.pow(l[2] - m[1], 2))
                                    if temp_distance <= 100:
                                        l[7] -= bullet_damage / 2
                                elif l[0] == 2:
                                    arr = l[1]
                                    for k in arr:
                                        temp_distance = math.sqrt(math.pow(k[0] - m[0], 2) + math.pow(k[1] - m[1], 2))
                                        if temp_distance <= 100:
                                            k[8] -= bullet_damage / 2
                        bullets.pop(bullets.index(m))
                        if n[7] <= 0:
                            enemies.pop(enemies.index(n))
                            enemy_death(n[1], n[2], True)
                            break
                if n[0] == 2:
                    for ship in n[1]:
                        distance = math.sqrt(math.pow(ship[0] - m[0], 2) + math.pow(ship[1] - m[1], 2))
                        if distance < 30:
                            if fire_mode == 2:
                                contact_location.append((ship[0], ship[1]))
                                contact_time.append(pygame.time.get_ticks())
                                explosion_level.append(-1)
                                explosion_size.append("large")
                                for l in enemies:
                                    if l[0] == 1:
                                        temp_distance = math.sqrt(math.pow(l[1] - m[0], 2) + math.pow(l[2] - m[1], 2))
                                        if temp_distance <= 100:
                                            l[7] -= bullet_damage / 2
                                    elif l[0] == 2:
                                        arr = l[1]
                                        for k in arr:
                                            temp_distance = math.sqrt(
                                                math.pow(k[0] - m[0], 2) + math.pow(k[1] - m[1], 2))
                                            if temp_distance <= 100:
                                                k[8] -= bullet_damage / 2

                            if ship[8] <= 0:
                                n[1].pop(n[1].index(ship))
                                contact_location.append((ship[0], ship[1]))
                                contact_time.append(pygame.time.get_ticks())
                                explosion_level.append(-1)
                                explosion_size.append("large")
                            n[3] += 1
                            if ship[7] == False:
                                n[2] += 1
                            if n[3] == 5:

                                enemies.pop(enemies.index(n))
                                for i in range(5):
                                    enemy_death(z=False)


# Fucntion to check enemy bullet and player collision !
def ebullet_player_collision_check():
    global health, enemy_bullets, playerInfo

    for m in enemy_bullets:
        distance = math.sqrt(math.pow(playerInfo[0] + 16 - m[0], 2) + math.pow(playerInfo[1] - m[1], 2))
        if distance < 30:
            health -= 1
            enemy_bullets.pop(enemy_bullets.index(m))


def bullet_fire_delay():
    global rate_of_fire, fire_ready, bullet_fire_delay_switch
    print(bullet_fire_delay_switch)
    while bullet_fire_delay_switch:
        time.sleep(rate_of_fire)
        # print(rate_of_fire)
        fire_ready = 1
    print(bullet_fire_delay_switch)


# Function to slow down time
def slow_time():
    global enemies, enemy_1_bullet_speed, time_slowed
    time_slowed = True
    for i in enemies:
        if i[0] == 1:
            i[3] = i[3] / 2
            i[4] = i[4] / 2
    enemy_1_bullet_speed /= 2
    # pygame.mixer.Sound.play(pause_time)
    # pygame.mixer.music.pause()
    pygame.mixer.music.set_volume(0.4)


# Function To make time Normal
def normalize_time():
    global enemies, enemy_1_bullet_speed, time_slowed
    time_slowed = False
    for i in enemies:
        if i[0] == 1:
            i[3] = i[3] * 2
            i[4] = i[4] * 2
    enemy_1_bullet_speed *= 2
    # pygame.mixer.Sound.play(resume_time)
    # pygame.mixer.music.unpause()
    pygame.mixer.music.set_volume(1)


running = True

#c = threading.Thread(target=bullet_fire_delay, daemon=True)
#c.start()

enemy_initial_spawn()
while running:
    # Checking for all events happening in the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerInfo[2] -= move_speed

                if upgrade_screen_pause == True:
                    temp_selected = upgrade_1_selected
                    upgrade_1_selected = upgrade_2_selected
                    upgrade_2_selected = upgrade_3_selected
                    upgrade_3_selected = temp_selected
            if event.key == pygame.K_RIGHT:
                playerInfo[2] += move_speed

                if upgrade_screen_pause == True:
                    temp_selected = upgrade_3_selected
                    upgrade_3_selected = upgrade_2_selected
                    upgrade_2_selected = upgrade_1_selected
                    upgrade_1_selected = temp_selected
            if event.key == pygame.K_UP:
                playerInfo[3] -= move_speed
            if event.key == pygame.K_DOWN:
                playerInfo[3] += move_speed
            if event.key == pygame.K_LCTRL:
                slow_time()
            if event.key == pygame.K_ESCAPE:
                game_pause = not game_pause
                if game_pause:
                    pygame.mixer.music.set_volume(0.4)
                else:
                    pygame.mixer.music.set_volume(1)
            if event.key == pygame.K_SPACE:
                if menu_screen_pause == False and game_pause==True and upgrade_screen_pause== False:
                    menu_screen_pause == True
                    game_pause = False
                    pygame.mixer.music.play(-1)
                    # print("Enter is pressed, ")
            if event.key == pygame.K_SPACE:
                firing = True
            if event.key == pygame.K_a:
                if upgrade_screen_pause == True:
                    global level, time_slow_coefficient, bullet_fire_delay_switch
                    if upgrade_screen_pause == True:
                        upgrade_screen_pause = False
                        if upgrade_1_selected == 5:
                            global rate_of_fire, limiting_factor, fire_mode, base_rate_of_fire, base_bullet_damage, base_bullet_speed
                            if level != 5:
                                if rate_of_fire - fire_rate_upgrade_rate > fire_rate_limit:
                                    rate_of_fire -= fire_rate_upgrade_rate
                                    upgrade_1_count += 1
                            elif level == 5:
                                fire_mode = 1
                                fire_rate_limit = 100
                                base_rate_of_fire = 500
                                bullets.clear()
                                no_of_bullets = 0
                                rate_of_fire = base_rate_of_fire - upgrade_1_count * fire_rate_upgrade_rate
                                bullet_damage = base_bullet_damage + upgrade_2_count * base_bullet_damage / 2
                                bullet_speed = base_bullet_speed + upgrade_3_count * bullet_speed_upgrade_rate
                            game_pause = False

                        elif upgrade_2_selected == 5:
                            if level != 5:
                                bullet_damage += damage_upgrade_rate
                                upgrade_2_count += 1
                            elif level == 5:
                                fire_mode = 2
                                base_bullet_damage *= 3
                                base_rate_of_fire *= 2
                                base_bullet_speed /= 2
                                bullets.clear()
                                no_of_bullets = 0
                                rate_of_fire = base_rate_of_fire - upgrade_1_count * fire_rate_upgrade_rate
                                bullet_damage = base_bullet_damage + upgrade_2_count * base_bullet_damage / 2
                                bullet_speed = base_bullet_speed + upgrade_3_count * bullet_speed_upgrade_rate
                            game_pause = False

                        elif upgrade_3_selected == 5:
                            if level != 5:
                                bullet_speed += bullet_speed_upgrade_rate
                                upgrade_3_count += 1
                            elif level == 5:
                                fire_mode = 3
                                base_bullet_damage *= 4
                                time_slow_coefficient = 4
                                base_rate_of_fire *= 1.5
                                bullets.clear()
                                no_of_bullets = 0
                                rate_of_fire = base_rate_of_fire - upgrade_1_count * fire_rate_upgrade_rate
                                bullet_damage = base_bullet_damage + upgrade_2_count * base_bullet_damage / 2
                                bullet_speed = base_bullet_speed + upgrade_3_count * bullet_speed_upgrade_rate
                            game_pause = False
                        #c = threading.Thread(target=bullet_fire_delay, daemon=True)
                        #c.start()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerInfo[2] += move_speed
            if event.key == pygame.K_RIGHT:
                playerInfo[2] -= move_speed
            if event.key == pygame.K_UP:
                playerInfo[3] += move_speed
            if event.key == pygame.K_DOWN:
                playerInfo[3] -= move_speed
            if event.key == pygame.K_LCTRL:
                normalize_time()
            if event.key == pygame.K_SPACE:
                firing = False

    if menu_screen_pause == False:
        #global text
        #move_background()
        # font of the menu screen
        #temp = pygame.font.Font("xirod.ttf", 25)
        #title = pygame.font.Font("Lato-BlackItalic.ttf", 90)
        #title_message1 = title.render("It's", True, (30, 150, 130))
        #pygame.draw.rect(screen, (0, 0, 0), (20, 210, 760, 100))

        #text = renderer.animate()
        #screen.blit(text,(170,220))
        #title_message2 = title.render("C O R O N A T I M E", True, (3, 252, 211))
        #menu_message = temp.render("Press Space to play", True, (255, 255, 255))
        #screen.blit(title_message1, (350, 100))
        #screen.blit(title_message2, (45, 200))
        #screen.blit(menu_message, (175, 500))
        screen.blit(menu_image,(0,0))
    if game_pause == False:
        move_background()
        player()
        enemy()
        if firing:
            if fire_mode == 3:
                now = pygame.time.get_ticks()
                #print(bullet_damage)
                if now - last_fire_shot > rate_of_fire:
                    last_fire_shot = now
                    print(rate_of_fire)
                    slash_time.append(pygame.time.get_ticks())
                    slash_level.append(1)
                    slash_location.append([playerInfo[0], playerInfo[1]])
            else:
                fire_bullet()
        bullet_enemy_collision_check()
        ebullet_player_collision_check()
        health_display()
        score_display()
        draw_explosion()
        draw_slash()

    if upgrade_screen_pause == True:
        move_background()
        upgrade_text = pygame.font.Font("xirod.ttf", 23)
        upgrade_text_2 = pygame.font.Font("xirod.ttf", 14)

        if level == 5:
            pygame.draw.rect(screen, (0, 0, 0), (100, 50, 600, 500))
            text = upgrade_text.render("Choose your Big Upgrade", True, (255, 255, 255))
            screen.blit(text, (170, 130))
            upgrade_1_text = upgrade_text_2.render("futureistic aid", True, (255, 255, 255))
            upgrade_2_text = upgrade_text_2.render("Defribillator", True, (255, 255, 255))
            upgrade_3_text = upgrade_text_2.render("Sanitizer Spray", True, (255, 255, 255))
            upgrade_select_text_line1_1 = upgrade_text.render("Press", True, (255, 255, 255))
            upgrade_select_text_line1_2 = upgrade_text.render("A ", True, (0, 0, 255))
            upgrade_select_text_line1_3 = upgrade_text.render("to Upgrade! ", True, (255, 255, 255))
            screen.blit(upgrade_1_text, (125, 200))
            screen.blit(upgrade_2_text, (325, 200))
            screen.blit(upgrade_3_text, (530, 200))
            # screen.blit(upgrade_3_text_line2,(530,300))
            screen.blit(upgrade_select_text_line1_1, (210, 450))
            screen.blit(upgrade_select_text_line1_2, (335, 450))
            screen.blit(upgrade_select_text_line1_3, (365, 450))


            pygame.draw.rect(screen, (0, 0, 255), (125, 230, 150, 150), 1 * upgrade_1_selected)
            screen.blit(weapon1, (135, 240))
            pygame.draw.rect(screen, (0, 0, 255), (325, 230, 150, 150), 1 * upgrade_2_selected)
            screen.blit(weapon2, (335, 240))
            pygame.draw.rect(screen, (0, 0, 255), (525, 230, 150, 150), 1 * upgrade_3_selected)
            screen.blit(weapon3, (535, 240))

        else:
            pygame.draw.rect(screen, (0, 0, 0), (100, 50, 600, 500))
            text = upgrade_text.render("Choose a Upgrade!", True, (255, 255, 255))
            screen.blit(text, (170, 120))
            upgrade_1_text = upgrade_text_2.render("Fire Rate", True, (255, 255, 255))
            upgrade_2_text = upgrade_text_2.render("Damage", True, (255, 255, 255))
            upgrade_3_text_line1 = upgrade_text_2.render("Speed", True, (255, 255, 255))
            # upgrade_3_text_line2 = upgrade_text.render("Speed", True, (255, 255, 255))
            upgrade_select_text_line1_1 = upgrade_text.render("Press", True, (255, 255, 255))
            upgrade_select_text_line1_2 = upgrade_text.render("A ", True, (230, 255, 3))
            upgrade_select_text_line1_3 = upgrade_text.render("to Upgrade!", True, (255, 255, 255))

            screen.blit(upgrade_1_text, (125, 200))
            screen.blit(upgrade_2_text, (325, 200))
            screen.blit(upgrade_3_text_line1, (530, 200))
            # screen.blit(upgrade_3_text_line2,(530,300))
            screen.blit(upgrade_select_text_line1_1, (210, 450))
            screen.blit(upgrade_select_text_line1_2, (335, 450))
            screen.blit(upgrade_select_text_line1_3, (365, 450))

            pygame.draw.rect(screen, (230, 255, 3), (125, 230, 150, 150), 1 * upgrade_1_selected)
            screen.blit(img1, (135, 240))
            pygame.draw.rect(screen, (230, 255, 3), (325, 230, 150, 150), 1 * upgrade_2_selected)
            screen.blit(img2, (335, 240))
            pygame.draw.rect(screen, (230, 255, 3), (525, 230, 150, 150), 1 * upgrade_3_selected)
            screen.blit(img3, (535, 240))
    # print(enemy_1_X_change, enemy_1_Y_change)
    pygame.display.update()
