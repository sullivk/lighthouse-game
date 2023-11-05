# -*- coding: utf-8 -*-

import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, position):
    
        #load image
        self.sheet = pygame.image.load("spritesheet2.png")
        
        #defines area of a single sprite of an image
        self.sheet.set_clip(pygame.Rect(0, 0, 200, 275))
        
        #loads spritesheet images
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        
        #position image in the screen surface
        self.rect.topleft = position
        
        #variable for looping the frame sequence
        self.frame = 0
        
        self.rectWidth = 200
        self.rectHeight = 275

        # Jump info
        self.is_jumping = False
        self.jump_count = 10
        #self.ground_level = position[1]
        self.ground_level = 600 - 135 - 250

        self.down_states = { 0: (35, 602, self.rectWidth, self.rectHeight) }     
            
        self.up_states = { 0: (35, 602, self.rectWidth, self.rectHeight) }  
        
         
        self.right_states = { 0: (35, 602, self.rectWidth, self.rectHeight), 
                            1: (0, 0, self.rectWidth,  self.rectHeight), 
                            2: (330, 0, self.rectWidth,  self.rectHeight), 
                            3: (660, 0, self.rectWidth,  self.rectHeight),
                            4: (990, 0, self.rectWidth,  self.rectHeight),
                            5: (1315, 0, self.rectWidth, self.rectHeight),
                            6: (1645, 0, self.rectWidth, self.rectHeight) }

        self.left_states = {  0: (256, 602, self.rectWidth, self.rectHeight), 
                            1: (0, 288, self.rectWidth,  self.rectHeight), 
                            2: (330, 288, self.rectWidth,  self.rectHeight), 
                            3: (660, 288, self.rectWidth,  self.rectHeight),
                            4: (990, 288, self.rectWidth,  self.rectHeight),
                            5: (1315, 288, self.rectWidth, self.rectHeight),
                            6: (1645, 288, self.rectWidth, self.rectHeight) }


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

    def update(self, direction):
        if direction == 'left':
            self.clip(self.left_states)
            #animate rect coordinates
            self.rect.x -= 5
        if direction == 'right':
            self.clip(self.right_states)
            self.rect.x += 5
        if direction == 'up':
            self.clip(self.up_states)
            #self.rect.y -= 5
        if direction == 'down':
            self.clip(self.down_states)
            #self.rect.y += 5
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                new_y = self.rect.y - (self.jump_count ** 2) * 0.5 * neg
                self.rect.y = new_y
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10
                self.rect.y = self.ground_level

        if direction == 'stand_left':
            self.clip(self.left_states[0])
        if direction == 'stand_right':
            self.clip(self.right_states[0])
        if direction == 'stand_up':
            self.clip(self.up_states[0])
        if direction == 'stand_down':
            self.clip(self.down_states[0])

        self.image = self.sheet.subsurface(self.sheet.get_clip())

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                self.update('left')
            if event.key == pygame.K_RIGHT:
                self.update('right')
            if event.key == pygame.K_UP:
                #self.update('up')
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
