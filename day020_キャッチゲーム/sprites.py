# sprites.py

import pygame
import random
from settings import WIDTH, HEIGHT, tile_size


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] * tile_size, pos[1] * tile_size)
        self.facing_right = True
    def update(self):
        pass
    def move_left(self):
        if self.rect.left > 0:
            self.rect.x -= tile_size
            if self.facing_right:
                self.image = pygame.transform.flip(self.original_image, True, False)
                self.facing_right = False
    def move_right(self):
        if self.rect.right < WIDTH:
            self.rect.x += tile_size
            if not self.facing_right:
                self.image = self.original_image
                self.facing_right = True

class FallingObject(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.reset()
    def update(self):
        self.rect.y += 3 #speed
        #if self.rect.y > HEIGHT:
        #    self.reset()
    def reset(self):
        self.rect.x = random.randint(0, WIDTH // tile_size - 1) * tile_size
        self.rect.y = 0