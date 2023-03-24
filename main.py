import pygame
from player import Player
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

        self.ground = Ground()
        self.player = Player()

        self.ground_sprites = pygame.sprite.GroupSingle(self.ground)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.game_over = False

        self.camera_offset_x = 0

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True

            self.all_sprites.update()

            # Check for collisions between player and ground
            if pygame.sprite.spritecollide(self.player, self.ground_sprites, False):
                self.player.rect.y = self.ground.rect.y - self.player.rect.height
                self.player.y_vel = 0

            # Update the camera offset based on the player's position
            self.camera_offset_x = self.player.rect.x - Game.DISPLAY_WIDTH // 2

            # Draw game objects
            self.game_display.fill(Game.WHITE)
            for sprite in self.all_sprites:
                self.game_display.blit(
                    sprite.image, (sprite.rect.x - self.camera_offset_x, sprite.rect.y))
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
