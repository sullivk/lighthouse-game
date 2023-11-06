import pygame
import player

pygame.init()

clock = pygame.time.Clock()

FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Lighthouse - Milestone 2")


# define game variables
scroll = 0

# Load background images
bg_images = []

for i in range(4):
    bg_image = pygame.image.load(f"BG1/IMG_{i}.png").convert_alpha()
    bg_images.append(bg_image)

bg_width = bg_images[0].get_width()

# Calculate the minimum width of background images
min_bg_width = min(bg.get_width() for bg in bg_images)

# Initialize the right scrolling limit
right_scroll_limit = min_bg_width - SCREEN_WIDTH

ground_image = pygame.image.load("BG1/ground.png").convert_alpha()

ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

# Create a new level (BG2)
bg2_image = pygame.image.load("BG2/IMG_1.png").convert_alpha()
bg2_width = bg2_image.get_width()
right_scroll_limit_bg2 = bg2_width - SCREEN_WIDTH

# draw background images
def draw_bg():
    global scroll
    speed = 1
    for x in range(2):
        screen.blit(bg_images[x], (int(0 - scroll * speed * 0.25), 0))
        speed += 0.2
    for y in range(2, 4):
        screen.blit(bg_images[y], (int(0 - scroll * speed * 0.5), SCREEN_HEIGHT * 0.5))

# draw background
def draw_ground():
    for x in range(5):
        screen.blit(ground_image, (0, SCREEN_HEIGHT - ground_height))


player = player.Character((20, SCREEN_HEIGHT - ground_height - 250))

# Initialize the current level
current_level = bg_images

# Flag to track if the player is at the door
at_lighthouse_entrance_door = False

# Game loop
run = True
while run:
    clock.tick(FPS)

    draw_bg()
    draw_ground()

    print("CHECK")
    
    # Input data. Left and right keys to create the parallax effect
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll > 0:
        scroll -= 5
    if key[pygame.K_RIGHT] and scroll < right_scroll_limit:
        scroll += 5
        
    # Check if the character is at the right scroll limit
    if scroll == right_scroll_limit:
        at_lighthouse_entrance_door = True
    else:
        at_lighthouse_entrance_door = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if at_lighthouse_entrance_door:
                if event.type == pygame.K_y:
                    # Transition to the new level (BG2)
                    current_level = [bg2_image]
                    # Place the player next to the door
                    player.rect.x = 20
                    player.rect.y = SCREEN_HEIGHT - ground_height - 250
                    at_lighthouse_entrance_door = False
                elif event.key == pygame.K_n:
                    at_lighthouse_entrance_door = False

    if not at_lighthouse_entrance_door:
        key = pygame.key.get_pressed()
        if scroll > 0 and scroll < right_scroll_limit:
            player.handle_event(event)
        else:
            end_screen = pygame.event.Event(pygame.KEYUP)
            if scroll == 0:
                end_screen.key = pygame.K_RIGHT
            else:
                end_screen.key = pygame.K_LEFT
            player.handle_event(end_screen)

    # Display the prompt if the player is at the door
    if at_lighthouse_entrance_door:
        prompt_font = pygame.font.Font(None, 36)
        prompt_text = prompt_font.render(
                "Do you want to enter the lighthouse? (Y/N)", True, (255, 255, 255)
            )
        prompt_rect = prompt_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)
        )
        screen.blit(prompt_text, prompt_rect)

    screen.blit(player.image, player.rect)
    pygame.display.update()

pygame.quit()
