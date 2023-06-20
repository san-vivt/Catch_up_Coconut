import pygame
import random

# Function to respawn the target
def respawn_target():
    target_rect.x = random.randint(0, W - target_rect.w)
    target_rect.y = random.randint(0, H - target_rect.h)

pygame.init()
pygame.font.init()

W = 1280
H = 800

black = (0, 0, 0)
white = (255, 255, 255)
purple = (255, 50, 255)
red = (235, 208, 202)
green = (232, 255, 208)

size = (W, H)
center = (W // 2, H // 2)
mid = (W // 2, 0)

monitor = pygame.display.set_mode(size)  # pygame.RESIZABLE
pygame.display.set_caption("Catch up Coconut")
pygame.display.set_icon(pygame.image.load("icon_coconut.png"))

FPS = 60
clock = pygame.time.Clock()

IMPACT_40 = pygame.font.SysFont('impact', 40)
IMPACT_25 = pygame.font.SysFont('impact', 25)

delay = 1200
finish = delay
base = 1.003
last_respawn_time = 0

game_over = False
retry_monitor = IMPACT_25.render('НАЖМИТЕ ЛЮБУЮ КЛАВИШУ', True, black)
retry_rect = retry_monitor.get_rect()
retry_rect.midtop = center

score = 0

target_image = pygame.image.load('coconut.png')
target_image = pygame.transform.scale(target_image, (100, 100))
target_rect = target_image.get_rect()

respawn_target()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if game_over:
                score = 0
                finish = delay
                game_over = False
                last_respawn_time = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if not game_over and target_rect.collidepoint(event.pos):
                    score += 1
                    respawn_target()
                    last_respawn_time = pygame.time.get_ticks()
                    finish = delay / (base ** score)

    clock.tick(FPS)
    monitor.fill(red)

    score_text = IMPACT_40.render(str(score), True, black)
    score_rect = score_text.get_rect()

    now = pygame.time.get_ticks()
    past = now - last_respawn_time

    if past > finish:
        game_over = True
        score_rect.midbottom = center
        monitor.blit(retry_monitor, retry_rect)
    else:
        h = H - H * past / finish
        time_rect = pygame.Rect((0, 0), (W, h))
        time_rect.bottomleft = (0, H)
        pygame.draw.rect(monitor, green, time_rect)

        monitor.blit(target_image, target_rect)
        score_rect.midtop = mid

    monitor.blit(score_text, score_rect)
    pygame.display.flip()

pygame.quit()
