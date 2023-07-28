import pygame
import random 
class Ball():
    def __init__(self,x,y,radius,speed,color,height,width,screen):
        self.x = x
        self.y = y
        self.r = radius
        self.speed = speed
        self.color = color
        self.xFac = random.choice([-1,1])
        self.yFac = random.choice([-1,1])
        self.ball = pygame.draw.circle(screen, self.color, (self.x,self.y),self.r)
        self.firstTime = 1
        self.screen_height = height
        self.screen_width = width
        self.screen = screen

    def display(self):
        self.ball = pygame.draw.circle(self.screen, self.color, (self.x,self.y),self.r)
    
    def getplayer(self):
        return 0 if self.xFac==-1 else 1

    def hit(self,x):
        if x==1:
            self.xFac *= -1
        else:
            self.yFac *=-1
        self.speed+=0.1

    def update(self):
        self.x += self.speed*self.xFac
        self.y += self.speed*self.yFac
        
        # font20 = pygame.font.Font('freesansbold.ttf', 20)
        # text = font20.render(str(self.x)+",   "+str(self.y), True, (255,255,255))
        # textRect = text.get_rect()
        # textRect.center = (self.x, self.y)
        # self.screen.blit(text, textRect)
        if self.y <= 0 or self.y >= self.screen_height:
            self.yFac *= -1
  
        if self.x <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.x >= self.screen_width and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0
        
        

    def reset(self):
        self.x = self.screen_width//2
        self.y = self.screen_height//2
        self.xFac *= random.choice([-1,1])
        self.yFac *= random.choice([-1,1])
        self.firstTime = 1
        self.speed = 10

    def getRect(self):
        return self.ball
