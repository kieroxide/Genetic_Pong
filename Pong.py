"""Pong game implementation for AI training."""

from Canvas import Canvas
import pygame
from ai_controls import *
import random
import math

class Pong:
    """Pong game with AI paddle control."""
    
    def __init__(self, drawn = True, net = None, maxFrames = 500, gen = None):
        """Initialize Pong game with optional visualization."""
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

        #ball
        self.max_speed = 10
        self.velocity = [6,3]

        self.paddle_speed = self.max_speed * 0.5


        self.running = True
    
    def start(self):
        """Start game and return survival time and score."""
        self.setup()
        self.game_loop()
        return self.frames_survived, self.score

    def setup(self):
        """Initialize ball and paddle positions."""
        self.ball = pygame.Rect(400, 300, 15, 15)
        self.ball.x = random.randint(300, 500)
        self.ball.y = random.randint(100, 500)

        angle = random.choice([45, 315])
        r = math.radians(angle)
        self.velocity = [self.max_speed * math.cos(r), self.max_speed * math.sin(r)]

        self.paddle = pygame.Rect(30, 200, 10, 100)

    def quitCheck(self):
        """Check for quit events."""
        #Allows to quit using window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def controlsCheck(self):
        """Handle manual paddle controls (unused in AI mode)."""
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
        """Handle ball-paddle collisions with realistic physics."""
        if(self.paddle.colliderect(self.ball)):
            self.ball.left = self.paddle.right
            self.velocity[0] = -self.velocity[0]

            max_bounce_angle = math.radians(45)  # max angle from horizontal
            hit_pos = (self.ball.centery - self.paddle.centery) / (self.paddle.height / 2)
            speed = math.hypot(*self.velocity)

            # Clamp hit_pos to -1..1
            hit_pos = max(-1, min(1, hit_pos))

            # Calculate new angle: 0 is straight right, positive is upward
            angle = hit_pos * max_bounce_angle
            if abs(angle) < math.radians(5):  # or even 10
                angle = math.copysign(math.radians(10), angle if angle != 0 else random.choice([-1, 1]))

            # Update velocities with new angle, preserving speed
            self.velocity[0] = speed * math.cos(angle)
            self.velocity[1] = speed * math.sin(angle)
            self.score += 5
            if self.drawn:
                self.score_text = self.canvas.font.render(f"Score: {self.score}", True, self.WHITE)
    
    def boundary_detection(self):
        """Handle ball bouncing off walls."""
        if(self.ball.top < 0):
            self.velocity[1] = -self.velocity[1]
            self.ball.top = 0
        if(self.ball.bottom > self.HEIGHT):
            self.velocity[1] = -self.velocity[1]
            self.ball.bottom = self.HEIGHT
        if(self.ball.right > self.WIDTH):
            self.velocity[0] = -self.velocity[0]
            self.ball.right = self.WIDTH
    
    def update(self):
        """Update ball position."""
        self.ball.x += self.velocity[0]
        self.ball.y += self.velocity[1]

    def draw(self):
        """Render game objects to screen."""
        #Clears, Draws objects, then updates display
        self.canvas.screen.fill(self.BLACK)
        self.canvas.screen.blit(self.score_text,(self.canvas.WIDTH/2 , 10))
        self.canvas.screen.blit(self.gen_text,(self.canvas.WIDTH/2 , 40))

        pygame.draw.rect(self.canvas.screen, self.WHITE, self.paddle)
        pygame.draw.rect(self.canvas.screen, self.WHITE, self.ball)

        pygame.display.flip()

    def game_loop(self):
        """Main game loop."""
        self.running = True
        while self.running:
            if(self.drawn):
                self.quitCheck()
            ai_controls(self, self.net)
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