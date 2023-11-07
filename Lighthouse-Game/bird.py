import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, position):
        #super().__init__()
        self.sheet = pygame.image.load("seagull.png")
        
        #defines area of a single sprite of an image
        self.sheet.set_clip(pygame.Rect(50, 0, 255, 273))
        
        #loads spritesheet images
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        
        #position image in the screen surface
        self.rect.topleft = position
        
        #variable for looping the frame sequence
        self.frame = 0
        
        self.rectWidth = 255
        self.rectHeight = 273

        self.down_states = { 0: (50, 32, self.rectWidth, self.rectHeight),
                            1: (350, 32, self.rectWidth, self.rectHeight)
                             
                             
                              }     
            
        self.up_states = { 0: (50, 32, self.rectWidth, self.rectHeight),
                          1: (350, 32, self.rectWidth, self.rectHeight)
                           
                           
                            }  
         
        self.right_states = { 0: (50, 32, self.rectWidth, self.rectHeight), 
                            1: (350, 32, self.rectWidth, self.rectHeight) 
                             
                             
                              }

        self.left_states = {  0: (50, 32, self.rectWidth, self.rectHeight), 
                            1: (350, 32, self.rectWidth, self.rectHeight),
                            2: (620, 32, self.rectWidth, self.rectHeight),
                            3: (920, 32, self.rectWidth, self.rectHeight),
                            4: (1220, 32, self.rectWidth, self.rectHeight), 
                            5: (1510, 32, self.rectWidth, self.rectHeight),
                            6: (50, 360, self.rectWidth, self.rectHeight),
                            7: (350, 360, self.rectWidth, self.rectHeight),
                            8: (620, 360, self.rectWidth, self.rectHeight),
                            9: (920, 360, self.rectWidth, self.rectHeight),
                            10: (1220, 360, self.rectWidth, self.rectHeight)
                                
                                
                                
                                    }
        
        self.rect.topleft = position
        self.velocity_x = 2
        self.direction = -1  # 1 for right, -1 for left
        #self.scroll = 0
        self.is_attacking = False
        self.frame_index = 0
        self.frame_delay = 100

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

    def change_direction(self):
        self.direction *= -1
        print("changed direction")

    def detect_player_proximity(self, player):
        if pygame.sprite.collide_rect(self, player):
            self.is_attacking = True

    def attack_player(self, player):
        if self.is_attacking:
            # Implement dive bomb
            if self.rect.x < player.rect.x:
                self.rect.x += self.velocity * 2
            else:
                self.is_attacking = False
