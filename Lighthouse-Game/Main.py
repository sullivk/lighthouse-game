import pygame
import player

pygame.init()

# =========================================
# Section 1: Initialization and Constants
# =========================================

# Initialize Pygame clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Lighthouse - Milestone 2")


# Game variables
scroll = 0

# ============================================
# Section 2: Load Background Images and Ground
# ============================================

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

# Load ground image
ground_image = pygame.image.load("BG1/ground.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

# ============================================
# Section 3: Create New Levels
# ============================================

# Create a new level (BG2)
#bg2_image = pygame.image.load("BG2/IMG_1.png").convert_alpha()
#bg2_width = bg2_image.get_width()
#right_scroll_limit_bg2 = bg2_width - SCREEN_WIDTH

# Function to load a new level
def load_level(level_folder):
    level_image = pygame.image.load(level_folder).convert_alpha()
    level_width = level_image.get_width()
    return level_image, level_width

# Load BG2 level
bg2_image, right_scroll_limit_bg2 = load_level("BG2/IMG_1.png")

# ========================================
# Section 4: Draw Functions and Player
# ========================================

# draw background images
def draw_bg(current_level):
    global scroll
    speed = 1
    for x in range(2):
        if x < len(current_level): 
            screen.blit(current_level[x], (int(0 - scroll * speed * 0.25), 0))
        speed += 0.2
    for y in range(2, 4):
        if y < len(current_level):  # Check if the index is within the list
            screen.blit(current_level[y], (int(0 - scroll * speed * 0.5), SCREEN_HEIGHT * 0.5))

# draw ground
def draw_ground():
    for x in range(5):
        screen.blit(ground_image, (0, SCREEN_HEIGHT - ground_height))

# Create the player character
player = player.Character((20, SCREEN_HEIGHT - ground_height - 250))

# ========================================
# Section 5: Main Game Loop and Logic
# ========================================

# Initialize the current level to BG1
current_level = bg_images

# Flag to track if the player is at the lighthouse entrance door
at_lighthouse_entrance_door = False

# Function to switch between levels
def switch_level(new_level, new_scroll):
    global current_level, scroll, at_lighthouse_entrance_door
    current_level = [new_level]
    scroll = new_scroll
    at_lighthouse_entrance_door = False

# Game loop
run = True
while run:
    clock.tick(FPS)
    
    # =================================
    # Section 6: Draw Background and Ground
    # =================================

    draw_bg(current_level) # Changed: draw_bg() -> draw_bg(current_level)
    draw_ground()

    # Debug test
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
                if event.key == pygame.K_y:
                    # Switch to the new level (BG2)
                    switch_level(bg2_image, 0)
                    
                    # Transition to the new level (BG2)
                    #current_level = [bg2_image]
                    # Place the player next to the door
                    #player.rect.x = 20
                    #player.rect.y = SCREEN_HEIGHT - ground_height - 250
                    #@at_lighthouse_entrance_door = False
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

    # =================================
    # Section 7: Display Prompt and Player
    # =================================
    # Display the prompt if the player is at the door
    if at_lighthouse_entrance_door:
        # Draw a white background for the prompt
        prompt_bg = pygame.Surface((400, 100))
        prompt_bg.fill((255, 255, 255))
        screen.blit(prompt_bg, (200, 250))

        prompt_font = pygame.font.Font(None, 36)
        prompt_text = prompt_font.render(
                "Do you want to enter the lighthouse? (Y/N)", True, (0, 0, 0)
            )
        prompt_rect = prompt_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)
        )
        screen.blit(prompt_text, prompt_rect)

    # Draw the player character
    screen.blit(player.image, player.rect)
    pygame.display.update()

# ========================
# Section 8: Cleanup and Quit
# ========================
pygame.quit()
