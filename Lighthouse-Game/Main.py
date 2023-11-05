import pygame
import player 

pygame.init()

clock = pygame.time.Clock()

FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Midterm - Parallax Effect")


#define game variables
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

#draw background images 
def draw_bg():
    global scroll
    speed = 1
    for x in range(2):
        screen.blit(bg_images[x], (int(0 - scroll * speed * 0.25), 0))
        speed += 0.2
    for y in range(2,4):
        screen.blit(bg_images[y], (int(0 - scroll * speed * 0.5), SCREEN_HEIGHT * 0.5))

#draw background
def draw_ground():
	for x in range(5):	
		screen.blit(ground_image, (0, SCREEN_HEIGHT - ground_height))

player = player.Character((20, SCREEN_HEIGHT - ground_height - 250))

# Game loop
run = True
while run:
    clock.tick(FPS)
    
    draw_bg()
    draw_ground()
    
    # Input data. Left and right keys to create the parallax effect
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll > 0:
        scroll -= 5
    if key[pygame.K_RIGHT] and scroll < right_scroll_limit:
        scroll += 5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

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

    screen.blit(player.image, player.rect)
    
    pygame.display.update()

pygame.quit()
