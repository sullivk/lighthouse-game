# -*- coding: utf-8 -*-

import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Character(pygame.sprite.Sprite):
    def __init__(self, position, ground_width):
        # Loads the image
        self.sheet = pygame.image.load("spritesheet1.png")
        
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

        # Jump info
        self.is_jumping = False
        self.jump_count = 10
        self.ground_level = 600 - 135 - 250

        # Up/down states
        self.down_states = { 0: (35, 602, self.rectWidth, self.rectHeight) }     
        
        self.up_states = { 0: (35, 602, self.rectWidth, self.rectHeight) }  
         
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

    # Updates the player
    # def update(self, direction):
    #     self.calculate_gravity()
    #     if self.is_jumping:
    #         # Handle jumping
    #         self.change_y += 0.35
    #         if self.rect.y >= self.ground_level:
    #             self.is_jumping = False
    #             self.change_y = 0
    #             self.rect.y = self.ground_level
 
    #     # Moves left/right
    #     self.rect.x += self.change_x
 
    #     if self.change_x > 0:
    #         self.clip(self.right_states)
    #     elif self.change_x < 0:
    #         self.clip(self.left_states)
 
    #     # Moves up/down
    #     self.rect.y += self.change_y
 
    #     self.image = self.sheet.subsurface(self.sheet.get_clip())
    def update(self, direction):
        # Calculate gravity effect
        self.calculate_gravity()

        # Handle jumping
        if self.is_jumping:
            self.change_y += 0.35
            if self.rect.y >= self.ground_level:
                self.is_jumping = False
                self.change_y = 0
                self.rect.y = self.ground_level

        # Update sprite position
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # Update the sprite image based on direction and ensure the animation frame rate is controlled
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time > self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.right_states)  # assuming right_states has the frames for animation
            self.last_frame_time = current_time
            if self.change_x > 0:
                self.clip(self.right_states)
            elif self.change_x < 0:
                self.clip(self.left_states)

            self.image = self.sheet.subsurface(self.sheet.get_clip())

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
        if (scroll < 6):
            self.clip(self.left_states)
            self.change_x = -1
        else:
            #self.stop()
            self.change_x = 0
 
    # Moves right
    def go_right(self, scroll):
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
