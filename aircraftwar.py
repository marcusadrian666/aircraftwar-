import pygame
import random

# 初始化游戏
pygame.init()

# 设置屏幕大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("飞机大战")

# 加载飞机、敌人和子弹图片
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
bullet_img = pygame.image.load("bullet.png")
background_img = pygame.image.load("background.jpg")

# 设置颜色
white = (255, 255, 255)
red = (255, 0, 0)

# 设置玩家飞机初始位置和速度
player_x = 370
player_y = 480
player_x_change = 0

# 创建多个敌人
num_enemies = 6
enemies = []
for _ in range(num_enemies):
    enemy_x = random.randint(0, 736)
    enemy_y = random.randint(50, 150)
    enemies.append({"x": enemy_x, "y": enemy_y, "x_change": 4, "y_change": 40})

# 设置子弹初始位置和速度
bullet_x = 0
bullet_y = 480
bullet_y_change = 10
bullet_state = "ready"  # "ready"表示子弹在飞机上，"fire"表示子弹发射中

# 初始化分数
score = 0

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y):
    screen.blit(enemy_img, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = ((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2) ** 0.5
    if distance < 27:
        return True
    return False

# 游戏循环
running = True
while running:
    screen.fill(white)
    screen.blit(background_img, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
    
    player_x += player_x_change
    if player_x < 0:
        player_x = 0
    elif player_x > screen_width - 64:
        player_x = screen_width - 64
        
    for enemy_info in enemies:
        enemy_x = enemy_info["x"]
        enemy_y = enemy_info["y"]
        enemy_x_change = enemy_info["x_change"]
        
        if enemy_x < 0 or enemy_x > screen_width - 64:
            enemy_info["x_change"] = -enemy_x_change
            enemy_info["y"] += enemy_info["y_change"]
            
        enemy_info["x"] += enemy_info["x_change"]
        
        if is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
            bullet_y = 480
            bullet_state = "ready"
            score += 1
            enemy_info["x"] = random.randint(0, 736)
            enemy_info["y"] = random.randint(50, 150)
        
        enemy(enemy_x, enemy_y)
        
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
        if bullet_y < 0:
            bullet_y = 480
            bullet_state = "ready"
    
    player(player_x, player_y)
    
    pygame.display.update()

pygame.quit()
