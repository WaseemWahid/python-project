
import pygame
from settings import *

from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice

class Level:
    def __init__(self):
        
        #get the display surface 
        self.display_surace = pygame.display.get_surface()
        # sprite group set uip
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()


    def create_map(self):
        layout = {
            'boundary': import_csv_layout('map_FloorBlocks.csv'),
            'grass': import_csv_layout('map_Grass.csv'),
            'object': import_csv_layout('map_LargeObjects.csv')
        }
        graphics = {
            'grass': import_folder('grass'),
            'objects': import_folder('objects')
        }

        for style, layout in layout.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col!='-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_img = choice(graphics['grass'])
                            Tile((x,y),[self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_img)
                        if style == 'object':
                            surface = graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites, self.obstacle_sprites], 'object', surface)

        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacle_sprites)



    def run(self):
        #update draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        #general setup
        super().__init__()
        self.display_surace = pygame.display.get_surface()
        self.half_width = self.display_surace.get_size()[0] // 2
        self.half_height= self.display_surace.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load('ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
        

    def custom_draw(self, player):
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing ther floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surace.blit(self.floor_surf, floor_offset_pos)
        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surace.blit(sprite.image, offset_pos)

        