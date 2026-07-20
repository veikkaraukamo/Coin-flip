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
pygame.display.set_caption("Coin Flip Simulator")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (25, 25, 25)
GOLD = (255, 215, 0)
BLUE = (25, 115, 180)
PURPLE = (60, 40, 110)

BACKGROUND_OPTIONS = [
    ("Midnight", BLACK),
    ("Snow", WHITE),
    ("Ocean", BLUE),
    ("Royal", PURPLE),
]

COIN_STYLES = [
    ("Classic", "classic"),
    ("Gold", "gold"),
    ("Neon", "neon"),
]

# Images
base_heads = pygame.image.load("heads.png").convert_alpha()
base_tails = pygame.image.load("tails.png").convert_alpha()

base_heads = pygame.transform.smoothscale(base_heads, (220, 220))
base_tails = pygame.transform.smoothscale(base_tails, (220, 220))


def tint_image(image, color):
    tinted = image.copy()
    overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    overlay.fill((color[0], color[1], color[2], 80))
    tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    return tinted


def build_coin_surface(image, style_name):
    if style_name == "gold":
        return tint_image(image, GOLD)
    if style_name == "neon":
        return tint_image(image, (80, 220, 255))
    return image


def refresh_coin_assets():
    global heads, tails, current_image
    heads = build_coin_surface(base_heads, coin_style)
    tails = build_coin_surface(base_tails, coin_style)
    if not flipping:
        current_image = heads


heads = base_heads
tails = base_tails
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
small_font = pygame.font.SysFont("Arial", 28)

# Flip function
def start_flip():
    global flipping, flip_start, result_text

    flipping = True
    flip_start = pygame.time.get_ticks()
    result_text = "Flipping coin..."

    if sound_on and flip_sound:
        flip_sound.play()


# Reset function
def reset_game():
    global flipping, result_text, current_image
    global heads_count, tails_count
    flipping = False
    result_text = "Press SPACE to flip coin!"
    current_image = heads

    heads_count = 0
    tails_count = 0


# Toggle sound
def toggle_sound():
    global sound_on

    sound_on = not sound_on

    if sound_on:
        pygame.mixer.unpause()
    else:
        pygame.mixer.pause()


# Settings helpers
def toggle_settings():
    global settings_open
    settings_open = not settings_open


def adjust_setting(step):
    global bg_index, coin_style_index, coin_style, background_color, sound_on, particles_on

    if selected_option == 0:
        bg_index = (bg_index + step) % len(BACKGROUND_OPTIONS)
        background_color = BACKGROUND_OPTIONS[bg_index][1]
    elif selected_option == 1:
        coin_style_index = (coin_style_index + step) % len(COIN_STYLES)
        coin_style = COIN_STYLES[coin_style_index][1]
        refresh_coin_assets()
    elif selected_option == 2:
        toggle_sound()
    elif selected_option == 3:
        particles_on = not particles_on


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
flip_duration = 1500

result_text = "Press SPACE to flip coin"

running = True
settings_open = False
selected_option = 0
bg_index = 0
coin_style_index = 0
coin_style = COIN_STYLES[coin_style_index][1]
background_color = BACKGROUND_OPTIONS[bg_index][1]
sound_on = True
particles_on = True
heads_count = 0
tails_count = 0
refresh_coin_assets()

# Main Loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if settings_open:
                    settings_open = False
                else:
                    toggle_settings()

            elif settings_open:
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected_option = (selected_option - 1) % 4
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected_option = (selected_option + 1) % 4
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    adjust_setting(-1)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    adjust_setting(1)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    adjust_setting(1)

            elif event.key == pygame.K_SPACE and not flipping:
                start_flip()

            elif event.key == pygame.K_r:
                reset_game()

            elif event.key == pygame.K_m:
                toggle_sound()

    screen.fill(background_color)
    text_color = BLACK if background_color == WHITE else WHITE

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

            if current_image == heads:
                result_text = "HEADS!"
                heads_count += 1
            else:
                result_text = "TAILS!"
                tails_count += 1
            
            if sound_on and land_sound:
                    land_sound.play()

            if particles_on:
                for _ in range(80):
                    particles.append(
                        Particle(WIDTH // 2, HEIGHT // 2)
                    )

            coin = current_image

    # Draw Coin
    rect = coin.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(coin, rect)

    # Draw Particles
    if particles_on:
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)

            if particle.life <= 0:
                particles.remove(particle)

    # Draw Text
    text = font.render(result_text, True, text_color)

    screen.blit(
        text,
        (
            WIDTH // 2 - text.get_width() // 2,
            60
        )
    )

    stats = small_font.render(
    f"Heads: {heads_count}   Tails: {tails_count}",
    True,
    text_color)

    screen.blit(
        stats,
        (
            WIDTH // 2 - stats.get_width() // 2,
            105
        )
    )

    info = font.render("Press SPACE to flip again", True, text_color)

    screen.blit(
        info,
        (
            WIDTH // 2 - info.get_width() // 2,
            520
        )
    )

    bottom_text = font.render("Press ESC for settings", True, text_color)

    screen.blit(
        bottom_text,
        (
            WIDTH // 2 - bottom_text.get_width() // 2,
            580
        )
    )

    if settings_open:
        panel = pygame.Surface((500, 320), pygame.SRCALPHA)
        panel.fill((20, 20, 20, 220))
        pygame.draw.rect(panel, (255, 255, 255, 180), panel.get_rect(), 2)
        screen.blit(panel, (150, 120))

        title = font.render("Settings", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 140))

        items = [
            ("Background", BACKGROUND_OPTIONS[bg_index][0]),
            ("Coin style", COIN_STYLES[coin_style_index][0]),
            ("Sound", "On" if sound_on else "Off"),
            ("Particles", "On" if particles_on else "Off"),
        ]

        for index, (label, value) in enumerate(items):
            prefix = ">" if index == selected_option else " "
            color = GOLD if index == selected_option else WHITE
            option_text = small_font.render(f"{prefix} {label}: {value}", True, color)
            screen.blit(option_text, (220, 200 + index * 38))

        help_text = small_font.render("Arrows change values • ESC closes", True, WHITE)
        screen.blit(help_text, (200, 380))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()