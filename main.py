import pygame
from character import Character
from player import Player
from enemy import Enemy
from ground import Ground


class Game:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600

    def __init__(self):
        pygame.init()
        self.game_display = pygame.display.set_mode(
            (Game.DISPLAY_WIDTH, Game.DISPLAY_HEIGHT))
        pygame.display.set_caption('My Game')
        self.clock = pygame.time.Clock()

        self.enemy_spawn_time = 3000
        self.last_enemy_spawn_time = pygame.time.get_ticks()

        self.ground = Ground()
        self.player = Player()
        self.enemy = Enemy(self.player)
        self.character = Character()

        self.ground_sprites = pygame.sprite.GroupSingle(self.ground)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        # Add the ground to the all_sprites group
        self.all_sprites.add(self.ground)
        # self.all_sprites.add(self.enemy)
        self.game_over = False
        self.enemy_spawned = False

        self.camera_offset_x = 0

        # None uses the default font, 36 is the font size
        self.font = pygame.font.Font(None, 36)

    def render_player_health(self):
        health_text = f"Health: {self.player.health}"
        health_surface = self.font.render(health_text, True, (0, 0, 0))
        return health_surface

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True

            current_time = pygame.time.get_ticks()
            if not self.enemy_spawned and current_time - self.last_enemy_spawn_time >= self.enemy_spawn_time:
                self.enemy = Enemy(self.player)
                self.all_sprites.add(self.enemy)
                self.enemy_spawned = True

            if self.player.is_attacking() and self.player.is_collided_with(self.enemy):
                self.player.attack_enemy(self.enemy)

            if self.enemy.is_collided_with(self.player):
                self.enemy.attack_player(self.player)

            # Check for collisions between player and ground
            self.player.handle_collision_with_ground(self.ground_sprites)
            self.enemy.handle_collision_with_ground(self.ground_sprites)

            # Update the camera offset based on the player's position
            self.camera_offset_x = self.player.rect.x - Game.DISPLAY_WIDTH // 2

            self.all_sprites.update()

            # Draw game objects
            self.game_display.fill(Game.WHITE)
            for sprite in self.all_sprites:
                self.game_display.blit(
                    sprite.image, (sprite.rect.x - self.camera_offset_x, sprite.rect.y))

            # Draw the health text after game objects
            health_surface = self.render_player_health()
            self.game_display.blit(health_surface, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
