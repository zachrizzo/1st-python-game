
import pygame
from character import Character


class Player(Character):
    def __init__(self):
        super().__init__()

        # Load the sprite sheet and extract idle frames
        idle_sprite_sheet = pygame.image.load(
            './craftpix-net-794961-free-warrior-pixel-art-sprite-sheets/Warrior_1/Idle.png').convert_alpha()
        attack_sprite_sheet = pygame.image.load(
            './craftpix-net-794961-free-warrior-pixel-art-sprite-sheets/Warrior_1/Attack_1.png').convert_alpha()
        run_sprite_sheet = pygame.image.load(
            './craftpix-net-794961-free-warrior-pixel-art-sprite-sheets/Warrior_1/Run.png').convert_alpha()
        jump_sprite_sheet = pygame.image.load(
            './craftpix-net-794961-free-warrior-pixel-art-sprite-sheets/Warrior_1/Jump.png').convert_alpha()

        self.idle_frames = self.extract_frames(
            idle_sprite_sheet, frame_width=96, frame_height=96, num_frames=6)
        self.attack_frames = self.extract_frames(
            attack_sprite_sheet, frame_width=96, frame_height=96, num_frames=6)
        self.run_frames = self.extract_frames(
            run_sprite_sheet, frame_width=96, frame_height=96, num_frames=6)
        self.jump_frames = self.extract_frames(
            jump_sprite_sheet, frame_width=96, frame_height=96, num_frames=6)

        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.frame_idx = 0
        self.frame_update_time = 100
        self.last_frame_update = pygame.time.get_ticks()

    def attack_enemy(self, enemy):
        enemy.health -= self.attack

    def receive_damage(self, enemy):
        self.health -= enemy.attack

    def is_attacking(self):
        mouse = pygame.mouse.get_pressed()
        return mouse[0] != 0

    def is_collided_with(self, other):
        return pygame.sprite.collide_rect(self, other)

    def update(self):
        # Animate player idle state
        now = pygame.time.get_ticks()
        if now - self.last_frame_update > self.frame_update_time:
            self.frame_idx = (self.frame_idx + 1) % len(self.idle_frames)
            self.image = self.idle_frames[self.frame_idx]
            self.last_frame_update = now

        # Move player based on arrow key input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            # Flip the image on the x-axis to face left
            self.frame_idx = (self.frame_idx + 1) % len(self.run_frames)
            flipped_frame = pygame.transform.flip(
                self.run_frames[self.frame_idx], True, False)
            self.image = flipped_frame

            self.rect.x -= 5
        if keys[pygame.K_d]:

            self.frame_idx = (self.frame_idx + 1) % len(self.run_frames)
            self.image = self.run_frames[self.frame_idx]
            self.rect.x += 5
        if keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_s]:
            self.rect.y += 5
        # jump
        if keys[pygame.K_SPACE]:
            self.y_vel = -10
            self.frame_idx = (self.frame_idx + 1) % len(self.jump_frames)
            self.image = self.jump_frames[self.frame_idx]

        # Gravity
        self.y_vel += self.gravity
        self.rect.y += self.y_vel

        mouse = pygame.mouse.get_pressed()
        # on mouse click release attack
        if mouse[0] != 0:

            self.frame_idx = (self.frame_idx + 1) % len(self.attack_frames)
            self.image = self.attack_frames[self.frame_idx]
            self.last_frame_update = now
