import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Creative Process Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Font
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# States
states = [
    "Wake up",
    "Psychosis?",
    "Dissociate",
    "Tired yet?",
    "Manically create",
    "Pass out"
]

# Random weirdness messages
weirdness_messages = [
    "I see colors",
    "The walls are melting",
    "Is this real life?",
    "I'm a banana",
    "The universe is inside me"
]


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, image_file):
        super().__init__()
        self.original_image = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.sleeping = False
        self.typing = False
        self.weirdness_text = ""
        self.pass_out_pos = self.rect.center

    def update(self, state):
        self.sleeping = False
        self.typing = False
        target_x, target_y = 400, HEIGHT // 2
        if state == 4:  # Manically create
            if self.rect.x < target_x:
                self.rect.x += 5
            elif self.rect.x > target_x:
                self.rect.x -= 5

            if self.rect.y < target_y:
                self.rect.y += 5
            elif self.rect.y > target_y:
                self.rect.y -= 5

            if self.rect.x == target_x and self.rect.y == target_y:
                self.typing = True
        elif state == 2 or state == 1 or state == 3:  # Dissociate or Random Walk
            self.rect.x += random.choice([-5, 5])
            self.rect.y += random.choice([-5, 5])
            self.rect.x = max(0, min(self.rect.x, WIDTH - 50))
            self.rect.y = max(0, min(self.rect.y, HEIGHT - 50))
            if state == 2:
                self.weirdness_text = random.choice(weirdness_messages)
        elif state == 5:  # Pass out
            self.sleeping = True
            self.pass_out_pos = self.rect.center
        else:  # Wake up
            self.rect.center = self.pass_out_pos
            self.weirdness_text = ""


class Computer(pygame.sprite.Sprite):
    def __init__(self, x, y, image_file):
        super().__init__()
        self.original_image = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Simulation:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.character = Character(100, HEIGHT // 2,
                                   'character.jpg')  # Replace 'character.jpg' with your character image file
        self.computer = Computer(400, HEIGHT // 2,
                                 'computer.jpg')  # Replace 'computer.jpg' with your computer image file
        self.all_sprites = pygame.sprite.Group(self.computer, self.character)
        self.current_state = 0
        self.last_update_time = time.time()

    def draw_text(self, text, x, y, font, color=BLACK):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    def update_state(self):
        if self.current_state == 0:  # Wake up
            self.current_state = 1
        elif self.current_state == 1:  # Psychosis?
            self.current_state = 3 if random.choice([True, False]) else 2
        elif self.current_state == 2:  # Dissociate
            self.current_state = 3
        elif self.current_state == 3:  # Tired yet?
            self.current_state = 4 if random.choice([True, False]) else 5
        elif self.current_state == 4:  # Manically create
            self.current_state = 5
        elif self.current_state == 5:  # Pass out
            self.current_state = 0

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            screen.fill(WHITE)

            self.draw_text("Current State:", 50, 50, font)
            self.draw_text(states[self.current_state], 50, 100, font)
            self.all_sprites.update(self.current_state)
            self.all_sprites.draw(screen)

            if self.character.sleeping:
                self.draw_text("Zzz...", self.character.rect.x + 10, self.character.rect.y - 30, small_font, BLUE)
            elif self.character.typing:
                self.draw_text("Typing...", self.computer.rect.x + 60, self.computer.rect.y, small_font, BLUE)
            elif self.character.weirdness_text:
                self.draw_text(self.character.weirdness_text, self.character.rect.x + 60, self.character.rect.y,
                               small_font, BLUE)

            if time.time() - self.last_update_time > 2:  # Update state every 2 seconds
                self.update_state()
                self.last_update_time = time.time()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    sim = Simulation()
    sim.run()
