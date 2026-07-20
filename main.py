import pygame
import sys
import random
import math
import os

# Initialize
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin flip")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (25, 25, 25)
GOLD = (255, 215, 0)

# Images
heads = pygame.image.load("heads.png").convert_alpha()
tails = pygame.image.load("tails.png").convert_alpha()

heads = pygame.transform.smoothscale(heads, (220, 220))
tails = pygame.transform.smoothscale(tails, (220, 220))

current_image = heads

# Sounds if available
flip_sound = None
land_sound = None

if os.path.exists("flip.wav"):
    flip_sound = pygame.mixer.Sound("flip.wav")

if os.path.exists("land.wav"):
    land_sound = pygame.mixer.Sound("land.wav")

# Font
font = pygame.font.SysFont("Arial", 36)
small_font = pygame.font.SysFont("Arial", 24)

# Flip function
def start_flip():
    global flipping, flip_start, result_text

    flipping = True
    flip_start = pygame.time.get_ticks()
    result_text = "Flipping coin..."

    if flip_sound:
        flip_sound.play()

# Reset function
def reset_game():
    global flipping, result_text, current_image

    flipping = False
    result_text = ""
    current_image = heads

# Toggle sound
def toggle_sound():
    global sound_on

    sound_on = not sound_on

    if sound_on:
        pygame.mixer.sound.unpause()
    else:
        pygame.mixer.sound.pause()


# Particle Effect
particles = []


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(-4, 4)
        self.dy = random.uniform(-6, -2)
        self.life = random.randint(40, 70)
        self.radius = random.randint(2, 5)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.15
        self.life -= 1

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            GOLD,
            (int(self.x), int(self.y)),
            self.radius
        )


# Coin Animation Variables
flipping = False
flip_start = 0
flip_duration = 800

result_text = ""

running = True

# Main Loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_SPACE and not flipping:
                start_flip()

            if event.key == pygame.K_r:
                reset_game()

            if event.key == pygame.K_m:
                toggle_sound()

    screen.fill(BLACK)

    # Coin Flip Animation
    if flipping:

        elapsed = pygame.time.get_ticks() - flip_start

        if elapsed < flip_duration:

            # Alternate image every few frames
            if (elapsed // 80) % 2 == 0:
                current_image = heads
            else:
                current_image = tails

            # Fake 3D spin using width scaling
            angle = elapsed * 0.03
            scale = abs(math.cos(angle))

            width = max(10, int(220 * scale))

            coin = pygame.transform.smoothscale(
                current_image,
                (width, 220)
            )

        else:
            flipping = False

            current_image = random.choice([heads, tails])

            result_text = (
                "HEADS!"
                if current_image == heads
                else "TAILS!"
            )

            if land_sound:
                land_sound.play()

            for i in range(80):
                particles.append(
                    Particle(WIDTH // 2, HEIGHT // 2)
                )

            coin = current_image

    else:

        coin = current_image

    # Draw Coin
    rect = coin.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(coin, rect)

    # Draw Particles
    for particle in particles[:]:
        particle.update()
        particle.draw(screen)

        if particle.life <= 0:
            particles.remove(particle)

    # Draw Text
    text = font.render(result_text, True, GOLD)

    screen.blit(
        text,
        (
            WIDTH // 2 - text.get_width() // 2,
            60
        )
    )

    info = font.render("Press SPACE to flip", True, WHITE)

    screen.blit(
        info,
        (
            WIDTH // 2 - info.get_width() // 2,
            520
        )
    )

    esc_text = small_font.render("Press ESC to exit", True, WHITE)
    screen.blit(esc_text, (10, 10))

    reset_text = small_font.render("R = Reset", True, WHITE)
    screen.blit(reset_text, (10, 40))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()