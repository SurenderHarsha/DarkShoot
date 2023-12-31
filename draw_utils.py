import pygame as p
import pygame.gfxdraw as pgf
import sys
import math
import time
import rasterio.features

from settings import *
from shapely.geometry import Polygon


def compute_polygon_points( center, radius, startAngle, stopAngle):
    points = [center]
    for i in range(int(startAngle), int(stopAngle) + 1):
        ax, ay = center[0] + radius * math.cos(math.radians(i)), \
                 center[1] + radius * math.sin(math.radians(i))
        points.append((ax, ay))
    points.append(center)
    return points

def draw_fov(surface, color, points):
    pgf.filled_polygon(surface, points, color)
    return points


def get_fov_angle(pos):
    shifted_x, shifted_y = pos[0] - player_local_x, pos[1] - player_local_y
    out = math.degrees(math.atan2(shifted_y, shifted_x))
    if out < 0:
        a = out + 360
    else:
        a = out
    return a

def coordinate_to_box(h1x, h1y, x, y):
    by = (x - player_local_x)/box_size + h1y
    bx = (y - player_local_y)/box_size + h1x
    return int(bx), int(by)
def box_to_coordinate(h1x, h1y, box_pos):
    c_x = player_local_x + (box_pos[1] - h1y) * box_size
    c_y = player_local_y + (box_pos[0] - h1x) * box_size
    # return ((c_x, c_y), (c_x - box_size/2, c_y - box_size/2), (c_x + box_size/2, c_y + box_size/2),
    #         (c_x - box_size/2, c_y + box_size/2), (c_x + box_size/2, c_y - box_size/2))
    return (c_x, c_y)

def render_box(sc, h1x, h1y, box_pos, shifts, under_tile = None, is_player=False):
    c_x = player_local_x + (box_pos[1] - h1y)*box_size - box_size/2 + shifts[0]
    c_y = player_local_y + (box_pos[0] - h1x)*box_size - box_size/2 + shifts[1]
    #cfloor = floor.convert_alpha()
    #cfloor2 = floor2.convert_alpha()
    if is_player:
        if under_tile == movable_places[0]:
            sc.blit(floor, (c_x + box_size/2, c_y + box_size/2))
        elif under_tile == movable_places[1]:
            sc.blit(floor2, (c_x + box_size/2, c_y + box_size/2))
        return
    try:
        if map[box_pos[0]][box_pos[1]] == movable_places[0]:
            sc.blit(floor, (c_x+ box_size/2, c_y+ box_size/2))
        elif map[box_pos[0]][box_pos[1]] == movable_places[1]:
            sc.blit(floor2, (c_x+ box_size/2, c_y+ box_size/2))
    except:
        pass
def is_point_in_arc(p, arcangle):
    dist = math.sqrt((p[0] - player_local_x)**2 + (p[1] - player_local_y)**2)
    if dist < fov_dist:
        s_x, s_y = p[0] - player_local_x, p[1] - player_local_y
        new_arc = math.degrees(math.atan2(s_y, s_x))
        if new_arc < 0:
            na = new_arc + 360
        else:
            na = new_arc
        anglediff = (na - arcangle + 180 + 360) % 360 - 180
        if anglediff <= fov_angle and anglediff>=-fov_angle:
            return True
        else:
            return False

    else:
        return False
def render_available_boxes(sc, h1x, h1y, l_x, u_x, l_y, u_y, arcangle, shifts, under_tile, points):
    visited = []
    poly = Polygon(points)
    print(shifts)
    img = rasterio.features.rasterize([poly], out_shape=(screen_size[1],screen_size[0]))
    y, x = np.where(img == 1)
    #start= time.time()
    for i, j in zip(x, y):
        a, b = coordinate_to_box(h1x, h1y, i, j)
        if map[a][b] != H:
            item_to_blit = floor_dict[map[a][b]]
        else:
            item_to_blit = floor_dict[under_tile]
        ax, ay = box_to_coordinate(h1x, h1y, (a, b))
        sx, sy = i - ax, j - ay
        sc.blit(item_to_blit, (i , j), (sx, sy, 1, 1))
        pass
    #end = time.time()
    #print(end-start)
    # for i in range(int(l_x), int(u_x)):
    #     for j in range(int(l_y), int(u_y)):
    #         cc = box_to_coordinate(h1x, h1y, (i, j))
    #         for k in cc:
    #             if is_point_in_arc(k, arcangle):
    #                 if (i, j) not in visited:
    #                     render_box(sc, h1x, h1y, (i,j), shifts)
    #                     visited.append((i,j))
    # render_box(sc, h1x, h1y, (h1x, h1y), shifts, under_tile, is_player=True)
    # #Create combo from a function to detect edge cases
    # combos = [(h1x+1, h1y+1),
    #           (h1x+1, h1y-1),
    #           (h1x-1, h1y+1),
    #           (h1x-1, h1y-1),
    #           (h1x, h1y+1),
    #           (h1x+1, h1y),
    #           (h1x, h1y-1),
    #           (h1x-1, h1y)]
    # for i in range(8):
    #     render_box(sc, h1x, h1y, combos[i], shifts)



def compute_boxes(screen, hx, hy, angle, shifts, under_tile, points):
    lower_x, upper_x = max(0, hx - num_x_boxes ), min(map_height, hx + num_x_boxes )
    lower_y, upper_y = max(0, hy - num_y_boxes ), min(map_width, hy + num_y_boxes )
    render_available_boxes(screen, hx, hy, lower_x, upper_x, lower_y, upper_y, angle, shifts, under_tile, points)
