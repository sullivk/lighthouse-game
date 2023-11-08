import pygame
import player
import os

file_path = os.path.abspath("Main.py")
print(file_path)

pygame.init()

# =========================================
# Section 1: Initialization and Constants
# =========================================

# Initialize Pygame clock and FPS
clock = pygame.time.Clock()
FPS = 60
ground_image = ""
ground_width = 0
ground_height = 0

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
    bg_image = pygame.image.load(f"BG1/background/IMG_{i}.png").convert_alpha()
    bg_images.append(bg_image)

bg_width = bg_images[0].get_width()

# Calculate the minimum width of background images
min_bg_width = min(bg.get_width() for bg in bg_images)

# Initialize the right scrolling limit
right_scroll_limit = min_bg_width - SCREEN_WIDTH

# Load ground image
bg1_ground_image = pygame.image.load("BG1/ground/ground.png").convert_alpha()
bg1_ground_width = bg1_ground_image.get_width()
bg1_ground_height = bg1_ground_image.get_height()

ground_image = bg1_ground_image
ground_width = bg1_ground_width
ground_height = bg1_ground_height
#************************************************************************************#

# Load bg2 images
bg2_images = []
bg2_image = pygame.image.load(f"BG2/background/IMG_0.png").convert_alpha()
bg2_images.append(bg2_image)

bg2_width = bg2_images[0].get_width()

# Calculate the minimum width of background images
min_bg2_width = min(bg2.get_width() for bg2 in bg2_images)

# Initialize the right scrolling limit
bg2_right_scroll_limit = min_bg2_width - SCREEN_WIDTH

# Load ground image
bg2_ground_image = pygame.image.load("BG2/ground/ground.png").convert_alpha()
bg2_ground_width = bg2_ground_image.get_width()
bg2_ground_height = bg2_ground_image.get_height()

# ============================================
# Section 3: Create New Levels
# ============================================

# Create a new level (BG2)
#bg2_image = pygame.image.load("BG2/IMG_1.png").convert_alpha()
#bg2_width = bg2_image.get_width()
#right_scroll_limit_bg2 = bg2_width - SCREEN_WIDTH

# Function to load a new level
def load_level(level_folder):
    ground_image = pygame.image.load(f"{level_folder}/ground/ground.png").convert_alpha()
    level_image = pygame.image.load(f"{level_folder}/background/IMG_0.png").convert_alpha()
    level_width = level_image.get_width()
    return level_image, level_width, ground_image

# Load BG2 level
bg2_image, right_scroll_limit_bg2, bg2_ground_image = load_level('BG2')
# Set the ground image to the new level's ground image


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
    global current_level, scroll, at_lighthouse_entrance_door, ground_image, ground_height, ground_width
    current_level = [new_level]
    scroll = new_scroll
    if new_level == bg2_image:
        print("Switching to level 2")
        ground_image = bg2_ground_image
        ground_height = bg2_ground_height
        ground_width = bg2_ground_width
    at_lighthouse_entrance_door = False
    
# Initialize the arrow position to "Yes" by default
arrow_position = "Yes"
    
# Function to display the custom Pokemon-style prompt
def display_pokemon_style_prompt(arrow_position):
    # Create a custom dialogue box background
    prompt_bg = pygame.Surface((400, 150))
    prompt_bg.fill((255, 255, 255))  # Background color (white)

    # Draw a border for the dialogue box
    pygame.draw.rect(prompt_bg, (0, 0, 0), pygame.Rect(0, 0, 400, 150), 3)  # Border color (black), thickness 3

    # Create a custom font for the text
    prompt_font = pygame.font.Font(None, 24)  # You can adjust the font size as needed

    # Render and display the text on the dialogue box
    prompt_text = prompt_font.render("Do you want to enter the lighthouse? (Y/N)", True, (0, 0, 0))  # Text color (black)

    # Position the text in the center of the dialogue box
    text_rect = prompt_text.get_rect(center=(200, 50))

    # Display the dialogue box with the text
    prompt_bg.blit(prompt_text, text_rect)
    
    # Create a custom font for the selected option
    selected_option_font = pygame.font.Font(None, 36)
    
    # Define Unicode arrow characters
    arrow_yes = u"\u25B6"  # Right arrow
    arrow_no = u"\u25B2"   # Up arrow
    
    # Define text for "Yes" and "No" options with arrow
    text_yes = f"{arrow_yes} Yes"
    text_no = f"{arrow_no} No"
    
    # Render and display the selected option with the arrow
    if arrow_position == "Yes":
        selected_text = selected_option_font.render(text_yes, True, (0, 0, 0))
    elif arrow_position == "No":
        selected_text = selected_option_font.render(text_no, True, (0, 0, 0))

    selected_rect = selected_text.get_rect(center=(200, 110))  # Position the selected text

    # Render and display the other option without the arrow
    if arrow_position == "Yes":
        other_text = prompt_font.render("No", True, (0, 0, 0))
    elif arrow_position == "No":
        other_text = prompt_font.render("Yes", True, (0, 0, 0))

    other_rect = other_text.get_rect(center=(200, 140))  # Position the other text

    # Display the selected and other options
    prompt_bg.blit(selected_text, selected_rect)
    prompt_bg.blit(other_text, other_rect)
    
    screen.blit(prompt_bg, (200, 450))

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
        # Display the custom Pokemon-style prompt
        display_pokemon_style_prompt(arrow_position)
        # Draw a white background for the prompt
        #prompt_bg = pygame.Surface((400, 100))
        #prompt_bg.fill((255, 255, 255))
        #screen.blit(prompt_bg, (200, 250))

        #prompt_font = pygame.font.Font(None, 36)
        #prompt_text = prompt_font.render(
        #        "Do you want to enter the lighthouse? (Y/N)", True, (0, 0, 0)
        #    )
        #prompt_rect = prompt_text.get_rect(
        #    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)
        #)
        #screen.blit(prompt_text, prompt_rect)
        
        # Handle user input for arrow navigation
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    arrow_position = "Yes"
                elif event.key == pygame.K_DOWN:
                    arrow_position = "No"

    # Draw the player character
    screen.blit(player.image, player.rect)
    pygame.display.update()

# ========================
# Section 8: Cleanup and Quit
# ========================
pygame.quit()
# ========================
# Section 8: Cleanup and Quit
# ========================
pygame.quit()
