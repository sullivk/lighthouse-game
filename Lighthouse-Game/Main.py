import pygame
import player
import bird
import pauseMenu
import winScreen
import loseScreen
from bird import Character

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
bird2_has_spawned = False
# Flag to track whether the prompt should be displayed
display_prompt = False

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Creates the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Lighthouse - Milestone 3")

# ============================================
#                     HUD
# ============================================
#                  Health Bar
# Character health
max_health = 5
current_health = max_health

# Loads heart images
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
if is_level_1:
    player_start = (20, SCREEN_HEIGHT - ground_height + 300)
elif is_level_2:
    player_start = (20, SCREEN_HEIGHT)

player = player.Character(player_start, ground_width)
bird = bird.Character((500, 10), bird2_has_spawned)
bird1 = Character((950, 20), bird2_has_spawned)
bird2 = Character((500, -200), bird2_has_spawned)
bird3 = Character((700, -200), bird2_has_spawned)
PLAYER_SPEED = 1
scroll = 0
new_scroll = 0

# ========================================
# Section 5: Main Game Loop and Logic
# ========================================

# Initializes the current level to BG1
current_level = bg_images

# Flag to track if the player is at the lighthouse entrance door
at_lighthouse_entrance_door = False
at_ladder = False

# Resets the player's position
def reset_player_position():
    # Set the player's x position to be outside
    if is_level_1:
        player.rect.x = 630 # ???
    elif is_level_2:
        # Set the player's x position to be inside the lighthouse
        player.rect.x = 20

# Function to switch between levels
def switch_level(new_level, new_scroll):
    global bird3, bird2, bird1, bird2_has_spawned, current_level, scroll, at_lighthouse_entrance_door, ground_image, ground_height, ground_width, is_level_1, is_level_2, left_scroll_limit, right_scroll_limit
    current_level = [new_level]
    # print("Switching levels...")
    # print(f"is_level_1: {is_level_1}, is_level_2: {is_level_2}")
    # print(f"new_level: {new_level}, new_scroll: {new_scroll}")

    if new_level == bg2_image:
        left_scroll_limit = -100
        right_scroll_limit = bg2_right_scroll_limit
        is_level_1 = False
        is_level_2 = True
        # print("Switching to level 2")
        ground_image = bg2_ground_image
        ground_height = bg2_ground_height
        ground_width = bg2_ground_width
        level_image = bg2_image
        at_lighthouse_entrance_door = False
        scroll = 0
        # print(f"is_level_1: {is_level_1}, is_level_2: {is_level_2}")
        # print(f"new_level: {new_level}, new_scroll: {new_scroll}")
        reset_player_position()
        # Reveals new birds
        bird2.rect.y = 10
        bird3.rect.y = 160
    else:
        scroll = 0#new_scroll
        left_scroll_limit = -100
        right_scroll_limit = bg1_right_scroll_limit
        is_level_1 = True
        is_level_2 = False
        current_level = bg_images
        at_lighthouse_entrance_door = False
        reset_player_position()

# Initializes the arrow position to "Yes" by default
arrow_position = "Yes"

# Function to display the custom prompt
def display_text_prompt():
    global display_prompt

    if display_prompt == True:
        # Create a custom dialogue box background
        prompt_bg = pygame.image.load("Prompt Images/tattered_prompt.png").convert_alpha()
        prompt_bg = pygame.transform.scale(prompt_bg, (400, 200))

        # Get the dimensions of the prompt_bg
        prompt_bg_width = prompt_bg.get_width()
        prompt_bg_height = prompt_bg.get_height()

        # Print or use the dimensions as needed
        #print("Dimensions of the drawn rectangle:", border_width, "x", border_height)
        #print("Dimensions of the prompt_bg:", prompt_bg_width, "x", prompt_bg_height)

        # Creates a custom font for the text
        prompt_font = pygame.font.Font(
            None, 24
        )  # You can adjust the font size as needed

        # Renders and displays the text on the dialogue box
        if is_level_1 and player.rect.x >= 615 and player.rect.x <= 650:
            prompt_text = prompt_font.render(
                "Do you want to enter the lighthouse?",
                True, (0, 0, 0)
            )  # Text color (black)
        if is_level_2 and left_scroll_limit:
            prompt_text = prompt_font.render(
                "Do you want to exit the lighthouse? (Press ENTER to Exit)", True, (0, 0, 0)
            )  # Text color (black)

        # Positions the text in the center of the dialogue box
        text_rect = prompt_text.get_rect(center=(200, 50))

        # Displays the dialogue box with the text
        prompt_bg.blit(prompt_text, text_rect)

        # Creates a custom font for the selected option
        selected_option_font = pygame.font.Font(None, 36)

        # Loads the arrow image
        pointer_image = pygame.image.load('pointer.png') #Added
        pointer_image = pygame.transform.scale(pointer_image, (30, 30)) #Added

        # Defines text for "Yes" and "No" options with arrow
        text_yes = "Yes (ENTER key)"

        # Renders and displays the selected option with the arrow
        selected_text = selected_option_font.render(text_yes, True, (0, 0, 0))
        # Creates a new surface to combine the arrow image and text
        combined_surface = pygame.Surface((pointer_image.get_width() + selected_text.get_width(), max(pointer_image.get_height(), selected_text.get_height())))
        combined_surface.fill((255, 255, 255))  # Set the background color (white)
        combined_surface.blit(pointer_image, (0, 0))  # Blit the arrow image
        combined_surface.blit(selected_text, (pointer_image.get_width(), 0))
        # Positions the selected text
        selected_rect = selected_text.get_rect(
            center=(200, 110)
        )

        # Displays the selected and other options
        prompt_bg.blit(selected_text, selected_rect)

        # Calculates the position of the arrow based on the arrow_position
        arrow_x = 60

        # Blits the arrow image onto the prompt_bg
        prompt_bg.blit(pointer_image, (arrow_x, 95)) #Added
        screen.blit(prompt_bg, (150, 400))

# Initializes variables to track key states
left_key_pressed = False
right_key_pressed = False

# Creates the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Discover the Lighthouse")

# Title Menu
title_background_image = pygame.image.load("Menu/Title.png") 

# Game loop
title_menu = True
run = False
paused = False

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
    draw_bg(current_level)
    draw_ground()
    
    # Handles user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False
            # Added for ingame menu =====================
            if event.key == pygame.K_p:
                print("GAME PAUSED")
                paused = pauseMenu.display_pause_menu(screen, False)  # Call the pause menu function
            # ===========================================
            if (player.alive):
                if event.key == pygame.K_LEFT:
                    new_position_x = player.rect.x - PLAYER_SPEED
                    # Checks if the new position is within bounds, doesn't work sadly
                    if new_position_x >= 0:
                        player.go_left()
                elif event.key == pygame.K_RIGHT:
                    if player.rect.x < 700:
                        player.go_right()
                elif event.key == pygame.K_UP:
                    if at_ladder:
                        player.rect.y -= 15
                        player.climbing = True
                        player.update_climbing_animation2(True)
                    else:    
                        player.jump()
                elif event.key == pygame.K_DOWN:
                    if at_ladder:
                        player.rect.y += 15
                        player.update_climbing_animation2(True)     
                if event.key == pygame.K_SPACE:
                    player.punch = True    
                    if pygame.sprite.collide_rect(bird, player):
                        bird.take_damage()
                    if pygame.sprite.collide_rect(bird1, player):
                        bird1.take_damage()    
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.stop()   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False   
            elif event.key == pygame.K_RETURN:
                    if is_level_1 and at_lighthouse_entrance_door:
                        switch_level(bg2_image, 0)  # Switch to level 2
                        display_prompt = False  # Hide the prompt after switching levels
                        at_lighthouse_entrance_door = False                  

    key = pygame.key.get_pressed()

    # Updates the player
    player.update(is_level_2, at_ladder)
    if player.change_x != 0:
        if is_level_1:
            scroll -= (player.change_x * 5)
        else:
            scroll -= (player.change_x * 5)
    #if player.alive:         
        #print(f"Player X: {player.rect.x}, Player Y: {player.rect.y}, Change X: {player.change_x}, Scroll: {scroll}, Change Y: {player.change_y}") #*

    # Limits the scrolling to the size of the ground image
    scroll = max(min(0, scroll), SCREEN_WIDTH - ground_image.get_width())

    # Draws the background, clouds, and ground
    if is_level_1:
        screen.blit(bg_images[0], (scroll, 0))
        screen.blit(bg_images[1], (scroll * .25, 0))
        screen.blit(ground_image, (scroll, SCREEN_HEIGHT - ground_height))
    elif is_level_2:
        screen.blit(bg2_image, (scroll * 1.25, 0))
        screen.blit(bg2_ground_image, (scroll, SCREEN_HEIGHT - bg2_ground_height))
        
    # Checks if the player has been attacked recently
    if player.invulnerable and (pygame.time.get_ticks() - player.last_damage_time > player.invulnerability_duration):
        player.invulnerable = False

    # Checks for collisions between the birds and the player
    if (player.alive and bird.alive):
        if pygame.sprite.collide_rect(bird, player) and not player.invulnerable:
            player.take_damage()
            current_health = player.health
    if (player.alive and bird1.alive):
        if pygame.sprite.collide_rect(bird1, player) and not player.invulnerable:
            player.take_damage()
            current_health = player.health 
    if (player.alive and bird2.alive):
        if pygame.sprite.collide_rect(bird2, player) and not player.invulnerable:
            player.take_damage()
            current_health = player.health     
    if (player.alive and bird3.alive):
        if pygame.sprite.collide_rect(bird3, player) and not player.invulnerable:
            player.take_damage()
            current_health = player.health          

    # Checks for win condition
    if (player.alive and player.rect.y < -200 and is_level_2):
        run = winScreen.display_winning_screen(screen, paused, run)

    # Checks for loss condition
    if current_health < 1:
        run = loseScreen.display_losing_screen(screen, paused, run)

    # Draws the health bar
    for i in range(max_health):
        if i < current_health:
            screen.blit(heart_image, (10 + i * 40, SCREEN_HEIGHT - 40))
        else:
            screen.blit(empty_heart_image, (10 + i * 40, SCREEN_HEIGHT - 40))

    # Updates the birds
    # Outside birds
    if bird.alive:
        bird.update()
        bird.detect_player_proximity(player)
        if is_level_1:
            if bird.rect.x > 1000:
                bird.change_direction()
            if bird.rect.x < -200:
                bird.change_direction()  
        elif is_level_2:
            if not bird2_has_spawned:
                bird.die()
                bird1.die()
    if bird1.alive:
        bird1.update()
        bird1.detect_player_proximity(player)
        if is_level_1:
            if bird1.rect.x > 1000:
                bird1.change_direction()
            if bird1.rect.x < -200:
                bird1.change_direction()  
    # Inside birds
    if bird2.alive:
        bird2.update()
        bird2.velocity_x = 8
        if bird2.rect.x > 700:
            bird2.change_direction()
        if bird2.rect.x < 0:
            bird2.change_direction() 
    if bird3.alive:
        bird3.update()
        bird3.velocity_x = 6
        if bird3.rect.x > 700:
            bird3.change_direction()
        if bird3.rect.x < 0:
            bird3.change_direction()         

    # Draws the player and birds
    screen.blit(player.image, player.rect)
    if bird.alive:
        screen.blit(bird.image, bird.rect)
    if bird1.alive:
        screen.blit(bird1.image, bird1.rect)     
    if bird2.alive:
        screen.blit(bird2.image, bird2.rect)    
    if bird3.alive:
        screen.blit(bird3.image, bird3.rect)    

    # Checks if player is at the the front door of the lighthouse
    if is_level_1:
        if player.rect.x >= 615 and player.rect.x <= 650:
            at_lighthouse_entrance_door = True
            #print("At Lighthouse door: player.rect.x == ")
            #print(player.rect.x)
            display_text_prompt()
            display_prompt = True  # Set the display_prompt flag to True to show the prompt
        else:
            display_prompt = False  # Set the display_prompt flag to False if not at the specific x position

    # Checks if player is at the ladder
    if is_level_2:
        if player.rect.x >= 355 and player.rect.x <= 375:
            if player.alive:
                at_ladder = True
        else:
            at_ladder = False

    # Draws the prompt if the flag is set
    if display_prompt:
        display_text_prompt()

    # Updates display    
    pygame.display.update()

# ========================
# Section 8: Cleanup and Quit
# ========================
pygame.quit()
