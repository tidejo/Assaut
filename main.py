### Main script for Assaut game
### 
### Tijn de Jong, Daan Peeters and Mitchell Kampert

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
        self.radius = 20
        self.speed = 5

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def update_position(self, dx, dy, other_players):
        # Update position within window boundaries
        new_x = self.x + dx
        new_y = self.y + dy
        if (0+self.radius) <= new_x <= (WIDTH-self.radius) and (0+self.radius) <= new_y <= (HEIGHT-self.radius):
            # Check collision with other players
            for player in other_players:
                if player is not self:
                    distance = ((new_x - player.x) ** 2 + (new_y - player.y) ** 2) ** 0.5
                    if distance > self.radius + player.radius:          
                        self.x = new_x
                        self.y = new_y

# Main function
def main():
    # Create players
    player1 = Player(100, HEIGHT // 2, (255, 0, 0))
    player2 = Player(WIDTH - 100, HEIGHT // 2, (0, 0, 255))
    players = [player1, player2]

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player 1 controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1.update_position(0, -player1.speed, players)
        if keys[pygame.K_s]:
            player1.update_position(0, player1.speed, players)
        if keys[pygame.K_a]:
            player1.update_position(-player1.speed, 0, players)
        if keys[pygame.K_d]:
            player1.update_position(player1.speed, 0, players)
        
        # Player 2 controls
        if keys[pygame.K_UP]:
            player2.update_position(0, -player2.speed, players)
        if keys[pygame.K_DOWN]:
            player2.update_position(0, player2.speed, players)
        if keys[pygame.K_LEFT]:
            player2.update_position(-player2.speed, 0, players)
        if keys[pygame.K_RIGHT]:
            player2.update_position(player2.speed, 0, players)

        # Draw everything
        win.fill(BLACK)
        player1.draw()
        player2.draw()
        pygame.display.flip()

        # Limit frame rate
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()

