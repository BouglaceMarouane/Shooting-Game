import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600  # Screen dimensions
FPS = 60  # Frames per second
WHITE = (255, 255, 255)  # Background color
RED = (255, 0, 0)  # Color for debugging or other purposes

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")

# Load images
player_img = pygame.image.load("img.png")  # Player sprite
enemy_img = pygame.image.load("enemy.png")  # Enemy sprite
bullet_img = pygame.image.load("bullet.png")  # Bullet sprite

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img  # Set the player's image
        self.rect = self.image.get_rect()  # Get the rectangle for positioning
        self.rect.centerx = WIDTH // 2  # Start at the center of the screen
        self.rect.bottom = HEIGHT - 10  # Position near the bottom of the screen
        self.speedx = 5  # Horizontal movement speed

    def update(self):
        # Handle player movement based on key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:  # Move left
            self.rect.x -= self.speedx
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:  # Move right
            self.rect.x += self.speedx

# Define the Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img  # Set the enemy's image
        self.rect = self.image.get_rect()  # Get the rectangle for positioning
        self.rect.x = random.randrange(WIDTH - self.rect.width)  # Random horizontal position
        self.rect.y = random.randrange(-100, -40)  # Start off-screen vertically
        self.speedy = random.randrange(1, 5)  # Random vertical speed

    def update(self):
        # Move the enemy down the screen
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:  # If the enemy moves off-screen
            self.rect.x = random.randrange(WIDTH - self.rect.width)  # Reset position
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)

# Define the Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img  # Set the bullet's image
        self.rect = self.image.get_rect()  # Get the rectangle for positioning
        self.rect.centerx = x  # Start at the player's position
        self.rect.bottom = y
        self.speedy = -10  # Move upwards

    def update(self):
        # Move the bullet upwards
        self.rect.y += self.speedy
        if self.rect.bottom < 0:  # Remove the bullet if it goes off-screen
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()  # Group for all sprites
enemies = pygame.sprite.Group()  # Group for enemy sprites
bullets = pygame.sprite.Group()  # Group for bullet sprites

# Create the player
player = Player()
all_sprites.add(player)

# Create enemies
for _ in range(8):  # Add 8 enemies to the game
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game loop
clock = pygame.time.Clock()  # Clock to control the frame rate
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Shoot a bullet
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Update all sprites
    all_sprites.update()

    # Check for collisions between bullets and enemies
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)  # Remove both on collision
    for hit in hits:
        enemy = Enemy()  # Spawn a new enemy
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check for collisions between the player and enemies
    if pygame.sprite.spritecollide(player, enemies, False):  # End the game on collision
        running = False

    # Draw everything
    screen.fill(WHITE)  # Clear the screen
    all_sprites.draw(screen)  # Draw all sprites

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()
