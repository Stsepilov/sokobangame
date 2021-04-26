import os
import sys

import pygame


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


def load_image(name, color_key=None):
    full_name = os.path.join('data', name)

    if not os.path.isfile(full_name):
        print(f"Файл с изображением '{full_name}' не найден")
        sys.exit()

    image = pygame.image.load(full_name)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()

    return image


def main():
    pygame.init()
    size = width, height = 1366, 768
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Арканоид')
    clock = pygame.time.Clock()
    fps = 60
    paddle_speed = 15

    sprites = pygame.sprite.Group()
    sprites1 = pygame.sprite.Group()
    sprites2 = pygame.sprite.Group()
    start_btn = pygame.sprite.Sprite(sprites1)
    start_btn.image = load_image('start_btn.png')
    start_btn.rect = start_btn.image.get_rect()
    start_btn.rect.x = 683
    start_btn.rect.y = 600
    on_btn = pygame.sprite.Sprite(sprites1)
    on_btn.image = load_image('on.png')
    on_btn.rect = on_btn.image.get_rect()
    on_btn.rect.x = 1300
    off_btn = pygame.sprite.Sprite(sprites2)
    off_btn.image = load_image('off.png')
    off_btn.rect = off_btn.image.get_rect()
    off_btn.rect.x = 1300

    img = pygame.image.load("1.png")
    image = pygame.image.load("start.png")
    img2 = pygame.image.load('gameover.png')
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.set_volume(0.03)
    paddle = pygame.sprite.Sprite(sprites)
    paddle.image = load_image("1234.png")
    paddle.rect = paddle.image.get_rect()
    sprites.add(paddle)
    paddle.rect.x = 483
    n, k, d = 0, 0, 0
    paddle.rect.y = 700
    ball = pygame.sprite.Sprite(sprites)
    ball.image = load_image("123.png")
    ball.rect = ball.image.get_rect()
    ball.rect.x = 640
    sprites.add(paddle)
    block_list = []
    ball_speed = 8
    dx, dy = 1, -1
    ball.rect.y = 675
    ball_radius = 35
    for j in range(9):
        block = pygame.sprite.Sprite(sprites)
        block.image = load_image("block1.png")
        block.rect = block.image.get_rect()
        block.rect.x = 20 + 150 * j
        block.rect.y = 40
        block_list.append(block.rect)
        sprites.add(paddle)
    for j in range(9):
        block = pygame.sprite.Sprite(sprites)
        block.image = load_image("block2.png")
        block.rect = block.image.get_rect()
        block.rect.x = 20 + 150 * j
        block.rect.y = 90
        block_list.append(block.rect)
        sprites.add(paddle)
    for j in range(9):
        block = pygame.sprite.Sprite(sprites)
        block.image = load_image("block3.png")
        block.rect = block.image.get_rect()
        block.rect.x = 20 + 150 * j
        block.rect.y = 140
        block_list.append(block.rect)
    for j in range(9):
        block = pygame.sprite.Sprite(sprites)
        block.image = load_image("block4.png")
        block.rect = block.image.get_rect()
        block.rect.x = 20 + 150 * j
        block.rect.y = 190
        block_list.append(block.rect)
    for j in range(9):
        block = pygame.sprite.Sprite(sprites)
        block.image = load_image("block5.png")
        block.rect = block.image.get_rect()
        block.rect.x = 20 + 150 * j
        block.rect.y = 240
        block_list.append(block.rect)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pygame.key.get_pressed()[pygame.K_r] and n != 0:
                main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_btn.rect.collidepoint(mouse_pos):
                    if d != 1:
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.stop()
                    k = 1

        if k == 1:
            screen.blit(img, (0, 0))
            sprites.draw(screen)

            ball.rect.x += ball_speed * dx
            ball.rect.y += ball_speed * dy
            if ball.rect.centerx < ball_radius or ball.rect.centerx > width - ball_radius:
                dx = -dx
            if ball.rect.centery < ball_radius:
                dy = -dy
            if ball.rect.colliderect(paddle.rect) and dy > 0:
                dx, dy = detect_collision(dx, dy, ball.rect, paddle.rect)
            hit_index = ball.rect.collidelist(block_list)
            if hit_index != -1:
                hit_rect = block_list.pop(hit_index)

                dx, dy = detect_collision(dx, dy, ball.rect, hit_rect)
                hit_rect.x = hit_rect.x * 100
                hit_rect.y = hit_rect.y * 100
                sound = pygame.mixer.Sound('music2.wav')
                if d != 1:
                    sound.set_volume(0.1)
                else:
                    sound.set_volume(0)
                sound.play()
                fps += 1
            if ball.rect.bottom >= height:
                n += 1
                if n >= 2:
                    continue
                else:
                    pygame.mixer.music.stop()
                    sound = pygame.mixer.Sound('music1.mp3')
                    if d != 1:
                        sound.set_volume(0.05)
                    else:
                        sound.set_volume(0)
                    sound.play()
                    screen.blit(img2, (0, 0))

            elif not len(block_list):
                print('WIN!!!')

            if pygame.key.get_pressed()[pygame.K_LEFT] and paddle.rect.left > 10:
                paddle.rect.x -= paddle_speed
                paddle.rect.left -= paddle_speed
            if pygame.key.get_pressed()[pygame.K_RIGHT] and paddle.rect.right < width + 8:
                paddle.rect.x += paddle_speed
                paddle.rect.right += paddle_speed
            pygame.display.flip()
            clock.tick(fps)
        else:
            screen.blit(image, (0, 0))
            sprites1.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if on_btn.rect.collidepoint(mouse_pos):
                        on_btn.rect.x = 1000000000
                        d = 1
                    elif off_btn.rect.collidepoint(mouse_pos):
                        on_btn.rect.x = 1300
                        d = 0
            if d == 1:
                sprites2.draw(screen)
            pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
