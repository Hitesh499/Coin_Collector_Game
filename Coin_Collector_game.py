import pygame
import random
import time
import sys
import os

# --- FIXED: PyInstaller-compatible path resolution ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # For PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()
pygame.mixer.init()

pygame.display.set_icon(pygame.image.load(resource_path("icon.png")))

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collect the Coins!")

# --- FIXED: All asset loads use resource_path and proper scaling ---
walk_right = pygame.transform.scale(
    pygame.image.load(resource_path("walk_right.png")), (50, 50))
walk_left = pygame.transform.scale(
    pygame.image.load(resource_path("walk_left.png")), (50, 50))
walk_up = pygame.transform.scale(
    pygame.image.load(resource_path("walk_up.png")), (50, 50))
walk_down = pygame.transform.scale(
    pygame.image.load(resource_path("walk_down.png")), (50, 50))
player_imgs = {
    "right": walk_right,
    "left": walk_left,
    "up": walk_up,
    "down": walk_down
}

coin_img = pygame.transform.scale(
    pygame.image.load(resource_path("coin.png")), (32, 32))
object_img = pygame.transform.scale(
    pygame.image.load(resource_path("object.png")), (40, 40))
ball_img = pygame.transform.scale(
    pygame.image.load(resource_path("ball.png")), (25, 25))

# --- FIXED: Sound loading using resource_path ---
pygame.mixer.music.load(resource_path("background.mp3"))
pygame.mixer.music.play(-1)

coin_sound = pygame.mixer.Sound(resource_path("coin_pick.wav"))
game_over_sound = pygame.mixer.Sound(resource_path("game_over.mp3"))

# Font and colors
font = pygame.font.SysFont('comicsans', 40)
BLACK, YELLOW, WHITE, RED, GREEN = (0, 0, 0), (255, 255, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0)

def draw_start_screen():
    win.fill((20, 20, 60))
    title = font.render("Collect the Coins!", True, WHITE)

    small_font = pygame.font.SysFont('comicsans', 30)  # Smaller font for button text
    start_btn_text = small_font.render("START THE GAME", True, BLACK)

    btn_rect = pygame.Rect(WIDTH // 2 - 190, HEIGHT // 2, 380, 70)  # Wider button
    pygame.draw.rect(win, GREEN, btn_rect)

    win.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
    win.blit(start_btn_text, (btn_rect.x + (btn_rect.width - start_btn_text.get_width()) // 2,
                              btn_rect.y + (btn_rect.height - start_btn_text.get_height()) // 2))
    pygame.display.update()
    return btn_rect


def wait_for_start():
    while True:
        btn_rect = draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(event.pos):
                    return

def restart_game():
    pygame.mixer.music.play(-1)
    main()

def draw_game_over(score, elapsed_time):
    win.fill((30, 0, 0))
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, YELLOW)
    time_text = font.render(f"Time: {elapsed_time}s", True, WHITE)

    win.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 80))
    win.blit(score_text, (WIDTH // 2 - 120, HEIGHT // 2 - 20))
    win.blit(time_text, (WIDTH // 2 - 100, HEIGHT // 2 + 30))

    restart_btn = pygame.Rect(250, 400, 200, 60)
    exit_btn = pygame.Rect(500, 400, 220, 60)
    pygame.draw.rect(win, GREEN, restart_btn)
    pygame.draw.rect(win, RED, exit_btn)

    small_font = pygame.font.SysFont('comicsans', 30)
    restart_text = small_font.render("RESTART", True, BLACK)
    exit_text = small_font.render("EXIT GAME", True, BLACK)

    win.blit(restart_text, (restart_btn.x + (restart_btn.width - restart_text.get_width()) // 2,
                            restart_btn.y + (restart_btn.height - restart_text.get_height()) // 2))
    win.blit(exit_text, (exit_btn.x + (exit_btn.width - exit_text.get_width()) // 2,
                         exit_btn.y + (exit_btn.height - exit_text.get_height()) // 2))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    restart_game()
                elif exit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def main():
    wait_for_start()

    player_rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 50, 50)
    player_speed = 5
    player_direction = "down"
    score = 0
    start_time = time.time()
    game_over = False

    coins = [pygame.Rect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), 32, 32) for _ in range(5)]
    objects = [pygame.Rect(0, 0, 40, 40), pygame.Rect(WIDTH - 40, 0, 40, 40),
               pygame.Rect(0, HEIGHT - 40, 40, 40), pygame.Rect(WIDTH - 40, HEIGHT - 40, 40, 40)]
    for _ in range(8):
        objects.append(pygame.Rect(random.randint(0, WIDTH-40), random.randint(0, HEIGHT-40), 40, 40))

    balls = []
    next_ball_time = time.time() + 5
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)
        win.fill(BLACK)

        if game_over:
            pygame.mixer.music.stop()
            game_over_sound.play()
            elapsed_time = int(time.time() - start_time)
            draw_game_over(score, elapsed_time)
            return

        # Draw
        win.blit(player_imgs[player_direction], player_rect.topleft)
        for coin in coins:
            win.blit(coin_img, coin.topleft)
        for obj in objects:
            win.blit(object_img, obj.topleft)
        for ball in balls:
            rect, speed = ball
            win.blit(ball_img, rect.topleft)

        elapsed_time = int(time.time() - start_time)
        win.blit(font.render(f"Score: {score}", True, YELLOW), (20, 20))
        win.blit(font.render(f"Time: {elapsed_time}s", True, WHITE), (WIDTH - 200, 20))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -player_speed
            player_direction = "left"
        elif keys[pygame.K_RIGHT]:
            dx = player_speed
            player_direction = "right"
        elif keys[pygame.K_UP]:
            dy = -player_speed
            player_direction = "up"
        elif keys[pygame.K_DOWN]:
            dy = player_speed
            player_direction = "down"

        next_rect = player_rect.move(dx, dy)
        if win.get_rect().contains(next_rect) and not any(next_rect.colliderect(obj) for obj in objects):
            player_rect = next_rect

        for coin in coins[:]:
            if player_rect.colliderect(coin):
                coins.remove(coin)
                coins.append(pygame.Rect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), 32, 32))
                score += 1
                coin_sound.play()

        if time.time() > next_ball_time:
            for _ in range(2):
                edge = random.choice(["left", "right", "top", "bottom"])
                if edge == "left":
                    rect = pygame.Rect(0, random.randint(0, HEIGHT-25), 25, 25)
                    speed = [random.randint(3, 6), random.randint(-3, 3)]
                elif edge == "right":
                    rect = pygame.Rect(WIDTH-25, random.randint(0, HEIGHT-25), 25, 25)
                    speed = [-random.randint(3, 6), random.randint(-3, 3)]
                elif edge == "top":
                    rect = pygame.Rect(random.randint(0, WIDTH-25), 0, 25, 25)
                    speed = [random.randint(-3, 3), random.randint(3, 6)]
                else:
                    rect = pygame.Rect(random.randint(0, WIDTH-25), HEIGHT-25, 25, 25)
                    speed = [random.randint(-3, 3), -random.randint(3, 6)]
                balls.append((rect, speed))
            next_ball_time = time.time() + random.randint(2, 10)

        new_balls = []
        for rect, speed in balls:
            rect.x += speed[0]
            rect.y += speed[1]

            for obj in objects:
                if rect.colliderect(obj):
                    if abs(rect.right - obj.left) < 10 or abs(rect.left - obj.right) < 10:
                        speed[0] *= -1
                    if abs(rect.bottom - obj.top) < 10 or abs(rect.top - obj.bottom) < 10:
                        speed[1] *= -1

            if rect.colliderect(player_rect):
                game_over = True

            if win.get_rect().contains(rect):
                new_balls.append((rect, speed))
        balls = new_balls

main()
