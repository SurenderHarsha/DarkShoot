import pygame as p
import sys
import math

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)
yellow = (255, 255, 0)
screen_size = (1200, 700)
title = "DarkClient"
font_name = 'freesansbold.ttf'
font_size = 32
player_move = 3
bullet_velocity = 20
fov_dist = 300
fov_angle = 50

class Bullet:

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.pos = [x, y]

    def draw(self):
        bullet = font.render("-", True, blue, None)
        t = bullet.get_rect()
        t.center = (self.pos[0], self.pos[1])
        bullet = p.transform.rotozoom(bullet, self.angle, 1)
        self.pos[0] += bullet_velocity * math.cos(math.radians(self.angle))
        self.pos[1] -= bullet_velocity * math.sin(math.radians(self.angle))
        screen.blit(bullet, t)


p.init()
screen = p.display.set_mode(screen_size)
p.display.set_caption(title)

clock = p.time.Clock()
font = p.font.Font(font_name, font_size)

n_fps = 60
p_x, p_y = 200, 300
active = True
bullets = []
while active:

    clock.tick(n_fps)
    e = p.event.get()
    mouse_pressed = False
    screen.fill(black)
    for events in e:
        if events.type == p.MOUSEBUTTONDOWN:
            mouse_pressed = True
        if events.type == p.QUIT:
            sys.exit()
        if events.type == p.KEYDOWN and events.key == p.K_RETURN:
            active = False
            break
    keys = p.key.get_pressed()
    if keys[p.K_w]:
        p_y -= player_move
    if keys[p.K_a]:
        p_x -= player_move
    if keys[p.K_d]:
        p_x += player_move
    if keys[p.K_s]:
        p_y += player_move
    pos = p.mouse.get_pos()
    text = font.render("->", True, red, None)
    text_rect = text.get_rect()
    text_rect.center = (p_x, p_y)

    surf = p.Surface((fov_dist*2, fov_dist*2))
    s_rect = surf.get_rect()
    s_rect.center = (p_x, p_y)
    shifted_x, shifted_y = pos[0] - p_x, pos[1] - p_y
    out = math.degrees(math.atan2(shifted_y, shifted_x))
    if out < 0:
        a = out + 360
    else:
        a = out
    text = p.transform.rotozoom(text, 360 - a, 1)
    p.draw.arc(screen, yellow, s_rect, math.radians(360 - a - fov_angle), math.radians(360 - a + fov_angle))
    left_angle = 360 - a - fov_angle
    right_angle = 360 - a + fov_angle
    ax, ay = p_x + fov_dist * math.cos(math.radians(-left_angle)),\
        p_y + fov_dist * math.sin(math.radians(-left_angle))
    p.draw.line(screen, yellow, (p_x, p_y), (ax, ay))
    bx, by = p_x + fov_dist * math.cos(math.radians(-right_angle)), \
        p_y + fov_dist * math.sin(math.radians(-right_angle))
    p.draw.line(screen, yellow, (p_x, p_y), (bx, by))
    if mouse_pressed:
        bullets.append(Bullet(p_x, p_y, 360-a))
        mouse_pressed = False
    for b in bullets:
        b.draw()
    screen.blit(text, text_rect)
    p.display.flip()
