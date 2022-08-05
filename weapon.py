import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        direction = player.status.split('_', [0])


        # Graphic of the weapon
        self.image = pygame.Surface((40,40))
        # Placement of the weapon 
        if direction == 'right':
            self.rect = self.image.get_rect(center = player.rect.center)