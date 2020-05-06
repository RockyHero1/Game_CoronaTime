from global_vairables import *
from enemy_patterns import *


# Upgrade unction

def choose_upgrade():
    global game_pause, upgrade_screen_pause
    game_pause = True
    upgrade_screen_pause = True
    if level % 5 != 0:
        pygame.draw.rect(screen, (200, 300, 400, 200))
        pygame.draw.rect(screen, (400, 220, 50, 50))
        # pygame.draw.rect(screen, (200, 300))
        # pygame.draw.rect(screen, (200, 300))
    game_pause = False
    upgrade_screen_pause = False


# Sword upgrade

def slash():
    global playerInfo, bullet_speed, bullets, no_of_bullets, fire_ready, fire_mode, firing,last_fire_shot
    now = pygame.time.get_ticks()
    if now - last_fire_shot > rate_of_fire :
        #print("hulk slash")
        slash_time.append(pygame.time.get_ticks())
        slash_level.append(0)
        fire_ready = 0


def draw_slash():
    # global slash_location,slash_level,slash_time,sword_imgs
    global bullet_damage, score,playerInfo
    for i in slash_time:
        now = pygame.time.get_ticks()
        if now - i >= 30:
            index = slash_time.index(i)
            slash_time[index] = now
            slash_level[index] += 1
            if slash_level[index] > 7:
                for n in enemies:
                    # If enemy is the most Basic enemy
                    if n[0] == 1:
                        if n[7] <= 0:
                            enemies.pop(enemies.index(n))
                            enemy_death(n[1], n[2], True)
                            break
                        distance = math.sqrt(
                            math.pow(n[1] - playerInfo[0], 2) + math.pow(n[2] - playerInfo[1], 2))
                        if distance < 200:
                            pygame.mixer.Sound.play(enemy_hit)
                            pygame.mixer.Sound(enemy_hit)
                            #print(bullet_damage)
                            n[7] -= bullet_damage
                            if n[7] <= 0:
                                enemies.pop(enemies.index(n))
                                enemy_death(n[1], n[2], True)
                                break
                    if n[0] == 2:
                        for ship in n[1]:
                            distance = math.sqrt(math.pow(ship[0] - playerInfo[0], 2) + math.pow(
                                ship[1] - playerInfo[1], 2))
                            if distance < 200:
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
                slash_location.pop(index)
                slash_level.pop(index)
                slash_time.pop(index)
                continue
            screen.blit(sword_imgs[slash_level[index]], (slash_location[index][0] - 90, slash_location[index][1] - 180))

    # Bullet Path


def draw_explosion():
    for i in contact_time:
        now = pygame.time.get_ticks()
        if now - i > frame_rate:
            index = contact_time.index(i)
            contact_time[index] = now
            explosion_level[index] += 1
            if explosion_level[index] > 8:
                contact_location.pop(index)
                contact_time.pop(index)
                explosion_level.pop(index)
                explosion_size.pop(index)
                continue
            if explosion_size[index] == "large":
                screen.blit(explosionImgs[explosion_level[index]],
                            (contact_location[index][0] - 100, contact_location[index][1] - 100))
            else:
                screen.blit(explosionImgs_small[explosion_level[index]],
                            (contact_location[index][0], contact_location[index][1]))


def normalize_stats():
    global bullet_damage, bullet_speed, rate_of_fire, base_rate_of_fire, base_bullet_speed, base_bullet_damage, bullet_fire_delay_switch
    # print("previous base_damage")
    # print(base_bullet_damage)
    # print("previous rate of fire")
    # print(base_rate_of_fire)
    # print("previous bullet speed")
    # print(base_bullet_speed)

    rate_of_fire = base_rate_of_fire - upgrade_1_count * fire_rate_upgrade_rate
    bullet_damage = base_bullet_damage + upgrade_2_count * base_bullet_damage / 2
    bullet_speed = base_bullet_speed + upgrade_3_count * bullet_speed_upgrade_rate
    bullet_fire_delay_switch = True

    # print("Base damage")
    # print(base_bullet_damage)
    # print("bullet speed")
    # print(base_bullet_speed)


def fire_mode_1(x, y):
    pass


def fire_mode_1_L1():
    pass


def fire_mode_1_R1():
    pass


# Missile Path
def fire_mode_2():
    pass


# Sword Path
def fire_mode_3():
    pass
