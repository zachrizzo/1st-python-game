import pygame


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((8000, 20))

        # Change the fill color to brown
        BROWN = (139, 69, 19)
        self.image.fill(BROWN)

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 500

    # make it collide with everything
    def update(self):
        self.rect.x = 0
        self
