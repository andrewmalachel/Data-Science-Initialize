import math
import random
import pygame

# ----------------------------
# Survival FPS Game Prototype
# ----------------------------

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini FPS - Survival Mode")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 70, 70)
GREEN = (90, 220, 90)
BLUE = (70, 120, 255)
GRAY = (80, 80, 90)
DARK = (15, 15, 20)
GOLD = (230, 185, 40)

# Map Definition (20 columns x 17 rows)
MAP = [
    "####################",
    "#..................#",
    "#..#..............##",
    "#..#...........#...#",
    "#......#........#..#",
    "#......#...........#",
    "#..##..............#",
    "#...........#......#",
    "#....#.............#",
    "#....#.............#",
    "#...........##.....#",
    "#.............#....#",
    "#....#.............#",
    "#..#...........#...#",
    "#..............#...#",
    "#..................#",
    "####################",
]

MAP_WIDTH = len(MAP[0])
MAP_HEIGHT = len(MAP)

class Player:
    def __init__(self):
        self.x = 2.5
        self.y = 2.5
        self.angle = 0.0
        self.fov = math.radians(70)
        self.speed = 2.3
        self.turn_speed = 2.2
        self.health = 100
        self.ammo = 12

    def move(self, keys):
        dx, dy = 0.0, 0.0
        if keys[pygame.K_w]:
            dx += math.cos(self.angle) * self.speed
            dy += math.sin(self.angle) * self.speed
        if keys[pygame.K_s]:
            dx -= math.cos(self.angle) * self.speed
            dy -= math.sin(self.angle) * self.speed
        if keys[pygame.K_a]:
            dx += math.cos(self.angle - math.pi / 2) * self.speed
            dy += math.sin(self.angle - math.pi / 2) * self.speed
        if keys[pygame.K_d]:
            dx += math.cos(self.angle + math.pi / 2) * self.speed
            dy += math.sin(self.angle + math.pi / 2) * self.speed

        nx = self.x + dx * 0.016
        ny = self.y + dy * 0.016
        if not is_wall(nx, self.y):
            self.x = nx
        if not is_wall(self.x, ny):
            self.y = ny

    def turn(self, direction):
        self.angle += direction * self.turn_speed * 0.016

    def shoot(self):
        if self.ammo <= 0:
            return False
        self.ammo -= 1
        return True

def is_wall(x, y):
    grid_x = int(x)
    grid_y = int(y)
    if grid_x < 0 or grid_y < 0 or grid_x >= MAP_WIDTH or grid_y >= MAP_HEIGHT:
        return True
    return MAP[grid_y][grid_x] == '#'

def distance(a_x, a_y, b_x, b_y):
    return math.hypot(b_x - a_x, b_y - a_y)

def get_random_empty_floor():
    while True:
        rx = random.uniform(1.5, MAP_WIDTH - 1.5)
        ry = random.uniform(1.5, MAP_HEIGHT - 1.5)
        if not is_wall(rx, ry) and distance(rx, ry, player.x, player.y) > 4.0:
            return rx, ry

def cast_ray(player, ray_angle):
    step = 0.02
    max_dist = 20
    dist = 0.0
    hit = False
    while dist < max_dist and not hit:
        x = player.x + math.cos(ray_angle) * dist
        y = player.y + math.sin(ray_angle) * dist
        if is_wall(x, y):
            hit = True
        dist += step
    return dist

def draw_background():
    sky = pygame.Surface((WIDTH, HEIGHT // 2))
    for y in range(sky.get_height()):
        c = 60 + int(y / sky.get_height() * 80)
        color = (c, c + 20, 180 + c // 3)
        pygame.draw.line(sky, color, (0, y), (WIDTH, y))
    screen.blit(sky, (0, 0))

    floor = pygame.Surface((WIDTH, HEIGHT // 2))
    for y in range(floor.get_height()):
        c = 30 + int(y / floor.get_height() * 80)
        color = (c, c, c)
        pygame.draw.line(floor, color, (0, y), (WIDTH, y))
    screen.blit(floor, (0, HEIGHT // 2))

def draw_walls(player):
    num_rays = 220
    fov = player.fov
    start_angle = player.angle - fov / 2
    step = fov / num_rays

    wall_columns = []
    for i in range(num_rays):
        ray_angle = start_angle + i * step
        dist = cast_ray(player, ray_angle)
        corrected = dist * math.cos(ray_angle - player.angle)
        if corrected < 0.0001:
            corrected = 0.0001
        wall_height = min(HEIGHT, (HEIGHT * 0.85) / corrected)
        shade = max(20, 255 - int(corrected * 25))
        color = (shade, shade, max(80, shade))
        wall_columns.append((wall_height, color))

    column_width = WIDTH / num_rays
    for i, (wall_height, color) in enumerate(wall_columns):
        x = int(i * column_width)
        y = HEIGHT // 2 - wall_height / 2
        pygame.draw.rect(screen, color, (x, y, max(2, int(column_width) + 1), wall_height))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.damage_cooldown = 0

    def update(self, player, dt):
        dist = distance(self.x, self.y, player.x, player.y)
        
        # Player Collision & Damage implementation
        if dist < 0.45:
            if self.damage_cooldown <= 0:
                player.health = max(0, player.health - 10)
                self.damage_cooldown = 1000  # 1 second invincibility window frame
            
            # Slide enemy backward away from player to prevent clipping
            angle = math.atan2(self.y - player.y, self.x - player.x)
            self.x = player.x + math.cos(angle) * 0.46
            self.y = player.y + math.sin(angle) * 0.46
        else:
            angle_to_player = math.atan2(player.y - self.y, player.x - self.x)
            dx = math.cos(angle_to_player) * 0.7 * 0.016
            dy = math.sin(angle_to_player) * 0.7 * 0.016
            if not is_wall(self.x + dx, self.y):
                self.x += dx
            if not is_wall(self.x, self.y + dy):
                self.y += dy
                
        if self.damage_cooldown > 0:
            self.damage_cooldown -= dt

    def draw(self, player):
        rel_x = self.x - player.x
        rel_y = self.y - player.y
        dist = math.hypot(rel_x, rel_y)
        if dist < 0.2:
            return
        angle = math.atan2(rel_y, rel_x) - player.angle
        angle = (angle + math.pi) % (2 * math.pi) - math.pi
        
        if abs(angle) > player.fov / 2 + 0.4:
            return
            
        screen_x = WIDTH / 2 + math.tan(angle) * WIDTH / (2 * math.tan(player.fov / 2))
        sprite_height = min(HEIGHT, (HEIGHT / dist) * 1.8)
        sprite_width = sprite_height * 0.7
        sprite_y = HEIGHT / 2 - sprite_height / 2
        sprite_rect = pygame.Rect(screen_x - sprite_width / 2, sprite_y, sprite_width, sprite_height)

        if dist < 8:
            # DYNAMIC DAMAGE TRANSPARENCY: Blends red down based on remaining health percentage
            health_percentage = max(0.0, min(1.0, self.health / 100.0))
            
            # The red channel drops, fading them into a ghostly dark shade
            r = int(70 + (185 * health_percentage))
            g = int(20 * health_percentage)
            b = int(20 * health_percentage)
            enemy_color = (r, g, b)
            
            pygame.draw.rect(screen, enemy_color, sprite_rect)


class AmmoPickup:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bob_timer = random.uniform(0, 10)

    def update(self, player):
        self.bob_timer += 0.05
        if distance(self.x, self.y, player.x, player.y) < 0.4:
            player.ammo = min(30, player.ammo + 12)
            return True  
        return False

    def draw(self, player):
        rel_x = self.x - player.x
        rel_y = self.y - player.y
        dist = math.hypot(rel_x, rel_y)
        if dist < 0.2:
            return
        angle = math.atan2(rel_y, rel_x) - player.angle
        angle = (angle + math.pi) % (2 * math.pi) - math.pi
        
        if abs(angle) > player.fov / 2 + 0.4:
            return
            
        screen_x = WIDTH / 2 + math.tan(angle) * WIDTH / (2 * math.tan(player.fov / 2))
        sprite_height = min(HEIGHT, (HEIGHT / dist) * 0.6)
        sprite_width = sprite_height * 1.0
        
        bob_offset = math.sin(self.bob_timer) * (sprite_height * 0.15)
        sprite_y = (HEIGHT / 2) + (sprite_height * 0.2) + bob_offset
        
        sprite_rect = pygame.Rect(screen_x - sprite_width / 2, sprite_y, sprite_width, sprite_height)
        if dist < 8:
            pygame.draw.rect(screen, GREEN, sprite_rect, border_radius=3)
            pygame.draw.rect(screen, GOLD, (screen_x - sprite_width/4, sprite_y + sprite_height/3, sprite_width/2, sprite_height/3))


hud_font = pygame.font.SysFont(None, 30)
game_over_font = pygame.font.SysFont(None, 70)

# Initialize Entities
enemies = [Enemy(8.5, 8.5), Enemy(12.5, 3.5), Enemy(15.0, 8.5)]
ammo_pickups = [AmmoPickup(5.5, 5.5)]
player = Player()

enemy_spawn_timer = 0
ammo_spawn_timer = 0
hitmarker_timer = 0  # <--- ADD THIS LINE HERE

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

running = True
while running:
    dt = clock.tick(60)
    mouse_dx = 0

    enemy_spawn_timer += dt
    ammo_spawn_timer += dt

    if hitmarker_timer > 0:            # <--- ADD THESE TWO LINES
        hitmarker_timer -= dt          # <--- TO FADE OUT THE HITMARKER

    # Spawner: Max 7 enemies, spawns every 4 seconds
    if enemy_spawn_timer >= 4000:
        enemy_spawn_timer = 0
        if len(enemies) < 7:
            ex, ey = get_random_empty_floor()
            enemies.append(Enemy(ex, ey))

    # Spawner: Ammo items spawn every 1 seconds (approx 2.5 per min)
    if ammo_spawn_timer >= 1000:
        ammo_spawn_timer = 0
        if len(ammo_pickups) < 5:
            ax, ay = get_random_empty_floor()
            ammo_pickups.append(AmmoPickup(ax, ay))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r and player.ammo < 12:
                player.ammo = 12
        elif event.type == pygame.MOUSEMOTION:
            mouse_dx += event.rel[0]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and player.health > 0:
                shot_ok = player.shoot()
                if shot_ok:
                    for enemy in enemies[:]:
                        dx = enemy.x - player.x
                        dy = enemy.y - player.y
                        dist = math.hypot(dx, dy)
                        aim_angle = math.atan2(dy, dx)
                        angle_diff = (aim_angle - player.angle + math.pi) % (2 * math.pi) - math.pi
                        if dist < 6 and abs(angle_diff) < 0.18:
                            enemy.health -= 35
                            hitmarker_timer = 150  # <--- ADD THIS LINE (Lasts 150 milliseconds)
                            if enemy.health <= 0:
                                enemies.remove(enemy)

    if player.health > 0:
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.turn(1 if keys[pygame.K_RIGHT] else 0)
        player.turn(-1 if keys[pygame.K_LEFT] else 0)
        if mouse_dx != 0:
            player.angle += math.radians(mouse_dx * 0.12)

        if is_wall(player.x, player.y):
            player.x, player.y = 2.5, 2.5

        for enemy in enemies:
            enemy.update(player, dt)
            
        for pickup in ammo_pickups[:]:
            if pickup.update(player):
                ammo_pickups.remove(pickup)

    # Rendering Scene
    draw_background()
    draw_walls(player)
    
    render_queue = []
    for e in enemies:
        render_queue.append((distance(player.x, player.y, e.x, e.y), e))
    for p in ammo_pickups:
        render_queue.append((distance(player.x, player.y, p.x, p.y), p))
        
    render_queue.sort(key=lambda item: item[0], reverse=True)
    for _, entity in render_queue:
        entity.draw(player)

    # UI Health Bar & Ammo
    pygame.draw.rect(screen, BLACK, (20, 20, 220, 18))
    if player.health > 0:
        pygame.draw.rect(screen, GREEN, (20, 20, 220 * (player.health / 100), 18))
    
    label = hud_font.render(f"Ammo: {player.ammo}", True, WHITE)
    screen.blit(label, (20, 45))

    # Crosshair
    cx, cy = WIDTH // 2, HEIGHT // 2
    pygame.draw.line(screen, WHITE, (cx - 8, cy), (cx + 8, cy), 2)
    pygame.draw.line(screen, WHITE, (cx, cy - 8), (cx, cy + 8), 2)

    # Minimap
    mini_size = 150
    mini_x = WIDTH - mini_size - 20
    mini_y = 20
    for gy, row in enumerate(MAP):
        for gx, cell in enumerate(row):
            color = GRAY if cell == '#' else (30, 30, 30)
            pygame.draw.rect(screen, color, (mini_x + gx * 6, mini_y + gy * 6, 5, 5))
            
    for enemy in enemies:
        pygame.draw.circle(screen, RED, (int(mini_x + enemy.x * 6), int(mini_y + enemy.y * 6)), 2)
    for pickup in ammo_pickups:
        pygame.draw.circle(screen, GOLD, (int(mini_x + pickup.x * 6), int(mini_y + pickup.y * 6)), 2)

    # ==========================================
    # GEOMETRY DASH WAVE STYLE PLAYER INDICATOR
    # ==========================================
    # 1. Get the center position of the player on the minimap
    px = mini_x + player.x * 6
    py = mini_y + player.y * 6
    
    # 2. Calculate the three corner points of the wave triangle based on player.angle
    # The tip points forward, the other two points form the back corners
    tip_x = px + math.cos(player.angle) * 7
    tip_y = py + math.sin(player.angle) * 7
    
    back_left_x = px + math.cos(player.angle + math.radians(140)) * 5
    back_left_y = py + math.sin(player.angle + math.radians(140)) * 5
    
    back_right_x = px + math.cos(player.angle - math.radians(140)) * 5
    back_right_y = py + math.sin(player.angle - math.radians(140)) * 5
    
    # 3. Draw the sleek solid white Wave icon triangle
    pygame.draw.polygon(screen, WHITE, [(tip_x, tip_y), (back_left_x, back_left_y), (back_right_x, back_right_y)])
    
    pygame.draw.circle(screen, WHITE, (int(mini_x + player.x * 6), int(mini_y + player.y * 6)), 3)

    if player.health <= 0:
        go_lbl = game_over_font.render("GAME OVER", True, RED)
        screen.blit(go_lbl, (WIDTH//2 - go_lbl.get_width()//2, HEIGHT//2 - 80))
        esc_lbl = hud_font.render("Press ESC to exit game", True, WHITE)
        screen.blit(esc_lbl, (WIDTH//2 - esc_lbl.get_width()//2, HEIGHT//2 + 10))



    pygame.display.flip()

pygame.quit()
