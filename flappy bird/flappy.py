import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
GREEN = (34, 139, 34)
YELLOW = (255, 223, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60

# Load assets
bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (40, 40))
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.width = 40
        self.height = 40
        self.velocity = 0
        self.gravity = 0.5

    def draw(self):
        screen.blit(bird_image, (self.x, self.y))

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def flap(self):
        self.velocity = -8

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 50
        self.gap = 150
        self.top_height = random.randint(50, SCREEN_HEIGHT - self.gap - 50)

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, GREEN, (self.x, self.top_height + self.gap, self.width, SCREEN_HEIGHT))

    def update(self):
        self.x -= 3

    def is_off_screen(self):
        return self.x + self.width < 0

# Check for collision
def check_collision(bird, pipes):
    for pipe in pipes:
        if (bird.x + bird.width > pipe.x and bird.x < pipe.x + pipe.width and
            (bird.y < pipe.top_height or bird.y + bird.height > pipe.top_height + pipe.gap)):
            return True
    if bird.y <= 0 or bird.y + bird.height >= SCREEN_HEIGHT:
        return True
    return False

# Home screen function
def home_screen(highscore):
    running = True
    font = pygame.font.SysFont("Arial", 30)
    title_font = pygame.font.SysFont("Arial", 60)
    highscore_font = pygame.font.SysFont("Arial", 40)
    instruction_font = pygame.font.SysFont("Arial", 20)

    while running:
        screen.blit(background_image, (0, 0))

        # Title
        title_text = title_font.render("FLAPPY BIRD", True, YELLOW)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Highscore
        highscore_text = highscore_font.render(f"Highscore: {highscore}", True, WHITE)
        screen.blit(highscore_text, (SCREEN_WIDTH // 2 - highscore_text.get_width() // 2, 200))

        # Start button
        start_text = instruction_font.render("Press SPACE to Start", True, WHITE)
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 300))

        # Instructions
        instruction_text = instruction_font.render("Use SPACE to flap and avoid pipes!", True, WHITE)
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False

        pygame.display.flip()
        clock.tick(FPS)

# Main game function
def main():
    highscore = 0

    while True:
        home_screen(highscore)

        running = True
        bird = Bird()
        pipes = [Pipe(SCREEN_WIDTH)]
        score = 0
        font = pygame.font.SysFont("Arial", 30)

        while running:
            screen.blit(background_image, (0, 0))

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird.flap()

            # Update bird
            bird.update()

            # Update pipes
            for pipe in pipes:
                pipe.update()

            # Remove off-screen pipes and add new pipes
            if pipes[0].is_off_screen():
                pipes.pop(0)
                pipes.append(Pipe(SCREEN_WIDTH))
                score += 1

            # Check for collision
            if check_collision(bird, pipes):
                running = False

            # Draw bird and pipes
            bird.draw()
            for pipe in pipes:
                pipe.draw()

            # Draw score
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            # Update display
            pygame.display.flip()

            # Control frame rate
            clock.tick(FPS)

        highscore = max(highscore, score)

if __name__ == "__main__":
    main()
