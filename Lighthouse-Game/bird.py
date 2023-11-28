import pygame
import math
import player

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Character(pygame.sprite.Sprite):
    def __init__(self, position):
        self.sheet = pygame.image.load("seagull-spritesheet.png")
        self.attack_sheet = pygame.image.load("seagull-attack.png")

        # Defines the area of a single sprite of an image
        self.sheet.set_clip(pygame.Rect(0, 0, 122, 112))
        
        # Loads the spritesheet images
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        
        # Positions the image in the screen surface
        self.rect.topleft = position
        
        # Defaults to false
        self.is_returning = False

        # Variable for looping the frame sequence
        self.frame = 0
        self.last_frame_time = pygame.time.get_ticks()
        
        # Spritesheet variables
        self.rectWidth = 122
        self.rectHeight = 112
        self.original_height = position[1]

        # Attack states
        self.down_states = { 0: (0, 0, self.rectWidth, self.rectHeight),
                            #1: (350, 32, self.rectWidth, self.rectHeight)
                             
                             
                              }     
            
        self.up_states = { 0: (0, 0, self.rectWidth, self.rectHeight),
                          #1: (350, 32, self.rectWidth, self.rectHeight)
                           
                           
                            }  
         
        # Right/left movement states 
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
        
        # Variables for the bird
        self.rect.topleft = position
        self.velocity_x = 2
        self.direction = -1  # 1 for right, -1 for left
        self.is_attacking = False
        self.frame_index = 0
        self.frame_delay = 16
        self.is_attacking = False
        self.attack_speed = 5
        self.attack_target = None
        self.alive = True
        self.health = 2

    #
    def get_frame(self, frame_set):
        # Loops through the sprite sequences
        self.frame += 1
        
        #if loop index is higher that the size of the frame return to the first frame 
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    #
    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    # Causes the bird to take damage
    def take_damage(self):
        if self.alive:
            self.health -= 1
            if self.health <= 0:
                self.die()

    # Causes the bird to die
    def die(self):
        self.alive = False
        #self.kill()
        #self.stop()
        #self.image = pygame.transform.rotate(self.sheet.subsurface(self.sheet.get_clip()), 270)
        print("rip birdo")
        print("rip birdo")
        print("rip birdo")

    # Updates the bird
    def update(self):
        if self.alive:
            if not self.is_attacking:
                current_time = pygame.time.get_ticks()
                # Moves the bird right/left
                self.rect.x += self.velocity_x * self.direction
                if self.direction == 1:
                    self.current_states = self.right_states
                else:
                    self.current_states = self.left_states

                # Loops through the sprite sequences

                # self.frame_index += 1
                # if self.frame_index >= len(self.current_states):
                #     self.frame_index = 0
                # self.image = self.sheet.subsurface(self.current_states[self.frame_index])

                # self.current_states = self.right_states if self.direction == 1 else self.left_states
                # self.frame_index = (self.frame_index + 1) % len(self.current_states)
                # self.image = self.sheet.subsurface(self.current_states[self.frame_index])   
                
                if current_time - self.last_frame_time > self.frame_delay:
                    self.frame_index = (self.frame_index + 1) % len(self.current_states)
                    self.image = self.sheet.subsurface(self.current_states[self.frame_index])
                    self.last_frame_time = current_time 

            else:
                # Attacks the player
                if (player.Character.alive):
                    self.attack_player()
                else:
                    self.is_attacking = False
                    self.is_returning = False   

    # Changes the horizontal direction of the bird
    def change_direction(self):
        if self.rect.x <= 0 or self.rect.x + self.rect.width >= SCREEN_WIDTH:
            self.direction *= -1

    # Detects how close the bird is to the player
    def detect_player_proximity(self, player):
        # if not player.alive:
        #     return
        player_x, player_y = player.rect.center
        bird_x, bird_y = self.rect.center
        
        dx = player_x - bird_x
        dy = player_y - bird_y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        attack_threshold = 400 

        if distance < attack_threshold:
            self.is_attacking = True
            self.attack_target = player

    # Attacks the player if the bird gets close
    def attack_player(self):
        if not player.Character.alive:
            return
        self.current_states = self.right_states if self.direction == 1 else self.left_states
        self.frame_index = (self.frame_index + 1) % len(self.current_states)
        self.image = self.sheet.subsurface(self.current_states[self.frame_index]) 
        if self.is_attacking and self.attack_target:
            player_x, player_y = self.attack_target.rect.center
            seagull_x, seagull_y = self.rect.center

            # Calculates the direction vector from the seagull to the player
            dx = player_x - seagull_x
            dy = player_y - seagull_y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            # Updates the bird's direction based on the player's position
            if dx > 0:
                # right
                self.direction = 1
            else:
                # left
                self.direction = -1

            # Normalizes the direction vector
            if distance > 0:
                dx /= distance
                dy /= distance

            # Distance between bird and player
            if distance < 50:
                self.is_returning = True

            # Adjusts the seagull's position
            if not self.is_returning:
                # Dives towards the player
                self.rect.x += dx * self.attack_speed
                self.rect.y += dy * self.attack_speed
            else:
                # Returns to original flying height
                self.rect.y -= self.attack_speed
                if self.rect.y <= self.original_height:
                    self.rect.y = self.original_height
                    self.is_attacking = False
                    self.is_returning = False
                    