from draw_utils import draw_fov, get_fov_angle, compute_boxes
from settings import *
import pygame as p


class Player:

    def __init__(self, start_box_pos):
        self.player_global_x = start_box_pos[1] * box_size + box_size/2
        self.player_global_y = start_box_pos[0] * box_size + box_size/2
        self.player_box_x = start_box_pos[0]
        self.player_box_y = start_box_pos[1]
        self.player_image = p.image.load('player.png')
        self.player_image = p.transform.scale(self.player_image, (box_size, box_size))
        self.player_image = p.transform.rotozoom(self.player_image, -90, 1)
        map[start_box_pos[0]][start_box_pos[1]] = H
        self.fov_dist = fov_dist
        self.old_movable_place = '.'
        self.fov_angle = fov_angle

    def draw_player(self, screen, angle):
        player_rect = self.player_image.get_rect()
        player_rect.center = (player_local_x, player_local_y)
        self.player_obj = p.transform.rotozoom(self.player_image, 360 - angle, 1)
        screen.blit(self.player_obj, player_rect)

    def update_coords_with_keys(self, keys):

            self.player_global_y += player_move
    def update_map(self, keys):
        old_player_global_y = self.player_global_y
        old_player_global_x = self.player_global_x
        if keys[p.K_w]:
            self.player_global_y -= player_move
        if keys[p.K_a]:
            self.player_global_x -= player_move
        if keys[p.K_d]:
            self.player_global_x += player_move
        if keys[p.K_s]:
            self.player_global_y += player_move
        if self.player_global_x <= 0 or self.player_global_x >= global_x_max or self.player_global_y <=0 or self.player_global_y >= global_y_max:
            self.player_global_x = old_player_global_x
            self.player_global_y = old_player_global_y
        box_x = int(self.player_global_y/box_size)
        box_y = int(self.player_global_x/box_size)
        if map[box_x][box_y] not in movable_places and (box_x != self.player_box_x and box_y != self.player_box_y):
            self.player_global_x = old_player_global_x
            self.player_global_y = old_player_global_y
            box_x = int(self.player_global_y / box_size)
            box_y = int(self.player_global_x / box_size)


        map[self.player_box_x][self.player_box_y] = self.old_movable_place
        self.player_box_y = box_y
        self.player_box_x = box_x
        #print(map[box_x][box_y], self.old_movable_place)
        self.old_movable_place = map[box_x][box_y]
        map[box_x][box_y] = H
        center_box_x = box_y * box_size
        center_box_y = box_x * box_size
        shift_x = center_box_x - self.player_global_x
        shift_y = center_box_y - self.player_global_y
        return shift_x, shift_y

    def update(self, screen, keys, pos):
        angle = get_fov_angle(pos)
        s_x, s_y = self.update_map(keys)
        compute_boxes(screen, self.player_box_x, self.player_box_y, angle, (s_x, s_y), self.old_movable_place)
        self.draw_player(screen, angle)
        points = draw_fov(screen, light_yellow, (player_local_x, player_local_y), self.fov_dist,
                          angle - self.fov_angle, angle + self.fov_angle)