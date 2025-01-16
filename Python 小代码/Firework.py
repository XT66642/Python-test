import pygame
import random
import math

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fireworks Show")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 105, 180)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BUTTON_COLOR = GREEN
BUTTON_PRESSED_COLOR = (128, 128, 128)  # Gray color for pressed button

# Button settings
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_X = WIDTH // 2 - BUTTON_WIDTH // 2
BUTTON_Y = HEIGHT - BUTTON_HEIGHT - 20
BUTTON_TEXT = "Fire Firework"
FONT = pygame.font.SysFont(None, 36)

# Firework class
class Firework:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.target_y = random.randint(100, 300)
        self.color = random.choice([RED, BLUE, GREEN, PURPLE, ORANGE, YELLOW])
        self.radius = 5
        self.exploded = False
        self.particles = []
        self.trail_particles = []  # List to store trail particles
        self.velocity = 5  # Initial velocity of the firework
        self.trail_length = 20  # Length of the trail

    def update(self):
        if not self.exploded:
            self.y -= self.velocity
            if self.y <= self.target_y:
                self.explode()
            # Add trail particles at the current position of the firework
            self.trail_particles.append((self.x, self.y, self.color, self.radius, 255))  # (x, y, color, radius, alpha)
            if len(self.trail_particles) > self.trail_length:
                self.trail_particles.pop(0)  # Remove the oldest particle to maintain trail length
        else:
            new_particles = []
            for px, py, vx, vy, p_radius, p_color in self.particles:
                px += vx
                py += vy
                vy += 0.1  # Gravity effect
                p_radius -= 0.05
                if p_radius > 0:
                    new_particles.append((px, py, vx, vy, p_radius, p_color))
            self.particles = new_particles

        # Update trail particles
        for i, (px, py, p_color, p_radius, p_alpha) in enumerate(self.trail_particles):
            p_alpha -= 10  # Decrease alpha to make the trail fade
            p_radius -= 0.05  # Decrease radius to make the trail fade
            self.trail_particles[i] = (px, py, p_color, p_radius, p_alpha)

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        else:
            for px, py, _, _, p_radius, p_color in self.particles:
                pygame.draw.circle(surface, p_color, (int(px), int(py)), int(p_radius))

        # Draw trail particles with alpha
        for px, py, p_color, p_radius, p_alpha in self.trail_particles:
            if p_alpha > 0 and p_radius > 0:
                # Create a surface for the trail particle with alpha
                particle_surface = pygame.Surface((p_radius * 2, p_radius * 2), pygame.SRCALPHA)
                particle_surface.fill((0, 0, 0, 0))
                pygame.draw.circle(particle_surface, (*p_color, p_alpha), (p_radius, p_radius), p_radius)
                surface.blit(particle_surface, (int(px - p_radius), int(py - p_radius)))

    def explode(self):
        self.exploded = True
        num_particles = 50
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            px = self.x
            py = self.y
            p_radius = random.uniform(3, 5)
            p_color = random.choice([RED, BLUE, GREEN, PURPLE, ORANGE, YELLOW])
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.particles.append((px, py, vx, vy, p_radius, p_color))

# Main loop
def main():
    clock = pygame.time.Clock()
    running = True
    fireworks = []
    fade_alpha = 5  # For fading effect
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill(BLACK)
    button_pressed = False  # Track button press state

    while running:
        screen.fill(BLACK)
        for firework in fireworks:
            firework.update()
            firework.draw(screen)

        # Draw button
        button_color = BUTTON_PRESSED_COLOR if button_pressed else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
        text_surface = FONT.render(BUTTON_TEXT, True, WHITE)
        text_rect = text_surface.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
        screen.blit(text_surface, text_rect)

        # Add fading effect
        overlay.set_alpha(fade_alpha)
        screen.blit(overlay, (0, 0))

        pygame.display.flip()
        clock.tick(30)

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fireworks.append(Firework())  # Add a new firework when space is pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = event.pos
                    if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT:
                        fireworks.append(Firework())  # Add a new firework when button is clicked
                        button_pressed = True  # Set button press state
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    button_pressed = False  # Reset button press state

        # Remove finished fireworks
        fireworks = [firework for firework in fireworks if not (firework.exploded and not firework.particles)]

    pygame.quit()

if __name__ == "__main__":
    main()
