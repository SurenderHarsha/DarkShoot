from map import *

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)
yellow = (255, 255, 0)
light_yellow = (255, 255, 0, 20)
fps = 60
screen_size = (1900, 1000)
num_x_boxes = screen_size[0]/box_size
num_y_boxes = screen_size[1]/box_size
title = "DarkClient"
font_name = 'freesansbold.ttf'
font_size = 32
player_move = 3
bullet_velocity = 20
fov_dist = 500
fov_angle = 30
player_local_x = screen_size[0]//2
player_local_y = screen_size[1]//2
