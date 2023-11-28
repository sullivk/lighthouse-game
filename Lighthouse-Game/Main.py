import pygame
import player
import os
import bird

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
is_level_1 = True
is_level_2 = False
right_scroll_limit = 0
left_scroll_limit = -2
# Flag to track whether the prompt should be displayed
display_prompt = False

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Lighthouse - Milestone 3")

# ============================================
#                     HUD
# ============================================
#                  Health Bar
# Character health
max_health = 5
current_health = max_health

# Load heart image
heart_image = pygame.image.load('HUD/heart.png')
empty_heart_image = pygame.image.load('HUD/empty_heart.png') #Added
heart_image = pygame.transform.scale(heart_image, (30, 30))
empty_heart_image = pygame.transform.scale(empty_heart_image, (30, 30)) #Added
# ============================================

# ============================================
# Section 2: Load Background Images and Ground
# ============================================

# Loads background images
bg_images = []

for i in range(3):
    bg_image = pygame.image.load(f"BG1/background/IMG_{i}.png").convert_alpha()
    bg_images.append(bg_image)

bg_width = bg_images[0].get_width()

# Calculates the minimum width of background images
min_bg_width = min(bg.get_width() for bg in bg_images)

# Initializes the right scrolling limit
bg1_right_scroll_limit = min_bg_width - SCREEN_WIDTH
bg1_left_scroll_limit = 0

# Loads ground image
bg1_ground_image = pygame.image.load("BG1/ground/ground.png").convert_alpha()
bg1_ground_width = bg1_ground_image.get_width()
bg1_ground_height = bg1_ground_image.get_height()

ground_image = bg1_ground_image
ground_width = bg1_ground_width
ground_height = bg1_ground_height

right_scroll_limit = bg1_right_scroll_limit
# ************************************************************************************#

# Loads bg2 images
bg2_images = []
bg2_image = pygame.image.load(f"BG2/background/IMG_0.png").convert_alpha()
bg2_images.append(bg2_image)

bg2_width = bg2_images[0].get_width()

# Calculates the minimum width of background images
min_bg2_width = min(bg2.get_width() for bg2 in bg2_images)

# Initializes the right scrolling limit
bg2_right_scroll_limit = min_bg2_width - SCREEN_WIDTH

# Loads ground image
bg2_ground_image = pygame.image.load("BG2/ground/ground.png").convert_alpha()
bg2_ground_width = bg2_ground_image.get_width()
bg2_ground_height = bg2_ground_image.get_height()

# ============================================
# Section 3: Create New Levels
# ============================================


# Function to load a new level
def load_level(level_folder):
    ground_image = pygame.image.load(f"{level_folder}/ground/ground.png").convert_alpha()
    level_image = pygame.image.load(f"{level_folder}/background/IMG_0.png").convert_alpha()
    level_width = level_image.get_width()
    return level_image, level_width, ground_image


# Loads BG2 level
bg2_image, bg2_right_scroll_limit, bg2_ground_image = load_level("BG2")
# Set the ground image to the new level's ground image


# ========================================
# Section 4: Draw Functions and Player
# ========================================


# Draws the background images
def draw_bg(current_level):
    global scroll
    speed = 1
    for x in range(2):
        if x < len(current_level):
            screen.blit(current_level[x], (int(0 - scroll * speed * 0.25), 0))
        speed += 0.2
    for y in range(2, 3):
        if y < len(current_level):  # Check if the index is within the list
            screen.blit(current_level[y], (int(0 - scroll * speed * 0.5), SCREEN_HEIGHT * 0.5))


# Draws the ground
def draw_ground():
    for x in range(5):
        screen.blit(ground_image, (0, SCREEN_HEIGHT - ground_height))

# Creates entities
player_start = (20, SCREEN_HEIGHT - ground_height + 300)
player = player.Character(player_start, ground_width)
bird = bird.Character((500, 10))
PLAYER_SPEED = 6
scroll = 0

# ========================================
# Section 5: Main Game Loop and Logic
# ========================================

# Initializes the current level to BG1
current_level = bg_images

# Flag to track if the player is at the lighthouse entrance door
at_lighthouse_entrance_door = False

# Resets the player's position
def reset_player_position():
    # Set the player's x position to be inside the lighthouse
    player.rect.x = 20
    # Set the player's y position to the ground inside the lighthouse
    player.rect.y = SCREEN_HEIGHT - ground_height - player.rect.height + 10


# Function to switch between levels
def switch_level(new_level, new_scroll):
    global current_level, scroll, at_lighthouse_entrance_door, ground_image, ground_height, ground_width, is_level_1, is_level_2, left_scroll_limit, right_scroll_limit
    current_level = [new_level]

    if new_level == bg2_image:
        left_scroll_limit = -2
        right_scroll_limit = bg2_right_scroll_limit
        is_level_1 = False
        is_level_2 = True
        print("Switching to level 2")
        ground_image = bg2_ground_image
        ground_height = bg2_ground_height
        ground_width = bg2_ground_width
        at_lighthouse_entrance_door = False
        scroll = new_scroll
        reset_player_position()  # Reset player's position inside the lighthouse
    else:
        scroll = new_scroll
        left_scroll_limit = 0
        right_scroll_limit = bg1_right_scroll_limit
        is_level_1 = True
        is_level_2 = False
        current_level = bg_images
        at_lighthouse_entrance_door = False
        reset_player_position()


# Initializes the arrow position to "Yes" by default
arrow_position = "Yes"

# Function to display the custom Pokemon-style prompt
def display_pokemon_style_prompt(arrow_position):
    if display_prompt == True:
        # Create a custom dialogue box background
        prompt_bg = pygame.Surface((400, 150))
        prompt_bg.fill((255, 255, 255))  # Background color (white)

        # Draw a border for the dialogue box
        pygame.draw.rect(
            prompt_bg, (0, 0, 0), pygame.Rect(0, 0, 400, 150), 3
        )  # Border color (black), thickness 3

        # Create a custom font for the text
        prompt_font = pygame.font.Font(
            None, 24
        )  # You can adjust the font size as needed

        # Render and display the text on the dialogue box
        if is_level_1 and right_scroll_limit:
            prompt_text = prompt_font.render(
                "Do you want to enter the lighthouse? (Y/N)", True, (0, 0, 0)
            )  # Text color (black)
        if is_level_2 and left_scroll_limit:
            prompt_text = prompt_font.render(
                "Do you want to exit the lighthouse? (Y/N)", True, (0, 0, 0)
            )  # Text color (black)

        # Positions the text in the center of the dialogue box
        text_rect = prompt_text.get_rect(center=(200, 50))

        # Displays the dialogue box with the text
        prompt_bg.blit(prompt_text, text_rect)

        # Creates a custom font for the selected option
        selected_option_font = pygame.font.Font(None, 36)

        # Defines Unicode arrow characters
        arrow_yes = "\u25B6"  # Right arrow
        arrow_no = "\u25B2"  # Up arrow

        # Defines text for "Yes" and "No" options with arrow
        text_yes = f"{arrow_yes} Yes"
        text_no = f"{arrow_no} No"

        # Renders and displays the selected option with the arrow
        if arrow_position == "Yes":
            selected_text = selected_option_font.render(text_yes, True, (0, 0, 0))
        elif arrow_position == "No":
            selected_text = selected_option_font.render(text_no, True, (0, 0, 0))

        selected_rect = selected_text.get_rect(
            center=(200, 110)
        )  # Positions the selected text

        # Renders and display the other option without the arrow
        if arrow_position == "Yes":
            other_text = prompt_font.render("No", True, (0, 0, 0))
        elif arrow_position == "No":
            other_text = prompt_font.render("Yes", True, (0, 0, 0))

        other_rect = other_text.get_rect(center=(200, 140))  # Position the other text

        # Displays the selected and other options
        prompt_bg.blit(selected_text, selected_rect)
        prompt_bg.blit(other_text, other_rect)

        screen.blit(prompt_bg, (200, 450))

# Initializes variables to track key states
left_key_pressed = False
right_key_pressed = False

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Discover the Lighthouse")

# Title Menu
title_background_image = pygame.image.load("Menu/Title.png") 

# Game loop
title_menu = True
run = False

while title_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            title_menu = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Space bar pressed to start the game
                title_menu = False
                run = True

    screen.blit(title_background_image, (0, 0))
    pygame.display.flip()

while run:
    clock.tick(FPS)
    
    # =================================
    # Section 6: Draw Background and Ground
    # =================================
    draw_bg(current_level)  # Changed: draw_bg() -> draw_bg(current_level)
    draw_ground()
    
    # Handles user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if (player.alive):
                if event.key == pygame.K_LEFT:
                    player.go_left(scroll)
                elif event.key == pygame.K_RIGHT:
                    player.go_right(scroll)
                elif event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_SPACE:
                    player.punch = True    
                    if pygame.sprite.collide_rect(bird, player):
                        bird.take_damage()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.stop()   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False                 

    key = pygame.key.get_pressed()

    # Updates the player
    player.update(player_start)
    if player.change_x != 0:
        scroll -= (player.change_x * 5)
    print(f"Player X: {player.rect.x}, Change X: {player.change_x}, Scroll: {scroll}, Change Y: {player.change_y}")

    # Limits the scrolling to the size of the ground image
    scroll = max(min(0, scroll), SCREEN_WIDTH - ground_image.get_width())

    # Draws the background, clouds, and ground at the new position
    screen.blit(bg_images[0], (scroll, 0))
    screen.blit(bg_images[1], (scroll * .25, 0))
    screen.blit(ground_image, (scroll, SCREEN_HEIGHT - ground_height))

    # Checks if the player has been attacked recently
    if player.invulnerable and (pygame.time.get_ticks() - player.last_damage_time > player.invulnerability_duration):
        player.invulnerable = False

    # Checks for collision between bird and player
    if (player.alive and bird.alive):
        if pygame.sprite.collide_rect(bird, player) and not player.invulnerable:
            player.take_damage()
            current_health = player.health

    # Draws the health bar
    for i in range(max_health):
        if i < current_health:
            screen.blit(heart_image, (10 + i * 40, SCREEN_HEIGHT - 40))
        else:
            screen.blit(empty_heart_image, (10 + i * 40, SCREEN_HEIGHT - 40))

    # Updates the bird
    if bird.alive:
        bird.update()
        bird.detect_player_proximity(player)
        if bird.rect.x > 1000:
            bird.change_direction()
        if bird.rect.x < -200:
            bird.change_direction()       
        
    # Draws the player character
    screen.blit(player.image, player.rect)
    if bird.alive:
        screen.blit(bird.image, bird.rect)
    pygame.display.update()

# ========================
# Section 8: Cleanup and Quit
# ========================
pygame.quit()
