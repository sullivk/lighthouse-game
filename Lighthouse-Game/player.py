# -*- coding: utf-8 -*-

import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Character(pygame.sprite.Sprite):
    def __init__(self, position, ground_width):
        # Loads the image
        self.sheet = pygame.image.load("spritesheet1.png")
        self.punch_bird_sheet = pygame.image.load("punch-bird.png")
        self.full_sheet = pygame.image.load("full-spritesheet.png")
        
        # Defines the area of a single sprite of an image
        self.sheet.set_clip(pygame.Rect(0, 0, 116, 211))
        
        # Loads the spritesheet images
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        
        # Positions the image in the screen surface
        self.rect.topleft = position

        # Sets the ground width
        self.ground_width = ground_width

        #variable for looping the frame sequence
        self.frame = 0
        
        # Spritesheet variables
        self.rectWidth = 114
        self.rectHeight = 211

        # Player variables
        self.moving_right = False
        self.moving_left = False
        self.speed = 5
        self.change_x = 0
        self.change_y = 0
        self.last_frame_time = pygame.time.get_ticks()
        self.frame_delay = 60
        self.frame_index = 0
        self.health = 5
        self.invulnerable = False
        self.invulnerability_duration = 3000
        self.last_damage_time = 0
        self.alive = True
        self.fall_speed = 1
        self.fallen_distance = 0
        self.fall_limit = 1
        self.punch = False
        self.punch_duration = 2000
        self.punch_time = 0
        self.facing_right = True

        # Jump info
        self.is_jumping = False
        self.jump_count = 10
        self.ground_level = 600 - 135 - 250

        # Up/down states
        self.down_states = { 0: (35, 602, self.rectWidth, self.rectHeight) }     
        
        self.up_states = { 0: (35, 602, self.rectWidth, self.rectHeight) }  
         
        # Right/left punch states
        self.punch_right_states = { 0: (0, 426, self.rectWidth, self.rectHeight) }     
        
        self.punch_left_states = { 0: (119, 426, self.rectWidth, self.rectHeight) }  

        # Dead states
        self.dead_left = { 0: (186, 6856, self.rectWidth, self.rectHeight) }     
        
        self.dead_right = { 0: (0, 856, self.rectWidth, self.rectHeight) }  

        # Right/left states 
        self.right_states = { 0: (0, 0, self.rectWidth, self.rectHeight), 
                            1: (115, 0, self.rectWidth,  self.rectHeight), 
                            2: (236, 0, self.rectWidth,  self.rectHeight), 
                            3: (352, 0, self.rectWidth,  self.rectHeight),

                              }

        self.left_states = {  0: (0, 203, self.rectWidth, self.rectHeight), 
                            1: (125, 203, self.rectWidth,  self.rectHeight), 
                            2: (240, 203, self.rectWidth,  self.rectHeight), 
                            3: (350, 203, self.rectWidth,  self.rectHeight),
                            
                              }

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

    def update(self, direction):
        self.calculate_gravity()
        if not self.alive and self.rect.y >= self.ground_level:
            self.change_y = 0
            self.rect.y = self.ground_level + 200
            return
        else: 
            # Handles punching
            if self.punch:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_frame_time > self.frame_delay/10:
                    if self.facing_right:
                        self.frame_index = (self.frame_index + 1) % len(self.punch_right_states)
                        self.last_frame_time = current_time
                        self.image = self.punch_bird_sheet.subsurface(self.punch_right_states[self.frame_index])
                    else:
                        self.frame_index = (self.frame_index + 1) % len(self.punch_left_states)
                        self.last_frame_time = current_time
                        self.image = self.punch_bird_sheet.subsurface(self.punch_left_states[self.frame_index])    

                # Check if the punch duration has elapsed
                if current_time - self.punch_time > self.punch_duration:
                    self.punch = False

            elif self.change_x > 0:
                self.clip(self.right_states)
            elif self.change_x < 0:
                self.clip(self.left_states)
            
            # Handles jumping
            if self.is_jumping:
                self.change_y += 0.35
                if self.rect.y >= self.ground_level:
                    self.is_jumping = False
                    self.change_y = 0
                    self.rect.y = self.ground_level

            # Updates sprite position
            self.rect.x += self.change_x
            self.rect.y += self.change_y

            # Updates the sprite image based on direction and ensure the animation frame rate is controlled
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time > self.frame_delay:
                self.frame_index = (self.frame_index + 1) % len(self.right_states)
                self.last_frame_time = current_time
                if self.change_x > 0:
                    self.clip(self.right_states)
                elif self.change_x < 0:
                    self.clip(self.left_states)

                self.image = self.sheet.subsurface(self.sheet.get_clip())

    # Causes the player to take damage
    def take_damage(self):
        if self.health > 0 and not self.invulnerable:
            self.invulnerable = True
            self.health -= 1
            #print(self.health)
            self.last_damage_time = pygame.time.get_ticks()
            if self.health <= 0:
                self.die()

    # Causes the player to die
    def die(self):
        # Handles player death (menu stuff?)
        self.alive = False
        self.stop()
        #self.image = pygame.transform.rotate(self.sheet.subsurface(self.sheet.get_clip()), 270)
        if self.facing_right:
            self.full_sheet.set_clip(pygame.Rect(0, 0, 124, 190))
            self.image = self.full_sheet.subsurface(self.dead_right[0])
        else:
            self.full_sheet.set_clip(pygame.Rect(0, 0, 124, 190))
            self.image = self.full_sheet.subsurface(self.dead_left[0])
        print("rip bozo")
        print("rip bozo")
        print("rip bozo")

    # Causes the player to punch
    def punch(self):
        self.punch = True
        self.frame_index = 0
        self.punch_time = pygame.time.get_ticks()

        # Chooses the correct punch states based on the facing direction
        if self.facing_right:
            self.current_states = self.punch_right_states
        else:
            self.current_states = self.punch_left_states

    # Calculates gravity
    def calculate_gravity(self):
        # Calculates gravity
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # Makes sure the player hits the ground
        if self.rect.y >= SCREEN_HEIGHT - 100 - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - 100 - self.rect.height
 
    # Jumps
    def jump(self):
        if not self.is_jumping:
                    self.is_jumping = True
                    self.change_y = -10
 
    # Moves left
    def go_left(self, scroll):
        self.facing_right = False
        if (scroll < 6):
            self.clip(self.left_states)
            self.change_x = -1
        else:
            #self.stop()
            self.change_x = 0
 
    # Moves right
    def go_right(self, scroll):
        self.facing_right = True
        self.clip(self.right_states)
        self.change_x = 1

    # Stops movement
    def stop(self):
        self.change_x = 0

    # Handles keyboard input
    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                #self.rect.x -= self.speed
                #self.update('left')
                self.go_left()
            if event.key == pygame.K_RIGHT:
                #self.rect.x += self.speed
                #self.update('right')
                self.go_right() 
            if event.key == pygame.K_UP:
                self.update('up')
                if not self.is_jumping:
                    self.is_jumping = True
            if event.key == pygame.K_DOWN:
                self.update('down')

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.update('stand_left')
            if event.key == pygame.K_RIGHT:
                self.update('stand_right')
            if event.key == pygame.K_UP:
                self.update('stand_up')
            if event.key == pygame.K_DOWN:
                self.update('stand_down')
