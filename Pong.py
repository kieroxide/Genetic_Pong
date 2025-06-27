from Canvas import Canvas
import pygame
from GA import *
import random
import math

class Pong:
    def __init__(self, drawn = True, net = None, maxFrames = 500, gen = None):
        self.WIDTH = 600
        self.HEIGHT = 600
        self.gen = gen
        self.score = 0
        self.frames_survived = 0
        self.maxFrames = maxFrames
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        if(drawn):
            self.canvas = Canvas(drawn=drawn, width=self.WIDTH, height=self.HEIGHT)
            self.score_text = self.canvas.font.render(f"Score: {self.score}", True, self.WHITE)
            self.gen_text = self.canvas.font.render(f"Generation: {self.gen}", True, self.WHITE)
        self.paddle = None
        self.ball = None
        self.drawn = drawn
        self.net = net
        self.paddle_speed = 8

        #ball
        self.max_speed = 20
        self.velocity = [6,3]



        self.running = True
    
    def start(self):
        self.setup()
        self.game_loop()
        return self.frames_survived, self.score

    def setup(self):
        self.ball = pygame.Rect(400, 300, 15, 15)
        self.ball.x = random.randint(300, 500)
        self.ball.y = random.randint(100, 500)

        angle = random.choice([45, 315])
        r = math.radians(angle)
        self.velocity = [self.max_speed * math.cos(r), self.max_speed * math.sin(r)]

        self.paddle = pygame.Rect(30, 200, 10, 100)

    def quitCheck(self):
        #Allows to quit using window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def controlsCheck(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.paddle.y -= self.paddle_speed
        if keys[pygame.K_s]:
            self.paddle.y += self.paddle_speed  

        # Clamp paddle inside window
        if self.paddle.top < 0:
                self.paddle.top = 0
        if self.paddle.bottom > 600:
            self.paddle.bottom = 600

    def collision_detection(self):
        if(self.paddle.colliderect(self.ball)):
            self.ball.left = self.paddle.right
            self.velocity[0] = -self.velocity[0]
            self.score += 5
            if self.drawn:
                self.score_text = self.canvas.font.render(f"Score: {self.score}", True, self.WHITE)
    
    def boundary_detection(self):
        if(self.ball.top < 0 or self.ball.bottom > self.HEIGHT):
            self.velocity[1] = -self.velocity[1]
        if(self.ball.left < 0 or self.ball.right > self.WIDTH):
            self.velocity[0] = -self.velocity[0]
    
    def update(self):
        self.ball.x += self.velocity[0]
        self.ball.y += self.velocity[1]

    def draw(self):
        #Clears, Draws objects, then updates display
        self.canvas.screen.fill(self.BLACK)
        self.canvas.screen.blit(self.score_text,(self.canvas.WIDTH/2 , 10))
        self.canvas.screen.blit(self.gen_text,(self.canvas.WIDTH/2 , 40))

        pygame.draw.rect(self.canvas.screen, self.WHITE, self.paddle)
        pygame.draw.rect(self.canvas.screen, self.WHITE, self.ball)

        pygame.display.flip()

    def game_loop(self):
        self.running = True
        while self.running:
            if(self.drawn):
                self.quitCheck()
            GA(self, self.net)
            #self.controlsCheck()

            self.boundary_detection()
            self.collision_detection()

            self.update()
            if(self.drawn):
                self.draw()
            if(self.frames_survived == self.maxFrames):
                self.running = False
            if(self.ball.left <= 0):
                self.score -= 20
                self.running = False
            self.frames_survived += 1
            if(self.drawn):
                self.canvas.clock.tick(60)