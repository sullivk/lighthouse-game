import math
import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, position):
        #super().__init__()
        self.sheet = pygame.image.load("seagull-spritesheet.png")
        
        #defines area of a single sprite of an image
        self.sheet.set_clip(pygame.Rect(0, 0, 122, 112))
        
        #loads spritesheet images
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        
        #position image in the screen surface
        self.rect.topleft = position
        
        #variable for looping the frame sequence
        self.frame = 0
        
        self.rectWidth = 122
        self.rectHeight = 112
        self.original_height = position[1]

        self.down_states = { 0: (0, 0, self.rectWidth, self.rectHeight),
                            #1: (350, 32, self.rectWidth, self.rectHeight)
                             
                             
                              }     
            
        self.up_states = { 0: (0, 0, self.rectWidth, self.rectHeight),
                          #1: (350, 32, self.rectWidth, self.rectHeight)
                           
                           
                            }  
         
        self.right_states = { 0: (1582, 0, self.rectWidth, self.rectHeight), 
                            1: (1437, 0, self.rectWidth, self.rectHeight),
                            2: (1290, 0, self.rectWidth, self.rectHeight),
                            3: (1142, 0, self.rectWidth, self.rectHeight),
                            4: (997, 0, self.rectWidth, self.rectHeight),
                            5: (852, 6, self.rectWidth, self.rectHeight),
                            6: (1582, 170, self.rectWidth, self.rectHeight),
                            7: (1437, 170, self.rectWidth, self.rectHeight),
                            8: (1290, 170, self.rectWidth, self.rectHeight),
                            9: (1142, 170, self.rectWidth, self.rectHeight),
                            10: (997, 170, self.rectWidth, self.rectHeight)
                             
                              }

        self.left_states = {  0: (0, 0, self.rectWidth, self.rectHeight), 
                            1: (148, 0, self.rectWidth, self.rectHeight),
                            2: (298, 0, self.rectWidth, self.rectHeight),
                            3: (440, 0, self.rectWidth, self.rectHeight),
                            4: (585, 0, self.rectWidth, self.rectHeight),
                            5: (730, 12, self.rectWidth, self.rectHeight),
                            6: (0, 176, self.rectWidth, self.rectHeight),
                            7: (140, 176, self.rectWidth, self.rectHeight),
                            8: (285, 176, self.rectWidth, self.rectHeight),
                            9: (440, 176, self.rectWidth, self.rectHeight),
                            10: (585, 170, self.rectWidth, self.rectHeight) }
        
        self.rect.topleft = position
        self.velocity_x = 2
        self.direction = -1  # 1 for right, -1 for left
        #self.scroll = 0
        self.is_attacking = False
        self.frame_index = 0
        self.frame_delay = 100

        #attack stuff
        self.is_attacking = False
        self.attack_speed = 5
        self.attack_target = None

    def get_frame(self, frame_set):
        #looping the sprite sequences.
        self.frame += 1
        
        #if loop index is higher that the size of the frame return to the first frame 
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        #print(frame_set[self.frame])
        return frame_set[self.frame]

    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    def update(self):
        if not self.is_attacking:
            # Implement moving right to left
            self.rect.x += self.velocity_x * self.direction

            if self.direction == 1:
                self.current_states = self.right_states
            else:
                self.current_states = self.left_states

            self.frame_index += 1
            if self.frame_index >= len(self.current_states):
                self.frame_index = 0
            self.image = self.sheet.subsurface(self.current_states[self.frame_index])

        else:
            # Seagull is attacking
            self.attack_player()

    def change_direction(self):
        self.direction *= -1
        #print("Bird changed direction")

    def detect_player_proximity(self, player):
        player_x, player_y = player.rect.center
        bird_x, bird_y = self.rect.center
        
        # Adjust this threshold as needed to control when the bird attacks
        attack_threshold = 1
        
        if bird_y < player_y - attack_threshold:
            self.is_attacking = True
            self.attack_target = player
            print("Bird is above the player")

    def attack_player(self):
        if self.is_attacking and self.attack_target:
            player_x, player_y = self.attack_target.rect.center
            seagull_x, seagull_y = self.rect.center

            # Calculate the direction vector from the seagull to the player
            dx = player_x - seagull_x
            dy = player_y - seagull_y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            # Normalize the direction vector
            if distance > 0:
                dx /= distance
                dy /= distance

            # Adjust the seagull's position based on the direction vector
            self.rect.x += dx * self.attack_speed
            self.rect.y += dy * self.attack_speed

            # Check if the seagull has reached the player's position
            if abs(self.rect.x - player_x) < self.attack_speed and abs(self.rect.y - player_y) < self.attack_speed:
                self.is_attacking = False

            # Check if the seagull has returned to its original height
            if self.rect.y <= self.original_height:
                self.rect.y = self.original_height
                self.is_attacking = False
