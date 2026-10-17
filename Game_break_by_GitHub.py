import math
import random
import pygame

# ----------------------------
# Simple FPS Game Prototype
# ----------------------------

pygame.init()

WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini FPS")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 70, 70)
GREEN = (90, 220, 90)
BLUE = (70, 120, 255)
GRAY = (80, 80, 90)
DARK = (15, 15, 20)

# Map
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
TILE_SIZE = 1

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
        self.radius = 0.2

    def move(self, keys, enemies, dt):
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

        nx = self.x + dx * dt
        ny = self.y + dy * dt
        if not is_wall(nx, self.y) and not collides_with_enemy(nx, self.y, enemies, self.radius):
            self.x = nx
        if not is_wall(self.x, ny) and not collides_with_enemy(self.x, ny, enemies, self.radius):
            self.y = ny

    def turn(self, direction, dt):
        self.angle += direction * self.turn_speed * dt

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


def collides_with_enemy(x, y, enemies, player_radius):
    return any(
        distance(x, y, enemy.x, enemy.y) < player_radius + enemy.size
        for enemy in enemies
    )


def random_open_position(avoid_positions=(), min_distance=0.0):
    open_tiles = [
        (x + 0.5, y + 0.5)
        for y, row in enumerate(MAP)
        for x, tile in enumerate(row)
        if tile == '.'
    ]
    valid_tiles = [
        position for position in open_tiles
        if all(distance(*position, *other) >= min_distance for other in avoid_positions)
    ]
    return random.choice(valid_tiles) if valid_tiles else None


def cast_ray(player, ray_angle):
    step = 0.02
    max_dist = 20
    dist = 0.0
    hit = False
    wall_x = 0.0
    wall_y = 0.0

    while dist < max_dist and not hit:
        x = player.x + math.cos(ray_angle) * dist
        y = player.y + math.sin(ray_angle) * dist
        if is_wall(x, y):
            hit = True
            wall_x = x
            wall_y = y
        dist += step

    return dist, wall_x, wall_y


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
        dist, wall_x, wall_y = cast_ray(player, ray_angle)
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
        pygame.draw.rect(
            screen,
            color,
            (x, y, max(2, int(column_width) + 1), wall_height),
        )


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.size = 0.35
        self.attack_cooldown = 0.0

    def update(self, player, dt):
        angle_to_player = math.atan2(player.y - self.y, player.x - self.x)
        dx = math.cos(angle_to_player) * 0.5 * dt
        dy = math.sin(angle_to_player) * 0.5 * dt
        target_distance = self.size + player.radius
        current_distance = distance(self.x, self.y, player.x, player.y)
        if current_distance > target_distance:
            if not is_wall(self.x + dx, self.y):
                self.x += dx
            if not is_wall(self.x, self.y + dy):
                self.y += dy
        else:
            self.attack_cooldown -= dt
            if self.attack_cooldown <= 0:
                player.health = max(0, player.health - 10)
                self.attack_cooldown = 1.0

    def draw(self, player):
        rel_x = self.x - player.x
        rel_y = self.y - player.y
        dist = math.hypot(rel_x, rel_y)
        if dist < 0.2:
            return
        angle = math.atan2(rel_y, rel_x) - player.angle
        visible = abs(angle) < player.fov / 2 + 0.4
        if not visible:
            return
        screen_x = WIDTH / 2 + math.tan(angle) * WIDTH / (2 * math.tan(player.fov / 2))
        sprite_height = min(HEIGHT, (HEIGHT / dist) * 1.8)
        sprite_width = sprite_height * 0.7
        sprite_y = HEIGHT / 2 - sprite_height / 2
        sprite_rect = pygame.Rect(screen_x - sprite_width / 2, sprite_y, sprite_width, sprite_height)

        if dist < 7:
            health_ratio = max(0.0, min(1.0, self.health / 100))
            opacity = max(35, int(255 * health_ratio))
            sprite = pygame.Surface(sprite_rect.size, pygame.SRCALPHA)
            sprite.fill((*RED, opacity))
            screen.blit(sprite, sprite_rect.topleft)


class AmmoPickup:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, player, elapsed):
        rel_x = self.x - player.x
        rel_y = self.y - player.y
        dist = math.hypot(rel_x, rel_y)
        angle = math.atan2(rel_y, rel_x) - player.angle
        angle = (angle + math.pi) % (2 * math.pi) - math.pi
        if dist < 0.25 or dist > 10 or abs(angle) > player.fov / 2 + 0.4:
            return
        screen_x = WIDTH / 2 + math.tan(angle) * WIDTH / (2 * math.tan(player.fov / 2))
        sprite_size = min(42, max(8, int(90 / dist)))
        bob = math.sin(elapsed * 4) * 5
        rect = pygame.Rect(
            screen_x - sprite_size / 2,
            HEIGHT / 2 - sprite_size / 2 + bob,
            sprite_size,
            sprite_size,
        )
        pygame.draw.rect(screen, (245, 205, 55), rect, border_radius=4)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=4)


# Create enemies
enemies = [Enemy(8.5, 8.5), Enemy(12.5, 3.5), Enemy(15.0, 8.5)]
ammo_pickups = []
player = Player()

# Mouse aiming
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

running = True
enemy_spawn_timer = 4.0
ammo_spawn_timer = random.uniform(20.0, 30.0)
hit_flash_duration = 0.24
hit_flash_timer = 0.0
max_enemies = 7
while running:
    dt = clock.tick(60) / 1000
    elapsed = pygame.time.get_ticks() / 1000
    mouse_dx = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                player.ammo = 12
        elif event.type == pygame.MOUSEMOTION:
            mouse_dx += event.rel[0]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                shot_ok = player.shoot()
                if shot_ok:
                    for enemy in enemies[:]:
                        dx = enemy.x - player.x
                        dy = enemy.y - player.y
                        dist = math.hypot(dx, dy)
                        aim_angle = math.atan2(dy, dx)
                        if dist < 6 and abs((aim_angle - player.angle + math.pi) % (2 * math.pi) - math.pi) < 0.18:
                            enemy.health -= 35
                            hit_flash_timer = hit_flash_duration
                            if enemy.health <= 0:
                                enemies.remove(enemy)

    keys = pygame.key.get_pressed()
    player.move(keys, enemies, dt)
    player.turn(1 if keys[pygame.K_RIGHT] else 0, dt)
    player.turn(-1 if keys[pygame.K_LEFT] else 0, dt)
    if mouse_dx != 0:
        player.angle += math.radians(mouse_dx * 0.12)

    # Keep player in bounds via map walls
    if is_wall(player.x, player.y):
        player.x = 2.5
        player.y = 2.5

    enemy_spawn_timer -= dt
    if enemy_spawn_timer <= 0:
        if len(enemies) < max_enemies:
            avoid_positions = [(player.x, player.y)] + [(enemy.x, enemy.y) for enemy in enemies]
            spawn_position = random_open_position(avoid_positions, min_distance=3.0)
            if spawn_position:
                enemies.append(Enemy(*spawn_position))
        enemy_spawn_timer = 4.0

    for enemy in enemies:
        enemy.update(player, dt)

    ammo_spawn_timer -= dt
    if ammo_spawn_timer <= 0:
        if len(ammo_pickups) < 3:
            avoid_positions = [(player.x, player.y)]
            avoid_positions.extend((enemy.x, enemy.y) for enemy in enemies)
            avoid_positions.extend((pickup.x, pickup.y) for pickup in ammo_pickups)
            spawn_position = random_open_position(avoid_positions, min_distance=2.0)
            if spawn_position:
                ammo_pickups.append(AmmoPickup(*spawn_position))
        ammo_spawn_timer = random.uniform(20.0, 30.0)

    for pickup in ammo_pickups[:]:
        if distance(player.x, player.y, pickup.x, pickup.y) < 0.55:
            player.ammo = min(30, player.ammo + 8)
            ammo_pickups.remove(pickup)

    # Draw world
    draw_background()
    draw_walls(player)
    for pickup in ammo_pickups:
        pickup.draw(player, elapsed)
    for enemy in enemies:
        enemy.draw(player)

    hit_flash_timer = max(0.0, hit_flash_timer - dt)
    flash_amount = hit_flash_timer / hit_flash_duration
    crosshair_color = tuple(
        int(WHITE[channel] + (RED[channel] - WHITE[channel]) * flash_amount)
        for channel in range(3)
    )
    crosshair_size = 8 + int(4 * flash_amount)
    crosshair_width = 2 + int(flash_amount)

    # HUD
    pygame.draw.rect(screen, BLACK, (20, 20, 220, 18))
    pygame.draw.rect(screen, GREEN, (20, 20, 220 * (player.health / 100), 18))
    ammo_text = f"Ammo: {player.ammo}"
    label = pygame.font.SysFont(None, 30).render(ammo_text, True, WHITE)
    screen.blit(label, (20, 45))

    # Crosshair
    cx, cy = WIDTH // 2, HEIGHT // 2
    pygame.draw.line(screen, crosshair_color, (cx - crosshair_size, cy), (cx + crosshair_size, cy), crosshair_width)
    pygame.draw.line(screen, crosshair_color, (cx, cy - crosshair_size), (cx, cy + crosshair_size), crosshair_width)

    # Minimap
    mini_size = 150
    mini_x = WIDTH - mini_size - 20
    mini_y = 20
    for gy, row in enumerate(MAP):
        for gx, cell in enumerate(row):
            color = WHITE if cell == '#' else (30, 30, 30)
            pygame.draw.rect(screen, color, (mini_x + gx * 5, mini_y + gy * 5, 5, 5))
    player_map_x = mini_x + player.x * 5
    player_map_y = mini_y + player.y * 5
    forward_x = math.cos(player.angle)
    forward_y = math.sin(player.angle)
    side_x = -forward_y
    side_y = forward_x
    wave_points = []
    for index, along in enumerate((-4, -2, 0, 2, 4)):
        across = 2 if index % 2 == 0 else -2
        wave_points.append((
            round(player_map_x + forward_x * along + side_x * across),
            round(player_map_y + forward_y * along + side_y * across),
        ))
    pygame.draw.lines(screen, WHITE, False, wave_points, 5)
    pygame.draw.lines(screen, BLUE, False, wave_points, 3)
    for enemy in enemies:
        pygame.draw.circle(screen, RED, (int(mini_x + enemy.x * 5), int(mini_y + enemy.y * 5)), 3)
    for pickup in ammo_pickups:
        pygame.draw.circle(screen, (245, 205, 55), (int(mini_x + pickup.x * 5), int(mini_y + pickup.y * 5)), 3)

    pygame.display.flip()

pygame.quit()
