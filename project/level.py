import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Wildflower, Tree
from pytmx.util_pygame import load_pygame



class Level:
    
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        
        
        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):

        tmx_data = load_pygame('../data/map.tmx')

        #house
        for layer in ['HouseFloor','HouseFurnitureBottom']:
            for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILESIZE,y*TILESIZE),surf,self.all_sprites,LAYERS['house bottom'])

        for layer in ['HouseWalls','HouseFurnitureTop']:
            for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILESIZE,y*TILESIZE),surf,self.all_sprites)
        
        #trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree((obj.x,obj.y),obj.image,[self.all_sprites,self.collision_sprites],obj.name) 

        #wildflowers
        for obj in tmx_data.get_layer_by_name('Decoration'):
            Wildflower((obj.x,obj.y),obj.image,[self.all_sprites,self.collision_sprites])        


        #collision tiles
        for x,y,surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generic((x*TILESIZE,y*TILESIZE),pygame.Surface((TILESIZE,TILESIZE)),self.collision_sprites)    


        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
               self.player = Player((obj.x,obj.y),self.all_sprites,self.collision_sprites)
        Generic(
            pos=(0,0),
            surf=pygame.image.load('../graphics/world/ground.png').convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS['ground']
        )
    
    def run(self,dt):
        self.display_surface.fill('black')
        #self.all_sprites.draw(self.display_surface)
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)
        self.overlay.display()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0,0)

    def custom_draw(self,player):

        self.offset.x=player.rect.centerx - WIDTH/2
        self.offset.y=player.rect.centery - HEIGHT/2

        for layer in LAYERS.values():
           for sprite in sorted(self.sprites(),key= lambda sprite: sprite.rect.centery):
              if sprite.z == layer:
                offset_rect=sprite.rect.copy()
                offset_rect.center-=self.offset
                self.display_surface.blit(sprite.image,offset_rect)
        
  