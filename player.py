
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # gravity
        self.gravity = 0.5
        self.y_vel = 0
        self.x_vel = 0

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

    def extract_frames(self, sprite_sheet, frame_width, frame_height, num_frames):
        frames = []
        for i in range(num_frames):
            frame = pygame.Surface(
                (frame_width, frame_height), pygame.SRCALPHA, 32)
            frame.blit(sprite_sheet, (0, 0),
                       (i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames

    def update(self):
        # Animate player idle state
        now = pygame.time.get_ticks()
        if now - self.last_frame_update > self.frame_update_time:
            self.frame_idx = (self.frame_idx + 1) % len(self.idle_frames)
            self.image = self.idle_frames[self.frame_idx]
            self.last_frame_update = now

        # Move player based on arrow key input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            # Flip the image on the x-axis to face left
            self.frame_idx = (self.frame_idx + 1) % len(self.run_frames)
            flipped_frame = pygame.transform.flip(
                self.run_frames[self.frame_idx], True, False)
            self.image = flipped_frame

            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:

            self.frame_idx = (self.frame_idx + 1) % len(self.run_frames)
            self.image = self.run_frames[self.frame_idx]
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
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
