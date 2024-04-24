### Main script for Assaut game
### 
### Tijn de Jong, Daan Peeters and Mitchell Kamppert

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")

BLACK = (0, 0, 0)

# Player class
class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 50
        self.height = 50
        self.speed = 5

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

# Main function
def main():
    # Create players
    player1 = Player(100, HEIGHT // 2, (255, 0, 0))
    player2 = Player(WIDTH - 100, HEIGHT // 2, (0, 0, 255))

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player 1 controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1.y -= player1.speed
        if keys[pygame.K_s]:
            player1.y += player1.speed
        if keys[pygame.K_a]:
            player1.x -= player1.speed
        if keys[pygame.K_d]:
            player1.x += player1.speed
        
        # Player 2 controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player2.y -= player2.speed
        if keys[pygame.K_DOWN]:
            player2.y += player2.speed
        if keys[pygame.K_LEFT]:
            player2.x -= player2.speed
        if keys[pygame.K_RIGHT]:
            player2.x += player2.speed

        # Draw everything
        win.fill(BLACK)
        player1.draw()
        player2.draw()
        pygame.display.flip()

        # Limit frame rate
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()
