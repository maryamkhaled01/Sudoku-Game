import pygame
from Constants import *

class Button():
    def __init__(self,x,y,image,scale):
        self.x = x
        self.y = y
        width = image.get_width()
        height = image.get_height()

        self.width = int(width*scale)
        self.height = int(height*scale)

        self.image = pygame.transform.scale(image, (self.width , self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self,screen):
        action = False
        pos = pygame.mouse.get_pos()
        #print("HII") 
        if self.rect.collidepoint(pos):
            pygame.draw.rect(screen, BLACK, (self.x-10,self.y-10,self.width+20,self.height+20), 50)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image,(self.rect.x, self.rect.y))
        return action