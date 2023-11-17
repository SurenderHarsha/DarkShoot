import pygame as p
import pygame.gfxdraw as pgf
import sys
import math
from settings import *






# 20 and 15
def box_to_coordinate(h1x, h1y, box_pos):
    c_x = p_x + (box_pos[0] - h1x) * box_size
    c_y = p_y + (box_pos[1] - h1y) * box_size
    return c_x, c_y
def render_box(sc, h1x, h1y, box_pos):
    c_x = p_x + (box_pos[0] - h1x)*box_size - box_size/2
    c_y = p_y + (box_pos[1] - h1y)*box_size - box_size/2
    sc.blit(floor, (c_x, c_y))
def is_point_in_arc(p, arcangle):
    dist = math.sqrt((p[0] - p_x)**2 + (p[1] - p_y)**2)
    if dist < fov_dist:
        s_x, s_y = p[0] - p_x, p[1] - p_y
        new_arc = math.degrees(math.atan2(s_y, s_x))
        if new_arc < 0:
            na = new_arc + 360
        else:
            na = new_arc
        print(na)
        anglediff = (na - arcangle + 180 + 360) % 360 - 180
        if anglediff <= fov_angle and anglediff>=-fov_angle:
            return True
        else:
            return False

    else:
        return False
def render_available_boxes(sc, h1x, h1y, l_x, u_x, l_y, u_y, arcangle):
    for i in range(int(l_x), int(u_x)):
        for j in range(int(l_y), int(u_y)):
            cc = box_to_coordinate(h1x, h1y, (i, j))
            if is_point_in_arc(cc, arcangle):
                render_box(sc, h1x, h1y, (i,j))
            #render_box(sc, h1x, h1y, (i,j))


def DrawFOV(surface, color, center, radius, startAngle, stopAngle):
    points = [center]
    for i in range(int(startAngle), int(stopAngle) + 1):
        ax, ay = center[0] + radius * math.cos(math.radians(i)), \
                 center[1] + radius * math.sin(math.radians(i))
        points.append((ax, ay))
    points.append(center)
    pgf.filled_polygon(surface, points, color)
    return points


class Bullet:

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.pos = [x, y]

    def draw(self):
        bullet = font.render("-", True, red, None)
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
#p_x, p_y = 200, 300
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
    # if keys[p.K_w]:
    #     p_y -= player_move
    # if keys[p.K_a]:
    #     p_x -= player_move
    # if keys[p.K_d]:
    #     p_x += player_move
    # if keys[p.K_s]:
    #     p_y += player_move


    hx, hy = np.where(map == H)
    lower_x, upper_x = max(0, hx[0] - x_boxes/2), min(screen_size[0], hx[0] + x_boxes/2)
    lower_y, upper_y = max(0, hy[0] - y_boxes/2), min(screen_size[0], hy[0] + y_boxes/2)

    pos = p.mouse.get_pos()
    text = font.render("->", True, red, None)
    text_rect = text.get_rect()
    text_rect.center = (p_x, p_y)

    surf = p.Surface((fov_dist * 2, fov_dist * 2))
    s_rect = surf.get_rect()
    s_rect.center = (p_x, p_y)
    shifted_x, shifted_y = pos[0] - p_x, pos[1] - p_y
    out = math.degrees(math.atan2(shifted_y, shifted_x))
    if out < 0:
        a = out + 360
    else:
        a = out
    text = p.transform.rotozoom(text, 360 - a, 1)

    render_available_boxes(screen, hx[0], hy[0], lower_x, upper_x, lower_y, upper_y, a)
    points = DrawFOV(screen, light_yellow, (p_x, p_y), fov_dist, a - fov_angle, a + fov_angle)
    #pgf.pie(screen, int(p_x), int(p_y), fov_dist, int(a - fov_angle), int(a + fov_angle), yellow)
    # p.draw.arc(screen, yellow, s_rect, math.radians(360 - a - fov_angle), math.radians(360 - a + fov_angle))
    left_angle = 360 - a - fov_angle
    right_angle = 360 - a + fov_angle
    ax, ay = p_x + fov_dist * math.cos(math.radians(-left_angle)), \
             p_y + fov_dist * math.sin(math.radians(-left_angle))
    # p.draw.line(screen, yellow, (p_x, p_y), (ax, ay))
    bx, by = p_x + fov_dist * math.cos(math.radians(-right_angle)), \
             p_y + fov_dist * math.sin(math.radians(-right_angle))
    # p.draw.line(screen, yellow, (p_x, p_y), (bx, by))
    if mouse_pressed:
        bullets.append(Bullet(p_x, p_y, 360 - a))
        mouse_pressed = False
    for b in bullets:
        b.draw()
    screen.blit(text, text_rect)
    p.display.flip()
