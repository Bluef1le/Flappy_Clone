import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600

# Colors
CYAN = (173, 216, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Game settings
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
PIPE_GAP = 200
PIPE_MIN_HEIGHT = 50
PIPE_SPACING = 200
FPS = 60

# Load assets
BIRD_IMAGE = pygame.image.load("bird.png")
BIRD_IMAGE = pygame.transform.scale(BIRD_IMAGE, (40, 30))  # Resize bird image
PIPE_IMAGE = pygame.image.load("pipe.png")  # Load pipe image
PIPE_IMAGE = pygame.transform.scale(PIPE_IMAGE, (PIPE_WIDTH, PIPE_HEIGHT))
BACKGROUND1_IMAGE = pygame.image.load("background1.png")
BACKGROUND1_IMAGE = pygame.transform.scale(BACKGROUND1_IMAGE, (WIDTH, HEIGHT))
BACKGROUND2_IMAGE = pygame.image.load("background2.png")
BACKGROUND2_IMAGE = pygame.transform.scale(BACKGROUND2_IMAGE, (WIDTH, 100))

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock
clock = pygame.time.Clock()

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        self.image = BIRD_IMAGE
        self.angle = 0  # Angle of rotation

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

        # Adjust the angle based on velocity
        if self.velocity < 0:
            self.angle = max(self.angle - 5, -30)  # Tilt up, limit to -30 degrees
        else:
            self.angle = min(self.angle + 4, 56)  # Tilt down, limit to 56 degrees (reduced)

    def draw(self):
        # Rotate the bird image based on the angle
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        new_rect = rotated_image.get_rect(center=(self.x, int(self.y)))
        screen.blit(rotated_image, new_rect.topleft)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(PIPE_MIN_HEIGHT, HEIGHT - PIPE_GAP - PIPE_MIN_HEIGHT)

    def update(self):
        self.x -= 5

    def draw(self):
        # Draw top pipe
        top_pipe = pygame.transform.flip(PIPE_IMAGE, False, True)
        screen.blit(top_pipe, (self.x, self.height - PIPE_HEIGHT))
        # Draw bottom pipe
        screen.blit(PIPE_IMAGE, (self.x, self.height + PIPE_GAP))

    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0

# Background class
class Background:
    def __init__(self):
        self.x1 = 0
        self.x2 = 0
        self.speed = 2

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed * 2  # Foreground moves faster

        if self.x1 <= -WIDTH:
            self.x1 = 0

        if self.x2 <= -WIDTH:
            self.x2 = 0

    def draw(self):
        # Draw the two layers of background
        screen.blit(BACKGROUND1_IMAGE, (self.x1, 0))
        screen.blit(BACKGROUND1_IMAGE, (self.x1 + WIDTH, 0))
        screen.blit(BACKGROUND2_IMAGE, (self.x2, HEIGHT - 100))
        screen.blit(BACKGROUND2_IMAGE, (self.x2 + WIDTH, HEIGHT - 100))

# Main game loop
def main():
    best_score = 0

    while True:
        bird = Bird()
        pipes = [Pipe(WIDTH + i * PIPE_SPACING) for i in range(3)]
        background = Background()
        score = 0
        game_over = False

        while not game_over:
            background.update()
            background.draw()

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
                if pipe.is_off_screen():
                    pipes.remove(pipe)
                    pipes.append(Pipe(WIDTH + PIPE_SPACING))
                    score += 1

                # Collision detection
                if (bird.x + BIRD_IMAGE.get_width() // 2 > pipe.x and bird.x - BIRD_IMAGE.get_width() // 2 < pipe.x + PIPE_WIDTH and
                    (bird.y - BIRD_IMAGE.get_height() // 2 < pipe.height or bird.y + BIRD_IMAGE.get_height() // 2 > pipe.height + PIPE_GAP)):
                    game_over = True

            # Check if bird hits the ground or flies off-screen
            if bird.y - BIRD_IMAGE.get_height() // 2 < 0 or bird.y + BIRD_IMAGE.get_height() // 2 > HEIGHT:
                game_over = True

            if game_over:
                best_score = max(best_score, score)
                font = pygame.font.Font(None, 48)
                game_over_text = font.render("Game Over!", True, BLACK)
                score_text = font.render(f"Score: {score}", True, BLACK)
                best_score_text = font.render(f"Best Score: {best_score}", True, BLACK)
                restart_text = font.render("Press R to Restart", True, BLACK)

                screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 60))
                screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
                screen.blit(best_score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))
                screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 60))
                pygame.display.flip()

                waiting_for_restart = True
                while waiting_for_restart:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            waiting_for_restart = False

            # Draw bird and pipes
            bird.draw()
            for pipe in pipes:
                pipe.draw()

            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()
