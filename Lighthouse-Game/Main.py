import pygame
import player 
import bird

pygame.init()

clock = pygame.time.Clock()

FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lighthouse Game")


# Load background images
bg_images = []

for i in range(3):
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
    for y in range(2,3):
        screen.blit(bg_images[y], (int(0 - scroll * speed * 0.5), SCREEN_HEIGHT * 0.5))

#draw background
def draw_ground():
	for x in range(5):	
		screen.blit(ground_image, (0, SCREEN_HEIGHT - ground_height))

# Creates entities
player_start = (20, SCREEN_HEIGHT - ground_height + 300)
player = player.Character(player_start, ground_width)
bird = bird.Character((1000, 10))
PLAYER_SPEED = 6
scroll = 0

# Game loop
run = True
while run:
    clock.tick(FPS)
    
    draw_bg()
    draw_ground()
    
    # Input data. Left and right keys to create the parallax effect
    # key = pygame.key.get_pressed()
    # if key[pygame.K_LEFT] and scroll > 0:
    #     scroll -= 5
    # if key[pygame.K_RIGHT] and scroll < right_scroll_limit:
    #     scroll += 5
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         run = False
    # if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_ESCAPE:
    #             run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left(scroll)
            elif event.key == pygame.K_RIGHT:
                player.go_right(scroll)
            elif event.key == pygame.K_UP:
                player.jump()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.stop()   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False                 

    key = pygame.key.get_pressed()

    # if scroll > 0 and scroll < right_scroll_limit: 
    #     #player.handle_event(event)
    #     PLAYER_SPEED = 6
    # else: 
    #     end_screen = pygame.event.Event(pygame.KEYUP)
    #     if scroll == 0: 
    #         end_screen.key = pygame.K_RIGHT
    #     else:
    #         end_screen.key = pygame.K_LEFT
    #     player.handle_event(end_screen)

    player.update(player_start)
    if player.change_x != 0:
        scroll -= (player.change_x * 5)
    print(f"Player X: {player.rect.x}, Change X: {player.change_x}, Scroll: {scroll}")

    # #scroll = min(0, SCREEN_WIDTH // 2 - player.rect.centerx)
    # if player.change_x < 0 and player.rect.x < SCREEN_WIDTH // 2 and scroll < 0:
    #     #scroll += PLAYER_SPEED
    #     scroll += player.change_x
    # elif player.change_x > 0 and player.rect.x > SCREEN_WIDTH // 2 and scroll > right_scroll_limit:
    #     #scroll -= PLAYER_SPEED
    #     scroll -= player.change_x


    # if player.change_x < 0 and scroll < 0:
    #     scroll += PLAYER_SPEED
    # elif player.change_x > 0 and scroll > right_scroll_limit:
    #     scroll -= PLAYER_SPEED

    # # Limit scrolling to the size of the ground image
    scroll = max(min(0, scroll), SCREEN_WIDTH - ground_image.get_width())


    # if player.change_x < 0 and player.rect.centerx < SCREEN_WIDTH // 2:
    #     scroll = min(scroll + PLAYER_SPEED, 0)
    # elif player.change_x > 0 and player.rect.centerx > SCREEN_WIDTH // 2:
    #     scroll = max(scroll - PLAYER_SPEED, SCREEN_WIDTH - ground_image.get_width())


    # Draw the background, clouds, and ground at the new position
    screen.blit(bg_images[0], (scroll, 0))
    screen.blit(bg_images[1], (scroll * .25, 0))
    screen.blit(ground_image, (scroll, SCREEN_HEIGHT - ground_height))

    bird.update()
    bird.detect_player_proximity(player)
    #print(bird.rect.x)
    if bird.rect.x > 1000:
        bird.change_direction()
    if bird.rect.x < -200:
        bird.change_direction()
    screen.blit(bird.image, bird.rect)
    screen.blit(player.image, player.rect)
    
    pygame.display.update()

pygame.quit()
