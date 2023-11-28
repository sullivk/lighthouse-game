import pygame
import os

def display_pause_menu(screen):
    paused = True
    
    pause_bg = pygame.image.load("Prompt Images/resized_pause_menu_bg.png").convert_alpha()
    #pause_bg = pygame.transform.scale(pause_bg, (400, 200))
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Draw your pause menu elements here
        screen.fill((0, 0, 0))
        # Add your pause menu elements (text, buttons, etc.)
        
        # Add "Game Paused" text
        font = pygame.font.Font(None, 36)
        text = font.render("Game Paused", True, (255, 255, 255))  # White color
        text_rect = text.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(text, text_rect)
        
        image_rect = pause_bg.get_rect(center=(screen.get_width() // 2, 300))
        screen.blit(pause_bg, image_rect)

        pygame.display.update()

        # Add your pause menu logic (e.g., button clicks, resume game, etc.)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:  # Resume game
            paused = False
        elif keys[pygame.K_q]:  # Quit game
            pygame.quit()
            quit()

    return paused