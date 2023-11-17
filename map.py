import random

import pygame as p
import numpy as np
box_size = 50
floor = p.image.load('floor.png')
floor = p.transform.scale(floor, (box_size, box_size))
floor2 = p.image.load('floor2.png')
floor2 = p.transform.scale(floor2, (box_size, box_size))


map_width = 50
map_height = 50
movable_places = ['.', '..']

H = "P1"
global_x_max = map_width * box_size
global_y_max = map_height * box_size
map = np.array([[random.choice(movable_places) for i in range(map_width)] for j in range(map_height)])
player_start_x = 25
player_start_y = 25

