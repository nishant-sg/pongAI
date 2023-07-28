import pygame
import neat
import os
import pickle
from paddle import Paddle
from ball import Ball
pygame.init()
WIDTH, HEIGHT = 900, 600
clock = pygame.time.Clock()    
FPS = 30
WHITE = (0, 0, 0)
BLACK = (245,245,245)
GREY = (169,169,169)
GREEN = (0, 255, 0)
    

class Game():
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.paddle1 = Paddle(20, 0, 10, 100, 10, GREY,HEIGHT,WIDTH,self.screen)
        self.paddle2 = Paddle(WIDTH-30, 0, 10, 100, 10, GREY,HEIGHT,WIDTH,self.screen)  
        self.ball = Ball(WIDTH//2, HEIGHT//2, 10, 10, GREY,HEIGHT,WIDTH,self.screen)
        self.score1 = 0
        self.score2 = 0
        self.hits1 = 0
        self.hits2 = 0
        self.lastplayer = self.ball.getplayer()

    def run(self):
        running = True
        p1yfac,p2yfac = 0,0
        while running:
            # print("running")
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_o:
                        p2yfac = -1
                    if event.key == pygame.K_l:
                        p2yfac = 1
                    if event.key == pygame.K_w:
                        p1yfac = -1
                    if event.key == pygame.K_s:
                        p1yfac = 1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_o or event.key == pygame.K_l:
                        p2yfac = 0
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        p1yfac = 0
            # pygame.key.set_repeat(10,10)
            # self.paddle2.automate(self.ball)
            self.loop(p1yfac,p2yfac)
            self.draw()
            self.draw_score()
            pygame.display.update()
            clock.tick(FPS)   

    def loop(self,p1yfac,p2yfac):
        self.screen.fill(WHITE)
        players = [self.paddle1,self.paddle2]
        self.paddle1.update(p1yfac)
        self.paddle2.update(p2yfac)
        for player in players:
            if pygame.Rect.colliderect(self.ball.getRect(), player.getRect()):
                if (self.ball.y>player.y or self.ball.y==player.y) and (self.ball.y<player.y + player.h or self.ball.y==player.y + player.h) :
                    if self.ball.x>WIDTH//2 and self.lastplayer==1:
                        self.hits2+=1
                        self.ball.hit(1)
                        self.lastplayer = 0
                    elif self.ball.x<WIDTH//2 and self.lastplayer==0:
                        self.hits1+=1
                        self.ball.hit(1)
                        self.lastplayer=1
                else:
                    self.ball.hit(0)
    
        point = self.ball.update()

        if point == -1:
            self.score1 += 1

        elif point == 1:
            self.score2 += 1
    
        if point:   
            self.reset()    
    
    def debug(self):
        run = True
        window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PONG AI")
        
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            window.fill(WHITE)
            # self.draw()
            self.paddle1.display(window)
            self.paddle2.display(window)
            pygame.display.update()
            clock.tick(FPS)   

    def draw(self):
        self.paddle1.display()
        self.paddle2.display()
        self.ball.display()

    def reset(self):
        self.paddle1.reset()
        self.paddle2.reset()
        self.ball.reset()
        self.lastplayer = self.ball.getplayer()

    def draw_score(self):
        self.paddle1.displayScore( self.score1, 100, 20, BLACK)
        self.paddle2.displayScore( self.score2, WIDTH-100, 20, BLACK)
        

    def draw_hits(self):
        self.paddle1.displayScore( self.hits1, 100, 20, BLACK)
        self.paddle2.displayScore( self.hits2, WIDTH-100, 20, BLACK)

    def test_ai(self,genome,config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            p1 = 0
            if keys[pygame.K_w]:
                p1 = -1
            if keys[pygame.K_s]:
                p1 = 1

            output = net.activate((self.paddle2.y, self.ball.y, abs(self.paddle2.x - self.ball.x)))
            decision = output.index(max(output))

            if decision == 0:
                p2 = 0
            elif decision == 1:
                p2 = 1
            else:
                p2 = -1

            self.loop(p1,p2)
            # self.paddle1.automate(self.ball)
            self.draw()
            self.draw_score()
            pygame.display.update()

        pygame.quit()

    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            output1 = net1.activate((self.paddle1.y, self.ball.y, abs(self.paddle1.x - self.ball.x)))
            output2 = net2.activate((self.paddle2.y, self.ball.y, abs(self.paddle2.x - self.ball.x)))
            # print(output1,output2)
            decision1 = output1.index(max(output1))
            if decision1==0:
                p1 = 0
            elif decision1 == 1:
                p1 = 1
            else:
                p1 = -1
            
            decision2 = output2.index(max(output2))
            if decision2==0:
                p2 = 0
            elif decision2 == 1:
                p2 = 1
            else:
                p2 = -1
            self.loop(p1,p2)
            self.draw()
            self.draw_hits()
            pygame.display.update()

            if self.score1 >= 1 or self.score2 >= 1 or self.hits1 > 50:
                self.calculate_fitness(genome1, genome2)
                break
    
    def train_ai_single(self, genome1, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            output1 = net1.activate((self.paddle1.y, self.ball.y, abs(self.paddle1.x - self.ball.x)))
            decision1 = output1.index(max(output1))
            if decision1==0:
                p1 = 0
            elif decision1 == 1:
                p1 = 1
            else:
                p1 = -1
            
            self.loop(p1,0)
            self.paddle2.automate(self.ball)
            self.draw()
            self.draw_score()
            pygame.display.update()

            if self.score1 >= 3 or self.score2 >= 3 or self.hits2 > 50:
                genome1.fitness += self.hits1
                break


    def calculate_fitness(self, genome1, genome2):
        genome1.fitness += self.hits1
        genome2.fitness += self.hits2
    
    def test_ai_single(self,genome,config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(240)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            output = net.activate((self.paddle1.y, self.ball.y, abs(self.paddle1.x - self.ball.x)))
            decision = output.index(max(output))

            if decision == 0:
                p1 = 0
            elif decision == 1:
                p1 = 1
            else:
                p1 = -1

            self.loop(p1,0)
            self.paddle2.automate(self.ball)
            self.draw()
            self.draw_score()
            pygame.display.update()
            # clock.tick(240)   

        pygame.quit()

def eval_genomes(genomes, config):

    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = Game()
            game.train_ai(genome1, genome2, config)

def eval_genomes_single(genomes, config):

    for i, (genome_id1, genome1) in enumerate(genomes):
        genome1.fitness = 0
        game = Game()
        game.train_ai_single(genome1, config)

def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-112')
    # p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    winner = p.run(eval_genomes, 50)
    with open("best.pickle", "wb") as f:
        print("saved best to pickle file \n")
        pickle.dump(winner, f)


def test_ai(config):

    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    game = Game()
    game.test_ai_single(winner, config)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    # run_neat(config)
    test_ai(config)

    # game = Game()
    # game.run()