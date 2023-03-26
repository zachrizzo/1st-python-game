
import pygame
from player import Player
from character import Character


class Enemy(Character):
    def __init__(self, player):
        super().__init__()
        self.player = player

        # Load the sprite sheet and extract idle frames
        idle_sprite_sheet = pygame.image.load(
            './craftpix-net-794961-free-warrior-pixel-art-sprite-sheets/Warrior_2/Idle.png').convert_alpha()
        attack_sprite_sheet = pygame.image.load(
            './craftpix-net-794961-free-warrior-pixel-art-sprite-sheets/Warrior_2/Attack_1.png').convert_alpha()
        run_sprite_sheet = pygame.image.load(
            './craftpix-net-794961-free-warrior-pixel-art-sprite-sheets/Warrior_2/Run.png').convert_alpha()
        jump_sprite_sheet = pygame.image.load(
            './craftpix-net-794961-free-warrior-pixel-art-sprite-sheets/Warrior_2/Jump.png').convert_alpha()

        self.idle_frames = self.extract_frames(
            idle_sprite_sheet, frame_width=96, frame_height=96, num_frames=5)
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

        self.attack_cooldown = 1000  # Cooldown time in milliseconds
        self.last_attack_time = 0

    def attack_player(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            player.receive_damage(self)
            self.last_attack_time = current_time

    def receive_damage(self, player):
        self.health -= player.attack

    def update(self):
        # Animate enemy idle state
        now = pygame.time.get_ticks()
        if now - self.last_frame_update > self.frame_update_time:
            self.frame_idx = (self.frame_idx + 1) % len(self.idle_frames)
            self.image = self.idle_frames[self.frame_idx]
            self.last_frame_update = now

        # Move enemy towards player
        player_x = self.player.rect.x
        if player_x < self.rect.x:
            self.rect.x -= 1
            self.frame_idx = (self.frame_idx + 1) % len(self.run_frames)
            flipped_frame = pygame.transform.flip(
                self.run_frames[self.frame_idx], True, False)
            self.image = flipped_frame
        else:
            self.rect.x += 1
            self.frame_idx = (self.frame_idx + 1) % len(self.run_frames)
            self.image = self.run_frames[self.frame_idx]

        # Attack the player if close enough
        if abs(player_x - self.rect.x) < 50:
            self.frame_idx = (self.frame_idx + 1) % len(self.attack_frames)
            self.image = self.attack_frames[self.frame_idx]
            self.last_frame_update = now
            self.attack_player(self.player)

        # Gravity
        self.y_vel += self.gravity
        self.rect.y += self.y_vel

        # if health is 0, remove enemy
        if self.health <= 0:
            self.kill()
