import pygame


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((800, 100))
        # fill the surface with a color black
        self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 500

    # make it collide with everything
    def update(self):
        self.rect.x = 0
        self.rect.y = 500
