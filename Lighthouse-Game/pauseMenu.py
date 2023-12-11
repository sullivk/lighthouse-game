import pygame
import os

def display_pause_menu(screen, paused):
    paused = True
    is_controls = False

    try:
        pause_bg = pygame.image.load("Prompt Images/resized_pause_menu_bg.png").convert_alpha()
    except pygame.error as e:
        print(f"Error loading image: {e}")

    button_width, button_height = 200, 40

    resume_button_rect = pygame.Rect(screen.get_width() // 2 - button_width // 2, 150, button_width, button_height)
    controls_button_rect = pygame.Rect(screen.get_width() // 2 - button_width // 2, 200, button_width, button_height)
    quit_game_button_rect = pygame.Rect(screen.get_width() // 2 - button_width // 2, 250, button_width, button_height)

    buttons = [
        {"text": "Resume", "rect": resume_button_rect, "clicked": False},
        {"text": "Controls", "rect": controls_button_rect, "clicked": False},
        {"text": "Quit Game", "rect": quit_game_button_rect, "clicked": False}
    ]
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button in buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        button["clicked"] = True
                        draw_button(screen, button["text"], button["rect"], button["clicked"], button["hovered"])
                        paused = handle_button_click(button, screen, paused, is_controls)
    
        # Check if the mouse is over any button and set cursor accordingly
        for button in buttons:
            if button["rect"].collidepoint(pygame.mouse.get_pos()):
                button["hovered"] = True
                #pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                button["hovered"] = False

        
        # Draw your pause menu elements here
        screen.fill((0, 0, 0))
        # Add your pause menu elements (text, buttons, etc.)
        
        # Add "Game Paused" text
        font = pygame.font.Font(None, 36)
        text = font.render("Game Paused", True, (255, 255, 255))  # Black color
        text_rect = text.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(text, text_rect)
        
        image_rect = pause_bg.get_rect(center=(screen.get_width() // 2, 300))
        screen.blit(pause_bg, image_rect)
        
        # Draw buttons with hover effect
        for button in buttons:
           draw_button(screen, button["text"], button["rect"], button["clicked"], button["hovered"])
        
        pygame.display.update()

        # Add your pause menu logic (e.g., button clicks, resume game, etc.)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:  # Resume game
            #paused = False # WORKS
            paused = handle_button_click({"text": "Resume"}, screen, paused)
        elif keys[pygame.K_q]:  # Quit game
            pygame.quit()
            quit()
        elif keys[pygame.K_c]:  # Controls
            is_controls = True
            display_controls_menu(screen, is_controls);
        #elif keys[pygame.K_t]:  #Back To Title Screen

    return paused

def draw_button(screen, text, rect, clicked, hovered):
    #print("Hovered:", hovered) 
    border_color = (0, 0, 0)
    text_color = (0, 0, 0)  # Default text color black - DONT CHANGE
    
    if clicked:
        #print("Clicked:", clicked) 
        border_color = (50, 50, 50)  # Change color when clicked
        text_color = (255, 255, 255)  # Change color when clicked
    elif hovered:
        #print("Hovered:", hovered) 
        border_color = (255, 255, 255)  # Change border color when hovered
        text_color = (255, 255, 255) 

    pygame.draw.rect(screen, border_color, rect, 5)#border_radius=5, width=3)  # Draw button border

    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    
def handle_button_click(button, screen, paused, is_controls):
    # Handle button click logic
    if button["text"] == "Resume":
        paused = False
    elif button["text"] == "Controls":
        # Handle controls button click (e.g., show controls)
        is_controls = True
        display_controls_menu(screen, is_controls)
    elif button["text"] == "Quit Game":
        pygame.quit()
        quit()
    elif button["text"] == "Back":
        paused = display_pause_menu(screen)
        
    return paused
    
def display_controls_menu(screen, is_controls):
    controls_bg = pygame.image.load("Prompt Images/resized_pause_menu_bg.png").convert_alpha()

    button_width, button_height = 200, 40
    back_button_rect = pygame.Rect(screen.get_width() // 2 - button_width // 2, 150, button_width, button_height)

    back_button = {"text": "Back", "rect": back_button_rect, "clicked": False, "hovered": False}

    controls_info = [
        "Left Arrow Key - Move Left",
        "Right Arrow Key - Move Right",
        "Up Arrow Key - Jump/Climb",
        "Down Arrow Key - Move Down",
        "Right Arrow Key - Move Right",
        "Space Bar - Punch",
        "P Key - Pause Game",
        "R Key - Resume Game",
        "Q Key - Quit Game",
    ]

    # Draw buttons with hover effect
    draw_button(screen, back_button["text"], back_button["rect"], back_button["clicked"], back_button["hovered"])
    
    while is_controls:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if back_button["rect"].collidepoint(mouse_pos):
                    back_button["clicked"] = True
                    return
        
        # Check if the mouse is over the back button and set cursor accordingly
        if back_button["rect"].collidepoint(pygame.mouse.get_pos()):
            back_button["hovered"] = True
            #pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            back_button["hovered"] = False

        # Draw controls menu elements
        screen.fill((0, 0, 0))
        controls_bg = pygame.image.load("Prompt Images/resized_pause_menu_bg.png").convert_alpha()
        image_rect = controls_bg.get_rect(center=(screen.get_width() // 2, 300))
        screen.blit(controls_bg, image_rect)
        
        font = pygame.font.Font(None, 36)
        text = font.render("Controls", True, (255, 255, 255))  # White color
        text_rect = text.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(text, text_rect)

        # Draw controls information
        controls_font = pygame.font.Font(None, 24)
        controls_y_pos = 210
        for line in controls_info:
            controls_text = controls_font.render(line, True, (0, 0, 0))
            controls_text_rect = controls_text.get_rect(center=(screen.get_width() // 2, controls_y_pos))
            screen.blit(controls_text, controls_text_rect)
            controls_y_pos += 30
        
        # Draw back button
        draw_button(screen, back_button["text"], back_button["rect"], back_button["clicked"], back_button["hovered"])

        pygame.display.update()
