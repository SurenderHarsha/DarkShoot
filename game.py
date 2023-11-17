import sys

import pygame as p
from settings import *
from world import Player


class Game:

    def __init__(self):
        p.init()
        self.screen = p.display.set_mode(screen_size)
        p.display.set_caption(title)

        self.clock = p.time.Clock()
        self.font = p.font.Font(font_name, font_size)
        self.active = True
        self.bullets = []
        self.player = Player((player_start_x, player_start_y))

    def run(self):
        while self.active:

            self.clock.tick(fps)
            e = p.event.get()
            mouse_pressed = False
            self.screen.fill(black)
            for events in e:
                if events.type == p.MOUSEBUTTONDOWN:
                    mouse_pressed = True
                if events.type == p.QUIT:
                    sys.exit()
                if events.type == p.KEYDOWN and events.key == p.K_RETURN:
                    active = False
                    break
            keys = p.key.get_pressed()
            pos = p.mouse.get_pos()
            self.player.update(self.screen, keys, pos)
            p.display.flip()

