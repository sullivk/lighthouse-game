# -*- coding: utf-8 -*-

import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Character(pygame.sprite.Sprite):
    def __init__(self, position, ground_width):
        #load image
        self.sheet = pygame.image.load("spritesheet1.png")
        
        #defines area of a single sprite of an image
        self.sheet.set_clip(pygame.Rect(0, 0, 116, 211))
        
        #loads spritesheet images
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        
        #position image in the screen surface
        self.rect.topleft = position

        self.ground_width = ground_width

        #variable for looping the frame sequence
        self.frame = 0
        
        self.rectWidth = 114
        self.rectHeight = 211

        self.moving_right = False
        self.moving_left = False
        self.speed = 5
        self.change_x = 0
        self.change_y = 0

        # Jump info
        self.is_jumping = False
        self.jump_count = 10
        #self.ground_level = position[1]
        self.ground_level = 600 - 135 - 250

        self.down_states = { 0: (35, 602, self.rectWidth, self.rectHeight) }     
            
        self.up_states = { 0: (35, 602, self.rectWidth, self.rectHeight) }  
         
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

    # def update(self, direction):
    #     if direction == 'left':
    #         self.clip(self.left_states)
    #         #animate rect coordinates
    #         self.rect.x -= 5
    #     if direction == 'right':
    #         self.clip(self.right_states)
    #         self.rect.x += 5
    #     if direction == 'up':
    #         self.clip(self.up_states)
    #         #self.rect.y -= 5
    #     if direction == 'down':
    #         self.clip(self.down_states)
    #         #self.rect.y += 5
    #     # if self.is_jumping:
    #     #     if self.jump_count >= -10:
    #     #         neg = 1
    #     #         if self.jump_count < 0:
    #     #             neg = -1
    #     #         new_y = self.rect.y - (self.jump_count ** 2) * 0.5 * neg
    #     #         self.rect.y = new_y
    #     #         self.jump_count -= 1
    #     #     else:
    #     #         self.is_jumping = False
    #     #         self.jump_count = 10
    #     #         self.rect.y = self.ground_level

    #     if direction == 'stand_left':
    #         self.clip(self.left_states[0])
    #     if direction == 'stand_right':
    #         self.clip(self.right_states[0])
    #     if direction == 'stand_up':
    #         self.clip(self.up_states[0])
    #     if direction == 'stand_down':
    #         self.clip(self.down_states[0])

    #     self.image = self.sheet.subsurface(self.sheet.get_clip())

    def update(self, direction):
        """ Move the player. """
        # Gravity
        self.calc_grav()
        if self.is_jumping:
            # Handle jumping
            self.change_y += 0.35
            if self.rect.y >= self.ground_level:
                self.is_jumping = False
                self.change_y = 0
                self.rect.y = self.ground_level
 
        # Move left/right
        self.rect.x += self.change_x
 
        if self.change_x > 0:
            self.clip(self.right_states)
        elif self.change_x < 0:
            self.clip(self.left_states)

        # # See if we hit anything
        # block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        # for block in block_hit_list:
        #     # If we are moving right,
        #     # set our right side to the left side of the item we hit
        #     if self.change_x > 0:
        #         self.rect.right = block.rect.left
        #     elif self.change_x < 0:
        #         # Otherwise if we are moving left, do the opposite.
        #         self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # # Check and see if we hit anything
        # block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        # for block in block_hit_list:
 
        #     # Reset our position based on the top/bottom of the object.
        #     if self.change_y > 0:
        #         self.rect.bottom = block.rect.top
        #     elif self.change_y < 0:
        #         self.rect.top = block.rect.bottom
 
        #     # Stop our vertical movement
        #     self.change_y = 0
        self.image = self.sheet.subsurface(self.sheet.get_clip())
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - 100 - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - 100 - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
        if not self.is_jumping:
                    self.is_jumping = True
                    self.change_y = -10
 
    # Player-controlled movement:
    def go_left(self, scroll):
        """ Called when the user hits the left arrow. """
        self.clip(self.left_states)
        self.change_x = -1
 
    def go_right(self, scroll):
        """ Called when the user hits the right arrow. """
        self.clip(self.right_states)
        self.change_x = 1
    # def go_left(self, scroll):
    #     """ Called when the user hits the left arrow. """
    #     # Prevent moving left if at the left edge
    #     if self.rect.x + scroll > 0:
    #         self.change_x = -1
    #     else:
    #         self.change_x = 0

    # def go_right(self, scroll):
    #     """ Called when the user hits the right arrow. """
    #     # Prevent moving right if at the right edge
    #     if self.rect.x + scroll < self.ground_width - self.rect.width:
    #         self.change_x = 1
    #     else:
    #         self.change_x = 0

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

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
