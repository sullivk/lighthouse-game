import pygame
import sys

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

def display_pause_menu(screen, run, selected_option):
    
    
    # Create a semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)  # Adjust transparency (0-255)
    overlay.fill((0, 0, 0))  # Black overlay

    # Create a font for the pause menu text
    font = pygame.font.Font(None, 36)
    text = font.render("Game Paused", True, (255, 255, 255))  # White text
    options_font = pygame.font.Font(None, 24)

    # Display the overlay
    screen.blit(overlay, (0, 0))

    # Display "Game Paused" text
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(text, text_rect)

    # Display menu options
    options = ["Resume", "Settings", "Quit"]
    option_rects = []

    for i, option in enumerate(options):
        option_text = options_font.render(option, True, (255, 255, 255))
        option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40))
        screen.blit(option_text, option_rect)
        option_rects.append(option_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False  # Close the game
                elif event.key == pygame.K_DOWN:
                    # Move down the options
                    selected_index = option_rects.index(min(option_rects, key=lambda x: abs(x.centery - SCREEN_HEIGHT // 2)))
                    selected_index = (selected_index + 1) % len(option_rects)
                    option_rects = option_rects[selected_index:] + option_rects[:selected_index]
                elif event.key == pygame.K_UP:
                    # Move up the options
                    selected_index = option_rects.index(min(option_rects, key=lambda x: abs(x.centery - SCREEN_HEIGHT // 2)))
                    selected_index = (selected_index - 1) % len(option_rects)
                    option_rects = option_rects[selected_index:] + option_rects[:selected_index]
                elif event.key == pygame.K_RETURN:
                    # Execute the selected option
                    selected_option = options[option_rects.index(min(option_rects, key=lambda x: abs(x.centery - SCREEN_HEIGHT // 2)))]
                    if selected_option == "Resume":
                        run = True  # Resume the game
                        break  # Break out of the loop if "Resume" is selected
                    elif selected_option == "Settings":
                        print("Settings option selected")  # Add settings logic here
                    elif selected_option == "Quit":
                        pygame.quit()
                        sys.exit()

         # Highlight the selected option
        for i, rect in enumerate(option_rects):
            if i == option_rects.index(min(option_rects, key=lambda x: abs(x.centery - SCREEN_HEIGHT // 2))):
                pygame.draw.rect(screen, (255, 255, 255), rect, 2)

        pygame.display.flip()

        if run:
            break  # Break out of the loop if the game is resumed

    return run, selected_option