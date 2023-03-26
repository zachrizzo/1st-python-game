import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # gravity
        self.gravity = 0.5
        self.y_vel = 0
        self.x_vel = 0
        self.health = 100
        self.attack = 10

    def extract_frames(self, sprite_sheet, frame_width, frame_height, num_frames):
        frames = []
        for i in range(num_frames):
            frame = pygame.Surface(
                (frame_width, frame_height), pygame.SRCALPHA, 32)
            frame.blit(sprite_sheet, (0, 0),
                       (i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames

    def handle_collision_with_ground(self, ground_sprites):
        if pygame.sprite.spritecollide(self, ground_sprites, False):
            self.rect.y = ground_sprites.sprite.rect.y - self.rect.height
            self.y_vel = 0
