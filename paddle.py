import pygame

class Paddle():
    def __init__(self,x,y,w,h,speed,color,height,width,screen):
        self.x = x
        self.w = w
        self.h = h
        self.y = height//2-h//2
        self.speed = speed
        self.color = color
        self.rect = pygame.Rect(x,y,w,h)
        self.screen_height = height
        self.screen_width = width
        self.screen = screen
        self.paddle = pygame.draw.rect(self.screen, self.color, self.rect)
    
    def display(self):
        # print("drawin")
        self.paddle = pygame.draw.rect(self.screen, self.color, self.rect)
    
    def displayScore(self,  score, x, y, color):
        font20 = pygame.font.Font('freesansbold.ttf', 20)
        text = font20.render(str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
        self.screen.blit(text, textRect)

    def update(self, yFac):
        self.y = self.y + self.speed*yFac
        # self.y-=self.h
        if self.y <= 0:
            self.y = 0
        elif self.y + self.h >= self.screen_height: 
            self.y = self.screen_height-self.h
        self.rect = (self.x, self.y, self.w, self.h)
        
        # font20 = pygame.font.Font('freesansbold.ttf', 20)
        # # text = font20.render(str(self.x)+","+str(self.y), True, (255,255,255))
        # text = font20.render(".",True, (255,255,255))
        # textRect = text.get_rect()
        # textRect.center = (self.x+self.w, self.y+self.h)
        # self.screen.blit(text, textRect)
        # textRect.center = (self.x+self.w, self.y)
        # self.screen.blit(text, textRect)
        # textRect.center = (self.x, self.y)
        # self.screen.blit(text, textRect)

        
    
    def automate(self,ball):
        # print(self.y)
        if self.y+(self.h//2)<ball.y:
            self.y = self.y+self.speed
        else:
            self.y = self.y-self.speed
        # elif ball.y<=self.h//2 and self.y>=self.h//2:
        #     self.y = self.y+ball.speed*ball.yFac
        # self.y-=self.h
        if self.y <= 0:
            self.y = 0
        elif self.y + self.h >= self.screen_height: 
            self.y = self.screen_height-self.h
        self.rect = (self.x, self.y, self.w, self.h)

    def reset(self):
        self.y = self.screen_height//2-self.h//2
        
    def getRect(self):
        return self.paddle
