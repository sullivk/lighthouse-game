import pygame
import os

def display_pause_menu(screen, paused, run):
    paused = True
    is_controls = False

    try:
        pause_bg = pygame.image.load("Prompt Images/resized_pause_menu_bg.png").convert_alpha()
    except pygame.error as e:
        print(f"Error loading image: {e}")

    button_width, button_height = 200, 50

    quit_game_button_rect = pygame.Rect(screen.get_width() // 2 - button_width // 2, 290, button_width, button_height)

    buttons = [
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
                        paused = handle_button_click(button)
    
        # Check if the mouse is over any button and set cursor accordingly
        for button in buttons:
            if button["rect"].collidepoint(pygame.mouse.get_pos()):
                button["hovered"] = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                button["hovered"] = False

        
        # Draw your pause menu elements here
        screen.fill((0, 0, 0))
        # Add your pause menu elements (text, buttons, etc.)
        
        # Add "Game Paused" text
        image_rect = pause_bg.get_rect(center=(screen.get_width() // 2, 300))
        screen.blit(pause_bg, image_rect)

        font = pygame.font.Font(None, 60)
        font2 = pygame.font.Font(None, 24)
        text = font.render("You Won!", True, (255, 255, 255))  # Red color
        text2 = font2.render("You did made it to", True, (0, 0, 0))
        text3 = font2.render("the top of the lighthouse!", True, (0, 0, 0))  # Red color

        text_rect = text.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(text, text_rect)

        text2_rect = text2.get_rect(center=(screen.get_width() // 2, 245))
        screen.blit(text2, text2_rect)
        text3_rect = text3.get_rect(center=(screen.get_width() // 2, 265))
        screen.blit(text3, text3_rect)

        
        # Draw buttons with hover effect
        for button in buttons:
           draw_button(screen, button["text"], button["rect"], button["clicked"], button["hovered"])
        
        pygame.display.update()

        # Add your pause menu logic (e.g., button clicks, resume game, etc.)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:  # Quit game
            pygame.quit()
            quit()

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

    pygame.draw.rect(screen, border_color, rect, border_radius=5, width=3)  # Draw button border

    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    
def handle_button_click(button):
    if button["text"] == "Quit Game":
        pygame.quit()
        quit()

