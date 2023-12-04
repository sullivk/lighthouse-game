import pygame
import os

def display_pause_menu(screen):
    paused = True
    
    pause_bg = pygame.image.load("Prompt Images/resized_pause_menu_bg.png").convert_alpha()
    
    button_width, button_height = 200, 40

    resume_button_rect = pygame.Rect(screen.get_width() // 2 - button_width // 2, 150, button_width, button_height)
    settings_button_rect = pygame.Rect(screen.get_width() // 2 - button_width // 2, 200, button_width, button_height)
    quit_title_button_rect = pygame.Rect(screen.get_width() // 2 - button_width // 2, 250, button_width, button_height)
    quit_game_button_rect = pygame.Rect(screen.get_width() // 2 - button_width // 2, 300, button_width, button_height)
    
    buttons = [
        {"text": "Resume", "rect": resume_button_rect, "clicked": False, "hovered": False},
        #{"text": "Settings", "rect": settings_button_rect, "clicked": False, "hovered": False},
        #{"text": "Quit to Title", "rect": quit_title_button_rect, "clicked": False, "hovered": False},
        #{"text": "Quit Game", "rect": quit_game_button_rect, "clicked": False, "hovered": False}
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
                        handle_button_click(button, screen, paused)
    
        # Check if the mouse is over any button and set cursor accordingly
        for button in buttons:
            if button["rect"].collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                button["hovered"] = True
                draw_button(screen, button["text"], button["rect"], button["clicked"], button["hovered"])
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                button["hovered"] = False
                draw_button(screen, button["text"], button["rect"], button["clicked"], button["hovered"])

        # Draw your pause menu elements here
        screen.fill((0, 0, 0))
        # Add your pause menu elements (text, buttons, etc.)
        
        # Add "Game Paused" text
        font = pygame.font.Font(None, 36)
        text = font.render("Game Paused", True, (0, 0, 0))  # Black color
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
            paused = False
        elif keys[pygame.K_q]:  # Quit game
            pygame.quit()
            quit()
        elif keys[pygame.K_s]:  # Settings
            display_settings_menu(screen);
        #elif keys[pygame.K_t]:  #Back To Title Screen

    return paused

def draw_button(screen, text, rect, clicked, hovered):
    print("Hovered:", hovered) 
    border_color = (0, 0, 0)
    text_color = (0, 0, 0)  # Default text color black - DONT CHANGE
    
    if clicked:
        print("Clicked:", clicked) 
        border_color = (50, 50, 50)  # Change color when clicked
        text_color = (255, 255, 255)  # Change color when clicked
    elif hovered:
        print("Hovered:", hovered) 
        border_color = (255, 0, 0)  # Change border color when hovered
        text_color = (255, 0, 0) 

    pygame.draw.rect(screen, border_color, rect, border_radius=5, width=3)  # Draw button border

    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    
def handle_button_click(button, screen, paused):
    # Handle button click logic
    if button["text"] == "Resume":
        paused = False
    elif button["text"] == "Settings":
        # Handle Settings button click (e.g., show controls)
        display_settings_menu(screen)
    elif button["text"] == "Quit to Title":
        # Handle Quit to Title Screen button click
        # You may want to add logic to return to the title screen
        pass
    elif button["text"] == "Quit Game":
        pygame.quit()
        quit()
        
    return paused
    
def display_settings_menu(screen):
    # Add logic to display settings menu
    # For example, show controls and a back button
    pass
